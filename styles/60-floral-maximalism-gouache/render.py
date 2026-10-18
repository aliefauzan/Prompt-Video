"""Floral Maximalism Gouache — local approximation of the frame-by-frame restyle.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [all | 13 49 85 ...]

Needs faces.json next to this script (Apple Vision boxes + landmarks, made by
`swift faces.swift ../../_source/frames faces.json`) for the cheek blush.

Per frame:
  1. flat 2D illustration: edge-preserving smoothing, then every pixel snaps to
     a fixed pastel folk-art gouache palette (Lab nearest, pastel-lifted), the
     label map is smoothed into clean flat shapes (blurred one-hot argmax) with
     slightly wobbly hand-painted edges (noise domain warp, re-drawn on twos).
  2. gouache surface: low-frequency value mottling inside each flat, dry-brush
     streaks, paper tooth grain, matte (no specular, no harsh shadows).
  3. floral maximalism: a fixed, seeded layout of folk-art motifs — round
     many-petal blooms with dotted centres, daisies, tulips, leafy sprigs and
     vines climbing the frame edges, berry and dot clusters. Background motifs
     sit behind the people (mask), a few foreground blooms/vines at the bottom
     corners overlap them ("through the frame"). Motifs grow in over the first
     ~3 s (staggered, ease-out), then sway gently; petals boil slightly on twos.
  4. storybook faces: soft round pink blush on the cheeks.
"""
import json
import math
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
W, H = 1620, 1080
FACES = json.loads((HERE / "faces.json").read_text())

PAL = np.array([
    (248, 240, 226),  # cream
    (240, 226, 214),  # warm paper
    (244, 196, 194),  # blush
    (236, 150, 158),  # rose pink
    (238, 126, 104),  # coral
    (247, 192, 152),  # peach
    (232, 186, 82),   # mustard
    (246, 222, 146),  # butter
    (166, 192, 152),  # sage
    (100, 150, 112),  # leaf green
    (66, 132, 134),   # teal
    (194, 222, 208),  # mint
    (172, 206, 230),  # sky
    (138, 158, 212),  # periwinkle
    (204, 184, 226),  # lavender
    (198, 112, 82),   # terracotta
    (140, 88, 64),    # cocoa
    (98, 70, 66),     # dark cocoa
    (48, 52, 78),     # navy ink
    (246, 204, 176),  # skin light
    (232, 168, 134),  # skin mid
    (204, 132, 102),  # skin deep
], np.float32)


def lab(rgb):
    a = np.clip(rgb, 0, 255).astype(np.uint8).reshape(-1, 1, 3)
    return cv2.cvtColor(a, cv2.COLOR_RGB2LAB).reshape(-1, 3).astype(np.float32)


PAL_LAB = lab(PAL)
WAB = np.array([1.0, 1.6, 1.6], np.float32)   # prefer hue matches


def flat_labels(frame, mask, n):
    s = 2
    small = cv2.resize(frame, (W // 3, H // 3), interpolation=cv2.INTER_AREA)
    small = cv2.pyrMeanShiftFiltering(small, 6, 22)
    small = cv2.resize(small, (W // s, H // s), interpolation=cv2.INTER_CUBIC)
    small = cv2.bilateralFilter(small, 9, 35, 7).astype(np.float32)
    ms = cv2.resize(mask, (W // s, H // s), interpolation=cv2.INTER_AREA)[..., None]
    L = lab(small).reshape(H // s, W // s, 3)
    # flatten shading ("no harsh shadows"): divide out half of the large-scale light
    illum = cv2.GaussianBlur(L[..., 0], (0, 0), 22)
    L[..., 0] = np.clip(L[..., 0] * (np.mean(illum) / np.maximum(illum, 20)) ** (0.5 + 0.3 * ms[..., 0]), 0, 255)
    # pastel lift: lighter, more chroma; the room goes extra pastel
    L[..., 0] = L[..., 0] * 0.72 + 255 * 0.26
    L[..., 1:] = (L[..., 1:] - 128) * (1.35 + 0.9 * (1 - ms)) + 128
    flat = L.reshape(-1, 3)
    d = (((flat[:, None, :] - PAL_LAB[None]) * WAB) ** 2).sum(-1)
    idx = d.argmin(1).reshape(H // s, W // s)
    # smooth shapes: blurred one-hot argmax, with a noise domain warp for painted edges
    rng = np.random.default_rng(1000 + n // 2)
    nx = cv2.GaussianBlur(rng.normal(0, 1, (H // s, W // s)).astype(np.float32), (0, 0), 6) * 22
    ny = cv2.GaussianBlur(rng.normal(0, 1, (H // s, W // s)).astype(np.float32), (0, 0), 6) * 22
    gy, gx = np.mgrid[0:H // s, 0:W // s].astype(np.float32)
    idx = cv2.remap(idx.astype(np.float32), gx + nx, gy + ny, cv2.INTER_NEAREST,
                    borderMode=cv2.BORDER_REPLICATE).astype(np.int64)
    best = np.full(idx.shape, -1.0, np.float32)
    out = np.zeros_like(idx)
    for k in np.unique(idx):
        sc = cv2.GaussianBlur((idx == k).astype(np.float32), (0, 0), 3.2)
        upd = sc > best
        out[upd] = k
        best[upd] = sc[upd]
    return cv2.resize(out.astype(np.uint8), (W, H), interpolation=cv2.INTER_NEAREST)


def gouache(idx, n):
    col = PAL[idx]
    rng = np.random.default_rng(n // 2)
    # value mottling within flats (opaque gouache is never perfectly even)
    mott = cv2.GaussianBlur(rng.normal(0, 1, (H // 8, W // 8)).astype(np.float32), (0, 0), 2)
    mott = cv2.resize(mott, (W, H), interpolation=cv2.INTER_CUBIC)
    # dry-brush streaks (directional noise, mostly horizontal)
    st = rng.normal(0, 1, (H // 2, W // 2)).astype(np.float32)
    st = cv2.GaussianBlur(st, (0, 0), sigmaX=14, sigmaY=1.2)
    st = cv2.resize(st, (W, H), interpolation=cv2.INTER_LINEAR)
    col = col * (1 + 0.035 * mott[..., None] + 0.05 * st[..., None])
    return col


def paper_grain(n):
    rng = np.random.default_rng(77)   # fixed paper tooth
    g = rng.normal(0, 1, (H, W)).astype(np.float32)
    g = cv2.GaussianBlur(g, (0, 0), 0.8) * 0.6 + cv2.GaussianBlur(g, (0, 0), 2.5) * 1.4
    fresh = np.random.default_rng(n).normal(0, 1, (H, W)).astype(np.float32) * 0.35
    return g + fresh


# ---------------------------------------------------------------- motifs ----

BLOOM = [(236, 150, 158), (238, 126, 104), (232, 186, 82), (138, 158, 212), (204, 184, 226),
         (244, 196, 194), (198, 112, 82), (247, 192, 152)]
LEAF = [(100, 150, 112), (66, 132, 134), (166, 192, 152), (122, 150, 96)]
CREAM = (250, 242, 228)
INK = (48, 52, 78)


def ellipse_poly(cx, cy, a, b, rot, n=28):
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    x, y = a * np.cos(t), b * np.sin(t)
    c, s = math.cos(rot), math.sin(rot)
    return [(cx + x[i] * c - y[i] * s, cy + x[i] * s + y[i] * c) for i in range(n)]


def leaf_poly(x0, y0, ang, L, wdt):
    pts = []
    for t in np.linspace(0, 1, 12):
        pts.append((t * L, math.sin(math.pi * t) * wdt))
    for t in np.linspace(1, 0, 12):
        pts.append((t * L, -math.sin(math.pi * t) * wdt))
    c, s = math.cos(ang), math.sin(ang)
    return [(x0 + x * c - y * s, y0 + x * s + y * c) for x, y in pts]


def draw_bloom(d, cx, cy, r, rot, col, jit, rng):
    k = int(rng.integers(6, 10))
    for i in range(k):
        a = rot + i * 2 * np.pi / k + jit[i % len(jit)]
        px, py = cx + math.cos(a) * r * 0.55, cy + math.sin(a) * r * 0.55
        d.polygon(ellipse_poly(px, py, r * 0.55, r * 0.30, a), fill=col)
    inner = BLOOM[(BLOOM.index(col) + 3) % len(BLOOM)]
    d.ellipse([cx - r * 0.42, cy - r * 0.42, cx + r * 0.42, cy + r * 0.42], fill=inner)
    d.ellipse([cx - r * 0.2, cy - r * 0.2, cx + r * 0.2, cy + r * 0.2], fill=INK if rng.random() < 0.4 else (232, 186, 82))
    for i in range(10):                        # folk dot ring
        a = rot + i * 2 * np.pi / 10
        x, y = cx + math.cos(a) * r * 0.31, cy + math.sin(a) * r * 0.31
        q = max(1.5, r * 0.035)
        d.ellipse([x - q, y - q, x + q, y + q], fill=CREAM)
    for i in range(k):                         # petal veins
        a = rot + i * 2 * np.pi / k + jit[i % len(jit)]
        x1, y1 = cx + math.cos(a) * r * 0.6, cy + math.sin(a) * r * 0.6
        x2, y2 = cx + math.cos(a) * r * 0.88, cy + math.sin(a) * r * 0.88
        d.line([(x1, y1), (x2, y2)], fill=CREAM, width=max(1, int(r * 0.03)))


def draw_daisy(d, cx, cy, r, rot, jit):
    for i in range(12):
        a = rot + i * np.pi / 6 + jit[i % len(jit)] * 0.5
        px, py = cx + math.cos(a) * r * 0.55, cy + math.sin(a) * r * 0.55
        d.polygon(ellipse_poly(px, py, r * 0.5, r * 0.15, a), fill=CREAM)
    d.ellipse([cx - r * 0.25, cy - r * 0.25, cx + r * 0.25, cy + r * 0.25], fill=(232, 186, 82))


def draw_tulip(d, x, y, r, rot, col):
    c, s = math.cos(rot), math.sin(rot)
    P = lambda u, v: (x + u * c - v * s, y + u * s + v * c)
    d.line([P(0, 0), P(0, r * 1.6)], fill=LEAF[0], width=max(2, int(r * 0.12)))
    d.polygon(leaf_poly(*P(0, r * 1.3), rot + math.pi * 1.25, r * 0.9, r * 0.22), fill=LEAF[2])
    d.polygon([P(-r * 0.5, 0), P(-r * 0.55, -r * 0.7), P(-r * 0.2, -r * 0.35), P(0, -r * 0.85),
               P(r * 0.2, -r * 0.35), P(r * 0.55, -r * 0.7), P(r * 0.5, 0), P(0, r * 0.35)], fill=col)


def draw_sprig(d, x, y, L, ang, col, rng, sway):
    pts = []
    for t in np.linspace(0, 1, 18):
        a = ang + sway * t + 0.35 * math.sin(t * 3 + x * 0.01)
        if not pts:
            pts.append((x, y))
        else:
            px, py = pts[-1]
            pts.append((px + math.cos(a) * L / 17, py + math.sin(a) * L / 17))
    d.line(pts, fill=col, width=max(2, int(L * 0.018)), joint="curve")
    for i in range(2, 18, 2):
        px, py = pts[i]
        a = ang + sway * i / 17
        side = 1 if i % 4 == 0 else -1
        d.polygon(leaf_poly(px, py, a + side * 0.9, L * 0.16, L * 0.05), fill=LEAF[int(rng.integers(0, 4))])
    return pts[-1]


def layout():
    rng = np.random.default_rng(2026)
    items = []
    # vines climbing the left and right edges and along the bottom (behind)
    for i in range(7):
        x = rng.uniform(0, 110) if i % 2 == 0 else rng.uniform(W - 110, W)
        items.append(dict(kind="vine", x=x, y=H + 20, L=rng.uniform(380, 720),
                          ang=-math.pi / 2 + (0.35 if x < W / 2 else -0.35) * rng.uniform(0.3, 1),
                          fg=False, born=rng.integers(0, 24)))
    # background blooms: dense near edges / top band, sparser toward centre
    tries = 0
    while len(items) < 125 and tries < 6000:
        tries += 1
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        edge = min(x, W - x, y * 1.6, (H - y) * 1.2) / (W / 2)
        if rng.random() < edge * 1.15:
            continue
        r = rng.uniform(24, 66) * (1.25 - 0.5 * edge)
        if any(math.hypot(x - it["x"], y - it["y"]) < (r + it.get("r", 30)) * 0.8 for it in items if it["kind"] != "vine"):
            continue
        kind = rng.choice(["bloom", "bloom", "daisy", "tulip", "sprig", "dots"])
        items.append(dict(kind=kind, x=x, y=y, r=r, rot=rng.uniform(0, 6.28),
                          col=BLOOM[int(rng.integers(0, len(BLOOM)))], fg=False,
                          born=int(rng.integers(0, 34))))
    # foreground growth at the bottom corners, overlapping the people
    for x, y, r in [(70, 1030, 120), (230, 1075, 80), (1560, 1020, 125), (1390, 1070, 85), (820, 1110, 70)]:
        items.append(dict(kind="vine", x=x, y=H + 30, L=rng.uniform(260, 420),
                          ang=-math.pi / 2 + (0.5 if x < W / 2 else -0.5), fg=True, born=int(rng.integers(6, 30))))
        items.append(dict(kind="bloom", x=x, y=y, r=r, rot=rng.uniform(0, 6.28),
                          col=BLOOM[int(rng.integers(0, len(BLOOM)))], fg=True, born=int(rng.integers(8, 36))))
    return items


ITEMS = layout()


def draw_motifs(n, fg):
    S = 2
    im = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    jr = np.random.default_rng(5000 + n // 2)
    for i, it in enumerate(ITEMS):
        if it["fg"] != fg:
            continue
        g = np.clip((n - 1 - it["born"]) / 10.0, 0, 1)
        g = 1 - (1 - g) ** 3                       # ease-out growth
        if g <= 0:
            continue
        sway = 0.06 * math.sin(n * 0.18 + i * 1.7)
        rng = np.random.default_rng(i)
        jit = list(jr.normal(0, 0.05, 4))
        x, y = it["x"] * S, it["y"] * S
        if it["kind"] == "vine":
            end = draw_sprig(d, x, y, it["L"] * S * g, it["ang"], LEAF[i % 4], rng, sway * 2)
            if g > 0.8:
                r = 34 * S * (g - 0.8) / 0.2
                draw_bloom(d, end[0], end[1], r, sway, BLOOM[i % len(BLOOM)], jit, rng)
            continue
        r = it["r"] * S * g
        rot = it["rot"] + sway
        if it["kind"] == "bloom":
            for k in range(3):                    # leaves tucked under the bloom
                a = rot + k * 2.1
                d.polygon(leaf_poly(x, y, a, r * 1.35, r * 0.32), fill=LEAF[(i + k) % 4])
            draw_bloom(d, x, y, r, rot, it["col"], jit, rng)
        elif it["kind"] == "daisy":
            draw_daisy(d, x, y, r * 0.8, rot, jit)
        elif it["kind"] == "tulip":
            draw_tulip(d, x, y, r * 0.75, sway * 2 + (rot % 0.6 - 0.3), it["col"])
        elif it["kind"] == "sprig":
            draw_sprig(d, x, y + r, r * 2.4, -math.pi / 2 + (rot % 1.2 - 0.6), LEAF[i % 4], rng, sway * 3)
        elif it["kind"] == "dots":
            for k in range(7):
                a = rot + k * 0.9
                q = r * (0.12 + 0.05 * (k % 3))
                px, py = x + math.cos(a) * r * 0.6 * (k % 3 + 1) / 3, y + math.sin(a) * r * 0.6 * (k % 3 + 1) / 3
                d.ellipse([px - q, py - q, px + q, py + q], fill=it["col"] if k % 2 else (198, 112, 82))
    im = im.resize((W, H), Image.LANCZOS)
    a = np.asarray(im).astype(np.float32)
    return a[..., :3], a[..., 3:] / 255


def blush_layer(n):
    b = np.zeros((H, W), np.float32)
    for f in FACES.get(f"frame_{n:03d}.png", []):
        x, y, w, h = f["box"]
        for ek in ("leftEye", "rightEye"):
            if ek not in f:
                continue
            e = np.array(f[ek]).mean(0)
            side = 1 if e[0] > x + w / 2 else -1
            cx, cy = e[0] + side * w * 0.06, e[1] + h * 0.22
            cv2.ellipse(b, (int(cx), int(cy)), (int(w * 0.13), int(w * 0.09)), 0, 0, 360, 1.0, -1, cv2.LINE_AA)
    return cv2.GaussianBlur(b, (0, 0), 4)[..., None]


def render(frame, mask, n):
    idx = flat_labels(frame, mask, n)
    img = gouache(idx, n)
    m = cv2.GaussianBlur(mask, (0, 0), 1.0)
    m = np.clip((m - 0.5) * 4 + 0.5, 0, 1)[..., None]
    bc, ba = draw_motifs(n, False)
    ba = ba * (1 - m)                             # behind the people
    img = img * (1 - ba) + gouache_tint(bc, n) * ba
    bl = blush_layer(n) * 0.55
    img = img * (1 - bl) + bl * np.array([240, 140, 146])
    fc, fa = draw_motifs(n, True)
    img = img * (1 - fa) + gouache_tint(fc, n) * fa
    # matte paper finish
    img = img + paper_grain(n)[..., None] * 4.5
    img = img * 0.96 + 10
    return np.clip(img, 0, 255).astype(np.uint8)


def gouache_tint(c, n):
    rng = np.random.default_rng(9000 + n // 2)
    st = cv2.GaussianBlur(rng.normal(0, 1, (H // 2, W // 2)).astype(np.float32), (0, 0), sigmaX=6, sigmaY=6)
    st = cv2.resize(st, (W, H))
    return c * (1 + 0.06 * st[..., None])


def main():
    fdir, mdir, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    out.mkdir(parents=True, exist_ok=True)
    args = sys.argv[4:] or ["13", "49", "85", "109", "145", "178"]
    nums = list(range(1, 180)) if args == ["all"] else [int(a) for a in args]
    for n in nums:
        f = cv2.cvtColor(cv2.imread(str(fdir / f"frame_{n:03d}.png")), cv2.COLOR_BGR2RGB)
        m = cv2.imread(str(mdir / f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
        img = render(f, m, n)
        cv2.imwrite(str(out / f"frame_{n:03d}.png"), cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
        print(n, end=" ", flush=True)
    print()


if __name__ == "__main__":
    main()
