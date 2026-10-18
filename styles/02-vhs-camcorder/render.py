"""90s VHS camcorder home-video restyle, frame by frame.

usage: python -I render.py <frames_dir> <out_dir> [frame numbers... | all]
Default frames: the six sheet frames. Whole-frame signal emulation, so no
person mask is needed: identity and pose stay exactly as in the source.

Pipeline per frame (NTSC-ish 720x480 working size, then back up to source size):
  colour grade -> on-screen display burned in -> luma low-pass + edge-enhance ringing
  -> chroma (YIQ I/Q) low-pass, delayed right, noisy -> per-line jitter
  -> tracking band + snow streaks -> head-switching noise at the bottom
  -> tape noise -> soft upscale + faint interlace lines.
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FRAMES, OUT = sys.argv[1:3]
ARGS = sys.argv[3:]
N = len([f for f in os.listdir(FRAMES) if f.endswith(".png")])
SHEET = [13, 49, 85, 109, 145, 178]
W, H = 720, 480

# BGR <-> YIQ
TO_YIQ = np.array([[0.114, 0.587, 0.299],
                   [-0.322, -0.274, 0.596],
                   [0.312, -0.523, 0.211]], np.float32)
FROM_YIQ = np.linalg.inv(TO_YIQ).astype(np.float32)

MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]


def font(size):
    for p, i in (("/System/Library/Fonts/Menlo.ttc", 1), ("/System/Library/Fonts/Monaco.ttf", 0)):
        try:
            return ImageFont.truetype(p, size, index=i)
        except OSError:
            pass
    return ImageFont.load_default()


def grade(img):
    """Camcorder CCD colour: lifted blacks, clipped hot whites, warm-green fluorescent cast."""
    b, g, r = img[..., 0], img[..., 1], img[..., 2]
    y = 0.114 * b + 0.587 * g + 0.299 * r
    sat = 1.08
    img = y[..., None] + (img - y[..., None]) * sat
    img = img * np.array([0.93, 1.0, 1.04], np.float32)            # warm, slight green
    img = 0.055 + img * 1.02                                       # lifted, milky blacks
    img = np.where(img > 0.82, 0.82 + (img - 0.82) * 0.45, img)     # soft-clipped highlights
    return img.clip(0, 1)


def osd(img, n, rng):
    """Burn the camcorder on-screen display into the 720x480 frame (white, black shadow)."""
    pil = Image.fromarray((img[..., ::-1] * 255).astype(np.uint8))
    d = ImageDraw.Draw(pil)
    f, fs = font(26), font(22)
    secs = (n - 1) // 12
    rec = n <= 60 or n > 120
    def txt(x, y, s, fill=(250, 250, 250), fo=f):
        d.text((x + 2, y + 2), s, font=fo, fill=(10, 10, 10))
        d.text((x, y), s, font=fo, fill=fill)
    if rec:
        if (n // 6) % 2 == 0:                                       # blinking dot
            d.ellipse((40, 36, 60, 56), fill=(235, 30, 30))
        txt(70, 30, "REC")
        # battery icon
        d.rectangle((600, 36, 650, 56), outline=(250, 250, 250), width=3)
        d.rectangle((650, 41, 655, 51), fill=(250, 250, 250))
        for k in range(3):
            d.rectangle((605 + k * 15, 41, 615 + k * 15, 51), fill=(250, 250, 250))
        txt(40, 66, f"0:00:{secs:02d}", fo=fs)
    else:
        txt(40, 30, "PLAY ▶")
        txt(610, 30, "SP")
        txt(40, 66, f"0:{secs // 60:02d}:{secs % 60:02d}", fo=fs)
    txt(470, 388, f"{MONTHS[9]}.18 1997")
    txt(470, 420, f"10:24:{(7 + secs) % 60:02d} AM")
    return np.asarray(pil)[..., ::-1].astype(np.float32) / 255


def hshift_rows(ch, offs):
    """Shift each row of a 2-D channel horizontally by offs[y] pixels (float, edge fill)."""
    h, w = ch.shape
    xs = np.arange(w, dtype=np.float32)[None, :] - offs[:, None].astype(np.float32)
    ys = np.repeat(np.arange(h, dtype=np.float32)[:, None], w, 1)
    return cv2.remap(ch, xs, ys, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)


def render(n):
    rng = np.random.default_rng(9000 + n)
    src = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png")).astype(np.float32) / 255
    sh, sw = src.shape[:2]
    img = cv2.resize(src, (W, H), interpolation=cv2.INTER_AREA)
    img = grade(img)
    img = osd(img, n, rng)

    yiq = img @ TO_YIQ.T
    Y, I, Q = yiq[..., 0], yiq[..., 1], yiq[..., 2]

    # luma: ~3 MHz bandwidth (soft) + edge-enhancement ringing halos
    Y = cv2.GaussianBlur(Y, (0, 0), sigmaX=1.6, sigmaY=0.6)
    Y = Y + 0.85 * (Y - cv2.GaussianBlur(Y, (0, 0), sigmaX=3.5, sigmaY=0.3))
    # chroma: ~0.5 MHz, smeared and delayed to the right, slightly undersaturated reds bleed
    for c in (I, Q):
        c[:] = cv2.GaussianBlur(c, (0, 0), sigmaX=7.0, sigmaY=1.0)
    I = np.roll(I, 9, axis=1)
    Q = np.roll(Q, 6, axis=1)
    # chroma noise: horizontal colour streaks
    cn = cv2.GaussianBlur(rng.normal(0, 1, (H, W)).astype(np.float32), (0, 0), sigmaX=9, sigmaY=0.5)
    I += cn * 0.05
    Q += np.roll(cn, 40, axis=0) * 0.04

    # per-line time-base jitter (wobble)
    jit = cv2.GaussianBlur(rng.normal(0, 1, (H, 1)).astype(np.float32), (0, 0), 3)[:, 0] * 2.2
    jit += np.sin(np.arange(H) / 37.0 + n * 0.9) * 0.6
    # tracking band: a horizontal zone of displaced, noisy lines that rolls through the frame
    band_on = (n % 36) < 20
    by = int((n * 23) % (H + 160)) - 80
    bh = int(rng.integers(18, 34))
    band = np.zeros(H, np.float32)
    if band_on:
        yy = np.arange(H)
        band = np.exp(-((yy - by) / bh) ** 2).astype(np.float32)
        jit += band * rng.normal(0, 1, H).astype(np.float32) * 9
    # head-switching noise: bottom lines torn sideways
    hs = 12
    jit[-hs:] += np.linspace(4, 26, hs) + rng.normal(0, 3, hs)

    Y = hshift_rows(Y, jit)
    I = hshift_rows(I, jit * 1.1)
    Q = hshift_rows(Q, jit * 1.1)

    # snow streaks inside tracking band and a few random dropouts
    streak = (rng.random((H, W)) > 0.9955).astype(np.float32)
    streak = cv2.GaussianBlur(cv2.dilate(streak, np.ones((1, 25), np.uint8)), (0, 0), sigmaX=4, sigmaY=0.4)
    Y += streak * (0.75 * band[:, None] + 0.04) * 1.5
    drop_rows = rng.integers(0, H, 2)
    for r in drop_rows:
        x0 = int(rng.integers(0, W - 120))
        Y[r, x0:x0 + int(rng.integers(30, 160))] += 0.6
    Y[-hs:] = Y[-hs:] * 0.75 + rng.random((hs, W)).astype(np.float32) * 0.25

    # tape noise (luma grain is horizontally stretched)
    Y += cv2.GaussianBlur(rng.normal(0, 1, (H, W)).astype(np.float32), (0, 0), sigmaX=1.2, sigmaY=0.3) * 0.035

    out = np.stack([Y, I, Q], -1) @ FROM_YIQ.T
    # dark blanking edge on the left, frayed right edge
    out[:, :6] *= 0.15
    out[:, -4:] *= 0.5
    out = out.clip(0, 1)

    out = cv2.resize(out, (sw, sh), interpolation=cv2.INTER_LINEAR)
    lines = (np.arange(sh) % 4 < 2).astype(np.float32)[:, None, None]
    out = out * (1 - 0.07 * lines)
    # soft bloom on bright areas (tube/CCD smear)
    hi = np.clip(out - 0.7, 0, 1)
    out = out + cv2.GaussianBlur(hi, (0, 0), 12) * 0.6
    # vignette
    yy, xx = np.mgrid[0:sh, 0:sw].astype(np.float32)
    v = ((xx / sw - 0.5) ** 2 + (yy / sh - 0.5) ** 2)
    out *= (1 - 0.35 * v)[..., None]
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), (out.clip(0, 1) * 255).astype(np.uint8))
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    todo = list(range(1, N + 1)) if ARGS == ["all"] else ([int(a) for a in ARGS] or SHEET)
    with Pool(min(8, len(todo))) as p:
        for n in p.imap_unordered(render, todo):
            print(n, end=" ", flush=True)
    print()
