"""Impasto oil painting restyle, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [all | frame numbers...]

Every frame is repainted with brush strokes on a primed canvas:
  1. a warm/cool painterly grade of the source (lights warmer, shadows cooler)
  2. three stroke layers (big -> small). Strokes follow the image structure
     (structure-tensor orientation); smaller brushes only go where the canvas
     still differs from the source (Hertzmann-style), and people get finer
     brushes so faces stay readable
  3. a few palette-knife swipes in the background
  4. a height map built stroke by stroke (paint ridges + bristle grooves),
     relit with a raking light -> thick impasto relief, specular glints
  5. canvas weave showing where the paint is thin
Strokes on people are re-laid every frame; background strokes are re-laid
every 3 frames with small jitter in between, so the painting "boils" like
painted animation without the static room flickering hard.
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np

FRAMES, MASKS, OUT = sys.argv[1:4]
ARGS = sys.argv[4:]
H, W = 1080, 1620


def frame_list():
    if not ARGS or ARGS == ["all"]:
        return list(range(1, 180))
    return [int(a) for a in ARGS]


def orientation(gray):
    g = cv2.GaussianBlur(gray, (0, 0), 2.0)
    gx = cv2.Sobel(g, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(g, cv2.CV_32F, 0, 1, ksize=3)
    jxx = cv2.GaussianBlur(gx * gx, (0, 0), 7)
    jyy = cv2.GaussianBlur(gy * gy, (0, 0), 7)
    jxy = cv2.GaussianBlur(gx * gy, (0, 0), 7)
    theta = 0.5 * np.arctan2(2 * jxy, jxx - jyy) + np.pi / 2   # along edges
    coher = np.sqrt((jxx - jyy) ** 2 + 4 * jxy ** 2) / (jxx + jyy + 1e-3)
    return theta.astype(np.float32), coher.astype(np.float32)


def grade(bgr):
    """Painterly colour: richer saturation, warm lights, cool shadows."""
    f = bgr.astype(np.float32) / 255
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
    hsv[..., 1] = np.clip(hsv[..., 1] * 1.55 + 0.05, 0, 1)
    f = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    lum = f.mean(axis=2, keepdims=True)
    warm = np.array([0.80, 0.95, 1.10], np.float32)   # BGR multipliers
    cool = np.array([1.22, 0.96, 0.86], np.float32)
    t = np.clip((lum - 0.12) / 0.4, 0, 1)
    f = f * (cool * (1 - t) + warm * t)
    f = np.clip((f - 0.5) * 1.05 + 0.5, 0, 1)            # gentle chiaroscuro
    f = f ** 0.8                                           # luminous, lifted mids
    return (f * 255).astype(np.uint8)


def weave(h, w):
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    a = np.sin(x * 2 * np.pi / 5.0) * np.sin(y * 2 * np.pi / 5.0 + np.pi / 2)
    b = np.sin(y * 2 * np.pi / 5.0) * 0.5
    return (0.6 * a + 0.4 * b).astype(np.float32)


WEAVE = weave(H, W)
GROUND = None


def ground(rng):
    base = np.full((H, W, 3), (205, 222, 236), np.float32)   # warm primed canvas
    n = cv2.resize(rng.random((H // 24, W // 24)).astype(np.float32), (W, H))
    return np.clip(base * (0.93 + 0.1 * n[..., None]), 0, 255).astype(np.uint8)


def paint_layer(canvas, height, ref, theta, rng, r, spacing, mask_sel, length,
                bristles=True, hscale=1.0, cjit=1.0):
    h, w = ref.shape[:2]
    ys = np.arange(spacing // 2, h, spacing)
    xs = np.arange(spacing // 2, w, spacing)
    gy, gx = np.meshgrid(ys, xs, indexing="ij")
    pts = np.stack([gy.ravel(), gx.ravel()], 1).astype(np.float32)
    pts += rng.uniform(-spacing / 2, spacing / 2, pts.shape)
    pts[:, 0] = np.clip(pts[:, 0], 0, h - 1)
    pts[:, 1] = np.clip(pts[:, 1], 0, w - 1)
    iy, ix = pts[:, 0].astype(int), pts[:, 1].astype(int)
    keep = mask_sel[iy, ix]
    pts, iy, ix = pts[keep], iy[keep], ix[keep]
    order = rng.permutation(len(pts))
    pts, iy, ix = pts[order], iy[order], ix[order]
    cols = ref[iy, ix].astype(np.float32)
    # pigment variation: brightness + slight hue wobble per stroke
    cols *= rng.uniform(1 - 0.08 * cjit, 1 + 0.08 * cjit, (len(cols), 1))
    cols += rng.normal(0, 6 * cjit, cols.shape)
    cols = np.clip(cols, 0, 255)
    ang = theta[iy, ix] + rng.normal(0, 0.18, len(iy))
    ln = length * rng.uniform(0.6, 1.3, len(iy))
    hv = rng.uniform(0.55, 1.0, len(iy)) * hscale
    for k in range(len(iy)):
        cy, cx = pts[k]
        dx, dy = np.cos(ang[k]) * ln[k] / 2, np.sin(ang[k]) * ln[k] / 2
        p1 = (int(cx - dx), int(cy - dy))
        p2 = (int(cx + dx), int(cy + dy))
        rr = max(1, int(r * rng.uniform(0.8, 1.15)))
        c = tuple(float(v) for v in cols[k])
        cv2.line(canvas, p1, p2, c, rr * 2, cv2.LINE_AA)
        cv2.line(height, p1, p2, float(hv[k]), rr * 2, cv2.LINE_8)
        if bristles and rr >= 3:
            # bristle grooves: thin parallel lines across the stroke width, in the
            # height map (relief) and a few in colour (unmixed pigment streaks)
            nx, ny = -np.sin(ang[k]), np.cos(ang[k])
            nb = max(2, int(rr * 0.8))
            for o in np.linspace(-rr * 0.85, rr * 0.85, nb):
                o += rng.uniform(-0.6, 0.6)
                t0, t1 = rng.uniform(0, 0.15), rng.uniform(0.85, 1.0)
                q1 = (int(p1[0] + (p2[0] - p1[0]) * t0 + nx * o), int(p1[1] + (p2[1] - p1[1]) * t0 + ny * o))
                q2 = (int(p1[0] + (p2[0] - p1[0]) * t1 + nx * o), int(p1[1] + (p2[1] - p1[1]) * t1 + ny * o))
                cv2.line(height, q1, q2, float(hv[k] + rng.uniform(-0.18, 0.12)), 1, cv2.LINE_8)
                if rng.random() < 0.25:
                    shade = tuple(float(np.clip(v * rng.uniform(0.88, 1.12), 0, 255)) for v in cols[k])
                    cv2.line(canvas, q1, q2, shade, 1, cv2.LINE_AA)


def knife_swipes(canvas, height, ref, mask, rng):
    """Flat palette-knife slabs in the background: sharp edges, ridge at the end."""
    h, w = mask.shape
    for _ in range(26):
        cy, cx = rng.integers(0, h), rng.integers(0, w)
        if mask[cy, cx] > 0.2:
            continue
        L, T = rng.uniform(50, 120), rng.uniform(14, 30)
        a = rng.uniform(-0.6, 0.6) + (np.pi / 2 if rng.random() < 0.3 else 0)
        box = cv2.boxPoints(((float(cx), float(cy)), (L, T), np.degrees(a))).astype(np.int32)
        reg = np.zeros((h, w), np.uint8)
        cv2.fillConvexPoly(reg, box, 1)
        reg[mask > 0.2] = 0
        if reg.sum() < 200:
            continue
        col = ref[reg > 0].mean(axis=0) * rng.uniform(0.95, 1.08)
        canvas[reg > 0] = np.clip(col, 0, 255).astype(np.uint8)
        hv = rng.uniform(0.3, 0.6)
        height[reg > 0] = hv
        ex = (int(cx + np.cos(a) * L / 2), int(cy + np.sin(a) * L / 2))
        cv2.line(height, (int(ex[0] - np.sin(a) * T / 2), int(ex[1] + np.cos(a) * T / 2)),
                 (int(ex[0] + np.sin(a) * T / 2), int(ex[1] - np.cos(a) * T / 2)), hv + 0.6, 3)


def dabs(canvas, height, mask, n):
    """Frameloop's 'scattered abstract colourful paint dabs' — fixed spots on the wall."""
    rng = np.random.default_rng(777)
    pal = [(70, 80, 220), (60, 170, 235), (170, 130, 60), (90, 160, 90), (150, 90, 200)]
    jit = np.random.default_rng(n // 3)
    for i in range(9):
        cy, cx = int(rng.uniform(40, 420)), int(rng.uniform(200, 1500))
        if mask[min(cy, H - 1), min(cx, W - 1)] > 0.2:
            continue
        r = int(rng.uniform(9, 17))
        cy += int(jit.normal(0, 1.2)); cx += int(jit.normal(0, 1.2))
        c = pal[i % len(pal)]
        cv2.ellipse(canvas, (cx, cy), (r, int(r * 0.8)), rng.uniform(0, 180), 0, 360, c, -1, cv2.LINE_AA)
        cv2.ellipse(height, (cx, cy), (r, int(r * 0.8)), 0, 0, 360, 1.1, -1)
        cv2.circle(height, (cx - r // 3, cy - r // 3), max(2, r // 3), 1.5, -1)


def lic(noise, theta, steps=11):
    """Smear noise along the brush direction -> bristle striations."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dx, dy = np.cos(theta), np.sin(theta)
    acc = noise.copy()
    for s in range(1, steps + 1):
        for sg in (-1, 1):
            acc += cv2.remap(noise, xx + sg * s * dx, yy + sg * s * dy, cv2.INTER_LINEAR,
                             borderMode=cv2.BORDER_REFLECT)
    return acc / (2 * steps + 1)


def relight(canvas, height):
    hh = height
    gx = cv2.Sobel(hh, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(hh, cv2.CV_32F, 0, 1, ksize=3)
    k = 1.1
    nx, ny, nz = -gx * k, -gy * k, np.ones_like(gx)
    nl = np.sqrt(nx * nx + ny * ny + nz * nz)
    nx, ny, nz = nx / nl, ny / nl, nz / nl
    L = np.array([-0.55, -0.6, 0.58]); L /= np.linalg.norm(L)
    diff = nx * L[0] + ny * L[1] + nz * L[2]
    shade = 1.0 + 0.9 * (diff - L[2])
    hv = L + np.array([0, 0, 1.0]); hv /= np.linalg.norm(hv)
    spec = np.clip(nx * hv[0] + ny * hv[1] + nz * hv[2], 0, 1) ** 30 * 0.22
    out = canvas.astype(np.float32) * shade[..., None] + 255 * spec[..., None]
    return out


def read_mask(n):
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE)
    return cv2.GaussianBlur(m.astype(np.float32) / 255, (0, 0), 2)


def render(n):
    src = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png"))
    mask = read_mask(n)
    ref = grade(src)
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY).astype(np.float32)
    theta, coher = orientation(gray)
    # low-coherence areas (flat wall) get a lazy diagonal brush direction
    lazy = 0.6 + 0.25 * np.sin(np.arange(W)[None, :] / 140.0 + np.arange(H)[:, None] / 210.0)
    theta = np.where(coher < 0.25, lazy.astype(np.float32), theta)

    bg_seed = 1000 + (n // 3) * 7
    rng_bg = np.random.default_rng(bg_seed)
    rng_fg = np.random.default_rng(50000 + n)
    rng_j = np.random.default_rng(90000 + n)

    canvas = ground(np.random.default_rng(5))
    height = np.zeros((H, W), np.float32)
    person = mask > 0.35
    anywhere = np.ones((H, W), bool)

    ref1 = cv2.GaussianBlur(ref, (0, 0), 9)
    ref2 = cv2.GaussianBlur(ref, (0, 0), 4)
    ref3 = cv2.GaussianBlur(ref, (0, 0), 1.6)

    # layer 1: big strokes everywhere (bg seed held 3 frames, people every frame)
    bgsel = ~person
    paint_layer(canvas, height, ref1, theta + rng_j.normal(0, 0.04), rng_bg, 13, 15, bgsel, 46)
    paint_layer(canvas, height, ref1, theta, rng_fg, 12, 15, person, 40)
    knife_swipes(canvas, height, ref1, mask, np.random.default_rng(bg_seed + 3))
    dabs(canvas, height, mask, n)

    # layer 2: medium where the canvas still differs from the source
    diff = np.abs(cv2.GaussianBlur(canvas, (0, 0), 3).astype(np.float32) - ref2.astype(np.float32)).sum(2)
    sel2 = (diff > 38) | person
    paint_layer(canvas, height, ref2, theta, rng_bg, 6, 8, sel2 & ~person, 24)
    paint_layer(canvas, height, ref2, theta, rng_fg, 6, 7, sel2 & person, 20, cjit=0.7)

    # layer 3: small strokes for detail, mostly faces / hands / edges
    diff = np.abs(cv2.GaussianBlur(canvas, (0, 0), 1.5).astype(np.float32) - ref3.astype(np.float32)).sum(2)
    sel3 = ((diff > 70) & ~person) | ((diff > 40) & person)
    paint_layer(canvas, height, ref3, theta, rng_fg, 4, 5, sel3, 13, hscale=0.85, cjit=0.4)

    # relief = soft paint lumps (stroke plateaus) + bristle striations along the
    # stroke direction; thin paint shows the canvas weave
    lumps = cv2.GaussianBlur(height, (0, 0), 1.2)
    noise = np.random.default_rng(70000 + n).random((H, W)).astype(np.float32)
    bris = lic(cv2.GaussianBlur(noise, (0, 0), 0.8), theta)
    bris = (bris - bris.mean()) / (bris.std() + 1e-6)
    cover = cv2.GaussianBlur(height, (0, 0), 3)
    height = 1.0 * lumps + 0.025 * bris + 0.10 * WEAVE * (1.2 - np.clip(cover, 0, 1))
    out = relight(canvas, height)
    # varnish warmth + slight vignette
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    vig = 1 - 0.10 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
    out *= vig[..., None]
    out = np.clip(out, 0, 255).astype(np.uint8)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), out)
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    nums = frame_list()
    with Pool(min(8, os.cpu_count() or 4)) as p:
        for n in p.imap_unordered(render, nums):
            print(n, end=" ", flush=True)
    print()
