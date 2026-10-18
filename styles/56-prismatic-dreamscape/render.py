"""Prismatic Dreamscape restyle, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [all | frame numbers...]

Per frame:
  * overexposed, sun-drenched pastel base: lifted lavender blacks, soft contrast,
    background in soft focus with iridescent round bokeh
  * spectral dispersion: the frame is resampled at 7 "wavelengths" with slightly
    different radial scale, each tinted its spectral colour -> rainbow fringes on
    every edge, strongest toward the frame edges
  * prism refraction: a glass prism held at the lens edge folds a displaced,
    mirrored, blurred copy of the scene into one side, with a rainbow seam
  * rainbow light leaks: soft diagonal spectrum bands of sunlight through prism
    glass, drifting slowly across the frame and faces
  * holographic lens-flare ghosts, sparkle glints, glowing bloom, pastel haze
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
YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)


def spectrum(u):
    """u in 0..1 -> BGR rainbow (red..violet), float."""
    hue = (np.clip(u, 0, 1) * 150).astype(np.uint8)  # OpenCV hue 0..179; stop at violet
    hsv = np.dstack([hue, np.full_like(hue, 200), np.full_like(hue, 255)])
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR).astype(np.float32) / 255


def dispersion(img, strength):
    """Resample at 7 radial scales, each weighted by its spectral colour."""
    cx, cy = W / 2, H / 2
    out = np.zeros_like(img)
    wsum = np.zeros(3, np.float32)
    for i in range(7):
        u = i / 6
        col = spectrum(np.array([[u]], np.float32))[0, 0] + 0.08
        s = 1 + (u - 0.5) * strength
        M = cv2.getRotationMatrix2D((cx, cy), 0, s)
        warped = cv2.warpAffine(img, M, (W, H), borderMode=cv2.BORDER_REFLECT)
        out += warped * col
        wsum += col
    return out / wsum


def bokeh_layer(rng_world, t):
    """Iridescent round bokeh discs drifting slowly (fixed population, moving with time)."""
    layer = np.zeros((H // 2, W // 2, 3), np.float32)
    for i in range(22):
        x0, y0 = rng_world[i, 0] * W / 2, rng_world[i, 1] * H / 2
        r = int(8 + rng_world[i, 2] * 34)
        x = int((x0 + 9 * t * (0.5 + rng_world[i, 3])) % (W / 2))
        y = int(y0 + 6 * np.sin(t * 0.3 + i))
        col = spectrum(np.array([[(rng_world[i, 4] + 0.02 * t) % 1]], np.float32))[0, 0] * 0.6 + 0.4
        disc = np.zeros((H // 2, W // 2), np.float32)
        cv2.circle(disc, (x, y), r, 0.35, -1, cv2.LINE_AA)
        cv2.circle(disc, (x, y), r, 0.65, 2, cv2.LINE_AA)
        layer += disc[..., None] * col * (0.35 + 0.5 * rng_world[i, 5])
    layer = cv2.GaussianBlur(layer, (0, 0), 1.6)
    return cv2.resize(layer, (W, H), interpolation=cv2.INTER_LINEAR)


def light_leaks(t, n):
    """Diagonal rainbow bands (sunlight through prism glass)."""
    out = np.zeros((H, W, 3), np.float32)
    bands = [  # angle deg, offset (0..1 across frame), width px, strength, drift
        (-28, 0.42, 420, 0.42, 0.010),
        (-34, 0.80, 260, 0.34, -0.007),
        (-22, 0.10, 520, 0.22, 0.006),
    ]
    for ang, off, width, s, drift in bands:
        a = np.deg2rad(ang)
        d = XX * np.cos(a) + YY * np.sin(a)
        dmin, dmax = d.min(), d.max()
        c = dmin + (dmax - dmin) * ((off + drift * t) % 1.2 - 0.1)
        u = (d - c) / width + 0.5
        inside = np.clip(1 - np.abs(u - 0.5) * 2, 0, 1) ** 0.35
        col = spectrum(np.clip(u, 0, 1))
        # brighter toward the top (sun side), feathered
        fall = np.clip(1.25 - YY / H, 0.2, 1.0)[..., None]
        out += (col - 0.25) * 1.4 * inside[..., None] * s * fall * (0.85 + 0.15 * np.sin(t * 0.9 + off * 9))
    return cv2.GaussianBlur(out, (0, 0), 6)


def prism_fold(img, t, ms):
    """A prism at the left edge of the lens folds a mirrored, shifted copy into a wedge."""
    edge_x = W * (0.13 + 0.03 * np.sin(t * 0.12))
    tilt = 0.18 + 0.05 * np.sin(t * 0.08)
    boundary = edge_x + (YY - H / 2) * tilt
    wedge = np.clip((boundary - XX) / 40 + 0.5, 0, 1)                   # 1 inside the wedge
    # mirrored copy: reflect across the boundary + shift up
    mx = (2 * boundary - XX + 120).clip(0, W - 1)
    my = (YY - 40).clip(0, H - 1)
    copy = cv2.remap(img, mx.astype(np.float32), my.astype(np.float32), cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    copy = cv2.GaussianBlur(copy, (0, 0), 5)
    copy = 1 - (1 - copy) * 0.75  # paler, glassy
    seam_u = (XX - boundary) / 70 + 0.5
    seam = np.clip(1 - np.abs(seam_u - 0.5) * 2, 0, 1)
    seam_col = spectrum(np.clip(seam_u, 0, 1)) * seam[..., None]
    wa = wedge[..., None] * (0.55 - 0.35 * ms)   # people stay readable through the glass
    out = img * (1 - wa) + copy * wa
    # second, smaller prism ghost at the top-right corner
    b2 = W * 0.86 - (YY - 0) * 0.5
    w2 = np.clip((XX - b2) / 30 + 0.5, 0, 1) * np.clip(1 - YY / (H * 0.55), 0, 1)
    mx2 = (2 * b2 - XX - 90).clip(0, W - 1)
    copy2 = cv2.GaussianBlur(cv2.remap(img, mx2.astype(np.float32), YY, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT), (0, 0), 7)
    w2a = w2[..., None] * (0.45 - 0.3 * ms)
    out = out * (1 - w2a) + (1 - (1 - copy2) * 0.7) * w2a
    s2u = (XX - b2) / 50 + 0.5
    s2 = np.clip(1 - np.abs(s2u - 0.5) * 2, 0, 1) * np.clip(1 - YY / (H * 0.55), 0, 1)
    return out, seam_col * 0.85 + spectrum(np.clip(s2u, 0, 1)) * s2[..., None] * 0.6


def flare_ghosts(t, rng):
    """Holographic ghosts along the axis from the sun (top-left) through centre."""
    sx, sy = W * (0.10 + 0.01 * np.sin(t * 0.2)), H * 0.04
    layer = np.zeros((H, W, 3), np.float32)
    for k, (f, r, a) in enumerate(((0.35, 26, 0.35), (0.7, 60, 0.18), (1.15, 38, 0.28), (1.45, 90, 0.12), (1.8, 20, 0.35))):
        px = W / 2 + (sx - W / 2) * (1 - 2 * f) * -1
        py = H / 2 + (sy - H / 2) * (1 - 2 * f) * -1
        g = np.zeros((H, W), np.float32)
        pts = cv2.ellipse2Poly((int(px), int(py)), (r, r), 15, 0, 360, 60)  # hexagonal aperture
        cv2.fillPoly(g, [pts], a, cv2.LINE_AA)
        dist = np.sqrt((XX - px) ** 2 + (YY - py) ** 2) / max(r, 1)
        col = spectrum(np.clip(dist * 0.9 - 0.1 + 0.15 * k, 0, 1))
        layer += cv2.GaussianBlur(g, (0, 0), 3)[..., None] * col
    # sun glow
    d = np.sqrt((XX - sx) ** 2 + (YY - sy) ** 2)
    glow = np.exp(-d / 260)[..., None] * np.array([0.85, 0.92, 1.0], np.float32) * 0.9
    return layer + glow


def face_rainbow(m, t):
    """The prism-photography signature: a narrow, vivid spectrum stripe projected across
    the main subject's face. Main subject = largest mask blob; stripe sits ~eye height."""
    mb = (m > 0.5).astype(np.uint8)
    cnt, lab, stats, _ = cv2.connectedComponentsWithStats(mb)
    if cnt <= 1:
        return np.zeros((H, W, 3), np.float32), 0
    i = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA] * (1.2 - np.abs(stats[1:, cv2.CC_STAT_LEFT] + stats[1:, cv2.CC_STAT_WIDTH] / 2 - W / 2) / W)))
    x0, y0, w, h = stats[i, :4]
    head = max(80, min(w * 0.45, 260))
    cy = y0 + head * (0.92 + 0.10 * np.sin(t * 0.15))
    cx = x0 + w / 2
    a = np.deg2rad(-14)
    d = -(XX - cx) * np.sin(a) + (YY - cy) * np.cos(a)
    width = head * 0.42
    u = d / width + 0.5
    inside = np.clip(1 - np.abs(u - 0.5) * 2, 0, 1) ** 0.5
    hsv_u = np.clip(u, 0, 1)
    hue = (hsv_u * 150).astype(np.uint8)
    col = cv2.cvtColor(np.dstack([hue, np.full_like(hue, 255), np.full_like(hue, 255)]), cv2.COLOR_HSV2BGR).astype(np.float32) / 255
    along = np.clip(1 - np.abs((XX - cx) * np.cos(a) + (YY - cy) * np.sin(a)) / (w * 0.9), 0, 1) ** 0.7
    return cv2.GaussianBlur(col * (inside * along)[..., None], (0, 0), 3), 1


def sparkles(rng, m):
    layer = np.zeros((H, W), np.float32)
    for _ in range(int(rng.integers(14, 24))):
        x, y = int(rng.uniform(0, W)), int(rng.uniform(0, H * 0.8))
        l = int(rng.uniform(10, 34))
        b = float(rng.uniform(0.4, 1.0))
        cv2.line(layer, (x - l, y), (x + l, y), b * 0.6, 1, cv2.LINE_AA)
        cv2.line(layer, (x, y - l), (x, y + l), b * 0.6, 1, cv2.LINE_AA)
        cv2.circle(layer, (x, y), 2, b, -1, cv2.LINE_AA)
    return cv2.GaussianBlur(layer, (0, 0), 0.9) + cv2.GaussianBlur(layer, (0, 0), 5) * 0.8


def render(n):
    rng = np.random.default_rng(5600 + n)
    world = np.random.default_rng(56).random((40, 6)).astype(np.float32)
    t = n / 12 * 2 * np.pi
    img = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png")).astype(np.float32) / 255
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
    msoft = cv2.GaussianBlur(m, (0, 0), 2.0)[..., None]

    # soft-focus background
    bg = 1 - m
    k = 15
    num = cv2.GaussianBlur(img * bg[..., None], (0, 0), k)
    den = cv2.GaussianBlur(bg, (0, 0), k)[..., None] + 1e-4
    bgb = num / den
    base = img * msoft + bgb * (1 - msoft)

    # sun-drenched pastel exposure: lift, soften, pastel tint
    base = 1 - np.power(1 - np.clip(base, 0, 1), 1.22)
    gray = base.mean(2, keepdims=True)
    base = gray + (base - gray) * 0.95
    tint = (np.array([0.97, 0.86, 1.0], np.float32) * (1 - XX / W)[..., None]          # blush pink left
            + np.array([1.0, 0.93, 0.86], np.float32) * (XX / W)[..., None])           # lavender-sky right
    base = base * tint
    base = 0.10 * np.array([0.95, 0.80, 0.88], np.float32) + base * 0.9                 # lavender blacks

    disp = dispersion(base, 0.034 + 0.006 * np.sin(t * 0.7))
    folded, seams = prism_fold(disp, t, msoft)
    out = folded

    leaks = light_leaks(t, n)
    leaks_on_people = 0.75  # light passes over faces too, but a bit softer
    leak_mask = (1 - msoft) + msoft * leaks_on_people
    out = np.clip(out + leaks * leak_mask * 0.6, 0, None)
    out = 1 - (1 - out) * (1 - np.clip(seams, 0, 1))
    fr, ok = face_rainbow(m, t)
    if ok:
        lum = out.mean(2, keepdims=True)
        on = msoft * 0.85 + (1 - msoft) * 0.35
        out = out * (1 - fr.max(2, keepdims=True) * on * 0.45) + fr * on * (0.55 + 0.6 * lum)
    # bokeh behind the people only
    out = out + bokeh_layer(world, t) * (1 - msoft) * 0.42
    out = 1 - (1 - out) * (1 - np.clip(flare_ghosts(t, rng), 0, 1) * 0.8)
    out = out + sparkles(rng, m)[..., None] * np.array([1.0, 0.97, 0.95], np.float32)

    # glowing bloom on highlights (overexposed, colourful)
    hi = np.clip(out - 0.75, 0, 1)
    out = out + cv2.GaussianBlur(hi, (0, 0), 10) * 0.6 + cv2.GaussianBlur(hi, (0, 0), 40) * 0.5
    # pastel haze breathing
    haze = np.array([0.98, 0.90, 0.97], np.float32) * (0.06 + 0.02 * np.sin(t * 0.5))
    out = out * (1 - haze.mean()) + haze
    out = out / (1 + 0.18 * np.clip(out - 0.8, 0, None))
    out = out + cv2.GaussianBlur(rng.normal(0, 1, (H, W)).astype(np.float32), (0, 0), 0.8)[..., None] * 0.012
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), (np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8))
    return n


def main():
    os.makedirs(OUT, exist_ok=True)
    nums = list(range(1, N + 1)) if (not ARGS or ARGS == ["all"]) else [int(a) for a in ARGS]
    with Pool(min(6, os.cpu_count() or 4)) as p:
        list(p.imap_unordered(render, nums))
    print("rendered", len(nums), "->", OUT)


if __name__ == "__main__":
    main()
