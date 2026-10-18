"""Teal & Orange Anamorphic blockbuster grade, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [all | frame numbers...]

Per frame:
  * shallow depth of field: the room behind the people is defocused with a
    vertically oval (anamorphic) bokeh kernel, highlights bloom into oval discs
  * teal/orange grade in Lab: warm hues (skin, wood, batik) pushed to orange,
    everything neutral or cool pushed to teal, teal shadows, warm highlights
  * horizontal blue anamorphic streak flares from the brightest points
  * red-orange halation around highlights, 35mm grain, vignette
  * 2.39:1 letterbox inside the 3:2 frame; the scope window pans smoothly so
    every head stays in the picture (precomputed from the masks over the clip)
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
SCOPE_H = round(W / 2.39)          # 678
BAR = (H - SCOPE_H) // 2           # 201


def load(n):
    img = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png")).astype(np.float32) / 255
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
    return img, m


def scope_offsets():
    """Top row of the 2.39 window for every frame, smoothed over time."""
    tops = []
    for n in range(1, N + 1):
        m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE)
        rows = np.where((m > 128).sum(1) > 25)[0]
        tops.append(rows[0] if len(rows) else 0)
    tops = np.array(tops, np.float32)
    oy = np.clip(tops - 70, 0, H - SCOPE_H)
    k = 9
    pad = np.pad(oy, k, mode="edge")
    sm = np.convolve(pad, np.ones(2 * k + 1) / (2 * k + 1), mode="same")[k:-k]
    # never cut a head: the window may only be higher than the smoothed value
    return np.minimum(sm, np.clip(tops - 20, 0, H - SCOPE_H)).round().astype(int)


def oval_kernel(rx, ry):
    k = np.zeros((2 * ry + 1, 2 * rx + 1), np.float32)
    cv2.ellipse(k, (rx, ry), (rx, ry), 0, 0, 360, 1.0, -1, cv2.LINE_AA)
    # brighter rim, like real lens bokeh
    inner = np.zeros_like(k)
    cv2.ellipse(inner, (rx, ry), (max(1, rx - 2), max(1, ry - 3)), 0, 0, 360, 1.0, -1, cv2.LINE_AA)
    k = k * 0.75 + (k - inner).clip(0, 1) * 0.6
    return k / k.sum()


def defocus(img, m):
    """Background-only oval bokeh blur at quarter res (normalized so people don't bleed)."""
    s = 4
    small = cv2.resize(img, (W // s, H // s), interpolation=cv2.INTER_AREA)
    bg = 1 - cv2.resize(m, (W // s, H // s), interpolation=cv2.INTER_AREA)
    bg = cv2.erode(bg, np.ones((5, 5), np.uint8))
    lin = np.power(small, 2.6) * 1.0
    hot = np.clip((small.max(2, keepdims=True) - 0.82) / 0.18, 0, 1) ** 2
    lin = lin * (1 + 5.0 * hot)                      # highlights dominate the blur -> discs
    k = oval_kernel(9, 14)
    num = cv2.filter2D(lin * bg[..., None], -1, k)
    den = cv2.filter2D(bg, -1, k)[..., None] + 1e-4
    out = np.power(np.clip(num / den / (1 + 1.2 * cv2.filter2D(hot[..., 0] * bg, -1, k)[..., None]), 0, 4), 1 / 2.6)
    out = cv2.resize(out, (W, H), interpolation=cv2.INTER_CUBIC)
    return out


def grade(img, rng):
    lab = cv2.cvtColor(np.clip(img, 0, 1), cv2.COLOR_BGR2Lab)
    L, a, b = lab[..., 0] / 100, lab[..., 1], lab[..., 2]
    warm = 1 / (1 + np.exp(-((b + 0.6 * a) - 14) / 5))
    warm = cv2.GaussianBlur(warm, (0, 0), 2)
    # contrast S-curve on L
    Lc = np.clip(L, 0, 1)
    Lc = Lc + 0.35 * (Lc - 0.5) * (1 - np.abs(2 * Lc - 1))
    Lc = 0.035 + Lc * 0.93
    shadow = (1 - Lc) ** 1.6
    hi = np.clip((Lc - 0.6) / 0.4, 0, 1)
    teal_a, teal_b = -15 - 6 * shadow, -17 - 8 * shadow
    na = warm * (a * 1.25 + 9) + (1 - warm) * (teal_a * (1 - 0.5 * hi) + 0.3 * a)
    nb = warm * (b * 1.45 + 20) + (1 - warm) * (teal_b * (1 - 0.55 * hi) + 0.2 * b)
    # warm, slightly creamy highlights everywhere
    na += hi * 3
    nb += hi * 8
    out = cv2.cvtColor(np.dstack([Lc * 100, na, nb]).astype(np.float32), cv2.COLOR_Lab2BGR)
    return np.clip(out, 0, 1)


def streaks(img, m, rng, t):
    """Horizontal anamorphic flares from small bright points."""
    s = 4
    small = cv2.resize(img, (W // s, H // s), interpolation=cv2.INTER_AREA)
    L = small.max(2)
    bg = 1 - cv2.dilate(cv2.resize(m, (W // s, H // s), interpolation=cv2.INTER_AREA), np.ones((9, 9), np.uint8))
    hot = np.clip((L - 0.6) / 0.2, 0, 1) * bg
    local = hot - cv2.GaussianBlur(hot, (0, 0), 5)
    local = np.clip(local, 0, 1) ** 2 * 0.5
    # one practical light hidden behind the top window frame, drifting a little
    cx = int((0.30 + 0.015 * np.sin(t * 0.21)) * W / s)
    cy = int(0.07 * H / s)
    cv2.circle(local, (cx, cy), 3, 2.4, -1, cv2.LINE_AA)
    xs = np.arange(-W // s, W // s + 1, dtype=np.float32)
    k = np.exp(-np.abs(xs) / (W / s * 0.18)) * 0.6 + np.exp(-np.abs(xs) / (W / s * 0.04))
    k = (k / k.sum())[None, :]
    st = cv2.filter2D(local, -1, k, borderType=cv2.BORDER_CONSTANT) * 30
    st = cv2.GaussianBlur(st, (0, 0), sigmaX=1.5, sigmaY=0.8)
    core = cv2.GaussianBlur(local, (0, 0), 2.5) * 2.2
    flick = 1 + 0.12 * np.sin(t * 1.7) + rng.normal(0, 0.04)
    st = cv2.resize(st * flick, (W, H), interpolation=cv2.INTER_CUBIC)
    core = cv2.resize(core, (W, H), interpolation=cv2.INTER_CUBIC)
    blue = np.array([1.0, 0.62, 0.22], np.float32)
    # faint ghost discs along the optical axis, mirrored through frame centre
    ghosts = np.zeros((H, W), np.float32)
    gx, gy = cx * s, cy * s
    for f, r, a in ((0.55, 38, 0.10), (1.25, 22, 0.14), (1.6, 60, 0.06)):
        px = int(W / 2 + (W / 2 - gx) * f)
        py = int(H / 2 + (H / 2 - gy) * f)
        cv2.ellipse(ghosts, (px, py), (r, int(r * 1.5)), 0, 0, 360, a, -1, cv2.LINE_AA)
    ghosts = cv2.GaussianBlur(ghosts, (0, 0), 5)
    return st[..., None] * blue + core[..., None] * np.array([1.0, 0.9, 0.8], np.float32) \
        + ghosts[..., None] * np.array([0.9, 0.75, 0.35], np.float32)


def render(n, oy):
    rng = np.random.default_rng(5400 + n)
    img, m = load(n)
    t = n / 12 * 2 * np.pi
    msoft = cv2.GaussianBlur(m, (0, 0), 2.5)[..., None]
    bgblur = defocus(img, m)
    # exposure for a moody scope look: roll off the blown window, darker room,
    # people lit a stop brighter than the background
    bgblur = 0.95 * bgblur / (1 + 0.45 * bgblur)
    subj = np.power(img, 1.15) * 0.98
    comp = subj * msoft + bgblur * (1 - msoft)
    g = grade(comp, rng)
    # halation: red/orange glow around highlights
    L = g.max(2)
    hal = cv2.GaussianBlur(np.clip((L - 0.62) / 0.3, 0, 1), (0, 0), 9)
    g = g + hal[..., None] * np.array([0.02, 0.10, 0.30], np.float32)
    # gentle bloom
    bl = cv2.GaussianBlur(np.clip(g - 0.7, 0, 1), (0, 0), 25)
    g = g + bl * 0.25
    g = 1 - (1 - g) * (1 - np.clip(streaks(g, m, rng, t), 0, 1.5) * 0.85)
    # vignette
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    cyy = oy + SCOPE_H / 2
    r = np.sqrt(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - cyy) / (SCOPE_H * 0.85)) ** 2)
    g = g * (1 - 0.38 * np.clip(r - 0.45, 0, 1) ** 1.4)[..., None]
    # 35mm grain, stronger in mids, slightly coloured, new every frame
    gr = cv2.GaussianBlur(rng.normal(0, 1, (H, W)).astype(np.float32), (0, 0), 0.75)
    grc = cv2.GaussianBlur(rng.normal(0, 1, (H, W, 3)).astype(np.float32), (0, 0), 1.1)
    Lm = g.mean(2, keepdims=True)
    amp = 0.025 + 0.035 * (4 * Lm * (1 - Lm))
    g = g + gr[..., None] * amp + grc * 0.008
    g = np.clip(g, 0, 1)
    # letterbox: take the scope window from the graded frame, black bars outside
    out = np.zeros_like(g)
    out[BAR:BAR + SCOPE_H] = g[oy:oy + SCOPE_H]
    out[BAR:BAR + SCOPE_H] *= 1.0
    out = (out * 255 + rng.random(out.shape) - 0.5).clip(0, 255).astype(np.uint8)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), out)
    return n


def main():
    os.makedirs(OUT, exist_ok=True)
    nums = list(range(1, N + 1)) if (not ARGS or ARGS == ["all"]) else [int(a) for a in ARGS]
    offs = scope_offsets()
    with Pool(min(8, os.cpu_count() or 4)) as p:
        for n in p.starmap(render, [(n, int(offs[n - 1])) for n in nums]):
            pass
    print("rendered", len(nums), "->", OUT)


if __name__ == "__main__":
    main()
