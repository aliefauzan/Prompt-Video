"""16-bit pixel-art restyle (SNES-era sprite look), frame by frame.

usage: python -I render.py [frame numbers...]   (default: the 6 sheet frames)
Reads ../../_source/frames + masks, writes ./frames/frame_NNN.png.

Look: the frame rebuilt on a 270x180 pixel grid (6x6 screen pixels per art
pixel), every pixel snapped to one fixed 32-colour palette (Endesga 32) with
4x4 ordered Bayer dithering, people as sprites with a 1-pixel dark outline,
the window turned into a banded dithered pixel sky, a small game HUD.
Frames 97-132 switch to the 4-shade Game Boy palette (optional mode in the prompt).
"""
import os
import sys
from multiprocessing import Pool
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
SRC = HERE.parent.parent / "_source"
FRAMES, MASKS, OUT = SRC / "frames", SRC / "masks", HERE / "frames"
SHEET = [13, 49, 85, 109, 145, 178]
PX = 6                                       # screen pixels per art pixel

ENDESGA32 = """be4a2f d77643 ead4aa e4a672 b86f50 733e39 3e2731 a22633 e43b44 f77622 feae34
fee761 63c74d 3e8948 265c42 193c3e 124e89 0099db 2ce8f5 ffffff c0cbdc 8b9bb4 5a6988 3a4466
262b44 181425 ff0044 68386c b55088 f6757a e8b796 c28569""".split()
GAMEBOY = "0f380f 306230 8bac0f 9bbc0f".split()
BAYER4 = (np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]], np.float32) + 0.5) / 16 - 0.5
GB_FRAMES = range(97, 133)


def pal(hexes):
    rgb = np.array([[int(h[i:i + 2], 16) for i in (0, 2, 4)] for h in hexes], np.float32) / 255
    return rgb[:, ::-1].copy()                           # BGR


def to_lab(bgr):
    return cv2.cvtColor(bgr.astype(np.float32).reshape(-1, 1, 3), cv2.COLOR_BGR2LAB).reshape(-1, 3)


def quantise(img, palette, spread, ox=0, oy=0):
    """Ordered-dither img (h,w,3 float BGR) to the palette; nearest colour in Lab."""
    h, w = img.shape[:2]
    b = np.tile(BAYER4, (h // 4 + 2, w // 4 + 2))[oy:oy + h, ox:ox + w][..., None]
    d = np.clip(img + b * spread, 0, 1)
    lab = to_lab(d)
    plab = to_lab(palette)
    idx = ((lab[:, None, :] - plab[None]) ** 2).sum(-1).argmin(1)
    return palette[idx].reshape(h, w, 3), idx.reshape(h, w)


def read(n):
    img = cv2.imread(str(FRAMES / f"frame_{n:03d}.png")).astype(np.float32) / 255
    m = cv2.imread(str(MASKS / f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
    return img, m


def grade(img, sat, gamma, contrast):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv[..., 1] = np.clip(hsv[..., 1] * sat, 0, 1)
    out = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    out = np.clip((out - 0.5) * contrast + 0.5, 0, 1) ** gamma
    return out


def pixel_sky(h, w, n):
    """Banded game sky (top dark blue -> pale cyan) with blocky clouds, in art pixels."""
    t = np.linspace(0, 1, h, dtype=np.float32)[:, None, None]
    top = np.float32([0.54, 0.29, 0.07])
    bot = np.float32([0.96, 0.91, 0.17])
    out = np.broadcast_to(top * (1 - t) + bot * t, (h, w, 3)).copy()
    rng = np.random.default_rng(3)
    drift = (n // 3) % (w + 60)                          # clouds step 1 px every 3 frames
    for _ in range(6):
        cx, cy = rng.integers(0, w + 60), rng.integers(4, int(h * 0.5))
        cw = int(rng.integers(14, 30))
        x0 = (cx + drift) % (w + 60) - 30
        for j, (dx, dw) in enumerate([(4, cw - 8), (1, cw - 2), (0, cw)]):
            out[cy + j:cy + j + 1, max(0, x0 + dx):max(0, x0 + dx + dw)] = (1, 1, 1)
        out[cy + 3:cy + 4, max(0, x0 + 1):max(0, x0 + cw - 1)] = (0.86, 0.80, 0.75)
    return out


def hud(art, n, palette_mode):
    """Tiny game HUD drawn in hard 1-bit pixels on the art grid."""
    h, w = art.shape[:2]
    im = Image.fromarray((art[..., ::-1] * 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    d.fontmode = "1"
    try:
        f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Andale Mono.ttf", 9)
    except OSError:
        f = ImageFont.load_default()
    light = (255, 255, 255) if palette_mode == "snes" else (155, 188, 15)
    dark = (24, 20, 37) if palette_mode == "snes" else (15, 56, 15)
    red = (228, 59, 68) if palette_mode == "snes" else (48, 98, 48)
    score = f"SCORE {1200 + n * 50:06d}"
    for ox, oy in ((1, 1), (0, 0)):
        col = dark if (ox, oy) == (1, 1) else light
        d.text((6 + ox, 4 + oy), "1P", font=f, fill=col)
        d.text((w - 6 - d.textlength(score, font=f) + ox, 4 + oy), score, font=f, fill=col)
    heart = ["01100110", "11111111", "11111111", "01111110", "00111100", "00011000"]
    for k in range(3):
        for yy, row in enumerate(heart):
            for xx, c in enumerate(row):
                if c == "1":
                    d.point((22 + k * 10 + xx, 5 + yy), fill=red if k < 2 or n % 24 < 12 else dark)
    return np.asarray(im)[..., ::-1].astype(np.float32) / 255


def render(n):
    img, m = read(n)
    H, W = m.shape
    h, w = H // PX, W // PX
    mode = "gb" if n in GB_FRAMES else "snes"
    palette = pal(GAMEBOY if mode == "gb" else ENDESGA32)

    small = cv2.resize(img, (w, h), interpolation=cv2.INTER_AREA)
    ms = cv2.resize(m, (w, h), interpolation=cv2.INTER_AREA) > 0.5
    ms = cv2.morphologyEx(ms.astype(np.uint8), cv2.MORPH_OPEN, np.ones((2, 2), np.uint8)) > 0

    # window -> pixel sky (bright, low-saturation, upper part, not a person)
    hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)
    yy = np.linspace(0, 1, h)[:, None]
    win = (hsv[..., 2] > 0.80) & (hsv[..., 1] < 0.16) & (yy < 0.62) & ~ms
    win = cv2.morphologyEx(win.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8)) > 0
    win &= ~ms

    if mode == "gb":
        g = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        g = cv2.createCLAHE(2.0, (4, 4)).apply((g * 255).astype(np.uint8)).astype(np.float32) / 255
        src = np.repeat(g[..., None], 3, -1)
        src = np.where(ms[..., None], src ** 1.35, src ** 1.5 * 0.9)
        ramp = palette[::-1] if palette[0].mean() > palette[-1].mean() else palette
        # map luminance to the 4 greens with ordered dither
        b = np.tile(BAYER4, (h // 4 + 2, w // 4 + 2))[:h, :w]
        lv = np.clip(np.floor(src[..., 0] * 3.999 + b * 1.0 + 0.5), 0, 3).astype(int)
        art = ramp[lv]
    else:
        bg = grade(small, 1.15, 1.05, 1.05)
        bg[win] = pixel_sky(h, w, n)[win]
        fg = grade(cv2.bilateralFilter(small, 5, 0.08, 3), 1.2, 1.0, 1.15)
        src = np.where(ms[..., None], fg, bg)
        art, _ = quantise(src, palette, 0.16)
        # sky stays clean bands (no dither noise in large flat areas)
        sky_q, _ = quantise(pixel_sky(h, w, n), palette, 0.10)
        art[win] = sky_q[win]

    # 1-pixel sprite outline around the people (darkest palette colour)
    dark = palette[np.argmin(palette.sum(1))]
    mu = ms.astype(np.uint8)
    edge = (cv2.dilate(mu, np.ones((3, 3), np.uint8)) - mu) > 0
    art[edge] = dark
    # inner selective outline: darken art pixels on the inside contour (sel-out)
    inner = (mu - cv2.erode(mu, np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], np.uint8))) > 0
    shade = palette[((to_lab(art[inner] * 0.7)[:, None, :] - to_lab(palette)[None]) ** 2).sum(-1).argmin(1)]
    art[inner] = shade

    art = hud(art, n, mode)
    out = cv2.resize(art, (W - W % PX, H - H % PX), interpolation=cv2.INTER_NEAREST)
    out = cv2.copyMakeBorder(out, 0, H - out.shape[0], 0, W - out.shape[1], cv2.BORDER_REPLICATE)
    # faint LCD/pixel grid so the art pixels read as pixels at full size
    grid = np.ones((H, W), np.float32)
    grid[::PX, :] = 0.88
    grid[:, ::PX] = 0.88
    out = out * grid[..., None]
    cv2.imwrite(str(OUT / f"frame_{n:03d}.png"), (np.clip(out, 0, 1) * 255).astype(np.uint8))
    return n


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    todo = [int(a) for a in sys.argv[1:]] or SHEET
    with Pool(min(6, os.cpu_count() or 4)) as pool:
        for r in pool.imap_unordered(render, todo):
            print(r, end=" ", flush=True)
    print()
