"""Pencil-sketch rotoscope ("Take On Me") restyle, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [frame numbers...]
Frames are frame_001.png ... ; masks are person mattes with the same names.
Every frame gets new line wobble, new hatching and new paper so the drawing boils.
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np

FRAMES, MASKS, OUT = sys.argv[1:4]
ONLY = [int(a) for a in sys.argv[4:]]
N = len([f for f in os.listdir(FRAMES) if f.endswith(".png")])

PAPER = np.array([0.86, 0.89, 0.91], np.float32)      # BGR, warm grey sketch paper
GRAPHITE = np.array([0.17, 0.16, 0.16], np.float32)


def vnoise(rng, h, w, cell):
    a = rng.random((max(2, h // cell + 2), max(2, w // cell + 2))).astype(np.float32)
    return cv2.resize(a, (w, h), interpolation=cv2.INTER_CUBIC).clip(0, 1)


def warp(img, rng, amp, cell):
    h, w = img.shape[:2]
    dx = (vnoise(rng, h, w, cell) - 0.5) * 2 * amp
    dy = (vnoise(rng, h, w, cell) - 0.5) * 2 * amp
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    return cv2.remap(img, xx + dx, yy + dy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


def dog_lines(gray, s, k, gain):
    """Difference-of-Gaussians edge strength 0..1 (dark side of edges)."""
    g1 = cv2.GaussianBlur(gray, (0, 0), s)
    g2 = cv2.GaussianBlur(gray, (0, 0), s * k)
    d = g2 - g1
    return np.clip(d * gain - 0.06, 0, 1)


def hatch(rng, h, w, angle, spacing, width, wav):
    """Parallel hand-hatched strokes: wavy, broken into dashes, uneven pressure."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    c, s = np.cos(angle), np.sin(angle)
    u = xx * c + yy * s
    v = -xx * s + yy * c
    u = u + (vnoise(rng, h, w, 90) - 0.5) * wav + rng.uniform(0, spacing)
    d = np.abs(np.mod(u, spacing) - spacing / 2)
    line = np.clip(1 - d / width, 0, 1)
    # break into strokes: noise along the stroke direction, keyed per row
    row = np.floor(u / spacing)
    key = np.sin(row * 12.9898 + rng.uniform(0, 100)) * 43758.5453
    ph = key - np.floor(key)
    strokes = np.sin((v / rng.uniform(55, 85) + ph * 6.28)) > -0.55
    press = 0.55 + 0.45 * vnoise(rng, h, w, 25)
    return line * strokes * press


def paper(rng, h, w):
    tooth = cv2.GaussianBlur(rng.random((h, w)).astype(np.float32), (0, 0), 0.8)
    fibre = vnoise(rng, h, w, 6)
    tone = 0.985 - 0.05 * (1 - vnoise(rng, h, w, 260)) + (tooth - 0.5) * 0.06 + (fibre - 0.5) * 0.02
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    tone *= 1 - 0.14 * np.clip(r - 0.55, 0, 1) ** 1.5           # grubby, handled edges
    return PAPER[None, None, :] * tone[..., None], tooth


def render(n):
    rng = np.random.default_rng(1800 + n)
    bgr = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png"))
    h, w = bgr.shape[:2]
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
    m = cv2.GaussianBlur(m, (0, 0), 3)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 9, 40, 7).astype(np.float32) / 255
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    gl = clahe.apply((gray * 255).astype(np.uint8)).astype(np.float32) / 255

    img, tooth = paper(rng, h, w)

    # --- tone: hand hatching, three layers + graphite smudge -----------------
    tone = 1 - cv2.GaussianBlur(gl, (0, 0), 2.5)
    tone_bg = np.clip((tone - 0.25) * 0.85, 0, 1)                   # backgrounds drawn lighter
    tone_fg = np.clip((tone - 0.22) * 1.45, 0, 1) ** 1.15           # skin stays mostly paper
    t = tone_fg * m + tone_bg * (1 - m)
    t = t + (vnoise(rng, h, w, 40) - 0.5) * 0.12                  # ragged hatch boundaries
    base = rng.uniform(-0.25, 0.25)
    h1 = hatch(rng, h, w, 0.80 + base, 7.5, 1.3, 7) * np.clip((t - 0.30) * 6, 0, 1)
    h2 = hatch(rng, h, w, -0.75 + base, 7.0, 1.2, 7) * np.clip((t - 0.50) * 6, 0, 1)
    h3 = hatch(rng, h, w, 0.10 + base, 5.5, 1.1, 5) * np.clip((t - 0.66) * 6, 0, 1)
    hat = np.clip(h1 + h2 + h3, 0, 1)
    hat *= 0.55 + 0.45 * (m + (1 - m) * 0.55)
    smudge = cv2.GaussianBlur(np.clip((t - 0.55) * 2, 0, 1), (0, 0), 6)
    smudge = warp(smudge, rng, 10, 60) * (0.35 * m + 0.12)
    # scribbled solid shadows in hair / dark clothes
    scrib = hatch(rng, h, w, rng.uniform(-1.4, 1.4), 3.4, 1.4, 14) * np.clip((t - 0.70) * 4, 0, 1) * m

    # --- line work: contour + inner detail, doubled and boiling -------------
    fine = dog_lines(gl, 1.1, 1.8, 9.0)
    broad = dog_lines(gl, 2.4, 1.8, 7.0)
    contour = cv2.morphologyEx((m > 0.5).astype(np.uint8), cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8)).astype(np.float32)
    contour = cv2.GaussianBlur(contour, (0, 0), 0.9) * 1.4
    lines_fg = np.clip(fine * 1.4 + broad * 0.8 + contour * 1.2, 0, 1) * m
    lines_bg = np.clip(broad * 0.75, 0, 1) * (1 - m) * (vnoise(rng, h, w, 120) > 0.28)
    lines = lines_fg + lines_bg
    l1 = warp(lines, rng, 2.4, 45)
    l2 = warp(lines, rng, 3.2, 70) * 0.5                          # second, looser pass of the pencil
    ln = np.clip(np.maximum(l1, l2), 0, 1)

    # construction lines: a few long, faint, overshooting strokes
    cons = np.zeros((h, w), np.float32)
    ys, xs = np.nonzero(m > 0.5)
    for _ in range(int(rng.integers(5, 10))):
        x0, y0 = rng.integers(0, w), rng.integers(0, h)
        if len(xs) and rng.random() < 0.6:                        # start on the body, run off-figure
            i = rng.integers(len(xs))
            x0, y0 = xs[i], ys[i] + h // 5
        a = rng.uniform(0, np.pi)
        L = rng.uniform(150, 520)
        p0 = (int(x0 - L * np.cos(a)), int(y0 - L * np.sin(a)))
        p1 = (int(x0 + L * np.cos(a)), int(y0 + L * np.sin(a)))
        cv2.line(cons, p0, p1, rng.uniform(0.25, 0.5), 2, cv2.LINE_AA)
    for _ in range(int(rng.integers(1, 3))):                      # loose scribbled swirl
        cx, cy = rng.integers(w // 6, 5 * w // 6), rng.integers(h // 6, 5 * h // 6)
        tt = np.linspace(0, 1, 300)
        R = rng.uniform(40, 110)
        px = cx + R * np.cos(tt * 14 * np.pi) + tt * rng.uniform(-200, 200)
        py = cy + R * 0.45 * np.sin(tt * 14 * np.pi) + tt * rng.uniform(-150, 150)
        cv2.polylines(cons, [np.stack([px, py], 1).astype(np.int32)], False, 0.35, 2, cv2.LINE_AA)
    cons = warp(cons, rng, 3, 50)
    cons *= 1 - np.clip(m * (1 - tone_fg) * 1.6, 0, 0.9)          # keep faces clean

    # --- compose: graphite on toothy paper ----------------------------------
    grit = 0.55 + 0.45 * (tooth > 0.42)                           # paper tooth breaks the graphite
    a = np.clip(hat * 0.62 + scrib * 0.7 + ln * 1.0 + cons * 0.5, 0, 1) * grit
    a = np.clip(a + smudge, 0, 0.97)
    img = img * (1 - a[..., None]) + GRAPHITE * a[..., None]
    # eraser highlights on faces/skin: lift a little graphite where the photo is brightest
    hi = np.clip((gl - 0.78) * 4, 0, 1) * m
    img = img + (PAPER - img) * (hi * 0.35)[..., None]

    # scan: slight paper shift / rotation, grain
    M = cv2.getRotationMatrix2D((w / 2, h / 2), rng.normal(0, 0.15), 1.0)
    M[:, 2] += rng.normal(0, 1.5, 2)
    img = cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_REFLECT)
    img += cv2.GaussianBlur(rng.normal(0, 1, (h, w)).astype(np.float32), (0, 0), 0.7)[..., None] * 0.012
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), (img.clip(0, 1) * 255).astype(np.uint8))
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    todo = ONLY or list(range(1, N + 1))
    with Pool(min(6, os.cpu_count() or 2)) as p:
        for n in p.imap_unordered(render, todo):
            print(n, end=" ", flush=True)
    print()
