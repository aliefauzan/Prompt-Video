"""Neon scribble / doodle-outline overlay, frame by frame.

usage: python -I render.py [frame numbers...]   (default: the 6 sheet frames)
Reads ../../_source/frames + masks + ./faces.json (faces.swift), writes ./frames/.

Look: the real footage stays (slightly darkened so light reads as light), and
hand-drawn glowing neon marker lines are traced around every person: a white-hot
core with a coloured bloom, a loose doubled outline that wobbles ("boils") every
frame, plus doodles anchored to each head - crown, stars, sparkles, hearts,
arrows, spirals, zig-zag energy marks. One colour per person.
"""
import json
import os
import sys
from multiprocessing import Pool
from pathlib import Path

import cv2
import numpy as np

HERE = Path(__file__).resolve().parent
SRC = HERE.parent.parent / "_source"
FRAMES, MASKS, OUT = SRC / "frames", SRC / "masks", HERE / "frames"
SHEET = [13, 49, 85, 109, 145, 178]
FACES = json.loads((HERE / "faces.json").read_text())
# BGR neon colours, assigned left -> right by head position
NEON = [np.float32([1.0, 0.85, 0.15]),     # electric cyan
        np.float32([0.85, 0.25, 1.0]),     # hot pink
        np.float32([0.20, 1.0, 0.75]),     # acid lime
        np.float32([0.15, 0.80, 1.0])]     # warm yellow


def read(n):
    img = cv2.imread(str(FRAMES / f"frame_{n:03d}.png")).astype(np.float32) / 255
    m = cv2.imread(str(MASKS / f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE)
    return img, m


def wobble(pts, rng, amp, freq):
    """Hand-drawn wobble: smooth random offset along the stroke normal."""
    k = len(pts)
    if k < 3:
        return pts
    ctrl = rng.normal(0, amp, max(3, int(k / freq) + 2))
    off = np.interp(np.linspace(0, len(ctrl) - 1, k), np.arange(len(ctrl)), ctrl)
    d = np.gradient(pts, axis=0)
    nrm = np.stack([-d[:, 1], d[:, 0]], 1)
    nrm /= np.linalg.norm(nrm, axis=1, keepdims=True) + 1e-6
    return pts + nrm * off[:, None]


class Ink:
    """Accumulates neon strokes: per-colour line layer + a thinner white core."""

    def __init__(self, h, w):
        self.col = np.zeros((h, w, 3), np.float32)
        self.core = np.zeros((h, w), np.float32)

    def stroke(self, pts, colour, width, closed=False):
        p = np.round(pts).astype(np.int32).reshape(-1, 1, 2)
        lay = np.zeros(self.core.shape, np.float32)
        cv2.polylines(lay, [p], closed, 1.0, int(width), cv2.LINE_AA)
        self.col = np.maximum(self.col, lay[..., None] * colour)
        c = np.zeros_like(lay)
        cv2.polylines(c, [p], closed, 1.0, max(1, int(width * 0.45)), cv2.LINE_AA)
        self.core = np.maximum(self.core, c)

    def render(self, base):
        glow = (cv2.GaussianBlur(self.col, (0, 0), 3) * 1.6 + cv2.GaussianBlur(self.col, (0, 0), 10) * 1.4
                + cv2.GaussianBlur(self.col, (0, 0), 28) * 0.9)
        out = base + glow
        out = out * (1 - self.col.max(-1, keepdims=True) * 0.5) + self.col * 0.9
        out = out * (1 - self.core[..., None]) + np.float32([0.96, 0.96, 1.0]) * self.core[..., None]
        return out


def star(cx, cy, r, rot, rng):
    a = rot + np.arange(11) * np.pi / 5 * 2                 # 5-point star drawn as one pass + overshoot
    rad = r * rng.uniform(0.88, 1.12, 11)
    return np.stack([cx + np.cos(a) * rad, cy + np.sin(a) * rad], 1)


def sparkle(cx, cy, r):
    t = np.linspace(0, 2 * np.pi, 41)
    rr = r * (0.25 + 0.75 * np.abs(np.cos(2 * t)) ** 3)
    return np.stack([cx + np.cos(t) * rr, cy + np.sin(t) * rr], 1)


def heart(cx, cy, r):
    t = np.linspace(0, 2 * np.pi, 50)
    x = 16 * np.sin(t) ** 3
    y = -(13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t))
    return np.stack([cx + x * r / 16, cy + y * r / 16], 1)


def spiral(cx, cy, r, turns):
    t = np.linspace(0, turns * 2 * np.pi, 80)
    return np.stack([cx + np.cos(t) * r * t / t[-1], cy + np.sin(t) * r * t / t[-1]], 1)


def crown(cx, cy, w):
    xs = cx + np.array([-0.5, -0.5, -0.3, -0.15, 0, 0.15, 0.3, 0.5, 0.5]) * w
    ys = cy + np.array([0, -0.35, -0.12, -0.45, -0.15, -0.45, -0.12, -0.35, 0]) * w
    return np.stack([np.r_[xs, xs[0]], np.r_[ys, ys[0]]], 1)


def arrow(x0, y0, x1, y1):
    shaft = np.stack([np.linspace(x0, x1, 20), np.linspace(y0, y1, 20)], 1)
    a = np.arctan2(y1 - y0, x1 - x0)
    L = np.hypot(x1 - x0, y1 - y0) * 0.25
    head = np.array([[x1 + np.cos(a + 2.6) * L, y1 + np.sin(a + 2.6) * L], [x1, y1],
                     [x1 + np.cos(a - 2.6) * L, y1 + np.sin(a - 2.6) * L]])
    return shaft, head


def zigzag(x0, y0, x1, y1, k, amp):
    t = np.linspace(0, 1, k * 2 + 1)
    p = np.stack([x0 + (x1 - x0) * t, y0 + (y1 - y0) * t], 1)
    a = np.arctan2(y1 - y0, x1 - x0) + np.pi / 2
    s = np.where(np.arange(len(t)) % 2, amp, -amp)
    return p + np.stack([np.cos(a) * s, np.sin(a) * s], 1)


def heads(n):
    fs = sorted(FACES.get(f"frame_{n:03d}.png", []), key=lambda f: f["box"][0])
    return [(f["box"][0] + f["box"][2] / 2, f["box"][1], f["box"][2]) for f in fs]


def colour_for(x, hs, n):
    """Pick the neon colour of the nearest head (stable left->right order)."""
    if not hs:
        return NEON[0]
    i = int(np.argmin([abs(x - h[0]) for h in hs]))
    return NEON[i % len(NEON)] if len(hs) > 1 else NEON[1]


def outline(ink, m, rng, hs, n):
    h, w = m.shape
    r = int(rng.integers(9, 14))
    dil = cv2.dilate((m > 127).astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1)))
    dil = cv2.morphologyEx(dil, cv2.MORPH_CLOSE, np.ones((21, 21), np.uint8))
    cs, _ = cv2.findContours(dil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for c in cs:
        if cv2.contourArea(c) < 4000:
            continue
        p = c[::6, 0, :].astype(np.float32)
        p = cv2.GaussianBlur(p.reshape(-1, 1, 2), (1, 9), 0).reshape(-1, 2) if len(p) > 9 else p
        for rep in range(2):                                  # loose doubled marker line
            q = wobble(p, rng, 3.0 + rep * 3.0, 9) + rng.normal(0, 1.5, 2)
            onb = (q[:, 1] > h - 6) | (q[:, 0] < 4) | (q[:, 0] > w - 5)
            seg = []
            for i, pt in enumerate(q):
                cut = onb[i] or (rep == 1 and rng.random() < 0.012)   # gaps + no line on the frame edge
                if cut:
                    if len(seg) > 4:
                        ink.stroke(np.array(seg), colour_for(np.mean(seg, 0)[0], hs, n), 6 if rep == 0 else 3)
                    seg = []
                else:
                    seg.append(pt)
                    if len(seg) > 40:                          # short pieces so colour follows the person
                        ink.stroke(np.array(seg), colour_for(np.mean(seg, 0)[0], hs, n), 6 if rep == 0 else 3)
                        seg = [pt]
            if len(seg) > 4:
                ink.stroke(np.array(seg), colour_for(np.mean(seg, 0)[0], hs, n), 6 if rep == 0 else 3)


def on_face(pts, hs):
    """True if any point falls on a head (box around the face, brow to chin, plus margin)."""
    for cx, top, bw in hs:
        if np.any((np.abs(pts[:, 0] - cx) < bw * 0.75) & (pts[:, 1] > top - bw * 0.45) & (pts[:, 1] < top + bw * 1.45)):
            return True
    return False


def doodles(ink, hs, rng, n, h, w, m):
    sec = (n - 1) // 24                                       # doodle set changes every 2 s
    for i, (cx, top, bw) in enumerate(hs):
        col = NEON[i % len(NEON)] if len(hs) > 1 else NEON[1]
        j = lambda s=1.0: rng.normal(0, 2.5 * s)              # per-frame boil
        hy = top - bw * 0.80                                  # above the hair (box top = brow line)
        kind = (i + sec) % 4
        if kind == 0:
            ink.stroke(wobble(crown(cx + j(), hy + j(), bw * 0.9), rng, 1.5, 3), col, 5, True)
        elif kind == 1:
            t = np.linspace(0, 6.6, 60)                       # halo ring, drawn past 360 deg
            ring = np.stack([cx + j() + np.cos(t) * bw * 0.55, hy + bw * 0.05 + np.sin(t) * bw * 0.14], 1)
            ink.stroke(wobble(ring, rng, 1.2, 4), col, 5)
        elif kind == 2:
            for s in (-1, 1):
                ink.stroke(star(cx + s * bw * 0.95 + j(), hy + bw * 0.35 + j(), bw * 0.22, rng.uniform(0, 1), rng), col, 4)
        else:
            for s in (-1, 1):                                  # energy zig-zags off the head
                ink.stroke(zigzag(cx + s * bw * 0.70, top - bw * 0.3 + j(), cx + s * bw * 1.15, top - bw * 0.8, 3, 10), col, 4)
        # sparkles near the face, a heart or spiral at shoulder height
        if not on_face(np.array([[cx + bw * 1.0, top + bw * 0.1]]), hs):
            ink.stroke(sparkle(cx + bw * 1.0 + j(), top + bw * 0.1 + j(), bw * 0.16), (1, 1, 1), 3, True)
        if (i + sec) % 2 == 0:
            ink.stroke(heart(cx - bw * 1.05 + j(), top + bw * 1.3 + j(), bw * 0.2), col, 4, True)
        else:
            ink.stroke(wobble(spiral(cx - bw * 1.05 + j(), top + bw * 1.3 + j(), bw * 0.2, 2.5), rng, 1, 4), col, 4)
    # one big arrow pointing at the most central head
    if hs:
        c = min(hs, key=lambda q: abs(q[0] - w / 2))
        first = 1 if c[0] < w * 0.6 else -1
        for side in (first, -first):                           # never draw the arrow across a face
            shaft, head = arrow(c[0] + side * c[2] * 2.2 + rng.normal(0, 3), c[1] - c[2] * 0.2,
                                c[0] + side * c[2] * 1.15, c[1] + c[2] * 0.25)
            if not on_face(np.vstack([shaft, head]), hs):
                ink.stroke(wobble(shaft, rng, 2, 5), (0.3, 1.0, 1.0), 5)
                ink.stroke(head, (0.3, 1.0, 1.0), 5)
                break
    # random small background doodles (boil every frame)
    for _ in range(4):
        x, y = rng.uniform(0.05, 0.95) * w, rng.uniform(0.05, 0.4) * h
        if m[int(y), int(x)] > 64:                          # never on a person
            continue
        ink.stroke(sparkle(x, y, rng.uniform(10, 20)), (1, 1, 1), 2, True)


def render(n):
    rng = np.random.default_rng(900 + n)
    img, m = read(n)
    h, w = m.shape
    # footage: a touch darker and punchier so the neon reads as emitted light
    base = np.clip((img - 0.5) * 1.12 + 0.5, 0, 1) ** 1.25 * 0.72
    hs = heads(n)
    ink = Ink(h, w)
    outline(ink, m, rng, hs, n)
    doodles(ink, hs, rng, n, h, w, m)
    out = ink.render(base)
    cv2.imwrite(str(OUT / f"frame_{n:03d}.png"), (np.clip(out, 0, 1) * 255).astype(np.uint8))
    return n


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    todo = [int(a) for a in sys.argv[1:]] or SHEET
    with Pool(min(6, os.cpu_count() or 4)) as pool:
        for r in pool.imap_unordered(render, todo):
            print(r, end=" ", flush=True)
    print()
