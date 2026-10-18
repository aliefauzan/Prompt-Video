"""Red-Cyan Anaglyph 3D: local approximation of style 95.

usage: python -I render.py <out_dir> [frame numbers...]   (default: all 179)

Reads ../94-xray-skeleton-scan/pose.json only for face boxes (Apple Vision),
used to guess how near each person is (bigger face = nearer).

Builds a two-layer depth scene per frame: the room (people filled in from the
surrounding wall so they leave no ghost) with a gentle depth ramp behind the
screen, and the people (from the masks) in front of it, each with its own
nearness from face size plus a little rounding from the mask's distance
transform. A left-eye and a right-eye view are rendered by shifting each layer
by its own disparity and compositing people over room. The red channel comes
from the left view and green + blue from the right view (half-colour
anaglyph: the left view goes in as luma, so skin is not red-washed). Then a
light print contrast, a soft vignette and fine grain.
"""
import json
import sys
from pathlib import Path

import cv2
import numpy as np

HERE = Path(__file__).resolve().parent
SRC = HERE.parent.parent / "_source"
POSE = json.loads((HERE.parent / "94-xray-skeleton-scan" / "pose.json").read_text())
H, W = 1080, 1620
COUNT = 179


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


def faces(n):
    out = []
    for f in POSE[f"frame_{n:03d}.png"].get("faces", []):
        x, y, w, h = f["box"]
        if w > 50:
            out.append((x + w / 2, y + h / 2, w))
    return out


def smooth_faces(n):
    """Face list of frame n with sizes averaged over +-3 frames (nearest match)."""
    res = []
    for cx, cy, w in faces(n):
        ws = [w]
        for m in range(max(1, n - 3), min(COUNT, n + 3) + 1):
            if m == n:
                continue
            c = [(abs(fx - cx) + abs(fy - cy), fw) for fx, fy, fw in faces(m)]
            if c and min(c)[0] < 120:
                ws.append(min(c)[1])
        res.append((cx, cy, float(np.median(ws))))
    return res


def person_disparity(n, m):
    """Disparity (px) for the people layer: nearness from face width, by x."""
    fl = [f for f in smooth_faces(n) if m[int(np.clip(f[1], 0, H - 1)), int(np.clip(f[0], 0, W - 1))] > 0.3]
    xs = np.arange(W, dtype=np.float32)
    if fl:
        wsum = np.zeros(W, np.float32)
        dsum = np.zeros(W, np.float32)
        for cx, cy, fw in fl:
            d = 12 + 62 * fw / W                  # 130 px face ~ 17 px, 400 px face ~ 27 px
            wt = np.exp(-((xs - cx) / (1.2 * fw + 60)) ** 2) + 1e-4
            wsum += wt
            dsum += wt * d
        row = dsum / wsum
    else:
        row = np.full(W, 12, np.float32)
    disp = np.repeat(row[None, :], H, 0)
    mb = (m > 0.5).astype(np.uint8)
    dist = cv2.distanceTransform(mb, cv2.DIST_L2, 5)
    disp = disp + 5 * (1 - np.exp(-dist / 60))   # bodies are round, not cardboard
    return cv2.GaussianBlur(disp, (0, 0), 6)


def fill_behind(img, m):
    """Room without people: normalized convolution from the surrounding pixels."""
    keep = (1 - cv2.dilate(m, np.ones((15, 15), np.uint8))).astype(np.float32)
    small = cv2.resize(img.astype(np.float32), (W // 4, H // 4), interpolation=cv2.INTER_AREA)
    ks = cv2.resize(keep, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
    acc = small * ks[..., None]
    den = ks.copy()
    out = small.copy()
    for s in (2, 4, 8, 16, 32):
        a = cv2.GaussianBlur(acc, (0, 0), s)
        d = cv2.GaussianBlur(den, (0, 0), s)
        est = a / np.maximum(d[..., None], 1e-4)
        miss = (ks < 0.5)[..., None]
        out = np.where(miss & (d[..., None] > 0.02), est, out)
        if s == 2:
            out = np.where(miss, est, out)
    big = cv2.resize(out, (W, H), interpolation=cv2.INTER_CUBIC)
    k3 = keep[..., None]
    return img.astype(np.float32) * k3 + big * (1 - k3)


def shift(img, dx):
    """Sample img at x - dx (dx is a per-pixel map)."""
    xs, ys = np.meshgrid(np.arange(W, dtype=np.float32), np.arange(H, dtype=np.float32))
    return cv2.remap(img, xs - dx.astype(np.float32), ys, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)


def render(n):
    img = cv2.imread(str(SRC / "frames" / f"frame_{n:03d}.png")).astype(np.float32)
    m = load_mask(n)
    room = fill_behind(img, (m > 0.3).astype(np.uint8))
    yy = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    room_d = np.repeat(-13 + 9 * yy, W, 1)            # far wall behind the screen, floor comes forward
    pd = person_disparity(n, m)

    views = []
    for sgn in (1, -1):                               # left eye, right eye
        r = shift(room, sgn * room_d / 2)
        p = shift(img, sgn * pd / 2)
        a = shift(m, sgn * pd / 2)[..., None]
        views.append(r * (1 - a) + p * a)
    L, R = views

    luma = 0.299 * L[..., 2] + 0.587 * L[..., 1] + 0.114 * L[..., 0]
    red = 0.6 * luma + 0.4 * L[..., 2]
    out = np.dstack([R[..., 0], R[..., 1], red])      # BGR

    # print-like contrast + slight saturation so the fringes read
    out = out / 255
    out = np.clip((out - 0.5) * 1.12 + 0.5, 0, 1)
    gray = out.mean(2, keepdims=True)
    out = np.clip(gray + (out - gray) * 1.15, 0, 1)
    xx = np.linspace(-1, 1, W)[None, :]
    yv = np.linspace(-1, 1, H)[:, None]
    out *= (1 - 0.18 * np.clip((xx ** 2 + yv ** 2) / 2, 0, 1))[..., None]
    g = np.random.default_rng(n).normal(0, 0.012, (H, W, 1)).astype(np.float32)
    return np.clip((out + g) * 255, 0, 255).astype(np.uint8)


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    nums = [int(a) for a in sys.argv[2:]] or range(1, COUNT + 1)
    for n in nums:
        cv2.imwrite(str(out / f"frame_{n:03d}.png"), render(n))
        print(n, end=" ", flush=True)
    print()


if __name__ == "__main__":
    main()
