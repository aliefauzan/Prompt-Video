"""Loose watercolour + ink-line restyle, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [frame numbers...]
Frames are frame_001.png ... ; masks are person mattes with the same names.
Washes are re-flooded every frame (new bleeds, blooms, granulation) and the ink
line is re-drawn with a new wobble, so the painting breathes.
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np

FRAMES, MASKS, OUT = sys.argv[1:4]
ONLY = [int(a) for a in sys.argv[4:]]
N = len([f for f in os.listdir(FRAMES) if f.endswith(".png")])

PAPER = np.array([0.93, 0.96, 0.975], np.float32)        # BGR, cold-press white
INK = np.array([0.16, 0.14, 0.15], np.float32)           # sepia-black fineliner


def vnoise(rng, h, w, cell):
    a = rng.random((max(2, h // cell + 2), max(2, w // cell + 2))).astype(np.float32)
    return cv2.resize(a, (w, h), interpolation=cv2.INTER_CUBIC).clip(0, 1)


def fbm(rng, h, w, cell, octaves=4):
    out, amp, tot = 0, 1.0, 0
    for i in range(octaves):
        out = out + vnoise(rng, h, w, max(2, cell >> i)) * amp
        tot += amp
        amp *= 0.5
    return out / tot


def warp(img, rng, amp, cell):
    h, w = img.shape[:2]
    dx = (vnoise(rng, h, w, cell) - 0.5) * 2 * amp
    dy = (vnoise(rng, h, w, cell) - 0.5) * 2 * amp
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    return cv2.remap(img, xx + dx, yy + dy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


def paper(rng, h, w):
    tooth = cv2.GaussianBlur(rng.random((h, w)).astype(np.float32), (0, 0), 1.2)
    big = fbm(rng, h, w, 48, 3)
    t = 0.985 + (tooth - 0.5) * 0.05 + (big - 0.5) * 0.025
    return PAPER[None, None, :] * t[..., None], tooth


def wash_colour(bgr, rng):
    """Soft local colour, cleaned up and pushed toward a painter's pigment set."""
    h, w = bgr.shape[:2]
    sm = cv2.resize(bgr, (w // 6, h // 6), interpolation=cv2.INTER_AREA)
    sm = cv2.bilateralFilter(sm, 7, 40, 5)
    sm = cv2.resize(sm, (w, h), interpolation=cv2.INTER_CUBIC)
    hsv = cv2.cvtColor(sm, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[..., 1] = np.clip(hsv[..., 1] * 2.1 + 35, 0, 240)
    hsv[..., 2] = np.clip(hsv[..., 2] * 0.85 + 45, 0, 255)
    col = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32) / 255
    # painterly colour drift: ultramarine, rose, raw sienna, sap green, floating in
    pig = np.array([[0.75, 0.38, 0.22], [0.55, 0.42, 0.88], [0.25, 0.55, 0.85], [0.35, 0.62, 0.42]], np.float32)
    wts = np.stack([fbm(rng, h, w, 260, 2) for _ in pig], -1) ** 3
    wts /= wts.sum(-1, keepdims=True) + 1e-6
    drift = wts @ pig
    return col * 0.62 + drift * 0.38


def render(n):
    rng = np.random.default_rng(1900 + n)
    bgr = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png"))
    h, w = bgr.shape[:2]
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
    ms = cv2.GaussianBlur(m, (0, 0), 4)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255

    img, tooth = paper(rng, h, w)
    col = wash_colour(bgr, rng)

    # pigment density: darker photo -> more pigment; subjects fuller, room barely tinted
    lum = cv2.GaussianBlur(gray, (0, 0), 3)
    dens = np.clip((0.95 - lum) * 1.35, 0, 1) ** 0.85             # highlights stay white paper
    # where the wash reaches: ragged, wet-edged coverage that leaves white paper
    reach_fg = ms
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    r = np.sqrt(((xx - w / 2) / (w * 0.55)) ** 2 + ((yy - h * 0.55) / (h * 0.6)) ** 2)
    reach_bg = np.clip(1.05 - r, 0, 1) * 0.55
    reach = np.maximum(reach_fg * 0.95, reach_bg)
    reach *= np.clip((h * 1.02 - yy) / (h * 0.3), 0, 1)               # figures dissolve toward the bottom
    reach = warp(reach, rng, 28, 90) + (fbm(rng, h, w, 120) - 0.5) * 0.55
    cover = np.clip((reach - 0.36) * 7, 0, 1)                     # sharp-ish wet boundary
    # misregister the wash against the line: the painter is loose
    shift = rng.normal(0, 7, 2)
    M = np.float32([[1, 0, shift[0]], [0, 1, shift[1]]])
    col_s = cv2.warpAffine(warp(col, rng, 9, 70), M, (w, h), borderMode=cv2.BORDER_REFLECT)
    dens_s = cv2.warpAffine(dens, M, (w, h), borderMode=cv2.BORDER_REFLECT)

    # two glazes: a broad light flat, then a smaller, darker shadow glaze
    a1 = cover * (0.45 + 0.25 * fbm(rng, h, w, 60))
    sh_reach = warp(np.clip((dens_s - 0.55) * 2.2, 0, 1), rng, 14, 60) + (fbm(rng, h, w, 70) - 0.5) * 0.5
    a2 = np.clip((sh_reach - 0.25) * 4, 0, 1) * cover * (ms * 0.8 + 0.2)
    gran = (cv2.GaussianBlur(rng.random((h, w)).astype(np.float32), (0, 0), 1.6) - 0.5) * 2
    for a, strength in ((a1, 0.5), (a2, 0.45)):
        # edge darkening: pigment pools at the drying edge of each wash
        edge = np.clip(a - cv2.GaussianBlur(a, (0, 0), 6), 0, 1) * 2.2
        d = a * strength * dens_s * (1 + 0.35 * gran + 0.25 * (tooth - 0.5)) + edge * 0.35 * dens_s
        trans = 1 - np.clip(d, 0, 1)[..., None] * (1 - col_s)      # subtractive glaze
        img = img * trans

    # cauliflower blooms: back-runs where wet paint met wet paint
    for _ in range(int(rng.integers(3, 6))):
        cx, cy = rng.integers(0, w), rng.integers(h // 2, h)        # lower half: clothes and floor
        R = rng.uniform(40, 120)
        blob = np.exp(-(((xx - cx) ** 2 + (yy - cy) ** 2) / (2 * R * R)))
        blob = warp(blob, rng, R * 0.35, 25)
        ring = np.clip(blob - 0.35, 0, 0.12) / 0.12 - np.clip(blob - 0.5, 0, 0.5) * 2
        img = img + (PAPER - img) * (np.clip(blob - 0.5, 0, 1) * cover * 0.55)[..., None]
        img = img * (1 - (np.clip(ring, 0, 1) * cover * 0.12)[..., None])

    # splatter flicks from the loaded brush
    spl = np.zeros((h, w), np.float32)
    for _ in range(int(rng.integers(20, 45))):
        x, y = int(rng.normal(w * 0.5, w * 0.3)), int(rng.normal(h * 0.55, h * 0.3))
        cv2.circle(spl, (x, y), int(rng.choice([1, 2, 2, 3, 5, 8])), 1.0, -1, cv2.LINE_AA)
    spl_col = col_s[np.clip(int(h * 0.6), 0, h - 1), np.clip(int(w * rng.uniform(0.2, 0.8)), 0, w - 1)]
    img = img * (1 - (spl * 0.55)[..., None] * (1 - spl_col))

    # ink line: fine, confident contour + selected inner detail, mostly on people
    g = cv2.createCLAHE(2.0, (8, 8)).apply(cv2.bilateralFilter((gray * 255).astype(np.uint8), 9, 50, 7)).astype(np.float32) / 255
    d = cv2.GaussianBlur(g, (0, 0), 2.2) - cv2.GaussianBlur(g, (0, 0), 1.2)
    df = cv2.GaussianBlur(g, (0, 0), 1.5) - cv2.GaussianBlur(g, (0, 0), 0.9)
    lines = np.clip(np.maximum(d * 32 - 0.17, df * 45 - 0.17), 0, 1) ** 0.8
    contour = cv2.morphologyEx((m > 0.5).astype(np.uint8), cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8)).astype(np.float32)
    lines = np.maximum(lines * (0.25 + 0.75 * ms), contour * 0.95)
    lines *= (fbm(rng, h, w, 80) > 0.33) * 0.6 + 0.4                # line lifts off in places
    lines = warp(lines, rng, 2.6, 55)
    lines = cv2.GaussianBlur(lines, (0, 0), 0.6)
    lines_bg = np.clip(d * 30 - 0.4, 0, 1) * (1 - ms) * (r < 0.95) * (fbm(rng, h, w, 140) > 0.42)
    lines_bg = warp(lines_bg, rng, 3.5, 70) * 0.45
    la = np.clip(lines + lines_bg, 0, 1) * (0.85 + 0.15 * tooth)
    img = img * (1 - la[..., None]) + INK * la[..., None]

    img += (cv2.GaussianBlur(rng.normal(0, 1, (h, w)).astype(np.float32), (0, 0), 0.8) * 0.01)[..., None]
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), (img.clip(0, 1) * 255).astype(np.uint8))
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    todo = ONLY or list(range(1, N + 1))
    with Pool(min(6, os.cpu_count() or 2)) as p:
        for n in p.imap_unordered(render, todo):
            print(n, end=" ", flush=True)
    print()
