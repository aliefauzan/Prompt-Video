"""Giallo Gel Lighting (1970s Italian thriller), frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [all | frame numbers...]

  * the room is lit only by coloured theatre gels: the walls drown in
    blood red, the window turns into a cobalt-blue light box, the screen and
    plants go emerald green; everything else falls to crushed black
  * the people get a hard two-gel split: each body is lit red from its left
    side and cobalt blue from its right side (the split is found per row
    from the person masks, so every person has their own line down the face)
    with a narrow amber key in the middle, over their own shading
  * 1970s 35 mm: high contrast, diffusion-filter glow on highlights, warm
    grain regenerated every frame, a hair of gate weave, heavy vignette
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
RED = np.array([0.08, 0.06, 1.0], np.float32)          # BGR gels
BLUE = np.array([1.0, 0.32, 0.08], np.float32)
GREEN = np.array([0.42, 0.95, 0.18], np.float32)
AMBER = np.array([0.45, 0.78, 1.0], np.float32)


def smooth(x, a, b):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def render(n):
    rng = np.random.default_rng(6500 + n)
    img = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png")).astype(np.float32) / 255
    mr = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE)
    m = cv2.GaussianBlur(mr.astype(np.float32) / 255, (0, 0), 1.5)[..., None]
    lin = img ** 2.2
    luma = lin @ np.array([0.11, 0.59, 0.30], np.float32)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hue, sat = hsv[..., 0], hsv[..., 1]

    # ---------- background: gels on the set
    window = smooth(luma, 0.5, 0.9) * (1 - smooth(sat, 0.25, 0.5))
    blueish = np.exp(-((hue - 215) / 30) ** 2) * smooth(sat, 0.2, 0.45)
    greenish = np.exp(-((hue - 110) / 40) ** 2) * smooth(sat, 0.15, 0.35)
    green = np.clip(blueish + greenish, 0, 1)
    shade = luma ** 0.8
    bg = RED * (shade ** 1.25 * 0.95)[..., None]
    bg = bg * (1 - window[..., None]) + BLUE * (0.25 + 0.75 * luma)[..., None] * window[..., None]
    bg = bg * (1 - green[..., None]) + GREEN * (0.15 + 1.2 * luma)[..., None] * green[..., None]
    # pools of light: brighter low-centre, falling to black at the edges
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    pool = np.exp(-(((xx - W * 0.5) / (W * 0.55)) ** 2 + ((yy - H * 0.45) / (H * 0.7)) ** 2))
    bg *= (0.18 + 0.85 * pool ** 1.5)[..., None]

    # ---------- people: hard red / blue split per body, amber key between
    # which way each part of a body faces, from the slope of a heavily
    # blurred mask: left flanks face left (red gel), right flanks right (blue)
    mb = cv2.GaussianBlur(mr.astype(np.float32) / 255, (0, 0), 45)
    nx = cv2.Sobel(mb, cv2.CV_32F, 1, 0, ksize=5)
    nx = cv2.GaussianBlur(nx, (0, 0), 6)
    nx /= np.abs(nx).max() * 0.05 + 1e-6
    split = smooth(-nx, -0.2, 0.2)[..., None]
    key = np.exp(-(nx / 0.12) ** 2)[..., None] * 0.3
    gel = RED * (1 - split) + BLUE * split
    gel = gel * (1 - key) + AMBER * key
    form = np.clip(luma * 1.6, 0, 1) ** 0.85                  # own shading
    ppl = gel * form[..., None] * 1.3 + lin * 0.1             # a little true colour
    out = bg * (1 - m) + ppl * m

    # ---------- 70s film: contrast, diffusion glow, grain, weave
    out = np.clip(out, 0, 1.5) ** (1 / 2.2)
    out = np.clip(out, 0, 1)
    out = np.clip((out - 0.06) / 0.94, 0, 1)                   # crush blacks
    out = out + 0.35 * (out - 0.5) * (1 - np.abs(2 * out - 1))
    glow = cv2.GaussianBlur(np.clip(out - 0.45, 0, 1), (0, 0), 16)
    out = 1 - (1 - out) * (1 - glow * 0.9)
    gr = cv2.GaussianBlur(rng.normal(0, 1, (H, W)).astype(np.float32), (0, 0), 1.0)
    out = out + gr[..., None] * np.array([0.028, 0.032, 0.04], np.float32)
    r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
    out *= (1 - 0.55 * np.clip(r - 0.35, 0, 1) ** 1.3)[..., None]
    out = np.clip(out, 0, 1)
    dx, dy = rng.normal(0, 0.6), rng.normal(0, 0.8)
    out = cv2.warpAffine(out, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), (np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8))
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
