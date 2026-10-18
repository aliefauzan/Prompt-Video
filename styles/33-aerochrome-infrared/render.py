"""Aerochrome Infrared: Kodak Aerochrome III 1443 false-colour IR slide film, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [frame numbers... | all]

Aerochrome's three layers are sensitive to green, red and near-infrared, and
print as blue, green and red (a yellow filter blocks blue). So we estimate a
near-IR channel from the visible frame (foliage and skin reflect IR strongly,
plants most of all), then map  IR -> red, red -> green, green -> blue.
Green leaves go hot pink/crimson, blue sky and cool walls go teal/cyan, skin
goes pale peach, and greyish-green fabric goes dusty rose. On top: a slide-film
contrast curve, cyan-teal shadows, halation on highlights, a soft vignette and
fresh grain + a slight exposure/colour breath every frame.
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


def grain(rng, h, w):
    g = rng.normal(0, 1, (h // 2, w // 2)).astype(np.float32)
    g = cv2.resize(g, (w, h), interpolation=cv2.INTER_LINEAR)
    g += rng.normal(0, 0.6, (h, w)).astype(np.float32)
    return g


def render(n):
    rng = np.random.default_rng(3300 + n)
    bgr = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png")).astype(np.float32) / 255
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), 0).astype(np.float32) / 255
    h, w = m.shape
    lin = bgr ** 2.2
    B, G, R = lin[..., 0], lin[..., 1], lin[..., 2]
    L = 0.2126 * R + 0.7152 * G + 0.0722 * B

    # --- near-IR estimate -------------------------------------------------
    # chlorophyll: green clearly above red and blue -> very bright in IR
    d = (G - np.maximum(R, B)) / (L + 0.02)
    # on the people, average over a wide window so a dyed fabric shifts as one colour
    mw = cv2.GaussianBlur(m, (0, 0), 25) + 1e-4
    d_cloth = cv2.GaussianBlur(d * m, (0, 0), 25) / mw
    d = d * (1 - m) + d_cloth * m
    veg = cv2.GaussianBlur(np.clip(d * 4.0, 0, 2.0), (0, 0), 4)
    # warm organics (skin, wood, brown cloth, red leaves) reflect IR at least as
    # well as red light, so their IR sits at or above their red value
    warm = np.clip((R - B) / (R + B + 0.03), 0, 1)
    ir = L + 3.2 * warm * np.clip(R - L, 0, None) + veg * (0.30 + 0.9 * np.sqrt(L + 1e-4))
    ms = cv2.GaussianBlur(m, (0, 0), 3)
    ir = ir * (1 + 0.15 * ms)                       # cotton clothes glow in IR
    ir = cv2.GaussianBlur(ir, (0, 0), 1.2)          # IR focus is a touch soft

    # --- layer swap: IR->R, R->G, G->B (yellow filter kills blue) -----------
    # a neutral grey (R=G=B=IR) stays neutral; only the hues rotate
    out = np.stack([G, R, ir], -1)
    # blue light (window, cool walls, screen) has no layer of its own: it lands as teal/cyan
    cool = np.clip((B - 0.5 * (R + G)) / (L + 0.03), 0, 1)
    out[..., 0] += cool * L * 0.9
    out[..., 1] += cool * L * 0.45
    out[..., 2] *= 1 - 0.35 * cool
    # foliage lands hot pink-magenta (Richard Mosse pink): its red layer is near-empty
    vg = np.clip(veg, 0, 1)
    out[..., 1] *= 1 - 0.55 * vg
    out[..., 0] = out[..., 0] * (1 - 0.3 * vg) + out[..., 2] * 0.45 * vg
    out = np.clip(out, 0, None) ** (1 / 2.2)

    # skin glows in IR: pale, smooth, luminous (veins and blemishes vanish)
    skin = ms * np.clip((warm - 0.25) * 3, 0, 1) * np.clip((bgr.mean(-1) - 0.25) * 4, 0, 1)
    skin = cv2.GaussianBlur(skin, (0, 0), 4)[..., None]
    soft = cv2.GaussianBlur(out, (0, 0), 3)
    out = out * (1 - 0.45 * skin) + soft * 0.45 * skin
    out = out + skin * (np.array([0.86, 0.88, 1.0], np.float32) - out) * 0.30

    # --- slide-film grade --------------------------------------------------
    hsv = cv2.cvtColor(np.clip(out, 0, 1), cv2.COLOR_BGR2HSV)
    hsv[..., 1] = np.clip(hsv[..., 1] * 1.6, 0, 1)
    out = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    # unsaturated surroundings (walls, ceiling, floor) drift cyan-teal against the pink
    sat = hsv[..., 1:2]
    neut = (1 - ms[..., None]) * np.clip(1 - sat * 3, 0, 1)
    out = out + neut * np.array([0.07, 0.03, -0.07], np.float32)
    breath = 1 + rng.normal(0, 0.015)
    x = np.clip(out * breath, 0, 1)
    out = x * x * (3 - 2 * x) * 0.75 + x * 0.25       # E-6 S-curve
    lum = out.mean(-1, keepdims=True)
    sh = np.clip(1 - lum * 2.2, 0, 1)
    out = out + sh * np.array([0.09, 0.05, -0.04], np.float32)   # teal-cyan shadows
    out = np.clip((out - 0.035) / 0.97, 0, 1)

    # halation: red-orange glow bleeding from highlights
    hi = np.clip(out.max(-1) - 0.78, 0, 1)
    hal = cv2.GaussianBlur(hi, (0, 0), 14)[..., None] * np.array([0.10, 0.25, 0.85], np.float32)
    out = out + hal * 0.35

    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    out = out * (1 - 0.22 * np.clip(r - 0.55, 0, 1) ** 1.5)[..., None]

    # slide-film grain: per channel, coarser in the shadows
    for c in range(3):
        out[..., c] += grain(rng, h, w) * (0.022 + 0.03 * sh[..., 0])
    # tiny per-frame colour breath of the emulsion
    out = out * (1 + rng.normal(0, 0.012, 3)).astype(np.float32)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), (np.clip(out, 0, 1) * 255).astype(np.uint8))
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    with Pool(min(8, os.cpu_count() or 2)) as p:
        for n in p.imap_unordered(render, ONLY):
            print("frame", n, flush=True)
