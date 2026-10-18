"""Topographic Contour Lines, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [all | frame numbers...]

Per frame:
  * brightness becomes elevation: the frame's luminance is flattened with an
    edge-preserving filter (so batik and stripes don't turn to mush), then the
    people are raised as broad hills from the blurred masks, plus a fixed
    gentle terrain swell in the room
  * isolines are drawn at a fixed contour interval as constant-width,
    anti-aliased lines (distance-to-level / gradient); every 5th one is a
    heavier index contour; where lines crowd closer than a few pixels they
    fade out like on a cliff
  * printed on cream map paper with fibre texture, a faint blue grid, a
    layer tint by elevation (low ground tan, high ground pale), a soft
    hillshade, elevation numbers set along index contours at fixed
    anchor points in the room, a neatline border and a map-sheet legend
  * paper and labels hold still; only the terrain changes with the footage
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FRAMES, MASKS, OUT = sys.argv[1:4]
ARGS = sys.argv[4:]
N = len([f for f in os.listdir(FRAMES) if f.startswith("frame_") and f.endswith(".png")])
W, H = 1620, 1080
STEP = 3.2            # contour interval in "metres"
INDEX = 5             # every 5th contour is an index contour
BASE = 1200           # elevation offset for the labels
PAPER = np.array([0.80, 0.90, 0.95], np.float32)     # cream, BGR
INK = np.array([0.10, 0.24, 0.45], np.float32)       # USGS brown, BGR
GRID = np.array([0.82, 0.70, 0.55], np.float32)      # pale blue grid


def font(size):
    for p in ("/System/Library/Fonts/Supplemental/Arial Narrow.ttf",
              "/System/Library/Fonts/Supplemental/Arial.ttf",
              "/System/Library/Fonts/Helvetica.ttc"):
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            pass
    return ImageFont.load_default()


def paper():
    rng = np.random.default_rng(93)
    fib = cv2.GaussianBlur(rng.normal(0, 1, (H, W)).astype(np.float32), (0, 0), 1.2)
    fib2 = cv2.GaussianBlur(rng.normal(0, 1, (H, W)).astype(np.float32), (0, 0), 30)
    streak = cv2.GaussianBlur(rng.normal(0, 1, (H, W)).astype(np.float32), (0, 0), sigmaX=12, sigmaY=0.8)
    p = PAPER[None, None] * (1 + 0.025 * fib[..., None] + 0.06 * fib2[..., None] / fib2.std()
                             + 0.008 * streak[..., None] / streak.std())
    # faint grid every 135 px
    g = np.zeros((H, W), np.float32)
    for x in range(0, W, 135):
        g[:, x] = 1
    for y in range(0, H, 135):
        g[y, :] = 1
    g = cv2.GaussianBlur(g, (0, 0), 0.6) * 0.9
    p = p * (1 - g[..., None]) + GRID * g[..., None] * 1.0 + p * g[..., None] * 0.0
    return p.astype(np.float32)


def terrain():
    rng = np.random.default_rng(39)
    t = cv2.GaussianBlur(rng.normal(0, 1, (H // 8, W // 8)).astype(np.float32), (0, 0), 6)
    t = cv2.resize(t / t.std(), (W, H), interpolation=cv2.INTER_CUBIC)
    return t


def init():
    global PAPER_IMG, TERR, ANCHORS
    PAPER_IMG = paper()
    TERR = terrain()
    rng = np.random.default_rng(7)
    ANCHORS = [(int(x), int(y)) for x, y in zip(rng.uniform(60, W - 60, 60), rng.uniform(60, H - 120, 60))]


def elevation(img, m):
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    s = cv2.bilateralFilter(g, 13, 0.10, 9)
    s = cv2.bilateralFilter(s, 13, 0.10, 9)
    s = cv2.GaussianBlur(s, (0, 0), 2.2)
    hill = cv2.GaussianBlur(m, (0, 0), 28)
    return 100 * s + 30 * hill + 7 * TERR


def lines(E, step, width):
    f = E / step
    gx = cv2.Sobel(E, cv2.CV_32F, 1, 0, ksize=3) / 8
    gy = cv2.Sobel(E, cv2.CV_32F, 0, 1, ksize=3) / 8
    gm = np.sqrt(gx * gx + gy * gy) + 1e-4
    d = np.abs(f - np.round(f)) * step / gm          # px distance to the nearest level
    ln = np.clip(width / 2 + 0.5 - d, 0, 1)
    spacing = step / gm                               # px between neighbouring lines
    ln *= np.clip((spacing - 3.0) / 3.0, 0, 1)        # cliffs: let crowded lines drop out
    return ln, gx, gy, gm


def render(n):
    rng = np.random.default_rng(9300 + n)
    img = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png")).astype(np.float32) / 255
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
    E = elevation(img, m)
    thin, gx, gy, gm = lines(E, STEP, 1.15)
    idx, _, _, _ = lines(E, STEP * INDEX, 2.1)
    # gentle hillshade from a smoothed surface (sun from the north-west)
    Es = cv2.GaussianBlur(E, (0, 0), 7)
    sx = cv2.Sobel(Es, cv2.CV_32F, 1, 0, ksize=3) / 8
    sy = cv2.Sobel(Es, cv2.CV_32F, 0, 1, ksize=3) / 8
    shade = np.tanh((sx + sy) * 1.2)
    # layer tint: low ground a deeper tan, high ground pale paper
    Et = cv2.GaussianBlur(E, (0, 0), 2.5)
    lo, hi = np.percentile(Et, 3), np.percentile(Et, 98)
    z = np.clip((Et - lo) / (hi - lo), 0, 1)[..., None] ** 0.8
    tint = (1 - z) * np.array([0.66, 0.80, 0.93], np.float32) + z * np.array([1.03, 1.03, 1.02], np.float32)
    out = PAPER_IMG * tint * (1 + 0.06 * shade[..., None])
    ink = np.clip(0.85 * thin + idx, 0, 1)
    # ink sinks into the paper: slight bleed
    ink = np.clip(ink + 0.25 * cv2.GaussianBlur(ink, (0, 0), 1.0), 0, 1)
    out = out * (1 - ink[..., None]) + INK * ink[..., None]
    # labels on index contours at fixed anchors, room only
    pil = Image.fromarray((np.clip(out[..., ::-1], 0, 1) * 255).astype(np.uint8))
    fnt = font(17)
    placed = []
    for (ax, ay) in ANCHORS:
        if len(placed) >= 9:
            break
        if m[max(0, ay - 30):ay + 30, max(0, ax - 50):ax + 50].max() > 0.3:
            continue
        e = E[ay, ax]
        lvl = np.round(e / (STEP * INDEX)) * STEP * INDEX
        g = np.array([gx[ay, ax], gy[ay, ax]])
        gn = np.linalg.norm(g)
        if gn < 0.05 or gn > 1.2:
            continue
        px, py = np.array([ax, ay]) - (e - lvl) * g / gn ** 2
        if not (40 < px < W - 40 and 40 < py < H - 90):
            continue
        if any(abs(px - qx) < 160 and abs(py - qy) < 70 for qx, qy in placed):
            continue
        ang = np.degrees(np.arctan2(g[0], -g[1]))        # along the contour
        ang = (ang + 90) % 180 - 90
        txt = f"{int(BASE + lvl * 4)}"
        tw = int(fnt.getlength(txt)) + 10
        tile = Image.new("RGBA", (tw, 24), (0, 0, 0, 0))
        dd = ImageDraw.Draw(tile)
        c = tuple(int(v * 255) for v in PAPER[::-1])
        dd.rectangle((0, 2, tw, 21), fill=c + (255,))
        dd.text((5, 2), txt, font=fnt, fill=tuple(int(v * 255) for v in INK[::-1]) + (255,))
        tile = tile.rotate(-ang, resample=Image.BICUBIC, expand=True)
        pil.paste(tile, (int(px - tile.width / 2), int(py - tile.height / 2)), tile)
        placed.append((px, py))
    # neatline + legend strip
    d = ImageDraw.Draw(pil)
    inkc = tuple(int(v * 255) for v in INK[::-1])
    d.rectangle((14, 14, W - 15, H - 15), outline=(40, 40, 40), width=3)
    d.rectangle((22, 22, W - 23, H - 23), outline=(40, 40, 40), width=1)
    d.rectangle((W - 470, H - 66, W - 24, H - 24), fill=tuple(int(v * 255) for v in PAPER[::-1]),
                outline=(40, 40, 40), width=1)
    d.text((W - 458, H - 62), "CONTOUR INTERVAL 10 METERS", font=font(16), fill=(40, 40, 40))
    d.text((W - 458, H - 43), f"OFFICE QUADRANGLE  ·  SHEET {n:03d}", font=font(16), fill=inkc)
    out = np.asarray(pil).astype(np.float32)[..., ::-1] / 255
    out = out + rng.normal(0, 0.006, (H, W, 1)).astype(np.float32)
    out = (np.clip(out, 0, 1) * 255 + rng.random(out.shape) - 0.5).clip(0, 255).astype(np.uint8)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), out)
    return n


def main():
    os.makedirs(OUT, exist_ok=True)
    nums = list(range(1, N + 1)) if (not ARGS or ARGS == ["all"]) else [int(a) for a in ARGS]
    with Pool(4, initializer=init) as p:
        for _ in p.imap_unordered(render, nums):
            pass
    print("rendered", len(nums), "->", OUT)


if __name__ == "__main__":
    main()
