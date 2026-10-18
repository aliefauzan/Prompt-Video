"""Hand-Drawn Frame-by-Frame FX (手绘逐帧特效): local approximation of style 97.

usage: python -I render.py <out_dir> [frame numbers...]   (default: all 179)

The live-action footage stays photographic (slightly darkened so the effects
read). Over it, cel-painted elemental effects are drawn fresh on every frame,
anchored to the people's outlines from the source mattes:

  0-5 s    FIRE: flame tongues licking up from heads and shoulders, built as a
           heat field and posterized into hard cel bands (dark red edge, red,
           orange, yellow, white core), embers and cel smoke puffs rising
  ~5 s     a big cel smoke cloud wipes the frame (hiding the hand-over-lens shot)
  5-10 s   LIGHTNING: jagged blue-white bolts crawling over the outlines and
           arcing between people, one-frame blue flashes, sparks
  10-15 s  GREEN SPIRIT FLAME with crescent slash arcs on the beat

Every shape is redrawn each frame with new random wobble (the "boil" of
hand-drawn animation on ones at 12 fps), but sizes follow slow noise so the
effect lives instead of flickering. Light from the effects is cast back onto the
people, and a soft glow is added.
"""
import json
import sys
from functools import lru_cache
from pathlib import Path

import cv2
import numpy as np

HERE = Path(__file__).resolve().parent
SRC = HERE.parent.parent / "_source"
POSE = json.loads((HERE.parent / "94-xray-skeleton-scan" / "pose.json").read_text())
H, W = 1080, 1620
COUNT = 179
FIRE = (1, 60)
WIPE = (56, 67)          # smoke wipe: grows to cover the frame, then clears
BOLT = (61, 121)
GREEN = (121, 180)
SLASHES = (96, 124, 140, 158, 171)

# cel bands (BGR): edge, dark, mid, light, core
PAL_FIRE = [(18, 24, 120), (10, 60, 225), (0, 140, 255), (70, 215, 255), (205, 248, 255)]
PAL_GREEN = [(30, 80, 10), (40, 160, 25), (70, 225, 80), (170, 255, 185), (235, 255, 240)]
PAL_BOLT = [(120, 30, 10), (255, 120, 30), (255, 210, 110), (255, 245, 220), (255, 255, 255)]


def raw_mask(n):
    return cv2.imread(str(SRC / "masks" / f"frame_{n:03d}.png"), 0).astype(np.float32) / 255


@lru_cache(maxsize=40)
def load_mask(n):
    m = raw_mask(n)
    if 1 < n < COUNT:                     # broken mattes 023 / 068
        a, b = raw_mask(n - 1), raw_mask(n + 1)
        if m.sum() < 0.85 * min(a.sum(), b.sum()):
            m = np.maximum(m, np.minimum(a, b))
    k, lab, st, _ = cv2.connectedComponentsWithStats((m > 0.5).astype(np.uint8))
    keep = np.zeros(k, bool)
    keep[1:] = st[1:, cv2.CC_STAT_AREA] > 0.012 * H * W
    m = m * cv2.dilate(keep[lab].astype(np.uint8), np.ones((9, 9), np.uint8))
    return cv2.GaussianBlur(m, (0, 0), 3)


@lru_cache(maxsize=40)
def outline(n):
    """Outline points of the people with outward normals, every ~6 px."""
    m = load_mask(n)
    cs, _ = cv2.findContours((m > 0.5).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    gy, gx = np.gradient(cv2.GaussianBlur(m, (0, 0), 6))
    pts, nrm = [], []
    for c in cs:
        if len(c) < 60:
            continue
        p = c[::6, 0, :]
        g = np.stack([-gx[p[:, 1], p[:, 0]], -gy[p[:, 1], p[:, 0]]], 1)
        g /= np.linalg.norm(g, axis=1, keepdims=True) + 1e-6
        inside = (p[:, 0] > 3) & (p[:, 0] < W - 4) & (p[:, 1] > 3) & (p[:, 1] < H - 4)
        pts.append(p[inside].astype(np.float32))
        nrm.append(g[inside])
    if not pts:
        return np.zeros((0, 2), np.float32), np.zeros((0, 2), np.float32)
    return np.concatenate(pts), np.concatenate(nrm)


def face_boxes(n):
    """Apple Vision face boxes of frames n-1..n+1 (a miss in one frame is covered)."""
    out = []
    for m in range(max(1, n - 1), min(COUNT, n + 1) + 1):
        out += [f["box"] for f in POSE[f"frame_{m:03d}.png"].get("faces", []) if f["box"][2] > 40]
    return out


def upper_anchors(n, step=52):
    """Outline points facing up (heads, shoulders, arms), spaced ~step px.
    Points beside or below a face are skipped so flames never cover a face."""
    p, g = outline(n)
    sel = g[:, 1] < -0.25
    for x, y, w, h in face_boxes(n):
        sel &= ~((p[:, 0] > x - 0.35 * w) & (p[:, 0] < x + 1.35 * w) & (p[:, 1] > y - 0.15 * h))
    p, g = p[sel], g[sel]
    out, last = [], None
    for i in np.argsort(p[:, 0]):
        if last is None or abs(p[i, 0] - last[0]) > step or abs(p[i, 1] - last[1]) > step:
            out.append((p[i], g[i]))
            last = p[i]
    return out


def noise1(x, t, seed=0):
    """Smooth pseudo-noise in [-1, 1] from a few sines."""
    return (np.sin(x * 0.021 + t * 1.3 + seed) * 0.5 + np.sin(x * 0.047 - t * 2.1 + seed * 2.3) * 0.3
            + np.sin(x * 0.009 + t * 0.7 + seed * 5.1) * 0.2)


# ---------------------------------------------------------------- fire
def tongue(base, up, h, w, t, rng, lean):
    """Polygon of one flame tongue (base point, up direction)."""
    perp = np.array([-up[1], up[0]])
    s = np.linspace(0, 1, 14)
    phase = rng.uniform(0, 6.3)
    wig = (0.22 * w + 0.12 * h) * np.sin(s * np.pi * 1.3 + phase + t * 3) * s ** 1.2 + lean * h * s ** 2
    hw = w * (1 - s) ** 0.75 * (1 + 0.25 * np.sin(s * 9 + phase)) * (0.6 + 0.4 * np.sin(np.pi * np.clip(s * 1.6, 0, 1)))
    hw += rng.normal(0, 0.05 * w, s.shape)              # boil: new hand-drawn wobble every frame
    spine = base[None, :] + up[None, :] * (s * h)[:, None] + perp[None, :] * wig[:, None]
    left = spine + perp[None, :] * hw[:, None]
    right = spine - perp[None, :] * hw[:, None]
    return np.concatenate([left, right[::-1]])


def fire_field(n, scale=1.0):
    t = n / 12
    rng = np.random.default_rng(1000 + n)
    heat = np.zeros((H, W), np.float32)
    tips = []
    for p, g in upper_anchors(n):
        up = np.array([0.25 * g[0], -1.0])
        up /= np.linalg.norm(up)
        nz = noise1(p[0], t, 1.0)
        h = scale * (125 + 85 * nz + rng.uniform(-15, 15)) * (1.25 if g[1] < -0.8 else 0.85)
        if h < 40:
            continue
        w = 0.3 * h + 14
        base = p - g * 0.25 * w                          # flames rise from just inside the outline
        lean = 0.25 * np.sin(t * 1.1) + 0.1 * nz        # wind sway
        for k in range(4):
            f = 1 - 0.2 * k
            poly = tongue(base + up * 0.12 * k * h, up, h * f, w * (1 - 0.23 * k), t, rng, lean)
            tmp = np.zeros_like(heat)
            cv2.fillPoly(tmp, [np.round(poly * 4).astype(np.int32)], 1.0, lineType=cv2.LINE_AA, shift=2)
            heat += 0.26 * tmp
        tips.append(base + up * h * 0.85)
    return np.minimum(heat, 1.0), tips


def cel(field, pal, th=(0.12, 0.3, 0.52, 0.76, 0.95)):
    """Posterize a 0-1 field into hard cel bands; returns colour and alpha."""
    f = cv2.GaussianBlur(field, (0, 0), 2.2)
    col = np.zeros((H, W, 3), np.float32)
    a = (f > th[0]).astype(np.float32)
    for c, lo in zip(pal, th):
        col[f > lo] = c
    a = cv2.GaussianBlur(a, (0, 0), 0.8)
    return col, a


# ---------------------------------------------------------------- particles
@lru_cache(maxsize=40)
def tips_of(n):
    if not (FIRE[0] <= n < FIRE[1] or GREEN[0] <= n < GREEN[1]):
        return ()
    return tuple(map(tuple, fire_field(n, 0.9 if n >= GREEN[0] else 1.0)[1]))


def smoke_layer(n, tint):
    """Cel smoke puffs: spawned at flame tips over the last 14 frames, rising,
    growing then breaking up. Two tones plus a dark outline."""
    body = np.zeros((H, W), np.uint8)
    lite = np.zeros((H, W), np.uint8)
    for s in range(max(1, n - 14), n + 1):
        tips = tips_of(s)
        if not tips:
            continue
        rng = np.random.default_rng(5000 + s)
        idx = rng.choice(len(tips), size=min(1, len(tips)), replace=False)
        for i in idx:
            age = n - s
            x0, y0 = tips[i]
            drift = rng.uniform(-1.5, 1.5)
            x = x0 + drift * age * 3 + 6 * np.sin(age * 0.6 + i)
            y = y0 - 20 - age * rng.uniform(8, 12)
            r = rng.uniform(26, 40) * (1 + 0.1 * age) * max(0.0, 1 - (age / 15) ** 2.2)
            if r < 3:
                continue
            for j in range(3):                            # a little cluster per puff
                ox, oy = rng.uniform(-0.7, 0.7) * r, rng.uniform(-0.5, 0.3) * r
                rr = int(r * rng.uniform(0.6, 0.95))
                c = (int(x + ox), int(y + oy))
                cv2.circle(body, c, rr, 1, -1, cv2.LINE_AA)
                cv2.circle(lite, (int(c[0] - rr * 0.25), int(c[1] - rr * 0.3)), int(rr * 0.62), 1, -1, cv2.LINE_AA)
    lite &= body
    edge = cv2.dilate(body, np.ones((3, 3), np.uint8)) - body
    col = np.zeros((H, W, 3), np.float32)
    col[body > 0] = tint[0]
    col[lite > 0] = tint[1]
    col[edge > 0] = tint[2]
    a = ((body | edge) > 0).astype(np.float32) * 0.6
    return col, cv2.GaussianBlur(a, (0, 0), 0.7)


def embers(n, pal, cv):
    for s in range(max(1, n - 10), n + 1):
        tips = tips_of(s)
        if not tips:
            continue
        rng = np.random.default_rng(9000 + s)
        for i in rng.choice(len(tips), size=min(5, len(tips)), replace=False):
            age = n - s
            x0, y0 = tips[i]
            vx, vy = rng.uniform(-6, 6), rng.uniform(-16, -9)
            x, y = x0 + vx * age + 8 * np.sin(age + i), y0 + vy * age
            sz = rng.uniform(4, 8) * (1 - age / 11)
            if sz < 1.5:
                continue
            d = np.array([[0, -2.2], [1, 0], [0, 1], [-1, 0]]) * sz + [x, y]
            cv2.fillPoly(cv, [np.round(d * 4).astype(np.int32)], pal[3], cv2.LINE_AA, shift=2)
            cv2.circle(cv, (int(x), int(y)), max(1, int(sz * 0.35)), pal[4], -1, cv2.LINE_AA)


# ---------------------------------------------------------------- lightning
def jag(a, b, rng, rough, depth=5):
    """Midpoint-displacement lightning path a->b."""
    pts = [np.asarray(a, np.float32), np.asarray(b, np.float32)]
    for d in range(depth):
        new = [pts[0]]
        for p, q in zip(pts[:-1], pts[1:]):
            v = q - p
            nrm = np.array([-v[1], v[0]]) / (np.linalg.norm(v) + 1e-6)
            mid = (p + q) / 2 + nrm * rng.normal(0, rough * np.linalg.norm(v))
            new += [mid, q]
        pts = new
    return np.array(pts)


def draw_bolt(cv, glow, path, pal, wid):
    p = np.round(path * 4).astype(np.int32)
    cv2.polylines(cv, [p], False, pal[0], wid + 6, cv2.LINE_AA, shift=2)
    cv2.polylines(cv, [p], False, pal[1], wid + 3, cv2.LINE_AA, shift=2)
    cv2.polylines(cv, [p], False, pal[3], max(1, wid), cv2.LINE_AA, shift=2)
    cv2.polylines(glow, [p], False, 1.0, wid + 10, cv2.LINE_AA, shift=2)


def lightning(n, cv, glow):
    rng = np.random.default_rng(3000 + n)
    p, g = outline(n)
    if len(p) < 20:
        return
    # crawling bolts hugging the outline
    for _ in range(9):
        i = rng.integers(0, len(p) - 1)
        L = rng.integers(14, 40)
        idx = np.arange(i, min(len(p), i + L))
        if len(idx) < 6:
            continue
        sub = p[idx] + g[idx] * rng.uniform(4, 22)
        jump = np.nonzero(np.linalg.norm(np.diff(p[idx], axis=0), axis=1) > 40)[0]
        if len(jump):                                   # outline points jump across a gap: stop there
            idx, sub = idx[:jump[0] + 1], sub[:jump[0] + 1]
        if len(idx) < 6:
            continue
        path = []
        for a, b in zip(sub[:-3:3], sub[3::3]):
            seg = jag(a, b, rng, 0.35, 2)
            path.extend(seg[:-1])
        if len(path) < 3:
            continue
        path = np.array(path)
        draw_bolt(cv, glow, path, PAL_BOLT, 6)
        if rng.random() < 0.6:                          # a fork shooting outward
            k = rng.integers(1, len(path) - 1)
            o = path[k] + g[idx[min(len(idx) - 1, k // 4)]] * rng.uniform(60, 150) + rng.normal(0, 30, 2)
            draw_bolt(cv, glow, jag(path[k], o, rng, 0.2, 4), PAL_BOLT, 3)
    # sparks
    for _ in range(14):
        i = rng.integers(0, len(p))
        c = p[i] + g[i] * rng.uniform(5, 40)
        d = rng.normal(0, 1, 2)
        d /= np.linalg.norm(d)
        q = c + d * rng.uniform(10, 26)
        cv2.line(cv, (int(c[0]), int(c[1])), (int(q[0]), int(q[1])), PAL_BOLT[3], 2, cv2.LINE_AA)


def rim_light(n, color, strength):
    """Coloured rim around the outline (the effect lighting the people)."""
    m = load_mask(n)
    ring = cv2.GaussianBlur(m, (0, 0), 14) - cv2.GaussianBlur(m, (0, 0), 2)
    ring = np.clip(np.abs(ring) * 3, 0, 1)
    return ring[..., None] * np.array(color, np.float32)[None, None, :] * strength


# ---------------------------------------------------------------- slash
def slash(n, cv, glow, pal):
    for s0 in SLASHES:
        k = n - s0
        if not 0 <= k < 4:
            continue
        rng = np.random.default_rng(s0)
        cx, cy = W * rng.uniform(0.35, 0.65), H * rng.uniform(0.45, 0.65)
        R = rng.uniform(380, 520)
        a0 = rng.uniform(-2.6, -2.2) if s0 % 2 else rng.uniform(-0.9, -0.5)
        span = 1.9 * (1 if s0 % 2 else -1)
        reach = [0.6, 1.0, 1.0, 1.0][k]
        width = [46, 58, 30, 14][k]
        ss = np.linspace(0, reach, 60)
        prof = np.sin(np.pi * ss / max(reach, 1e-3)) ** 0.7
        if k >= 2:                                    # breaking up as it fades
            prof *= (np.sin(ss * 40 + k) > -0.2 * k)
        ang = a0 + span * ss
        for col, f in ((pal[1], 1.0), (pal[3], 0.55), (pal[4], 0.22)):
            outer = np.stack([cx + (R + width * f * prof) * np.cos(ang), cy + (R + width * f * prof) * np.sin(ang)], 1)
            inner = np.stack([cx + (R - 0.3 * width * f * prof) * np.cos(ang), cy + (R - 0.3 * width * f * prof) * np.sin(ang)], 1)
            poly = np.concatenate([outer, inner[::-1]])
            cv2.fillPoly(cv, [np.round(poly * 4).astype(np.int32)], col, cv2.LINE_AA, shift=2)
            if f == 1.0:
                cv2.fillPoly(glow, [np.round(poly * 4).astype(np.int32)], 1.0, cv2.LINE_AA, shift=2)


# ---------------------------------------------------------------- smoke wipe
def wipe(n):
    """Big cel smoke cloud covering the frame around the hand-over-lens shot."""
    a, b = WIPE
    if not a <= n < b:
        return None
    mid = 61.5
    cover = (n - a) / (mid - a) if n < mid else 1 - (n - mid) / (b - mid)
    cover = np.clip(cover, 0, 1) ** 0.8
    rng = np.random.default_rng(77)
    body = np.zeros((H, W), np.uint8)
    lite = np.zeros((H, W), np.uint8)
    hi = np.zeros((H, W), np.uint8)
    for i in range(70):
        x, y = rng.uniform(-100, W + 100), rng.uniform(H * 0.1, H + 150)
        r = rng.uniform(140, 300) * cover * (1 + 0.04 * np.sin(n * 0.9 + i))
        y -= cover * 160 + (n - a) * 6
        if r < 4:
            continue
        cv2.circle(body, (int(x), int(y)), int(r), 1, -1, cv2.LINE_AA)
        cv2.circle(lite, (int(x - r * 0.15), int(y - r * 0.2)), int(r * 0.86), 1, -1, cv2.LINE_AA)
    lite &= body
    edge = cv2.dilate(body, np.ones((7, 7), np.uint8)) - body
    col = np.zeros((H, W, 3), np.float32)
    col[body > 0] = (92, 60, 70)
    col[lite > 0] = (150, 125, 140)
    col[edge > 0] = (45, 25, 35)
    return col, cv2.GaussianBlur(((body | edge) > 0).astype(np.float32), (0, 0), 0.8)


# ---------------------------------------------------------------- frame
def over(base, col, a):
    return base * (1 - a[..., None]) + col * a[..., None]


def render(n):
    img = cv2.imread(str(SRC / "frames" / f"frame_{n:03d}.png")).astype(np.float32)
    gray = img.mean(2, keepdims=True)
    out = (gray + (img - gray) * 0.8) * 0.72              # darker, a little desaturated: FX read
    glow = np.zeros((H, W), np.float32)
    glow_col = (0, 0, 0)
    fx = np.zeros((H, W, 3), np.float32)
    fa = np.zeros((H, W), np.float32)

    if FIRE[0] <= n < FIRE[1] or GREEN[0] <= n < GREEN[1]:
        green = n >= GREEN[0]
        pal = PAL_GREEN if green else PAL_FIRE
        out += rim_light(n, pal[2], 0.55)
        tint = ((70, 80, 60), (130, 150, 120), (25, 35, 20)) if green else ((60, 58, 72), (120, 120, 140), (25, 22, 35))
        sc, sa = smoke_layer(n, tint)
        out = over(out, sc, sa)
        heat, _ = fire_field(n, 0.9 if green else 1.0)
        col, a = cel(heat, pal)
        cv = np.zeros((H, W, 3), np.uint8)
        embers(n, pal, cv)
        ea = (cv.max(2) > 0).astype(np.float32)
        col = np.where(ea[..., None] > 0, cv.astype(np.float32), col)
        a = np.maximum(a, ea)
        fx, fa = col, a
        glow = cv2.GaussianBlur(heat, (0, 0), 9)
        glow_col = pal[2]
        if green:
            cv = np.zeros((H, W, 3), np.uint8)
            g2 = np.zeros((H, W), np.float32)
            slash(n, cv, g2, PAL_GREEN)
            sa2 = (cv.max(2) > 0).astype(np.float32)
            fx = np.where(sa2[..., None] > 0, cv.astype(np.float32), fx)
            fa = np.maximum(fa, cv2.GaussianBlur(sa2, (0, 0), 0.7))
            glow = np.maximum(glow, g2)
    elif BOLT[0] <= n < BOLT[1]:
        out += rim_light(n, PAL_BOLT[1], 0.6)
        cv = np.zeros((H, W, 3), np.uint8)
        g2 = np.zeros((H, W), np.float32)
        lightning(n, cv, g2)
        slash(n, cv, g2, PAL_BOLT)
        a = (cv.max(2) > 0).astype(np.float32)
        fx, fa = cv.astype(np.float32), cv2.GaussianBlur(a, (0, 0), 0.7)
        glow = g2
        glow_col = PAL_BOLT[1]
        if n % 9 in (0, 4) and n > BOLT[0] + 8:              # one-frame electric flash
            out = out * 1.25 + np.array([60, 30, 0], np.float32)

    # glow and the light the effect casts on the people
    g = cv2.GaussianBlur(glow, (0, 0), 30)
    out += g[..., None] * np.array(glow_col, np.float32) * 0.9
    m = load_mask(n)[..., None]
    out += m * cv2.GaussianBlur(glow, (0, 0), 90)[..., None] * np.array(glow_col, np.float32) * 1.4
    out = over(out, fx, fa)
    out += cv2.GaussianBlur(fa, (0, 0), 6)[..., None] * np.array(glow_col, np.float32) * 0.25

    w = wipe(n)
    if w is not None:
        out = over(out, *w)
    return np.clip(out, 0, 255).astype(np.uint8)


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
