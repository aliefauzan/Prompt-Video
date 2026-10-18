"""Chronophotography Strobe (频闪 残影), frame by frame from earlier frames.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [all | frame numbers...]

Needs the whole 12 fps frame sequence + person masks: every output frame
stacks the people from several earlier source frames.

Per output frame n (Marey "fixed-plate" chronophotograph, as a strobe video):
  * the room is crushed to a near-black velvet ground (a faint cool trace
    of it survives, like an underexposed plate)
  * the people are lit like a strobe flash on a black backdrop: silvery,
    mostly desaturated, hard contrast, crisp edges
  * STROBE: copies of the people from frames n-3, n-6, n-9, n-12 (a 4 Hz
    flash) are laid down first with falling exposure, combined "lighten"
    (max), as several exposures on one plate add up; each copy is a crisp
    frozen pose, never smeared
  * the current pose is laid on top at full exposure, so the newest copy is
    always clean and in front
  * film-plate finish: fine grain, slight vignette, and a thin white
    graduated scale along the bottom like Marey's measuring rule
"""
import os
import sys

import cv2
import numpy as np

FRAMES, MASKS, OUT = sys.argv[1:4]
ARGS = sys.argv[4:]
N = len([f for f in os.listdir(FRAMES) if f.startswith("frame_") and f.endswith(".png")])
W, H = 1620, 1080
ECHOES = [(3, 0.78), (6, 0.60), (9, 0.45), (12, 0.33)]   # (frames back, exposure)
SAT = 0.30             # how much colour survives the flash
BG_LEVEL = 0.055       # how much of the room survives as a faint plate
LIFT = 0.16            # floor of the flash-lit people, so dark clothes read on black

_cache = {}


def load(i):
    i = min(max(i, 1), N)
    if i not in _cache:
        if len(_cache) > 30:
            _cache.pop(next(iter(_cache)))
        img = cv2.imread(os.path.join(FRAMES, f"frame_{i:03d}.png")).astype(np.float32) / 255
        m = cv2.imread(os.path.join(MASKS, f"frame_{i:03d}.png"), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
        # pull the matte in 2 px so no window-white fringe rides on the copies
        m = cv2.erode(m, np.ones((5, 5), np.uint8))
        m = cv2.GaussianBlur(m, (0, 0), 0.8)
        _cache[i] = (flash(img), m)
    return _cache[i]


def flash(img):
    """Strobe-lit silver: mostly grey, hard S-curve, cool highlights."""
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)[..., None]
    c = g + (img - g) * SAT
    c = np.clip((c - 0.08) / 0.84, 0, 1)
    c = c * c * (3 - 2 * c)                              # S-curve
    c = c ** 0.85
    c = LIFT + (1 - LIFT) * c                            # the flash lights even dark clothes
    return c * np.array([1.04, 1.0, 0.95], np.float32)   # BGR: slightly cool


yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
VIGNETTE = (1 - 0.35 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2))[..., None]


def scale_bar(out):
    """Thin graduated rule along the bottom edge (Marey's measuring scale)."""
    y0 = H - 34
    cv2.line(out, (40, y0), (W - 40, y0), (0.85, 0.85, 0.85), 2, cv2.LINE_AA)
    for i, x in enumerate(np.linspace(40, W - 40, 61)):
        L = 16 if i % 10 == 0 else (10 if i % 5 == 0 else 6)
        cv2.line(out, (int(x), y0), (int(x), y0 - L), (0.85, 0.85, 0.85), 2, cv2.LINE_AA)


def render(n):
    rng = np.random.default_rng(n)
    cur, cm = load(n)
    raw = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png")).astype(np.float32) / 255
    g = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)[..., None]
    out = (g * BG_LEVEL * np.array([1.15, 1.0, 0.85], np.float32)) * (1 - cm[..., None])

    for back, expo in reversed(ECHOES):                  # oldest first
        img, m = load(n - back)
        out = np.maximum(out, img * expo * m[..., None])
    a = cm[..., None]
    out = out * (1 - a) + cur * a

    # a faint halo around the newest copy, like flash spill on the backdrop
    halo = cv2.GaussianBlur(cm, (0, 0), 18)[..., None] * (1 - a)
    out = out + 0.05 * halo

    out = out * VIGNETTE
    out = out + cv2.GaussianBlur(rng.normal(0, 0.03, (H, W)).astype(np.float32), (0, 0), 0.9)[..., None]
    scale_bar(out)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), (np.clip(out, 0, 1) * 255).astype(np.uint8))
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    todo = range(1, N + 1) if not ARGS or ARGS == ["all"] else [int(a) for a in ARGS]
    for n in todo:
        render(n)
        print(n, end=" ", flush=True)
    print()
