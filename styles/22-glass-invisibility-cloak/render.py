"""Glass invisibility cloak restyle, frame by frame.

usage: python render.py <frames_dir> <masks_dir> <plate_png> <out_dir> [frame numbers...]
<plate_png> is the clean background plate from plate.py (people removed).
Each person becomes a transparent glass body: the room behind them shows
through, bent by the body's shape (edge lensing) and by the person's own
light/dark detail (the After Effects displacement-map trick), with a cold rim
light, chromatic fringe and a shimmer that changes every frame.
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np

FRAMES, MASKS, PLATE, OUT = sys.argv[1:5]
ONLY = [int(a) for a in sys.argv[5:]]
N = len([f for f in os.listdir(FRAMES) if f.endswith(".png")])

CLOAK_IN = (1, 26)          # cloak sweeps on, top to bottom
FLICKER = {104: 0.55, 105: 0.25, 108: 0.35, 109: 0.6, 110: 0.2}   # decloak glitch: visibility


def vnoise(rng, h, w, cell):
    a = rng.random((max(2, h // cell + 2), max(2, w // cell + 2))).astype(np.float32)
    return cv2.resize(a, (w, h), interpolation=cv2.INTER_CUBIC)


def grad(a):
    gx = cv2.Sobel(a, cv2.CV_32F, 1, 0, ksize=3) / 8
    gy = cv2.Sobel(a, cv2.CV_32F, 0, 1, ksize=3) / 8
    return gx, gy


def sample(img, mx, my):
    return cv2.remap(img, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


def render(n):
    rng = np.random.default_rng(7000 + n)
    frame = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png")).astype(np.float32) / 255
    plate = cv2.imread(PLATE).astype(np.float32) / 255
    mask = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
    h, w = mask.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)

    m = cv2.GaussianBlur(mask, (0, 0), 1.5)
    hard = (m > 0.5).astype(np.uint8)
    # glass thickness: a dome that rises fast at the silhouette and flattens inside
    d = cv2.distanceTransform(hard, cv2.DIST_L2, 5)
    T = np.sqrt(np.clip(d / 55.0, 0, 1))
    T = cv2.GaussianBlur(T, (0, 0), 3)
    tx, ty = grad(T)

    # the person's own luminance as a displacement map (keeps a ghost of face, glasses, stripes)
    L = cv2.cvtColor((frame * 255).astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
    Lb = cv2.GaussianBlur(L, (0, 0), 3.5)
    lx, ly = grad(Lb)

    # living shimmer: slow ripples that change every frame
    t = n / 12
    rip = (np.sin(xx / 23 + t * 5.1 + np.sin(yy / 41) * 2) + np.sin(yy / 31 - t * 4.3 + np.sin(xx / 57) * 2)) * 0.5
    nz = vnoise(rng, h, w, 26) - 0.5
    sx = rip * 2.2 + nz * 4
    sy = np.roll(rip, 9, 0) * 2.2 + np.roll(nz, 17, 1) * 4

    dx = -tx * 1400 + lx * 1100 + sx
    dy = -ty * 1400 + ly * 1100 + sy
    dx *= m
    dy *= m

    # chromatic split: each channel bends a little differently
    glass = np.zeros_like(plate)
    for c, k in enumerate((1.10, 1.0, 0.90)):
        glass[..., c] = sample(plate[..., c], xx + dx * k, yy + dy * k)
    glass = cv2.GaussianBlur(glass, (0, 0), 0.9)
    glass = glass * np.array([1.03, 1.0, 0.96], np.float32) * 0.94 + 0.02    # faint cold tint, slight absorption

    # rim light from top-left + thin dark refraction line just inside the edge
    nx, ny = -tx * 60 - lx * 12, -ty * 60 - ly * 12
    nl = np.clip((nx * -0.6 + ny * -0.8), 0, None)
    edge = np.clip(np.hypot(tx, ty) * 40, 0, 1)
    edge_zone = np.clip(1 - d / 7.0, 0, 1) * (d > 0)
    rim = np.clip(nl, 0, 1) ** 2.2 * edge_zone
    dark = np.clip(edge - 0.35, 0, 1) * 0.35
    # sparkles from the person's fine detail (eyes, glasses rims, stripes, hair)
    hp = L - cv2.GaussianBlur(L, (0, 0), 2.5)
    spark = np.clip(hp * 6 - 0.3, 0, 1) * (0.55 + 0.45 * vnoise(rng, h, w, 9))
    caustic = np.clip(vnoise(rng, h, w, 60) - 0.8, 0, 1) * T

    g = glass * (1 - dark[..., None])
    g = g + (rim * 0.55 + spark * 0.22 + caustic * 0.12)[..., None] * np.array([1.0, 0.98, 0.93], np.float32)

    # how visible the real person still is (0 = fully cloaked)
    vis = np.zeros((h, w), np.float32)
    band = np.zeros((h, w), np.float32)
    if CLOAK_IN[0] <= n <= CLOAK_IN[1]:
        p = (n - CLOAK_IN[0]) / (CLOAK_IN[1] - CLOAK_IN[0])
        front = -0.1 * h + p * 1.25 * h + (vnoise(np.random.default_rng(3), h, w, 90) - 0.5) * 70
        vis = np.clip((yy - front) / 26, 0, 1)
        band = np.exp(-((yy - front) / 14) ** 2)
    if n in FLICKER:
        vis[:] = FLICKER[n]
        # glitch: horizontal slices of the decloaking body slip sideways
        rows = (vnoise(rng, h, 1, 11)[:, 0] > 0.62).astype(np.float32)[:, None] * np.ones((1, w), np.float32)
        shift = rng.integers(-28, 28)
        person_src = np.where(rows[..., None] > 0, np.roll(frame, shift, 1), frame)
        band = rows * 0.35

    person = (person_src if n in FLICKER else frame) * (1 - 0.15 * band[..., None])
    inside = g * (1 - vis[..., None]) + person * vis[..., None]
    # energy band where the cloak is switching on: electric cyan-white shimmer
    inside += (band * (0.5 + 0.5 * vnoise(rng, h, w, 5)))[..., None] * np.array([1.0, 0.95, 0.55], np.float32) * 0.8

    out = frame * (1 - m[..., None]) + inside * m[..., None]
    # outside the body the room is untouched; add only the camera's own grain
    out += rng.normal(0, 0.012, (h, w, 1)).astype(np.float32)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), (out.clip(0, 1) * 255).astype(np.uint8))
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    todo = ONLY or list(range(1, N + 1))
    with Pool(min(8, os.cpu_count() or 4)) as pool:
        for n in pool.imap_unordered(render, todo):
            print(n, end=" ", flush=True)
    print()
