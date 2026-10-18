"""Manga ink + screentone restyle, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [all | frame numbers...]

Built like a printed black-and-white manga page:
  INK: G-pen contour lines from an XDoG edge pass, a heavier silhouette line
    around every person (from the masks), and SOLID BLACK fills for hair and
    the deepest shadows, with the hair sheen left as white paper.
  SCREENTONE: the people get 3 flat tone sheets (fine 45-degree dot screens
    of different weights) cut to their shadow shapes; the room behind gets a
    smooth gradation tone and lighter lines so the figures read first.
  FOCUS LINES: thin tapering concentration lines (shuchusen) radiate in from
    the panel edges toward the people, background only, redrawn every 2 frames.
  PAGE: pure white paper, a black panel border inside a white gutter.
  Tones are mechanical and do not boil; contour lines wobble a pixel and the
    focus lines are re-drawn every 2 frames, like re-inked panels.
  No colour at all: every pixel is black ink or white paper (plus anti-aliasing).
"""
import json
import os
import sys
from multiprocessing import Pool
from pathlib import Path

import cv2
import numpy as np

FRAMES, MASKS, OUT = sys.argv[1:4]
ARGS = sys.argv[4:]
H, W = 1080, 1620
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
GUTTER, BORDER = 26, 6
# Apple Vision face boxes + landmarks for every source frame (faces.swift)
FACES = json.loads((Path(__file__).resolve().parent / "faces.json").read_text())


def frame_list():
    if not ARGS or ARGS == ["all"]:
        return list(range(1, 180))
    return [int(a) for a in ARGS]


def read(n):
    src = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png"))
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
    return src, m


def dot_screen(period, angle=45.0, phase=0.0):
    """Value 0..1 of a round-dot screen; a dot of coverage c is s < c."""
    a = np.deg2rad(angle)
    u = (xx * np.cos(a) + yy * np.sin(a)) * 2 * np.pi / period + phase
    v = (-xx * np.sin(a) + yy * np.cos(a)) * 2 * np.pi / period + phase
    s = 0.5 - 0.25 * (np.cos(u) + np.cos(v))       # 0 at dot centre, 1 at the gaps
    return s


SCREEN_FINE = dot_screen(6.0)          # the people's flat tones (61 lpi-ish at this size)
SCREEN_BG = dot_screen(5.0, 45.0, 1.3)  # gradation tone behind


def tone(screen, cover, soft=0.035):
    """Ink (1) where the dot screen is under the coverage, anti-aliased."""
    return np.clip((cover - screen) / soft + 0.5, 0, 1)


CLAHE = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(6, 9))


def xdog(g, sigma, k=1.6, p=0.985, eps=-0.012, phi=60.0):
    a = cv2.GaussianBlur(g, (0, 0), sigma)
    b = cv2.GaussianBlur(g, (0, 0), sigma * k)
    d = a - p * b
    return np.clip(-(d - eps) * phi, 0, 1)


def wobble(img, seed, amp=0.9):
    """Tiny smooth displacement so re-inked lines differ a little each boil step."""
    rng = np.random.default_rng(seed)
    dx = cv2.resize(rng.normal(0, 1, (H // 60, W // 60)).astype(np.float32), (W, H), interpolation=cv2.INTER_CUBIC)
    dy = cv2.resize(rng.normal(0, 1, (H // 60, W // 60)).astype(np.float32), (W, H), interpolation=cv2.INTER_CUBIC)
    return cv2.remap(img, (xx + amp * dx).astype(np.float32), (yy + amp * dy).astype(np.float32),
                     cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)


def focus_lines(mask, seed):
    """Concentration lines: black tapering wedges from the edges toward the people."""
    ys, xs = np.nonzero(mask > 0.5)
    if len(xs):
        cx, cy = float(np.median(xs)), float(np.percentile(ys, 30))
    else:
        cx, cy = W / 2, H / 2
    rng = np.random.default_rng(seed)
    canvas = np.zeros((H, W), np.uint8)
    R = np.hypot(W, H)
    n = 230
    angs = np.sort(rng.uniform(0, 2 * np.pi, n))
    for a in angs:
        # distance from centre to frame edge along this ray
        ca, sa = np.cos(a), np.sin(a)
        tx = (W - cx) / ca if ca > 1e-6 else (-cx / ca if ca < -1e-6 else R)
        ty = (H - cy) / sa if sa > 1e-6 else (-cy / sa if sa < -1e-6 else R)
        edge = min(tx, ty)
        inner = edge * rng.uniform(0.42, 0.78)
        width = rng.uniform(0.0025, 0.009)                     # half-angle of the wedge at the edge
        p_tip = (cx + ca * inner, cy + sa * inner)
        p1 = (cx + np.cos(a - width) * R, cy + np.sin(a - width) * R)
        p2 = (cx + np.cos(a + width) * R, cy + np.sin(a + width) * R)
        pts = np.array([p_tip, p1, p2], np.float32) * 4
        cv2.fillPoly(canvas, [pts.astype(np.int32)], 255, cv2.LINE_AA, shift=2)
    lines = canvas.astype(np.float32) / 255
    # keep them off the people (with a white halo, as an inker would leave)
    halo = cv2.dilate((mask > 0.4).astype(np.uint8), np.ones((31, 31), np.uint8)).astype(np.float32)
    halo = cv2.GaussianBlur(halo, (0, 0), 6)
    return lines * np.clip(1 - halo * 1.4, 0, 1)


def face_mask(n):
    """Skin area of every detected face: jaw contour + forehead up to the box top."""
    fm = np.zeros((H, W), np.uint8)
    for f in FACES.get(f"frame_{n:03d}.png", []):
        x, y, w, h = f["box"]
        pts = [tuple(p) for p in f.get("faceContour", [])]
        pts += [(x + 0.12 * w, y - 0.12 * h), (x + 0.88 * w, y - 0.12 * h)]
        hull = cv2.convexHull(np.array(pts, np.float32)).astype(np.int32)
        cv2.fillPoly(fm, [hull], 255, cv2.LINE_AA)
    return cv2.GaussianBlur(fm.astype(np.float32) / 255, (0, 0), 6)


def render(n):
    src, mask = read(n)
    boil = n // 2
    g8 = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    g8 = CLAHE.apply(g8)
    g = g8.astype(np.float32) / 255
    sm = cv2.bilateralFilter(g, 9, 0.12, 6)
    sm = cv2.bilateralFilter(sm, 9, 0.10, 6)
    m = cv2.GaussianBlur(mask, (0, 0), 1.2)
    mb = (m > 0.5).astype(np.float32)

    # ---- tone decisions (people) on a value map smoothed into shapes
    v = cv2.GaussianBlur(sm, (0, 0), 1.6)
    v8 = (np.clip(v, 0, 1) * 255).astype(np.uint8)
    v = cv2.medianBlur(v8, 7).astype(np.float32) / 255
    # faces are left as clean paper: lift skin values, keep hair / brows / eyes dark
    fm = face_mask(n) * mb
    v = v + 0.42 * fm * np.clip((v - 0.24) / 0.12, 0, 1)
    solid = np.clip((0.20 - v) / 0.03 + 0.5, 0, 1)                           # spot black
    dark = np.clip((0.36 - v) / 0.03 + 0.5, 0, 1) * (1 - solid)              # heavy tone
    mid = np.clip((0.55 - v) / 0.03 + 0.5, 0, 1) * (1 - solid) * (1 - dark)   # light tone
    ink_p = solid + dark * tone(SCREEN_FINE, 0.52) + mid * tone(SCREEN_FINE, 0.22)

    # ---- background: lifted, smooth gradation tone, fewer blacks
    vb = cv2.GaussianBlur(sm, (0, 0), 3.0)
    vb = 0.30 + 0.75 * vb
    cover = np.clip((0.92 - vb) * 1.1, 0, 0.62)
    cover = np.round(cover * 10) / 10                                         # tone sheets come in steps
    cover = cv2.GaussianBlur(cover, (0, 0), 1.0)
    ink_b = tone(SCREEN_BG, cover) * (cover > 0.04)
    ink_b = np.maximum(ink_b, np.clip((0.30 - vb) / 0.03 + 0.5, 0, 1))

    ink = ink_p * mb + ink_b * (1 - mb)

    # ---- G-pen lines
    lines_f = xdog(sm, 1.1)                 # fine detail lines
    lines_c = xdog(sm, 2.4, eps=-0.008)     # bolder form lines
    lp = np.maximum(lines_f, lines_c)
    lb = xdog(cv2.GaussianBlur(sm, (0, 0), 1.5), 2.0, eps=-0.02)
    line = lp * mb + lb * (1 - mb) * 0.85
    line = wobble(line, 500 + boil)
    # silhouette: thick tapered outline around every person
    edge = cv2.morphologyEx((m > 0.5).astype(np.uint8), cv2.MORPH_GRADIENT, np.ones((5, 5), np.uint8)).astype(np.float32)
    edge = wobble(cv2.GaussianBlur(edge, (0, 0), 0.8), 900 + boil, 1.2)
    line = np.maximum(line, np.clip(edge * 1.6, 0, 1))

    ink = np.maximum(ink, line)
    ink = np.maximum(ink, focus_lines(m, 77 + boil) * 0.95)

    # ---- page: white paper, panel border inside a gutter
    page = 1 - np.clip(ink, 0, 1)
    page = page * 0.965 + 0.035 * (page > 0.5)        # ink is a hair off pure black
    page = cv2.GaussianBlur(page, (0, 0), 0.45)
    inner = (xx >= GUTTER + BORDER) & (xx < W - GUTTER - BORDER) & (yy >= GUTTER + BORDER) & (yy < H - GUTTER - BORDER)
    outer = (xx >= GUTTER) & (xx < W - GUTTER) & (yy >= GUTTER) & (yy < H - GUTTER)
    page = np.where(inner, page, np.where(outer, 0.04, 0.985))
    out = (np.clip(page, 0, 1) * 255).astype(np.uint8)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), cv2.cvtColor(out, cv2.COLOR_GRAY2BGR))
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    with Pool(4) as p:
        for n in p.imap_unordered(render, frame_list()):
            print(n, end=" ", flush=True)
    print()
