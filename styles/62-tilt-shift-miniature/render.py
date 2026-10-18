"""Tilt-Shift Miniature, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [all | frame numbers...]

Per frame:
  * a thin horizontal plane of focus sits across the faces; its height is
    found from the person masks and smoothed over the whole clip so it glides
  * everything above and below that band is blurred by vertical position only
    (not by depth), so the people's hair, chests and hands go soft too: the
    optical cue that makes a real scene read as a tabletop model
  * the blur ramps up smoothly (lens-like disc blur with bright highlights)
  * toy-model colour: strong saturation, punchy S-curve, bright high key,
    slightly smoothed plastic-looking surfaces inside the band, crisp edges
  * light vignette; no grain (miniatures look clean)
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
SIGMAS = [0, 3, 6, 10, 15, 21, 28]     # blur levels, px
SHARP = 55                               # half height of the fully sharp band
RAMP = 360                               # distance over which blur reaches max


def band_centres():
    """Row of the focus band for every frame: across the faces, smoothed."""
    c = []
    for n in range(1, N + 1):
        m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE)
        rows = np.where((m > 128).sum(1) > 25)[0]
        top = rows[0] if len(rows) else 200
        # faces: from the top of the highest head down ~ a head height;
        # bigger (closer) heads get a lower centre
        width = (m[min(top + 60, H - 1)] > 128).sum()
        c.append(top + np.clip(width * 0.75, 90, 230))
    c = np.array(c, np.float32)
    k = 7
    pad = np.pad(c, k, mode="edge")
    return np.convolve(pad, np.ones(2 * k + 1) / (2 * k + 1), mode="same")[k:-k]


KEY = 0.10                               # keystone: top row shows 10% more width


def keystone(img):
    """Fake a camera tilted down at a tabletop: the top of the frame (far
    away) shrinks, the bottom (near) grows. Zoomed so no border shows."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    s = (1 + KEY * (1 - yy / H)) / (1 + KEY)
    mx = (W / 2 + (xx - W / 2) * s).astype(np.float32)
    my = (H * 0.04 + yy * 0.96 * (1 - 0.04 * (1 - yy / H))).astype(np.float32)
    return cv2.remap(img, mx, my, cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)


def disc(r):
    if r < 1:
        return None
    r = int(round(r))
    k = np.zeros((2 * r + 1, 2 * r + 1), np.float32)
    cv2.circle(k, (r, r), r, 1.0, -1, cv2.LINE_AA)
    return k / k.sum()


def grade(img):
    """Toy-model colour: saturated, contrasty, bright; skin held back so it
    stays skin while greens, blues and neutrals go candy-bright."""
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2Lab)
    L, a, b = lab[..., 0], lab[..., 1], lab[..., 2]
    hue = np.degrees(np.arctan2(b, a)) % 360
    chroma = np.hypot(a, b)
    skin = np.exp(-((hue - 55) / 22) ** 2) * (chroma > 8)     # orange-ish hues
    gain = 2.8 - 1.25 * skin
    lab[..., 1] = a * gain
    lab[..., 2] = b * gain
    # cool neutrals (walls, grey shirt) a little minty-blue, toy paint
    lab[..., 1] -= 2.5 * (1 - skin) * (chroma < 10)
    lab[..., 2] -= 3.0 * (1 - skin) * (chroma < 10)
    lab[..., 0] = np.clip(L * 1.02 + 7, 0, 100)
    out = np.clip(cv2.cvtColor(lab, cv2.COLOR_Lab2BGR), 0, 1)
    # S-curve
    out = out + 0.5 * (out - 0.5) * (1 - np.abs(2 * out - 1)) * 1.7
    return np.clip(out, 0, 1)


def render(n, centre):
    img = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png")).astype(np.float32) / 255
    img = cv2.resize(img, (W, H)) if img.shape[:2] != (H, W) else img
    # plastic smoothing: flatten fine texture a little, keep edges
    smooth = cv2.bilateralFilter(img, 9, 0.08, 6)
    img = cv2.addWeighted(img, 0.45, smooth, 0.55, 0)
    # crisp model edges
    soft = cv2.GaussianBlur(img, (0, 0), 1.6)
    img = np.clip(img + 0.9 * (img - soft), 0, 1)
    img = grade(img)
    img = np.clip(keystone(img), 0, 1)

    # lens blur stack in linear-ish light so highlights bloom into discs
    lin = img ** 2.2
    stack = [lin]
    for s in SIGMAS[1:]:
        stack.append(cv2.filter2D(lin, -1, disc(s * 1.3)))
    stack = np.stack(stack)                                   # L,H,W,3

    y = np.arange(H, dtype=np.float32)
    # above the band the frame is short, so the ramp is shorter: the top
    # edge always ends fully soft, like a lens tilted toward the floor
    up = max(120.0, 0.8 * (centre - SHARP))
    d = np.where(y < centre, (centre - y - SHARP) / up, (y - centre - SHARP) / RAMP)
    d = np.clip(d, 0, 1)
    d = d ** 1.25 * (len(SIGMAS) - 1)                         # fractional level
    lo = np.floor(d).astype(int)
    hi = np.minimum(lo + 1, len(SIGMAS) - 1)
    t = (d - lo)[:, None, None]
    rows = np.arange(H)
    out = stack[lo, rows] * (1 - t) + stack[hi, rows] * t     # H,W,3
    out = np.clip(out, 0, 1) ** (1 / 2.2)

    # vignette
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
    out *= (1 - 0.18 * np.clip(r - 0.55, 0, 1) ** 1.5)[..., None]
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), (np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8))
    return n


def main():
    os.makedirs(OUT, exist_ok=True)
    centres = band_centres()
    nums = list(range(1, N + 1)) if not ARGS or ARGS == ["all"] else [int(a) for a in ARGS]
    with Pool(3) as p:
        for n in p.starmap(render, [(n, float(centres[n - 1])) for n in nums]):
            print(n, end=" ", flush=True)
    print()


if __name__ == "__main__":
    main()
