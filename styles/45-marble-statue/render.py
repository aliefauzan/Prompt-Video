"""Marble Statue restyle, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [frame numbers... | all]

Every person becomes carved, polished white marble while the room stays the
room (cooled and dimmed like a gallery). Form comes from the frame's own
luminance (smoothed, darks lifted, so hair and eyes read as carved stone) plus
a dome normal map from the matte lit by a soft skylight. Veins are a
procedural turbulence field held in texture coordinates that are advected
with optical flow, so the stone pattern rides on the body and does not boil.
Frames are simulated in order from frame 1 (the vein coordinates need it).
"""
import os
import sys

import cv2
import numpy as np

FRAMES, MASKS, OUT = sys.argv[1:4]
ARGS = sys.argv[4:]
N = len([f for f in os.listdir(FRAMES) if f.endswith(".png")])

# (first, last, name, stone BGR, vein BGR, vein strength, gold vein)
SECTIONS = [
    (1, 90, "carrara", (0.95, 0.96, 0.965), (0.50, 0.52, 0.53), 0.45, 0.0),
    (91, 999, "calacatta", (0.93, 0.955, 0.97), (0.36, 0.38, 0.40), 0.60, 0.30),
]
SKY = np.array([-0.25, -0.80, 0.55], np.float32)   # soft gallery skylight from above-left
SKY /= np.linalg.norm(SKY)
SCALE = 2                                          # vein/flow work at half resolution


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


def value_noise(seed, h, w, cell):
    rng = np.random.default_rng(seed)
    a = rng.random((h // cell + 3, w // cell + 3)).astype(np.float32)
    return a


def sample(grid, cell, u, v):
    """Bicubic sample of a coarse noise grid at continuous coords (u, v) in px."""
    return cv2.remap(grid, (u / cell + 1).astype(np.float32), (v / cell + 1).astype(np.float32),
                     cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)


H0, W0 = 1080 // SCALE, 1620 // SCALE
OCT = [(value_noise(450 + i, H0 * 3, W0 * 3, c), c) for i, c in enumerate([120, 60, 30, 15, 7])]


def veins(u, v, strength, gold):
    turb = 0
    amp = 1.0
    for grid, cell in OCT:
        turb = turb + amp * (sample(grid, cell, u + W0, v + H0) - 0.5)
        amp *= 0.45
    # two diagonal vein families, warped by turbulence
    a = np.sin((u * 0.85 + v * 0.5) / 70.0 + turb * 1.7)
    b = np.sin((u * -0.4 + v * 0.9) / 115.0 + turb * 1.3 + 1.3)
    va = np.exp(-np.abs(a) / 0.05) * 0.9 + np.exp(-np.abs(a) / 0.22) * 0.25
    vb = np.exp(-np.abs(b) / 0.025) * 0.55
    cloud = sample(OCT[1][0], OCT[1][1] * 2, u + 17, v + 9)
    vein = np.clip(va * strength + vb * strength * 0.7, 0, 1)
    goldv = np.exp(-np.abs(np.sin((u * 0.6 - v * 0.8) / 90.0 + turb * 4.0)) / 0.02) * gold
    return vein, cloud, goldv


def dome_normals(mb):
    h, w = mb.shape
    small = cv2.resize(mb, (w // 4, h // 4), interpolation=cv2.INTER_AREA)
    d = cv2.distanceTransform((small > 0).astype(np.uint8), cv2.DIST_L2, 5)
    hgt = (np.minimum(d, 60) / 60.0) ** 0.6
    hgt = cv2.GaussianBlur(hgt, (0, 0), 6)
    hgt = cv2.resize(hgt, (w, h), interpolation=cv2.INTER_CUBIC)
    gx = cv2.Sobel(hgt, cv2.CV_32F, 1, 0, ksize=5) / 32.0
    gy = cv2.Sobel(hgt, cv2.CV_32F, 0, 1, ksize=5) / 32.0
    n = np.dstack([-gx * 60, -gy * 60, np.ones_like(gx)])
    return n / np.linalg.norm(n, axis=2, keepdims=True)


def render_frame(n, img, m, u, v, rng):
    _, _, _, stone, vein_c, vstr, gold = section(n)
    h, w = m.shape
    mb = (m > 0.5).astype(np.uint8)
    # drop stray matte pieces (bits of the office chair) and fill pin holes
    k_, lab, st, _ = cv2.connectedComponentsWithStats(mb)
    keep = np.zeros(k_, np.uint8)
    keep[1:] = st[1:, 4] > 0.012 * h * w
    mb = keep[lab]
    mb = cv2.morphologyEx(mb, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
    core = cv2.erode(mb, np.ones((5, 5), np.uint8)).astype(np.float32)
    alpha = cv2.GaussianBlur(cv2.erode(mb, np.ones((3, 3), np.uint8)).astype(np.float32), (0, 0), 1.2)

    # carved form from luminance: edge-preserving smooth, local contrast, lifted darks
    lum = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # carve away printed cloth patterns: a vertical-line opening removes thin
    # bright horizontal stripes, a short closing evens the dark gaps between them
    hs = cv2.resize(lum, (w // 2, h // 2), interpolation=cv2.INTER_AREA)
    hs = cv2.morphologyEx(hs, cv2.MORPH_OPEN, np.ones((13, 1), np.uint8))
    hs = cv2.morphologyEx(hs, cv2.MORPH_CLOSE, np.ones((5, 1), np.uint8))
    hs = cv2.medianBlur((hs * 255).astype(np.uint8), 5).astype(np.float32) / 255
    clean = cv2.resize(hs, (w, h), interpolation=cv2.INTER_CUBIC)
    sm = hs.copy()
    sm = cv2.bilateralFilter(sm, 9, 0.08, 6)
    sm = cv2.bilateralFilter(sm, 9, 0.06, 6)
    sm = cv2.resize(sm, (w, h), interpolation=cv2.INTER_CUBIC)
    clahe = cv2.createCLAHE(2.0, (8, 8))
    eq = clahe.apply((sm * 255).astype(np.uint8)).astype(np.float32) / 255
    eq = eq * core + cv2.GaussianBlur(eq * core, (0, 0), 8) / (cv2.GaussianBlur(core, (0, 0), 8) + 1e-4) * (1 - core)
    loc = cv2.GaussianBlur(eq, (0, 0), 12)
    eq = loc + 0.55 * (eq - loc)
    form = 0.64 + 0.42 * eq ** 0.6
    # fine chisel detail (eyes, lips, folds): band-pass of the luminance
    detail = (cv2.GaussianBlur(clean, (0, 0), 1.5) - cv2.GaussianBlur(clean, (0, 0), 6))
    fine = cv2.GaussianBlur(lum, (0, 0), 1.0) - cv2.GaussianBlur(lum, (0, 0), 3.0)
    detail = 0.10 * np.tanh(detail * 6.0) + 0.05 * np.tanh(fine * 10.0)

    nrm = dome_normals(mb)
    lam = np.clip((nrm @ SKY + 0.5) / 1.5, 0, 1)
    shade = form * (0.50 + 0.62 * lam) + detail
    half = nrm @ (SKY + np.array([0, 0, 1], np.float32)) / np.linalg.norm(SKY + np.array([0, 0, 1], np.float32))
    spec = np.clip(half, 0, 1) ** 40 * 0.22 * np.clip(eq * 1.5, 0, 1)

    vein, cloud, goldv = veins(u, v, vstr, gold)
    vein = cv2.resize(vein, (w, h), interpolation=cv2.INTER_LINEAR)
    cloud = cv2.resize(cloud, (w, h), interpolation=cv2.INTER_LINEAR)
    goldv = cv2.resize(goldv, (w, h), interpolation=cv2.INTER_LINEAR)
    alb = np.array(stone, np.float32) * (0.94 + 0.10 * cloud[..., None])
    alb = alb * (1 - vein[..., None]) + np.array(vein_c, np.float32) * vein[..., None]
    alb = alb * (1 - goldv[..., None] * 0.6) + np.array([0.35, 0.62, 0.78], np.float32) * goldv[..., None] * 0.6
    marble = alb * shade[..., None]
    # translucency: a little light scattered under the surface
    marble = marble * 0.82 + cv2.GaussianBlur(marble, (0, 0), 5) * 0.18
    marble += spec[..., None]
    # crevices: darken where the matte bends inward (ambient occlusion)
    ao = cv2.GaussianBlur(mb.astype(np.float32), (0, 0), 14)
    marble *= (0.72 + 0.28 * np.clip(ao * 1.5, 0, 1) ** 1.5)[..., None]

    # gallery: room desaturated, cooled and dimmed, soft overhead skylight
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)[..., None]
    room = (g + (img - g) * 0.30) * 0.50 * np.array([1.05, 1.0, 0.94], np.float32)
    yy = np.linspace(0, 1, h, dtype=np.float32)[:, None, None]
    room *= 1.05 - 0.35 * yy
    # soft contact shadow of the statues on the room
    sh = cv2.GaussianBlur(mb.astype(np.float32), (0, 0), 22)
    room *= (1 - 0.28 * sh)[..., None]

    out = room * (1 - alpha[..., None]) + marble * alpha[..., None]
    gr = cv2.GaussianBlur(rng.normal(0, 1, (h, w)).astype(np.float32), (0, 0), 0.6)
    out += gr[..., None] * 0.006
    return np.clip(out, 0, 1)


def main():
    os.makedirs(OUT, exist_ok=True)
    nums = list(range(1, N + 1)) if (not ARGS or ARGS == ["all"]) else sorted(int(a) for a in ARGS)
    want = set(nums)
    gy, gx = np.mgrid[0:H0, 0:W0].astype(np.float32)
    u, v = gx.copy(), gy.copy()
    prev = None
    for n in range(1, max(nums) + 1):
        img = cv2.imread(f"{FRAMES}/frame_{n:03d}.png").astype(np.float32) / 255
        m = load_mask(n)
        gray = cv2.cvtColor(cv2.resize(img, (W0, H0), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY)
        g8 = (gray * 255).astype(np.uint8)
        ms = cv2.resize(m, (W0, H0), interpolation=cv2.INTER_AREA)
        if prev is not None:
            # backward flow (current -> previous): pull texture coords along the motion
            flow = cv2.calcOpticalFlowFarneback(g8, prev, None, 0.5, 4, 25, 4, 7, 1.5, 0)
            # near-rigid: average the motion over large patches inside the bodies
            wgt = cv2.GaussianBlur(ms, (0, 0), 18) + 1e-3
            flow = cv2.GaussianBlur(flow * ms[..., None], (0, 0), 18) / wgt[..., None]
            mx = (gx + flow[..., 0]).astype(np.float32)
            my = (gy + flow[..., 1]).astype(np.float32)
            u = cv2.remap(u, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
            v = cv2.remap(v, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        # outside the people the coords relax back to the grid
        k = np.clip(ms * 1.5, 0, 1) * 0.985
        u = u * k + gx * (1 - k)
        v = v * k + gy * (1 - k)
        prev = g8
        if n in want:
            out = render_frame(n, img, m, u, v, np.random.default_rng(4500 + n))
            cv2.imwrite(f"{OUT}/frame_{n:03d}.png", (out * 255 + 0.5).astype(np.uint8))
    print("done", len(nums))


if __name__ == "__main__":
    main()
