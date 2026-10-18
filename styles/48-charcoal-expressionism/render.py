"""Charcoal expressionism restyle, frame by frame.

usage: python render.py <frames_dir> <masks_dir> <out_dir> [frame numbers...]
Dark monochrome charcoal drawing on toothy paper. People become velvety
near-black shadow figures (faces lifted just enough to stay recognisable, lit
from one side), their edges smudged out into a pale, drifting fog. The room
dissolves into blurred grey shapes behind the fog with a darker ground, a few
eraser-lifted light shafts and heavy vignetting. Loose charcoal strokes rework
the silhouettes and finger smudges and charcoal dust change every frame; the fog
drifts slowly so the background never jumps.
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
H0, W0 = 1080, 1620

_r = np.random.default_rng(48)
TOOTH = cv2.GaussianBlur(_r.random((H0, W0)).astype(np.float32), (0, 0), 1.3)          # static paper tooth
TOOTH = cv2.blur(TOOTH, (5, 2))                                                        # laid-paper fibres
TOOTH = (TOOTH - TOOTH.mean()) / TOOTH.std()
FOG = cv2.resize(cv2.GaussianBlur(_r.random((H0 // 6, W0 // 6 * 2)).astype(np.float32), (0, 0), 9),
                 (W0 * 2, H0))                                                         # wide fog field, scrolled
FOG = (FOG - FOG.min()) / np.ptp(FOG)
FOG2 = cv2.resize(cv2.GaussianBlur(_r.random((H0 // 4, W0 // 4 * 2)).astype(np.float32), (0, 0), 4),
                  (W0 * 2, H0))
FOG2 = (FOG2 - FOG2.min()) / np.ptp(FOG2)


def streaks(rng, h, w, angle, length, sigma=1.0):
    """Directional charcoal stroke texture (zero mean, unit std)."""
    k = np.zeros((length, length), np.float32)
    c = length // 2
    dx, dy = np.cos(np.radians(angle)), np.sin(np.radians(angle))
    for t in np.linspace(-c, c, length * 2):
        k[int(round(c + t * dy)) % length, int(round(c + t * dx)) % length] = 1
    k /= k.sum()
    nz = cv2.GaussianBlur(rng.random((h, w)).astype(np.float32), (0, 0), sigma)
    s = cv2.filter2D(nz, -1, k, borderType=cv2.BORDER_REFLECT)
    return (s - s.mean()) / (s.std() + 1e-6)


BG_STROKES = streaks(np.random.default_rng(481), H0, W0 * 2, -22, 91, 2.5)               # sweeping bg strokes


def vnoise(rng, h, w, cell):
    a = rng.random((max(2, h // cell + 2), max(2, w // cell + 2))).astype(np.float32)
    return cv2.resize(a, (w, h), interpolation=cv2.INTER_CUBIC)


def face_light(n, h, w):
    """Soft pools of light on each face, so identities survive the darkness."""
    lay = np.zeros((h, w), np.float32)
    for f in FACES.get(f"frame_{n:03d}.png", []):
        x, y, bw, bh = f["box"]
        if bw < 40:
            continue
        cv2.ellipse(lay, (int(x + bw / 2), int(y + bh * 0.45)), (int(bw * 0.55), int(bh * 0.75)), 0, 0, 360, 1, -1)
    return cv2.GaussianBlur(lay, (0, 0), 18)


def charcoal_strokes(region, rng, h, w):
    """Loose, broken, soft charcoal strokes reworking the silhouette."""
    lay = np.zeros((h, w), np.uint8)
    cs, _ = cv2.findContours(region.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for c in cs:
        if len(c) < 150:
            continue
        p = c[:, 0, :].astype(np.float32)
        k = 21
        p = np.stack([np.convolve(np.r_[p[-k:, i], p[:, i], p[:k, i]], np.ones(k) / k, "same")[k:-k]
                      for i in range(2)], 1)[::3]
        i = 0
        while i < len(p):
            L = int(rng.integers(15, 60))
            seg = p[i:i + L]
            i += L + int(rng.integers(0, 25))
            if len(seg) < 4 or rng.random() < 0.3:
                continue
            off = rng.normal(0, 4, 2)
            cv2.polylines(lay, [(seg + off).astype(np.int32)], False, 255, int(rng.integers(4, 14)), cv2.LINE_AA)
    a = cv2.GaussianBlur(lay.astype(np.float32) / 255, (0, 0), 2.5)
    return a * (0.5 + 0.5 * (vnoise(rng, h, w, 3) > 0.35))


def smudge(img, rng, h, w, count):
    """Finger smudges: soft directional smears of the drawing in random patches."""
    out = img.copy()
    for _ in range(count):
        ang = rng.uniform(-40, 40) + (90 if rng.random() < 0.3 else 0)
        L = int(rng.integers(25, 70))
        k = np.zeros((L, L), np.float32)
        c = L // 2
        dx, dy = np.cos(np.radians(ang)), np.sin(np.radians(ang))
        for t in np.linspace(-c, c, L * 2):
            k[int(round(c + t * dy)) % L, int(round(c + t * dx)) % L] = 1
        k /= k.sum()
        cx, cy = rng.integers(0, w), rng.integers(0, h)
        r = int(rng.integers(80, 220))
        x0, x1, y0, y1 = max(0, cx - r), min(w, cx + r), max(0, cy - r), min(h, cy + r)
        patch = cv2.filter2D(img[y0:y1, x0:x1], -1, k, borderType=cv2.BORDER_REFLECT)
        yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
        wgt = np.clip(1 - np.hypot((xx - cx) / r, (yy - cy) / r * 1.6), 0, 1) ** 1.5
        out[y0:y1, x0:x1] = out[y0:y1, x0:x1] * (1 - wgt) + patch * wgt
    return out


def render(n):
    rng = np.random.default_rng(4800 + n)
    rng2 = np.random.default_rng(9800 + (n - 1) // 2)                 # strokes & smudges on twos
    bgr = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png"))
    mk = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE)
    h, w = mk.shape
    g = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
    m = mk.astype(np.float32) / 255
    soft = cv2.GaussianBlur(m, (0, 0), 7)                               # silhouettes dissolve into fog
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)

    # ---- background: the room seen through fog ------------------------------
    bg = cv2.GaussianBlur(g, (0, 0), 9)
    bg = 0.42 + 0.38 * (bg - 0.5)                                       # flattened greys
    ground = np.clip((yy / h - 0.62) / 0.38, 0, 1)
    bg -= 0.20 * ground                                                 # darker ground plane
    sh = int(n * 2.2) % W0                                              # fog drifts left->right
    fog = FOG[:, sh:sh + w] * 0.7 + FOG2[:, (sh * 2) % W0:(sh * 2) % W0 + w] * 0.3
    band = np.exp(-((yy / h - 0.48) / 0.28) ** 2)                       # fog is thickest at mid height
    bg = bg + (0.90 - bg) * np.clip(0.32 + 0.55 * fog * band, 0, 0.88)
    # eraser-lifted light shafts from top left
    t = (xx * 0.42 - yy) / w
    shaft = np.zeros_like(g)
    for c0, wd in ((0.06, 0.035), (0.18, 0.02), (0.31, 0.05)):
        shaft += np.exp(-((t - c0) / wd) ** 2)
    bg += 0.09 * shaft * (1 - yy / h) * (0.6 + 0.4 * fog)
    glow = np.exp(-(((xx - 0.55 * w) / (0.45 * w)) ** 2 + ((yy - 0.38 * h) / (0.38 * h)) ** 2))
    bg += (0.95 - bg) * 0.45 * glow                                     # luminous fog behind the figures
    bg += 0.045 * BG_STROKES[:, sh // 2:sh // 2 + w]                    # broad charcoal strokes, drift with the fog

    # ---- people: velvety shadow figures -------------------------------------
    pg = cv2.bilateralFilter(g, 9, 0.15, 5)
    fig = 0.03 + 0.30 * np.power(pg, 1.6)                               # crushed, velvety
    fl = face_light(n, h, w)
    side = np.clip(0.55 + 0.45 * (xx / w - 0.5) * 2, 0.3, 1)             # eerie key from the right
    fig = fig + fl * (0.16 + 0.70 * np.power(pg, 1.1)) * side
    fig += 0.035 * streaks(rng2, h, w, 78, 41, 1.5) * (1 - fl)          # vertical body strokes, redrawn on twos
    fig = cv2.GaussianBlur(fig, (0, 0), 1.2)
    tone = bg * (1 - soft) + fig * soft
    # fog curls in front of the lower bodies
    front = np.clip((yy / h - 0.70) / 0.3, 0, 1) * FOG2[:, (sh * 3) % W0:(sh * 3) % W0 + w]
    tone += (0.7 - tone) * 0.35 * front

    # ---- charcoal work -------------------------------------------------------
    strokes = charcoal_strokes(m > 0.5, rng2, h, w)
    tone = tone * (1 - 0.75 * strokes)
    tone = smudge(tone, rng2, h, w, 10)
    vig = np.clip(1 - 0.55 * (((xx - w / 2) / (w / 1.7)) ** 2 + ((yy - h / 2) / (h / 1.5)) ** 2), 0, 1)
    tone *= 0.48 + 0.52 * vig

    # charcoal on toothy paper: darkness catches on the tooth, dust changes per frame
    dark = np.clip(1 - tone, 0, 1)
    dust = cv2.GaussianBlur(rng.random((h, w)).astype(np.float32), (0, 0), 1.1)
    dust = (dust - dust.mean()) / dust.std()
    mid = 4 * dark * (1 - dark)                                         # grain shows most in the mid greys
    calm = 1 - 0.6 * fl * soft                                          # keep faces readable
    dep = dark + mid * calm * (0.055 * TOOTH + 0.022 * dust) + 0.012 * TOOTH
    dep = np.clip(dep, 0, 1)
    out = 1 - dep
    out = 0.035 + 0.92 * out                                            # charcoal black / warm grey paper
    rgb = np.stack([out * 0.97, out * 0.985, out], -1)                   # tiny warmth of the paper
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), (np.clip(rgb, 0, 1) * 255).astype(np.uint8))
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    todo = ONLY or list(range(1, N + 1))
    with Pool(max(1, os.cpu_count() - 2)) as p:
        for _ in p.imap_unordered(render, todo):
            pass
