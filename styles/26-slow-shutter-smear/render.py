"""12 fps slow-shutter / step-print smear, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [frame numbers...]

Every output frame is a fake long exposure: the current frame stays readable,
earlier frames are stacked behind it as discrete stepped echoes (step printing),
and every layer is streaked along its own optical-flow motion (not a flat
directional blur). Static areas stay sharp because identical pixels average to
themselves. The colour grade is left untouched apart from a light highlight
bloom on the trails and fine grain.
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np

FRAMES, MASKS, OUT = sys.argv[1:4]
ONLY = [int(a) for a in sys.argv[4:]] or [13, 49, 85, 109, 145, 178]
N = len([f for f in os.listdir(FRAMES) if f.endswith(".png")])

ECHOES = [(10, 0.22), (8, 0.28), (6, 0.34), (4, 0.42), (2, 0.50)]  # (frames back, opacity), oldest first
# camera drag during the exposure: (first frame, last frame, dx, dy) in px per frame back
DRAG = [(1, 40, 7.0, 1.0), (41, 80, -6.5, 2.0), (81, 120, 7.5, -1.2), (121, 999, -7.0, -0.8)]
FLOW_SCALE = 0.5
STREAK = 2.4          # streak length, in multiples of the frame-to-frame motion
SAMPLES = 10


def load(n):
    n = min(max(n, 1), N)
    return cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png")).astype(np.float32) / 255


def mask(n):
    n = min(max(n, 1), N)
    return cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), 0).astype(np.float32) / 255


def flow(a, b):
    """Dense flow from frame a to frame b at reduced resolution, returned full size (pixels)."""
    h, w = a.shape[:2]
    sa = cv2.resize(cv2.cvtColor((a * 255).astype(np.uint8), cv2.COLOR_BGR2GRAY), None, fx=FLOW_SCALE, fy=FLOW_SCALE)
    sb = cv2.resize(cv2.cvtColor((b * 255).astype(np.uint8), cv2.COLOR_BGR2GRAY), None, fx=FLOW_SCALE, fy=FLOW_SCALE)
    f = cv2.calcOpticalFlowFarneback(sa, sb, None, 0.5, 4, 25, 4, 7, 1.5, 0)
    f = cv2.GaussianBlur(f, (0, 0), 3)
    return cv2.resize(f, (w, h)) / FLOW_SCALE


def streak(img, f, length, rng):
    """Smear img backwards along its own motion vectors (per-pixel line integral)."""
    h, w = img.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    acc = np.zeros_like(img)
    wsum = 0.0
    for i in range(SAMPLES):
        t = i / (SAMPLES - 1)
        wt = 1.0 - 0.75 * t                       # heavier at the leading edge
        jit = rng.normal(0, 0.15)
        mx = xx + f[..., 0] * length * (t + jit * t)
        my = yy + f[..., 1] * length * (t + jit * t)
        acc += cv2.remap(img, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT) * wt
        wsum += wt
    return acc / wsum


def drag_of(n):
    for a, b, dx, dy in DRAG:
        if a <= n <= b:
            return dx, dy
    return 0.0, 0.0


def shift(img, dx, dy):
    m = np.float32([[1, 0, dx], [0, 1, dy]])
    return cv2.warpAffine(img, m, (img.shape[1], img.shape[0]), borderMode=cv2.BORDER_REFLECT)


def render(n):
    rng = np.random.default_rng(1000 + n)
    cur = load(n)
    h, w = cur.shape[:2]
    shutter = rng.uniform(0.9, 1.15)               # each "exposure" is a little different
    dx, dy = drag_of(n)
    # background: one long exposure of the plate, lightly dragged
    bg = np.zeros_like(cur)
    for k in range(0, 7):
        bg += shift(load(n - k), dx * k * 0.35, dy * k * 0.35)
    bg = bg / 7 * 0.6 + cur * 0.4
    out = bg
    # stepped echoes of the people, oldest first, each streaked along its own motion
    for back, op in ECHOES:
        a = load(n - back)
        f = flow(a, load(n - back - 1))
        sm = streak(a, f, STREAK * shutter, rng)
        ma = cv2.GaussianBlur(mask(n - back), (0, 0), 3)
        ma = np.maximum(ma, streak(ma[..., None].repeat(3, 2), f, STREAK * shutter, rng)[..., 0])
        sx, sy = dx * back * shutter, dy * back * shutter
        sm, ma = shift(sm, sx, sy), shift(ma, sx, sy)
        al = (ma * op)[..., None]
        out = out * (1 - al) + sm * al
    # the leading exposure on top: crisp, with only a short smear of its own motion
    m = cv2.GaussianBlur(mask(n), (0, 0), 2.5)[..., None]
    fl = flow(cur, load(n - 1))
    fast = np.clip((np.hypot(fl[..., 0], fl[..., 1]) - 6.0) / 16.0, 0, 1)[..., None]   # fast parts smear
    sm = streak(cur, fl, STREAK * 1.3, rng)
    lead = cur * (1 - fast) + sm * fast
    lead = lead * 0.88 + sm * 0.12
    al = m * (0.9 - 0.25 * fast)
    out = out * (1 - al) + lead * al
    # long-exposure highlight drag: bright trail pixels bloom a little (lighten blend)
    lum = cv2.cvtColor(out, cv2.COLOR_BGR2GRAY)
    glow = cv2.GaussianBlur(np.clip(out - 0.75, 0, 1), (0, 0), 9) * 0.9
    out = out + glow * (lum[..., None] > 0.45)

    # subtle softness + grain (12 fps cine look), grade untouched
    out = cv2.addWeighted(out, 0.85, cv2.GaussianBlur(out, (0, 0), 1.2), 0.15, 0)
    g = cv2.GaussianBlur(rng.normal(0, 1, (h, w)).astype(np.float32), (0, 0), 0.7)
    out += g[..., None] * 0.018
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), (out.clip(0, 1) * 255).astype(np.uint8))
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    with Pool(min(6, os.cpu_count() or 2)) as p:
        for n in p.imap_unordered(render, ONLY):
            print("frame", n)
