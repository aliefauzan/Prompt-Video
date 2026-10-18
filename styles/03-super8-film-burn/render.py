"""Super 8 home-movie film restyle with light leaks and film burns, frame by frame.

usage: python -I render.py <frames_dir> <out_dir> [frame numbers... | all]
Default frames: the six sheet frames. Whole-frame film emulation, so the people
stay exactly as in the source.

Per frame: warm faded reversal-film grade -> softness + halation -> grain + flicker
-> dust, hairs, scratches -> light leaks / film burn (by section)
-> picture placed on a weaving Super 8 strip (rounded gate, frame lines,
neighbouring frames, sprocket hole) on a dark scanner bed.
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np

FRAMES, OUT = sys.argv[1:3]
ARGS = sys.argv[3:]
N = len([f for f in os.listdir(FRAMES) if f.endswith(".png")])
SHEET = [13, 49, 85, 109, 145, 178]
CW, CH = 1620, 1080               # output canvas
PW, PH = 1430, 954                # picture (keeps the 3:2 composition)
PX, PY = 150, (CH - PH) // 2      # picture origin on the strip
GAP = 30                          # frame line between frames
BASE = np.array([0.035, 0.05, 0.07], np.float32)  # film base / scanner bed (BGR, warm black)

# (first, last, leak edge, leak colour BGR, burn)
SECTIONS = [
    (1, 30, "left", (0.15, 0.45, 1.0), False),
    (31, 66, "top", (0.10, 0.30, 1.0), False),
    (67, 100, None, None, False),
    (101, 116, "right", (0.05, 0.35, 1.0), True),
    (117, 160, "bottom", (0.25, 0.55, 1.0), False),
    (161, 999, "left", (0.05, 0.25, 0.95), True),
]


def section(n):
    for s in SECTIONS:
        if s[0] <= n <= s[1]:
            return s
    return SECTIONS[-1]


def vnoise(rng, h, w, cell):
    a = rng.random((max(2, h // cell + 2), max(2, w // cell + 2))).astype(np.float32)
    return cv2.resize(a, (w, h), interpolation=cv2.INTER_CUBIC).clip(0, 1)


def grade(img):
    """Faded Kodachrome/Ektachrome reversal: warm amber, brown lifted blacks, creamy highlights."""
    y = img @ np.array([0.114, 0.587, 0.299], np.float32)
    img = y[..., None] + (img - y[..., None]) * 0.92
    # per-channel curves (B, G, R)
    img = np.stack([
        0.07 + 0.80 * np.power(img[..., 0], 1.18),
        0.07 + 0.86 * np.power(img[..., 1], 1.02),
        0.09 + 0.90 * np.power(img[..., 2], 0.88),
    ], -1)
    img = img * img * (3 - 2 * img) * 0.35 + img * 0.65          # gentle S for punchy mids
    return img.clip(0, 1)


def grain(rng, h, w):
    g = np.zeros((h, w, 3), np.float32)
    lum = cv2.GaussianBlur(rng.normal(0, 1, (h, w)).astype(np.float32), (0, 0), 1.9)
    for c in range(3):
        g[..., c] = lum * 0.75 + cv2.GaussianBlur(
            rng.normal(0, 1, (h, w)).astype(np.float32), (0, 0), 1.0) * 0.45
    return g


def leak(n, h, w, edge, colour):
    """Soft additive light leak entering from one edge; drifts and breathes over the section."""
    if edge is None:
        return np.zeros((h, w, 3), np.float32)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    t = n * 0.21
    s = 0.55 + 0.45 * np.sin(t) * np.sin(t * 0.37 + 1.0)
    if edge == "left":
        d = xx / w + 0.12 * np.sin(yy / h * 3 + t)
        cy = h * (0.5 + 0.3 * np.sin(t * 0.5))
        d = d + 0.25 * np.abs(yy - cy) / h
    elif edge == "right":
        d = 1 - xx / w + 0.12 * np.sin(yy / h * 3 + t)
        d = d + 0.25 * np.abs(yy - h * 0.3) / h
    elif edge == "top":
        d = yy / h + 0.15 * np.sin(xx / w * 4 + t)
        d = d + 0.2 * np.abs(xx - w * (0.7 + 0.2 * np.sin(t * 0.4))) / w
    else:
        d = 1 - yy / h + 0.15 * np.sin(xx / w * 4 + t)
    a = np.exp(-(d / (0.20 + 0.10 * s)) ** 2) * (0.75 + 0.35 * s)
    col = np.array(colour, np.float32)
    core = np.exp(-(d / 0.07) ** 2)[..., None] * np.array([0.6, 0.85, 1.0], np.float32)
    return a[..., None] * col + core * 0.6 * s


def burn(n, rng, h, w, first, last):
    """Film burn: an organic white-hot hole that grows from one side, ringed yellow-orange-red-brown.
    Returns (additive light, darkening of the charred rim)."""
    p = (n - first + 1) / (last - first + 1)                  # 0..1 through the burn section
    p = 0.35 + 0.65 * p
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    srng = np.random.default_rng(first)                       # same burn shape all section
    cx, cy = (w * 0.95, h * 0.35) if first < 150 else (w * 0.05, h * 0.6)
    r = np.sqrt((xx - cx) ** 2 + ((yy - cy) * 1.2) ** 2) / w
    field = r + 0.20 * vnoise(srng, h, w, 160) + 0.06 * vnoise(srng, h, w, 55) + 0.012 * vnoise(rng, h, w, 18)
    lvl = 0.04 + 0.36 * p
    e = field - lvl                                           # <0 inside the hole
    hot = np.clip(-e / 0.06, 0, 1)
    ring = np.exp(-(e / 0.05) ** 2)
    glow = np.exp(-np.clip(e, 0, None) / 0.18)
    light = (hot[..., None] * np.array([0.85, 0.98, 1.0], np.float32) * 1.4
             + ring[..., None] * np.array([0.05, 0.55, 1.0], np.float32) * 1.1
             + glow[..., None] * np.array([0.0, 0.18, 0.55], np.float32) * 0.8)
    char = np.exp(-((e - 0.035) / 0.012) ** 2) * 0.55         # dark brown edge just outside the ring
    return light, char


def dirt(rng, n, h, w):
    """Dark dust specks and hairs + a couple of vertical scratches (positions persist per section)."""
    d = np.zeros((h, w), np.float32)
    for _ in range(int(rng.integers(12, 40))):
        x, y = int(rng.integers(0, w)), int(rng.integers(0, h))
        r = int(rng.integers(1, 5))
        cv2.ellipse(d, (x, y), (r, max(1, r + int(rng.integers(-1, 3)))), float(rng.uniform(0, 180)),
                    0, 360, float(rng.uniform(0.4, 1.0)), -1, cv2.LINE_AA)
    for _ in range(int(rng.integers(0, 3))):
        x, y = rng.uniform(0, w), rng.uniform(0, h)
        pts = []
        a = rng.uniform(0, np.pi * 2)
        for k in range(14):
            a += rng.normal(0, 0.35)
            x += np.cos(a) * 9
            y += np.sin(a) * 9
            pts.append((x, y))
        cv2.polylines(d, [np.int32(pts)], False, 0.9, int(rng.integers(1, 3)), cv2.LINE_AA)
    d = cv2.GaussianBlur(d, (0, 0), 0.8)
    s = np.zeros((h, w), np.float32)
    srng = np.random.default_rng(section(n)[0] * 7)
    for _ in range(2):
        x = srng.uniform(0.1, 0.9) * w + rng.normal(0, 2)
        y0, y1 = 0, h
        if rng.random() < 0.5:
            y0 = int(rng.uniform(0, h * 0.5))
            y1 = int(y0 + rng.uniform(h * 0.3, h))
        cv2.line(s, (int(x), y0), (int(x + rng.normal(0, 4)), y1), float(rng.uniform(0.3, 0.8)), 1, cv2.LINE_AA)
    return d, cv2.GaussianBlur(s, (0, 0), 0.6)


def picture(n, rng, src):
    img = cv2.resize(src, (PW, PH), interpolation=cv2.INTER_AREA)
    img = grade(img)
    img = cv2.GaussianBlur(img, (0, 0), 2.2)                   # soft 8 mm optics
    hi = np.clip(img.max(-1, keepdims=True) - 0.72, 0, 1)
    img += cv2.GaussianBlur(hi, (0, 0), 16)[..., None] * np.array([0.08, 0.35, 0.9], np.float32) * 0.9  # halation
    img *= 1 + rng.normal(0, 0.045)                            # exposure flicker
    yy, xx = np.mgrid[0:PH, 0:PW].astype(np.float32)
    v = ((xx / PW - 0.5) ** 2 * 1.1 + (yy / PH - 0.5) ** 2)
    img *= (1 - 0.95 * v)[..., None]                           # heavy projector-lamp vignette
    mid = 0.4 + 0.6 * (1 - np.abs(img.mean(-1, keepdims=True) - 0.45) * 1.6).clip(0, 1)
    img += grain(rng, PH, PW) * 0.13 * mid
    s = section(n)
    if s[2]:
        img = 1 - (1 - img) * (1 - np.clip(leak(n, PH, PW, s[2], s[3]), 0, 1) * 0.85)   # screen
    if s[4] and n in range(s[0], s[1] + 1):
        lt, ch = burn(n, rng, PH, PW, s[0], min(s[1], N))
        img = img * (1 - ch[..., None]) + lt
    d, sc = dirt(rng, n, PH, PW)
    img = img * (1 - 0.85 * d[..., None]) + sc[..., None] * 0.55
    return img.clip(0, 1.2)


def gate_mask(rng):
    """Rounded-corner Super 8 gate with slightly rough, soft edges."""
    m = np.zeros((PH, PW), np.float32)
    r = 34
    cv2.rectangle(m, (r, 0), (PW - r, PH), 1, -1)
    cv2.rectangle(m, (0, r), (PW, PH - r), 1, -1)
    for cx, cy in ((r, r), (PW - r, r), (r, PH - r), (PW - r, PH - r)):
        cv2.circle(m, (cx, cy), r, 1, -1, cv2.LINE_AA)
    rough = cv2.GaussianBlur(rng.normal(0, 1, (PH, PW)).astype(np.float32), (0, 0), 3) * 0.6
    m = cv2.GaussianBlur(m, (0, 0), 2.2)
    return np.clip((m - 0.5 + rough * 0.15) * 4 + 0.5, 0, 1)


def render(n):
    rng = np.random.default_rng(8800 + n)
    src = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png")).astype(np.float32) / 255
    sh, sw = src.shape[:2]
    pic = picture(n, rng, src)
    gm = gate_mask(rng)

    # tall strip: previous frame above, current, next frame below
    sh_ = PH * 3 + GAP * 2
    strip = np.empty((sh_, CW, 3), np.float32)
    strip[:] = BASE
    nb = {-1: max(1, n - 1), 0: n, 1: min(N, n + 1)}
    for k in (-1, 0, 1):
        y = PH + GAP + k * (PH + GAP)
        if k == 0:
            p = pic
        else:
            nsrc = cv2.imread(os.path.join(FRAMES, f"frame_{nb[k]:03d}.png")).astype(np.float32) / 255
            p = picture(nb[k], np.random.default_rng(7700 + nb[k]), nsrc)
        strip[y:y + PH, PX:PX + PW] = strip[y:y + PH, PX:PX + PW] * (1 - gm[..., None]) + p * gm[..., None]
        # sprocket hole beside the frame line (bright: scanner light shines through)
        hy = y - GAP // 2
        hole = np.zeros((sh_, CW), np.float32)
        cv2.rectangle(hole, (38, hy - 62), (108, hy + 62), 1, -1)
        hole = cv2.GaussianBlur(hole, (0, 0), 6)
        hole = np.clip((hole - 0.5) * 3 + 0.5, 0, 1)
        strip += hole[..., None] * (np.array([0.82, 0.92, 1.0], np.float32) - strip)
    # thin bright film edge on the far left, edge printing smear
    strip[:, :14] = strip[:, :14] * 0.4 + np.array([0.55, 0.65, 0.75], np.float32) * 0.6

    # gate weave: the whole strip drifts a few px each frame (smooth + jitter), tiny rotation
    t = n * 0.9
    dx = 3.0 * np.sin(t * 0.7) + rng.normal(0, 1.2)
    dy = 4.0 * np.sin(t * 0.45 + 1) + rng.normal(0, 1.5)
    rot = 0.18 * np.sin(t * 0.33) + rng.normal(0, 0.05)
    M = cv2.getRotationMatrix2D((CW / 2, sh_ / 2), rot, 1.0)
    M[0, 2] += dx
    M[1, 2] += dy
    strip = cv2.warpAffine(strip, M, (CW, sh_), borderMode=cv2.BORDER_REPLICATE)
    y0 = PH + GAP - PY
    out = strip[y0:y0 + CH]
    out += cv2.GaussianBlur(rng.normal(0, 1, out.shape[:2]).astype(np.float32), (0, 0), 1.2)[..., None] * 0.012
    out = cv2.resize(out, (sw, sh), interpolation=cv2.INTER_AREA) if (sw, sh) != (CW, CH) else out
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), (out.clip(0, 1) * 255).astype(np.uint8))
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    todo = list(range(1, N + 1)) if ARGS == ["all"] else ([int(a) for a in ARGS] or SHEET)
    with Pool(min(8, len(todo))) as p:
        for n in p.imap_unordered(render, todo):
            print(n, end=" ", flush=True)
    print()
