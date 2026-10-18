"""Spider-Verse Comic Offset: Into/Across the Spider-Verse look, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [frame numbers... | all]

People: flattened, saturated colour in 3-4 tone steps, thick black ink
contours, diagonal ink HATCHING in the shadows (cross-hatch in the deepest)
and a coarse halftone dot screen in the mid-shadows. Background: instead of
depth blur it is printed OFF-REGISTER: the cyan, magenta and yellow plates
are split apart by 10-20 px, a big halftone screen rides on top, and the
palette is pushed toward night purple/magenta/teal. Accents: Kirby-dot
clusters (black dots with a magenta/cyan glow) in the corners and glitch
frames (slice offsets, RGB split, a block re-printed in a "different
universe" palette) every ~2 s. Texture is animated ON TWOS: hatching, dot
screens, plate offsets and Kirby dots step every second frame, while the
people's pose follows the source on every frame.
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np

FRAMES, MASKS, OUT = sys.argv[1:4]
ARGS = sys.argv[4:]
if ARGS == ["all"]:
    ONLY = list(range(1, 180))
else:
    ONLY = [int(a) for a in ARGS] or [13, 49, 85, 109, 145, 178]

GLITCH = {23, 24, 47, 71, 72, 98, 121, 122, 146, 169}   # glitch frames (pairs = 2-frame hits)
KIRBY = [(1, 30), (60, 90), (110, 140), (160, 179)]       # sections with Kirby-dot energy


def ones(n):
    return (n + 1) // 2          # texture key: steps every second frame ("on twos")


def kirby_on(n):
    return any(a <= n <= b for a, b in KIRBY)


def dot_screen(h, w, cell, angle, ox, oy):
    """Distance-to-dot-centre field for a rotated square dot grid, 0 at centre .. ~0.7 at corner."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    a = np.deg2rad(angle)
    u = (xx * np.cos(a) + yy * np.sin(a) + ox) / cell
    v = (-xx * np.sin(a) + yy * np.cos(a) + oy) / cell
    du, dv = u - np.round(u), v - np.round(v)
    return np.sqrt(du * du + dv * dv)


def hatch(h, w, spacing, angle, phase, wob, rng):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    a = np.deg2rad(angle)
    t = xx * np.cos(a) + yy * np.sin(a) + phase
    noise = cv2.resize(rng.normal(0, 1, (h // 40 + 1, w // 40 + 1)).astype(np.float32), (w, h))
    t = t + noise * wob
    f = np.abs(((t / spacing) % 1) - 0.5) * 2          # 1 on the line
    return np.clip((f - 0.62) / 0.2, 0, 1)


def posterize_colour(img):
    small = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    u8 = (np.clip(small, 0, 1) * 255).astype(np.uint8)
    for _ in range(2):
        u8 = cv2.bilateralFilter(u8, 9, 45, 7)
    sm = cv2.resize(u8, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_LINEAR).astype(np.float32) / 255
    hsv = cv2.cvtColor(sm, cv2.COLOR_BGR2HSV)
    hsv[..., 1] = np.clip(hsv[..., 1] * 1.55 + 0.05, 0, 1)
    v = hsv[..., 2]
    steps = np.array([0.16, 0.42, 0.68, 0.92], np.float32)
    idx = np.clip((v * 4).astype(int), 0, 3)
    hsv[..., 2] = steps[idx] * 0.75 + v * 0.25                    # stepped cel tones
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR), sm, v


def misregister(img, rng, amp):
    """Split into C, M, Y plates and print them off-register."""
    cmy = 1 - img                     # B,G,R -> Y,M,C
    out = np.empty_like(cmy)
    h, w = img.shape[:2]
    for ch in range(3):
        dx, dy = rng.uniform(-1, 1, 2) * amp
        M = np.float32([[1, 0, dx], [0, 1, dy]])
        out[..., ch] = cv2.warpAffine(cmy[..., ch], M, (w, h), borderMode=cv2.BORDER_REFLECT)
    return 1 - out


def kirby(rng, h, w):
    """Clusters of black dots with a neon glow, Jack Kirby 'krackle'."""
    dots = np.zeros((h, w), np.float32)
    for _ in range(rng.integers(2, 4)):
        side = rng.integers(0, 4)
        cx = rng.uniform(0.0, 0.25) * w if side == 0 else (rng.uniform(0.75, 1.0) * w if side == 1 else rng.uniform(0, 1) * w)
        cy = rng.uniform(0, 1) * h if side < 2 else (rng.uniform(0, 0.2) * h if side == 2 else rng.uniform(0.8, 1.0) * h)
        for _ in range(rng.integers(14, 30)):
            r = abs(rng.normal(0, 1)) * 14 + 4
            x = cx + rng.normal(0, 70)
            y = cy + rng.normal(0, 70)
            cv2.circle(dots, (int(x), int(y)), int(r), 1.0, -1, cv2.LINE_AA)
    return dots


def glitch(out, rng, h, w):
    res = out.copy()
    for _ in range(rng.integers(5, 10)):                      # horizontal slice offsets
        y0 = int(rng.uniform(0, h - 20))
        hh = int(rng.uniform(8, 70))
        dx = int(rng.normal(0, 60))
        res[y0:y0 + hh] = np.roll(res[y0:y0 + hh], dx, 1)
    res[..., 2] = np.roll(res[..., 2], int(rng.uniform(8, 18)), 1)   # RGB split
    res[..., 0] = np.roll(res[..., 0], -int(rng.uniform(8, 18)), 1)
    # one block re-printed in a different universe: inverted, cyan/magenta duotone
    bw, bh = int(rng.uniform(0.15, 0.3) * w), int(rng.uniform(0.15, 0.35) * h)
    x0, y0 = int(rng.uniform(0, w - bw)), int(rng.uniform(0, h - bh))
    blk = res[y0:y0 + bh, x0:x0 + bw]
    g = 1 - blk.mean(-1, keepdims=True)
    duo = np.array([0.55, 0.05, 0.95], np.float32) * (1 - g) + np.array([1.0, 0.95, 0.2], np.float32) * g
    res[y0:y0 + bh, x0:x0 + bw] = duo
    cv2.rectangle(res, (x0, y0), (x0 + bw, y0 + bh), (0, 0, 0), 3)
    return res


def render(n):
    tk = ones(n)
    rng = np.random.default_rng(3000 + tk)            # on twos: texture holds for 2 frames
    src = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png")).astype(np.float32) / 255
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), 0).astype(np.float32) / 255
    h, w = m.shape
    mb = cv2.GaussianBlur(m, (0, 0), 1.2)[..., None]

    cel, sm, v = posterize_colour(src)

    # skin: keep faces readable (softer tone steps, no dot blobs, light hatching only)
    hsv0 = cv2.cvtColor(np.clip(sm, 0, 1), cv2.COLOR_BGR2HSV)
    skin = ((hsv0[..., 0] < 28) & (hsv0[..., 1] > 0.18) & (hsv0[..., 1] < 0.75) & (hsv0[..., 2] > 0.32)).astype(np.float32)
    skin = cv2.GaussianBlur(skin * m, (0, 0), 4)[..., None]
    cel = cel * (1 - skin * 0.6) + sm * skin * 0.6
    v = v * (1 - skin[..., 0] * 0.6) + np.clip(v + 0.12, 0, 1) * skin[..., 0] * 0.6

    # ---- people: cel colour + halftone mid-shadows + hatching shadows + ink lines
    ox, oy = rng.uniform(0, 9, 2)
    dsc = dot_screen(h, w, 9, 15, ox, oy)
    shade = np.clip((0.62 - v) / 0.32, 0, 1) * (1 - skin[..., 0])   # 0 lit .. 1 deep shadow
    dot_r = np.sqrt(shade * 0.45)                                   # dot radius grows with darkness
    dots = np.clip((dot_r - dsc) * 6 + 0.5, 0, 1) * (shade > 0.05)
    ink_col = cel * 0.3
    subj = cel * (1 - dots[..., None] * 0.75) + ink_col * dots[..., None] * 0.75
    ph = rng.uniform(0, 12)
    h1 = hatch(h, w, 8, 45, ph, 1.5, rng)
    h2 = hatch(h, w, 9, -40, ph * 1.3, 1.5, rng)
    # hatching sits on the coloured mid-shadows (where it reads), cross-hatch deeper;
    # the very darkest areas go flat ink
    band = np.clip((0.50 - v) / 0.10, 0, 1) * np.clip((v - 0.10) / 0.06, 0, 1)
    band2 = np.clip((0.34 - v) / 0.08, 0, 1) * np.clip((v - 0.10) / 0.06, 0, 1)
    hat = np.maximum(h1 * band * (1 - 0.5 * skin[..., 0]), h2 * band2 * (1 - skin[..., 0]))[..., None]
    subj = subj * (1 - hat * 0.85)
    flat = np.clip((0.12 - v) / 0.05, 0, 1)[..., None]
    subj = subj * (1 - flat) + np.array([0.06, 0.03, 0.05], np.float32) * flat

    g8 = (cv2.cvtColor(np.clip(sm, 0, 1), cv2.COLOR_BGR2GRAY) * 255).astype(np.uint8)
    e = cv2.Canny(g8, 35, 95)
    e = cv2.dilate(e, np.ones((2, 2), np.uint8)).astype(np.float32) / 255
    mu = (m > 0.5).astype(np.uint8)
    contour = (cv2.dilate(mu, np.ones((5, 5), np.uint8)) - cv2.erode(mu, np.ones((3, 3), np.uint8))).astype(np.float32)
    lines = np.clip(e * 0.95 + contour, 0, 1)
    # line weight wobble, re-drawn on twos
    wob = cv2.resize(rng.uniform(0.6, 1.0, (h // 30 + 1, w // 30 + 1)).astype(np.float32), (w, h))
    subj = subj * (1 - (lines * wob)[..., None])
    # tiny print offset on the people too (a hairline of magenta/cyan on edges)
    subj = misregister(subj, rng, 2.5)

    # ---- background: night palette, off-register plates, big halftone
    bgc = cel.copy()
    lum = bgc.mean(-1, keepdims=True)
    lum = np.clip((lum - 0.25) / 0.7, 0, 1) ** 1.3
    night = np.array([0.40, 0.04, 0.16], np.float32) * (1 - lum) + np.array([0.85, 0.45, 1.0], np.float32) * lum
    bgc = bgc * 0.3 + night * 0.7
    bgc = misregister(bgc, rng, 16)
    big = dot_screen(h, w, 16, 30, *rng.uniform(0, 16, 2))
    bshade = np.clip(0.85 - bgc.mean(-1), 0, 1)
    bdots = np.clip((np.sqrt(bshade * 0.45) - big) * 5 + 0.5, 0, 1)[..., None]
    bgc = bgc * (1 - bdots * 0.35) + np.array([0.5, 0.0, 0.6], np.float32) * bdots * 0.25
    be = cv2.Canny(g8, 60, 140)
    be = cv2.GaussianBlur(be.astype(np.float32) / 255, (0, 0), 0.8)
    be = np.roll(be, int(rng.uniform(4, 10)), 1)                    # bg line art off-register too
    bgc = bgc * (1 - be[..., None] * 0.5)

    out = bgc * (1 - mb) + subj * mb

    if kirby_on(n):
        kd = kirby(rng, h, w) * (1 - m)
        glow = np.clip(cv2.GaussianBlur(cv2.dilate(kd, np.ones((15, 15), np.uint8)), (0, 0), 10) * 1.6, 0, 1)[..., None]
        col = np.array([0.95, 0.15, 1.0], np.float32) if tk % 2 else np.array([1.0, 0.85, 0.1], np.float32)
        out = out * (1 - glow * 0.5) + glow * col * 0.9
        out = out * (1 - kd[..., None])

    # print paper: slight warm stock + fine grain that also steps on twos
    out = out * 0.96 + np.array([0.02, 0.03, 0.04], np.float32)
    out = out + rng.normal(0, 0.02, (h, w, 1)).astype(np.float32)

    if n in GLITCH:
        out = glitch(np.clip(out, 0, 1), np.random.default_rng(9000 + n), h, w)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), (np.clip(out, 0, 1) * 255).astype(np.uint8))
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    with Pool(min(8, os.cpu_count() or 2)) as p:
        for n in p.imap_unordered(render, ONLY):
            print("frame", n, flush=True)
