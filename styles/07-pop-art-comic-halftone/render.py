"""Pop-art comic / Lichtenstein restyle, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [frame numbers...]

People are flattened into a four-colour comic print: thick black ink line,
spot blacks, flat primary fills and Ben-Day dots on skin, the colour plates
slightly off-register against the black plate. Backgrounds swap between a
sunburst, a dot field, speed lines and a flattened version of the room.
Caption boxes, speech balloons and SFX bursts sit in the empty space.
Lines, dot phase and registration change every frame so the print boils.
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


def bgr(r, g, b):
    return np.array([b, g, r], np.float32) / 255


PAPER = bgr(250, 243, 226)
INK = bgr(22, 20, 26)
YEL = bgr(255, 218, 20)
RED = bgr(228, 32, 44)
BLU = bgr(24, 92, 196)
SKY = bgr(120, 190, 235)

# (first, last, background, overlay kind, overlay text)
SECTIONS = [
    (1, 30, "dots", "caption", "MEANWHILE, AT THE OFFICE..."),
    (31, 66, "sunburst", "bubble", "HEY! YOU'RE IN THE COMIC NOW!"),
    (67, 100, "env", "sfx", "WOW!"),
    (101, 136, "speed", "sfx", "POW!"),
    (137, 160, "dots", "bubble", "OOPS... TOO CLOSE?"),
    (161, 999, "sunburst", "sfx", "BAM!"),
]
FONT_DIR = "/System/Library/Fonts/Supplemental/"


def font(name, size):
    try:
        return ImageFont.truetype(FONT_DIR + name, size)
    except OSError:
        return ImageFont.load_default()


def section_of(n):
    for i, s in enumerate(SECTIONS):
        if s[0] <= n <= s[1]:
            return i, s
    return len(SECTIONS) - 1, SECTIONS[-1]


def vnoise(rng, h, w, cell):
    a = rng.random((max(2, h // cell + 2), max(2, w // cell + 2))).astype(np.float32)
    return cv2.resize(a, (w, h), interpolation=cv2.INTER_CUBIC).clip(0, 1)


def grain(rng, h, w, sigma=0.7):
    return cv2.GaussianBlur(rng.normal(0, 1, (h, w)).astype(np.float32), (0, 0), sigma)


def bendays(h, w, cell, frac, ox=0.0, oy=0.0, angle=45):
    """Uniform Ben-Day dot field; frac may be an array (dot radius as share of cell)."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    a = np.radians(angle)
    u = (xx + ox) * np.cos(a) + (yy + oy) * np.sin(a)
    v = -(xx + ox) * np.sin(a) + (yy + oy) * np.cos(a)
    du = np.mod(u, cell) - cell / 2
    dv = np.mod(v, cell) - cell / 2
    d = np.sqrt(du * du + dv * dv) / cell
    return np.clip((frac * 0.5 - d) * cell * 0.9 + 0.5, 0, 1)   # antialiased dot coverage


def over(dst, colour, alpha):
    a = alpha[..., None]
    return dst * (1 - a) + colour * a


def read_mask(n):
    return cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE)


def empty_spot(mask, h, w, bw, bh, prefer_top=True):
    """Top-left corner of the bw x bh box that overlaps the people least."""
    m = (mask > 128).astype(np.float32)
    best, pos = 1e9, (30, 30)
    for y in ([40, 60, 120] if prefer_top else [h - bh - 60, h - bh - 140]) + [h // 2 - bh // 2]:
        for x in np.linspace(40, w - bw - 40, 9).astype(int):
            y = int(np.clip(y, 30, h - bh - 30))
            cost = m[y:y + bh, x:x + bw].mean() + 0.05 * (y / h)
            if cost < best:
                best, pos = cost, (x, y)
    return pos


def section_plan(si, sec, h, w):
    rng = np.random.default_rng(300 + si * 11)
    mid = (sec[0] + min(sec[1], N)) // 2
    m = read_mask(mid)
    ys, xs = np.nonzero(m > 128)
    cx = float(np.median(xs)) if len(xs) else w / 2
    cy = float(np.percentile(ys, 20)) if len(ys) else h / 3
    kind, text = sec[3], sec[4]
    plan = dict(centre=(cx, cy), kind=kind, text=text, rot=rng.uniform(-0.15, 0.15))
    if kind == "caption":
        plan["box"] = (36, 30, 640, 92)
    elif kind == "bubble":
        bw, bh = 600, 230
        plan["box"] = (*empty_spot(m, h, w, bw, bh), bw, bh)
    else:
        bw, bh = 400, 300
        plan["box"] = (*empty_spot(m, h, w, bw, bh), bw, bh)
    return plan


def sunburst(h, w, cx, cy, rays, phase):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    ang = np.arctan2(yy - cy, xx - cx) + phase
    return (np.mod(ang / (2 * np.pi) * rays, 1.0) < 0.5).astype(np.float32)


def speed_lines(rng, h, w, cx, cy):
    lay = np.zeros((h, w), np.uint8)
    for _ in range(150):
        a = rng.uniform(0, 2 * np.pi)
        r0 = rng.uniform(0.28, 0.45) * w
        r1 = 1.2 * w
        p0 = (cx + r0 * np.cos(a), cy + r0 * np.sin(a))
        da = rng.uniform(0.002, 0.009)
        pts = np.array([p0, (cx + r1 * np.cos(a - da), cy + r1 * np.sin(a - da)),
                        (cx + r1 * np.cos(a + da), cy + r1 * np.sin(a + da))], np.int32)
        cv2.fillPoly(lay, [pts], 255, cv2.LINE_AA)
    return lay.astype(np.float32) / 255


def comic_lines(gray_smooth, rng, h, w):
    """XDoG-style ink lines from a flattened image, re-thresholded per frame."""
    g = gray_smooth.astype(np.float32) / 255
    s1 = cv2.GaussianBlur(g, (0, 0), 1.6)
    s2 = cv2.GaussianBlur(g, (0, 0), 1.6 * 1.7)
    d = s1 - s2
    thr = -0.018 + grain(rng, h, w, 2.0) * 0.003
    lines = (d < thr).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(lines, 8)
    keep = np.zeros(n, bool)
    keep[1:] = st[1:, cv2.CC_STAT_AREA] > 60                    # drop specks
    lines = keep[lab].astype(np.float32)
    return cv2.GaussianBlur(lines, (0, 0), 0.8)


def draw_overlays(img_u8, plan, rng, h, w):
    """Caption box / speech balloon / SFX burst with PIL, jittered per frame."""
    pil = Image.fromarray(cv2.cvtColor(img_u8, cv2.COLOR_BGR2RGB))
    d = ImageDraw.Draw(pil)
    x, y, bw, bh = plan["box"]
    x += int(rng.normal(0, 1.2))
    y += int(rng.normal(0, 1.2))
    ink = (22, 20, 26)
    if plan["kind"] == "caption":
        f = font("Comic Sans MS Bold.ttf", 40)
        bw = int(d.textlength(plan["text"], font=f)) + 48
        d.rectangle((x, y, x + bw, y + bh), fill=(255, 222, 40), outline=ink, width=6)
        d.text((x + 24, y + 20), plan["text"], font=f, fill=ink)
    elif plan["kind"] == "bubble":
        cx, cy = x + bw / 2, y + bh / 2
        px, py = plan["centre"]
        tail = [(cx - 40, cy + bh * 0.3), (cx + 30, cy + bh * 0.32),
                (px + (cx - px) * 0.35, py + (cy - py) * 0.35)]
        d.polygon(tail, fill=(255, 255, 255), outline=ink, width=7)
        d.ellipse((x, y, x + bw, y + bh), fill=(255, 255, 255), outline=ink, width=7)
        f = font("Comic Sans MS Bold.ttf", 46)
        words = plan["text"].split()
        half = (len(words) + 1) // 2
        for i, line in enumerate([" ".join(words[:half]), " ".join(words[half:])]):
            tw = d.textlength(line, font=f)
            d.text((cx - tw / 2, cy - 58 + i * 58), line, font=f, fill=ink)
    else:
        cx, cy = x + bw / 2, y + bh / 2
        r = np.random.default_rng(int(cx))
        k = 14
        pts = []
        for i in range(2 * k):
            a = i * np.pi / k + plan["rot"]
            rr = (bw * 0.5 if i % 2 == 0 else bw * 0.30) * r.uniform(0.85, 1.12)
            pts.append((cx + rr * np.cos(a) * 1.0, cy + rr * np.sin(a) * bh / bw))
        pts = [(px + rng.normal(0, 1.5), py + rng.normal(0, 1.5)) for px, py in pts]
        d.polygon(pts, fill=(255, 222, 40), outline=ink)
        d.line(pts + [pts[0]], fill=ink, width=7)
        f = font("Impact.ttf", 120)
        tw = d.textlength(plan["text"], font=f)
        layer = Image.new("RGBA", (int(tw) + 40, 170), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        ld.text((20, 10), plan["text"], font=f, fill=(228, 32, 44), stroke_width=7, stroke_fill=ink)
        layer = layer.rotate(np.degrees(-plan["rot"]) + rng.normal(0, 0.6), expand=True, resample=Image.BICUBIC)
        pil.paste(layer, (int(cx - layer.width / 2), int(cy - layer.height / 2)), layer)
    return cv2.cvtColor(np.array(pil), cv2.COLOR_RGB2BGR)


def render(n):
    si, sec = section_of(n)
    bgmode = sec[2]
    rng = np.random.default_rng(40_000 + n)
    src = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png"))
    h, w = src.shape[:2]
    plan = section_plan(si, sec, h, w)
    mask_u8 = read_mask(n)
    m = cv2.GaussianBlur((mask_u8 > 128).astype(np.float32), (0, 0), 1.0)

    # flatten the photo into comic-sized colour areas
    small = cv2.resize(src, (w // 2, h // 2), interpolation=cv2.INTER_AREA)
    flat = cv2.pyrMeanShiftFiltering(small, 9, 26)
    flat = cv2.resize(flat, (w, h), interpolation=cv2.INTER_LINEAR)
    flat = cv2.bilateralFilter(flat, 9, 40, 9)
    gray = cv2.cvtColor(flat, cv2.COLOR_BGR2GRAY)
    L = gray.astype(np.float32) / 255
    hsv = cv2.cvtColor(flat, cv2.COLOR_BGR2HSV).astype(np.float32)
    H, S = hsv[..., 0] * 2, hsv[..., 1] / 255
    ycc = cv2.cvtColor(flat, cv2.COLOR_BGR2YCrCb).astype(np.float32)
    skin = ((ycc[..., 1] > 141) & (ycc[..., 1] < 178) & (ycc[..., 2] > 80) & (ycc[..., 2] < 125)
            & (L > 0.32) & (S > 0.37) & (S < 0.62) & ((H < 40) | (H > 340))).astype(np.float32)
    skin = cv2.morphologyEx(skin, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    skin = cv2.GaussianBlur(skin, (0, 0), 1.2)
    warm = ((H < 60) | (H > 330)) & (S > 0.14)

    ox, oy = rng.uniform(0, 1.5), rng.uniform(0, 1.5)        # dot phase creeps a little each frame

    # ---------- background ----------
    img = np.broadcast_to(PAPER, (h, w, 3)).copy()
    cx, cy = plan["centre"]
    if bgmode == "sunburst":
        rays = sunburst(h, w, cx, cy, 28, si * 0.3 + rng.normal(0, 0.004))
        img = over(img, YEL, rays)
        img = over(img, RED, (1 - rays) * bendays(h, w, 16, 0.62, ox, oy))
    elif bgmode == "dots":
        yy = np.mgrid[0:h, 0:w][0].astype(np.float32) / h
        img = over(img, BLU, bendays(h, w, 22, 0.35 + 0.45 * yy, ox, oy))
    elif bgmode == "speed":
        img = over(img, YEL, np.full((h, w), 1.0, np.float32) * 0.0 + 1.0)
        img = over(img, INK, speed_lines(np.random.default_rng(900 + n), h, w, cx, cy) * 0.95)
    else:  # env: the room flattened into the same comic plates, muted
        envc = np.where((L > 0.72)[..., None], PAPER, np.where((L > 0.45)[..., None], SKY, BLU))
        img = envc.astype(np.float32)
        img = over(img, PAPER, bendays(h, w, 14, 0.5, ox, oy) * (L > 0.45) * (L <= 0.72))
        img = over(img, YEL, ((warm & (L > 0.35) & (L < 0.8)).astype(np.float32)))

    # ---------- people: flat colour plates ----------
    fill = np.broadcast_to(PAPER, (h, w, 3)).copy()
    # clothes / objects
    fill = np.where((warm & (L > 0.42))[..., None], YEL, fill)
    fill = np.where((warm & (L <= 0.42))[..., None], RED, fill)
    cool = ~warm
    fill = np.where((cool & (L <= 0.5))[..., None], BLU, fill)
    fill = over(fill, BLU, ((cool & (L > 0.5) & (L < 0.78)).astype(np.float32)
                            * bendays(h, w, 13, 0.62, ox, oy)))
    fill = np.where(((L > 0.80) | ((L > 0.66) & (S < 0.26)))[..., None], PAPER, fill)   # whites, light stripes
    # skin: Lichtenstein red dots on paper
    skin_tone = over(np.broadcast_to(PAPER, (h, w, 3)).copy(), RED, bendays(h, w, 12, 0.56, ox, oy))
    fill = over(fill, skin_tone, skin)
    # hair blue highlight band
    near_skin = cv2.dilate((skin > 0.5).astype(np.uint8), np.ones((25, 25), np.uint8)).astype(np.float32)
    hair_hi = ((L > 0.17) & (L < 0.27) & ~warm).astype(np.float32) * (1 - near_skin)
    fill = over(fill, BLU, hair_hi)

    # colour plates are slightly off-register against the black plate
    M = np.float32([[1, 0, rng.normal(2.5, 0.8)], [0, 1, rng.normal(-1.5, 0.8)]])
    fill = cv2.warpAffine(fill, M, (w, h), borderMode=cv2.BORDER_REFLECT)
    img = over(img, fill, m)

    # ---------- black plate ----------
    blacks = np.clip((0.17 - L) / 0.012, 0, 1) * m               # spot blacks (hair, shadows)
    lines = comic_lines(gray, rng, h, w) * m
    # faces need their features inked: finer lines + spot blacks from the unflattened photo
    g0 = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    g0 = cv2.bilateralFilter(g0, 7, 30, 7)
    face_lines = comic_lines(g0, rng, h, w) * near_skin * m
    L0 = g0.astype(np.float32) / 255
    face_blacks = np.clip((0.30 - L0) / 0.06, 0, 1) * near_skin * m
    face_blacks = cv2.morphologyEx(face_blacks, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    lines = np.maximum(lines, np.maximum(face_lines, face_blacks))
    contour = cv2.morphologyEx((mask_u8 > 128).astype(np.uint8), cv2.MORPH_GRADIENT,
                               cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))).astype(np.float32)
    wob = vnoise(rng, h, w, 40)
    contour *= (wob > 0.12)
    env_lines = comic_lines(gray, rng, h, w) * (1 - m) * (0.9 if bgmode == "env" else 0.0)
    k = np.clip(blacks + lines + contour + env_lines, 0, 1)
    img = over(img, INK, k)

    img_u8 = (img.clip(0, 1) * 255).astype(np.uint8)
    img_u8 = draw_overlays(img_u8, plan, rng, h, w)
    img = img_u8.astype(np.float32) / 255

    # panel border + gutter
    b = 14
    img[:b, :] = PAPER
    img[-b:, :] = PAPER
    img[:, :b] = PAPER
    img[:, -b:] = PAPER
    cv2.rectangle(img, (b, b), (w - b - 1, h - b - 1), tuple(float(c) for c in INK), 7)

    # newsprint: yellowed fibre, faint grain, slight dot gain blur
    tone = 0.97 - np.clip(vnoise(rng, h, w, 220) - 0.55, 0, 1) * 0.12
    img = img * tone[..., None] + grain(rng, h, w, 0.8)[..., None] * 0.015
    img = cv2.GaussianBlur(img, (0, 0), 0.5)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), (img.clip(0, 1) * 255).astype(np.uint8))
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    todo = ONLY or list(range(1, N + 1))
    with Pool(min(8, os.cpu_count() or 4)) as pool:
        for n in pool.imap_unordered(render, todo):
            print(n, end=" ", flush=True)
    print()
