"""Sin City Noir Red: graphic-novel noir, pure black and white with one spot colour, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <faces.json> <out_dir> [frame numbers... | all]

The room is crushed to ink black; only its brightest light (the window, the
screen) survives as hard white shapes. The people become near two-tone
black/white with hard thresholds (a little grey only in faces) and a white
rim line around each silhouette. Heavy diagonal rain is drawn every frame and
inverts whatever it crosses (white on black, black on white). The only colour
is RED: the woman's lips (Apple Vision landmarks in faces.json) and the red
leaves of the plants. In sections the people flip to INVERTED silhouettes:
solid white figures with black ink lines inside, against black.
"""
import json
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np

FRAMES, MASKS, FACES, OUT = sys.argv[1:5]
ARGS = sys.argv[5:]
if ARGS == ["all"]:
    ONLY = list(range(1, 180))
else:
    ONLY = [int(a) for a in ARGS] or [13, 49, 85, 109, 145, 178]
with open(FACES) as f:
    FACE = json.load(f)

RED = np.array([0.10, 0.04, 0.86], np.float32)          # BGR spot red
INVERT = [(97, 120), (157, 166)]                         # white-silhouette sections


def inverted(n):
    return any(a <= n <= b for a, b in INVERT)


def rain(rng, h, w, n, density=1.0):
    """Long thin diagonal streaks, new every frame."""
    lay = np.zeros((h, w), np.uint8)
    ang = np.deg2rad(rng.uniform(70, 76))                # steep slant, left-leaning
    dx, dy = np.cos(ang), np.sin(ang)
    for _ in range(int(520 * density)):
        x, y = rng.uniform(-200, w), rng.uniform(-200, h)
        ln = rng.uniform(40, 220)
        th = 1 if rng.random() < 0.8 else 2
        cv2.line(lay, (int(x), int(y)), (int(x - dx * ln * 0.35), int(y + dy * ln)), 255, th, cv2.LINE_AA)
    return lay.astype(np.float32) / 255


def woman_lips(n, w):
    faces = FACE.get(f"frame_{n:03d}.png", [])
    if not faces:
        return None
    f = min(faces, key=lambda f: abs(f["box"][0] + f["box"][2] / 2 - w / 2))
    return np.array(f.get("outerLips", []), np.float32)


def ink(gray, lo, hi):
    """Hard two-tone with a narrow grey shoulder."""
    return np.clip((gray - lo) / (hi - lo), 0, 1)


def render(n):
    rng = np.random.default_rng(3100 + n)
    src = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png"))
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), 0).astype(np.float32) / 255
    h, w = m.shape
    img = src.astype(np.float32) / 255
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    g = cv2.bilateralFilter(gray, 9, 40, 7)
    loc = cv2.createCLAHE(3.0, (8, 8)).apply(g).astype(np.float32) / 255
    gf = g.astype(np.float32) / 255
    mb = cv2.GaussianBlur(m, (0, 0), 1.5)
    jit = rng.normal(0, 0.012)

    # background: crushed to black, only the brightest light stays white
    bg = ink(gf, 0.80 + jit, 0.86 + jit)
    # people: hard threshold on local contrast so faces keep their features
    subj = ink(loc, 0.37 + jit, 0.47 + jit)
    subj = np.maximum(subj, ink(gf, 0.62, 0.70))                   # highlights always white
    edges = cv2.Canny(g, 40, 110)
    edges = cv2.dilate(edges, np.ones((2, 2), np.uint8)).astype(np.float32) / 255
    subj = subj * (1 - edges * 0.9)

    if inverted(n):
        # white silhouettes with black ink lines inside, on black
        e2 = cv2.Canny(g, 25, 80)
        e2 = cv2.dilate(e2, np.ones((3, 3), np.uint8)).astype(np.float32) / 255
        dark = 1 - ink(loc, 0.18, 0.24)                             # deepest darks stay ink
        subj = np.clip(1 - e2 - dark * 0.9, 0, 1)
        bg = bg * 0.0

    out = bg * (1 - mb) + subj * mb
    # white rim around every silhouette (graphic-novel back light)
    mu = (m > 0.5).astype(np.uint8)
    rim = cv2.dilate(mu, np.ones((7, 7), np.uint8)) - mu
    rim = cv2.GaussianBlur(rim.astype(np.float32), (0, 0), 0.8)
    out = np.maximum(out, rim * rng.uniform(0.85, 1.0))

    # rain: inverts what it crosses; lighter over faces area (people)
    r = rain(rng, h, w, n, 1.0)
    r = r * (1 - 0.65 * mb)
    out = np.abs(out - r)
    # splash specks
    sp = (rng.random((h, w)) < 0.0006).astype(np.float32)
    out = np.abs(out - cv2.dilate(sp, np.ones((2, 2), np.uint8)))

    out3 = np.repeat(out[..., None], 3, -1)

    # spot colour 1: red leaves of the plants (hue of the source), background only
    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV).astype(np.float32)
    hue, sat, val = hsv[..., 0], hsv[..., 1] / 255, hsv[..., 2] / 255
    redness = ((hue < 9) | (hue > 160)).astype(np.float32) * np.clip((sat - 0.22) * 5, 0, 1) * np.clip((val - 0.30) * 4, 0, 1)
    redness = cv2.GaussianBlur(redness * (1 - m), (0, 0), 1.5)
    redness = np.clip(redness * 1.8, 0, 1)[..., None]
    out3 = out3 * (1 - redness) + RED * redness

    # spot colour 2: the woman's lips, flat saturated red
    lips = woman_lips(n, w)
    if lips is not None and len(lips) >= 3:
        lm = np.zeros((h, w), np.float32)
        cv2.fillPoly(lm, [lips.astype(np.int32)], 1.0, cv2.LINE_AA)
        lm = cv2.GaussianBlur(lm, (0, 0), 1.2)[..., None]
        shade = 0.75 + 0.25 * gf[..., None]
        out3 = out3 * (1 - lm) + RED * shade * lm

    # film grain and a touch of vignette
    out3 = out3 + rng.normal(0, 0.035, (h, w, 1)).astype(np.float32)
    Y, X = np.mgrid[0:h, 0:w].astype(np.float32)
    rr = np.sqrt(((X - w / 2) / (w / 2)) ** 2 + ((Y - h / 2) / (h / 2)) ** 2)
    out3 = out3 * (1 - 0.35 * np.clip(rr - 0.7, 0, 1))[..., None]
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), (np.clip(out3, 0, 1) * 255).astype(np.uint8))
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    with Pool(min(8, os.cpu_count() or 2)) as p:
        for n in p.imap_unordered(render, ONLY):
            print("frame", n, flush=True)
