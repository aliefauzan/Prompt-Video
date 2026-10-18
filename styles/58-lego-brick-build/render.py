"""LEGO Brick Build — local approximation of the frame-by-frame restyle.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [all | 13 49 85 ...]

The frame is rebuilt as a studs-out brick build in two layers:
  * the people (mask) on a fine 12 px stud grid (135 x 90 studs), sharp;
  * the room on a coarse 24 px grid (bigger bricks), behind a macro-lens
    depth-of-field blur, like a brick backdrop behind brick-built figures.
Every stud cell takes the nearest colour from a real LEGO colour palette
(after a little local contrast on the people so eyes and mouths survive),
lone stray studs are removed, runs of same-colour studs in a row merge into
1x1..1x4 bricks (lengths fixed by a hash of row/column so unchanged areas keep
their bricks), and each brick gets seams, bevel light/shadow, moulded studs
with rim light, drop shadow and specular dot, plus a soft ABS plastic sheen.
When frames are rendered in order ("all"), cells keep their previous colour
unless the new one is clearly better (hysteresis): static bricks hold still,
only bricks the people move through get "rebuilt" — no random boil.
"""
import sys
from pathlib import Path

import cv2
import numpy as np

W, H = 1620, 1080
FINE, COARSE = 12, 24

PALETTE = np.array([
    (244, 244, 242),  # White
    (160, 165, 169),  # Light Bluish Gray
    (108, 110, 114),  # Dark Bluish Gray
    (87, 88, 87),     # Pearl Dark Gray
    (33, 33, 35),     # Black
    (201, 26, 9),     # Red
    (114, 14, 15),    # Dark Red
    (88, 42, 18),     # Reddish Brown
    (53, 33, 10),     # Dark Brown
    (170, 125, 85),   # Medium Nougat
    (208, 145, 104),  # Nougat
    (246, 215, 179),  # Light Nougat
    (169, 85, 0),     # Dark Orange
    (242, 205, 55),   # Yellow
    (228, 205, 158),  # Tan
    (149, 138, 115),  # Dark Tan
    (155, 154, 90),   # Olive Green
    (35, 120, 65),    # Green
    (24, 70, 50),     # Dark Green
    (54, 174, 191),   # Medium Azure
    (0, 85, 191),     # Blue
    (10, 52, 99),     # Dark Blue
    (90, 147, 219),   # Medium Blue
    (96, 116, 161),   # Sand Blue
    (228, 173, 200),  # Bright Pink
    (200, 112, 160),  # Dark Pink
    (204, 112, 42),   # Dark Nougat
    (120, 85, 60),    # Medium Brown
], np.float32)


def to_lab(rgb):
    a = np.clip(rgb, 0, 255).astype(np.uint8).reshape(-1, 1, 3)
    return cv2.cvtColor(a, cv2.COLOR_RGB2LAB).reshape(-1, 3).astype(np.float32)


PAL_LAB = to_lab(PALETTE)


def stud_sprite(C):
    """Shading multiplier M and additive highlight A for one stud cell (4x supersampled)."""
    S = 4
    n = C * S
    y, x = np.mgrid[0:n, 0:n].astype(np.float32) / S + 0.5 / S
    cx = cy = C / 2
    r = C * 0.32
    k = C / 12
    dx, dy = x - cx, y - cy
    d = np.hypot(dx, dy)
    M = np.ones((n, n), np.float32)
    A = np.zeros((n, n), np.float32)
    # drop shadow of the stud on the brick top (light from upper left)
    ds = np.hypot(x - cx - 1.6 * k, y - cy - 1.8 * k)
    M *= 1 - 0.38 * np.clip((r + 0.9 * k - ds) / (1.8 * k), 0, 1)
    # stud top: slightly brighter, gradient toward the light
    top = np.clip((r - d) / (0.8 * k), 0, 1)
    grad = 1.08 - 0.08 * (dx + dy) / r
    M = M * (1 - top) + top * grad
    # rim: lit edge upper-left, dark edge lower-right
    rim = np.clip(1 - np.abs(d - (r - 0.7 * k)) / (0.9 * k), 0, 1)
    facing = -(dx + dy) / (np.sqrt(2) * np.maximum(d, 1e-3))
    A += rim * np.clip(facing, 0, 1) * 0.28
    M *= 1 - rim * np.clip(-facing, 0, 1) * 0.42
    # specular dot on the stud
    A += 0.45 * np.exp(-(((x - cx + r * 0.38) ** 2 + (y - cy + r * 0.42) ** 2) / (2 * (r * 0.2) ** 2)))
    M = cv2.resize(M, (C, C), interpolation=cv2.INTER_AREA)
    A = cv2.resize(A, (C, C), interpolation=cv2.INTER_AREA)
    return M, A


SPRITES = {c: stud_sprite(c) for c in (FINE, COARSE)}


def h32(*v):
    x = 2166136261
    for k in v:
        x = ((x ^ (k & 0xFFFFFFFF)) * 16777619) & 0xFFFFFFFF
    return x


def despeckle(idx):
    """Replace lone studs whose 4 neighbours all differ with the commonest neighbour colour."""
    p = np.pad(idx, 1, mode="edge")
    nb = np.stack([p[:-2, 1:-1], p[2:, 1:-1], p[1:-1, :-2], p[1:-1, 2:]])
    lone = (nb != idx).all(0)
    out = idx.copy()
    for r, c in zip(*np.nonzero(lone)):
        v, k = np.unique(nb[:, r, c], return_counts=True)
        out[r, c] = v[k.argmax()]
    return out


def quantise(frame, mask, C, prev, people):
    gw, gh = -(-W // C), -(-H // C)
    pad = cv2.copyMakeBorder(frame, 0, gh * C - H, 0, gw * C - W, cv2.BORDER_REPLICATE)
    small = cv2.resize(pad, (gw, gh), interpolation=cv2.INTER_AREA).astype(np.float32)
    if people:
        # local contrast so eyes, brows and mouths survive the stud grid
        small = small + 0.7 * (small - cv2.GaussianBlur(small, (0, 0), 1.2))
    g = small.mean(2, keepdims=True)
    small = g + (small - g) * (1.12 if people else 1.05)
    small = (small - 128) * 1.06 + 134
    lab = to_lab(small)
    dist = ((lab[:, None, :] - PAL_LAB[None]) ** 2).sum(-1)
    idx = despeckle(dist.argmin(1).reshape(gh, gw)).reshape(-1)
    if prev is not None:
        p = prev.reshape(-1)
        keep = dist[np.arange(len(idx)), p] < dist[np.arange(len(idx)), idx] + 90
        idx = np.where(keep, p, idx)
    return idx.reshape(gh, gw)


def bricks(idx):
    """Left/right brick-end flags per cell. Every row is a separate plate row."""
    gh, gw = idx.shape
    left = np.zeros(idx.shape, bool)
    right = np.zeros(idx.shape, bool)
    bid = np.zeros(idx.shape, np.int64)
    nxt = 0
    for r in range(gh):
        c = 0
        while c < gw:
            L = (1, 2, 2, 3, 4, 4, 2, 1)[h32(r, c, gw) % 8]
            e = c + 1
            while e < gw and e - c < L and idx[r, e] == idx[r, c]:
                e += 1
            left[r, c] = True
            right[r, e - 1] = True
            bid[r, c:e] = h32(r, c, idx[r, c]) % 1000
            nxt += 1
            c = e
    return left, right, bid


def build(idx, C):
    """Shade a brick layer from its colour-index grid."""
    gh, gw = idx.shape
    left, right, bid = bricks(idx)
    col = PALETTE[idx] * ((bid / 1000.0 - 0.5) * 0.06 + 1)[..., None]   # moulding variation
    up = lambda a: np.repeat(np.repeat(a, C, 0), C, 1)[:H, :W]
    base = up(col)
    SM, SA = SPRITES[C]
    M = np.tile(SM, (gh, gw))[:H, :W].copy()
    A = np.tile(SA, (gh, gw))[:H, :W].copy()
    yy, xx = np.mgrid[0:H, 0:W]
    ly, lx = yy % C, xx % C
    L, R = up(left), up(right)
    e = max(1, C // 12)
    M[ly < e] *= 0.42
    A[(ly >= e) & (ly < 2 * e)] += 0.08
    M[ly >= C - e] *= 0.78
    M[(lx < e) & L] *= 0.42
    A[(lx >= e) & (lx < 2 * e) & L] += 0.07
    M[(lx >= C - e) & R] *= 0.78
    lum = base.mean(2, keepdims=True) / 255
    return base * M[..., None] + 255 * A[..., None] * (0.55 + 0.45 * (1 - lum))


def render(frame, mask, state, n):
    fine_idx = quantise(frame, mask, FINE, state.get("fine"), True)
    coarse_idx = quantise(frame, mask, COARSE, state.get("coarse"), False)
    state["fine"], state["coarse"] = fine_idx, coarse_idx
    fine = build(fine_idx, FINE)
    room = build(coarse_idx, COARSE)
    # macro depth of field on the room, stronger toward top/bottom (tilt-shift)
    yy, xx = np.mgrid[0:H, 0:W]
    ts = np.clip(np.abs(yy / H - 0.5) * 2.2 - 0.5, 0, 1)[..., None]
    room = cv2.GaussianBlur(room, (0, 0), 2.6) * (1 - ts) + cv2.GaussianBlur(room, (0, 0), 5.0) * ts
    # people mask on the fine stud grid (whole studs, no soft matte)
    gm = cv2.resize(mask, (W // FINE, H // FINE), interpolation=cv2.INTER_AREA) > 0.45
    pm = np.repeat(np.repeat(gm, FINE, 0), FINE, 1).astype(np.float32)
    # soft contact shadow of the figures on the backdrop
    sh = cv2.GaussianBlur(np.roll(pm, (10, 14), (0, 1)), (0, 0), 10)
    room *= (1 - 0.35 * sh)[..., None]
    img = fine * pm[..., None] + room * (1 - pm[..., None])
    # broad ABS sheen from the key light (upper left)
    sheen = np.exp(-(((xx - W * 0.28) / (W * 0.55)) ** 2 + ((yy - H * 0.15) / (H * 0.6)) ** 2))
    img = img * (0.94 + 0.16 * sheen[..., None]) + 10 * sheen[..., None]
    img = np.clip(img, 0, 255).astype(np.float32)
    # bloom on bright plastic highlights
    br = np.clip(img.mean(2) - 200, 0, 55)[..., None] / 55
    img += cv2.GaussianBlur(img * br, (0, 0), 9) * 0.25
    # warm macro grade + vignette + faint sensor noise
    img = img * np.array([1.04, 1.0, 0.94])
    v = 1 - 0.20 * (((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H / 2) / (H * 0.62)) ** 2)
    img = img * np.clip(v, 0.55, 1)[..., None]
    img += np.random.default_rng(n).normal(0, 2.2, img.shape)
    return np.clip(img, 0, 255).astype(np.uint8)


def main():
    fdir, mdir, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    out.mkdir(parents=True, exist_ok=True)
    args = sys.argv[4:] or ["13", "49", "85", "109", "145", "178"]
    seq = args == ["all"]
    nums = list(range(1, 180)) if seq else [int(a) for a in args]
    state = {}
    for n in nums:
        f = cv2.cvtColor(cv2.imread(str(fdir / f"frame_{n:03d}.png")), cv2.COLOR_BGR2RGB)
        m = cv2.imread(str(mdir / f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
        if not seq:
            state = {}
        img = render(f, m, state, n)
        cv2.imwrite(str(out / f"frame_{n:03d}.png"), cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
        print(n, end=" ", flush=True)
    print()


if __name__ == "__main__":
    main()
