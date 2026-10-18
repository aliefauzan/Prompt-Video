"""Punk collage / photocopy restyle, frame by frame.

usage: python punk.py <frames_dir> <masks_dir> <out_dir> [frame numbers...]
Frames are frame_001.png ... ; masks are person mattes with the same names.
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np

FRAMES, MASKS, OUT = sys.argv[1:4]
ONLY = [int(a) for a in sys.argv[4:]]
N = len([f for f in os.listdir(FRAMES) if f.endswith(".png")])

# BGR, 0..1
INK = np.array([0.07, 0.07, 0.075], np.float32)
PAPER = np.array([0.89, 0.93, 0.95], np.float32)
RED = np.array([0.13, 0.10, 0.84], np.float32)
MARKERS = {
    "orange": (0.08, 0.47, 1.0),
    "yellow": (0.05, 0.80, 1.0),
    "pink": (0.55, 0.16, 1.0),
}

# (first, last, background, star, handwriting, shapes, marker colour)
SECTIONS = [
    (1, 24, "env", True, False, False, "orange"),
    (25, 48, "black", True, True, False, "yellow"),
    (49, 72, "white", True, True, False, "pink"),
    (73, 96, "env", False, True, True, "yellow"),
    (97, 132, "black", True, True, False, "orange"),
    (133, 156, "white", False, True, True, "orange"),
    (157, 999, "black", True, True, False, "yellow"),
]
WORDS = ["LOUD", "no future", "RAW", "xx", "zine #3", "yeah!!", "punk", "nope", "AAA", "go go"]


def vnoise(rng, h, w, cell):
    """Smooth value noise in 0..1."""
    a = rng.random((max(2, h // cell + 2), max(2, w // cell + 2))).astype(np.float32)
    return cv2.resize(a, (w, h), interpolation=cv2.INTER_CUBIC).clip(0, 1)


def grain(rng, h, w, sigma=0.7):
    return cv2.GaussianBlur(rng.normal(0, 1, (h, w)).astype(np.float32), (0, 0), sigma)


def halftone_screen(h, w, cell, ox, oy):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    xx += ox
    yy += oy
    u = (xx + yy) / np.sqrt(2)
    v = (xx - yy) / np.sqrt(2)
    du = np.mod(u, cell) - cell / 2
    dv = np.mod(v, cell) - cell / 2
    return (np.sqrt(du * du + dv * dv) / (cell / np.sqrt(2))).clip(0, 1)


def xerox(gray, rng, lo, hi):
    """Gray uint8 -> photocopied tone 0..1."""
    h, w = gray.shape
    g = cv2.createCLAHE(clipLimit=2.4, tileGridSize=(8, 8)).apply(gray).astype(np.float32) / 255
    lo += rng.normal(0, 0.012)
    hi += rng.normal(0, 0.012)
    g = ((g - lo) / (hi - lo)).clip(0, 1)
    g = g * g * (3 - 2 * g)
    screen = halftone_screen(h, w, 7.0, rng.uniform(0, 7), rng.uniform(0, 7))
    ht = 1.0 - ((1.0 - g) > screen).astype(np.float32)
    mid = 4 * g * (1 - g)
    g = g * (1 - 0.65 * mid) + ht * 0.65 * mid
    g += grain(rng, h, w, 0.8) * 0.09
    patch = vnoise(rng, h, w, 140)
    g += np.clip(patch - 0.6, 0, 1) * 0.45 * (1 - g)          # uneven toner, broken blacks
    g -= np.clip(0.35 - patch, 0, 1) * 0.35 * g               # heavy toner patches
    sp = rng.random((h, w))
    g[sp < 0.0025] = 0.95
    g[sp > 0.998] = 0.03
    g = cv2.GaussianBlur(g.clip(0, 1), (0, 0), 0.6)            # slight ink spread
    return g


def tone_to_bgr(g):
    return INK + g[..., None] * (PAPER - INK)


def black_paper(rng, h, w):
    b = 0.055 + vnoise(rng, h, w, 220) * 0.035 + grain(rng, h, w, 0.6) * 0.02
    img = np.repeat(b[..., None], 3, 2).astype(np.float32)
    for _ in range(60):  # paper fibres
        x, y = rng.integers(0, w), rng.integers(0, h)
        a = rng.uniform(0, np.pi)
        L = rng.integers(6, 26)
        cv2.line(img, (x, y), (int(x + L * np.cos(a)), int(y + L * np.sin(a))),
                 (0.13, 0.13, 0.13), 1, cv2.LINE_AA)
    sp = rng.random((h, w))
    img[sp < 0.0012] = (0.55, 0.55, 0.55)
    img[sp > 0.99985] = (0.75, 0.45, 0.25)                      # tiny blue print artefacts
    return img


def white_paper(rng, h, w):
    dirt = vnoise(rng, h, w, 160)
    t = 0.97 - np.clip(dirt - 0.55, 0, 1) * 0.18 + grain(rng, h, w, 0.6) * 0.025
    img = PAPER[None, None, :] * t[..., None]
    sp = rng.random((h, w))
    img[sp < 0.0009] = (0.25, 0.25, 0.25)
    return img.astype(np.float32)


def red_paper_layer(rng, h, w):
    tex = 0.86 + vnoise(rng, h, w, 60) * 0.12 + grain(rng, h, w, 0.7) * 0.04
    img = RED[None, None, :] * tex[..., None]
    sp = rng.random((h, w))
    img[sp < 0.002] = (0.75, 0.75, 0.85)
    return img.astype(np.float32)


def rough_poly(pts, rng, amp, sub=6):
    """Subdivide a polygon and jitter it so it looks hand-cut."""
    out = []
    n = len(pts)
    for i in range(n):
        a, b = np.array(pts[i], np.float32), np.array(pts[(i + 1) % n], np.float32)
        d = b - a
        nrm = np.array([-d[1], d[0]]) / (np.linalg.norm(d) + 1e-6)
        for k in range(sub):
            p = a + d * (k / sub)
            if k:
                p = p + nrm * rng.normal(0, amp)
            out.append(p)
    return np.array(out, np.int32)


def star_points(cx, cy, R, rot, radii):
    pts = []
    for i in range(10):
        ang = rot + i * np.pi / 5 - np.pi / 2
        r = R * radii[i] * (1.0 if i % 2 == 0 else 0.42)
        pts.append((cx + r * np.cos(ang), cy + r * np.sin(ang)))
    return pts


def section_of(n):
    for i, s in enumerate(SECTIONS):
        if s[0] <= n <= s[1]:
            return i, s
    return len(SECTIONS) - 1, SECTIONS[-1]


def read_mask(n):
    return cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE)


def section_plan(si, sec, h, w):
    """Fixed collage pieces for one section; frames jitter around them."""
    rng = np.random.default_rng(500 + si * 31)
    mid = (sec[0] + min(sec[1], N)) // 2
    m = read_mask(mid) > 128
    ys, xs = np.nonzero(m)
    if len(xs):
        cx, top, bottom = np.median(xs), ys.min(), ys.max()
    else:
        cx, top, bottom = w / 2, h * 0.2, h
    plan = {}
    if sec[3]:
        R = np.clip((bottom - top) * 0.55, h * 0.32, h * 0.62)
        plan["star"] = dict(cx=cx + rng.normal(0, w * 0.04), cy=top + R * 0.75,
                            R=R, rot=rng.uniform(-0.25, 0.25),
                            radii=rng.uniform(0.86, 1.14, 10))
    if sec[5]:
        shapes = []
        for _ in range(4):
            kind = rng.choice(["rect", "tri", "x", "stripe", "arrow"])
            x, y = rng.uniform(0.05, 0.95) * w, rng.uniform(0.08, 0.92) * h
            s = rng.uniform(0.12, 0.26) * h
            a = rng.uniform(0, np.pi)
            shapes.append((kind, x, y, s, a))
        plan["shapes"] = shapes
    if sec[4]:
        marks = []
        for _ in range(rng.integers(4, 7)):
            kind = rng.choice(["word", "word", "loops", "underline", "cross", "arrowline"])
            marks.append(dict(kind=kind, x=rng.uniform(0.03, 0.8) * w, y=rng.uniform(0.1, 0.92) * h,
                              word=rng.choice(WORDS), scale=rng.uniform(2.6, 4.6),
                              ang=rng.uniform(-0.35, 0.35), L=rng.uniform(0.12, 0.3) * w,
                              th=int(rng.integers(5, 9)), seed=int(rng.integers(1e6))))
        plan["marks"] = marks
    return plan


def shape_poly(kind, x, y, s, a):
    c, sn = np.cos(a), np.sin(a)

    def tr(p):
        return [(x + px * c - py * sn, y + px * sn + py * c) for px, py in p]

    if kind == "rect":
        return [tr([(-s, -s * 0.55), (s, -s * 0.6), (s * 1.05, s * 0.5), (-s * 0.95, s * 0.58)])]
    if kind == "tri":
        return [tr([(0, -s), (s * 0.95, s * 0.7), (-s * 0.9, s * 0.75)])]
    if kind == "stripe":
        return [tr([(-s * 2.2, -s * 0.14), (s * 2.2, -s * 0.18), (s * 2.25, s * 0.14), (-s * 2.1, s * 0.17)])]
    if kind == "x":
        b = [(-s, -s * 0.16), (s, -s * 0.2), (s, s * 0.16), (-s, s * 0.2)]
        return [tr(b), tr([(py, px) for px, py in b])]
    if kind == "arrow":
        return [tr([(-s * 1.3, -s * 0.15), (s * 0.4, -s * 0.18), (s * 0.35, -s * 0.5), (s * 1.3, 0),
                    (s * 0.4, s * 0.52), (s * 0.42, s * 0.16), (-s * 1.3, s * 0.14)])]
    return []


def draw_marks(plan_marks, rng, h, w):
    """Red handwriting layer as alpha 0..1."""
    layer = np.zeros((h, w), np.uint8)
    for mk in plan_marks:
        if rng.random() < 0.1:               # strokes drop in and out between frames
            continue
        r = np.random.default_rng(mk["seed"])
        x, y = int(mk["x"] + rng.normal(0, 1.5)), int(mk["y"] + rng.normal(0, 1.5))
        th = mk["th"]
        if mk["kind"] == "word":
            tmp = np.zeros((h, w), np.uint8)
            word = "".join(ch.lower() if r.random() < 0.4 else ch for ch in mk["word"])
            cx = x
            for ch in word:                                     # letter by letter, uneven size and baseline
                sc = mk["scale"] * r.uniform(0.75, 1.25)
                cy = y + int(r.normal(0, 9))
                cv2.putText(tmp, ch, (cx, cy), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, sc, 255,
                            max(3, th + int(r.integers(-2, 3))), cv2.LINE_AA)
                (tw, _), _ = cv2.getTextSize(ch, cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, sc, th)
                cx += int(tw * r.uniform(0.7, 1.0))
            if r.random() < 0.5:                                # scratched-out letters
                cv2.line(tmp, (x - 10, y - 20), (cx + 10, y - 35 + int(r.normal(0, 15))), 255, th, cv2.LINE_AA)
            M = cv2.getRotationMatrix2D((x, y), np.degrees(mk["ang"]), 1.0)
            M[0, 1] += r.uniform(-0.35, 0.1)                     # hand slant
            layer = np.maximum(layer, cv2.warpAffine(tmp, M, (w, h)))
        elif mk["kind"] == "loops":
            t = np.linspace(0, 1, 260)
            k = r.integers(4, 8)
            px = x + t * mk["L"] + 38 * np.sin(t * k * 2 * np.pi)
            py = y + 50 * np.cos(t * k * 2 * np.pi) * (0.6 + 0.4 * np.sin(t * 3))
            cv2.polylines(layer, [np.stack([px, py], 1).astype(np.int32)], False, 255, th, cv2.LINE_AA)
        elif mk["kind"] == "underline":
            for j in range(2):
                t = np.linspace(0, 1, 40)
                px = x + t * mk["L"]
                py = y + j * 18 + 6 * np.sin(t * 5 + j) + t * 20 * mk["ang"]
                cv2.polylines(layer, [np.stack([px, py], 1).astype(np.int32)], False, 255, th, cv2.LINE_AA)
        elif mk["kind"] == "cross":
            s = int(mk["L"] * 0.35)
            cv2.line(layer, (x - s, y - s), (x + s, y + s + 10), 255, th + 2, cv2.LINE_AA)
            cv2.line(layer, (x + s, y - s + 8), (x - s + 6, y + s), 255, th + 2, cv2.LINE_AA)
        elif mk["kind"] == "arrowline":
            ex, ey = int(x + mk["L"] * np.cos(mk["ang"])), int(y + mk["L"] * np.sin(mk["ang"]))
            t = np.linspace(0, 1, 30)
            px = x + (ex - x) * t
            py = y + (ey - y) * t + 25 * np.sin(t * np.pi)
            cv2.polylines(layer, [np.stack([px, py], 1).astype(np.int32)], False, 255, th, cv2.LINE_AA)
            cv2.line(layer, (ex, ey), (ex - 45, ey - 30), 255, th, cv2.LINE_AA)
            cv2.line(layer, (ex, ey), (ex - 40, ey + 35), 255, th, cv2.LINE_AA)
    # wobble the whole layer so it reads as quick marker, not type
    dx = (vnoise(rng, h, w, 70) - 0.5) * 22 + (vnoise(rng, h, w, 13) - 0.5) * 9
    dy = (vnoise(rng, h, w, 70) - 0.5) * 22 + (vnoise(rng, h, w, 13) - 0.5) * 9
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    layer = cv2.remap(layer, xx + dx, yy + dy, cv2.INTER_LINEAR)
    a = layer.astype(np.float32) / 255
    a *= (0.78 + 0.22 * (rng.random((h, w)) > 0.18))           # dry-marker grain
    return a


def cutout(mask_u8, rng):
    m = cv2.GaussianBlur(mask_u8.astype(np.float32) / 255, (0, 0), 2.0)
    h, w = m.shape
    jag = (vnoise(rng, h, w, 22) - 0.5) * 0.35 + (vnoise(rng, h, w, 6) - 0.5) * 0.18
    cut = ((m + jag) > 0.5).astype(np.uint8)
    cut = cv2.morphologyEx(cut, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    n, lab, stats, _ = cv2.connectedComponentsWithStats(cut, 8)
    keep = np.zeros(n, bool)
    keep[1:] = stats[1:, cv2.CC_STAT_AREA] > 4000
    return keep[lab]


def marker_outline(region, rng, colour_name, h, w):
    """Rough, broken, offset marker line around a region. Returns {colour: alpha}."""
    grown = cv2.dilate(region.astype(np.uint8), np.ones((9, 9), np.uint8))
    contours, _ = cv2.findContours(grown, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    layers = {k: np.zeros((h, w), np.uint8) for k in MARKERS}
    off = rng.normal(0, 2.5, 2) + np.sign(rng.normal(0, 1, 2)) * 2.0     # registration error
    for c in contours:
        if len(c) < 200:
            continue
        p = c[:, 0, :].astype(np.float32)
        k = 15
        p = np.stack([np.convolve(np.r_[p[-k:, i], p[:, i], p[:k, i]], np.ones(k) / k, "same")[k:-k]
                      for i in range(2)], 1)[::4]
        p += off
        wob = np.cumsum(rng.normal(0, 0.6, (len(p), 2)), 0)
        wob -= wob.mean(0)
        p += np.clip(wob, -4, 4)
        edge = (p[:, 0] < 4) | (p[:, 0] > w - 5) | (p[:, 1] < 4) | (p[:, 1] > h - 5)
        i = 0
        while i < len(p):
            L = int(rng.integers(12, 40))
            seg = p[i:i + L + 1]
            seg_edge = edge[i:i + L + 1]
            i += L
            if rng.random() < 0.2 or seg_edge.any() or len(seg) < 3:
                continue
            col = colour_name if rng.random() > 0.15 else "pink"
            th = int(rng.integers(4, 10))
            cv2.polylines(layers[col], [seg.astype(np.int32)], False, 255, th, cv2.LINE_AA)
            if rng.random() < 0.3:                                # doubled line
                cv2.polylines(layers[col], [(seg + rng.normal(0, 3, 2)).astype(np.int32)], False, 255,
                              max(2, th - 3), cv2.LINE_AA)
    out = {}
    for k, l in layers.items():
        if l.any():
            a = l.astype(np.float32) / 255
            a *= (0.7 + 0.3 * vnoise(rng, h, w, 3)) * (rng.random((h, w)) > 0.12)
            out[k] = a
    return out


def over(dst, colour, alpha):
    a = alpha[..., None]
    return dst * (1 - a) + colour * a


def render(n):
    si, sec = section_of(n)
    _, _, bgmode, star, write, shapes, mcol = sec
    rng = np.random.default_rng(10_000 + n)
    bgr = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png"))
    h, w = bgr.shape[:2]
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    plan = section_plan(si, sec, h, w)

    # background
    if bgmode == "black":
        img = black_paper(rng, h, w)
    elif bgmode == "white":
        img = white_paper(rng, h, w)
    else:
        img = tone_to_bgr(xerox(gray, rng, 0.34, 0.72) * 0.72)

    # red paper graphics
    red = red_paper_layer(rng, h, w)
    red_a = np.zeros((h, w), np.uint8)
    if "star" in plan:
        s = plan["star"]
        pts = star_points(s["cx"] + rng.normal(0, 2), s["cy"] + rng.normal(0, 2), s["R"],
                          s["rot"] + rng.normal(0, 0.006), s["radii"])
        cv2.fillPoly(red_a, [rough_poly(pts, rng, s["R"] * 0.012)], 255, cv2.LINE_AA)
    for kind, x, y, sz, a in plan.get("shapes", []):
        for poly in shape_poly(kind, x + rng.normal(0, 2), y + rng.normal(0, 2), sz, a + rng.normal(0, 0.005)):
            cv2.fillPoly(red_a, [rough_poly(poly, rng, sz * 0.02)], 255, cv2.LINE_AA)
    if red_a.any():
        ra = red_a.astype(np.float32) / 255
        if bgmode != "black":                                       # paper shadow on light grounds
            sh = cv2.GaussianBlur(np.roll(ra, (5, 4), (0, 1)), (0, 0), 3) * 0.25
            img = over(img, np.zeros(3, np.float32), sh)
        img = over(img, red, ra)
    if "marks" in plan:
        img = over(img, RED * 0.95, draw_marks(plan["marks"], rng, h, w) * 0.92)

    # cut-out character with white paper rim
    cut = cutout(read_mask(n), rng)
    outside = (~cut).astype(np.uint8)
    dist = cv2.distanceTransform(outside, cv2.DIST_L2, 5)
    width = 2 + 13 * vnoise(np.random.default_rng(900 + si), h, w, 110) + (vnoise(rng, h, w, 30) - 0.5) * 4
    width *= vnoise(np.random.default_rng(901 + si), h, w, 160) > 0.22
    rim = (dist > 0) & (dist < width + (vnoise(rng, h, w, 5) - 0.5) * 2.5)
    region = cut | rim
    shadow = cv2.GaussianBlur(np.roll(region.astype(np.float32), (7, 5), (0, 1)), (0, 0), 4)
    img = over(img, np.zeros(3, np.float32), shadow * (0.55 if bgmode != "black" else 0.0))
    rim_col = PAPER[None, None, :] * (0.95 + grain(rng, h, w, 0.8)[..., None] * 0.03)
    img = np.where(rim[..., None], rim_col, img)
    char = tone_to_bgr(xerox(gray, rng, 0.18, 0.80))
    img = np.where(cut[..., None], char, img)

    # rough marker outline, offset from the rim
    for k, a in marker_outline(region, rng, mcol, h, w).items():
        img = over(img, np.array(MARKERS[k], np.float32), a * 0.95)

    # scan back in: paper shift, dust, hairs, grain, light falloff
    M = cv2.getRotationMatrix2D((w / 2, h / 2), rng.normal(0, 0.12), 1.0)
    M[:, 2] += rng.normal(0, 1.4, 2)
    img = cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_REFLECT)
    for _ in range(int(rng.integers(0, 3))):
        x, y = rng.integers(0, w), rng.integers(0, h)
        pts = np.stack([x + np.cumsum(rng.normal(0, 3, 30)), y + np.cumsum(rng.normal(2, 3, 30))], 1)
        cv2.polylines(img, [pts.astype(np.int32)], False, tuple(float(v) for v in (rng.choice([0.1, 0.85]),) * 3), 1,
                      cv2.LINE_AA)
    sp = rng.random((h, w))
    img[sp < 0.0006] = 0.12
    img[sp > 0.9995] = 0.85
    img += grain(rng, h, w, 0.9)[..., None] * 0.018
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    vig = 1 - 0.08 * (((xx - w / 2) / w) ** 2 + ((yy - h / 2) / h) ** 2) * 4
    img *= vig[..., None]
    out = (img.clip(0, 1) * 255).astype(np.uint8)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), out)
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    todo = ONLY or list(range(1, N + 1))
    with Pool(min(8, os.cpu_count() or 4)) as pool:
        for n in pool.imap_unordered(render, todo):
            print(n, end=" ", flush=True)
    print()
