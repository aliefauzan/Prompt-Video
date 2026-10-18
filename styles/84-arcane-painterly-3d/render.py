"""Arcane-style painterly 3D restyle, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [all | frame numbers...]

Built like the painted-over 3D look of Arcane (Fortiche) and its imitators:
  PEOPLE: painted planes instead of photo shading (value bands with soft
    painted edges), visible BRUSHSTROKE albedo (cross-brushed dabs at two fixed
    angles), dark gritty ink accents along contours, painted accents on the
    eyes, brows and lips, sparse hatching in the deepest shadows, and two hard coloured RIM LIGHTS:
    teal-cyan from the left, hot magenta-pink from the right, read from the
    matte's edge normal. Animated on twos: the paint texture changes every
    second frame, like the show's stepped animation.
  BACKGROUND: a moody painted set: posterised value planes, teal-blue shadows,
    long cross-hatched brush texture, slight depth blur, warm amber glow from the window and practicals,
    floating dust motes in the light.
  FINISH: bloom on the hot rims and glows, mild grain, vignette.
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


def frame_list():
    if not ARGS or ARGS == ["all"]:
        return list(range(1, 180))
    return [int(a) for a in ARGS]


def read(n):
    src = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png"))
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE)
    src = cv2.resize(src, (w, h), interpolation=cv2.INTER_AREA)
    m = cv2.resize(m, (w, h), interpolation=cv2.INTER_AREA).astype(np.float32) / 255
    return src, m


def stroke_kernels(length=19, nb=8):
    ks = []
    for i in range(nb):
        a = np.pi * i / nb
        k = np.zeros((length, length), np.float32)
        c = length // 2
        dx, dy = np.cos(a) * c, np.sin(a) * c
        cv2.line(k, (int(round(c - dx)), int(round(c - dy))), (int(round(c + dx)), int(round(c + dy))), 1.0, 1, cv2.LINE_AA)
        ks.append(k / k.sum())
    return ks


KS = stroke_kernels()


KS_LONG = stroke_kernels(length=31)


def dab_texture(seed, coarse=2, ks=KS):
    """Painted dabs at two fixed angles (cross-brushed), for skin, cloth and the
    set: a surface texture, not a swirl that follows the contours."""
    rng = np.random.default_rng(seed)
    out = np.zeros((h, w), np.float32)
    for kk, wgt in ((ks[1], 0.6), (ks[6], 0.4)):
        n0 = rng.normal(0, 1, (h // coarse, w // coarse)).astype(np.float32)
        n0 = cv2.GaussianBlur(cv2.resize(n0, (w, h), interpolation=cv2.INTER_NEAREST), (0, 0), 1.3)
        out += wgt * cv2.filter2D(n0, -1, kk)
    return out / (out.std() + 1e-6)


def xdog(gray, sigma, k=1.6, tau=0.98, eps=-0.02, phi=50):
    g1 = cv2.GaussianBlur(gray, (0, 0), sigma)
    g2 = cv2.GaussianBlur(gray, (0, 0), sigma * k)
    d = g1 - tau * g2
    return np.where(d >= eps, 0.0, 1 - np.tanh(phi * (d - eps))).astype(np.float32)


def painted_planes(img, mask):
    """Replace photo shading by a few painted value planes with soft edges."""
    ms = cv2.pyrMeanShiftFiltering(img, 10, 30)
    ms = cv2.bilateralFilter(ms, 9, 40, 7)
    lab = cv2.cvtColor(ms, cv2.COLOR_BGR2LAB).astype(np.float32)
    L = cv2.GaussianBlur(lab[..., 0], (0, 0), 3.0)
    q = np.round(L / 255 * 5) / 5 * 255                          # 6 value planes
    q = cv2.GaussianBlur(q, (0, 0), 3.0)
    lab[..., 0] = 0.55 * q + 0.45 * L
    # richer, slightly stylised colour
    lab[..., 1:] = 128 + (lab[..., 1:] - 128) * 1.35
    return cv2.cvtColor(np.clip(lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR).astype(np.float32) / 255


def rim_light(mask):
    m8 = (mask > 0.5).astype(np.uint8)
    dist = cv2.distanceTransform(m8, cv2.DIST_L2, 5)
    sm = cv2.GaussianBlur(mask, (0, 0), 6)
    nx = -cv2.Sobel(sm, cv2.CV_32F, 1, 0, ksize=5)
    ny = -cv2.Sobel(sm, cv2.CV_32F, 0, 1, ksize=5)
    nn = np.sqrt(nx * nx + ny * ny) + 1e-6
    nx, ny = nx / nn, ny / nn
    # spread the edge normal inward so the rim has a few px of body
    nx = cv2.GaussianBlur(nx, (0, 0), 3)
    ny = cv2.GaussianBlur(ny, (0, 0), 3)
    band = np.exp(-dist / 6.5) * (m8 > 0)
    left = np.clip(-nx * 0.9 - ny * 0.3, 0, 1) ** 1.5 * band          # light from the left
    right = np.clip(nx * 0.9 - ny * 0.2, 0, 1) ** 1.5 * band          # light from the right
    teal = np.array([0.95, 0.85, 0.15], np.float32)                 # BGR
    pink = np.array([0.75, 0.25, 1.0], np.float32)
    return left[..., None] * teal + right[..., None] * pink, np.maximum(left, right)


def people(src, mask, n):
    tex_seed = 100 + n // 2                                         # on twos
    rng = np.random.default_rng(tex_seed)
    base = painted_planes(src, mask)
    # crisp painted forms: people stay sharp against the soft set
    base = np.clip(base + 0.7 * (base - cv2.GaussianBlur(base, (0, 0), 1.6)), 0, 1)
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
    tex = dab_texture(tex_seed)
    lum = cv2.cvtColor(base, cv2.COLOR_BGR2GRAY)
    # brush albedo: strokes modulate value, stronger in mid-tones
    mid = 1 - np.abs(lum - 0.5) * 1.4
    col = base * (1 + 0.05 * tex * np.clip(mid, 0.3, 1))[..., None]
    # dramatic grade: deep teal shadows, warm mid-tones
    sh = np.clip(1 - lum / 0.45, 0, 1)[..., None]
    col = col * (1 - 0.45 * sh) + sh * 0.45 * col * np.array([1.25, 0.95, 0.6], np.float32)
    col = col * np.array([0.92, 0.98, 1.06], np.float32)
    # painted dark accents on local dark features (eyes, brows, lips, nostrils)
    acc = np.clip((cv2.GaussianBlur(gray, (0, 0), 5) - cv2.GaussianBlur(gray, (0, 0), 1) - 0.025) / 0.07, 0, 1)
    col = col * (1 - 0.55 * acc[..., None] * (mask[..., None] > 0.5))
    col = np.clip((col - 0.5) * 1.15 + 0.48, 0, 1)
    # gritty ink accents: contours, broken by the stroke noise
    e = cv2.Canny((cv2.GaussianBlur(gray, (0, 0), 2.0) * 255).astype(np.uint8), 60, 140)
    num, lb, st, _ = cv2.connectedComponentsWithStats(e, connectivity=8)
    ok = st[:, cv2.CC_STAT_AREA] > 25
    ok[0] = False
    e = ok[lb].astype(np.float32)
    e *= (tex > -0.5)
    # sparse hatching in the deepest shadows
    hat = ((xx0 + yy0 + rng.integers(0, 6)) % 7 < 1).astype(np.float32)
    hat *= (lum < 0.18) * (cv2.GaussianBlur(rng.random((h, w)).astype(np.float32), (0, 0), 4) > 0.5)
    feat = xdog(gray, 0.9) * (cv2.GaussianBlur(gray, (0, 0), 1) < cv2.GaussianBlur(gray, (0, 0), 5) - 0.02)
    ink = np.clip(0.4 * e + 0.3 * hat + 1.0 * feat, 0, 1) * (mask > 0.5)
    col = col * (1 - ink[..., None] * 0.8) + ink[..., None] * 0.8 * np.array([0.10, 0.06, 0.08], np.float32)
    rim, rim_a = rim_light(mask)
    col = col * (1 - 0.35 * rim_a[..., None]) + rim * 1.5
    return np.clip(col, 0, 1.4), rim_a


def background(src, mask, n):
    ms = cv2.pyrMeanShiftFiltering(src, 14, 36)
    f = ms.astype(np.float32) / 255
    f = cv2.GaussianBlur(f, (0, 0), 1.8)                            # depth softness
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
    tex = dab_texture(900 + n // 2, coarse=4, ks=KS_LONG)
    lum = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
    # posterised painted value: flat set planes like a matte painting
    q = np.round(lum * 6) / 6
    f = f * (0.55 + 0.45 * (q / np.maximum(lum, 1e-3)))[..., None]
    lum = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV).astype(np.float32)
    glow = np.clip((gray - 0.72) / 0.28, 0, 1) * (hsv[..., 1] < 70)  # window / bright practicals
    glow = cv2.GaussianBlur(glow.astype(np.float32), (0, 0), 3)
    # moody set: darker, teal-blue shadows
    dark = f * 0.55
    dark = dark * (np.array([1.30, 1.05, 0.65], np.float32) * (1 - lum[..., None]) + np.array([0.95, 1.0, 1.05], np.float32) * lum[..., None])
    dark *= (1 + 0.09 * tex)[..., None]
    amber = np.array([0.30, 0.70, 1.0], np.float32)
    out = dark * (1 - glow[..., None]) + glow[..., None] * amber * (0.85 + 0.15 * lum[..., None])
    # wide warm glow from the window into the room
    out += cv2.GaussianBlur(glow, (0, 0), 30)[..., None] * np.array([0.06, 0.18, 0.32], np.float32)
    # floating dust motes in the light (slow drift)
    rng = np.random.default_rng(77)
    pts = rng.random((70, 3))
    motes = np.zeros((h, w), np.float32)
    for px, py, sp in pts:
        x = int((px * w + n * (0.4 + sp)) % w)
        y = int((py * h - n * (0.25 + 0.3 * sp) + 3 * np.sin(n / 9 + px * 6)) % h)
        cv2.circle(motes, (x, y), 1 + int(sp * 2), 1.0, -1, cv2.LINE_AA)
    light = cv2.GaussianBlur(glow, (0, 0), 50) * 4 + 0.15
    motes = cv2.GaussianBlur(motes, (0, 0), 0.8) * np.clip(light, 0, 1)
    out += motes[..., None] * np.array([0.5, 0.8, 1.0], np.float32) * 0.7
    return np.clip(out, 0, 1.3)


def render(n):
    src, mask = read(n)
    bg = background(src, mask, n)
    pe, rim_a = people(src, mask, n)
    m = cv2.GaussianBlur(mask, (0, 0), 0.8)[..., None]
    img = bg * (1 - m) + pe * m
    big = cv2.resize(img.astype(np.float32), (W, H), interpolation=cv2.INTER_CUBIC)
    # bloom on hot rims and glows
    hot = np.clip(big - 0.75, 0, None)
    big = big + cv2.GaussianBlur(hot, (0, 0), 14) * 1.2 + cv2.GaussianBlur(hot, (0, 0), 4) * 0.6
    # painted crispness, mild grain, vignette
    big = big + 0.35 * (big - cv2.GaussianBlur(big, (0, 0), 2.0))
    rng = np.random.default_rng(5000 + n)
    big += rng.normal(0, 0.012, (H, W, 1)).astype(np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - W / 2) / (W * 0.55)) ** 2 + ((yy - H / 2) / (H * 0.6)) ** 2)
    big *= np.clip(1.05 - 0.38 * r ** 2, 0.45, 1)[..., None]
    big = big / (1 + 0.12 * np.clip(big - 0.8, 0, None))
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), (np.clip(big, 0, 1) * 255).astype(np.uint8))
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    nums = frame_list()
    with Pool(3) as p:
        for n in p.imap_unordered(render, nums):
            print(n, end=" ", flush=True)
    print()
