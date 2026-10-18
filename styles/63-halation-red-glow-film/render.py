"""Halation Red-Glow Film (CineStill 800T), frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [all | frame numbers...]

Per frame:
  * a dim tungsten-night grade: about one stop under, lifted film blacks,
    cyan-green shadows, warm but natural skin (the masks hold skin back from
    the cool shift), deep inky midtones
  * HALATION: every highlight (window, monitor, white stripes, skin and hair
    speculars) grows a red-orange halo. The halo is built from the
    highlights of the *original* exposure, blurred at two radii, tinted red
    and kept off the bright core, so it reads as a glowing rim around light,
    like CineStill 800T with no rem-jet layer
  * a faint warm bloom on the brightest areas
  * 800-speed grain, regenerated every frame, stronger in the shadows
  * the halo strength breathes a few percent frame to frame
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np

FRAMES, MASKS, OUT = sys.argv[1:4]
ARGS = sys.argv[4:]
N = len([f for f in os.listdir(FRAMES) if f.startswith("frame_") and f.endswith(".png")])
W, H = 1620, 1080
HALO_BGR = np.array([0.02, 0.16, 1.0], np.float32)    # red-orange


def smooth(x, a, b):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def render(n):
    rng = np.random.default_rng(6300 + n)
    img = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png")).astype(np.float32) / 255
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
    m = cv2.GaussianBlur(m, (0, 0), 3)[..., None]
    lin = img ** 2.2
    luma = lin @ np.array([0.11, 0.59, 0.30], np.float32)

    # --- highlights that will halate (from the original exposure)
    hi = smooth(luma, 0.5, 0.92)
    halo = cv2.GaussianBlur(hi, (0, 0), 6) * 0.45 + cv2.GaussianBlur(hi, (0, 0), 20) * 1.1 \
        + cv2.GaussianBlur(hi, (0, 0), 55) * 0.8
    halo = np.clip(halo - hi * 1.3, 0, None)              # rim, not the core
    halo *= 1 + 0.05 * np.sin(n * 1.7) + rng.normal(0, 0.02)

    # --- tungsten night grade: the room drops ~1.5 stops, light sources hold
    keep = smooth(luma, 0.55, 0.97)[..., None]
    g = lin * (0.2 + 0.2 * m) * (1 - keep) + lin * 1.0 * keep
    # cool cyan-green scene, warmer people
    cool = np.array([1.22, 1.06, 0.72], np.float32)        # BGR multipliers
    warm = np.array([0.9, 1.0, 1.1], np.float32)
    g = g * (cool * (1 - m * 0.75) + warm * m * 0.75)
    g = np.clip(g, 0, 1) ** (1 / 2.2)
    # film toe: lifted, cyan-green blacks
    g = np.clip(g + 0.35 * (g - 0.45) * (1 - np.abs(2 * g - 1)), 0, 1)   # contrast
    shadow = np.array([0.06, 0.05, 0.015], np.float32)
    g = shadow + g * (1 - shadow)
    # reds/oranges a little richer, the rest a little muted
    hsv = cv2.cvtColor(np.clip(g, 0, 1), cv2.COLOR_BGR2HSV)
    h = hsv[..., 0]
    redness = np.exp(-(np.minimum(h, 360 - h) / 30) ** 2)
    hsv[..., 1] = np.clip(hsv[..., 1] * (0.85 + 0.45 * redness), 0, 1)
    g = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    # --- halation (additive red) and a faint warm bloom
    g = g + halo[..., None] * HALO_BGR * 1.1
    bloom = cv2.GaussianBlur(hi, (0, 0), 12)[..., None] * np.array([0.5, 0.6, 0.75], np.float32) * 0.18
    g = 1 - (1 - np.clip(g, 0, 1)) * (1 - bloom)
    # bright cores stay hot, slightly warm-white
    core = smooth(luma, 0.6, 1.0)[..., None]
    g = g * (1 - core * 0.4) + core * 0.4 * np.array([0.9, 0.96, 1.0], np.float32)

    # --- 800 speed grain, stronger in shadows, slight chroma
    gl = cv2.GaussianBlur(rng.normal(0, 1, (H, W)).astype(np.float32), (0, 0), 0.9)
    gc = cv2.GaussianBlur(rng.normal(0, 1, (H, W, 3)).astype(np.float32), (0, 0), 1.4)
    lum = g.mean(2, keepdims=True)
    amt = 0.022 + 0.03 * (1 - lum)
    g = g + gl[..., None] * amt + gc * 0.008
    # soft film-scan sharpness
    g = cv2.GaussianBlur(g, (0, 0), 0.6)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
    g *= (1 - 0.25 * np.clip(r - 0.5, 0, 1) ** 1.4)[..., None]
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), (np.clip(g, 0, 1) * 255 + 0.5).astype(np.uint8))
    return n


def main():
    os.makedirs(OUT, exist_ok=True)
    nums = list(range(1, N + 1)) if not ARGS or ARGS == ["all"] else [int(a) for a in ARGS]
    with Pool(3) as p:
        for n in p.imap(render, nums):
            print(n, end=" ", flush=True)
    print()


if __name__ == "__main__":
    main()
