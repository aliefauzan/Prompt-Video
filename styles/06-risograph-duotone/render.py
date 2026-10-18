"""Two-ink risograph restyle (fluorescent pink + blue), frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [frame numbers...]

Each frame is separated into two spot-colour plates, screened with coarse
grainy halftone, printed with mottled soy-ink coverage, the pink drum
misregistered against the blue one, overprinted (multiply) on off-white
stock with a bare paper margin. Grain, screen phase and registration change
every frame so the animation boils.
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np

FRAMES, MASKS, OUT = sys.argv[1:4]
ONLY = [int(a) for a in sys.argv[4:]]
N = len([f for f in os.listdir(FRAMES) if f.endswith(".png")])

# ink transmittance, BGR 0..1  (Riso Fluorescent Pink #FF48B0, Riso Blue #0078BF)
PINK = np.array([176, 72, 255], np.float32) / 255
BLUE = np.array([191, 120, 0], np.float32) / 255
PAPER = np.array([0.90, 0.95, 0.965], np.float32)

# (first, last, background mode, pink registration offset)
SECTIONS = [
    (1, 30, "duo", (9, -5)),
    (31, 66, "pinkfield", (-8, 6)),
    (67, 100, "paper", (10, 4)),
    (101, 136, "duo", (-7, -8)),
    (137, 160, "pinkfield", (8, 7)),
    (161, 999, "paper", (-10, 3)),
]


def section_of(n):
    for i, s in enumerate(SECTIONS):
        if s[0] <= n <= s[1]:
            return i, s
    return len(SECTIONS) - 1, SECTIONS[-1]


def vnoise(rng, h, w, cell):
    a = rng.random((max(2, h // cell + 2), max(2, w // cell + 2))).astype(np.float32)
    return cv2.resize(a, (w, h), interpolation=cv2.INTER_CUBIC).clip(0, 1)


def grain(rng, h, w, sigma=0.7):
    return cv2.GaussianBlur(rng.normal(0, 1, (h, w)).astype(np.float32), (0, 0), sigma)


def screen(h, w, cell, angle, ox, oy):
    """Round-dot screen 0..1 (0 at dot centre)."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    a = np.radians(angle)
    u = (xx + ox) * np.cos(a) + (yy + oy) * np.sin(a)
    v = -(xx + ox) * np.sin(a) + (yy + oy) * np.cos(a)
    du = np.mod(u, cell) - cell / 2
    dv = np.mod(v, cell) - cell / 2
    return (np.sqrt(du * du + dv * dv) / (cell / np.sqrt(2))).clip(0, 1)


def print_plate(density, rng, angle, cell=7.0):
    """Density 0..1 -> ink coverage 0..1 with screen, grain, mottle, dropouts."""
    h, w = density.shape
    scr = screen(h, w, cell, angle, rng.uniform(0, cell), rng.uniform(0, cell))
    # riso screens are grainy: jitter the threshold with fine noise
    thr = scr * 0.8 + 0.2 * rng.random((h, w)).astype(np.float32) + grain(rng, h, w, 1.2) * 0.12
    cov = (density > thr).astype(np.float32)
    solid = np.clip((density - 0.82) / 0.12, 0, 1)        # heavy areas print as solid ink
    cov = np.maximum(cov, solid)
    cov = cv2.GaussianBlur(cov, (0, 0), 0.7)               # ink spread on uncoated stock
    mottle = 0.80 + 0.20 * vnoise(rng, h, w, 9) * (0.7 + 0.3 * vnoise(rng, h, w, 120))
    cov *= mottle
    cov *= 1 - 0.35 * np.clip(vnoise(rng, h, w, 180) - 0.62, 0, 1) * 2.5  # starved-drum patches
    drop = (rng.random((h, w)) < 0.0025) & (vnoise(rng, h, w, 40) > 0.45)   # clustered fibre dropouts
    cov[cv2.dilate(drop.astype(np.uint8), np.ones((3, 2), np.uint8)) > 0] *= 0.2
    return cov.clip(0, 1)


def shift(img, dx, dy, rot, h, w):
    M = cv2.getRotationMatrix2D((w / 2, h / 2), rot, 1.0)
    M[:, 2] += (dx, dy)
    return cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_CONSTANT, borderValue=0)


def read_mask(n):
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE)
    return cv2.GaussianBlur(m.astype(np.float32) / 255, (0, 0), 1.2)


def section_plan(si, sec, h, w):
    """Fixed graphic elements of a section (a big pink sun / block)."""
    rng = np.random.default_rng(700 + si * 17)
    mid = (sec[0] + min(sec[1], N)) // 2
    m = read_mask(mid) > 0.5
    ys, xs = np.nonzero(m)
    cx = float(np.median(xs)) if len(xs) else w / 2
    return dict(sun=(cx + rng.normal(0, w * 0.06), h * rng.uniform(0.30, 0.42), h * rng.uniform(0.34, 0.42)),
                stripe_y=h * rng.uniform(0.72, 0.84))


def render(n):
    si, sec = section_of(n)
    _, _, mode, (pdx, pdy) = sec
    rng = np.random.default_rng(20_000 + n)
    bgr = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png"))
    h, w = bgr.shape[:2]
    mask = read_mask(n)
    plan = section_plan(si, sec, h, w)

    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    L = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(gray).astype(np.float32) / 255
    L = cv2.GaussianBlur(L, (0, 0), 1.0)
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV).astype(np.float32)
    warm = ((hsv[..., 0] < 25) | (hsv[..., 0] > 160)).astype(np.float32) * (hsv[..., 1] / 255)

    # plate separation: blue = key / shadows, pink = mid-tones and warm colour
    db = np.clip((0.66 - L) / 0.56, 0, 1) ** 1.15
    dp = np.clip((0.95 - L) / 0.62, 0, 1) ** 0.85 * 0.78 + warm * 0.35
    dp = dp.clip(0, 1)

    # background treatment differs per section; the people always print in both inks
    if mode == "pinkfield":
        bg_p = np.full((h, w), 0.93, np.float32)
        bg_b = db * 0.55
    elif mode == "paper":
        bg_p = np.zeros((h, w), np.float32)
        cx, cy, r = plan["sun"]
        sun = np.zeros((h, w), np.uint8)
        cv2.circle(sun, (int(cx + rng.normal(0, 1)), int(cy + rng.normal(0, 1))), int(r), 255, -1, cv2.LINE_AA)
        bg_p = np.maximum(bg_p, sun.astype(np.float32) / 255 * 0.95)
        y0 = int(plan["stripe_y"])
        bg_p[y0:, :] = np.maximum(bg_p[y0:, :], 0.55)       # flat pink floor band
        bg_b = np.clip((0.55 - L) / 0.55, 0, 1) * 0.45         # light blue echo of the room
    else:
        bg_p = dp * 0.75
        bg_b = db * 0.85

    # pink offset silhouette (classic riso knock-out shadow) in paper mode
    m = mask
    if mode == "paper":
        ghost = shift(m, 16, 10, 0, h, w)
        bg_p = np.maximum(bg_p, ghost * 0.9)

    plate_p = bg_p * (1 - m) + dp * m
    plate_b = bg_b * (1 - m) + db * m
    if mode == "pinkfield":
        # knock the people out of the flat pink with a bare-paper trap gap so they read
        ring = cv2.dilate((m > 0.5).astype(np.uint8), np.ones((15, 15), np.uint8)).astype(np.float32)
        ring = cv2.GaussianBlur(ring, (0, 0), 1.5) - m
        plate_p = plate_p * (1 - ring.clip(0, 1)) * (1 - m) + (dp * 0.7) * m
        plate_b = plate_b * (1 - ring.clip(0, 1) * (1 - m))

    cov_p = print_plate(plate_p, rng, 15)
    cov_b = print_plate(plate_b, rng, 75)

    # misregistration: pink drum offset per section + per-frame wobble
    cov_p = shift(cov_p, pdx + rng.normal(0, 1.3), pdy + rng.normal(0, 1.3), rng.normal(0, 0.08), h, w)
    cov_b = shift(cov_b, rng.normal(0, 0.8), rng.normal(0, 0.8), rng.normal(0, 0.04), h, w)

    # paper stock
    paper = PAPER[None, None, :] * (0.97 + grain(rng, h, w, 0.8)[..., None] * 0.02
                                    - np.clip(vnoise(rng, h, w, 200) - 0.6, 0, 1)[..., None] * 0.08)
    # bare paper margin with slightly uneven ink edge (no full bleed on a riso)
    mx = 26 + int(rng.normal(0, 1))
    edge = np.zeros((h, w), np.float32)
    edge[mx:h - mx, mx:w - mx] = 1
    edge = cv2.GaussianBlur(edge, (0, 0), 1.5) * (0.9 + 0.1 * vnoise(rng, h, w, 15))
    edge = (edge > 0.5).astype(np.float32)
    cov_p *= edge
    cov_b *= edge

    img = paper * (1 - cov_p[..., None] * (1 - PINK)) * (1 - cov_b[..., None] * (1 - BLUE))

    # scan: tiny dust, ink smudge specks, grain
    sp = rng.random((h, w))
    img[sp < 0.0004] *= 0.55
    img += grain(rng, h, w, 0.9)[..., None] * 0.012
    out = (img.clip(0, 1) * 255).astype(np.uint8)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), out)
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    todo = ONLY or list(range(1, N + 1))
    with Pool(min(8, os.cpu_count() or 4)) as pool:
        for n in pool.imap_unordered(render, todo):
            print(n, end=" ", flush=True)
    print()
