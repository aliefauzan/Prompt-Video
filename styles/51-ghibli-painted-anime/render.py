"""Ghibli-style painted anime restyle, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [all | frame numbers...]

Two layers, like a hand-painted anime film frame:
  BACKGROUND (everything outside the person masks): a gouache "background art"
    painting — mean-shift paint patches blended with soft gradients, lush
    greens, warm cream walls, soft brush texture and paper grain fixed in
    screen space (a background painting does not boil). The bright window is
    repainted as a summer sky with soft painted cumulus clouds.
  CHARACTERS (inside the masks): a clean cel — flat base colours from
    mean-shift, ONE hard-edged warm-violet shadow shape, a soft highlight on
    hair, thin brown line art (XDoG) and a thin brown silhouette line.
Then warm sunlight from the window (glow + light falloff), gentle bloom,
very light film grain and softness of a 35 mm anime print.
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np

FRAMES, MASKS, OUT = sys.argv[1:4]
ARGS = sys.argv[4:]
H, W = 1080, 1620


def frame_list():
    if not ARGS or ARGS == ["all"]:
        return list(range(1, 180))
    return [int(a) for a in ARGS]


def fbm(seed, h, w, octaves=5, base=6):
    rng = np.random.default_rng(seed)
    out = np.zeros((h, w), np.float32)
    amp, tot = 1.0, 0.0
    for o in range(octaves):
        c = base * 2 ** o
        n = rng.random((max(2, h * c // w), c)).astype(np.float32)
        out += amp * cv2.resize(n, (w, h), interpolation=cv2.INTER_CUBIC)
        tot += amp
        amp *= 0.5
    return out / tot


def lic(noise, theta, steps=9):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dx, dy = np.cos(theta), np.sin(theta)
    acc = noise.copy()
    for s in range(1, steps + 1):
        for sg in (-1, 1):
            acc += cv2.remap(noise, xx + sg * s * dx, yy + sg * s * dy, cv2.INTER_LINEAR,
                             borderMode=cv2.BORDER_REFLECT)
    return acc / (2 * steps + 1)


def make_sky():
    """Painted summer sky: big gouache cumulus + a lush tree canopy at the bottom
    (screen space, computed once — background art does not boil)."""
    y = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    top = np.array([210, 140, 70], np.float32)      # BGR deep summer blue
    bot = np.array([236, 214, 178], np.float32)     # pale horizon
    sky = top * (1 - y[..., None] ** 0.9) + bot * (y[..., None] ** 0.9)
    sky = np.broadcast_to(sky, (H, W, 3)).copy()
    # cumulus: clusters of overlapping puffs, flat bottoms, lit tops / shaded bellies
    rng = np.random.default_rng(12)
    cloud = np.zeros((H, W), np.float32)
    lit = np.zeros((H, W), np.float32)
    yy = np.arange(H, dtype=np.float32)[:, None]
    for cx, cy, sc in [(260, 170, 0.9), (780, 120, 1.15), (1300, 190, 1.0), (560, 330, 0.7),
                       (1520, 90, 0.75), (60, 360, 0.7), (1030, 320, 0.65)]:
        layer = np.zeros((H, W), np.float32)
        base = cy + 60 * sc
        for _ in range(13):
            r = rng.uniform(30, 72) * sc
            px = cx + rng.normal(0, 85 * sc)
            py = base - r * rng.uniform(0.35, 1.3)
            cv2.circle(layer, (int(px), int(py)), int(r), 1.0, -1, cv2.LINE_AA)
        layer[int(base):] = 0
        rows = np.where(layer.max(1) > 0)[0]
        if len(rows) == 0:
            continue
        top = rows[0]
        t = np.clip((yy - top) / max(1, base - top), 0, 1)
        shade = 1 - np.clip((t - 0.45) * 1.6, 0, 1)
        lit = np.where(layer > cloud, np.broadcast_to(shade, (H, W)), lit)
        cloud = np.maximum(cloud, layer)
    edge_n = fbm(13, H, W, 3, 30)
    cloud = cv2.GaussianBlur(cloud, (0, 0), 2.5) * (0.88 + 0.24 * edge_n)
    cloud = np.clip((cloud - 0.3) * 3, 0, 1)
    lit = cv2.GaussianBlur(lit, (0, 0), 5)
    white = np.array([248, 250, 255], np.float32)
    belly = np.array([206, 176, 176], np.float32)
    ccol = belly * (1 - lit[..., None]) + white * lit[..., None]
    sky = sky * (1 - cloud[..., None]) + ccol * cloud[..., None]
    # tree canopy: bumpy top edge, clumped leaves, lit tops / blue-green shade
    xs = np.arange(W, dtype=np.float32)
    rng = np.random.default_rng(5)
    edge = H * 0.40 + 40 * np.sin(xs / 97 + 1) + 25 * np.sin(xs / 41 + 2) + 12 * np.sin(xs / 17)
    yy = np.arange(H, dtype=np.float32)[:, None]
    clumps = fbm(61, H, W, 4, 24)
    can = np.clip((yy - edge[None, :] + 60 * (clumps - 0.5)) / 6, 0, 1)
    shade = np.clip((yy - edge[None, :]) / 140, 0, 1)
    leaf = clumps - cv2.GaussianBlur(clumps, (0, 0), 6)
    g_lit = np.array([70, 190, 150], np.float32)
    g_dark = np.array([70, 105, 40], np.float32)
    gcol = g_lit * (1 - shade[..., None]) + g_dark * shade[..., None]
    gcol = gcol * (1 + 2.5 * leaf[..., None])
    sky = sky * (1 - can[..., None]) + gcol * can[..., None]
    return np.clip(sky, 0, 255)


SKY = make_sky()
PAPER = (fbm(21, H, W, 6, 40) - 0.5).astype(np.float32)
DRIFT = (fbm(51, H, W, 3, 3) - 0.5).astype(np.float32)
BRUSH_THETA = (0.35 + 0.5 * fbm(31, H, W, 3, 3)).astype(np.float32)
BRUSH = lic(cv2.GaussianBlur(np.random.default_rng(41).random((H, W)).astype(np.float32), (0, 0), 3.5), BRUSH_THETA, 16)
BRUSH = ((BRUSH - BRUSH.mean()) / BRUSH.std()).astype(np.float32)


def read_mask(n):
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE)
    return m.astype(np.float32) / 255


def meanshift(img, sp, sr, scale=0.5):
    small = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    ms = cv2.pyrMeanShiftFiltering(small, sp, sr)
    ms = cv2.medianBlur(ms, 5)
    return cv2.resize(ms, (W, H), interpolation=cv2.INTER_LINEAR)


def grade_bg(bgr):
    f = bgr.astype(np.float32) / 255
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
    hue, sat, val = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    green = np.exp(-((hue - 100) / 35) ** 2)            # foliage
    sat = np.clip(sat * (1.25 + 1.2 * green) + 0.05 * green, 0, 1)
    hue = hue - 12 * green * (hue > 100)                 # bluish greens -> lush yellow-green
    val = np.clip(val * 0.92 + 0.1, 0, 1) ** 0.9
    f = cv2.cvtColor(np.dstack([hue, sat, val]), cv2.COLOR_HSV2BGR)
    f *= np.array([0.82, 0.96, 1.10], np.float32)      # warm afternoon
    return np.clip(f, 0, 1)


def window_mask(src, person):
    """Window = the bluish roller blinds + blown-out glass, filled to its hull."""
    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV).astype(np.int16)
    hue, sat, val = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    blind = (hue > 80) & (hue < 130) & (sat > 12) & (sat < 95) & (val > 150)
    glass = val > 238
    top = np.zeros((H, W), bool)
    top[: int(H * 0.66)] = True
    m = ((blind | glass) & top & (person < 0.3)).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((31, 31), np.uint8))
    num, lab, st, _ = cv2.connectedComponentsWithStats(m)
    keep = np.zeros_like(m)
    for i in range(1, num):
        x, y, w, h, a = st[i]
        if a > 9000 and w > 120 and h > 60:
            cnts, _ = cv2.findContours((lab == i).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            hull = cv2.convexHull(np.vstack(cnts))
            cv2.fillConvexPoly(keep, hull, 1)
    keep[person > 0.3] = 0
    return cv2.GaussianBlur(keep.astype(np.float32), (0, 0), 1.5)


def background(src, person):
    ms = meanshift(src, 12, 26).astype(np.float32)
    soft = cv2.GaussianBlur(src, (0, 0), 3).astype(np.float32)
    paint = 0.65 * ms + 0.35 * soft
    f = grade_bg(np.clip(paint, 0, 255).astype(np.uint8))
    # gouache: pigment pooling at patch edges, brush texture, paper
    lum = cv2.cvtColor((f * 255).astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32)
    edge = cv2.morphologyEx(lum, cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8))
    edge = cv2.GaussianBlur(np.clip(edge / 40, 0, 1), (0, 0), 1.2)
    f *= (1 - 0.10 * edge)[..., None]
    f *= (1 + 0.014 * BRUSH + 0.03 * PAPER)[..., None]
    f *= (1 + DRIFT[..., None] * np.array([0.10, 0.02, -0.08], np.float32))   # warm/cool wash
    win = window_mask(src, person)
    sky = (SKY / 255) * (1 + 0.012 * BRUSH + 0.025 * PAPER)[..., None]
    f = f * (1 - win[..., None]) + sky * win[..., None]
    return np.clip(f, 0, 1), win


def xdog(gray, s=1.0, k=1.6, p=22, eps=-0.02, phi=12):
    g1 = cv2.GaussianBlur(gray, (0, 0), s)
    g2 = cv2.GaussianBlur(gray, (0, 0), s * k)
    d = (1 + p) * g1 - p * g2
    return np.where(d >= eps, 1.0, 1 + np.tanh(phi * (d - eps)))


def characters(src, mask):
    ms = meanshift(src, 8, 28).astype(np.float32) / 255
    # gentle anime colour: warmer, slightly lighter, moderate saturation
    hsv = cv2.cvtColor(ms, cv2.COLOR_BGR2HSV)
    hsv[..., 1] = np.clip(hsv[..., 1] * 1.15, 0, 1)
    hsv[..., 2] = np.clip(hsv[..., 2] * 1.06 + 0.05, 0, 1)
    base = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR) * np.array([0.92, 0.98, 1.05], np.float32)
    # one hard-edged shadow shape where the source is darker than its surroundings
    lum = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY).astype(np.float32)
    local = cv2.GaussianBlur(lum, (0, 0), 22)
    hsv0 = cv2.cvtColor(src, cv2.COLOR_BGR2HSV).astype(np.float32)
    skin = ((hsv0[..., 0] < 22) & (hsv0[..., 1] > 50) & (hsv0[..., 1] < 170) & (hsv0[..., 2] > 90)).astype(np.float32)
    skin = cv2.GaussianBlur(skin, (0, 0), 6)
    thr = local - 8 - 10 * skin
    sh = (cv2.GaussianBlur(lum, (0, 0), 4) < thr).astype(np.uint8)
    sh = cv2.morphologyEx(sh, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
    sh = cv2.medianBlur(sh * 255, 15).astype(np.float32) / 255
    sh = cv2.GaussianBlur(sh, (0, 0), 0.8)
    shadow = base * np.array([0.84, 0.74, 0.78], np.float32)      # warm violet shade
    cel = base * (1 - sh[..., None]) + shadow * sh[..., None]
    # hair sheen: one soft light band on the top of very dark regions
    dark = (lum < 70).astype(np.float32) * mask
    sheen = np.clip(cv2.GaussianBlur(dark, (0, 0), 3) - cv2.GaussianBlur(np.roll(dark, 14, 0), (0, 0), 3), 0, 1)
    cel += 0.18 * sheen[..., None] * np.array([1.0, 0.9, 0.85])
    # thin brown line art
    gray = cv2.cvtColor((np.clip(ms, 0, 1) * 255).astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
    detail = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
    lines = np.minimum(xdog(gray, 1.3), xdog(detail, 1.1, p=16, eps=-0.06))
    ink = (lines < 0.5).astype(np.uint8)
    num, lab, st, _ = cv2.connectedComponentsWithStats(ink, connectivity=8)
    small = st[:, cv2.CC_STAT_AREA] < 22
    small[0] = False
    ink[small[lab]] = 0
    m8 = (mask > 0.5).astype(np.uint8)
    sil = cv2.morphologyEx(m8, cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8))
    inner = cv2.erode(m8, np.ones((5, 5), np.uint8))
    # facial features as solid dark shapes: small dark blobs surrounded by skin
    near_skin = cv2.GaussianBlur(skin, (0, 0), 10) > 0.25
    feat = ((lum < np.minimum(100, 0.62 * cv2.GaussianBlur(lum, (0, 0), 15))) & near_skin & (mask > 0.5)).astype(np.uint8)
    num, lab, st, _ = cv2.connectedComponentsWithStats(feat, connectivity=8)
    okf = (st[:, cv2.CC_STAT_AREA] > 12) & (st[:, cv2.CC_STAT_AREA] < 2200)
    okf[0] = False
    feat = okf[lab].astype(np.uint8)
    ink = np.maximum(np.maximum(ink * inner, sil), feat).astype(np.float32)
    ink = cv2.GaussianBlur(ink, (0, 0), 0.6)
    line_col = np.array([0.16, 0.20, 0.28], np.float32)            # dark sepia (BGR)
    cel = cel * (1 - 0.92 * ink[..., None]) + line_col * 0.92 * ink[..., None]
    return np.clip(cel, 0, 1)


def render(n):
    src = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png"))
    mask = read_mask(n)
    bg, win = background(src, mask)
    ch = characters(src, mask)
    m = cv2.GaussianBlur(mask, (0, 0), 0.8)[..., None]
    img = bg * (1 - m) + ch * m
    # warm sunlight spilling from the window + soft falloff into the room
    glow = cv2.GaussianBlur(win, (0, 0), 60)
    glow = glow / (glow.max() + 1e-6)
    img = img + 0.30 * glow[..., None] * np.array([0.45, 0.80, 1.0], np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    fall = 1 - 0.12 * (yy / H) - 0.06 * np.abs(xx / W - 0.45)
    img *= fall[..., None]
    # bloom on highlights
    hi = np.clip(img - 0.78, 0, 1)
    img = img + 0.5 * cv2.GaussianBlur(hi, (0, 0), 12)
    # print softness + very light grain
    img = cv2.GaussianBlur(img, (0, 0), 0.6)
    img += np.random.default_rng(n).normal(0, 0.008, (H, W, 1)).astype(np.float32)
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
