"""1950s editorial / travel-poster restyle, frame by frame.

usage: python render.py <frames_dir> <masks_dir> <out_dir> [frame numbers...]
Tri-tone screen print on aged cream paper: people keep their photo structure as
black ink brushwork (hair as solid black, features as gestural lines), their
clothes become a flat POPPY RED fill printed slightly off-register, faces stay
bare paper with red lips. The room is flattened into a few red, black and
pale-red-tint blocks with sparse black lines and lots of cream negative space.
Ink pinholes, brush wobble and the red offset change every frame (gentle boil).
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

CREAM = np.array([0.80, 0.89, 0.94], np.float32)    # BGR aged cream paper
RED = np.array([0.16, 0.20, 0.86], np.float32)      # poppy red
INK = np.array([0.10, 0.10, 0.12], np.float32)      # warm black


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


def ink_alpha(region, rng, rough=0.22, pin=0.06, cell=6):
    """Screen-print ink: ragged edge, pinholes and uneven coverage, 0..1."""
    h, w = region.shape
    m = cv2.GaussianBlur(region.astype(np.float32), (0, 0), 1.6)
    m = (m + (vnoise(rng, h, w, cell) - 0.5) * rough) > 0.5
    a = m.astype(np.float32)
    a *= (rng.random((h, w)) > pin).astype(np.float32)                 # pinholes
    a *= 0.86 + 0.14 * vnoise(rng, h, w, 40)                           # uneven squeegee pull
    return cv2.GaussianBlur(a, (0, 0), 0.7)


def brush(layer, pts, rng, wmin, wmax):
    """Gestural thick-thin brush stroke along a polyline, tapered ends."""
    n = len(pts)
    if n < 4:
        return
    ph = rng.random() * 6.28
    f = rng.uniform(0.01, 0.04)
    for i in range(n - 1):
        t = i / (n - 1)
        taper = min(1.0, t * 4, (1 - t) * 4)
        wv = wmin + (wmax - wmin) * (0.5 + 0.5 * np.sin(ph + i * f * 6.28)) * taper
        cv2.line(layer, tuple(pts[i]), tuple(pts[i + 1]), 255, max(1, int(round(wv))), cv2.LINE_AA)


def contour_strokes(region, rng, h, w, wmin, wmax, gap=0.18, min_len=120):
    lay = np.zeros((h, w), np.uint8)
    cs, _ = cv2.findContours(region.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for c in cs:
        if len(c) < min_len:
            continue
        p = c[:, 0, :].astype(np.float32)
        k = 15
        p = np.stack([np.convolve(np.r_[p[-k:, i], p[:, i], p[:k, i]], np.ones(k) / k, "same")[k:-k]
                      for i in range(2)], 1)[::2]
        edge = (p[:, 0] < 6) | (p[:, 0] > w - 7) | (p[:, 1] < 6) | (p[:, 1] > h - 7)
        i = 0
        while i < len(p):
            L = int(rng.integers(30, 110))
            seg = p[i:i + L]
            i += L - int(rng.integers(0, 6))
            if rng.random() < gap or edge[max(0, i - L):i].mean() > 0.2 or len(seg) < 6:
                continue
            seg = seg + rng.normal(0, 1.0, 2)
            brush(lay, seg.astype(np.int32), rng, wmin, wmax)
    return lay.astype(np.float32) / 255


def smooth(b, sigma):
    return cv2.GaussianBlur(b.astype(np.float32), (0, 0), sigma) > 0.5


def features(n, rng, h, w):
    """Elegant ink features from the landmarks: brows, lash lines, pupils, nose hook."""
    lay = np.zeros((h, w), np.uint8)
    for f in FACES.get(f"frame_{n:03d}.png", []):
        bw = f["box"][2]
        if "faceContour" not in f or bw < 40:
            continue
        s = bw / 180
        for k in ("leftEyebrow", "rightEyebrow"):
            if k in f:
                p = np.array(f[k], np.float32)
                p = p[: max(2, len(p) // 2 + 1)] if len(p) > 4 else p      # upper edge of the brow
                brush(lay, (p + rng.normal(0, 0.6, 2)).astype(np.int32), rng, 2 * s, 7 * s)
        for k in ("leftEye", "rightEye"):
            if k in f:
                p = np.array(f[k], np.float32)
                top = p[: len(p) // 2 + 1]
                brush(lay, (top + rng.normal(0, 0.5, 2)).astype(np.int32), rng, 2 * s, 6 * s)
        for k in ("leftPupil", "rightPupil"):
            if k in f:
                c = np.array(f[k], np.float32)[0]
                cv2.circle(lay, (int(c[0]), int(c[1]) + int(1 * s)), max(2, int(6 * s)), 255, -1, cv2.LINE_AA)
        if "nose" in f:
            p = np.array(f["nose"], np.float32)
            low = p[p[:, 1] > np.percentile(p[:, 1], 45)]
            low = low[np.argsort(low[:, 0])]
            brush(lay, (low + rng.normal(0, 0.5, 2)).astype(np.int32), rng, 1.5 * s, 4 * s)
    return lay.astype(np.float32) / 255


def face_masks(n, m, bgr, h, w):
    """Head skin (face hull up to the hairline, plus neck), head zones and lips, from Vision landmarks."""
    skin = np.zeros((h, w), np.uint8)
    neck = np.zeros((h, w), np.uint8)
    zone = np.zeros((h, w), np.uint8)
    cap = np.zeros((h, w), np.uint8)
    lips = np.zeros((h, w), np.uint8)
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
        if "outerLips" in f:
            cv2.fillPoly(lips, [np.array(f["outerLips"], np.int32)], 1)
    ycc = cv2.cvtColor(bgr, cv2.COLOR_BGR2YCrCb)
    loose = (ycc[..., 1] > 140) & (ycc[..., 2] < 122) & (ycc[..., 0] > 60)
    neck = clean((neck > 0) & loose, 5, 11, 300)
    return smooth(((skin > 0) | neck) & m, 3), zone > 0, cap > 0, lips > 0


def color_skin(bgr, m):
    """Strict skin colour for hands/arms (big blobs only)."""
    ycc = cv2.cvtColor(bgr, cv2.COLOR_BGR2YCrCb)
    sk = ((ycc[..., 1] > 147) & (ycc[..., 1] < 175) & (ycc[..., 2] > 85) & (ycc[..., 2] < 114)
          & (ycc[..., 0] > 78) & m)
    return clean(sk, 7, 15, 6000)


def render(n):
    rng = np.random.default_rng(4600 + n)
    bgr = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png"))
    mk = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE)
    h, w = mk.shape
    m = mk > 127
    body = clean(m, 9, 9)

    # flatten the photo into poster shapes
    small = cv2.resize(bgr, (w // 3, h // 3), interpolation=cv2.INTER_AREA)
    flat = cv2.pyrMeanShiftFiltering(small, 12, 26)
    flat = cv2.resize(flat, (w, h), interpolation=cv2.INTER_LINEAR)
    flat = cv2.bilateralFilter(flat, 9, 40, 9)
    L = cv2.cvtColor(flat, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
    hsv = cv2.cvtColor(flat, cv2.COLOR_BGR2HSV).astype(np.float32)
    H, S = hsv[..., 0], hsv[..., 1] / 255
    g = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
    g = cv2.bilateralFilter(g, 7, 0.12, 5)

    face, zone, cap, lips = face_masks(n, body, bgr, h, w)
    skin = face | color_skin(bgr, body)

    # ---- black plate -------------------------------------------------------
    dk = clean(body & (L < 0.15) & ~face, 5, 9, 400)
    hair = smooth((dk & zone) | (body & cap & ~face), 2.5)             # hair = dark head zone + crown
    deep = smooth(clean(body & (L < 0.06) & ~face & ~hair, 9, 21, 12000), 5)
    hair |= deep
    dark_bg = smooth(clean(~body & (L < 0.16), 9, 15, 3000), 5)
    d1 = cv2.GaussianBlur(g, (0, 0), 1.5) - cv2.GaussianBlur(g, (0, 0), 3.0)
    face_lines = (d1 < -0.016) & skin
    d2 = cv2.GaussianBlur(g, (0, 0), 2.6) - cv2.GaussianBlur(g, (0, 0), 6.0)
    cloth_lines = (d2 < -0.045) & body & ~skin
    d3 = cv2.GaussianBlur(g, (0, 0), 3.0) - cv2.GaussianBlur(g, (0, 0), 8.0)
    bg_lines = (d3 < -0.06) & ~body
    lines = clean(face_lines, 1, 1, 30) | clean(cloth_lines, 2, 1, 120) | clean(bg_lines, 2, 1, 200)

    outline = contour_strokes(body, rng, h, w, 2.0, 10.0)
    black = np.maximum(ink_alpha(hair | dark_bg | lines, rng, 0.25, 0.05, 4), outline)
    black = np.maximum(black, features(n, rng, h, w))

    # ---- red plate ---------------------------------------------------------
    cloth = smooth(clean(body & ~skin & ~hair, 9, 25), 3)
    cloth &= ~(body & (L > 0.66))                                       # light stripes stay paper
    warm_bg = smooth(clean(~body & (S > 0.28) & ((H < 22) | (H > 165)) & (L > 0.16) & (L < 0.75), 15, 31, 8000), 7)
    tint = smooth(clean(~body & ~warm_bg & ~dark_bg & (L > 0.16) & (L < 0.50), 21, 31, 12000), 9)

    dx, dy = int(rng.integers(8, 14)), int(rng.integers(4, 9))          # off-register red plate
    Mt = np.float32([[1, 0, dx], [0, 1, dy]])
    red = ink_alpha(cloth | warm_bg | lips, rng, 0.3, 0.04, 9)
    red = np.maximum(red, 0.36 * ink_alpha(tint, rng, 0.3, 0.1, 12))
    red = cv2.warpAffine(red, Mt, (w, h))
    core = cv2.erode(face.astype(np.uint8), np.ones((9, 9), np.uint8)).astype(np.float32)
    red *= 1 - cv2.GaussianBlur(core, (0, 0), 3)                        # no red over the faces
    red = np.maximum(red, ink_alpha(lips, rng, 0.1, 0.0, 3))           # lips print in register

    # ---- paper + print -----------------------------------------------------
    paper = np.ones((h, w, 3), np.float32) * CREAM
    stain = cv2.GaussianBlur(np.random.default_rng(46).random((h // 8, w // 8)).astype(np.float32), (0, 0), 6)
    stain = cv2.resize(stain, (w, h))
    stain = (stain - stain.min()) / (np.ptp(stain) + 1e-6)
    paper *= (0.94 + 0.08 * stain)[..., None]
    fib = cv2.blur(np.random.default_rng(47).random((h, w)).astype(np.float32), (9, 1))
    paper *= (0.97 + 0.05 * fib)[..., None]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    vig = 1 - 0.10 * (((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    paper *= vig[..., None]

    out = paper * (1 - red[..., None] * (1 - RED))
    out = out * (1 - black[..., None] * (1 - INK))
    tooth = (rng.random((h, w)).astype(np.float32) - 0.5) * 0.035
    out = np.clip(out + tooth[..., None], 0, 1)

    # cream poster margin + small signature
    mg = 26
    border = np.ones((h, w), bool)
    border[mg:h - mg, mg:w - mg] = False
    out[border] = paper[border]
    o8 = (out * 255).astype(np.uint8)
    cv2.putText(o8, "Lou '57", (w - 170, h - 48), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1.1,
                (int(RED[0] * 255), int(RED[1] * 255), int(RED[2] * 255)), 2, cv2.LINE_AA)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), o8)
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    todo = ONLY or list(range(1, N + 1))
    with Pool(max(1, os.cpu_count() - 2)) as p:
        for _ in p.imap_unordered(render, todo):
            pass
