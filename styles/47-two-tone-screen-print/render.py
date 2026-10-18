"""2-tone minimalist screen-print restyle, frame by frame.

usage: python render.py <frames_dir> <masks_dir> <out_dir> [frame numbers...]
Two inks only on clean white paper: CERULEAN BLUE for fine line art, hair and a
few solid shadow blocks, and ORANGE for flat garment blocks and lips. No photo
tone and no halftone: skin and light clothes stay white paper, shading is blue
stipple or blue hatching, the room is a sparse blue line drawing with lots of
white negative space. The orange plate sits 1-3 px off register and the lines,
stipple and lithographic grain are redrawn every frame.
faces.json = Apple Vision face boxes + landmarks (faces.swift, from style 10).
"""
import json
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np

FRAMES, MASKS, OUT = sys.argv[1:4]
ONLY = [int(a) for a in sys.argv[4:]]
N = len([f for f in os.listdir(FRAMES) if f.endswith(".png")])
FACES = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "faces.json")))

PAPER = np.array([0.93, 0.955, 0.965], np.float32)   # BGR clean warm white
BLUE = np.array([0.80, 0.42, 0.12], np.float32)      # cerulean / cobalt ink
ORANGE = np.array([0.12, 0.52, 0.97], np.float32)    # vivid orange ink


def vnoise(rng, h, w, cell):
    a = rng.random((max(2, h // cell + 2), max(2, w // cell + 2))).astype(np.float32)
    return cv2.resize(a, (w, h), interpolation=cv2.INTER_CUBIC)


def clean(b, k_open, k_close, min_area=0):
    b = cv2.morphologyEx(b.astype(np.uint8), cv2.MORPH_OPEN, np.ones((k_open, k_open), np.uint8))
    b = cv2.morphologyEx(b, cv2.MORPH_CLOSE, np.ones((k_close, k_close), np.uint8))
    if min_area:
        n, lab, st, _ = cv2.connectedComponentsWithStats(b, 8)
        keep = np.zeros(n, bool)
        keep[1:] = st[1:, cv2.CC_STAT_AREA] > min_area
        return keep[lab]
    return b > 0


def smooth(b, sigma):
    return cv2.GaussianBlur(b.astype(np.float32), (0, 0), sigma) > 0.5


def litho(region, rng, grain=0.10):
    """Flat screen-printed block with crayon-litho grain and a slightly ragged edge."""
    h, w = region.shape
    m = cv2.GaussianBlur(region.astype(np.float32), (0, 0), 1.2)
    m = (m + (vnoise(rng, h, w, 5) - 0.5) * 0.18) > 0.5
    tex = cv2.blur(rng.random((h, w)).astype(np.float32), (3, 1))
    a = m.astype(np.float32) * (1 - grain * (tex > 0.72)) * (0.92 + 0.08 * vnoise(rng, h, w, 50))
    return cv2.GaussianBlur(a, (0, 0), 0.6)


def fine_lines(gray, region, lo, hi, min_len, rng, h, w):
    """Thin pen line art: Canny on the smoothed photo, short bits dropped, wobbled per frame."""
    e = cv2.Canny(gray, lo, hi) > 0
    e &= region
    n, lab, st, _ = cv2.connectedComponentsWithStats(e.astype(np.uint8), 8)
    keep = np.zeros(n, bool)
    keep[1:] = (np.maximum(st[1:, cv2.CC_STAT_WIDTH], st[1:, cv2.CC_STAT_HEIGHT]) > min_len)
    e = keep[lab].astype(np.float32)
    # line boil: a smooth 1-2 px displacement field, new every frame
    fx = (vnoise(rng, h, w, 90) - 0.5) * 3.0
    fy = (vnoise(rng, h, w, 90) - 0.5) * 3.0
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    e = cv2.remap(e, xx + fx, yy + fy, cv2.INTER_LINEAR)
    e = cv2.GaussianBlur(e, (0, 0), 0.7) * 2.2
    e *= 0.7 + 0.3 * (rng.random((h, w)) > 0.25)                       # pen skips on paper tooth
    return np.clip(e, 0, 1)


def pen(layer, pts, width):
    if len(pts) > 1:
        cv2.polylines(layer, [pts.astype(np.int32)], False, 255, width, cv2.LINE_AA)


def face_parts(n, m, bgr, rng, h, w):
    skin = np.zeros((h, w), np.uint8)
    neck = np.zeros((h, w), np.uint8)
    zone = np.zeros((h, w), np.uint8)
    cap = np.zeros((h, w), np.uint8)
    lips = np.zeros((h, w), np.uint8)
    feat = np.zeros((h, w), np.uint8)
    for f in FACES.get(f"frame_{n:03d}.png", []):
        x, y, bw, bh = f["box"]
        if "faceContour" not in f or bw < 40:
            continue
        pts = np.array(f["faceContour"], np.float32)
        th = np.linspace(np.pi * 1.15, np.pi * 1.85, 9)                 # rounded hairline arc
        top = np.stack([x + bw * (0.5 + 0.40 * np.cos(th)), y + 0.12 * bh + 0.26 * bh * np.sin(th)], 1).astype(np.float32)
        cv2.fillConvexPoly(skin, cv2.convexHull(np.vstack([pts, top]).astype(np.int32)), 1)
        cx = pts[:, 0].mean()
        nk = np.array([[cx - 0.3 * bw, y + 0.75 * bh], [cx + 0.3 * bw, y + 0.75 * bh],
                       [cx + 0.34 * bw, y + 1.3 * bh], [cx - 0.34 * bw, y + 1.3 * bh]], np.int32)
        cv2.fillConvexPoly(neck, nk, 1)
        cv2.ellipse(zone, (int(cx), int(y + 0.3 * bh)), (int(bw * 0.95), int(bh * 1.05)), 0, 0, 360, 1, -1)
        cv2.ellipse(cap, (int(cx), int(y + 0.3 * bh)), (int(bw * 0.9), int(bh * 0.95)), 0, 180, 360, 1, -1)
        s = bw / 180
        jit = lambda p: p + rng.normal(0, 0.5, 2)
        for k in ("leftEyebrow", "rightEyebrow"):
            if k in f:
                p = np.array(f[k], np.float32)
                pen(feat, jit(p[: len(p) // 2 + 1]), max(2, int(3 * s)))
        for k in ("leftEye", "rightEye"):
            if k in f:
                p = np.array(f[k], np.float32)
                pen(feat, jit(p[: len(p) // 2 + 1]), max(2, int(3 * s)))
        for k in ("leftPupil", "rightPupil"):
            if k in f:
                c = np.array(f[k], np.float32)[0]
                cv2.circle(feat, (int(c[0]), int(c[1] + s)), max(2, int(5 * s)), 255, -1, cv2.LINE_AA)
        if "nose" in f:
            p = np.array(f["nose"], np.float32)
            low = p[p[:, 1] > np.percentile(p[:, 1], 50)]
            pen(feat, jit(low[np.argsort(low[:, 0])]), max(1, int(2 * s)))
        pen(feat, jit(pts), max(1, int(2 * s)))                       # jaw line
        if "outerLips" in f:
            cv2.fillPoly(lips, [np.array(f["outerLips"], np.int32)], 1)
    ycc = cv2.cvtColor(bgr, cv2.COLOR_BGR2YCrCb)
    loose = (ycc[..., 1] > 140) & (ycc[..., 2] < 122) & (ycc[..., 0] > 60)
    neck = clean((neck > 0) & loose, 5, 11, 300)
    face = smooth(((skin > 0) | neck) & m, 3)
    return face, zone > 0, cap > 0, lips > 0, feat.astype(np.float32) / 255


def color_skin(bgr, m):
    ycc = cv2.cvtColor(bgr, cv2.COLOR_BGR2YCrCb)
    sk = ((ycc[..., 1] > 147) & (ycc[..., 1] < 175) & (ycc[..., 2] > 85) & (ycc[..., 2] < 114)
          & (ycc[..., 0] > 78) & m)
    return clean(sk, 7, 15, 6000)


def hatch(h, w, angle, period, rng):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    t = xx * np.cos(np.radians(angle)) + yy * np.sin(np.radians(angle)) + rng.random() * period
    return (np.abs((t % period) - period / 2) < 1.1).astype(np.float32)


def render(n):
    rng = np.random.default_rng(4700 + n)
    bgr = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png"))
    mk = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE)
    h, w = mk.shape
    body = clean(mk > 127, 9, 9)

    small = cv2.resize(bgr, (w // 3, h // 3), interpolation=cv2.INTER_AREA)
    flat = cv2.pyrMeanShiftFiltering(small, 12, 26)
    flat = cv2.bilateralFilter(cv2.resize(flat, (w, h)), 9, 40, 9)
    L = cv2.cvtColor(flat, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
    hsv = cv2.cvtColor(flat, cv2.COLOR_BGR2HSV).astype(np.float32)
    S = hsv[..., 1] / 255
    g8 = cv2.bilateralFilter(cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY), 9, 30, 7)
    g = g8.astype(np.float32) / 255

    face, zone, cap, lips, feat = face_parts(n, body, bgr, rng, h, w)
    skin = face | color_skin(bgr, body)

    # ---- blue plate --------------------------------------------------------
    dk = clean(body & (L < 0.16) & ~face, 5, 9, 400)
    hair = smooth((dk & zone) | (body & cap & ~face), 2.5)
    hair_tex = 1 - 0.55 * cv2.blur((rng.random((h, w)) > 0.992).astype(np.float32), (2, 21)) * 10
    hair_a = litho(hair, rng, 0.05) * np.clip(hair_tex, 0.25, 1)       # white hair-strand streaks

    dark_bg = smooth(clean(~body & (L < 0.18), 9, 15, 5000), 5)
    leafy = smooth(clean(~body & (hsv[..., 0] > 30) & (hsv[..., 0] < 90) & (S > 0.18), 9, 21, 4000), 6)
    bg_blocks = litho(dark_bg | leafy, rng, 0.12)

    lines_bg = fine_lines(cv2.GaussianBlur(g8, (0, 0), 2.0), ~body, 30, 70, 50, rng, h, w)
    lines_p = fine_lines(g8, body & ~hair & ~cv2.dilate(lips.astype(np.uint8), np.ones((9, 9), np.uint8)).astype(bool),
                         25, 60, 18, rng, h, w)
    outline = cv2.Canny((body * 255).astype(np.uint8), 50, 150) > 0
    outline = cv2.GaussianBlur(cv2.dilate(outline.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(np.float32), (0, 0), 0.8)

    # blue stipple on skin shadows, blue hatching on deep garment shadows
    fl = cv2.GaussianBlur(g, (0, 0), 6)
    ref = np.median(fl[skin]) if skin.any() else 0.5
    shade = np.clip((ref - 0.06 - fl) / 0.25, 0, 1) * skin             # only the shadow side of skin
    stip = (rng.random((h, w)) < shade * 0.22).astype(np.float32)
    stip = cv2.dilate(stip, np.ones((2, 2), np.uint8))
    cloth = smooth(clean(body & ~skin & ~hair, 9, 25), 3)
    cref = np.median(fl[cloth]) if cloth.any() else 0.4
    deep = clean(cloth & (fl < min(0.16, cref - 0.12)), 7, 15, 3000)
    hat = hatch(h, w, 35, 9, rng) * cv2.GaussianBlur(deep.astype(np.float32), (0, 0), 3)

    blue = np.maximum.reduce([hair_a, bg_blocks, lines_bg, lines_p * 0.95, outline, feat, stip * 0.9, hat * 0.9])

    # ---- orange plate ------------------------------------------------------
    garment = cloth & ~(fl > 0.66)                                      # light stripes / white tees stay paper
    garment = smooth(clean(garment, 5, 9, 2500), 2)
    dx, dy = rng.integers(-3, 4), rng.integers(-2, 3)
    orange = litho(garment | lips, rng, 0.14)
    orange = cv2.warpAffine(orange, np.float32([[1, 0, dx], [0, 1, dy]]), (w, h))

    # ---- print -------------------------------------------------------------
    paper = np.ones((h, w, 3), np.float32) * PAPER
    paper *= (0.985 + 0.03 * cv2.blur(np.random.default_rng(47).random((h, w)).astype(np.float32), (5, 5)))[..., None]
    out = paper * (1 - orange[..., None] * (1 - ORANGE))
    out = out * (1 - blue[..., None] * (1 - BLUE))                       # overprint: blue on orange = dark brown
    out = np.clip(out + ((rng.random((h, w)) - 0.5) * 0.025)[..., None], 0, 1)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), (out * 255).astype(np.uint8))
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    todo = ONLY or list(range(1, N + 1))
    with Pool(max(1, os.cpu_count() - 2)) as p:
        for _ in p.imap_unordered(render, todo):
            pass
