"""Thermal fax / receipt print restyle, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [all | frame numbers...]

Built like each frame was sent through a fax and spat out of a thermal printer:
  1-BIT DOTS: the picture is printed at a coarse 1/3 resolution (540 dots
    across, like a 203 dpi head) with a stochastic, noisy threshold dither:
    every dot is either burnt black or left as paper, no greys, no colour.
  PRINT HEAD: row-by-row heat banding (some rows print lighter, some darker),
    a few dead heating elements that leave thin white streaks down the whole
    print, and occasional paper-feed slips where a band of rows is stretched or
    shifted sideways.
  PAPER: cool off-white thermal paper with a faint sheen, uneven fading of the
    black (patches go grey-brown), a soft curl shadow at the edges.
  LAYOUT: a fax transmission header line printed across the top and a receipt
    footer (dashed rule, totals, asterisks) across the bottom, both in dot font.
  The dither noise and banding are re-rolled every frame (each frame is a new
    printout); the dead-dot streaks, header and paper stay fixed.
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FRAMES, MASKS, OUT = sys.argv[1:4]
ARGS = sys.argv[4:]
H, W = 1080, 1620
DOT = 3                                   # output pixels per printer dot
h, w = H // DOT, W // DOT                 # 360 x 540 dots
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)

PAPER = np.array([236, 236, 230], np.float32) / 255     # BGR, cool thermal white
INK = np.array([46, 40, 38], np.float32) / 255          # BGR, blue-black burn
FADED = np.array([110, 118, 128], np.float32) / 255     # BGR, faded grey-brown


def frame_list():
    if not ARGS or ARGS == ["all"]:
        return list(range(1, 180))
    return [int(a) for a in ARGS]


def read(n):
    src = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png"))
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
    return src, m


def fbm(seed, hh, ww, octaves=4, base=3):
    rng = np.random.default_rng(seed)
    out = np.zeros((hh, ww), np.float32)
    amp, tot = 1.0, 0.0
    for o in range(octaves):
        c = base * 2 ** o
        nz = rng.random((max(2, hh * c // ww), c)).astype(np.float32)
        out += amp * cv2.resize(nz, (ww, hh), interpolation=cv2.INTER_CUBIC)
        tot += amp
        amp *= 0.5
    return out / tot


# fixed print-head defects: dead elements leave white columns down the print
_rng = np.random.default_rng(81)
DEAD = np.zeros(w, bool)
DEAD[_rng.choice(np.arange(20, w - 20), 3, replace=False)] = True
WEAK = np.clip(1 - 0.18 * np.abs(cv2.GaussianBlur(_rng.normal(0, 1, (1, w)).astype(np.float32), (0, 0), 6)), 0.75, 1).ravel()


def _text_layer():
    """Fax header + receipt footer, rendered as 1-bit dots at printer resolution."""
    img = Image.new("1", (w, h), 0)
    d = ImageDraw.Draw(img)
    d.fontmode = "1"
    f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Andale Mono.ttf", 9)
    fb = ImageFont.truetype("/System/Library/Fonts/Supplemental/Courier New Bold.ttf", 11)
    d.text((6, 2), "OCT-18-2026 08:44   FROM: OFFICE CAM 3   TO: +62 21 555 0112", fill=1, font=f)
    d.text((w - 6, 2), "P.01", fill=1, font=f, anchor="ra")
    for x in range(4, w - 4, 6):
        d.line([(x, h - 26), (x + 3, h - 26)], fill=1)
    d.text((6, h - 22), "12 FRAMES/SEC x 14.9 SEC", fill=1, font=f)
    d.text((w - 6, h - 22), "TOTAL  179", fill=1, font=fb, anchor="ra")
    d.text((w / 2, h - 11), "*** THANK YOU ***", fill=1, font=f, anchor="ma")
    return np.asarray(img, np.float32)


TEXT = _text_layer()
TEXT_ZONE = np.zeros((h, w), np.float32)
TEXT_ZONE[:14] = 1
TEXT_ZONE[h - 29:] = 1

_paper_fade = fbm(7, H, W, 4, 2)
_curl = np.clip(1 - ((xx / W - 0.5) ** 2 * 1.6 + (yy / H - 0.5) ** 2 * 1.0), 0, 1) ** 0.12
_sheen = 1 + 0.03 * np.exp(-((xx - yy * 0.9 - W * 0.35) / (W * 0.18)) ** 2)
PAPER_IMG = PAPER[None, None] * (_curl * _sheen * (1 - 0.02 * (_paper_fade - 0.5)))[..., None]
CLAHE = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(4, 6))


def noisy_diffuse(v, noise, amt=0.55):
    """Floyd-Steinberg on paper-white values with a jittered threshold; returns 1 = black."""
    img = v.astype(np.float64).tolist()
    thr = (0.5 + amt * noise).tolist()
    out = np.zeros((h, w), np.uint8)
    for y in range(h):
        r, t = img[y], thr[y]
        nxt = img[y + 1] if y + 1 < h else None
        o = out[y]
        for x in range(w):
            old = r[x]
            new = 1.0 if old > t[x] else 0.0
            if new == 0.0:
                o[x] = 1
            e = old - new
            if x + 1 < w:
                r[x + 1] += e * 0.4375
            if nxt is not None:
                if x > 0:
                    nxt[x - 1] += e * 0.1875
                nxt[x] += e * 0.3125
                if x + 1 < w:
                    nxt[x + 1] += e * 0.0625
    return out


def render(n):
    src, mask = read(n)
    rng = np.random.default_rng(10_000 + n)
    g = CLAHE.apply(cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)).astype(np.float32) / 255
    # fax-style contrast: crisp, blown highlights, people a little darker than the room
    sharp = np.clip(g + 1.2 * (g - cv2.GaussianBlur(g, (0, 0), 3)), 0, 1)
    m = cv2.GaussianBlur(mask, (0, 0), 3)
    v = sharp * (1 - 0.04 * m) + 0.08 * (1 - m)
    v = np.clip((v - 0.06) / 0.80, 0, 1) ** 0.80
    v = cv2.resize(v, (w, h), interpolation=cv2.INTER_AREA)

    # print-head heat banding: per-row gain, a few overheated (dark) or starved (light) bands
    row = 1 + 0.08 * rng.normal(0, 1, h)
    row = cv2.GaussianBlur(row.reshape(-1, 1).astype(np.float32), (0, 0), 0.8).ravel()
    for _ in range(rng.integers(2, 6)):
        y0, bh = rng.integers(0, h - 6), rng.integers(1, 7)
        row[y0:y0 + bh] *= rng.choice([0.62, 0.75, 1.3, 1.5])
    v = np.clip(v * row[:, None] / WEAK[None, :] ** 0.5, 0, 1)

    # stochastic 1-bit dither: error diffusion with a noisy threshold
    dots = noisy_diffuse(v, rng.random((h, w)) - 0.5).astype(np.float32)   # 1 = burnt (black)
    dots[:, DEAD] = 0

    # paper-feed slip: a band of rows stretched or shifted sideways
    if rng.random() < 0.35:
        y0 = int(rng.integers(20, h - 60))
        bh = int(rng.integers(6, 30))
        if rng.random() < 0.5:
            dots[y0:y0 + bh] = np.roll(dots[y0:y0 + bh], int(rng.integers(-4, 5)), axis=1)
        else:
            src_rows = np.linspace(y0, y0 + bh * 0.5, bh).astype(int)
            dots[y0:y0 + bh] = dots[src_rows]

    dots = dots * (1 - TEXT_ZONE) + TEXT * TEXT_ZONE

    # up to output size: square dots, slightly soft like a heated element
    big = cv2.resize(dots, (W, H), interpolation=cv2.INTER_NEAREST)
    big = cv2.GaussianBlur(big, (0, 0), 0.55)
    # uneven burn / fading: some patches print grey-brown instead of black
    fade = fbm(500 + n // 6, H, W, 3, 2)
    fade = np.clip((fade - 0.35) * 1.6, 0, 1) * 0.55
    ink = INK[None, None] * (1 - fade[..., None]) + FADED[None, None] * fade[..., None]
    a = np.clip(big * 0.97, 0, 1)[..., None]
    out = PAPER_IMG * (1 - a) + ink * a
    out = (np.clip(out, 0, 1) * 255).astype(np.uint8)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), out)
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    with Pool(4) as p:
        for k in p.imap_unordered(render, frame_list()):
            print(k, end=" ", flush=True)
    print()
