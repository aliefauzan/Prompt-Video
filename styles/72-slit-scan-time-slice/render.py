"""Slit-Scan Time-Slice (时间切片), frame by frame from neighbouring frames.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [all | frame numbers...]

Needs the whole 12 fps frame sequence: every output frame is assembled from
several source frames around it.

Per output frame n:
  * the frame is cut into parallel diagonal bands (tilted ~22 deg from vertical)
  * band k shows source frame n + offset(k): offsets step by STEP frames from
    band to band (a staircase of time, past on the left, future on the right),
    so one image holds a ~2.7 s sweep; time indices reflect at the clip ends
  * band edges are hard, with a thin bright seam line and a soft shadow, like
    strips of separate prints laid side by side; nothing is blended or blurred
  * the bands drift slowly to the left over the clip, so the cut lines sweep
    across the people and the time staircase keeps re-slicing them
"""
import os
import sys

import cv2
import numpy as np

FRAMES, MASKS, OUT = sys.argv[1:4]
ARGS = sys.argv[4:]
N = len([f for f in os.listdir(FRAMES) if f.startswith("frame_") and f.endswith(".png")])
W, H = 1620, 1080
BANDS = 9              # bands across the frame width
STEP = 4               # source frames between neighbouring bands (1/3 s)
ANGLE = np.deg2rad(22)  # tilt of the cut lines from vertical
DRIFT = 2.2            # px per output frame the band grid slides left
SEAM = 3               # seam width in px

_cache = {}


def frame(i):
    if i not in _cache:
        if len(_cache) > 40:
            _cache.pop(next(iter(_cache)))
        _cache[i] = cv2.imread(os.path.join(FRAMES, f"frame_{i:03d}.png"))
    return _cache[i]


def reflect(i):
    """Map any index onto 1..N by mirroring at the clip ends."""
    p = 2 * (N - 1)
    j = (i - 1) % p
    return 1 + (j if j < N - 1 else p - j)


yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
# coordinate across the bands (perpendicular to the tilted cut lines)
U = xx * np.cos(ANGLE) + (H - yy) * np.sin(ANGLE)
U_SPAN = W * np.cos(ANGLE) + H * np.sin(ANGLE)
BW = U_SPAN / BANDS


def render(n):
    u = U + DRIFT * n
    k = np.floor(u / BW).astype(np.int32)
    frac = u - k * BW
    out = np.zeros((H, W, 3), np.float32)
    for kk in np.unique(k):
        off = (int(kk) % BANDS - BANDS // 2) * STEP
        sel = k == kk
        out[sel] = frame(reflect(n + off))[sel]
    # hard seams: a thin light line on the cut, a soft shadow just after it
    seam = frac < SEAM
    shadow = np.clip(1 - (frac - SEAM) / 22, 0, 1) * (frac >= SEAM)
    out *= (1 - 0.28 * shadow)[..., None]
    out[seam] = out[seam] * 0.25 + 245 * 0.75
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), np.clip(out, 0, 255).astype(np.uint8))
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    todo = range(1, N + 1) if not ARGS or ARGS == ["all"] else [int(a) for a in ARGS]
    for n in todo:
        render(n)
        print(n, end=" ", flush=True)
    print()
