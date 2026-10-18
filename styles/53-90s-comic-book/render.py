"""Early-90s comic book restyle, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [all | frame numbers...]

Built like a 1990s direct-market comic page, re-inked every frame:
  INKS: heavy spot blacks (whole shadow shapes filled solid black), thick
    brush contour lines with a heavier silhouette on the figures, and
    aggressive feathering / cross-hatching that grows out of every black
    shape into the mid-tones (single hatch near the light, cross-hatch in
    the darker band). The hatch lines are redrawn with a small new jitter
    every 2 frames so the inks boil like re-drawn panels.
  COLOURS: early digital "computer colouring": saturated flat colour holds
    shaded with smooth airbrush gradients, purple/indigo shadows, warm hot
    highlights, a coloured rim light on the figures, and a dramatic
    gradient vignette.
  PAPER: matte, slightly yellowed newsprint with fibre texture; colours sit
    in the paper (multiplied), blacks are dense but not pure.
  No speech balloons, panel borders, Ben-Day pop-art dots or CMYK offset.
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np

FRAMES, MASKS, OUT = sys.argv[1:4]
ARGS = sys.argv[4:]
H, W = 1080, 1620
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)


def frame_list():
    if not ARGS or ARGS == ["all"]:
        return list(range(1, 180))
    return [int(a) for a in ARGS]


def fbm(seed, hh, ww, octaves=4, base=6):
    rng = np.random.default_rng(seed)
    out = np.zeros((hh, ww), np.float32)
    amp, tot = 1.0, 0.0
    for o in range(octaves):
        c = base * 2 ** o
        n = rng.random((max(2, hh * c // ww), c)).astype(np.float32)
        out += amp * cv2.resize(n, (ww, hh), interpolation=cv2.INTER_CUBIC)
        tot += amp
        amp *= 0.5
    return out / tot


# newsprint: warm off-white with fibre streaks and blotchy absorbency
_fib = cv2.GaussianBlur(np.random.default_rng(11).normal(0, 1, (H, W)).astype(np.float32), (0, 0), 0.8)
_fib = cv2.GaussianBlur(_fib, (9, 1), 0) * 0.6 + _fib * 0.4
PAPER = (np.array([0.80, 0.90, 0.95], np.float32)[None, None]
         * (1 + 0.035 * (fbm(12, H, W, 4, 5) - 0.5) * 2)[..., None]
         * (1 + 0.025 * _fib)[..., None])
VIGNETTE = 1 - 0.30 * np.clip(((xx / W - 0.5) ** 2 * 1.3 + (yy / H - 0.42) ** 2 * 1.6) * 2.2, 0, 1)


def read(n):
    src = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png"))
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
    return src, m


def colours(src, mask):
    """Computer colouring: flat holds + airbrush gradients + coloured light."""
    small = cv2.resize(src, (W // 2, H // 2), interpolation=cv2.INTER_AREA)
    ms = cv2.pyrMeanShiftFiltering(small, 12, 30)
    ms = cv2.medianBlur(ms, 7)
    ms = cv2.resize(ms, (W, H), interpolation=cv2.INTER_LINEAR)
    f = ms.astype(np.float32) / 255
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
    hsv[..., 1] = 1 - (1 - np.clip(hsv[..., 1], 0, 1)) ** 1.9   # lift dull colours most
    # flat colour holds: value posterised into 4 hard steps (the colourist's
    # base / shadow / deep shadow / highlight); gradients come back on top
    v = hsv[..., 2]
    q = np.clip(np.round(v * 4) / 4, 0.12, 1)
    q = cv2.medianBlur((q * 255).astype(np.uint8), 9).astype(np.float32) / 255
    hsv[..., 2] = 0.75 * q + 0.25 * v
    f = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    lum = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
    # airbrush gradient shading: big soft light falloff, pushed for drama
    soft = cv2.GaussianBlur(lum, (0, 0), 22)
    soft = (soft - soft.mean()) / (soft.std() + 1e-4)
    f *= np.clip(1 + 0.22 * soft, 0.5, 1.5)[..., None]
    # indigo/purple shadows, hot warm highlights (split toning on the light)
    t = np.clip((cv2.GaussianBlur(lum, (0, 0), 3) - 0.18) / 0.55, 0, 1)[..., None]
    shadow_tint = np.array([0.62, 0.22, 0.42], np.float32)
    f = f * (0.78 + 0.32 * t) + shadow_tint * (1 - t) * 0.22
    f = f * (1 + 0.18 * t * np.array([-0.4, 0.1, 0.5], np.float32))
    # coloured rim light down the right edge of every figure (classic 90s glow)
    m = cv2.GaussianBlur(mask, (0, 0), 1.5)
    rim = np.clip(m - cv2.warpAffine(m, np.float32([[1, 0, -9], [0, 1, 4]]), (W, H)), 0, 1)
    rim = cv2.GaussianBlur(rim, (0, 0), 3) * m
    f = f + rim[..., None] * np.array([0.95, 0.75, 0.15], np.float32) * 0.9
    f *= VIGNETTE[..., None]
    hsv = cv2.cvtColor(np.clip(f, 0, 1).astype(np.float32), cv2.COLOR_BGR2HSV)
    hsv[..., 1] = np.clip(hsv[..., 1] * 1.2, 0, 1)
    hsv[..., 2] = np.clip(hsv[..., 2] * 1.12 + 0.03, 0, 1)
    f = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return np.clip(f, 0, 1), lum


def hatch_field(angle, period, seed):
    a = np.deg2rad(angle)
    wob = cv2.resize(np.random.default_rng(seed).normal(0, 1, (H // 40, W // 40)).astype(np.float32),
                     (W, H), interpolation=cv2.INTER_CUBIC) * 2.2
    p = (xx * np.cos(a) + yy * np.sin(a) + wob) % period
    return np.minimum(p, period - p)          # distance to the nearest hatch line


CLAHE = cv2.createCLAHE(clipLimit=2.2, tileGridSize=(6, 9))


def inks(src, lum, mask, n):
    boil = n // 2
    # inking decisions on a locally normalised value (the inker reads form,
    # not the camera's exposure)
    lum = 0.6 * CLAHE.apply(cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)).astype(np.float32) / 255 + 0.4 * lum
    rng = np.random.default_rng(300 + boil)
    l2 = cv2.GaussianBlur(lum, (0, 0), 2.2)
    local = cv2.GaussianBlur(lum, (0, 0), 30)
    # spot blacks: whole shadow shapes filled solid
    blk = ((l2 < 0.23) | ((l2 < 0.36) & (l2 < local * 0.66))).astype(np.uint8)
    blk = cv2.morphologyEx(blk, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    blk = cv2.morphologyEx(blk, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    num, lb, st, _ = cv2.connectedComponentsWithStats(blk, connectivity=8)
    ok = st[:, cv2.CC_STAT_AREA] > 160
    ok[0] = False
    blk = ok[lb].astype(np.uint8)
    # feathering: hatch lines grow out of the blacks into the shadow side,
    # tapering with distance (thick at the black, hairline at the tip)
    dist = cv2.distanceTransform(1 - blk, cv2.DIST_L2, 5)
    shadow_side = np.clip((cv2.GaussianBlur(lum, (0, 0), 10) - l2) / 0.08, 0, 1)
    tone = np.clip((0.40 - l2) / 0.18, 0, 1)                       # darker mid-tones
    reach = 14 + 26 * tone
    taper = np.clip(1 - dist / reach, 0, 1) * (l2 < 0.55)
    h1 = hatch_field(-55 + rng.normal(0, 2), 9.0, 400 + boil)
    h2 = hatch_field(35 + rng.normal(0, 2), 10.0, 500 + boil)
    w1 = 1.5 * np.maximum(taper, np.maximum(tone, 0.6 * shadow_side * (l2 < 0.5)))
    w2 = 1.3 * np.clip((0.30 - l2) / 0.1, 0, 1)                    # cross-hatch only the darkest band
    hatch = np.maximum(np.clip(w1 - h1 + 0.35, 0, 1) * (w1 > 0.15), np.clip(w2 - h2 + 0.35, 0, 1) * (w2 > 0.15))
    # contour lines (XDoG) - brush weight, heavier on the figures
    g = lum
    g1 = cv2.GaussianBlur(g, (0, 0), 1.2)
    g2 = cv2.GaussianBlur(g, (0, 0), 1.2 * 1.6)
    dog = g1 - 0.985 * g2
    line = (dog < -0.0085).astype(np.uint8)
    # finer facial / fold lines (the 90s habit of over-rendering faces)
    gf = cv2.GaussianBlur(g, (0, 0), 0.8)
    dog2 = gf - 0.98 * cv2.GaussianBlur(g, (0, 0), 1.6)
    line |= ((dog2 < -0.0065) & (mask > 0.5)).astype(np.uint8)
    num, lb, st, _ = cv2.connectedComponentsWithStats(line, connectivity=8)
    ok = st[:, cv2.CC_STAT_AREA] > 30
    ok[0] = False
    line = ok[lb].astype(np.uint8)
    m8 = (mask > 0.5).astype(np.uint8)
    near_fig = cv2.dilate(m8, np.ones((9, 9), np.uint8))
    line_fig = cv2.dilate(line, np.ones((3, 3), np.uint8)) * near_fig
    line = np.maximum(cv2.dilate(line, np.ones((2, 2), np.uint8)), line_fig)
    sil = cv2.dilate(m8, np.ones((7, 7), np.uint8)) - cv2.erode(m8, np.ones((3, 3), np.uint8))
    ink = np.maximum.reduce([blk.astype(np.float32), hatch, line.astype(np.float32), sil.astype(np.float32)])
    # slight per-redraw line wobble
    dx = cv2.resize(rng.normal(0, 1, (H // 60, W // 60)).astype(np.float32), (W, H), interpolation=cv2.INTER_CUBIC) * 1.2
    dy = cv2.resize(rng.normal(0, 1, (H // 60, W // 60)).astype(np.float32), (W, H), interpolation=cv2.INTER_CUBIC) * 1.2
    ink = cv2.remap(ink, xx + dx, yy + dy, cv2.INTER_LINEAR)
    return np.clip(cv2.GaussianBlur(ink, (0, 0), 0.55) * 1.3, 0, 1)


def render(n):
    src, mask = read(n)
    col, lum = colours(src, mask)
    ink = inks(src, lum, mask, n)
    img = col * PAPER                                    # colour printed into newsprint
    inkc = np.array([0.09, 0.07, 0.10], np.float32)      # dense, not pure, black
    img = img * (1 - ink[..., None]) + inkc * ink[..., None]
    # ink spread / matte print softness + faint paper grain
    img = cv2.GaussianBlur(img, (0, 0), 0.5)
    img *= (1 + 0.02 * np.random.default_rng(900 + n).normal(0, 1, (H, W)).astype(np.float32))[..., None]
    out = (np.clip(img, 0, 1) * 255).astype(np.uint8)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), out)
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    nums = frame_list()
    with Pool(min(8, os.cpu_count() or 4)) as p:
        for n in p.imap_unordered(render, nums):
            print(n, end=" ", flush=True)
    print()
