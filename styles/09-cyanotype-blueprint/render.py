"""Cyanotype sun-print restyle, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [frame numbers...]

Each frame becomes a Prussian-blue cyanotype: tone mapped from paper white
through cyan-blue to deep Prussian blue, printed inside a hand-brushed patch
of emulsion on cold-press watercolour paper (ragged brush edges, dry-brush
bristle streaks, uneven coating), with white botanical photogram shadows
(ferns, leaves) where plants sat on the paper during exposure, and a pencil
note in the margin. Coating streaks, paper grain, brush edge and the plant
shadows shift a little every frame, as if every frame was printed by hand.
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FRAMES, MASKS, OUT = sys.argv[1:4]
ONLY = [int(a) for a in sys.argv[4:]]
N = len([f for f in os.listdir(FRAMES) if f.endswith(".png")])

PAPER = np.array([232, 241, 246], np.float32) / 255           # BGR warm watercolour white
# density -> colour ramp (BGR), paper white to Prussian blue
RAMP_D = np.array([0.0, 0.18, 0.42, 0.66, 0.86, 1.0], np.float32)
RAMP_C = np.array([[232, 241, 246], [222, 205, 170], [190, 150, 92], [150, 95, 38],
                   [104, 55, 18], [70, 32, 10]], np.float32) / 255

# (first, last, mode, pencil note)
SECTIONS = [
    (1, 30, "print", "no. 1  —  office, morning"),
    (31, 66, "photogram", "no. 2  —  with ferns"),
    (67, 100, "print", "no. 3  —  three of us"),
    (101, 136, "photogram", "no. 4  —  sun print"),
    (137, 160, "print", "no. 5  —  close"),
    (161, 999, "photogram", "no. 6  —  last light"),
]


def section_of(n):
    for i, s in enumerate(SECTIONS):
        if s[0] <= n <= s[1]:
            return i, s
    return len(SECTIONS) - 1, SECTIONS[-1]


def vnoise(rng, h, w, cell):
    a = rng.random((max(2, h // cell + 2), max(2, w // cell + 2))).astype(np.float32)
    return cv2.resize(a, (w, h), interpolation=cv2.INTER_CUBIC).clip(0, 1)


def streaks(rng, h, w, cx=900, cy=6):
    """Anisotropic noise: long horizontal brush streaks."""
    a = rng.random((max(2, h // cy), max(2, w // cx + 2))).astype(np.float32)
    return cv2.resize(a, (w, h), interpolation=cv2.INTER_CUBIC).clip(0, 1)


def grain(rng, h, w, sigma=0.7):
    return cv2.GaussianBlur(rng.normal(0, 1, (h, w)).astype(np.float32), (0, 0), sigma)


def ramp(d):
    d = d.clip(0, 1)
    out = np.zeros(d.shape + (3,), np.float32)
    for c in range(3):
        out[..., c] = np.interp(d, RAMP_D, RAMP_C[:, c])
    return out


def read_mask(n):
    return cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE)


def brushed_coat(rng, h, w, si):
    """Alpha of the hand-brushed emulsion patch: ragged edges + dry-brush bristles."""
    r = np.random.default_rng(5000 + si)                      # shape mostly fixed per section
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    top = 62 + 22 * (vnoise(r, 1, w, 90)[0] - 0.5) + 6 * (vnoise(rng, 1, w, 14)[0] - 0.5)
    bot = h - 70 + 22 * (vnoise(r, 1, w, 90)[0] - 0.5) + 6 * (vnoise(rng, 1, w, 14)[0] - 0.5)
    left = 80 + 34 * (vnoise(r, h, 1, 60)[:, 0] - 0.5) + 10 * (vnoise(rng, h, 1, 7)[:, 0] - 0.5)
    right = w - 80 + 34 * (vnoise(r, h, 1, 60)[:, 0] - 0.5) + 10 * (vnoise(rng, h, 1, 7)[:, 0] - 0.5)
    a = ((yy > top[None, :]) & (yy < bot[None, :]) & (xx > left[:, None]) & (xx < right[:, None])).astype(np.float32)
    # dry-brush bristles running out past the left / right ends of the strokes, in clumps
    bris = np.zeros((h, w), np.float32)
    for side in (0, 1):
        for _ in range(9):                                       # a few loaded brush passes
            yc = r.uniform(80, h - 80)
            for _ in range(int(r.integers(4, 11))):
                y = int(np.clip(yc + r.normal(0, 18), 0, h - 1))
                L = r.gamma(2.0, 28)
                x0 = left[y] + 4 if side == 0 else right[y] - 4
                x1 = x0 - L if side == 0 else x0 + L
                seg = np.linspace(0, 1, 8)
                for a0, a1 in zip(seg[:-1], seg[1:]):           # taper: opacity fades along the hair
                    xa, xb = x0 + (x1 - x0) * a0, x0 + (x1 - x0) * a1
                    cv2.line(bris, (int(xa), y), (int(xb), y), float(0.9 * (1 - a0) ** 0.7), int(r.integers(1, 3)), cv2.LINE_AA)
    a = np.maximum(a, bris)
    # bristle gaps along the top / bottom stroke edges
    gaps = (streaks(rng, h, w, 400, 3) > 0.82) & ((np.abs(yy - top[None, :]) < 26) | (np.abs(yy - bot[None, :]) < 26))
    a[gaps] *= 0.25
    a = cv2.GaussianBlur(a, (0, 0), 1.2)
    return a


# ---------------------------------------------------------------- botanicals
def fern(alpha, base, length, ang, curv, rng, leaf_w=0.30):
    t = np.linspace(0, 1, 60)
    a = ang + curv * t
    pts = np.zeros((60, 2), np.float32)
    pts[0] = base
    for i in range(1, 60):
        pts[i] = pts[i - 1] + length / 60 * np.array([np.cos(a[i]), np.sin(a[i])])
    cv2.polylines(alpha, [pts.astype(np.int32)], False, 1.0, 5, cv2.LINE_AA)
    for i in range(4, 58, 2):
        tt = i / 60
        L = length * 0.22 * np.sin(np.pi * min(1, tt * 1.15)) * (1 - 0.55 * tt) + 6
        for side in (-1, 1):
            la = a[i] + side * (1.15 - 0.3 * tt) + rng.normal(0, 0.05)
            c = pts[i] + L / 2 * np.array([np.cos(la), np.sin(la)])
            el = cv2.ellipse2Poly((int(c[0]), int(c[1])), (int(L / 2), max(2, int(L * leaf_w / 2))),
                                  int(np.degrees(la)), 0, 360, 12)
            cv2.fillPoly(alpha, [el], 1.0, cv2.LINE_AA)


def leaf(alpha, veins, centre, length, ang, rng):
    t = np.linspace(0, np.pi, 40)
    x = np.concatenate([t, t[::-1]]) / np.pi * length - length / 2
    y = np.concatenate([np.sin(t) ** 1.3, -np.sin(t[::-1]) ** 1.3]) * length * 0.22
    c, s = np.cos(ang), np.sin(ang)
    P = np.stack([centre[0] + x * c - y * s, centre[1] + x * s + y * c], 1)
    cv2.fillPoly(alpha, [P.astype(np.int32)], 1.0, cv2.LINE_AA)
    a0 = np.array(centre) - length / 2 * np.array([c, s])
    a1 = np.array(centre) + length / 2 * np.array([c, s])
    cv2.line(veins, tuple(a0.astype(int)), tuple(a1.astype(int)), 1.0, 3, cv2.LINE_AA)
    for k in range(1, 7):
        p = a0 + (a1 - a0) * k / 7.5
        for side in (-1, 1):
            q = p + length * 0.16 * np.array([np.cos(ang + side * 0.8), np.sin(ang + side * 0.8)])
            cv2.line(veins, tuple(p.astype(int)), tuple(q.astype(int)), 1.0, 2, cv2.LINE_AA)
    # stem
    st = a0 - length * 0.25 * np.array([c, s])
    cv2.line(alpha, tuple(st.astype(int)), tuple(a0.astype(int)), 1.0, 4, cv2.LINE_AA)


def section_plan(si, sec, h, w):
    rng = np.random.default_rng(3300 + si * 7)
    first, last = sec[0], min(sec[1], N)
    union = np.zeros((h, w), np.uint8)
    for k in range(first, last + 1, 4):
        union = np.maximum(union, read_mask(k))
    free = cv2.dilate((union > 128).astype(np.uint8), np.ones((71, 71), np.uint8)) == 0
    plants = []
    corners = [(60, 60, 0.6), (w - 60, 60, 2.4), (60, h - 60, -0.6), (w - 60, h - 60, -2.4),
               (w / 2, 40, 1.57), (w / 2, h - 40, -1.57)]
    rng.shuffle(corners)
    count = 4 if sec[2] == "photogram" else 2
    for x, y, a in corners[:count]:
        if rng.random() < 0.65:
            plants.append(("fern", (x, y), rng.uniform(0.38, 0.55) * h, a + rng.normal(0, 0.25), rng.normal(0, 0.5)))
        else:
            plants.append(("leaf", (x + 120 * np.cos(a), y + 120 * np.sin(a)), rng.uniform(170, 260), a + rng.normal(0, 0.3), 0))
    if sec[2] == "photogram":                                   # scatter small leaves in free space
        ys, xs = np.nonzero(free[::20, ::20])
        for i in rng.choice(len(xs), min(6, len(xs)), replace=False) if len(xs) else []:
            plants.append(("leaf", (xs[i] * 20, ys[i] * 20), rng.uniform(90, 160), rng.uniform(0, np.pi), 0))
    return dict(plants=plants)


def pencil_note(h, w, text, rng):
    lay = Image.new("L", (w, h), 0)
    try:
        f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Bradley Hand Bold.ttf", 30)
    except OSError:
        f = ImageFont.load_default()
    ImageDraw.Draw(lay).text((96 + rng.normal(0, 0.6), h - 50 + rng.normal(0, 0.6)), text, font=f, fill=255)
    a = np.array(lay).astype(np.float32) / 255
    return a * (0.55 + 0.45 * (rng.random((h, w)) > 0.3))        # graphite skips on the tooth


def render(n):
    si, sec = section_of(n)
    mode, note = sec[2], sec[3]
    rng = np.random.default_rng(70_000 + n)
    src = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png"))
    h, w = src.shape[:2]
    plan = section_plan(si, sec, h, w)
    m = cv2.GaussianBlur((read_mask(n) > 128).astype(np.float32), (0, 0), 1.5)

    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    L = cv2.createCLAHE(clipLimit=2.2, tileGridSize=(8, 8)).apply(gray).astype(np.float32) / 255
    L = cv2.GaussianBlur(L, (0, 0), 1.1)                          # contact-print softness
    D = np.clip((1.0 - L) * 1.12 - 0.02, 0, 1) ** 0.85

    if mode == "photogram":
        # room fully exposed to deep blue; only the people print as a photograph
        me = cv2.GaussianBlur(cv2.erode((read_mask(n) > 128).astype(np.uint8), np.ones((5, 5), np.uint8)).astype(np.float32), (0, 0), 1.5)
        D = D * me + (0.93 + 0.05 * vnoise(rng, h, w, 120)) * (1 - me)

    # botanical photogram: plants block UV -> paper white, translucent leaves show veins
    block = np.zeros((h, w), np.float32)
    veins = np.zeros((h, w), np.float32)
    jr = np.random.default_rng(si)
    for kind, pos, size, ang, curv in plan["plants"]:
        pos = (pos[0] + rng.normal(0, 1.5), pos[1] + rng.normal(0, 1.5))
        ang = ang + rng.normal(0, 0.004)
        if kind == "fern":
            fern(block, np.array(pos, np.float32), size, ang, curv, jr)
        else:
            leaf(block, veins, pos, size, ang, jr)
    block = cv2.GaussianBlur(block, (0, 0), 2.2)                  # leaves never sit perfectly flat
    veins = cv2.GaussianBlur(veins, (0, 0), 1.2)
    opacity = 0.93 - veins * 0.45
    D = D * (1 - block * opacity * (1 - m * 0.85))                # keep the people readable

    # uneven hand coating: streaks along the brush direction, pooling, thin spots
    coat = 0.93 + 0.08 * streaks(rng, h, w, 700, 16) + 0.06 * (vnoise(rng, h, w, 160) - 0.5)
    coat *= 1 - 0.18 * np.clip(vnoise(np.random.default_rng(40 + si), h, w, 260) - 0.65, 0, 1) * 3
    D = D * coat
    D = 0.06 + D * 0.94                                            # coated paper never washes fully clean
    a = brushed_coat(rng, h, w, si)
    D = D * a

    # chemistry specks: undeveloped pinholes and dark spots
    sp = rng.random((h, w))
    D[sp < 0.0008] *= 0.3
    D[(sp > 0.99985)] = 1.0

    img = ramp(D)

    # cold-press watercolour paper: fine embossed tooth lit from the top-left, soft fibre cloud
    tr = np.random.default_rng(9)
    tooth = grain(tr, h, w, 1.6) + 0.6 * grain(tr, h, w, 4.0)
    gy, gx = np.gradient(tooth)
    light = 1 - (gx + gy) * 0.35 + (vnoise(np.random.default_rng(10), h, w, 90) - 0.5) * 0.03
    light += grain(rng, h, w, 0.8) * 0.008
    img = img * light[..., None].clip(0.93, 1.05)
    # faint water tide-line along the coating edge
    tide = cv2.GaussianBlur(a, (0, 0), 6) - cv2.GaussianBlur(a, (0, 0), 1.5)
    img = img * (1 - np.clip(-tide, 0, 1)[..., None] * 0.25)

    img = img * (1 - pencil_note(h, w, note, rng)[..., None] * np.array([0.45, 0.47, 0.5], np.float32))
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), (img.clip(0, 1) * 255).astype(np.uint8))
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    todo = ONLY or list(range(1, N + 1))
    with Pool(min(8, os.cpu_count() or 4)) as pool:
        for n in pool.imap_unordered(render, todo):
            print(n, end=" ", flush=True)
    print()
