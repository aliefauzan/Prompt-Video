"""Dreamy double-exposure restyle, frame by frame.

usage: python -I render.py [frame numbers... | all]   (default: the six sheet frames)
       RENDER_OUT=/tmp/prompt-video-render/<slug> python -I render.py all   -> full clip for make_video.py
Reads ../../_source/frames + ../../_source/masks, writes ./frames/frame_NNN.png.

Classic double exposure: a high-key mono portrait on an off-white ground, with a second
image (misty pine forest, sunset clouds, dusk city, mountain ridges) SCREENED into the
silhouette. Faces keep most of the portrait; clothes and hair dissolve into the texture.
Then bloom, red-orange halation, light leak and film grain.
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "..", "_source")
FRAMES, MASKS, OUT = os.path.join(SRC, "frames"), os.path.join(SRC, "masks"), os.path.join(HERE, "frames")
OUT = os.environ.get("RENDER_OUT", OUT)        # e.g. /tmp/prompt-video-render/<slug> for the full clip
ONLY = (list(range(1, 180)) if sys.argv[1:] == ["all"] else [int(a) for a in sys.argv[1:]]) or [13, 49, 85, 109, 145, 178]
H, W = 1080, 1620
PAD = 900          # texture canvases are wider than the frame so they can pan

# first, last, second exposure, ground ('paper' = off-white, 'ghost' = faded original room)
SECTIONS = [
    (1, 30, "forest", "paper"),
    (31, 66, "clouds", "paper"),
    (67, 100, "city", "ghost"),
    (101, 136, "mountains", "paper"),
    (137, 160, "forest", "ghost"),
    (161, 999, "clouds", "paper"),
]


def section_of(n):
    for i, s in enumerate(SECTIONS):
        if s[0] <= n <= s[1]:
            return i, s
    return len(SECTIONS) - 1, SECTIONS[-1]


def vnoise(rng, h, w, cell):
    a = rng.random((max(2, h // cell + 2), max(2, w // cell + 2))).astype(np.float32)
    return cv2.resize(a, (w, h), interpolation=cv2.INTER_CUBIC).clip(0, 1)


def fbm(seed, h, w, shift, cell=360, octaves=5):
    rng = np.random.default_rng(seed)
    out = np.zeros((h, w), np.float32)
    amp = 0.5
    for _ in range(octaves):
        big = vnoise(rng, h, w + 400, cell)
        s = int(shift * cell / 360) % 400
        out += amp * big[:, s:s + w]
        amp *= 0.5
        cell = max(8, cell // 2)
    return out


def vgrad(stops):
    """Vertical gradient from [(t, (r,g,b)), ...] -> H x 1 x 3."""
    t = np.linspace(0, 1, H, dtype=np.float32)
    ts = [s[0] for s in stops]
    return np.stack([np.interp(t, ts, [s[1][c] for s in stops]) for c in range(3)], -1)[:, None, :].astype(np.float32)


# ---------------------------------------------------------------- second exposures (RGB 0..1)
_CACHE = {}


def pine(x, base, h, w, tiers, rng):
    def side(sgn):
        pts = []
        for i in range(1, tiers + 1):
            yb = base - h + h * i / tiers + rng.uniform(-0.2, 0.2) * h / tiers
            hw = w / 2 * (i / tiers) ** 0.85 * rng.uniform(0.75, 1.2)
            pts += [(x + sgn * hw, yb + 0.12 * h / tiers),                     # drooping branch tip
                    (x + sgn * hw * rng.uniform(0.55, 0.8), yb - 0.15 * h / tiers),
                    (x + sgn * hw * rng.uniform(0.2, 0.4), yb - 0.32 * h / tiers)]
        return pts
    right = side(1)
    left = list(reversed(side(-1)))
    trunk = [(x + w * 0.04, base), (x + w * 0.04, base + h * 0.06), (x - w * 0.04, base + h * 0.06), (x - w * 0.04, base)]
    return np.array([(x, base - h)] + right[:-1] + trunk + left[1:], np.float32)


def forest_layers(si):
    key = ("forest", si)
    if key not in _CACHE:
        rng = np.random.default_rng(1700 + si)
        layers = []
        # far -> near: (tree base y, mean height, colour)
        for d, (base, th) in enumerate([(0.58, 0.20), (0.66, 0.26), (0.76, 0.34), (0.90, 0.46)]):
            a = np.zeros((H, W + PAD), np.uint8)
            x = rng.uniform(-60, 0)
            while x < W + PAD + 60:
                h = H * th * rng.uniform(0.6, 1.25)
                wdt = h * rng.uniform(0.32, 0.42)
                b = H * base + rng.uniform(-0.03, 0.05) * H
                poly = pine(x, b, h, wdt, int(rng.integers(9, 15)), rng)
                cv2.fillPoly(a, [np.round(poly * 4).astype(np.int32)], 255, cv2.LINE_AA, shift=2)
                x += wdt * rng.uniform(0.35, 0.8)
            a[int(H * (base + 0.04)):, :] = 255             # ground under the row
            layers.append(cv2.GaussianBlur(a.astype(np.float32) / 255, (0, 0), [3.0, 2.0, 1.2, 2.2][d]))
        grain = fbm(1790 + si, H, W + PAD - 400, 0, cell=48, octaves=4)
        _CACHE[key] = (layers, np.pad(grain, ((0, 0), (0, 400)), mode='wrap'))
    return _CACHE[key]


def birds(img, n, seed, count=9, col=(0.22, 0.24, 0.27)):
    rng = np.random.default_rng(seed)
    cx, cy = rng.uniform(0.15, 0.6) * W, rng.uniform(0.12, 0.28) * H
    for i in range(count):
        x = (cx + rng.uniform(-160, 160) + n * 3.2) % (W + 200) - 100
        y = cy + rng.uniform(-70, 70) + 6 * np.sin(n * 0.5 + i)
        s = rng.uniform(7, 14)
        flap = 0.45 + 0.35 * np.sin(n * 1.3 + i * 1.7)
        pts = np.array([(x - s, y - s * flap), (x, y), (x + s, y - s * flap)], np.float32)
        cv2.polylines(img, [np.round(pts * 4).astype(np.int32)], False, col, 2, cv2.LINE_AA, shift=2)


def tex_forest(n, si):
    sky = vgrad([(0, (0.80, 0.86, 0.86)), (0.45, (0.95, 0.96, 0.93)), (1, (0.97, 0.95, 0.90))])
    img = np.broadcast_to(sky, (H, W, 3)).copy()
    fog = fbm(1750 + si, H, W, n * 0.9, cell=300)
    cols = [(0.70, 0.77, 0.77), (0.48, 0.57, 0.58), (0.26, 0.34, 0.35), (0.07, 0.11, 0.12)]
    layers, needles = forest_layers(si)
    for d, a in enumerate(layers):
        off = int(n * (0.6 + d * 0.9)) % PAD
        a = a[:, off:off + W]
        tone = (0.75 + 0.5 * needles[:, off:off + W])[..., None]          # needle / bark texture
        img = img * (1 - a[..., None]) + np.clip(np.array(cols[d], np.float32) * tone, 0, 1) * a[..., None]
        if d < 3:                                          # mist drifting between rows
            yy = np.linspace(0, 1, H, dtype=np.float32)[:, None]
            band = np.clip(1 - np.abs(yy - (0.62 + d * 0.1)) / 0.12, 0, 1) * (0.35 + 0.5 * fog)
            img = img * (1 - band[..., None] * 0.55) + np.array([0.94, 0.95, 0.93]) * band[..., None] * 0.55
    birds(img, n, 1760 + si)
    return img


def tex_clouds(n, si):
    sky = vgrad([(0, (0.30, 0.32, 0.55)), (0.35, (0.72, 0.50, 0.62)), (0.65, (0.98, 0.70, 0.55)), (1, (0.99, 0.86, 0.70))])
    c = fbm(3100 + si, H, W, n * 1.4, cell=420)
    d = fbm(3150 + si, H, W, n * 0.7, cell=200)
    dens = np.clip((c - 0.45) * 3.0, 0, 1)
    under = np.clip((d - 0.45) * 2.4, 0, 1) * dens            # lavender shaded undersides
    ccol = np.array([1.0, 0.97, 0.94], np.float32)
    shade = np.array([0.30, 0.26, 0.42], np.float32)
    img = sky * (1 - dens[..., None]) + ccol * dens[..., None]
    img = img * (1 - under[..., None] * 0.85) + shade * under[..., None] * 0.85
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    sun = np.exp(-(((xx - W * 0.68) / 260) ** 2 + ((yy - H * 0.55) / 260) ** 2))
    img = img + sun[..., None] * np.array([0.25, 0.16, 0.05])
    return np.clip(img, 0, 1)


def city_layers(si):
    key = ("city", si)
    if key not in _CACHE:
        rng = np.random.default_rng(6700 + si)
        layers = []
        for d, (top, var) in enumerate([(0.42, 0.10), (0.52, 0.12), (0.64, 0.14)]):
            a = np.zeros((H, W + PAD), np.float32)
            win = np.zeros((H, W + PAD), np.float32)
            x = 0
            while x < W + PAD:
                bw = int(rng.uniform(50, 150) * (0.7 + d * 0.25))
                y0 = int(H * (top + rng.uniform(-var, var)))
                a[y0:, x:x + bw] = 1
                if rng.random() < 0.3:                      # antenna / stepped crown
                    a[y0 - int(rng.uniform(20, 70)):y0, x + bw // 2 - 3:x + bw // 2 + 3] = 1
                if rng.random() < 0.4:
                    a[y0 - 30:y0, x + bw // 5:x + bw - bw // 5] = 1
                ws, gap = 6 + d * 2, 13 + d * 4
                for wy in range(y0 + 14, H, gap):
                    for wx in range(x + 8, x + bw - 10, gap):
                        if rng.random() < 0.32:
                            win[wy:wy + ws, wx:wx + ws] = rng.uniform(0.5, 1.0)
                x += bw + int(rng.uniform(0, 14))
            layers.append((cv2.GaussianBlur(a, (0, 0), 1.6 - d * 0.4), win))
        _CACHE[key] = layers
    return _CACHE[key]


def tex_city(n, si):
    sky = vgrad([(0, (0.18, 0.22, 0.42)), (0.35, (0.55, 0.50, 0.68)), (0.6, (0.98, 0.72, 0.58)), (1, (0.99, 0.86, 0.70))])
    img = np.broadcast_to(sky, (H, W, 3)).copy()
    cols = [(0.52, 0.48, 0.62), (0.28, 0.27, 0.42), (0.08, 0.09, 0.18)]
    flick = np.random.default_rng(6790 + n)
    for d, (a, win) in enumerate(city_layers(si)):
        off = int(n * (0.5 + d * 0.8)) % PAD
        a, wv = a[:, off:off + W], win[:, off:off + W]
        img = img * (1 - a[..., None]) + np.array(cols[d], np.float32) * a[..., None]
        on = wv * (flick.random((H // 16 + 1, W // 16 + 1)) > 0.06).repeat(16, 0).repeat(16, 1)[:H, :W]
        glow = np.array([1.0, 0.80, 0.45], np.float32) * (0.45 + 0.25 * d)
        img = img * (1 - on[..., None] * 0.9) + glow * on[..., None] * 0.9
    return np.clip(img, 0, 1)


def mountain_ridges(si):
    key = ("mtn", si)
    if key not in _CACHE:
        rng = np.random.default_rng(10100 + si)
        xs = np.arange(W + PAD, dtype=np.float32)
        ridges = []
        for d, base in enumerate([0.40, 0.52, 0.64, 0.80]):
            y = np.zeros_like(xs)
            amp, per = 0.14 - d * 0.015, 900.0
            for _ in range(6):
                ph = rng.uniform(0, 2 * np.pi)
                y += amp * H * np.abs(np.sin(xs / per * np.pi + ph)) ** 1.4 * rng.uniform(0.5, 1)
                amp *= 0.5
                per /= 2.1
            ridges.append(H * base + H * 0.12 - y)
        _CACHE[key] = ridges
    return _CACHE[key]


def tex_mountains(n, si):
    sky = vgrad([(0, (0.72, 0.80, 0.90)), (0.5, (0.93, 0.92, 0.92)), (1, (0.98, 0.94, 0.88))])
    img = np.broadcast_to(sky, (H, W, 3)).copy()
    yy = np.arange(H, dtype=np.float32)[:, None]
    cols = [(0.66, 0.72, 0.82), (0.45, 0.53, 0.66), (0.26, 0.32, 0.45), (0.09, 0.12, 0.19)]
    fog = fbm(10150 + si, H, W, n, cell=260)
    for d, ridge in enumerate(mountain_ridges(si)):
        off = int(n * (0.4 + d * 0.7)) % PAD
        r = ridge[off:off + W][None, :]
        a = np.clip((yy - r) / 2.0, 0, 1)
        shade = np.clip((yy - r) / (H * 0.25), 0, 1)[..., None] * 0.08    # slightly lighter at the base (mist)
        img = img * (1 - a[..., None]) + (np.array(cols[d], np.float32) + shade) * a[..., None]
        band = np.clip(1 - np.abs(yy - (r + H * 0.09)) / (H * 0.07), 0, 1) * (0.3 + 0.6 * fog) * a
        img = img * (1 - band[..., None] * 0.5) + np.array([0.93, 0.93, 0.94]) * band[..., None] * 0.5
    birds(img, n, 10160 + si, count=7, col=(0.2, 0.22, 0.3))
    return np.clip(img, 0, 1)


TEXTURES = {"forest": tex_forest, "clouds": tex_clouds, "city": tex_city, "mountains": tex_mountains}


# ---------------------------------------------------------------- frame
def heads(m):
    """Find heads from the matte: lowest-y peaks of the silhouette, head width from the row runs,
    stop at the neck dip / shoulder jump. Returns [(xc, y0, yneck, headw)]."""
    cols = m > 0.5
    has = cols.any(0)
    topy = np.where(has, cols.argmax(0), H).astype(np.float32)
    remaining = has.copy()
    out = []
    for _ in range(4):
        cand = np.flatnonzero(remaining & (topy < H * 0.85))
        if len(cand) < 12:
            break
        y0 = int(topy[cand].min())
        xs = cand[topy[cand] <= y0 + 4]
        grp = np.split(xs, np.flatnonzero(np.diff(xs) > 3) + 1)[0]
        x0 = int(grp[len(grp) // 2])
        row = cols[min(H - 1, y0 + 2)]
        l = x0 - (np.flatnonzero(~row[:x0][::-1])[:1].tolist() or [x0])[0]
        r = x0 + (np.flatnonzero(~row[x0:])[:1].tolist() or [W - x0])[0]
        if any(l <= h[0] <= r for h in out):           # a shoulder of a head we already have
            remaining[l:r] = False
            continue
        wmax, yneck, xc, wprev, grow = 1, None, x0, None, True
        for y in range(y0, min(H, y0 + int(H * 0.6))):
            row = cols[y]
            if not row[x0]:
                continue
            l = x0 - (np.flatnonzero(~row[:x0][::-1])[:1].tolist() or [x0])[0]
            r = x0 + (np.flatnonzero(~row[x0:])[:1].tolist() or [W - x0])[0]
            w = r - l
            dy = y - y0
            if wprev is not None and dy > 20 and w > wprev * 1.12 + 10:
                grow = False                            # sudden widening: shoulder or a merged neighbour
                if dy > 0.9 * wmax:
                    yneck = y
                    break
            wprev = w
            if grow and (dy < 1.0 * wmax or dy < 20):
                if w > wmax:
                    wmax, xc = w, (l + r) // 2
            elif dy < 0.9 * wmax:
                continue
            elif w < 0.85 * wmax or w > 1.7 * wmax or dy > 1.25 * wmax:
                yneck = y
                break
        yneck = yneck or min(H - 1, y0 + int(1.25 * wmax))
        if wmax >= 24:
            out.append((xc, y0, yneck, wmax))
        remaining[max(0, xc - int(wmax * 1.1)):xc + int(wmax * 1.1)] = False
        remaining[max(0, x0 - 12):x0 + 12] = False
    return out


def face_keep(rgb, m):
    """Soft map of faces to keep photographic: head ellipses, weighted toward skin inside them."""
    ell = np.zeros((H, W), np.float32)
    for xc, y0, yn, hw in heads(m):
        cy = int(y0 + (yn - y0) * 0.55)
        cv2.ellipse(ell, (int(xc), cy), (int(hw * 0.46), int((yn - y0) * 0.52)), 0, 0, 360, 1.0, -1, cv2.LINE_AA)
        ell = np.maximum(ell, 0)
    hw_med = max(20, np.median([h[3] for h in heads(m)] or [80]))
    ell = cv2.GaussianBlur(ell, (0, 0), hw_med * 0.10)
    ycc = cv2.cvtColor(rgb, cv2.COLOR_RGB2YCrCb)
    s = ((ycc[..., 1] > 135) & (ycc[..., 1] < 175) & (ycc[..., 2] > 80) & (ycc[..., 2] < 128) &
         (ycc[..., 0] > 60)).astype(np.float32)
    s = cv2.GaussianBlur(s, (0, 0), hw_med * 0.06)
    return np.clip(ell * (0.35 + 0.9 * s), 0, 1) * (m > 0.3)


def render(n):
    si, (first, last, kind, ground) = section_of(n)
    k = n - first
    rng = np.random.default_rng(17_000 + n)
    bgr = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png"))
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
    face = face_keep(rgb, m)
    alpha = cv2.GaussianBlur(m, (0, 0), 2.5)
    f = rgb.astype(np.float32) / 255

    # high-key warm mono portrait: faces bright and clean, clothes/hair pushed dark so the texture fills them
    lum = f @ np.array([0.30, 0.59, 0.11], np.float32)
    lum = np.clip((lum - 0.06) / 0.78, 0, 1)
    pf = np.clip(lum ** 0.75 * 1.08, 0, 1)
    pb = lum * 0.40
    p = pb + (pf - pb) * face
    port = p[..., None] * np.array([1.0, 0.96, 0.91], np.float32)
    port = port * (1 - 0.3 * face[..., None]) + np.clip(f * 1.1, 0, 1) * 0.3 * face[..., None]

    tex = TEXTURES[kind](n, si)
    tlum = tex @ np.array([0.30, 0.59, 0.11], np.float32)
    teff = tex * (1 - 0.82 * face[..., None])
    inside = 1 - (1 - port) * (1 - teff)                                  # screen
    inside = inside * (1 - 0.35 * (1 - tlum[..., None]) * (1 - face[..., None]))   # keep texture darks readable

    # ground
    paper = vgrad([(0, (0.96, 0.94, 0.90)), (1, (0.93, 0.90, 0.85))])
    bg = np.broadcast_to(paper, (H, W, 3)).copy()
    if ground == "ghost":
        g = cv2.GaussianBlur(f @ np.array([0.30, 0.59, 0.11], np.float32), (0, 0), 3)[..., None]
        bg = bg * 0.78 + g * 0.22 * np.array([0.98, 0.95, 0.9]) + 0.05
    # the second exposure bleeds softly past the silhouette (only its darks, multiplied)
    yy = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    bleed = np.clip(cv2.GaussianBlur(m, (0, 0), 45) * 0.9, 0, 1) * 0.45 + np.clip((yy - 0.72) / 0.28, 0, 1) * 0.35
    bg = bg * (1 - bleed[..., None]) + bg * tex * bleed[..., None]

    out = bg * (1 - alpha[..., None]) + inside * alpha[..., None]

    # bloom
    out = 1 - (1 - out) * (1 - cv2.GaussianBlur(out, (0, 0), 22) * 0.18)
    # red-orange halation where bright meets dark
    lo = out @ np.array([0.30, 0.59, 0.11], np.float32)
    hl = np.clip((lo - 0.72) / 0.28, 0, 1)
    halo = np.clip(cv2.GaussianBlur(hl, (0, 0), 9) - hl * 0.85, 0, 1) * (1 - lo) * 2.2
    out = out + halo[..., None] * np.array([0.55, 0.20, 0.08], np.float32) * (0.9 + 0.2 * rng.random())
    # light leak drifting along one edge, flickering
    xx = np.linspace(0, 1, W, dtype=np.float32)[None, :]
    side = (si % 2 == 0)
    lx = (1 - xx) if side else xx
    ly = 0.45 + 0.25 * np.sin(n * 0.07 + si)
    leak = np.exp(-((lx / 0.22) ** 2) - ((yy - ly) / 0.45) ** 2) * (0.30 + 0.12 * rng.random())
    out = 1 - (1 - out) * (1 - leak[..., None] * np.array([1.0, 0.52, 0.22], np.float32))
    # soft warm vignette + film grain (new every frame)
    vig = 1 - 0.10 * (((xx - 0.5) / 0.5) ** 2 + ((yy - 0.5) / 0.5) ** 2)
    out = out * vig[..., None]
    grain = cv2.GaussianBlur(rng.normal(0, 1, (H, W)).astype(np.float32), (0, 0), 0.7)
    out = out + grain[..., None] * 0.035 * (0.4 + out * (1 - out) * 2.4)
    out = np.clip(out, 0, 1)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), cv2.cvtColor((out * 255 + 0.5).astype(np.uint8), cv2.COLOR_RGB2BGR))
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    with Pool(6) as p:
        for n in p.imap_unordered(render, ONLY):
            print("frame", n)
