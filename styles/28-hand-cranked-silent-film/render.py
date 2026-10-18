"""Hand-cranked silent film (1910s-20s), frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [frame numbers...]

Orthochromatic-looking monochrome, sepia toned, soft old lens with highlight
halation, hot-centre / burnt-edge vignette, rounded projector gate, coarse
grain, per-frame exposure flicker, gate weave, vertical scratches, dust and
hairs. The final section closes in a soft iris around the main subject.
Timing is never touched: each source frame gives exactly one film frame.
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np

FRAMES, MASKS, OUT = sys.argv[1:4]
ONLY = [int(a) for a in sys.argv[4:]] or [13, 49, 85, 109, 145, 178]

# sepia toning ramp, BGR 0..1 (shadow -> mid -> paper)
RAMP = np.array([
    [0.035, 0.055, 0.085],
    [0.16, 0.25, 0.34],
    [0.42, 0.56, 0.68],
    [0.74, 0.86, 0.93],
    [0.86, 0.95, 0.99],
], np.float32)
IRIS_FROM = 157            # iris closes in on the main subject from this frame on
SCRATCH_SEED = [(1, 60), (61, 120), (121, 999)]   # scratches persist (and drift) within a reel section


def tone_map(g):
    x = g * (len(RAMP) - 1)
    i = np.clip(np.floor(x).astype(int), 0, len(RAMP) - 2)
    f = (x - i)[..., None]
    return RAMP[i] * (1 - f) + RAMP[i + 1] * f


def section(n):
    for k, (a, b) in enumerate(SCRATCH_SEED):
        if a <= n <= b:
            return k, a
    return 0, 1


def render(n):
    rng = np.random.default_rng(3000 + n)
    img = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png"))
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), 0).astype(np.float32) / 255
    h, w = m.shape

    # orthochromatic-ish: blue/green heavy, reds go dark (skin a bit darker, lips/shirts deep)
    b, gch, r = [c.astype(np.float32) / 255 for c in cv2.split(img)]
    g = 0.38 * b + 0.47 * gch + 0.15 * r
    g = cv2.GaussianBlur(g, (0, 0), 1.3)                       # soft period lens
    # contrasty but with milky blacks and rolled-off highlights
    g = np.clip((g - 0.06) / 0.86, 0, 1)
    g = g * g * (3 - 2 * g)
    g = 0.06 + 0.9 * g

    # exposure flicker (hand cranking = uneven exposure) + side-to-side density drift
    flick = rng.uniform(0.88, 1.10)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    side = 1 + rng.uniform(-0.05, 0.05) * (xx / w - 0.5) * 2
    g = g * flick * side

    # halation: highlights bleed
    hl = cv2.GaussianBlur(np.clip(g - 0.7, 0, 1), (0, 0), 14)
    g = g + hl * 0.8

    # hot centre + burnt edges
    cx, cy = w * 0.5 + rng.normal(0, 8), h * 0.45 + rng.normal(0, 8)
    rr = np.sqrt(((xx - cx) / (w * 0.62)) ** 2 + ((yy - cy) / (h * 0.62)) ** 2)
    g = g * (1.08 - 0.62 * np.clip(rr - 0.35, 0, 1) ** 1.4)

    # iris on the main subject in the last section
    if n >= IRIS_FROM:
        ys, xs = np.nonzero(m > 0.5)
        if len(xs):
            sel = xs > np.percentile(xs, 40)                     # the person nearest the right/centre
            fx, fy = xs[sel].mean(), np.percentile(ys[sel], 25)
            prog = min(1.0, (n - IRIS_FROM) / 22)
            R = h * (0.95 - 0.42 * prog)
            d = np.sqrt((xx - fx) ** 2 + (yy - fy) ** 2)
            iris = np.clip((R - d) / 60, 0, 1)
            g = g * (0.04 + 0.96 * iris)

    # coarse, clumpy grain (changes every frame)
    gr = cv2.GaussianBlur(rng.normal(0, 1, (h, w)).astype(np.float32), (0, 0), 1.1)
    gr2 = cv2.resize(rng.normal(0, 1, (h // 3, w // 3)).astype(np.float32), (w, h))
    g = g + (gr * 0.06 + gr2 * 0.025) * (0.4 + 0.6 * np.clip(g, 0, 1))

    # scratches: a few vertical lines that persist and drift through a reel section
    sec, start = section(n)
    srng = np.random.default_rng(77 + sec)
    for _ in range(srng.integers(2, 4)):
        x0 = srng.uniform(0.05, 0.95) * w + (n - start) * srng.uniform(-3, 3) + rng.normal(0, 2)
        if rng.random() < 0.75:
            wid = srng.uniform(0.8, 2.0)
            prof = np.exp(-((xx[0] - x0) / wid) ** 2)
            col = 0.45 if srng.random() < 0.6 else -0.35
            g = g + col * prof[None, :] * rng.uniform(0.5, 1.0)
    # dust specks + a hair now and then (different every frame)
    dust = np.zeros((h, w), np.float32)
    for _ in range(rng.integers(25, 60)):
        p = (int(rng.uniform(0, w)), int(rng.uniform(0, h)))
        cv2.circle(dust, p, int(rng.integers(1, 4)), float(rng.choice([1, -1])), -1, cv2.LINE_AA)
    if rng.random() < 0.6:
        pts = np.cumsum(rng.normal(0, 6, (25, 2)), 0) + [rng.uniform(0, w), rng.uniform(0, h)]
        cv2.polylines(dust, [pts.astype(np.int32)], False, -1.0, 1, cv2.LINE_AA)
    g = g + cv2.GaussianBlur(dust, (0, 0), 0.7) * 0.5

    out = tone_map(np.clip(g, 0, 1))

    # gate weave: the whole frame jitters a few pixels and a hair of rotation
    M = cv2.getRotationMatrix2D((w / 2, h / 2), rng.normal(0, 0.12), 1.0)
    M[:, 2] += [rng.normal(0, 2.5), rng.normal(0, 3.5)]
    out = cv2.warpAffine(out, M, (w, h), borderMode=cv2.BORDER_CONSTANT, borderValue=(0.02, 0.03, 0.04))

    # rounded projector gate
    gate = np.zeros((h, w), np.float32)
    pad, rad = 10, 60
    cv2.rectangle(gate, (pad + rad, pad), (w - pad - rad, h - pad), 1, -1)
    cv2.rectangle(gate, (pad, pad + rad), (w - pad, h - pad - rad), 1, -1)
    for c in [(pad + rad, pad + rad), (w - pad - rad, pad + rad), (pad + rad, h - pad - rad), (w - pad - rad, h - pad - rad)]:
        cv2.circle(gate, c, rad, 1, -1, cv2.LINE_AA)
    gate = cv2.GaussianBlur(gate, (0, 0), 4)[..., None]
    out = out * gate + np.array([0.02, 0.03, 0.04], np.float32) * (1 - gate)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), (out.clip(0, 1) * 255).astype(np.uint8))
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    with Pool(min(6, os.cpu_count() or 2)) as p:
        for n in p.imap_unordered(render, ONLY):
            print("frame", n)
