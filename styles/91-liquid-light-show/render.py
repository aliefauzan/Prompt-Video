"""Liquid Light Show (1960s overhead-projector oil + dye), frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [all | frame numbers...]

Per frame:
  * a projected "wet show" is simulated at half resolution: four transparent
    dye pools (magenta, amber, yellow, cyan) are domain-warped noise fields
    that swirl and drift slowly; they mix SUBTRACTIVELY like stacked liquids
    in a clock-glass dish, so overlaps go deep red, violet, green or black
  * clusters of clear oil drops float in the dye: round cells that push the
    dye aside, each with a dark meniscus outline and a bright refracted rim;
    they drift with the swirl and swell / shrink
  * the round projector dish shows as a big soft-edged light circle, a warm
    lamp hot spot sits in the middle, the light pulses slightly
  * the room goes dark: the wall acts as the projection screen and the people
    are lit only by the projected colour (plus a little key light so faces
    stay readable); haze glow and 16mm grain on top
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np

FRAMES, MASKS, OUT = sys.argv[1:4]
ARGS = sys.argv[4:]
N = len([f for f in os.listdir(FRAMES) if f.startswith("frame_") and f.endswith(".png")])
W, H = 1620, 1080
LW, LH = 810, 540
TEX = 512

# transmitted colour of each dye (BGR) — classic liquid-light palette
DYES = np.array([
    [0.55, 0.05, 1.00],   # magenta / hot pink
    [0.02, 0.55, 1.00],   # amber / orange
    [0.10, 0.95, 1.00],   # yellow
    [1.00, 0.10, 0.38],   # deep blue / violet
], np.float32)


def fbm_tex(seed, beta):
    """Periodic 2-D noise via 1/f^beta spectral filtering, range ~[0,1]."""
    rng = np.random.default_rng(seed)
    f = np.fft.fftfreq(TEX)
    k = np.sqrt(f[None, :] ** 2 + f[:, None] ** 2)
    k[0, 0] = 1
    amp = 1 / k ** beta
    amp[0, 0] = 0
    amp[k > 0.07] = 0
    ph = np.exp(2j * np.pi * rng.random((TEX, TEX)))
    n = np.real(np.fft.ifft2(amp * ph))
    n = (n - n.mean()) / n.std()
    return (0.5 + 0.18 * n).astype(np.float32)


def init():
    global TEXS, PART
    TEXS = [fbm_tex(910 + i, 2.1) for i in range(8)]
    rng = np.random.default_rng(91)
    # oil-drop clusters: each cluster has a centre path, drops sit around it
    parts = []
    for c in range(5):
        cx, cy = rng.random() * LW, rng.random() * LH
        vx, vy = rng.normal(0, 0.9), rng.normal(0, 0.6)
        for d in range(rng.integers(6, 16)):
            parts.append((c, cx, cy, vx, vy,
                          rng.normal(0, 70), rng.normal(0, 50),
                          np.exp(rng.normal(3.0, 0.45)), rng.random() * 6.28, rng.random()))
    PART = parts


YL, XL = np.mgrid[0:LH, 0:LW].astype(np.float32)


def sample(tex, x, y):
    return cv2.remap(tex, (x % TEX).astype(np.float32), (y % TEX).astype(np.float32),
                     cv2.INTER_LINEAR, borderMode=cv2.BORDER_WRAP)


def smooth(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


def projection(t):
    s = 0.42
    u, v = XL * s, YL * s
    # big slow swirl: rotate coordinates around the dish centre a little
    a = 0.012 * t
    cu, cv_ = LW * s / 2, LH * s / 2
    ru = cu + (u - cu) * np.cos(a) - (v - cv_) * np.sin(a)
    rv = cv_ + (u - cu) * np.sin(a) + (v - cv_) * np.cos(a)
    qx = sample(TEXS[0], ru + 0.9 * t, rv + 0.4 * t) - 0.5
    qy = sample(TEXS[1], ru - 0.5 * t, rv + 0.8 * t) - 0.5
    # finer second warp: tendrils and curls along the dye edges
    qx = qx + 0.35 * (sample(TEXS[6], ru * 3.1 + 0.6 * t, rv * 3.1) - 0.5)
    qy = qy + 0.35 * (sample(TEXS[7], ru * 3.1, rv * 3.1 - 0.6 * t) - 0.5)
    trans = np.ones((LH, LW, 3), np.float32)
    dens_all = []
    for i in range(4):
        f = sample(TEXS[2 + i], ru * (0.9 + 0.12 * i) + 150 * qx + (i - 1.5) * 0.7 * t,
                   rv * (0.9 + 0.12 * i) + 150 * qy + 0.35 * t * (1 - i % 2 * 2))
        th = 0.50 + 0.03 * np.sin(t * 0.05 + i)
        d = smooth(th - 0.022, th + 0.022, f) * 0.95
        dens_all.append(d)
        trans *= 1 - d[..., None] * (1 - DYES[i])
    # oil drops: push dye aside, dark meniscus, bright rim
    # union of the drops (min signed distance), so touching drops merge
    dmin = np.full((LH, LW), 99.0, np.float32)
    for (c, cx, cy, vx, vy, ox, oy, r0, ph, sp) in PART:
        x = (cx + vx * t + ox + 18 * np.sin(t * 0.03 + ph)) % (LW + 200) - 100
        y = (cy + vy * t + oy + 14 * np.cos(t * 0.025 + ph)) % (LH + 200) - 100
        r = r0 * (1 + 0.25 * np.sin(t * (0.04 + 0.04 * sp) + ph))
        x0, x1 = int(max(0, x - r - 8)), int(min(LW, x + r + 9))
        y0, y1 = int(max(0, y - r - 8)), int(min(LH, y + r + 9))
        if x1 <= x0 or y1 <= y0:
            continue
        d = np.sqrt((XL[y0:y1, x0:x1] - x) ** 2 + (YL[y0:y1, x0:x1] - y) ** 2) - r
        # lens shading: brighter towards the rim inside each drop
        dmin[y0:y1, x0:x1] = np.minimum(dmin[y0:y1, x0:x1], d)
    inside = smooth(0.8, -0.8, dmin)
    edge = np.exp(-((dmin - 0.3) / 1.2) ** 2)
    rim = np.exp(-((dmin + 2.5) / 2.0) ** 2)
    # inside a drop the dye is pushed aside: the cell glows with the lamp
    # through a thin amber / pink film, darker meniscus, bright crescent rim
    cell = np.array([0.35, 0.80, 1.0], np.float32) * (0.75 + 0.25 * dens_all[0][..., None]) \
        * (1 - dens_all[0][..., None] * 0.35 * np.array([0.0, 1.0, 0.0], np.float32))
    clear = np.sqrt(np.clip(trans, 0, 1)) * 0.6 + cell * 0.55
    trans = trans * (1 - inside[..., None]) + clear * inside[..., None]
    trans = trans * (1 - 0.7 * edge[..., None]) + rim[..., None] * np.array([0.35, 0.5, 0.6], np.float32)
    # lamp: warm hot spot, round projector dish with a soft edge
    rr = np.sqrt(((XL - LW * 0.5) / (LW * 0.62)) ** 2 + ((YL - LH * 0.46) / (LH * 0.80)) ** 2)
    dish = smooth(1.02, 0.86, rr)
    lamp = (0.8 + 0.45 * np.exp(-rr ** 2 / 0.25)) * dish
    lamp = lamp * (1 + 0.05 * np.sin(t * 0.9) + 0.03 * np.sin(t * 2.3))
    light = trans * lamp[..., None] * np.array([0.92, 0.98, 1.05], np.float32)
    return light


def render(n):
    rng = np.random.default_rng(9100 + n)
    t = float(n)
    img = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png")).astype(np.float32) / 255
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
    light = np.clip(cv2.resize(projection(t), (W, H), interpolation=cv2.INTER_CUBIC), 0, None)
    ms = cv2.GaussianBlur(m, (0, 0), 2)[..., None]
    lum = img.mean(2, keepdims=True)
    # wall / room behaves like a projection screen: flattened albedo
    bg_alb = 0.62 + 0.38 * lum
    # people keep their own texture and colour under the coloured light
    p_alb = np.clip(np.power(img, 0.85) * 1.25, 0, 1) * 0.75 + lum * 0.35
    alb = p_alb * ms + bg_alb * (1 - ms)
    out = alb * np.power(light, 1.15) * 1.2
    # a touch of dim key light on the people so faces never drop to black
    out = out + img * ms * 0.24
    # smoky-hall glow around bright projected colour
    glow = cv2.GaussianBlur(out, (0, 0), 18)
    out = 1 - (1 - out) * (1 - 0.35 * glow)
    # 16mm grain
    g = cv2.GaussianBlur(rng.normal(0, 1, (H, W)).astype(np.float32), (0, 0), 0.9)
    out = out + g[..., None] * 0.025
    out = np.clip(out, 0, 1)
    out = (out * 255 + rng.random(out.shape) - 0.5).clip(0, 255).astype(np.uint8)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), out)
    return n


def main():
    os.makedirs(OUT, exist_ok=True)
    nums = list(range(1, N + 1)) if (not ARGS or ARGS == ["all"]) else [int(a) for a in ARGS]
    with Pool(4, initializer=init) as p:
        for _ in p.imap_unordered(render, nums):
            pass
    print("rendered", len(nums), "->", OUT)


if __name__ == "__main__":
    main()
