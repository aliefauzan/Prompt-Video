"""Dark Stage Spotlight restyle, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [frame numbers... | all]

Person mattes cut the people out of the room. The room drops to a near-black
void with a faint haze beam. Each person is relit by one big key light from
45 degrees front-left. Their shape comes from a dome height map built from the
matte. Bodies fall off into darkness towards the floor, and a thin rim light
traces the back edge. Only grain and haze move between frames.
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np

FRAMES, MASKS, OUT = sys.argv[1:4]
ARGS = sys.argv[4:]
N = len([f for f in os.listdir(FRAMES) if f.endswith(".png")])

# (first, last, name, key colour BGR, rim colour BGR, shadow tint BGR, saturation)
SECTIONS = [
    (1, 60, "classic softbox", (0.98, 1.00, 1.04), (1.00, 0.96, 0.92), (0.020, 0.012, 0.008), 0.92),
    (61, 120, "colour gel", (1.00, 0.99, 1.02), (0.25, 0.62, 1.10), (0.060, 0.016, 0.004), 0.95),
    (121, 999, "rembrandt gold", (0.80, 0.95, 1.10), (0.95, 0.92, 0.88), (0.022, 0.010, 0.004), 0.85),
]
LIGHT = np.array([-0.62, -0.58, 0.53], np.float32)   # x right, y down, z to camera
LIGHT /= np.linalg.norm(LIGHT)


def load_mask(n):
    """Soft matte 0..1. A few frames have a broken matte (fast hand motion blur
    loses most of a person); if a matte is much smaller than both neighbours,
    borrow the region the two neighbours agree on."""
    def rd(k):
        return cv2.imread(f"{MASKS}/frame_{min(max(k, 1), N):03d}.png", 0).astype(np.float32) / 255
    m = rd(n)
    nb = [rd(n - 1), rd(n + 1)]
    if m.mean() < 0.85 * min(x.mean() for x in nb):
        m = np.maximum(m, np.minimum(*nb))
    return m


def section(n):
    for s in SECTIONS:
        if s[0] <= n <= s[1]:
            return s
    return SECTIONS[-1]


def vnoise(rng, h, w, cell):
    a = rng.random((max(2, h // cell + 2), max(2, w // cell + 2))).astype(np.float32)
    return cv2.resize(a, (w, h), interpolation=cv2.INTER_CUBIC).clip(0, 1)


def dome_normals(mb):
    """Pseudo surface normals from the matte: inflate the silhouette like a pillow."""
    h, w = mb.shape
    small = cv2.resize(mb, (w // 4, h // 4), interpolation=cv2.INTER_AREA)
    d = cv2.distanceTransform((small > 0).astype(np.uint8), cv2.DIST_L2, 5)
    hgt = (np.minimum(d, 70) / 70.0) ** 0.7
    hgt = cv2.GaussianBlur(hgt, (0, 0), 9)
    hgt = cv2.resize(hgt, (w, h), interpolation=cv2.INTER_CUBIC)
    gx = cv2.Sobel(hgt, cv2.CV_32F, 1, 0, ksize=5) / 32.0
    gy = cv2.Sobel(hgt, cv2.CV_32F, 0, 1, ksize=5) / 32.0
    k = 70.0
    n = np.dstack([-gx * k, -gy * k, np.ones_like(gx)])
    n /= np.linalg.norm(n, axis=2, keepdims=True)
    return n


def floor_falloff(mb):
    """Per column: bright near the top of each figure, fading towards the floor."""
    h, w = mb.shape
    has = mb.any(axis=0)
    top = np.where(has, mb.argmax(axis=0), h).astype(np.float32)
    top = cv2.GaussianBlur(top[None, :], (0, 0), 25)[0]
    yy = np.arange(h, dtype=np.float32)[:, None]
    rel = (yy - top[None, :]) / (h * 0.95)
    return np.clip(1.12 - 1.05 * rel, 0.16, 1.0)


def render(n):
    rng = np.random.default_rng(4300 + n)
    s = section(n)
    _, _, _, key, rim_c, shadow_t, sat = s
    img = cv2.imread(f"{FRAMES}/frame_{n:03d}.png").astype(np.float32) / 255
    m = load_mask(n)
    h, w = m.shape
    mb = (m > 0.5).astype(np.uint8)
    # tighten the matte and pull edge colours from inside the body, so the
    # bright wall never bleeds through as a white halo
    core = cv2.erode(mb, np.ones((7, 7), np.uint8)).astype(np.float32)
    m = cv2.GaussianBlur(cv2.erode(mb, np.ones((3, 3), np.uint8)).astype(np.float32), (0, 0), 1.4)
    wsum = cv2.GaussianBlur(core, (0, 0), 6) + 1e-4
    inner = cv2.GaussianBlur(img * core[..., None], (0, 0), 6) / wsum[..., None]
    img = img * core[..., None] + inner * (1 - core[..., None])

    nrm = dome_normals(mb)
    wrap = 0.45
    lam = np.clip((nrm @ LIGHT + wrap) / (1 + wrap), 0, 1)
    # broad key-light position: softbox up and left of frame
    xx = np.arange(w, dtype=np.float32)[None, :] / w
    side = np.clip(1.08 - 0.32 * xx, 0.6, 1.0)
    fall = floor_falloff(mb) * side
    light = 0.03 + 1.45 * (lam ** 2.2) * fall

    # rim light from behind-right on the edge band
    er = cv2.erode(mb, np.ones((7, 7), np.uint8))
    band = cv2.GaussianBlur((mb - er).astype(np.float32), (0, 0), 1.8)
    # back edge only: where the matte drops off to the right
    mr = cv2.GaussianBlur(mb.astype(np.float32), (0, 0), 6)
    facing = np.clip(-cv2.Sobel(mr, cv2.CV_32F, 1, 0, ksize=5) / 6.0, 0, 1)
    facing = cv2.GaussianBlur(facing, (0, 0), 4)
    rim = np.clip(band * facing * 3.0, 0, 1) * floor_falloff(mb) * 0.55

    # subject: original texture, exposure lifted then relit
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)[..., None]
    subj = gray + (img - gray) * sat
    subj = np.clip(subj * 1.15, 0, 1) ** 1.05
    lit = subj * light[..., None] * np.array(key, np.float32)
    lit += rim[..., None] * np.array(rim_c, np.float32)
    # shadow tint (gel or cool) sits in the darkest parts
    dark = np.clip(1 - light / 0.45, 0, 1)[..., None]
    lit += dark * np.array(shadow_t, np.float32) * 1.6
    # gentle filmic shoulder
    lit = 1 - np.exp(-lit * 1.25)
    lit = lit / (1 - np.exp(-1.25))

    # background: near-black void, ghost of the room at ~2 %, haze beam
    bg = cv2.GaussianBlur(img, (0, 0), 6) * 0.018
    yy, xg = np.mgrid[0:h, 0:w].astype(np.float32)
    ox, oy = -0.15 * w, -0.25 * h                     # beam origin, off frame top-left
    ang = np.arctan2(yy - oy, xg - ox)
    beam = np.exp(-((ang - 0.62) / 0.16) ** 2)
    dist = np.hypot(xg - ox, yy - oy) / w
    smoke = vnoise(np.random.default_rng(43 + n // 6), h // 4, w // 4, 22)
    smoke2 = vnoise(np.random.default_rng(4343 + n // 6), h // 4, w // 4, 22)
    t = (n % 6) / 6
    smoke = cv2.resize(smoke * (1 - t) + smoke2 * t, (w, h))
    haze = beam * np.exp(-dist * 1.4) * (0.5 + 0.7 * smoke) * 0.09
    bg += haze[..., None] * np.array(key, np.float32) * np.array([0.95, 0.97, 1.0], np.float32)
    bg += 0.006

    out = bg * (1 - m[..., None]) + lit * m[..., None]
    # vignette + fine grain (new every frame)
    vig = 1 - 0.45 * (((xg / w - 0.42) ** 2) / 0.36 + ((yy / h - 0.40) ** 2) / 0.5)
    out *= np.clip(vig, 0.35, 1)[..., None]
    g = cv2.GaussianBlur(rng.normal(0, 1, (h, w)).astype(np.float32), (0, 0), 0.7)
    out += g[..., None] * (0.010 + 0.018 * out)
    cv2.imwrite(f"{OUT}/frame_{n:03d}.png", (np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8))
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    nums = list(range(1, N + 1)) if (not ARGS or ARGS == ["all"]) else [int(a) for a in ARGS]
    with Pool(min(8, os.cpu_count() or 4)) as p:
        for n in p.imap_unordered(render, nums):
            pass
    print("done", len(nums))
