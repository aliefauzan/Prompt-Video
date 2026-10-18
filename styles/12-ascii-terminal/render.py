"""ASCII / terminal phosphor restyle, frame by frame.

usage: python -I render.py [frame numbers...]   (default: the 6 sheet frames)
Reads ../../_source/frames + masks, writes ./frames/frame_NNN.png.

Look: the frame rebuilt from monospace characters on a 12x20 px cell grid,
character density = luminance (people brighter than the room), edge cells use
direction glyphs (- / | \\), green P1 phosphor on near-black glass, bloom,
scanlines, slight CRT barrel + vignette, per-frame glyph flicker, a prompt line
and status bar. Frames 97-132 switch to amber phosphor (optional mode).
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
CW, CH = 12, 20                                   # character cell in screen pixels
FONT = "/System/Library/Fonts/Menlo.ttc"
CHARS = " .'`,:;-~_\"^!i|lI1+=r*/\\)(?7tfjxcvzunoJCLYT{}[]sz35a2eSkhdbqpGwmZO0Q8&%#B@M$W"
GREEN = np.float32([0.40, 1.00, 0.30])            # BGR
AMBER = np.float32([0.10, 0.72, 1.00])
AMBER_FRAMES = range(97, 133)


def build_atlas():
    f = ImageFont.truetype(FONT, 17)
    glyphs = []
    for c in CHARS:
        im = Image.new("L", (CW, CH), 0)
        d = ImageDraw.Draw(im)
        d.text((CW / 2, CH / 2), c, font=f, fill=255, anchor="mm")
        glyphs.append(np.asarray(im, np.float32) / 255)
    glyphs = np.stack(glyphs)
    cover = glyphs.mean((1, 2))
    order = np.argsort(cover, kind="stable")
    return glyphs, order, cover


GLYPHS, ORDER, COVER = build_atlas()
IDX = {c: i for i, c in enumerate(CHARS)}
RAMP = ORDER[np.unique(np.round(COVER[ORDER] / COVER.max() * 40), return_index=True)[1]]  # ~monotone ramp


def read(n):
    img = cv2.imread(str(FRAMES / f"frame_{n:03d}.png"))
    m = cv2.imread(str(MASKS / f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
    return img, m


def text_line(canvas_h, canvas_w, txt, y):
    im = Image.new("L", (canvas_w, CH), 0)
    ImageDraw.Draw(im).text((CW, CH / 2), txt, font=ImageFont.truetype(FONT, 16), fill=255, anchor="lm")
    out = np.zeros((canvas_h, canvas_w), np.float32)
    out[y:y + CH] = np.asarray(im, np.float32) / 255
    return out


def barrel(img, k):
    h, w = img.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    nx, ny = (xx - w / 2) / (w / 2), (yy - h / 2) / (h / 2)
    r2 = nx * nx + ny * ny
    f = 1 + k * r2
    return cv2.remap(img, nx * f * w / 2 + w / 2, ny * f * h / 2 + h / 2, cv2.INTER_LINEAR,
                     borderMode=cv2.BORDER_CONSTANT, borderValue=0)


def render(n):
    rng = np.random.default_rng(500 + n)
    img, m = read(n)
    H, W = m.shape
    cols, rows = W // CW, H // CH
    phos = AMBER if n in AMBER_FRAMES else GREEN

    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    g = cv2.createCLAHE(2.0, (8, 8)).apply(g).astype(np.float32) / 255
    lum = cv2.resize(g, (cols, rows), interpolation=cv2.INTER_AREA)
    ms = cv2.resize(m, (cols, rows), interpolation=cv2.INTER_AREA)
    # people bright and dense, room dim and sparse
    inside = ms > 0.5
    if inside.any():
        lo, hi = np.percentile(lum[inside], [3, 97])
        pl = np.clip((lum - lo) / max(hi - lo, 1e-3), 0, 1)
    else:
        pl = lum
    pl = np.clip(pl + (pl - cv2.GaussianBlur(pl, (0, 0), 2.0)) * 1.4, 0, 1)   # local contrast: eyes, mouth, folds
    lum = np.where(inside, 0.10 + 0.90 * pl, (lum * 0.52) ** 2.0)

    k = len(RAMP)
    jitter = np.random.default_rng(500).uniform(-0.35, 0.35, lum.shape)   # fixed per cell: still areas hold still
    idx = RAMP[np.clip((lum * (k - 1) + jitter).round().astype(int), 0, k - 1)]

    # direction glyphs on strong edges (silhouettes + big image edges)
    gs = cv2.resize(cv2.GaussianBlur(g, (0, 0), 3), (cols, rows), interpolation=cv2.INTER_AREA)
    gx = cv2.Sobel(gs + ms * 0.8, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(gs + ms * 0.8, cv2.CV_32F, 0, 1, ksize=3)
    mag = np.hypot(gx, gy)
    ang = (np.degrees(np.arctan2(gy, gx)) + 180) % 180          # gradient direction
    edge_ch = np.array([IDX["|"], IDX["\\"], IDX["-"], IDX["/"], IDX["|"]])
    e = edge_ch[np.round(ang / 45).astype(int)]
    gx2 = cv2.Sobel(ms, cv2.CV_32F, 1, 0, ksize=3)
    gy2 = cv2.Sobel(ms, cv2.CV_32F, 0, 1, ksize=3)
    edge = (np.hypot(gx2, gy2) > 1.2) | ((mag > 1.4) & (ms > 0.5))
    idx = np.where(edge, e, idx)

    # flicker: a few random glyph swaps every frame (the "boil")
    flick = rng.random(idx.shape) < 0.025
    idx = np.where(flick & (lum > 0.08), rng.integers(1, len(CHARS), idx.shape), idx)

    bright = np.clip(0.45 + 0.9 * lum, 0, 1.3) * np.where(edge, 1.15, 1.0)
    bright *= np.where(ms > 0.5, 1.25, 0.7)
    tiles = GLYPHS[idx] * bright[..., None, None]                  # rows, cols, CH, CW
    scr = tiles.transpose(0, 2, 1, 3).reshape(rows * CH, cols * CW)
    canvas = np.zeros((H, W), np.float32)
    oy, ox = (H - rows * CH) // 2, (W - cols * CW) // 2
    canvas[oy:oy + rows * CH, ox:ox + cols * CW] = scr

    # prompt line + status bar (terminal chrome)
    canvas[:CH + 6] *= 0
    canvas = np.maximum(canvas, text_line(H, W, f"user@crt:~$ ./ascii --live --fps 12 clip.mov   [frame {n:03d}]"
                                          + ("_" if n % 2 else " "), 4))
    canvas[H - CH - 6:] *= 0
    canvas = np.maximum(canvas, text_line(H, W, f"-- {cols}x{rows} -- luma ramp {k} -- "
                                          f"{'P3 AMBER' if n in AMBER_FRAMES else 'P1 GREEN'} -- 00:{(n - 1) / 12:05.2f}",
                                          H - CH - 4) * 0.8)

    # phosphor colour, bloom, scanlines, roll band, flicker, glass
    out = canvas[..., None] * phos * 1.25
    out = out + cv2.GaussianBlur(out, (0, 0), 2.5) * 0.35 + cv2.GaussianBlur(out, (0, 0), 14) * 0.30
    yy = np.arange(H, dtype=np.float32)[:, None, None]
    out *= 0.78 + 0.22 * (np.sin(yy * np.pi / 2) ** 2)                # 4 px scanline period
    band = (yy / H - (n * 0.037) % 1.2 + 0.1)
    out *= 1 + 0.10 * np.exp(-(band / 0.05) ** 2)                     # slow rolling bright band
    out *= rng.uniform(0.92, 1.0)
    out += np.float32([0.020, 0.040, 0.018]) if n not in AMBER_FRAMES else np.float32([0.012, 0.025, 0.04])
    out += rng.normal(0, 0.012, out.shape).astype(np.float32)
    out = barrel(np.clip(out, 0, 1.2), 0.045)
    vy, vx = np.ogrid[-1:1:H * 1j, -1:1:W * 1j]
    out *= np.clip(1.15 - 0.55 * (vx ** 2 + vy ** 2), 0, 1)[..., None]
    cv2.imwrite(str(OUT / f"frame_{n:03d}.png"), (np.clip(out, 0, 1) * 255).astype(np.uint8))
    return n


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    todo = [int(a) for a in sys.argv[1:]] or SHEET
    with Pool(min(6, os.cpu_count() or 4)) as pool:
        for r in pool.imap_unordered(render, todo):
            print(r, end=" ", flush=True)
    print()
