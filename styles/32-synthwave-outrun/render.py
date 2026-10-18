"""Synthwave Outrun: 80s retrowave restyle, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [frame numbers... | all]

The room is replaced by a synthwave set: a violet-to-magenta sky with stars,
a striped retro sun behind the group, wireframe mountains on the horizon and
a glowing magenta grid floor that scrolls toward camera. The people stay
photographic but are graded into the palette (indigo shadows, hot-pink mids,
peach highlights) and lit by two neon rims: cyan from the left, magenta from
the right, with a chrome-white specular line on the edge. Bloom, CRT
scanlines and a slight chroma shift finish it. Per frame: the grid scrolls,
the sun's stripe gaps drift up, stars twinkle, the rim flickers a little and
the scanline phase rolls.
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

# BGR 0..1
SKY_TOP = np.array([0.20, 0.03, 0.08], np.float32)       # near-black indigo
SKY_MID = np.array([0.45, 0.06, 0.38], np.float32)       # violet
SKY_LOW = np.array([0.50, 0.12, 0.95], np.float32)       # hot magenta-pink
SUN_TOP = np.array([0.30, 0.90, 1.00], np.float32)       # yellow
SUN_LOW = np.array([0.55, 0.15, 1.00], np.float32)       # pink
GRID = np.array([0.95, 0.25, 1.00], np.float32)          # neon magenta
GRID2 = np.array([1.00, 0.85, 0.20], np.float32)         # cyan (horizon line)
CYAN = np.array([1.00, 0.90, 0.25], np.float32)
MAGENTA = np.array([0.85, 0.20, 1.00], np.float32)
HORIZON = 0.60


def smoothstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def sky(h, w, rng):
    y = np.linspace(0, 1, h, dtype=np.float32)[:, None, None] / HORIZON
    t1 = smoothstep(0.0, 0.65, y)
    t2 = smoothstep(0.55, 1.0, y)
    col = SKY_TOP * (1 - t1) + SKY_MID * t1
    col = col * (1 - t2) + SKY_LOW * t2
    img = np.ascontiguousarray(np.broadcast_to(col, (h, w, 3)), np.float32).copy()
    # stars: fixed field, each twinkles per frame
    srng = np.random.default_rng(7)
    k = 260
    xs = srng.integers(0, w, k)
    ys = (srng.random(k) ** 1.6 * HORIZON * h * 0.75).astype(int)
    br = srng.uniform(0.3, 1.0, k) * rng.uniform(0.4, 1.0, k)
    for x, yy, b in zip(xs, ys, br):
        cv2.circle(img, (int(x), int(yy)), 1, (float(b), float(b) * 0.9, float(b)), -1, cv2.LINE_AA)
    return img


def sun(img, h, w, n, cx):
    R = int(h * 0.30)
    cy = int(h * HORIZON) - int(R * 0.55)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    disc = np.clip(R - d + 1, 0, 1)
    v = np.clip((yy - (cy - R)) / (2 * R), 0, 1)[..., None]
    col = SUN_TOP * (1 - v) + SUN_LOW * v
    # stripe gaps: start just above the middle, thicker toward the bottom, drift up
    rel = (yy - cy) / R
    phase = (n * 0.035) % 1
    band = (rel * 7 + phase) % 1
    gap = np.clip((rel + 0.05) * 0.55, 0, 0.55)
    cut = (band < gap) & (rel > -0.05)
    disc = disc * (~cut)
    glow = cv2.GaussianBlur(np.clip(R * 1.05 - d, 0, 1).astype(np.float32), (0, 0), 40)[..., None]
    img = img + glow * np.array([0.25, 0.10, 0.6], np.float32) * 0.9
    return img * (1 - disc[..., None]) + col * disc[..., None]


def mountains(img, h, w):
    hy = int(h * HORIZON)
    mrng = np.random.default_rng(11)
    layer = np.zeros((h, w), np.float32)
    edges = np.zeros((h, w), np.float32)
    for side, (x0, x1) in enumerate([(0, int(w * 0.42)), (int(w * 0.58), w)]):
        xs = np.linspace(x0, x1, 9)
        ys = hy - mrng.uniform(0.04, 0.16, 9) * h
        ys[-1 if side == 0 else 0] = hy
        pts = np.stack([xs, ys], 1).astype(np.int32)
        poly = np.vstack([[[x0, hy]], pts, [[x1, hy]]]).astype(np.int32)
        cv2.fillPoly(layer, [poly], 1.0, cv2.LINE_AA)
        cv2.polylines(edges, [pts], False, 1.0, 2, cv2.LINE_AA)
        for (px, py) in pts[1:-1]:          # wireframe ribs down the slopes
            cv2.line(edges, (int(px), int(py)), (int(px + mrng.uniform(-40, 40)), hy), 0.6, 1, cv2.LINE_AA)
    base = np.array([0.22, 0.02, 0.12], np.float32)
    img = img * (1 - layer[..., None]) + base * layer[..., None]
    img = img + edges[..., None] * MAGENTA * 0.9 + cv2.GaussianBlur(edges, (0, 0), 4)[..., None] * MAGENTA * 0.6
    return img


def floor(img, h, w, n):
    hy = h * HORIZON
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    below = yy > hy + 1
    dy = np.maximum(yy - hy, 1.0)
    z = 90.0 / dy                                   # depth
    zl = (z + n * 0.11) * 2.0                       # grid scrolls toward camera
    fz = np.abs((zl % 1) - 0.5) * 2                 # 1 on a line
    dzz = 90.0 / dy ** 2 * 2.0                      # derivative -> anti-aliased width
    hline = np.clip(1 - (1 - fz) / np.maximum(dzz * 1.6, 0.02), 0, 1)
    xw = (xx - w / 2) * z / 90.0 * 2.2
    fx = np.abs((xw % 1) - 0.5) * 2
    dxx = z / 90.0 * 2.2
    vline = np.clip(1 - (1 - fx) / np.maximum(dxx * 1.8, 0.02), 0, 1)
    fade = np.clip((yy - hy) / (h * 0.06), 0, 1)
    lines = np.maximum(hline, vline) * below * (0.35 + 0.65 * fade)
    base = SKY_TOP * 0.6 + np.array([0.10, 0.0, 0.10], np.float32)
    ground = base * (1 + 0.6 * (1 - fade))[..., None]
    img = np.where(below[..., None], ground, img)
    img = img + lines[..., None] * GRID + cv2.GaussianBlur(lines, (0, 0), 5)[..., None] * GRID * 0.8
    hl = np.exp(-((yy - hy) / 2.0) ** 2)            # bright cyan horizon line
    img = img + hl[..., None] * GRID2 * 0.9 + cv2.GaussianBlur(hl, (0, 0), 8)[..., None] * GRID2 * 0.5
    return img


def grade_subject(img):
    L = cv2.cvtColor(np.clip(img, 0, 1), cv2.COLOR_BGR2GRAY)
    L = cv2.createCLAHE(2.0, (8, 8)).apply((L * 255).astype(np.uint8)).astype(np.float32) / 255
    # gradient map indigo -> hot pink -> peach, with a little original colour mixed back
    lo = np.array([0.35, 0.05, 0.12], np.float32)
    mid = np.array([0.55, 0.20, 0.85], np.float32)
    hi = np.array([0.80, 0.85, 1.00], np.float32)
    t = L[..., None]
    a = np.clip(t * 2, 0, 1)
    b = np.clip(t * 2 - 1, 0, 1)
    gm = np.where(t < 0.5, lo * (1 - a) + mid * a, mid * (1 - b) + hi * b)
    return gm * 0.62 + img * 0.38


def render(n):
    rng = np.random.default_rng(3200 + n)
    src = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png")).astype(np.float32) / 255
    m8 = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), 0)
    # drop small matte debris (it would glow as neon specks)
    num, lab, st, _ = cv2.connectedComponentsWithStats((m8 > 127).astype(np.uint8))
    keep = np.zeros(num, bool)
    keep[1:] = st[1:, cv2.CC_STAT_AREA] > 6000
    m = (m8.astype(np.float32) / 255) * keep[lab]
    h, w = m.shape

    # sun sits behind the group's centre of mass (half-way to frame centre)
    cols = m.sum(0)
    cx = float((cols * np.arange(w)).sum() / max(cols.sum(), 1))
    cx = 0.5 * cx + 0.5 * w / 2
    bg = sky(h, w, rng)
    bg = sun(bg, h, w, n, cx)
    bg = mountains(bg, h, w)
    bg = floor(bg, h, w, n)

    subj = grade_subject(src)
    # neon rims from the matte normal: cyan from the left, magenta from the right
    mb = cv2.GaussianBlur(m, (0, 0), 2.0)
    ms = cv2.GaussianBlur(m, (0, 0), 6)
    gx = cv2.Sobel(ms, cv2.CV_32F, 1, 0, ksize=5)
    gy = cv2.Sobel(ms, cv2.CV_32F, 0, 1, ksize=5)
    dist = cv2.distanceTransform((m > 0.5).astype(np.uint8), cv2.DIST_L2, 5)
    band = np.clip(1 - dist / 22.0, 0, 1) ** 1.5 * (m > 0.5)
    left = cv2.GaussianBlur(np.clip(gx * 30, 0, 1), (0, 0), 8)    # matte rises left->right
    right = cv2.GaussianBlur(np.clip(-gx * 30, 0, 1), (0, 0), 8)
    flick = rng.uniform(0.85, 1.05)
    rimL = np.clip(band * left * 4, 0, 1)[..., None] * flick
    rimR = np.clip(band * right * 4, 0, 1)[..., None] * flick
    top = np.clip(band * cv2.GaussianBlur(np.clip(gy * 30, 0, 1), (0, 0), 8) * 3, 0, 1)[..., None]
    lum = cv2.cvtColor(np.clip(src, 0, 1), cv2.COLOR_BGR2GRAY)[..., None]
    subj = subj + rimL * CYAN * (0.55 + 0.6 * lum) + rimR * MAGENTA * (0.55 + 0.6 * lum)
    subj = subj + top * np.array([0.45, 0.6, 1.0], np.float32) * 0.45     # sun top-light
    spec = np.clip(1 - dist / 3.0, 0, 1) * (m > 0.5) * np.clip(left + right + 0.3, 0, 1)
    subj = subj + spec[..., None] * 0.6                                    # chrome edge

    out = bg * (1 - mb[..., None]) + subj * mb[..., None]
    # neon light spilling from the rim onto the set
    halo = cv2.GaussianBlur(np.clip(m - cv2.erode(m, np.ones((5, 5), np.uint8)), 0, 1), (0, 0), 14)
    lc = np.clip(left * 3, 0, 1)[..., None]
    out = out + halo[..., None] * (CYAN * lc + MAGENTA * (1 - lc)) * 0.6 * (1 - mb[..., None])

    hi = np.clip(out - 0.6, 0, None)                                      # bloom
    out = out + cv2.GaussianBlur(hi, (0, 0), 12) * 0.7 + cv2.GaussianBlur(hi, (0, 0), 40) * 0.5
    out[..., 2] = np.roll(out[..., 2], 2, 1)                              # CRT convergence error
    out[..., 0] = np.roll(out[..., 0], -2, 1)
    yy = np.arange(h, dtype=np.float32)[:, None, None]                    # rolling scanlines
    out = out * (0.86 + 0.14 * (np.sin((yy + n * 1.5) * np.pi / 2.0) ** 2))
    out = out * (1 + rng.normal(0, 0.012))
    out = out + rng.normal(0, 0.02, (h, w, 1)).astype(np.float32)
    Y, X = np.mgrid[0:h, 0:w].astype(np.float32)
    r = np.sqrt(((X - w / 2) / (w / 2)) ** 2 + ((Y - h / 2) / (h / 2)) ** 2)
    out = out * (1 - 0.3 * np.clip(r - 0.6, 0, 1))[..., None]
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), (np.clip(out, 0, 1) * 255).astype(np.uint8))
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    with Pool(min(8, os.cpu_count() or 2)) as p:
        for n in p.imap_unordered(render, ONLY):
            print("frame", n, flush=True)
