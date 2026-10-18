"""Pixel Stretch Slit Streak, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [all | frame numbers...]

Per frame:
  * the people stay the untouched source pixels (person mask, soft edge)
  * on every pixel row, each person is sampled at a slit just inside their
    trailing (left) edge, about 1/9 of the row's silhouette width deep and at
    most 34 px (median of a short run, so mask jitter does not flicker it);
    that colour is extruded sideways as a hard one-pixel-tall streak until it
    meets the next person or the frame edge; the thin strip of the person
    behind the slit is swallowed by the streak, so they seem to tear out of it
  * so every person trails a band of long, hard-edged colour ribbons made of
    their own hair / skin / shirt colours, like a Photoshop "pixel stretch"
  * the ribbons get a slight sheen falloff with distance and a fine 1 px
    row-to-row contrast so they read as stretched pixels, not motion blur
  * rows above and below the people keep the real room, sharp
"""
import os
import sys

import cv2
import numpy as np

FRAMES, MASKS, OUT = sys.argv[1:4]
ARGS = sys.argv[4:]
N = len([f for f in os.listdir(FRAMES) if f.startswith("frame_") and f.endswith(".png")])
DIRECTION = -1          # -1: streaks run to the left of each person (motion to the right)
INSET = (34, 46)        # the slit: a short run this far inside the silhouette edge
SAT, CONTRAST = 1.35, 1.12   # ribbons are pushed a little, like a graded edit


def load(n):
    img = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png"))
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE)
    return img, m


def runs(row):
    d = np.diff(np.concatenate(([0], row.astype(np.int8), [0])))
    return np.flatnonzero(d == 1), np.flatnonzero(d == -1)   # start, end (exclusive)


def render(n):
    img, m8 = load(n)
    H, W = m8.shape
    mb = cv2.morphologyEx((m8 > 127).astype(np.uint8), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    if DIRECTION > 0:                      # work in a mirrored frame, flip back at the end
        img, mb, m8 = img[:, ::-1].copy(), mb[:, ::-1].copy(), m8[:, ::-1].copy()

    streak = img.astype(np.float32).copy()
    filled = np.zeros((H, W), bool)
    dist = np.zeros((H, W), np.float32)
    xs = np.arange(W)
    for y in range(H):
        st, en = runs(mb[y])
        prev_end = 0
        for s, e in zip(st, en):
            if e - s >= 6:
                a = s + min(INSET[0], max(3, (e - s) // 9))
                b = a + max(3, min(INSET[1] - INSET[0], (e - s) // 12))
                col = np.median(img[y, a:b].astype(np.float32), axis=0)
                lo = prev_end
                if a > lo:
                    streak[y, lo:a] = col
                    filled[y, lo:a] = True
                    dist[y, lo:a] = (a - xs[lo:a]) / W
            prev_end = e

    # sheen: ribbons darken a little away from the subject, with a soft
    # highlight band near the source edge, like stretched glossy pixels
    shade = 1.0 - 0.28 * np.clip(dist, 0, 1) ** 0.8 + 0.10 * np.exp(-dist * 40)
    # fine row contrast so single-pixel rows stay readable after scaling
    rowj = 1.0 + 0.04 * np.sin(np.arange(H) * 2.1)[:, None]
    streak = np.where(filled[..., None], streak * (shade * rowj)[..., None], streak)
    hsv = cv2.cvtColor(np.clip(streak, 0, 255).astype(np.uint8), cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[..., 1] = np.clip(hsv[..., 1] * SAT, 0, 255)
    hsv[..., 2] = np.clip((hsv[..., 2] - 128) * CONTRAST + 128, 0, 255)
    graded = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32)
    streak = np.where(filled[..., None], graded, streak)

    # the slit is a hard cut: the strip of each person behind it is replaced too
    a = cv2.GaussianBlur(m8.astype(np.float32) / 255, (0, 0), 1.0)
    a = np.where(filled, 0.0, a)[..., None]
    out = streak * (1 - a) + img.astype(np.float32) * a
    out = out.astype(np.uint8)
    if DIRECTION > 0:
        out = out[:, ::-1]
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), out)
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    todo = range(1, N + 1) if not ARGS or ARGS == ["all"] else [int(a) for a in ARGS]
    for n in todo:
        render(n)
        print(n, end=" ", flush=True)
    print()
