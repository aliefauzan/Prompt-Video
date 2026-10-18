"""Broken Mirror Shards restyle, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [frame numbers... | all]

The frame is seen in a cracked mirror. Each section has its own impact point,
set on the upper body of the largest person. Radial cracks and irregular
rings around that point cut the glass into shards. Each shard reflects the
frame with its own small rotation, scale and shift. Some shards reflect a
moment 1-4 frames earlier, so one face does not agree with itself. Crack
edges get a dark seam and a bright glass highlight, and the area right at
the impact is crushed white. The glass holds still within a section. The
cracks grow over the first three frames of each section, and the glints
drift every frame.
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np

FRAMES, MASKS, OUT = sys.argv[1:4]
ARGS = sys.argv[4:]
N = len([f for f in os.listdir(FRAMES) if f.endswith(".png")])
SECTIONS = [(1, 36), (37, 72), (73, 106), (107, 142), (143, 999)]


def section(n):
    for i, (a, b) in enumerate(SECTIONS):
        if a <= n <= b:
            return i, a
    return len(SECTIONS) - 1, SECTIONS[-1][0]


def load(n):
    n = min(max(n, 1), N)
    return cv2.imread(f"{FRAMES}/frame_{n:03d}.png").astype(np.float32) / 255


def impact(first):
    m = cv2.imread(f"{MASKS}/frame_{first:03d}.png", 0)
    k, lab, st, cen = cv2.connectedComponentsWithStats((m > 128).astype(np.uint8))
    if k < 2:
        return 810.0, 420.0
    i = 1 + int(np.argmax(st[1:, 4]))
    x, y, w, h, _ = st[i]
    ys, xs = np.nonzero(lab[y:y + h // 3, x:x + w] == i)
    cx = x + (xs.mean() if len(xs) else w / 2)
    return float(cx), float(y + h * 0.30)


def shard_map(seed, P, h, w, reach):
    """Integer shard id per pixel (0 = unbroken glass) for impact point P.

    Straight radial cracks run out from the impact. Between each pair of
    neighbouring rays, straight chords at random radii cut the wedge into
    shards (concentric rings of a real shatter). Some chords are missing,
    so rings are broken and shards are uneven.
    """
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    dx, dy = xx - P[0], yy - P[1]
    r = np.hypot(dx, dy)
    th = np.arctan2(dy, dx)
    k = int(rng.integers(14, 20))
    gaps = rng.dirichlet(np.full(k, 2.5)) * 2 * np.pi
    angles = -np.pi + np.cumsum(gaps) - gaps[0] * rng.random()
    angles = np.sort(((angles + np.pi) % (2 * np.pi)) - np.pi)
    sec = np.searchsorted(angles, th) % k
    nr = 11
    base = np.cumsum(rng.uniform(26, 40, nr) * np.geomspace(1, 6.5, nr))
    radii = base[None, :] * rng.uniform(0.75, 1.25, (k, nr))
    ids = np.zeros((h, w), np.int32)
    for i in range(k):
        sel = sec == i
        a1, a2 = angles[i - 1], angles[i]
        px, py = dx[sel], dy[sel]
        ring = np.zeros(px.shape, np.int32)
        for j in range(nr):
            skip = j > 1 and rng.random() < 0.25
            if skip or max(radii[i - 1, j], radii[i, j]) > reach:
                continue
            p1 = radii[i - 1, j] * np.array([np.cos(a1), np.sin(a1)])
            p2 = radii[i, j] * np.array([np.cos(a2), np.sin(a2)])
            nx, ny = p2[1] - p1[1], -(p2[0] - p1[0])
            if nx * p1[0] + ny * p1[1] < 0:
                nx, ny = -nx, -ny
            ring += ((px - p1[0]) * nx + (py - p1[1]) * ny > 0).astype(np.int32)
        ids[sel] = i * 32 + ring + 1
    # a few long straight cracks crossing the whole sheet
    for _ in range(int(rng.integers(2, 5))):
        a = rng.uniform(0, np.pi)
        off = rng.uniform(150, 560) * rng.choice([-1, 1])
        cut = (dx * np.cos(a) + dy * np.sin(a)) > off
        if reach > 1e8:
            ids = ids * 2 + cut.astype(np.int32)
    _, ids = np.unique(ids, return_inverse=True)
    return ids.reshape(h, w), r, th


def render(n):
    si, first = section(n)
    rng = np.random.default_rng(4400 + n)
    img = load(n)
    h, w = img.shape[:2]
    P = impact(first)
    grow = n - first
    reach = [0.18, 0.45][grow] * w if grow < 2 else 1e9
    ids, r, th = shard_map(440 + si, P, h, w, reach)
    S = ids.max() + 1
    srng = np.random.default_rng(9000 + si)
    rot = np.radians(srng.uniform(-4.5, 4.5, S)).astype(np.float32)
    scl = srng.uniform(0.95, 1.06, S).astype(np.float32)
    tx = srng.normal(0, 24, S).astype(np.float32)
    ty = srng.normal(0, 24, S).astype(np.float32)
    lag = srng.choice([0, 0, 0, 1, 2, 3, 4], S)
    gain = srng.uniform(0.80, 1.10, S).astype(np.float32)
    cool = srng.uniform(0.0, 0.18, S).astype(np.float32)
    for p in (rot, scl, tx, ty, gain, cool):
        p[0] = p[0] * 0 + (1 if p is scl or p is gain else 0)
    lag[0] = 0
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    dx, dy = xx - P[0], yy - P[1]
    a, s = rot[ids], scl[ids]
    ca, sa = np.cos(a), np.sin(a)
    mx = P[0] + (ca * dx + sa * dy) / s - tx[ids]
    my = P[1] + (-sa * dx + ca * dy) / s - ty[ids]
    out = np.zeros_like(img)
    lag_px = lag[ids]
    for L in np.unique(lag_px):
        src = img if L == 0 else load(n - int(L))
        sel = lag_px == L
        warped = cv2.remap(src, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        out[sel] = warped[sel]
    # silver: per-shard brightness, cool desaturation
    g = out.mean(axis=2, keepdims=True)
    cs = cool[ids][..., None]
    out = out * (1 - cs) + (g * np.array([1.06, 1.0, 0.94], np.float32)) * cs
    out *= gain[ids][..., None]
    # a few fallen-out shards close to the impact show the dark mirror backing
    cen_r = np.bincount(ids.ravel(), r.ravel(), S) / np.maximum(np.bincount(ids.ravel(), None, S), 1)
    gone = (srng.random(S) < 0.10) & (cen_r < 0.30 * w) & (cen_r > 40)
    gone[0] = False
    gmask = gone[ids].astype(np.float32)
    if gmask.any():
        back = 0.07 + 0.03 * cv2.GaussianBlur(rng.random((h, w)).astype(np.float32), (0, 0), 1.5)
        out = out * (1 - gmask[..., None]) + back[..., None] * gmask[..., None]

    # crack seams: dark core + offset highlight
    edge = np.zeros((h, w), np.uint8)
    edge[:, 1:] |= (ids[:, 1:] != ids[:, :-1]).astype(np.uint8)
    edge[1:, :] |= (ids[1:, :] != ids[:-1, :]).astype(np.uint8)
    seam = cv2.GaussianBlur(cv2.dilate(edge, np.ones((4, 4), np.uint8)).astype(np.float32), (0, 0), 1.0)
    hi = cv2.GaussianBlur(np.roll(np.roll(edge, -2, 0), -2, 1).astype(np.float32), (0, 0), 0.8)
    glint_ang = 0.9 + 0.35 * np.sin(n * 0.21 + si)
    glint = np.clip(np.cos(th - glint_ang), 0, 1) ** 6
    out = out * (1 - 0.85 * seam[..., None])
    out += (hi * (0.35 + 0.65 * glint))[..., None] * np.array([1.0, 1.0, 1.0], np.float32)
    # chipped bevel: thin bright sliver along part of each seam
    bevel = cv2.GaussianBlur(cv2.dilate(edge, np.ones((5, 5), np.uint8)).astype(np.float32), (0, 0), 2.5) - seam * 0.6
    out += np.clip(bevel, 0, 1)[..., None] * 0.10 * glint[..., None]

    # impact: crushed white glass + fine spider cracks
    if grow >= 0:
        crush = np.exp(-(r / 38.0) ** 2)
        lines = np.abs(np.sin(th * 41 + np.sin(r / 9.0)))
        spider = (lines < 0.06) * np.exp(-r / 160.0)
        out = out * (1 - crush[..., None] * 0.85) + crush[..., None] * 0.92
        out = out * (1 - spider[..., None] * 0.5) + spider[..., None] * 0.55

    # mirror backing: faint dark tarnish at the edges, slight sheen
    vig = np.hypot((xx / w - 0.5) / 0.75, (yy / h - 0.5) / 0.75)
    out *= np.clip(1.08 - 0.45 * vig ** 2, 0.5, 1)[..., None]
    sheen = np.clip(1 - np.abs((xx + yy * 0.6) / w - 0.55 - 0.03 * np.sin(n * 0.3)) / 0.18, 0, 1) ** 2
    out += sheen[..., None] * 0.035
    gr = cv2.GaussianBlur(rng.normal(0, 1, (h, w)).astype(np.float32), (0, 0), 0.7)
    out += gr[..., None] * 0.008
    cv2.imwrite(f"{OUT}/frame_{n:03d}.png", (np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8))
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    nums = list(range(1, N + 1)) if (not ARGS or ARGS == ["all"]) else [int(a) for a in ARGS]
    with Pool(min(6, os.cpu_count() or 4)) as p:
        for n in p.imap_unordered(render, nums):
            pass
    print("done", len(nums))
