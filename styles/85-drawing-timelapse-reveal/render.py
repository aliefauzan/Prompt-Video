"""Drawing time-lapse reveal, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [all | frame numbers...]

The clip is "drawn" over its own length, like a sped-up Procreate / Clip
Studio time-lapse, while the people keep moving exactly as in the source.
Progress p runs 0 -> 1 from frame 1 to frame 179 and every frame shows the
drawing at that stage:
  0.00-0.04  blank paper
  0.04-0.24  loose BLUE construction sketch, several light overlapping passes
  0.22-0.42  clean dark LINE ART inked over it (head first, then downwards)
  0.40-0.62  FLAT COLOUR fills dropped in one colour region at a time
  0.58-0.82  SHADING brushed in with stroke-shaped reveals
  0.55-0.90  BACKGROUND painted in loose washes (after the figures)
  0.82-1.00  highlights and final polish; the blue sketch fades away
Each pixel has an "order" value inside each stage (stroke-shaped noise, a
top-down bias, or the colour region's turn), so the reveal reads as drawing,
not a fade. A round brush cursor sits on the active edge.
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np

FRAMES, MASKS, OUT = sys.argv[1:4]
ARGS = sys.argv[4:]
H, W = 1080, 1620
h, w = 540, 810
yy0, xx0 = np.mgrid[0:h, 0:w].astype(np.float32)
LW = np.array([0.4, 1.0, 1.0], np.float32)


def frame_list():
    if not ARGS or ARGS == ["all"]:
        return list(range(1, 180))
    return [int(a) for a in ARGS]


def fbm(seed, hh, ww, octaves=4, base=6):
    rng = np.random.default_rng(seed)
    out = np.zeros((hh, ww), np.float32)
    amp, tot = 1.0, 0.0
    for o in range(octaves):
        c = base * 2 ** o
        n = rng.random((max(2, hh * c // ww), c)).astype(np.float32)
        out += amp * cv2.resize(n, (ww, hh), interpolation=cv2.INTER_CUBIC)
        tot += amp
        amp *= 0.5
    return out / tot


def norm01(a):
    a = a - a.min()
    return a / (a.max() + 1e-6)


def streaky(seed, ang_deg, length=41):
    """Noise smeared along one direction: a stroke-shaped order map."""
    n = fbm(seed, h, w, 4, 20)
    k = np.zeros((length, length), np.float32)
    c = length // 2
    a = np.deg2rad(ang_deg)
    cv2.line(k, (int(c - np.cos(a) * c), int(c - np.sin(a) * c)), (int(c + np.cos(a) * c), int(c + np.sin(a) * c)), 1.0, 1)
    return norm01(cv2.filter2D(n, -1, k / k.sum()))


PAPER = (fbm(41, h, w, 6, 80) - 0.5).astype(np.float32)
TOPDOWN = yy0 / h
O_SKETCH = norm01(0.55 * TOPDOWN + 0.45 * streaky(1, 35))
O_INK = norm01(0.75 * TOPDOWN + 0.25 * streaky(2, -20))
O_SHADE = streaky(3, 60, 61)
O_BG = norm01(0.5 * streaky(4, 0, 81) + 0.5 * (1 - xx0 / w))
O_POLISH = streaky(5, -45)


def read(n):
    src = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png"))
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE)
    src = cv2.resize(src, (w, h), interpolation=cv2.INTER_AREA)
    m = cv2.resize(m, (w, h), interpolation=cv2.INTER_AREA).astype(np.float32) / 255
    return src, m


def stage(p, a, b):
    return float(np.clip((p - a) / (b - a), 0, 1))


def reveal(order, t, soft=0.04):
    """Pixels whose order is below t are drawn; a soft edge for the brush."""
    if t <= 0:
        return np.zeros_like(order)
    if t >= 1:
        return np.ones_like(order)
    return np.clip((t * (1 + soft) - order) / soft, 0, 1)


def xdog(gray, sigma, k=1.6, tau=0.99, eps=-0.01, phi=80):
    g1 = cv2.GaussianBlur(gray, (0, 0), sigma)
    g2 = cv2.GaussianBlur(gray, (0, 0), sigma * k)
    d = g1 - tau * g2
    return np.where(d >= eps, 0.0, 1 - np.tanh(phi * (d - eps))).astype(np.float32)  # 1 = line


# ---------------------------------------------------------------- palette
def _people_lab(n):
    src, mask = read(n)
    ms = cv2.pyrMeanShiftFiltering(src, 8, 26)
    lab = cv2.cvtColor(ms, cv2.COLOR_BGR2LAB).reshape(-1, 3).astype(np.float32)
    return lab[mask.reshape(-1) > 0.5]


def build_palette(k=8):
    data = np.concatenate([_people_lab(n)[::7] for n in (13, 49, 109, 160)]) * LW
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 40, 0.5)
    cv2.setRNGSeed(3)
    _, _, cent = cv2.kmeans(data, k, None, crit, 4, cv2.KMEANS_PP_CENTERS)
    raw = (cent / LW).astype(np.float32)
    paint = raw.copy()
    paint[:, 1:] = 128 + (paint[:, 1:] - 128) * 1.5
    paint[:, 0] = np.clip(paint[:, 0] * 1.05 + 14, 0, 255)
    bgr = cv2.cvtColor(np.clip(paint, 0, 255).astype(np.uint8)[None], cv2.COLOR_LAB2BGR)[0]
    # the order the artist fills the colours in: skin first, then dark, then the rest
    turn = np.argsort(np.argsort(-np.abs(raw[:, 1] - 128) - np.abs(raw[:, 2] - 128) + 0.3 * raw[:, 0]))
    return raw, bgr.astype(np.float32) / 255, (turn / max(1, k - 1)).astype(np.float32)


PAL = None


def init(pal):
    global PAL
    PAL = pal


def layers(src, mask, n):
    """Everything the finished drawing is made of, for this pose."""
    raw, pbgr, turn = PAL
    ms = cv2.pyrMeanShiftFiltering(src, 8, 26)
    lab = cv2.GaussianBlur(cv2.cvtColor(ms, cv2.COLOR_BGR2LAB).astype(np.float32), (0, 0), 2.5)
    d = (((lab[:, :, None, :] - raw[None, None]) * LW) ** 2).sum(-1)
    votes = cv2.GaussianBlur(np.exp(-(d - d.min(-1, keepdims=True)) / 120.0), (0, 0), 5.0)
    lbl = cv2.medianBlur(votes.argmax(-1).astype(np.uint8), 11)
    # clean flat regions: a second vote pass removes small islands
    oh = (lbl[..., None] == np.arange(len(raw))[None, None]).astype(np.float32)
    lbl = cv2.medianBlur(cv2.GaussianBlur(oh, (0, 0), 4.0).argmax(-1).astype(np.uint8), 9)
    flat = pbgr[lbl]
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
    # shading: soft painted value from the photo, on top of the flat colour
    L = cv2.GaussianBlur(gray, (0, 0), 3)
    local = cv2.GaussianBlur(gray, (0, 0), 18)
    shade = np.clip(1 + (L - local) * 1.6, 0.6, 1.25)
    shade_q = cv2.GaussianBlur(np.round(shade * 8) / 8, (0, 0), 1.2)
    shaded = flat * shade_q[..., None] * np.array([1.0, 0.97, 0.98], np.float32)
    hi = np.clip((cv2.GaussianBlur(gray, (0, 0), 2) - local - 0.08) * 6, 0, 1) * (gray > 0.55)
    final = np.clip(shaded + hi[..., None] * 0.25, 0, 1)
    # line art (clean) and the looser sketch (two jittered passes)
    m8 = (mask > 0.5).astype(np.uint8)
    ink = xdog(gray, 1.0) * cv2.dilate(m8, np.ones((5, 5), np.uint8))
    sil = (cv2.dilate(m8, np.ones((3, 3), np.uint8)) - m8).astype(np.float32)
    ink = np.clip(np.maximum(ink, sil), 0, 1)
    ink = cv2.morphologyEx(ink, cv2.MORPH_OPEN, np.ones((1, 1), np.uint8))
    sk = xdog(cv2.GaussianBlur(gray, (0, 0), 1.0), 1.25, eps=-0.009)
    sk = np.maximum(sk, cv2.dilate(sil, np.ones((2, 2), np.uint8)))
    sketch = np.zeros((h, w), np.float32)
    for k in range(3):
        r = np.random.default_rng(300 + k * 17 + n // 3)            # sketch lines re-drawn now and then
        dx = cv2.resize(r.normal(0, 1, (h // 60, w // 60)).astype(np.float32), (w, h), interpolation=cv2.INTER_CUBIC) * 3
        dy = cv2.resize(r.normal(0, 1, (h // 60, w // 60)).astype(np.float32), (w, h), interpolation=cv2.INTER_CUBIC) * 3
        sketch = np.maximum(sketch, cv2.remap(sk, xx0 + dx, yy0 + dy, cv2.INTER_LINEAR) * (0.55 + 0.2 * k))
    # background: loose wash painting
    bms = cv2.pyrMeanShiftFiltering(src, 14, 36).astype(np.float32) / 255
    bms = cv2.GaussianBlur(bms, (0, 0), 2.5)
    blab = cv2.cvtColor(bms, cv2.COLOR_BGR2LAB)
    blab[..., 0] = np.round(blab[..., 0] / 100 * 6) / 6 * 100 * 0.7 + blab[..., 0] * 0.3
    blab[..., 1:] *= 1.25
    bgpaint = np.clip(cv2.cvtColor(blab, cv2.COLOR_LAB2BGR), 0, 1)
    bgline = xdog(cv2.GaussianBlur(gray, (0, 0), 1.5), 1.6) * (1 - cv2.dilate(m8, np.ones((7, 7), np.uint8)))
    order_fill = turn[lbl]
    return dict(flat=flat, final=final, ink=ink, sketch=sketch, bgpaint=bgpaint, bgline=bgline,
                order_fill=order_fill, mask=cv2.GaussianBlur(mask, (0, 0), 0.8))


def render(n):
    p = (n - 1) / 178.0
    src, mask = read(n)
    Ly = layers(src, mask, n)
    paper = np.clip(0.955 + 0.03 * PAPER, 0, 1)[..., None] * np.array([0.93, 0.97, 1.0], np.float32)
    img = paper.copy()
    m = Ly["mask"][..., None]
    # background washes + background pencil lines (after the figures)
    tb = stage(p, 0.55, 0.90)
    rb = reveal(O_BG, tb, 0.08)[..., None] * (1 - m)
    img = img * (1 - rb) + Ly["bgpaint"] * rb
    tbl = stage(p, 0.30, 0.55)
    bl = reveal(O_BG, tbl, 0.1) * Ly["bgline"] * (1 - stage(p, 0.8, 1.0) * 0.7)
    img = img * (1 - 0.35 * bl[..., None]) + 0.35 * bl[..., None] * np.array([0.35, 0.3, 0.3], np.float32)
    # flat colour fills, one colour region at a time
    tf = stage(p, 0.40, 0.62)
    rf = reveal(Ly["order_fill"] * 0.85 + 0.15 * O_SHADE, tf, 0.03)[..., None] * m
    img = img * (1 - rf) + Ly["flat"] * rf
    # shading brushed in
    ts = stage(p, 0.58, 0.82)
    rs = reveal(O_SHADE, ts, 0.06)[..., None] * m * (rf > 0.5)
    img = img * (1 - rs) + Ly["final"] * rs
    # blue construction sketch, fading out at the polish stage
    tk = stage(p, 0.04, 0.24)
    sk = reveal(O_SKETCH, tk, 0.05) * Ly["sketch"] * (1 - 0.95 * stage(p, 0.70, 0.92))
    sk = sk * (1 - 0.85 * rf[..., 0]) * (1 - 0.5 * rb[..., 0])
    blue = np.array([0.92, 0.70, 0.45], np.float32)
    img = img * (1 - 0.42 * sk[..., None]) + 0.42 * sk[..., None] * blue
    # clean line art
    ti = stage(p, 0.22, 0.42)
    ri = reveal(O_INK, ti, 0.03) * Ly["ink"]
    inkc = np.array([0.16, 0.12, 0.14], np.float32)
    img = img * (1 - 0.9 * ri[..., None]) + 0.9 * ri[..., None] * inkc
    # final polish: a soft glow + rim highlight brushed over
    tp = stage(p, 0.82, 1.0)
    if tp > 0:
        rp = reveal(O_POLISH, tp, 0.08)[..., None]
        glow = cv2.GaussianBlur(img, (0, 0), 6)
        pol = np.clip(img + 0.18 * np.clip(glow - 0.6, 0, 1) + 0.06, 0, 1)
        pol = np.clip((pol - 0.5) * 1.08 + 0.5, 0, 1)
        img = img * (1 - rp) + pol * rp
    big = cv2.resize(img.astype(np.float32), (W, H), interpolation=cv2.INTER_CUBIC)
    # brush cursor on the active edge of whichever stage is running
    order, t, start = None, None, None
    for o, a, b in ((O_SKETCH, 0.04, 0.24), (O_INK, 0.22, 0.42), (O_SHADE, 0.40, 0.82), (O_BG, 0.82, 0.90)):
        if a <= p < b:
            order, t, start = o, stage(p, a, b), a
    if order is not None:
        band = np.abs(order - t) < 0.02
        if start < 0.8:
            band &= (mask > 0.5)
        ys, xs = np.nonzero(band)
        if len(ys):
            i = np.random.default_rng(n).integers(len(ys))
            cx, cy = int(xs[i] * 2), int(ys[i] * 2)
            cv2.circle(big, (cx, cy), 22, (0.95, 0.95, 0.95), 5, cv2.LINE_AA)
            cv2.circle(big, (cx, cy), 22, (0.12, 0.12, 0.12), 2, cv2.LINE_AA)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), (np.clip(big, 0, 1) * 255).astype(np.uint8))
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    nums = frame_list()
    pal = build_palette()
    with Pool(3, initializer=init, initargs=(pal,)) as p:
        for n in p.imap_unordered(render, nums):
            print(n, end=" ", flush=True)
    print()
