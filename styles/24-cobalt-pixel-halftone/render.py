"""Cobalt pixel-halftone restyle, frame by frame.

usage: python render.py <frames_dir> <masks_dir> <out_dir> [frame numbers...]
The picture is re-printed as a grid of square cells in ONE cobalt-blue ink on
white card: dark tones are solid deep-blue cells, mid tones cobalt, light tones
pale blue, highlights bare paper. People get the full tonal range; the room
is reduced to a pale ghost. In some sections the card is a sticker on a wall
of black / red / photo tiles (the epicuts "viral halftone" layout). Cell
thresholds, a few stray cells and the paper grain change every frame.
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np

FRAMES, MASKS, OUT = sys.argv[1:4]
ONLY = [int(a) for a in sys.argv[4:]]
N = len([f for f in os.listdir(FRAMES) if f.endswith(".png")])

CELL = 12
PAPER = np.array([0.95, 0.965, 0.97], np.float32)         # BGR, cool white card
INKS = np.array([                                         # BGR, level 1..4
    [0.98, 0.83, 0.70],    # pale blue
    [0.93, 0.55, 0.30],    # light cobalt
    [0.86, 0.30, 0.10],    # cobalt
    [0.55, 0.12, 0.05],    # deep navy-cobalt
], np.float32)
# (first, last, layout, room visible)
SECTIONS = [
    (1, 44, "card", True),
    (45, 96, "wall", True),
    (97, 132, "card", False),
    (133, 999, "wall", False),
]


def vnoise(rng, h, w, cell):
    a = rng.random((max(2, h // cell + 2), max(2, w // cell + 2))).astype(np.float32)
    return cv2.resize(a, (w, h), interpolation=cv2.INTER_CUBIC)


def section_of(n):
    for i, s in enumerate(SECTIONS):
        if s[0] <= n <= s[1]:
            return i, s
    return len(SECTIONS) - 1, SECTIONS[-1]


def halftone_card(n, rng, room):
    bgr = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png"))
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
    h, w = m.shape
    g = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    g = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(g).astype(np.float32) / 255
    gw, gh = w // CELL, h // CELL
    dark = 1 - cv2.resize(g, (gw, gh), interpolation=cv2.INTER_AREA)
    ms = cv2.resize(m, (gw, gh), interpolation=cv2.INTER_AREA)
    # crisp per-cell tone: stretch, then 5 levels with a little per-frame threshold drift
    d = np.clip((dark - 0.22) / 0.62, 0, 1) ** 1.15
    edges = cv2.Canny((g * 255).astype(np.uint8), 60, 140)
    es = cv2.resize(edges.astype(np.float32) / 255, (gw, gh), interpolation=cv2.INTER_AREA)
    d = np.clip(d + es * 0.7, 0, 1)                       # line work survives the coarse grid
    thr = np.array([0.16, 0.36, 0.56, 0.76], np.float32) + rng.normal(0, 0.015, 4).astype(np.float32)
    lev = (d[..., None] > thr).sum(-1)
    person = ms > 0.5
    if room:
        room_lev = np.where(d > 0.55, 1, 0) + np.where(d > 0.88, 1, 0)
        lev = np.where(person, lev, room_lev)
    else:
        lev = np.where(person, lev, 0)
    # silhouette outline: a ring of cobalt cells around every person
    pu = person.astype(np.uint8)
    ring = (cv2.dilate(pu, np.ones((3, 3), np.uint8)) - pu).astype(bool)
    lev = np.where(ring, np.maximum(lev, 3), lev)
    # stray cells flicker (misprinted / dropped cells)
    flip = rng.random(lev.shape)
    lev = np.where((flip < 0.006) & (lev > 0), lev - 1, lev)
    lev = np.where((flip > 0.9975) & person, np.minimum(lev + 1, 4), lev)

    colours = np.concatenate([PAPER[None], INKS], 0)
    cells = colours[lev]                                  # gh,gw,3
    img = cv2.resize(cells, (gw * CELL, gh * CELL), interpolation=cv2.INTER_NEAREST)
    # white gutters between cells, slightly uneven ink density inside each cell
    yy, xx = np.mgrid[0:gh * CELL, 0:gw * CELL]
    gut = ((xx % CELL) < 2) | ((yy % CELL) < 2)
    ink = cv2.resize((lev > 0).astype(np.float32), (gw * CELL, gh * CELL), interpolation=cv2.INTER_NEAREST)
    dens = 0.9 + 0.1 * vnoise(rng, gh * CELL, gw * CELL, 5)
    img = np.where(ink[..., None] > 0, img * dens[..., None] + PAPER * (1 - dens[..., None]), img)
    img[gut] = img[gut] * 0.25 + PAPER * 0.75
    full = np.empty((h, w, 3), np.float32)
    full[:] = PAPER
    full[:gh * CELL, :gw * CELL] = img
    # paper: faint fibre grain + soft light falloff
    full *= (0.985 + vnoise(rng, h, w, 90)[..., None] * 0.02 + rng.normal(0, 0.006, (h, w, 1)))
    return full.astype(np.float32)


def wall(si, h, w):
    """Static collage wall of square tiles: B&W photo crops, red, black, wavy patterns."""
    rng = np.random.default_rng(900 + si)
    img = np.zeros((h, w, 3), np.float32)
    t = 135
    for y in range(0, h, t):
        for x in range(0, w, t):
            k = rng.choice(["photo", "photo", "red", "black", "wave", "photo", "grey"])
            if k == "photo":
                f = cv2.imread(os.path.join(FRAMES, f"frame_{int(rng.integers(1, N + 1)):03d}.png"),
                               cv2.IMREAD_GRAYSCALE)
                s = int(rng.integers(160, 420))
                y0, x0 = int(rng.integers(0, h - s)), int(rng.integers(0, w - s))
                tile = cv2.resize(f[y0:y0 + s, x0:x0 + s], (t, t)).astype(np.float32) / 255
                tile = np.clip((tile - 0.5) * 1.8 + 0.5, 0, 1)
                tile = np.repeat(tile[..., None], 3, 2)
                if rng.random() < 0.3:
                    tile = tile * np.array([0.25, 0.25, 0.95], np.float32) + 0.05
            elif k == "red":
                tile = np.ones((t, t, 3), np.float32) * np.array([0.16, 0.14, 0.86], np.float32)
            elif k == "black":
                tile = np.ones((t, t, 3), np.float32) * 0.06
            elif k == "grey":
                tile = np.ones((t, t, 3), np.float32) * rng.uniform(0.55, 0.8)
            else:
                yy, xx = np.mgrid[0:t, 0:t].astype(np.float32)
                v = np.sin(xx / 7 + np.sin(yy / 11) * 3) > 0
                tile = np.repeat(np.where(v, 0.92, 0.05)[..., None], 3, 2).astype(np.float32)
            img[y:y + t, x:x + t] = tile[:h - y, :w - x]
            img[y:y + t, x:x + 3] = 0.1
            img[y:y + 3, x:x + t] = 0.1
    return img


def render(n):
    si, (_, _, layout, room) = section_of(n)
    rng = np.random.default_rng(4400 + n)
    card = halftone_card(n, rng, room)
    h, w = card.shape[:2]
    if layout == "card":
        out = card
    else:
        out = wall(si, h, w)
        out *= 0.92 + rng.normal(0, 0.01)
        s = 0.8
        ang = -1.6 + rng.normal(0, 0.12)                  # hand-held sticker wobble
        M = cv2.getRotationMatrix2D((w / 2, h / 2), ang, s)
        M[:, 2] += rng.normal(0, 1.5, 2)
        bord = 22
        padded = cv2.copyMakeBorder(card, bord, bord, bord, bord, cv2.BORDER_CONSTANT, value=PAPER.tolist())
        padded = cv2.resize(padded, (w, h))
        alpha = cv2.warpAffine(np.ones((h, w), np.float32), M, (w, h))
        warped = cv2.warpAffine(padded, M, (w, h))
        sh = cv2.GaussianBlur(np.roll(alpha, (14, 10), (0, 1)), (0, 0), 10) * 0.6
        out = out * (1 - sh[..., None])
        out = out * (1 - alpha[..., None]) + warped * alpha[..., None]
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), (out.clip(0, 1) * 255).astype(np.uint8))
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    todo = ONLY or list(range(1, N + 1))
    with Pool(min(8, os.cpu_count() or 4)) as pool:
        for n in pool.imap_unordered(render, todo):
            print(n, end=" ", flush=True)
    print()
