"""Boogley doodle-creature restyle, frame by frame.

usage: python render.py <frames_dir> <masks_dir> <out_dir> [frame numbers...]
The footage stays photographic (light social-media grade). A small cast of
flat cartoon blob creatures lives in the shot with the people: they peek from
the frame edge, sit on shoulders and heads, walk along furniture, and hide
behind the people (the person masks decide what is in front). Their outlines
boil a little every frame, like hand-drawn animation on twos.
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np

FRAMES, MASKS, OUT = sys.argv[1:4]
ONLY = [int(a) for a in sys.argv[4:]]
N = len([f for f in os.listdir(FRAMES) if f.endswith(".png")])

# BGR 0..1 flat fills
COL = {
    "orange": (0.13, 0.45, 0.98),
    "yellow": (0.18, 0.80, 0.98),
    "cyan": (0.93, 0.80, 0.32),
    "pink": (0.78, 0.45, 0.98),
    "green": (0.45, 0.85, 0.45),
}


def vnoise(rng, h, w, cell):
    a = rng.random((max(2, h // cell + 2), max(2, w // cell + 2))).astype(np.float32)
    return cv2.resize(a, (w, h), interpolation=cv2.INTER_CUBIC)


def read_mask(n):
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE)
    return m.astype(np.float32) / 255


def head_top(mask, x0, x1):
    """Top of the person silhouette inside a column band -> (x, y)."""
    band = mask[:, x0:x1] > 0.5
    rows = np.nonzero(band.any(1))[0]
    if not len(rows):
        return (x0 + x1) // 2, 200
    y = rows[0]
    xs = np.nonzero(band[y:y + 25].any(0))[0]
    return x0 + int(xs.mean()), int(y)


def bean(cx, cy, a, b, squash, rng, tilt=0.0, k=120):
    """Hand-drawn bean/blob outline; points wobble per frame (line boil)."""
    t = np.linspace(0, 2 * np.pi, k, endpoint=False)
    p = 2.6
    c, s = np.cos(t), np.sin(t)
    x = np.sign(c) * np.abs(c) ** (2 / p) * a * (1 + squash) * (1 + 0.12 * np.clip(s, 0, 1))
    y = np.sign(s) * np.abs(s) ** (2 / p) * b * (1 - squash)
    wob = np.convolve(np.r_[rng.normal(0, 1, k), rng.normal(0, 1, 8)], np.ones(8) / 8, "same")[:k] * (a * 0.025)
    x = x + wob * c
    y = y + wob * s
    ct, st = np.cos(tilt), np.sin(tilt)
    return np.stack([cx + x * ct - y * st, cy + x * st + y * ct], 1).astype(np.int32)


class Layer:
    """Colour + alpha canvas for one depth layer."""

    def __init__(self, h, w):
        self.c = np.zeros((h, w, 3), np.float32)
        self.a = np.zeros((h, w), np.float32)

    def fill(self, pts, col, alpha=1.0):
        m = np.zeros(self.a.shape, np.uint8)
        cv2.fillPoly(m, [pts], 255, cv2.LINE_AA)
        self._put(m, col, alpha)

    def ellipse(self, c, ax, ang, col, alpha=1.0):
        m = np.zeros(self.a.shape, np.uint8)
        cv2.ellipse(m, (int(c[0]), int(c[1])), (max(1, int(ax[0])), max(1, int(ax[1]))), ang, 0, 360, 255, -1,
                    cv2.LINE_AA)
        self._put(m, col, alpha)

    def line(self, pts, col, th, alpha=1.0):
        m = np.zeros(self.a.shape, np.uint8)
        cv2.polylines(m, [np.asarray(pts, np.int32)], False, 255, max(1, int(th)), cv2.LINE_AA)
        self._put(m, col, alpha)

    def _put(self, m, col, alpha):
        k = m.astype(np.float32) / 255 * alpha
        self.c = self.c * (1 - k[..., None]) + np.array(col, np.float32) * k[..., None]
        self.a = self.a + k * (1 - self.a)


def shade(col, f):
    return tuple(min(1.0, v * f) for v in col)


def creature(L, rng, cx, cy, size, colour, phase, look=(1, 0), kind="bean", wave=False, legs=True, blink=False,
             shadow=None):
    """Draw one Boogley-style blob creature with feet at (cx, cy)."""
    col = COL[colour]
    hop = max(0.0, np.sin(phase * 2 * np.pi))
    squash = 0.10 * np.cos(phase * 4 * np.pi)
    a = size * (0.42 if kind == "bean" else 0.5)
    b = size * (0.55 if kind == "bean" else 0.42)
    by = cy - b - size * 0.12 - hop * size * 0.22
    if shadow is not None:
        L.ellipse((cx, shadow), (a * (1.0 - hop * 0.3), size * 0.06), 0, (0.05, 0.05, 0.06), 0.35)
    if legs:
        for side in (-1, 1):
            step = np.sin(phase * 4 * np.pi + (side > 0) * np.pi) * size * 0.05
            lx = cx + side * a * 0.42
            L.line([(lx, by + b * 0.7), (lx + step, cy - hop * size * 0.22)], shade(col, 0.82), size * 0.11)
            L.ellipse((lx + step + side * size * 0.03, cy - hop * size * 0.22), (size * 0.08, size * 0.045), 0,
                      shade(col, 0.82))
    # arms
    for side in (-1, 1):
        ang = (-1.2 if (wave and side > 0) else 0.6) + 0.5 * np.sin(phase * 6 * np.pi + side)
        sx, sy = cx + side * a * 0.92, by + b * 0.15
        ex, ey = sx + side * size * 0.28 * np.cos(ang), sy + size * 0.28 * np.sin(ang) * (1 if side < 0 else 1)
        mx, my = (sx + ex) / 2 + side * 4, (sy + ey) / 2 - 6
        L.line([(sx, sy), (mx, my), (ex, ey)], shade(col, 0.85), size * 0.09)
    body = bean(cx, by, a, b, squash, rng, tilt=0.06 * np.sin(phase * 2 * np.pi))
    L.fill(body, shade(col, 0.78))                                            # darker rim line
    inner = bean(cx, by, a * 0.955, b * 0.955, squash, rng, tilt=0.06 * np.sin(phase * 2 * np.pi))
    L.fill(inner, col)
    # cel shade crescent bottom-right, highlight top-left
    m_body = np.zeros(L.a.shape, np.uint8)
    cv2.fillPoly(m_body, [inner], 255, cv2.LINE_AA)
    m_lit = np.zeros(L.a.shape, np.uint8)
    cv2.fillPoly(m_lit, [inner - np.array([int(a * 0.22), int(b * 0.18)], np.int32)], 255, cv2.LINE_AA)
    crescent = (m_body.astype(np.float32) / 255) * (1 - m_lit.astype(np.float32) / 255)
    L.c = L.c * (1 - crescent[..., None] * 0.9) + np.array(shade(col, 0.8), np.float32) * crescent[..., None] * 0.9
    L.ellipse((cx - a * 0.45, by - b * 0.55), (a * 0.16, b * 0.09), -30, shade(col, 1.25), 0.85)
    # face
    lx, ly = look
    ey = by - b * 0.25
    for side in (-1, 1):
        ex = cx + side * a * 0.36
        if blink:
            L.line([(ex - a * 0.16, ey), (ex + a * 0.16, ey)], (0.08, 0.06, 0.06), size * 0.04)
        else:
            L.ellipse((ex, ey), (a * 0.21, b * 0.22), 0, (0.98, 0.98, 0.98))
            L.ellipse((ex + lx * a * 0.08, ey + ly * b * 0.07), (a * 0.09, b * 0.1), 0, (0.06, 0.05, 0.05))
            L.ellipse((ex + lx * a * 0.08 - a * 0.03, ey + ly * b * 0.07 - b * 0.04), (a * 0.025, b * 0.025), 0,
                      (1, 1, 1))
    t = np.linspace(0.15, 0.85, 12) * np.pi
    L.line(np.stack([cx + np.cos(t) * a * 0.18, by + b * 0.08 + np.sin(t) * b * 0.1], 1), (0.1, 0.07, 0.07),
           max(2, size * 0.03))
    if kind == "antenna":
        L.line([(cx, by - b), (cx + 6, by - b - size * 0.28)], shade(col, 0.8), size * 0.05)
        L.ellipse((cx + 6, by - b - size * 0.3), (size * 0.07, size * 0.07), 0, COL["pink"])


def doodle_frog(L, rng, cx, cy, s, phase):
    """White hand-drawn doodle sticker character with black wobbly ink (epicuts frog)."""
    ink = (0.05, 0.05, 0.06)
    sway = np.sin(phase * 2 * np.pi) * 0.05

    def wob(pts, amp=2.0):
        pts = np.asarray(pts, np.float32)
        return (pts + rng.normal(0, amp, pts.shape)).astype(np.int32)

    t = np.linspace(0, 2 * np.pi, 60, endpoint=False)
    head = np.stack([cx + np.cos(t) * s * 0.42, cy - s * 1.25 + np.sin(t) * s * 0.3], 1)
    body = np.stack([cx + np.cos(t) * s * 0.34, cy - s * 0.55 + np.sin(t) * s * 0.5], 1)
    M = cv2.getRotationMatrix2D((cx, cy), np.degrees(sway), 1.0)

    def rot(p):
        p = np.asarray(p, np.float32)
        return np.c_[p, np.ones(len(p))] @ M.T

    for shape in (body, head):                                        # white sticker rim then paper fill
        L.fill(wob(rot(shape) * 1.0 + 0, 0.5), (1, 1, 1))
    grid = np.zeros(L.a.shape, np.float32)
    yy, xx = np.mgrid[0:L.a.shape[0], 0:L.a.shape[1]]
    grid[((xx % 14) == 0) | ((yy % 14) == 0)] = 1
    m = np.zeros(L.a.shape, np.uint8)
    cv2.fillPoly(m, [wob(rot(body), 0.3), wob(rot(head), 0.3)], 255)
    g = grid * (m > 0) * 0.25
    L.c = L.c * (1 - g[..., None]) + np.array((0.85, 0.65, 0.55), np.float32) * g[..., None]
    for shape in (body, head):
        L.line(np.r_[wob(rot(shape)), wob(rot(shape[:1]))], ink, s * 0.035)
    for side in (-1, 1):                                              # eyes, arms, legs, headband
        ex, ey = rot([(cx + side * s * 0.17, cy - s * 1.33)])[0]
        L.ellipse((ex, ey), (s * 0.08, s * 0.1), 0, (1, 1, 1))
        L.ellipse((ex, ey), (s * 0.08, s * 0.1), 0, ink, 0.0)
        tt = np.linspace(0, 2 * np.pi, 22)
        L.line(wob(np.stack([ex + np.cos(tt) * s * 0.08, ey + np.sin(tt) * s * 0.1], 1), 0.7), ink, s * 0.025)
        L.ellipse((ex + s * 0.02, ey + s * 0.02), (s * 0.035, s * 0.04), 0, ink)
        arm = rot([(cx + side * s * 0.3, cy - s * 0.7), (cx + side * s * 0.5, cy - s * 0.45),
                   (cx + side * s * 0.15, cy - s * 0.5)])
        L.line(wob(arm), ink, s * 0.03)
        leg = rot([(cx + side * s * 0.15, cy - s * 0.1), (cx + side * s * 0.18, cy), (cx + side * s * 0.35, cy)])
        L.line(wob(leg), ink, s * 0.03)
    band = rot([(cx - s * 0.4, cy - s * 1.45), (cx, cy - s * 1.52), (cx + s * 0.4, cy - s * 1.45)])
    L.line(wob(band), ink, s * 0.07)
    mouth = rot([(cx - s * 0.18, cy - s * 1.15), (cx, cy - s * 1.1), (cx + s * 0.2, cy - s * 1.16)])
    L.line(wob(mouth), ink, s * 0.03)


def over(dst, L):
    return dst * (1 - L.a[..., None]) + L.c * L.a[..., None]


def grade(img):
    """Light social-media grade: a touch of warmth, contrast and saturation."""
    hsv = cv2.cvtColor((img * 255).astype(np.uint8), cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[..., 1] = np.clip(hsv[..., 1] * 1.15, 0, 255)
    img = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32) / 255
    img = (img - 0.5) * 1.06 + 0.5
    return (img * np.array([0.97, 1.0, 1.03], np.float32)).clip(0, 1)


def render(n):
    rng = np.random.default_rng(3300 + (n // 2))       # boil on twos
    img = grade(cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png")).astype(np.float32) / 255)
    mask = read_mask(n)
    h, w = mask.shape
    back, front = Layer(h, w), Layer(h, w)
    ph = n / 12.0
    blink = (n % 37) in (0, 1)

    # cyan antenna blob clings to the TV screen all clip long (people pass in front of it)
    creature(back, rng, 1470 + 14 * np.sin(ph * 0.7), 330, 115, "cyan", ph * 0.9, look=(-1, 0.3), kind="antenna",
             wave=True, legs=True, blink=blink)
    # yellow pup patrols the planter between the people (people hide it as they move)
    px = 430 + (np.sin(ph * 0.45) * 0.5 + 0.5) * 680
    creature(back, rng, px, 642, 118, "yellow", ph * 1.6, look=(np.sign(np.cos(ph * 0.45)), 0), shadow=640)

    if n <= 60:
        # big orange peeks in from the left edge, in front of the first man
        creature(front, rng, 120 + 30 * np.sin(ph * 1.3), 1150, 560, "orange", ph * 0.35, look=(1, -0.2), legs=False,
                 blink=blink)
    elif n <= 120:
        # orange climbed onto the left man's shoulder and waves
        sx, sy = head_top(mask, 0, 420)
        creature(front, rng, sx + 150, sy + 330, 170, "orange", ph * 1.2, look=(1, 0.2), wave=True, blink=blink)
        creature(front, rng, 1450, 1110, 300, "pink", ph * 0.8, look=(-1, -0.3), wave=True, legs=False)
    else:
        # small orange rides on the woman's head; doodle frog sticker stands in the corner
        hx, hy = head_top(mask, 620, 1060)
        if hy > 120:
            creature(front, rng, hx, hy + 14, 150, "orange", ph * 1.4, look=(0.4, 0.5), blink=blink)
        else:
            # her head fills the frame: orange peeks out of the gap between her and the left man
            row = mask[620, 120:hx] < 0.5
            runs, x = [], 0
            while x < len(row):
                if row[x]:
                    x1 = x
                    while x1 < len(row) and row[x1]:
                        x1 += 1
                    runs.append((x1 - x, x + 120, x1 + 120))
                    x = x1
                x += 1
            gx = (max(runs)[1] + max(runs)[2]) // 2 if runs else 420
            creature(back, rng, gx, 800, 260, "orange", ph * 0.8, look=(1, -0.1), legs=False, blink=blink)
        doodle_frog(front, rng, 1430, 1075, 330, ph * 0.6)
        creature(front, rng, 210, 1090, 210, "green", ph * 1.1, look=(1, -0.4), wave=True)

    out = over(img, back)
    pm = cv2.GaussianBlur(mask, (0, 0), 1.0)[..., None]
    out = out * (1 - pm) + img * pm                         # people occlude the back layer
    out = over(out, front)
    out += rng.normal(0, 0.008, (h, w, 1)).astype(np.float32)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), (out.clip(0, 1) * 255).astype(np.uint8))
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    todo = ONLY or list(range(1, N + 1))
    with Pool(min(8, os.cpu_count() or 4)) as pool:
        for n in pool.imap_unordered(render, todo):
            print(n, end=" ", flush=True)
    print()
