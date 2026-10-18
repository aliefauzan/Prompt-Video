"""Y2K point-and-shoot digicam flash restyle, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [frame numbers... | all]
Default frames: the six sheet frames. The person mask decides where the
on-camera flash lands (people blown bright, room dark and cool behind them)
and casts the hard flash shadow.

Per frame: cool, underexposed ambient with slow-shutter ghosting
-> flash light on the people (falloff from the matte) -> hard drop shadow
-> blown highlight tone curve -> small-sensor noise -> oversharpening
-> purple fringing -> low-res JPEG (4:2:0) -> orange seven-segment date stamp.
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np

FRAMES, MASKS, OUT = sys.argv[1:4]
ARGS = sys.argv[4:]
N = len([f for f in os.listdir(FRAMES) if f.endswith(".png")])
SHEET = [13, 49, 85, 109, 145, 178]
SENSOR = (1152, 768)            # ~0.9 MP working size of the "camera"
ORANGE = (40, 150, 255)         # BGR date-stamp orange

# seven-segment layout: a b c d e f g
DIGITS = {
    "0": "abcdef", "1": "bc", "2": "abged", "3": "abgcd", "4": "fgbc",
    "5": "afgcd", "6": "afgedc", "7": "abc", "8": "abcdefg", "9": "abcdfg",
}


def load(n):
    n = min(max(n, 1), N)
    img = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png")).astype(np.float32) / 255
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), 0).astype(np.float32) / 255
    return img, m


def seg_polys(x, y, s, t):
    """Hexagon polygons for the seven segments of one digit at (x, y): width s, height 2s, thickness t."""
    h, g = t / 2, t * 0.25
    def hz(cx, cy):
        return np.array([(cx + g, cy), (cx + g + h, cy - h), (cx + s - g - h, cy - h),
                         (cx + s - g, cy), (cx + s - g - h, cy + h), (cx + g + h, cy + h)], np.float32)
    def vt(cx, cy):
        return np.array([(cx, cy + g), (cx + h, cy + g + h), (cx + h, cy + s - g - h),
                         (cx, cy + s - g), (cx - h, cy + s - g - h), (cx - h, cy + g + h)], np.float32)
    P = {
        "a": hz(x, y), "g": hz(x, y + s), "d": hz(x, y + 2 * s),
        "f": vt(x, y), "b": vt(x + s, y), "e": vt(x, y + s), "c": vt(x + s, y + s),
    }
    for p in P.values():                          # slight italic slant, like a camera LCD font
        p[:, 0] += (2 * s - (p[:, 1] - y)) * 0.12
    return P


def date_stamp(h, w, text, rng):
    """Render the orange LCD-style date stamp layer (alpha 0..1) at bottom right."""
    a = np.zeros((h, w), np.float32)
    s, t, gapd = 24, 7, 40
    x = w - 70 - gapd * len(text.replace(" ", "")) - 26 * text.count(" ")
    y = h - 70 - 2 * s
    for ch in text:
        if ch == " ":
            x += 26
            continue
        if ch == "'":
            cv2.fillPoly(a, [np.int32([(x + 6, y), (x + 13, y), (x + 8, y + 16), (x + 3, y + 16)])], 1.0, cv2.LINE_AA)
            x += 20
            continue
        P = seg_polys(x, y, s, t)
        for sgm in DIGITS[ch]:
            cv2.fillPoly(a, [np.int32(np.round(P[sgm]))], 1.0, cv2.LINE_AA)
        x += gapd
    a = cv2.GaussianBlur(a, (0, 0), 0.9)
    glow = cv2.GaussianBlur(a, (0, 0), 6) * 0.55
    return a, glow


def render(n):
    rng = np.random.default_rng(4400 + n)
    src, m = load(n)
    prev, _ = load(n - 2)
    h, w = src.shape[:2]
    ms = cv2.GaussianBlur(cv2.erode(m, np.ones((5, 5), np.uint8)), (0, 0), 1.5)

    # ambient: underexposed, cool fluorescent/blue cast, slow shutter ghost of the previous moment
    amb = 0.55 * src + 0.45 * prev
    k = np.zeros((1, 15), np.float32)
    k[0, :] = 1 / 15
    amb = cv2.filter2D(amb, -1, k)
    amb = amb * np.array([1.22, 1.02, 0.78], np.float32) * 0.30

    # flash: strong on the people, a little spill on the room right behind them
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    centre = 1 - 0.85 * (((xx / w - 0.5) ** 2) * 1.2 + ((yy / h - 0.45) ** 2))
    spill = 0.10 + cv2.GaussianBlur(m, (0, 0), 220) * 0.35
    F = (ms * 1.0 + (1 - ms) * spill) * centre
    F *= 1 + rng.normal(0, 0.06)
    flash = src * np.array([1.02, 1.0, 0.97], np.float32) * 2.05

    # hard flash shadow: flash sits just above the lens -> shadow falls down-right, offset by size
    sh = np.zeros_like(m)
    M = np.float32([[1.0, 0, 18], [0, 1.0, 14]])
    sh = cv2.warpAffine(m, M, (w, h))
    sh = cv2.GaussianBlur(sh, (0, 0), 3.5) * (1 - ms)

    lit = amb + flash * F[..., None]
    lit *= (1 - 0.75 * sh)[..., None]
    # blown, clipped highlights (cheap CCD): fast shoulder, hard clip
    out = 1 - np.exp(-1.6 * lit)
    out = out / (1 - np.exp(-1.6))
    out = np.where(out > 0.9, 0.9 + (out - 0.9) * 0.3, out)
    # flatten flash-lit faces a bit toward white, keep colour in the room
    y = out @ np.array([0.114, 0.587, 0.299], np.float32)
    out = y[..., None] + (out - y[..., None]) * (1.05 - 0.35 * ms)[..., None]

    # --- the camera ---
    sw, shh = SENSOR
    cam = cv2.resize(out.clip(0, 1), SENSOR, interpolation=cv2.INTER_AREA)
    dark = 1 - cam.mean(-1, keepdims=True)
    lum_n = rng.normal(0, 1, (shh, sw, 1)).astype(np.float32)
    chr_n = cv2.GaussianBlur(rng.normal(0, 1, (shh, sw, 3)).astype(np.float32), (0, 0), 1.6)
    cam += (lum_n * 0.025 + chr_n * 0.06) * (0.3 + dark)          # noisy shadows
    cam = cam + 0.8 * (cam - cv2.GaussianBlur(cam, (0, 0), 1.2))   # oversharpening halos
    cam = cam.astype(np.float32)
    # purple fringing on bright-dark edges
    edge = np.clip(cv2.Laplacian(cv2.GaussianBlur(cam.mean(-1), (0, 0), 1.2), cv2.CV_32F) * -6, 0, 1)
    cam += edge[..., None] * np.array([0.35, -0.05, 0.25], np.float32)
    cam = cam * (1 - 0.18 * (((np.mgrid[0:shh, 0:sw][1] / sw - 0.5) ** 2 + (np.mgrid[0:shh, 0:sw][0] / shh - 0.5) ** 2)))[..., None]

    cam = cam.astype(np.float32)
    # date stamp is burned in by the camera before compression
    a, glow = date_stamp(shh, sw, "'05 10 18", rng)
    col = np.array(ORANGE, np.float32) / 255
    cam = cam * (1 - a[..., None]) + col * a[..., None] + col * glow[..., None]
    q = int(rng.integers(28, 42))
    ok, buf = cv2.imencode(".jpg", (cam.clip(0, 1) * 255).astype(np.uint8),
                           [cv2.IMWRITE_JPEG_QUALITY, q, cv2.IMWRITE_JPEG_SAMPLING_FACTOR, cv2.IMWRITE_JPEG_SAMPLING_FACTOR_420])
    cam = cv2.imdecode(buf, cv2.IMREAD_COLOR)
    final = cv2.resize(cam, (w, h), interpolation=cv2.INTER_LINEAR)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), final)
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    todo = list(range(1, N + 1)) if ARGS == ["all"] else ([int(a) for a in ARGS] or SHEET)
    with Pool(min(8, len(todo))) as p:
        for n in p.imap_unordered(render, todo):
            print(n, end=" ", flush=True)
    print()
