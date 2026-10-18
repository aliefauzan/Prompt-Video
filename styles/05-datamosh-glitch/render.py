"""Datamosh / pixel-sort / RGB-split glitch restyle.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [frame numbers... | all]
Default output: the six sheet frames. Datamosh is stateful, so every frame from 1
up to the last requested one is simulated in order; only requested frames are written.

How it fakes a real codec mosh:
  * motion vectors = optical flow (current -> previous) averaged over 24 px macroblocks
  * a P-frame = previous MOSHED picture moved by those vectors + the true residual
    (current - motion-compensated previous source), so new detail lands on stale pixels
  * the I-frame is dropped: each section starts from a reference picture that may come
    from a different moment of the clip (the classic "scene A moves like scene B" mosh)
  * bloom sections repeat one strong motion field again and again (P-frame duplication)
  * intra-refresh: a share of macroblocks inside the person matte is re-coded from the
    real frame each step, so faces keep re-forming and stay recognizable
Then: macroblock quantisation, pixel sorting (rows or columns), RGB split, slice tears.
"""
import os
import sys

import cv2
import numpy as np

FRAMES, MASKS, OUT = sys.argv[1:4]
ARGS = sys.argv[4:]
N = len([f for f in os.listdir(FRAMES) if f.endswith(".png")])
SHEET = [13, 49, 85, 109, 145, 178]
MB = 24                          # macroblock size in output px
FS = 2                           # flow computed at 1/FS resolution

# (first, last, reference frame for the dropped I-frame, mode, intra-refresh in matte,
#  intra-refresh elsewhere, pixel sort: None | "rows" | "cols", rgb split px)
SECTIONS = [
    (1, 10, 1, "clean", 1.0, 1.0, None, 4),
    (11, 40, 1, "mosh", 0.10, 0.004, None, 6),
    (41, 64, 41, "mosh", 0.22, 0.01, "rows", 5),
    (65, 96, 22, "mosh", 0.12, 0.0, None, 8),          # reference from the close-up: transition mosh
    (97, 124, 97, "bloom", 0.10, 0.0, None, 10),
    (125, 160, 125, "mosh", 0.20, 0.006, "cols", 6),
    (161, 999, 150, "mosh", 0.16, 0.0, "rows", 14),
]


def section(n):
    for s in SECTIONS:
        if s[0] <= n <= s[1]:
            return s
    return SECTIONS[-1]


def load(n):
    n = min(max(n, 1), N)
    img = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png")).astype(np.float32) / 255
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), 0).astype(np.float32) / 255
    return img, m


DIS = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)


def block_flow(cur, prev):
    """Backward flow (cur -> prev) as per-macroblock motion vectors at full resolution."""
    h, w = cur.shape[:2]
    g1 = cv2.cvtColor((cv2.resize(cur, (w // FS, h // FS)) * 255).astype(np.uint8), cv2.COLOR_BGR2GRAY)
    g0 = cv2.cvtColor((cv2.resize(prev, (w // FS, h // FS)) * 255).astype(np.uint8), cv2.COLOR_BGR2GRAY)
    f = DIS.calc(g1, g0, None) * FS
    bw, bh = w // MB, h // MB
    fb = cv2.resize(cv2.resize(f, (w, h)), (bw, bh), interpolation=cv2.INTER_AREA)
    return cv2.resize(fb, (w, h), interpolation=cv2.INTER_NEAREST)


def warp(img, flow):
    h, w = flow.shape[:2]
    gx, gy = np.meshgrid(np.arange(w, dtype=np.float32), np.arange(h, dtype=np.float32))
    return cv2.remap(img, gx + flow[..., 0], gy + flow[..., 1], cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


def block_map(rng, h, w, p):
    """Random per-macroblock 0/1 map with probability p, upsampled to pixels."""
    b = (rng.random((h // MB + 1, w // MB + 1)) < p).astype(np.float32)
    return cv2.resize(b, ((w // MB + 1) * MB, (h // MB + 1) * MB), interpolation=cv2.INTER_NEAREST)[:h, :w]


def quantise_blocks(img, rng, frac):
    """Some macroblocks lose detail (DC-only / posterised), like a starved bitrate."""
    h, w = img.shape[:2]
    small = cv2.resize(img, (w // MB, h // MB), interpolation=cv2.INTER_AREA)
    dc = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
    sel = block_map(rng, h, w, frac)[..., None]
    post = np.round(img * 5) / 5
    sel2 = block_map(rng, h, w, frac * 0.6)[..., None]
    out = img * (1 - sel) + dc * sel
    return out * (1 - sel2) + post * sel2


def pixel_sort(img, mode, rng, keep):
    """Sort runs of mid/bright pixels by brightness along rows or columns (not where keep=1)."""
    a = img if mode == "rows" else img.transpose(1, 0, 2).copy()
    k = keep if mode == "rows" else keep.T
    lum = a @ np.array([0.114, 0.587, 0.299], np.float32)
    lo, hi = 0.42 + rng.uniform(-0.05, 0.05), 0.97
    sel = (lum > lo) & (lum < hi) & (k < 0.5)
    out = a.copy()
    for r in range(a.shape[0]):
        row = sel[r]
        if not row.any():
            continue
        d = np.diff(np.concatenate([[0], row.astype(np.int8), [0]]))
        starts, ends = np.where(d == 1)[0], np.where(d == -1)[0]
        for s0, e0 in zip(starts, ends):
            if e0 - s0 < 12:
                continue
            idx = np.argsort(lum[r, s0:e0])
            if mode == "cols":
                idx = idx[::-1]                   # bright pixels drip downward
            out[r, s0:e0] = a[r, s0:e0][idx]
    return out if mode == "rows" else out.transpose(1, 0, 2)


def rgb_split(img, px, rng):
    b, g, r = cv2.split(img)
    h, w = img.shape[:2]
    def sh(c, dx, dy):
        return cv2.warpAffine(c, np.float32([[1, 0, dx], [0, 1, dy]]), (w, h), borderMode=cv2.BORDER_REFLECT)
    j = rng.normal(0, px * 0.25)
    return cv2.merge([sh(b, -px - j, 0), g, sh(r, px + j, px * 0.15)])


def slices(img, rng, count, m):
    """Horizontal slice tears: bands shifted sideways, kept off the band where heads are."""
    out = img.copy()
    h, w = img.shape[:2]
    rows = np.where(m.max(1) > 0.5)[0]
    top = rows[0] if len(rows) else h
    heads = (top, top + int(0.55 * (h - top)))
    for _ in range(count):
        y0 = int(rng.integers(0, h - 10))
        y1 = min(h, y0 + int(rng.integers(6, 60)))
        if y1 > heads[0] and y0 < heads[1]:
            continue
        out[y0:y1] = np.roll(out[y0:y1], int(rng.integers(-120, 120)), axis=1)
    return out


def finish(n, moshed, src, m):
    rng = np.random.default_rng(5500 + n)
    s = section(n)
    keep = cv2.dilate(m, np.ones((9, 9), np.uint8))
    img = quantise_blocks(moshed, rng, 0.05 if s[3] != "clean" else 0.01)
    if s[6]:
        img = pixel_sort(img, s[6], rng, keep)
    img = rgb_split(img, s[7], rng)
    img = slices(img, rng, int(rng.integers(2, 7)) if s[3] != "clean" else 1, m)
    # codec-ish chroma: slight saturation boost, crushed blacks
    y = img @ np.array([0.114, 0.587, 0.299], np.float32)
    img = y[..., None] + (img - y[..., None]) * 1.3
    img = (img - 0.03) / 0.97
    return img.clip(0, 1)


def main():
    os.makedirs(OUT, exist_ok=True)
    want = set(range(1, N + 1)) if ARGS == ["all"] else set(int(a) for a in ARGS) or set(SHEET)
    last = max(want)
    moshed = None
    bloom_flow = None
    prev_src = None
    for n in range(1, last + 1):
        src, m = load(n)
        s = section(n)
        rng = np.random.default_rng(1234 + n)
        if n == s[0] or moshed is None:
            moshed = load(s[2])[0].copy()            # the (wrong) reference the P-frames build on
            bloom_flow = None
        elif s[3] == "clean":
            moshed = src.copy()
        else:
            flow = block_flow(src, prev_src)
            if s[3] == "bloom":
                if bloom_flow is None or np.abs(flow).mean() > np.abs(bloom_flow).mean():
                    bloom_flow = flow
                use = bloom_flow * 0.9 + flow * 0.4   # one strong vector field duplicated again and again
            else:
                use = flow
            # P-frame residuals are mostly high-frequency: new edges get drawn onto
            # the stale colours of the wrong reference, which is what makes it melt
            residual = src - warp(prev_src, flow)
            hp = residual - cv2.GaussianBlur(residual, (0, 0), 7)
            moshed = warp(moshed, use) + hp * 0.9 + residual * 0.12
            h, w = m.shape
            core = cv2.erode(m, np.ones((15, 15), np.uint8))
            refresh = block_map(rng, h, w, s[4]) * (core > 0.5) + block_map(rng, h, w, s[5])
            refresh = np.clip(refresh, 0, 1)[..., None]
            moshed = (moshed * (1 - refresh) + src * refresh).clip(0, 1)
        prev_src = src
        if n in want:
            out = finish(n, moshed, src, m)
            cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), (out * 255).astype(np.uint8))
            print(n, end=" ", flush=True)
    print()


if __name__ == "__main__":
    main()
