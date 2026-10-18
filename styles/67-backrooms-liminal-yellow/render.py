"""Backrooms Liminal Yellow restyle, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [all | frame numbers...]

Per frame:
  * flat, shadowless light: local contrast squashed toward a big blur
  * the whole room is mapped onto one mono-yellow ramp (olive-brown shadows,
    mustard mids, pale cream-yellow highlights); the people keep a little of
    their own colour under a sickly yellow cast
  * the white walls get the Level 0 wallpaper (thin vertical pinstripes with a
    small diamond motif) and faint damp blotches; the pattern is anchored to
    the room with a camera-shift track (phase correlation on the background)
  * the window turns into a blown-out fluorescent light box with a soft glow
  * fluorescent flicker (small exposure wobble, an occasional dip), slight
    wide-angle barrel distortion, soft focus, fine noise, vignette
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

# mono-yellow ramp, BGR 0..1, at luminance stops
STOPS = np.array([0.0, 0.18, 0.45, 0.72, 0.90, 1.0], np.float32)
RAMP = np.array([
    (0.03, 0.07, 0.08),      # near-black olive
    (0.06, 0.22, 0.27),      # olive brown
    (0.16, 0.55, 0.65),      # dirty mustard
    (0.32, 0.76, 0.85),      # Level 0 wall yellow
    (0.55, 0.91, 0.96),      # pale cream yellow
    (0.86, 0.99, 1.00),      # fluorescent white
], np.float32)


def mask(n):
    return cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255


def load(n):
    img = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png")).astype(np.float32) / 255
    m = mask(n)
    # the matte drops a motion-blurred hand on a few frames (23, 68): fill from the neighbours
    if 1 < n < N:
        a, b = mask(n - 1), mask(n + 1)
        if (m > 0.5).mean() < 0.8 * min((a > 0.5).mean(), (b > 0.5).mean()):
            m = np.maximum(m, np.maximum(a, b))
    return img, m


def camera_track():
    """Cumulative background shift (x, y) per frame, so the wallpaper sticks to the wall."""
    s = 4
    win = cv2.createHanningWindow((W // s, H // s), cv2.CV_32F)
    prev, pos, out = None, np.zeros(2), []
    for n in range(1, N + 1):
        img, m = load(n)
        g = cv2.cvtColor(cv2.resize(img, (W // s, H // s), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY)
        bg = 1 - cv2.dilate(cv2.resize(m, (W // s, H // s)), np.ones((9, 9), np.uint8))
        g = g * bg + (g * bg).sum() / max(bg.sum(), 1) * (1 - bg)
        if prev is not None:
            (dx, dy), resp = cv2.phaseCorrelate(prev, g, win)
            if resp > 0.05 and abs(dx) < 20 and abs(dy) < 20:
                pos += np.array([dx, dy]) * s
        out.append(pos.copy())
        prev = g
    return np.array(out, np.float32)


def wallpaper(ox, oy):
    """Level 0 wallpaper: pinstripes + small diamond motif, as a multiplicative 0.9..1.05 map."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    xx -= ox
    yy -= oy
    px, py = 34.0, 46.0
    u = np.mod(xx, px) / px
    v = np.mod(yy + np.floor(xx / px) % 2 * py / 2, py) / py
    stripe = np.exp(-((u - 0.0) ** 2) / 0.0015) + np.exp(-((u - 1.0) ** 2) / 0.0015)
    stripe += 0.6 * np.exp(-((u - 0.5) ** 2) / 0.0008)
    dia = np.clip(1 - (np.abs(u - 0.5) * 2.6 + np.abs(v - 0.5) * 2.0) * 2.2, 0, 1)
    dia = np.clip(dia * 2, 0, 1) - np.clip(dia * 2 - 1.3, 0, 1)        # outlined diamond
    pat = 1.0 - 0.13 * stripe - 0.11 * dia
    return cv2.GaussianBlur(pat, (0, 0), 0.9)


def damp(ox, oy):
    rng = np.random.default_rng(3)
    big = rng.random((40, 60)).astype(np.float32)
    big = cv2.resize(big, (W + 600, H + 400), interpolation=cv2.INTER_CUBIC)
    fine = cv2.resize(rng.random((160, 240)).astype(np.float32), (W + 600, H + 400), interpolation=cv2.INTER_CUBIC)
    d = np.clip((big * 0.8 + fine * 0.2 - 0.62) / 0.25, 0, 1)
    x0, y0 = int(np.clip(300 - ox, 0, 600)), int(np.clip(200 - oy, 0, 400))
    return d[y0:y0 + H, x0:x0 + W]


def ramp(lum):
    out = np.empty(lum.shape + (3,), np.float32)
    for c in range(3):
        out[..., c] = np.interp(lum, STOPS, RAMP[:, c])
    return out


def barrel(img, k=0.06):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    nx, ny = (xx - W / 2) / (W / 2), (yy - H / 2) / (W / 2)
    r2 = nx * nx + ny * ny
    f = (1 + k * r2) / (1 + k * 0.6)
    return cv2.remap(img, (nx * f * W / 2 + W / 2).astype(np.float32), (ny * f * W / 2 + H / 2).astype(np.float32),
                     cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)


TRACK = None


def render(n):
    rng = np.random.default_rng(500 + n)
    img, m = load(n)
    ms = cv2.GaussianBlur(m, (0, 0), 1.5)
    ox, oy = TRACK[n - 1]

    lum = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    v, sat = img.max(2), img.max(2) - img.min(2)
    # flat light: pull every pixel toward the big local average
    base = cv2.GaussianBlur(lum, (0, 0), 60)
    flat = np.clip(base * 0.55 + (lum - base) * 0.75 + 0.30, 0, 1)

    # walls: low-saturation mid-bright background -> wallpaper + damp blotches
    wall = np.clip((v - 0.42) / 0.12, 0, 1) * np.clip((0.88 - v) / 0.06, 0, 1) * np.clip((0.16 - sat) / 0.08, 0, 1)
    wall = cv2.GaussianBlur(cv2.morphologyEx(wall, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8)), (0, 0), 2) * (1 - ms)
    pat = wallpaper(ox, oy)
    dm = damp(ox, oy)
    flat = flat * (1 - wall * (1 - pat)) * (1 - wall * dm * 0.10)
    # walls sit at Level 0 yellow, not white
    flat = flat * (1 - wall * 0.10)

    room = ramp(flat)
    # people: sickly yellow cast but keep a bit of their own colour and contrast
    pl = np.clip(lum * 0.9 + 0.06, 0, 1)
    people = ramp(pl) * 0.70 + (img * np.array([0.45, 0.92, 1.05], np.float32)) * 0.30
    out = room * (1 - ms[..., None]) + people * ms[..., None]

    # window -> blown-out fluorescent light box with glow
    win = np.clip((v - 0.86) / 0.08, 0, 1) * np.clip((0.18 - sat) / 0.08, 0, 1) * (1 - ms)
    win = cv2.GaussianBlur(win, (0, 0), 2)
    out = out * (1 - win[..., None]) + RAMP[5] * win[..., None]
    glow = cv2.GaussianBlur(np.clip(out - 0.80, 0, 1), (0, 0), 25)
    out = out + glow * np.array([0.6, 1.0, 1.1], np.float32) * 0.9

    # overhead light fall-off: brighter top, darker bottom corners
    yy = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    xx = np.linspace(-1, 1, W, dtype=np.float32)[None, :]
    out *= (1.06 - 0.20 * yy ** 1.5 - 0.14 * xx ** 2 * yy)[..., None]

    # fluorescent flicker: small wobble, an occasional one-frame dip
    fl = 1.0 + 0.015 * np.sin(n * 2.3) + rng.normal(0, 0.008)
    if n % 41 in (17, 18):
        fl -= 0.07 if n % 41 == 17 else 0.03
    out = out * fl

    # soft, cheap wide-angle camera
    out = barrel(np.clip(out, 0, 1))
    out = cv2.GaussianBlur(out, (0, 0), 0.9)
    out += rng.normal(0, 0.016, (H, W, 1)).astype(np.float32) * np.array([0.8, 1, 1], np.float32)
    out = np.clip(out, 0, 1)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), (out * 255).astype(np.uint8))
    return n


def init(track):
    global TRACK
    TRACK = track


def main():
    os.makedirs(OUT, exist_ok=True)
    nums = list(range(1, N + 1)) if (not ARGS or ARGS == ["all"]) else [int(a) for a in ARGS]
    track = camera_track()
    with Pool(min(5, os.cpu_count() or 4), initializer=init, initargs=(track,)) as p:
        for _ in p.imap_unordered(render, nums):
            pass
    print("rendered", len(nums), "->", OUT)


if __name__ == "__main__":
    main()
