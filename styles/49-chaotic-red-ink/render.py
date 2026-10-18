"""Chaotic red ink restyle, frame by frame.

usage: python render.py <frames_dir> <masks_dir> <out_dir> [frame numbers...]
Indie-comic ink sketch on a SOLID FLAT VIBRANT RED ground. People are white
paper with rough heavy black marker linework drawn in several overlapping,
slightly misaligned passes; hair is black with scratchy white strands; dark
clothes are red with black scribble hatching. The room is only a few dark-red
and black marker lines on the red. Illegible white cursive scrawl fills the
empty background and erratic black scribble knots appear around the figures.
Every line is redrawn every frame (strong boil); the scrawl keeps its place.
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

RED = np.array([0.13, 0.11, 0.86], np.float32)       # BGR flat vibrant red
DRED = np.array([0.06, 0.05, 0.45], np.float32)      # darker red marker for the room
WHITE = np.array([0.95, 0.95, 0.95], np.float32)
INK = np.array([0.04, 0.03, 0.05], np.float32)


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


def marker(layer, edges, rng, passes, wmin, wmax, jit, min_len=20, step=3):
    """Redraw an edge map as rough marker strokes: several jittered, overshooting passes."""
    cs, _ = cv2.findContours(edges.astype(np.uint8), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    for c in cs:
        if len(c) < min_len:
            continue
        p = c[:, 0, :].astype(np.float32)[::step]
        if len(p) < 3:
            continue
        for _ in range(passes):
            if rng.random() < 0.25:
                continue
            a = int(rng.integers(0, max(1, len(p) // 5)))
            b = len(p) - int(rng.integers(0, max(1, len(p) // 5)))
            seg = p[a:b] + rng.normal(0, jit, 2) + rng.normal(0, jit * 0.35, (b - a, 2))
            if len(seg) < 2:
                continue
            cv2.polylines(layer, [seg.astype(np.int32)], False, 255, int(rng.integers(wmin, wmax + 1)), cv2.LINE_AA)


def scribble(layer, rng, cx, cy, r, turns, width, color=255):
    """An erratic tangled scribble knot."""
    t = np.linspace(0, turns * 6.28, turns * 40)
    rr = r * (0.4 + 0.6 * np.abs(np.sin(t * rng.uniform(0.2, 0.6) + rng.random() * 6)))
    x = cx + rr * np.cos(t + rng.normal(0, 0.2, len(t))) + np.cumsum(rng.normal(0, 1.5, len(t)))
    y = cy + rr * 0.7 * np.sin(t * rng.uniform(0.9, 1.4)) + np.cumsum(rng.normal(0, 1.5, len(t)))
    cv2.polylines(layer, [np.stack([x, y], 1).astype(np.int32)], False, color, width, cv2.LINE_AA)


def scrawl_layer(h, w, n):
    """Illegible white cursive: random script words, slanted, then warped so no word can be read.
    The layout is fixed for the clip; the warp is re-drawn every 3 frames (hand re-traced)."""
    srng = np.random.default_rng(49)
    lay = np.zeros((h, w), np.uint8)
    letters = "abcdeghklmnoprstuvwyz"
    for _ in range(30):
        x, y = int(srng.integers(-40, w - 150)), int(srng.integers(50, h - 20))
        sc = float(srng.uniform(0.9, 1.7))
        for _ in range(int(srng.integers(2, 5))):
            word = "".join(srng.choice(list(letters), int(srng.integers(3, 8))))
            cv2.putText(lay, word, (x, y + int(srng.normal(0, 4))), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, sc, 255, 2,
                        cv2.LINE_AA)
            x += int(cv2.getTextSize(word, cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, sc, 2)[0][0] + srng.integers(15, 45))
    M = cv2.getRotationMatrix2D((w / 2, h / 2), 7, 1.0)                 # everything slants uphill
    lay = cv2.warpAffine(lay, M, (w, h))
    wr = np.random.default_rng(4949 + n // 3)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    fx = (vnoise(wr, h, w, 14) - 0.5) * 14
    fy = (vnoise(wr, h, w, 14) - 0.5) * 18
    lay = cv2.remap(lay, xx + fx, yy + fy, cv2.INTER_LINEAR)
    return lay


def hatch(h, w, angle, period, rng):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    wob = (vnoise(rng, h, w, 40) - 0.5) * period * 1.5
    t = xx * np.cos(np.radians(angle)) + yy * np.sin(np.radians(angle)) + wob + rng.random() * period
    return np.abs((t % period) - period / 2) < 1.6


def faces(n):
    return [f for f in FACES.get(f"frame_{n:03d}.png", []) if "faceContour" in f and f["box"][2] >= 40]


def render(n):
    rng = np.random.default_rng(4900 + n)
    bgr = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png"))
    mk = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE)
    h, w = mk.shape
    body = smooth(clean(mk > 127, 9, 9), 2)

    small = cv2.resize(bgr, (w // 3, h // 3), interpolation=cv2.INTER_AREA)
    flat = cv2.pyrMeanShiftFiltering(small, 10, 24)
    flat = cv2.bilateralFilter(cv2.resize(flat, (w, h)), 9, 40, 9)
    L = cv2.cvtColor(flat, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
    g8 = cv2.bilateralFilter(cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY), 9, 30, 7)

    # head zones from the face landmarks
    face = np.zeros((h, w), np.uint8)
    zone = np.zeros((h, w), np.uint8)
    cap = np.zeros((h, w), np.uint8)
    for f in faces(n):
        x, y, bw, bh = f["box"]
        pts = np.array(f["faceContour"], np.float32)
        th = np.linspace(np.pi * 1.15, np.pi * 1.85, 9)                 # rounded hairline arc
        top = np.stack([x + bw * (0.5 + 0.40 * np.cos(th)), y + 0.12 * bh + 0.26 * bh * np.sin(th)], 1).astype(np.float32)
        cv2.fillConvexPoly(face, cv2.convexHull(np.vstack([pts, top]).astype(np.int32)), 1)
        cx = pts[:, 0].mean()
        cv2.ellipse(zone, (int(cx), int(y + 0.3 * bh)), (int(bw * 0.95), int(bh * 1.05)), 0, 0, 360, 1, -1)
        cv2.ellipse(cap, (int(cx), int(y + 0.3 * bh)), (int(bw * 0.9), int(bh * 0.95)), 0, 180, 360, 1, -1)
    face = smooth((face > 0) & body, 3)

    # ---- fills -------------------------------------------------------------
    dk = clean(body & (L < 0.17) & ~face, 5, 9, 400)
    hair = smooth((dk & (zone > 0)) | (body & (cap > 0) & ~face), 2.5)
    cloth = body & ~face & ~hair
    redcloth = smooth(clean(cloth & (L < 0.50), 7, 15, 2500), 2)
    deep = smooth(clean(cloth & (L < 0.22), 7, 15, 2500), 3)

    out = np.ones((h, w, 3), np.float32) * RED
    mt = vnoise(rng, h, w, 7)
    out *= (0.95 + 0.07 * mt)[..., None]                                # marker-flooded red, slightly uneven
    out[body] = WHITE
    out[redcloth] = RED * (0.97 + 0.05 * mt[redcloth])[..., None]

    ink = np.zeros((h, w), np.uint8)
    dred = np.zeros((h, w), np.uint8)
    white = np.zeros((h, w), np.uint8)

    # ---- background: the room as a few marker lines, white cursive scrawl ----
    e_bg = cv2.Canny(cv2.GaussianBlur(g8, (0, 0), 3), 25, 60) > 0
    e_bg &= ~cv2.dilate(body.astype(np.uint8), np.ones((25, 25), np.uint8)).astype(bool)
    marker(dred, e_bg, rng, 2, 2, 4, 2.5, 40, 4)
    marker(ink, e_bg & (vnoise(rng, h, w, 120) > 0.62), rng, 1, 2, 3, 2.0, 60, 4)
    dark_bg = smooth(clean(~body & (L < 0.2), 9, 15, 5000), 4)
    ink[dark_bg & hatch(h, w, 60, 11, rng)] = 255
    ink[dark_bg & hatch(h, w, -30, 15, rng)] = 255

    occupied = cv2.dilate(body.astype(np.uint8), np.ones((31, 31), np.uint8)).astype(bool)
    scr = scrawl_layer(h, w, n)
    white[~occupied] = scr[~occupied]

    # ---- figures: heavy black marker -----------------------------------------
    e_p = cv2.Canny(g8, 30, 70) > 0
    e_p &= body & ~hair
    marker(ink, e_p, rng, 2, 2, 4, 1.6, 25, 2)
    outline = cv2.Canny((body * 255).astype(np.uint8), 50, 150) > 0
    marker(ink, outline, rng, 3, 4, 8, 3.0, 60, 3)
    hb = hair.astype(np.uint8) * 255
    ink = np.maximum(ink, hb)
    ink[deep & hatch(h, w, 50, 9, rng)] = 255
    deepest = smooth(clean(cloth & (L < 0.12), 7, 15, 2500), 3)
    ink[deepest & hatch(h, w, -40, 13, rng)] = 255
    ink[redcloth & ~deep & hatch(h, w, 55, 16, rng) & (vnoise(rng, h, w, 60) > 0.55)] = 255

    # scratchy white strands through the hair
    strands = np.zeros((h, w), np.uint8)
    e_h = cv2.Canny(g8, 15, 40) > 0
    marker(strands, e_h & cv2.erode(hair.astype(np.uint8), np.ones((9, 9), np.uint8)).astype(bool), rng, 1, 1, 2, 1.0, 25, 2)
    for f in faces(n):
        x, y, bw, bh = f["box"]
        s = bw / 180
        for k in ("leftEyebrow", "rightEyebrow", "leftEye", "rightEye"):
            if k in f:
                p = np.array(f[k], np.float32)
                for _ in range(2):
                    q = p[: len(p) // 2 + 1] + rng.normal(0, 1.2, 2)
                    cv2.polylines(ink, [q.astype(np.int32)], False, 255, max(2, int(rng.integers(3, 6) * s)), cv2.LINE_AA)
        for k in ("leftPupil", "rightPupil"):
            if k in f:
                c = np.array(f[k], np.float32)[0]
                cv2.circle(ink, (int(c[0]), int(c[1] + s)), max(3, int(7 * s)), 255, -1, cv2.LINE_AA)
        if "innerLips" in f:
            p = np.array(f["innerLips"], np.float32)
            p = p[: len(p) // 2 + 1]                                    # the mouth line
            cv2.polylines(ink, [np.ascontiguousarray((p + rng.normal(0, 1, 2)).astype(np.int32))], False, 255,
                          max(2, int(3 * s)), cv2.LINE_AA)
        if "nose" in f:
            p = np.array(f["nose"], np.float32)
            low = p[p[:, 1] > np.percentile(p[:, 1], 55)]
            cv2.polylines(ink, [low[np.argsort(low[:, 0])].astype(np.int32)], False, 255, max(2, int(2 * s)), cv2.LINE_AA)
        # nervous scribble marks beside the head
        if rng.random() < 0.8:
            side = rng.choice([-1, 1])
            scribble(ink, rng, x + bw / 2 + side * bw * rng.uniform(0.9, 1.3), y - bh * rng.uniform(0.0, 0.5),
                     bw * rng.uniform(0.12, 0.22), int(rng.integers(3, 6)), 2)

    # erratic scribble knots and stray strokes around the figures
    cs, _ = cv2.findContours(body.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    pts = np.vstack([c[:, 0, :] for c in cs]) if cs else np.zeros((0, 2))
    for _ in range(int(rng.integers(4, 8))):
        if len(pts) == 0:
            break
        px, py = pts[rng.integers(len(pts))]
        if py > h - 40 or px < 30 or px > w - 30:
            continue
        scribble(ink, rng, px + rng.normal(0, 25), py + rng.normal(0, 25), rng.uniform(14, 40), int(rng.integers(3, 7)), 2)
    for _ in range(int(rng.integers(6, 12))):
        x0, y0 = rng.integers(0, w), rng.integers(0, h)
        ang = rng.uniform(0, 6.28)
        L_ = rng.uniform(40, 160)
        cv2.line(ink, (int(x0), int(y0)), (int(x0 + L_ * np.cos(ang)), int(y0 + L_ * np.sin(ang))), 255,
                 int(rng.integers(2, 4)), cv2.LINE_AA)

    # ---- composite ------------------------------------------------------------
    a = cv2.GaussianBlur(dred.astype(np.float32) / 255, (0, 0), 0.6)[..., None]
    out = out * (1 - a * 0.85) + DRED * a * 0.85
    a = cv2.GaussianBlur(white.astype(np.float32) / 255, (0, 0), 0.6)[..., None] * 0.92
    out = out * (1 - a) + WHITE * a
    inka = ink.astype(np.float32) / 255
    inka *= 0.82 + 0.18 * (rng.random((h, w)) > 0.2)                  # dry marker skips
    inka = cv2.GaussianBlur(inka, (0, 0), 0.6)[..., None]
    out = out * (1 - inka) + INK * inka
    sa = cv2.GaussianBlur(strands.astype(np.float32) / 255, (0, 0), 0.5)[..., None] * 0.85
    out = out * (1 - sa) + WHITE * sa
    out = np.clip(out + ((rng.random((h, w)) - 0.5) * 0.03)[..., None], 0, 1)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), (out * 255).astype(np.uint8))
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    todo = ONLY or list(range(1, N + 1))
    with Pool(max(1, os.cpu_count() - 2)) as p:
        for _ in p.imap_unordered(render, todo):
            pass
