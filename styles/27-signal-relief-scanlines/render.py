"""Signal Relief: Rutt-Etra style luminance-displaced scanlines, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [frame numbers...]

The picture is rebuilt from dense vertical scan lines on a dark navy ground.
Each line is pushed sideways by the brightness under it, so people rise out of
the line field as a ribbed relief; a hard black offset copy of the displaced
lines gives the extruded 3D shadow. The background lines stay almost straight.
Lines are drawn implicitly: a pixel is "on a line" when its displaced
horizontal coordinate lands on the line grid.
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np

FRAMES, MASKS, OUT = sys.argv[1:4]
ONLY = [int(a) for a in sys.argv[4:]] or [13, 49, 85, 109, 145, 178]

SPACING = 8.0          # px between scan lines at 1620 wide
AMP_SUBJECT = 26.0     # max sideways push on people
AMP_BG = 3.5           # background lines barely move
HALF_W = 1.35          # line half width, px
SHADOW = (5, 3)        # extrusion offset (dx, dy)

NAVY = np.array([0.10, 0.04, 0.02], np.float32)          # BGR ground between lines
BLUE_LO = np.array([0.62, 0.30, 0.10], np.float32)       # dark-tone line colour
BLUE_HI = np.array([1.00, 0.72, 0.42], np.float32)       # highlight line colour


def lines(u, s, dudx, hw):
    """Anti-aliased line intensity for displaced coordinate field u (hw = half width map)."""
    c = u / s
    d = np.abs(c - np.round(c)) * s / np.maximum(np.abs(dudx), 0.25)
    return np.clip(hw + 0.5 - d, 0, 1)


def render(n):
    rng = np.random.default_rng(2000 + n)
    img = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png"))
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), 0).astype(np.float32) / 255
    h, w = m.shape
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    L = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8)).apply(gray).astype(np.float32) / 255
    L = cv2.GaussianBlur(L, (0, 0), 1.2)
    ms = cv2.GaussianBlur(m, (0, 0), 3)

    # signal noise: the relief "boils" a little every frame
    noise = cv2.resize(rng.normal(0, 1, (h // 6, w // 6)).astype(np.float32), (w, h), interpolation=cv2.INTER_CUBIC)
    amp = AMP_SUBJECT * ms + AMP_BG * (1 - ms)
    disp = amp * (L + 0.03 * noise)
    # occasional horizontal tear rows (sync wobble)
    tear = np.zeros(h, np.float32)
    for _ in range(rng.integers(1, 4)):
        y0, hh = rng.integers(0, h), rng.integers(4, 26)
        tear[y0:y0 + hh] += rng.uniform(-9, 9)
    disp += tear[:, None]

    xx = np.tile(np.arange(w, dtype=np.float32), (h, 1))
    phase = rng.uniform(0, SPACING)
    u = xx - disp + phase
    dudx = 1 - np.gradient(disp, axis=1)
    hw = HALF_W * (0.55 + 0.9 * L) * ms + HALF_W * (1 - ms)    # highlights draw fatter lines
    on = lines(u, SPACING, dudx, hw)

    # extrusion: same lines shifted, people only, painted black under the real lines
    sx, sy = SHADOW
    M = np.float32([[1, 0, sx], [0, 1, sy]])
    sh = cv2.warpAffine(on * ms, M, (w, h))
    sh = cv2.dilate(sh, np.ones((2, 3), np.uint8))

    tone = (L ** 1.2)[..., None]
    col = BLUE_LO * (1 - tone) + BLUE_HI * tone
    bright = (0.32 + 0.78 * tone) * ms[..., None] + 0.95 * (1 - ms[..., None])   # dark tones fade into the ground
    col = col * bright
    col = col * (0.75 + 0.25 * rng.uniform(0.9, 1.1))          # brightness flicker
    out = np.broadcast_to(NAVY, (h, w, 3)).copy()
    out *= (1 - 0.9 * sh[..., None])
    out = out * (1 - on[..., None]) + col * on[..., None]

    # CRT-ish softness + faint glow, then fine noise
    glow = cv2.GaussianBlur(out, (0, 0), 3.5)
    out = out + glow * 0.35
    out += rng.normal(0, 0.012, out.shape).astype(np.float32)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), (out.clip(0, 1) * 255).astype(np.uint8))
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    with Pool(min(6, os.cpu_count() or 2)) as p:
        for n in p.imap_unordered(render, ONLY):
            print("frame", n)
