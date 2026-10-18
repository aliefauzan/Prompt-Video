"""Rubber-hose 1930s cartoon restyle, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [all | frame numbers...]

Built like an early-1930s black-and-white theatrical cartoon:
  CHARACTERS (inked cels): only four flat paints, black / dark grey / light
    grey / white. Skin is WHITE (rubber-hose faces and hands are white), hair
    and dark clothes are solid INKBLOT BLACK with a few white shine ticks,
    thick black brush outline around every figure, thinner inner lines,
    facial features as black shapes. A gentle travelling "noodle" wave keeps
    limbs rubbery, and the ink boils a little every frame.
  BACKGROUND: a grey watercolour painting on paper: posterised washes, pooled
    pigment at the wash edges, paper grain, low contrast, no outlines. It
    sways on a 6-frame (2 per second) beat, the way 1930s rooms dance.
  FILM: silver B/W print with a hint of warmth, frame flicker, gate weave,
    vertical scratches that live a few frames, dust and hairs, grain, heavy
    rounded academy gate + vignette, iris-in at the start, iris-out at the end.
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
BEAT = 6.0   # frames per bounce (2 bounces a second at 12 fps)


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


PAPER = (fbm(31, h, w, 6, 60) - 0.5).astype(np.float32)
WASH = (fbm(32, h, w, 4, 5) - 0.5).astype(np.float32)


def read(n):
    src = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png"))
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE)
    src = cv2.resize(src, (w, h), interpolation=cv2.INTER_AREA)
    m = cv2.resize(m, (w, h), interpolation=cv2.INTER_AREA).astype(np.float32) / 255
    return src, m


def background(src, n):
    ms = cv2.pyrMeanShiftFiltering(src, 12, 30)
    g = cv2.cvtColor(ms, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
    g = cv2.GaussianBlur(g, (0, 0), 2.0)
    q = np.floor(np.clip(g, 0, 0.999) * 5) / 4                  # five grey washes
    q = cv2.GaussianBlur(q, (0, 0), 1.6)
    # pooled pigment along wash edges (watercolour)
    gx = cv2.Sobel(q, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(q, cv2.CV_32F, 0, 1, ksize=3)
    edge = np.clip(np.sqrt(gx * gx + gy * gy) * 1.2, 0, 1)
    edge = cv2.GaussianBlur(edge, (0, 0), 1.0)
    bg = 0.42 + 0.48 * q                                       # soft background range
    bg = bg - 0.10 * edge + 0.05 * WASH + 0.035 * PAPER
    # beat sway: the room leans left/right and squashes on the beat
    ph = 2 * np.pi * n / BEAT
    up = ((h - yy0) / h) ** 1.4
    mx = xx0 - 5.0 * np.sin(ph) * up
    my = h - (h - yy0) * (1 + 0.018 * np.sin(ph * 2 + 0.5))
    bg = cv2.remap(bg.astype(np.float32), mx.astype(np.float32), my.astype(np.float32), cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    return np.clip(bg, 0, 1)


def characters(src, mask, n):
    rng = np.random.default_rng(1000 + n)
    ms = cv2.pyrMeanShiftFiltering(src, 5, 18)
    lum = cv2.cvtColor(ms, cv2.COLOR_BGR2GRAY).astype(np.float32)
    lum = cv2.GaussianBlur(lum, (0, 0), 1.2)
    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV).astype(np.float32)
    skin = ((hsv[..., 0] < 16) & (hsv[..., 1] > 95) & (hsv[..., 1] < 200) & (hsv[..., 2] > 85)).astype(np.float32)
    skin = cv2.GaussianBlur(skin, (0, 0), 2.5) > 0.5
    # 0 black, 1 dark grey, 2 light grey, 3 white
    lbl = np.full((h, w), 2, np.uint8)
    lbl[lum < 128] = 1
    lbl[lum < 78] = 0
    lbl[lum > 175] = 3
    lbl[skin & (lum > 70)] = 3
    lbl = cv2.medianBlur(lbl, 5)
    big = cv2.medianBlur(lbl, 15)
    for c in range(4):
        num, lb, st, _ = cv2.connectedComponentsWithStats((lbl == c).astype(np.uint8), connectivity=8)
        small = st[:, cv2.CC_STAT_AREA] < 160
        small[0] = False
        sm = small[lb]
        lbl[sm] = big[sm]
    paint = np.array([0.04, 0.36, 0.66, 0.97], np.float32)
    cel = paint[lbl]
    # white shine ticks on the inkblot black (hair, dark shirts)
    raw = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY).astype(np.float32)
    shine = (lbl == 0) & (cv2.GaussianBlur(raw, (0, 0), 1.5) > cv2.GaussianBlur(raw, (0, 0), 8) + 9)
    shine = cv2.morphologyEx(shine.astype(np.uint8), cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
    num, lb, st, _ = cv2.connectedComponentsWithStats(shine, connectivity=8)
    ok = (st[:, cv2.CC_STAT_AREA] > 8) & (st[:, cv2.CC_STAT_AREA] < 220)
    ok[0] = False
    cel[ok[lb]] = 0.95
    # ink: label boundaries + facial features + thick silhouette
    inner = np.zeros((h, w), np.uint8)
    for sy, sx in ((0, 1), (1, 0)):
        a, b = lbl[: h - sy, : w - sx].astype(int), lbl[sy:, sx:].astype(int)
        inner[: h - sy, : w - sx] |= (np.abs(a - b) >= 1).astype(np.uint8)
    inner = cv2.dilate(inner, np.ones((2, 2), np.uint8))
    feat = ((raw < np.minimum(100, 0.64 * cv2.GaussianBlur(raw, (0, 0), 8))) & (cv2.GaussianBlur(skin.astype(np.float32), (0, 0), 6) > 0.3)).astype(np.uint8)
    num, lb, st, _ = cv2.connectedComponentsWithStats(feat, connectivity=8)
    ok = (st[:, cv2.CC_STAT_AREA] > 5) & (st[:, cv2.CC_STAT_AREA] < 600)
    ok[0] = False
    feat = cv2.dilate(ok[lb].astype(np.uint8), np.ones((2, 2), np.uint8))
    m8 = (mask > 0.5).astype(np.uint8)
    inside = cv2.erode(m8, np.ones((5, 5), np.uint8))
    sil = cv2.dilate(m8, np.ones((7, 7), np.uint8)) - cv2.erode(m8, np.ones((2, 2), np.uint8))
    ink = np.maximum(np.maximum(inner * inside, feat), sil).astype(np.float32)
    # line boil
    dx = cv2.resize(rng.normal(0, 1, (h // 30, w // 30)).astype(np.float32), (w, h), interpolation=cv2.INTER_CUBIC) * 1.1
    dy = cv2.resize(rng.normal(0, 1, (h // 30, w // 30)).astype(np.float32), (w, h), interpolation=cv2.INTER_CUBIC) * 1.1
    ink = cv2.remap(ink, xx0 + dx, yy0 + dy, cv2.INTER_LINEAR)
    weight = 0.85 + 0.35 * cv2.resize(rng.random((h // 20, w // 20)).astype(np.float32), (w, h))
    ink = np.clip(cv2.GaussianBlur(ink, (0, 0), 0.6) * 1.7 * weight, 0, 1)
    cover = cv2.dilate(m8, np.ones((7, 7), np.uint8)).astype(np.float32)
    # rubber-hose noodle wave travelling through the figures on the beat
    ph = 2 * np.pi * n / BEAT
    wx = (xx0 + 2.2 * np.sin(yy0 / 55.0 - ph)).astype(np.float32)
    wy = (yy0 + 1.2 * np.sin(xx0 / 70.0 + ph)).astype(np.float32)
    cel = cv2.remap(cel, wx, wy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    ink = cv2.remap(ink, wx, wy, cv2.INTER_LINEAR)
    cover = cv2.remap(cover, wx, wy, cv2.INTER_LINEAR)
    return cel, ink, cover


def iris(n):
    """Iris-in over the first 10 frames, iris-out over the last 9 (it stops
    on a small circle around the face, as the cartoons did before the cut)."""
    diag = np.hypot(W, H) / 2
    if n <= 10:
        return diag * (0.10 + 0.90 * (n / 10) ** 1.5)
    if n >= 171:
        return diag * (0.20 + 0.80 * ((179 - n) / 8) ** 1.3)
    return None


def film(img, n):
    rng = np.random.default_rng(7000 + n)
    big = cv2.resize(img, (W, H), interpolation=cv2.INTER_CUBIC)
    big = cv2.GaussianBlur(big, (0, 0), 0.9)
    # flicker + slightly crushed print contrast
    big = (big - 0.5) * rng.uniform(1.0, 1.1) + 0.5 + rng.uniform(-0.04, 0.04)
    gx, gy = rng.normal(0, 1.3), rng.normal(0, 1.8)
    big = cv2.warpAffine(big, np.float32([[1, 0, gx], [0, 1, gy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    # vertical scratches living 3-5 frames, drifting sideways
    sc = np.zeros((H, W), np.float32)
    for k in range(3):
        ep = (n + k * 3) // 4 + 50 * k
        r2 = np.random.default_rng(ep)
        if r2.random() < 0.7:
            x = int(r2.integers(60, W - 60) + (n % 4) * r2.normal(0, 2))
            y0, y1 = sorted(r2.integers(0, H, 2))
            cv2.line(sc, (x, int(y0)), (x + int(r2.normal(0, 6)), int(y1)), float(r2.choice([1.0, -1.0])), 1, cv2.LINE_AA)
    big = big + 0.35 * sc
    # dust (white and black specks) and hairs, one frame only
    for _ in range(int(rng.integers(6, 16))):
        c = float(rng.choice([0.0, 1.0]))
        cv2.circle(big, (int(rng.integers(0, W)), int(rng.integers(0, H))), int(rng.integers(1, 4)), c, -1, cv2.LINE_AA)
    if rng.random() < 0.45:
        p = [(int(rng.integers(0, W)), int(rng.integers(0, H)))]
        a = rng.uniform(0, 6.28)
        for _ in range(10):
            a += rng.normal(0, 0.45)
            p.append((int(p[-1][0] + 10 * np.cos(a)), int(p[-1][1] + 10 * np.sin(a))))
        cv2.polylines(big, [np.array(p, np.int32)], False, 0.05, 2, cv2.LINE_AA)
    # grain
    g = cv2.resize(rng.normal(0, 1, (H // 2, W // 2)).astype(np.float32), (W, H), interpolation=cv2.INTER_LINEAR)
    big = big + 0.045 * g
    # vignette + rounded academy gate (1.37:1)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - W / 2) / (W * 0.5)) ** 2 + ((yy - H / 2) / (H * 0.55)) ** 2)
    big *= np.clip(1.12 - 0.45 * r ** 2.2, 0.25, 1)
    gate = np.zeros((H, W), np.uint8)
    gw = int(H * 1.37)
    x0 = (W - gw) // 2
    cv2.rectangle(gate, (x0 + 40, 12), (x0 + gw - 40, H - 12), 255, -1)
    for cx in (x0 + 40, x0 + gw - 40):
        for cy in (52, H - 52):
            cv2.circle(gate, (cx, cy), 40, 255, -1, cv2.LINE_AA)
    cv2.rectangle(gate, (x0, 52), (x0 + gw, H - 52), 255, -1)
    gate = cv2.GaussianBlur(gate.astype(np.float32) / 255, (0, 0), 2.5)
    big = big * gate
    rad = iris(n)
    if rad is not None:
        ir = np.zeros((H, W), np.float32)
        # iris-in opens from the middle, iris-out closes on the girl's face
        cx, cy = (W // 2, int(H * 0.45)) if n <= 10 else (int(W * 0.61), int(H * 0.36))
        cv2.circle(ir, (cx, cy), int(rad), 1.0, -1, cv2.LINE_AA)
        big = big * ir
    big = np.clip(big, 0, 1)
    # silver print with a hint of warmth
    tone = np.array([0.93, 0.97, 1.0], np.float32)
    out = big[..., None] * tone
    return (np.clip(out, 0, 1) * 255).astype(np.uint8)


def render(n):
    src, mask = read(n)
    bg = background(src, n)
    cel, ink, cover = characters(src, mask, n)
    m = np.clip(cv2.GaussianBlur(cover, (0, 0), 0.7), 0, 1)
    img = bg * (1 - m) + cel * m
    img = img * (1 - ink)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), film(img.astype(np.float32), n))
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    nums = frame_list()
    with Pool(3) as p:
        for n in p.imap_unordered(render, nums):
            print(n, end=" ", flush=True)
    print()
