"""Stained-glass window restyle, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [frame numbers...]
Frames are frame_001.png ... ; masks are person mattes with the same names.
The frame is cut into glass pieces (small on people and faces, large in the room),
each piece filled with one jewel-toned glass, joined by lead came, lit from behind.
Seed points jitter every frame so the pieces are re-cut and the window boils.
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np

FRAMES, MASKS, OUT = sys.argv[1:4]
ONLY = [int(a) for a in sys.argv[4:]]
N = len([f for f in os.listdir(FRAMES) if f.endswith(".png")])

LEAD = np.array([0.07, 0.075, 0.08], np.float32)
# background glass: cobalt, azure, teal, deep blue; ruby/amber/emerald as accents (BGR)
BG_GLASS = np.array([[0.62, 0.22, 0.05], [0.80, 0.45, 0.12], [0.55, 0.42, 0.06], [0.45, 0.12, 0.10],
                     [0.70, 0.30, 0.10], [0.62, 0.22, 0.05]], np.float32)
ACCENT = np.array([[0.10, 0.08, 0.70], [0.08, 0.55, 0.90], [0.20, 0.55, 0.10], [0.45, 0.10, 0.45]], np.float32)


def vnoise(rng, h, w, cell):
    a = rng.random((max(2, h // cell + 2), max(2, w // cell + 2))).astype(np.float32)
    return cv2.resize(a, (w, h), interpolation=cv2.INTER_CUBIC).clip(0, 1)


def seeds(m, h, w, rng):
    """Section-stable seed points, denser on people and densest on heads."""
    ys, xs = np.nonzero(m > 0.5)
    head = np.zeros((h, w), np.float32)
    if len(ys):
        top = ys.min()
        head[top:top + int(h * 0.35)] = 1
    dens = 0.12 + m * (0.20 + 0.04 * head)
    cand = rng.random((70000, 2)) * [w, h]
    keep = rng.random(70000) < dens[cand[:, 1].astype(int), cand[:, 0].astype(int)] ** 1.2 * 0.05
    return cand[keep]


def voronoi(pts, h, w):
    """Per-pixel index of the nearest seed (indices follow pts order, so they survive jitter)."""
    img = np.ones((h, w), np.uint8)
    xs = np.clip(pts[:, 0].astype(int), 0, w - 1)
    ys = np.clip(pts[:, 1].astype(int), 0, h - 1)
    img[ys, xs] = 0
    _, lab = cv2.distanceTransformWithLabels(img, cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
    # OpenCV numbers labels 1..K in raster order of the seed pixels; map back to seed index
    _, first = np.unique(ys * w + xs, return_index=True)
    lut = np.concatenate([[0], first]).astype(np.int32)
    return lut[lab]


def jewel(col_bgr, lift=0.12, vs=0.85):
    hsv = cv2.cvtColor(col_bgr[None].astype(np.float32), cv2.COLOR_BGR2HSV)[0]
    hsv[:, 1] = np.clip(hsv[:, 1] * 1.9 + 0.18, 0, 0.95)
    hsv[:, 2] = np.clip(hsv[:, 2] * vs + lift, 0, 1)
    if lift > 0.15:                                               # figures: flesh in pale rose-white glass
        skin = ((hsv[:, 0] < 45) | (hsv[:, 0] > 345)) & (hsv[:, 2] > 0.55)
        hsv[skin, 1] *= 0.42
        hsv[skin, 2] = np.clip(hsv[skin, 2] * 1.05, 0, 1)
    return cv2.cvtColor(hsv[None], cv2.COLOR_HSV2BGR)[0]


def render(n):
    rng = np.random.default_rng(2100 + n)
    bgr = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png"))
    h, w = bgr.shape[:2]
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
    mb = (cv2.GaussianBlur(m, (0, 0), 2) > 0.5).astype(np.uint8)
    srng = np.random.default_rng(777 + n // 12)                  # window design changes once a second
    pts = seeds(cv2.GaussianBlur(m, (0, 0), 25), h, w, srng)
    pts = pts + rng.normal(0, 3.0, pts.shape)                     # ...and is re-cut a little every frame

    # structure: Voronoi cells, split by the person outline and by flat colour zones
    vor = voronoi(pts, h, w)
    sm = cv2.bilateralFilter(cv2.resize(bgr, (w // 3, h // 3)), 9, 60, 9)
    lab = cv2.cvtColor(sm, cv2.COLOR_BGR2LAB).reshape(-1, 3).astype(np.float32)
    _, q, cent = cv2.kmeans(lab, 6, None, (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0),
                            2, cv2.KMEANS_PP_CENTERS)
    q = cv2.medianBlur(q.reshape(h // 3, w // 3).astype(np.uint8), 11)
    q = cv2.resize(q, (w, h), interpolation=cv2.INTER_NEAREST)
    key = vor.astype(np.int64) * 32 + q.astype(np.int64) * 2 + mb
    bd = np.zeros((h, w), np.uint8)
    bd[:, 1:] |= (key[:, 1:] != key[:, :-1]).astype(np.uint8)
    bd[1:, :] |= (key[1:, :] != key[:-1, :]).astype(np.uint8)
    contour = cv2.morphologyEx(mb, cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8))
    # wobble the came so it is hand-bent, not vector-perfect
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    dx = (vnoise(rng, h, w, 35) - 0.5) * 5
    dy = (vnoise(rng, h, w, 35) - 0.5) * 5
    lead = cv2.dilate(bd, np.ones((5, 5), np.uint8)) * (1 - mb) | cv2.dilate(bd, np.ones((3, 3), np.uint8)) | cv2.dilate(contour, np.ones((9, 9), np.uint8))
    lead = cv2.remap(lead.astype(np.float32), xx + dx, yy + dy, cv2.INTER_LINEAR)
    lead = (cv2.GaussianBlur(lead, (0, 0), 0.8) > 0.45).astype(np.uint8)
    npc, pieces = cv2.connectedComponents(1 - lead, connectivity=4)

    # one glass colour per piece
    flat = pieces.ravel()
    cnt = np.bincount(flat, minlength=npc).astype(np.float32) + 1e-6
    mean = np.stack([np.bincount(flat, bgr[..., c].ravel().astype(np.float32), npc) / cnt for c in range(3)], 1) / 255
    pm = np.bincount(flat, mb.ravel().astype(np.float32), npc) / cnt
    glass = jewel(mean)
    # per-piece randomness keyed to its Voronoi seed, so a sheet keeps its glass while the cut boils
    sid = np.round(np.bincount(flat, vor.ravel().astype(np.float64), npc) / cnt)
    pr = np.sin(sid[:, None] * np.array([12.9898, 78.233, 37.719, 4.581])) * 43758.5453
    pr = (pr - np.floor(pr)).astype(np.float32)
    sat = cv2.cvtColor(mean[None].astype(np.float32), cv2.COLOR_BGR2HSV)[0][:, 1]
    bgp = pm < 0.5
    # background: re-glaze greys/whites as cobalt-family glass with jewel accents
    pick = BG_GLASS[(pr[:, 0] * len(BG_GLASS)).astype(int)]
    acc = ACCENT[(pr[:, 1] * len(ACCENT)).astype(int)]
    pick = np.where((pr[:, 2] < 0.16)[:, None], acc, pick)
    lum = mean.mean(1, keepdims=True)
    pick = pick * (0.75 + 0.6 * lum)
    neutral = (sat < 0.35)[:, None]
    glass = np.where((bgp[:, None] & neutral), pick, np.where(bgp[:, None], glass * 0.6 + pick * 0.4, jewel(mean, 0.16, 1.15)))
    glass *= (0.88 + 0.24 * pr[:, 3])[:, None]                    # every sheet of glass is a bit different
    img = glass[pieces]

    # inside a piece: glass is brighter in the middle, darker by the came; streaks + seeds
    dist = cv2.distanceTransform(1 - lead, cv2.DIST_L2, 3)
    core = np.clip(dist / 14, 0, 1)
    img *= (0.72 + 0.4 * core)[..., None]
    streak = np.zeros((h, w), np.float32)
    for ang in (0.4, 1.3, 2.4):
        c, s = np.cos(ang), np.sin(ang)
        u = (xx * c + yy * s) * 0.03 + vnoise(rng, h, w, 60) * 6
        streak += (np.sin(u * 6.28) * 0.5 + 0.5) * ((pieces % 3) == int(ang) % 3)
    img *= (0.9 + 0.16 * streak)[..., None]
    bub = (rng.random((h, w)) > 0.9993).astype(np.float32)
    img += cv2.GaussianBlur(bub, (0, 0), 1.2)[..., None] * 2.5

    # grisaille: painted features on the glass so faces stay recognisable
    g = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
    g = cv2.createCLAHE(2.0, (8, 8)).apply((g * 255).astype(np.uint8)).astype(np.float32) / 255
    shade = cv2.GaussianBlur(g, (0, 0), 3)
    detail = cv2.GaussianBlur(g, (0, 0), 2.4) - cv2.GaussianBlur(g, (0, 0), 1.2)
    paint = np.clip(detail * 34 - 0.15, 0, 1) * m
    ms = cv2.GaussianBlur(m, (0, 0), 3)
    img *= (1 - ms * 0.4 * (1 - shade) ** 1.6)[..., None]        # matting: half-tone shading on figures
    img = img * (1 - paint[..., None] * 0.85) + np.array([0.05, 0.07, 0.10]) * paint[..., None] * 0.85

    # backlight glow
    bright = np.clip(img - 0.55, 0, 1)
    img += cv2.GaussianBlur(bright, (0, 0), 14) * 0.55 + cv2.GaussianBlur(bright, (0, 0), 40) * 0.35
    sun = vnoise(srng, h, w, 400)                                  # sun drifts slowly behind the window
    img *= (0.94 + 0.12 * sun + 0.03 * (vnoise(rng, h, w, 400) - 0.5))[..., None]

    # lead came on top, with a thin highlight along one bevel
    leadf = lead.astype(np.float32)
    hl = np.clip(leadf - np.roll(leadf, (2, 2), (0, 1)), 0, 1) * 0.25
    img = img * (1 - leadf[..., None]) + LEAD * leadf[..., None] + hl[..., None] * 0.6
    r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    img *= (1 - 0.3 * np.clip(r - 0.6, 0, 1))[..., None]
    img += cv2.GaussianBlur(rng.normal(0, 1, (h, w)).astype(np.float32), (0, 0), 0.8)[..., None] * 0.01
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), (img.clip(0, 1) * 255).astype(np.uint8))
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    todo = ONLY or list(range(1, N + 1))
    with Pool(min(6, os.cpu_count() or 2)) as p:
        for n in p.imap_unordered(render, todo):
            print(n, end=" ", flush=True)
    print()
