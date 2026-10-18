"""Instant-film photo-dump restyle, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [frame numbers...]
Each video frame becomes a fresh landscape instant print (Instax-Wide proportions,
so the whole composition survives) lying on a table or pinned to a corkboard,
with earlier prints piled underneath. The top print is re-dropped every frame:
small shuffle in angle/position, new glare, new grain, new chemistry.
The masks are not needed: the person stays fully photographic inside the print.
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np

FRAMES, MASKS, OUT = sys.argv[1:4]
ONLY = [int(a) for a in sys.argv[4:]]
N = len([f for f in os.listdir(FRAMES) if f.endswith(".png")])

W, H = 1620, 1080
# Instax Wide card 108 x 86 mm, image 99 x 62 mm
CARD_MM, IMG_MM, TOP_MM, SIDE_MM = (108, 86), (99, 62), 6.5, 4.5
CARD_BORDER = np.array([0.93, 0.945, 0.95], np.float32)       # BGR warm white plastic

# (first, last, surface, caption, base angle deg, ink colour BGR)
SECTIONS = [
    (1, 30, "wood", "office crew", -2.5, (0.12, 0.10, 0.10)),
    (31, 66, "cork", "tues 4pm :)", 2.0, (0.55, 0.25, 0.12)),
    (67, 100, "linen", "the trio", -1.2, (0.12, 0.10, 0.10)),
    (101, 140, "wood", "say hi!!", 3.0, (0.20, 0.12, 0.62)),
    (141, 999, "cork", "core memory", -2.8, (0.12, 0.10, 0.10)),
]


def vnoise(rng, h, w, cell):
    a = rng.random((max(2, h // cell + 2), max(2, w // cell + 2))).astype(np.float32)
    return cv2.resize(a, (w, h), interpolation=cv2.INTER_CUBIC).clip(0, 1)


def section_of(n):
    for i, s in enumerate(SECTIONS):
        if s[0] <= n <= s[1]:
            return i, s
    return len(SECTIONS) - 1, SECTIONS[-1]


# ---------------------------------------------------------------- surfaces
def wood(rng):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    warpn = vnoise(rng, H, W, 180) * 60 + vnoise(rng, H, W, 40) * 8
    grain = np.sin((yy * 0.9 + warpn) * 0.11) * 0.5 + 0.5
    fine = np.sin((yy + warpn * 1.7) * 0.6 + xx * 0.004) * 0.5 + 0.5
    t = 0.55 + 0.25 * grain + 0.08 * fine + (vnoise(rng, H, W, 300) - 0.5) * 0.25
    planks = np.zeros((H, W), np.float32)
    for y in range(int(rng.uniform(80, 200)), H, int(rng.uniform(260, 320))):
        planks[max(0, y - 2):y + 2] = 1
    t *= 1 - cv2.GaussianBlur(planks, (0, 0), 1.5) * 0.6
    base = np.array([0.13, 0.24, 0.40], np.float32)             # walnut, BGR
    return base * (0.6 + 0.7 * t[..., None])


def cork(rng):
    t = 0.75 + (vnoise(rng, H, W, 200) - 0.5) * 0.15
    img = np.array([0.38, 0.58, 0.76], np.float32) * t[..., None]
    for k, (cnt, rmax, col) in enumerate([(9000, 3, (0.20, 0.33, 0.48)), (4000, 2, (0.55, 0.72, 0.86)),
                                         (900, 5, (0.25, 0.40, 0.56))]):
        layer = np.zeros((H, W), np.float32)
        xs, ys = rng.integers(0, W, cnt), rng.integers(0, H, cnt)
        rs = rng.integers(1, rmax + 1, cnt)
        for x, y, r in zip(xs, ys, rs):
            cv2.circle(layer, (int(x), int(y)), int(r), 1.0, -1)
        layer = cv2.GaussianBlur(layer, (0, 0), 0.7) * 0.7
        img = img * (1 - layer[..., None]) + np.array(col, np.float32) * layer[..., None]
    return img


def linen(rng):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    weave = (np.sin(xx * 1.9) * np.sin(yy * 1.7)) * 0.03 + (vnoise(rng, H, W, 3) - 0.5) * 0.05
    folds = (vnoise(rng, H, W, 260) - 0.5) * 0.22 + (vnoise(rng, H, W, 90) - 0.5) * 0.06
    t = 0.86 + weave + folds
    return np.array([0.84, 0.88, 0.90], np.float32) * t[..., None]


SURF = {"wood": wood, "cork": cork, "linen": linen}


# ---------------------------------------------------------------- film
def instant_film(bgr, rng):
    """Faded instant-film chemistry: lifted blacks, soft, warm highs, cyan lows."""
    img = bgr.astype(np.float32) / 255
    img = cv2.GaussianBlur(img, (0, 0), 1.1)
    lum = img.mean(2, keepdims=True)
    img = lum + (img - lum) * 0.72                              # a little desaturated
    img = 0.11 + img * 0.80                                      # milky blacks, soft whites
    img = img ** np.array([1.06, 0.97, 0.88], np.float32)        # warm highlights
    shadow = np.clip(0.55 - lum, 0, 1)
    img += shadow * np.array([0.07, 0.06, -0.03], np.float32)  # teal shadows
    h, w = img.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    img *= (1 - 0.28 * np.clip(r - 0.45, 0, 1) ** 1.4)[..., None]
    bloom = cv2.GaussianBlur(np.clip(img - 0.75, 0, 1), (0, 0), 18)
    img += bloom * 0.6
    # chemical development: uneven density from the rollers + edge stains
    dev = vnoise(rng, h, w, 160)
    img += ((dev - 0.5) * 0.06)[..., None]
    edge = np.clip(1 - np.minimum.reduce([xx, w - xx, yy, h - yy]) / 26, 0, 1)
    stain = edge * (vnoise(rng, h, w, 30) > 0.5)
    img = img * (1 - stain[..., None] * 0.35) + stain[..., None] * np.array([0.30, 0.55, 0.75]) * 0.35
    img += cv2.GaussianBlur(rng.normal(0, 1, (h, w, 3)).astype(np.float32), (0, 0), 0.9) * 0.022
    return img.clip(0, 1)


def scribble_text(canvas, text, x, y, scale, th, rng, col):
    """Sharpie handwriting, letter by letter, uneven size and baseline."""
    cx = x
    for ch in text:
        sc = scale * rng.uniform(0.85, 1.12)
        cy = y + int(rng.normal(0, 3))
        cv2.putText(canvas, ch, (cx, cy), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, sc, col,
                    max(2, th + int(rng.integers(-1, 2))), cv2.LINE_AA)
        (tw, _), _ = cv2.getTextSize(ch, cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, sc, th)
        cx += int(tw * rng.uniform(0.82, 0.98))
    return cx


def heart(canvas, x, y, s, th, col):
    t = np.linspace(0, 2 * np.pi, 80)
    px = x + s * 16 * np.sin(t) ** 3 / 16
    py = y - s * (13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)) / 16
    cv2.polylines(canvas, [np.stack([px, py], 1).astype(np.int32)], False, col, th, cv2.LINE_AA)


def make_card(frame_bgr, px_per_mm, rng, caption, ink, n):
    cw, ch = int(CARD_MM[0] * px_per_mm), int(CARD_MM[1] * px_per_mm)
    iw, ih = int(IMG_MM[0] * px_per_mm), int(IMG_MM[1] * px_per_mm)
    ox, oy = int(SIDE_MM * px_per_mm), int(TOP_MM * px_per_mm)
    fh, fw = frame_bgr.shape[:2]
    crop_h = int(fw * ih / iw)
    y0 = (fh - crop_h) // 2
    photo = cv2.resize(frame_bgr[y0:y0 + crop_h], (iw, ih), interpolation=cv2.INTER_AREA)
    photo = instant_film(photo, rng)
    tex = 0.97 + (vnoise(rng, ch, cw, 4) - 0.5) * 0.03 + (vnoise(rng, ch, cw, 120) - 0.5) * 0.04
    card = CARD_BORDER * tex[..., None]
    card[oy:oy + ih, ox:ox + iw] = photo
    # recessed window: thin shadow line around the image
    rim = np.zeros((ch, cw), np.float32)
    cv2.rectangle(rim, (ox - 1, oy - 1), (ox + iw, oy + ih), 1.0, 2)
    card *= (1 - cv2.GaussianBlur(rim, (0, 0), 1.2) * 0.25)[..., None]
    if caption:
        lay = np.zeros((ch, cw), np.uint8)
        r = np.random.default_rng(n)                                  # handwriting jitters per print
        base_y = oy + ih + int((CARD_MM[1] - IMG_MM[1] - TOP_MM) * px_per_mm * 0.68)
        sc = px_per_mm * 0.19
        end = scribble_text(lay, caption, ox + int(cw * 0.06), base_y, sc, max(2, int(px_per_mm * 0.42)), r, 255)
        heart(lay, end + int(px_per_mm * 5), base_y - int(px_per_mm * 3), px_per_mm * 4.2, max(2, int(px_per_mm * 0.38)), 255)
        scribble_text(lay, "10.18", cw - int(px_per_mm * 30), base_y, sc * 0.6, max(2, int(px_per_mm * 0.3)), r, 255)
        M = cv2.getRotationMatrix2D((cw / 2, base_y), r.normal(0, 1.2), 1.0)
        lay = cv2.warpAffine(lay, M, (cw, ch)).astype(np.float32) / 255
        lay *= 0.85 + 0.15 * (rng.random((ch, cw)) > 0.2)
        card = card * (1 - lay[..., None]) + np.array(ink, np.float32) * lay[..., None]
    # fingerprints / scuffs on the plastic
    card *= (1 - np.clip(vnoise(rng, ch, cw, 50) - 0.82, 0, 1) * 0.3)[..., None]
    return card


def place(canvas, card, cx, cy, ang, keystone, rng, shadow=0.55, sheen=True):
    ch, cw = card.shape[:2]
    src = np.float32([[0, 0], [cw, 0], [cw, ch], [0, ch]])
    c, s = np.cos(np.radians(ang)), np.sin(np.radians(ang))
    pts = []
    for (x, y), k in zip(src, rng.normal(0, keystone, (4, 2))):
        x0, y0 = x - cw / 2, y - ch / 2
        pts.append([cx + x0 * c - y0 * s + k[0], cy + x0 * s + y0 * c + k[1]])
    dst = np.float32(pts)
    P = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(card, P, (W, H), flags=cv2.INTER_LINEAR)
    a = cv2.warpPerspective(np.ones((ch, cw), np.float32), P, (W, H), flags=cv2.INTER_LINEAR)
    sh = cv2.GaussianBlur(np.roll(a, (14, 9), (0, 1)), (0, 0), 12) * shadow
    canvas = canvas * (1 - sh[..., None])
    if sheen:                                                     # glossy print catches the lamp
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        band = np.exp(-((xx * 0.6 + yy - rng.uniform(300, 1300)) / rng.uniform(140, 260)) ** 2) * rng.uniform(0.04, 0.1)
        warped = warped + band[..., None] * a[..., None]
    return canvas * (1 - a[..., None]) + warped * a[..., None]


def light(img, rng):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    lx, ly = W * 0.25, -H * 0.2
    d = np.sqrt((xx - lx) ** 2 + (yy - ly) ** 2) / (W * 1.3)
    return img * (1.12 - 0.45 * d)[..., None]


def load(n):
    return cv2.imread(os.path.join(FRAMES, f"frame_{max(1, min(N, n)):03d}.png"))


def render(n):
    si, (first, last, surf, caption, base_ang, ink) = section_of(n)
    srng = np.random.default_rng(2000 + si)
    rng = np.random.default_rng(20_000 + n)
    canvas = SURF[surf](np.random.default_rng(2100 + si))

    # the pile: earlier prints from the clip, fixed for the section
    for k in range(4):
        src_n = max(1, first - 8 - k * 17 - int(srng.integers(0, 6)))
        card = make_card(load(src_n), 6.2, np.random.default_rng(src_n), None, ink, src_n)
        cx = srng.choice([srng.uniform(0.02, 0.22), srng.uniform(0.78, 0.98)]) * W
        cy = srng.uniform(0.1, 0.9) * H
        canvas = place(canvas, card, cx + rng.normal(0, 0.6), cy + rng.normal(0, 0.6),
                       srng.uniform(-28, 28), 2, np.random.default_rng(src_n), 0.45, False)

    # the hero print: this frame
    ppm = 11.0
    card = make_card(load(n), ppm, rng, caption, ink, n)
    ang = base_ang + rng.normal(0, 0.7)
    cx = W / 2 + srng.normal(0, 18) + rng.normal(0, 6)
    cy = H / 2 + 8 + srng.normal(0, 10) + rng.normal(0, 5)
    canvas = place(canvas, card, cx, cy, ang, 5, rng)

    # props: tape on wood/linen, push pins on cork
    if surf == "cork":
        for px, py in ((cx - 520, cy - 440), (cx + 500, cy - 430)):
            px, py = int(px + srng.normal(0, 10)), int(py + srng.normal(0, 8))
            pin = np.array([(0.20, 0.25, 0.85), (0.80, 0.55, 0.20)][int(srng.integers(0, 2))], np.float32)
            sh = np.zeros((H, W), np.float32)
            cv2.circle(sh, (px + 12, py + 14), 22, 1.0, -1)
            canvas *= (1 - cv2.GaussianBlur(sh, (0, 0), 6) * 0.45)[..., None]
            cv2.circle(canvas, (px, py), 20, tuple(float(v) for v in pin), -1, cv2.LINE_AA)
            cv2.circle(canvas, (px - 6, py - 7), 6, tuple(float(v) for v in np.minimum(pin + 0.35, 1)), -1, cv2.LINE_AA)
    else:
        for side in (-1, 1):
            tw, th = 190, 54
            tape = np.zeros((H, W), np.float32)
            tx, ty = cx + side * 560 + srng.normal(0, 8), cy - 450 + srng.normal(0, 8)
            box = cv2.boxPoints(((tx, ty), (tw, th), side * 38 + srng.normal(0, 6)))
            cv2.fillPoly(tape, [box.astype(np.int32)], 1.0, cv2.LINE_AA)
            tape *= 0.55 + 0.1 * vnoise(rng, H, W, 8)
            col = np.array([0.70, 0.80, 0.95], np.float32) if side < 0 else np.array([0.80, 0.90, 0.80], np.float32)
            canvas = canvas * (1 - tape[..., None]) + col * tape[..., None]

    canvas = light(canvas, rng)
    canvas += cv2.GaussianBlur(rng.normal(0, 1, (H, W)).astype(np.float32), (0, 0), 0.8)[..., None] * 0.012
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), (canvas.clip(0, 1) * 255).astype(np.uint8))
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    todo = ONLY or list(range(1, N + 1))
    with Pool(min(6, os.cpu_count() or 2)) as p:
        for n in p.imap_unordered(render, todo):
            print(n, end=" ", flush=True)
    print()
