"""Bad Apple 1-Bit Silhouette: local approximation of style 96.

usage: python -I render.py <inst_dir> <out_dir> [frame numbers...]   (default: all 179)

<inst_dir> holds per-person instance label PNGs from instances.swift
(`swiftc -O instances.swift -o instances && ./instances ../../_source/frames <inst_dir>`); they are only used
to cut thin separation gaps where one person overlaps another.

Every output pixel is pure black or pure white. People come from the source
mattes, smoothed so the outline reads as one clean cut shape. Where two people
overlap, a thin gap in the background colour separates them, as in the Bad
Apple!! shadow-art PV. The room is dropped completely: a blank ground, as in
the PV, so the figures carry the whole image. The polarity
flips on hard cuts: black figures on white (0-5 s), white on black (5-10 s),
then a split screen whose figures invert across a slowly drifting line.
"""
import sys
from functools import lru_cache
from pathlib import Path

import cv2
import numpy as np

HERE = Path(__file__).resolve().parent
SRC = HERE.parent.parent / "_source"
H, W = 1080, 1620
COUNT = 179
FLIPS = (61, 121)          # frames where the polarity flips (5 s and 10 s)
SPLIT_FROM = 121           # last section: split screen, figures invert across a drifting line


def raw_mask(n):
    return cv2.imread(str(SRC / "masks" / f"frame_{n:03d}.png"), 0).astype(np.float32) / 255


def load_mask(n):
    m = raw_mask(n)
    if 1 < n < COUNT:                     # broken mattes 023 / 068
        a, b = raw_mask(n - 1), raw_mask(n + 1)
        if m.sum() < 0.85 * min(a.sum(), b.sum()):
            m = np.maximum(m, np.minimum(a, b))
    k, lab, st, _ = cv2.connectedComponentsWithStats((m > 0.5).astype(np.uint8))
    keep = np.zeros(k, bool)
    keep[1:] = st[1:, cv2.CC_STAT_AREA] > 0.012 * H * W
    return m * cv2.dilate(keep[lab].astype(np.uint8), np.ones((9, 9), np.uint8))


def separation(inst, sil):
    """Thin lines where two different person instances meet inside the silhouette."""
    sep = np.zeros((H, W), np.uint8)
    # keep only the main body of each instance: stray islands (a hand labelled as
    # someone else for one frame) would draw flickering loops
    clean = np.zeros_like(inst)
    for v in np.unique(inst):
        if not v:
            continue
        n, lab, st, _ = cv2.connectedComponentsWithStats((inst == v).astype(np.uint8))
        big = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
        if st[big, cv2.CC_STAT_AREA] > 0.02 * H * W:
            clean[lab == big] = v
    inst = clean
    labels = [v for v in np.unique(inst) if v]
    k = np.ones((7, 7), np.uint8)
    for a in labels:
        da = cv2.dilate((inst == a).astype(np.uint8), k)
        for b in labels:
            if b <= a:
                continue
            db = cv2.dilate((inst == b).astype(np.uint8), k)
            sep |= da & db
    sep = cv2.dilate(sep, np.ones((3, 3), np.uint8)) & (sil > 0.5).astype(np.uint8)
    k, lab, st, _ = cv2.connectedComponentsWithStats(sep)
    keep = np.zeros(k, bool)
    keep[1:] = st[1:, cv2.CC_STAT_AREA] > 600          # only long, stable contour cuts
    return keep[lab].astype(np.uint8)


@lru_cache(maxsize=8)
def frame_sep(n, inst_dir):
    m = load_mask(n)
    sil = cv2.GaussianBlur(m, (0, 0), 2.5)
    inst = cv2.imread(str(Path(inst_dir) / f"frame_{n:03d}.png"), 0)
    if inst is None:
        return sil, np.zeros((H, W), np.uint8)
    return sil, separation(cv2.medianBlur(inst, 5), sil)


def stable_sep(n, inst_dir):
    """Separation gap of frame n, kept only where every frame within +-2 has a
    gap nearby: label swaps that last a frame or two never reach the image."""
    sil, sep = frame_sep(n, inst_dir)
    for m in range(max(1, n - 2), min(COUNT, n + 2) + 1):
        if m != n:
            sep = sep & cv2.dilate(frame_sep(m, inst_dir)[1], np.ones((15, 15), np.uint8))
    k, lab, st, _ = cv2.connectedComponentsWithStats(sep)
    keep = np.zeros(k, bool)
    keep[1:] = st[1:, cv2.CC_STAT_AREA] > 400
    return sil, keep[lab].astype(np.uint8)


def render(n, inst_dir):
    sil, sep = stable_sep(n, inst_dir)
    person = (sil > 0.5).astype(np.uint8) & (1 - sep)
    fig = person
    inverted = sum(n >= f for f in FLIPS) % 2 == 1
    if inverted:
        out = fig * 255                      # white figures on black
    else:
        out = (1 - fig) * 255                # black figures on white
    if n >= SPLIT_FROM:
        # Bad Apple split-screen: left half black ground, right half white ground;
        # the figure colour swaps across the line (XOR)
        t = (n - SPLIT_FROM) / 12
        xs = 0.5 * W + 0.18 * W * np.sin(t * 0.9)
        left = (np.arange(W)[None, :] < xs).astype(np.uint8)
        out = (fig ^ (1 - left)) * 255
    return np.dstack([out] * 3).astype(np.uint8)


def main():
    inst_dir, out = sys.argv[1], Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    nums = [int(a) for a in sys.argv[3:]] or range(1, COUNT + 1)
    for n in nums:
        cv2.imwrite(str(out / f"frame_{n:03d}.png"), render(n, inst_dir))
        print(n, end=" ", flush=True)
    print()


if __name__ == "__main__":
    main()
