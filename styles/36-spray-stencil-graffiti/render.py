"""Spray-paint stencil graffiti restyle, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [frame numbers... | all]
Frames are frame_001.png ... ; masks are person mattes with the same names.
The room is replaced by a fixed street wall (whitewashed brick with peeled patches,
grime streaks, old torn paste-up posters). The people are cut as a 3-layer stencil
(white base, grey mid-tone, black key) from the real frame and sprayed onto the wall
with overspray halo, speckle, drips and slight layer misregistration. Earlier
frames stay on the wall as buffed-over ghosts (wall-painted animation look), and a
red spot-colour heart is stencilled in the emptiest part of the wall.
Spray, drips and registration change every frame.
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FRAMES, MASKS, OUT = sys.argv[1:4]
ARGS = sys.argv[4:]
HERE = os.path.dirname(os.path.abspath(__file__))
H, W = 1080, 1620
IMPACT = "/System/Library/Fonts/Supplemental/Impact.ttf"


def vnoise(rng, h, w, cell):
    a = rng.random((max(2, h // cell + 2), max(2, w // cell + 2))).astype(np.float32)
    return cv2.resize(a, (w, h), interpolation=cv2.INTER_CUBIC)


WALL = None


def wall():
    """Whitewashed brick wall with peeled paint, grime and torn poster remnants (fixed)."""
    global WALL
    if WALL is not None:
        return WALL
    rng = np.random.default_rng(42)
    bw, bh, mo = 132, 44, 7
    brick = np.zeros((H, W, 3), np.float32)
    mortar = np.ones((H, W), np.float32)
    for r in range(H // bh + 2):
        off = (r % 2) * bw // 2
        for c in range(-1, W // bw + 2):
            x0, y0 = c * bw + off, r * bh
            col = np.array([0.24, 0.30, 0.46]) * rng.uniform(0.75, 1.15) + rng.normal(0, 0.02, 3)
            cv2.rectangle(brick, (x0 + mo // 2, y0 + mo // 2), (x0 + bw - mo // 2, y0 + bh - mo // 2), col.tolist(), -1)
            cv2.rectangle(mortar, (x0 + mo // 2, y0 + mo // 2), (x0 + bw - mo // 2, y0 + bh - mo // 2), 0, -1)
    mortar = cv2.GaussianBlur(mortar, (0, 0), 1.2)
    rough = 0.85 + 0.3 * vnoise(rng, H, W, 3) * vnoise(rng, H, W, 11)
    brick *= rough[..., None]
    mcol = np.array([0.55, 0.57, 0.58], np.float32)
    raw = brick * (1 - mortar[..., None]) + mcol * mortar[..., None]
    # whitewash over the brick, peeled in patches
    wash = np.array([0.80, 0.82, 0.83], np.float32) * (0.92 + 0.1 * vnoise(rng, H, W, 40))[..., None]
    wash_m = (vnoise(rng, H, W, 160) * 0.7 + vnoise(rng, H, W, 30) * 0.3) > 0.27
    wash_m = cv2.GaussianBlur(wash_m.astype(np.float32), (0, 0), 1.0)
    # brick relief shows through the paint
    relief = 1 - 0.18 * mortar - 0.05 * (1 - rough)
    painted = wash * relief[..., None]
    w = painted * wash_m[..., None] + raw * (1 - wash_m[..., None])
    # grime: rain streaks from the top, dirt near the ground
    streak = cv2.resize(rng.random((1, W // 6)).astype(np.float32), (W, H), interpolation=cv2.INTER_LINEAR)
    streak = cv2.GaussianBlur(streak, (0, 0), 3) ** 3 * np.linspace(1, 0.2, H)[:, None]
    ground = np.clip((np.arange(H)[:, None] - H * 0.8) / (H * 0.2), 0, 1) ** 1.5
    w *= (1 - 0.25 * streak - 0.3 * ground * vnoise(rng, H, W, 20))[..., None]
    # torn paste-up poster remnants, top-left and right edge
    pos = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(pos)
    for (cx, cy, pw, ph) in [(150, 120, 330, 420), (1540, 520, 260, 360), (1180, 60, 220, 180)]:
        pts = []
        for k in range(28):
            a = k / 28 * 2 * np.pi
            rx, ry = pw / 2 * rng.uniform(0.8, 1.05), ph / 2 * rng.uniform(0.8, 1.05)
            ca, sa = np.cos(a), np.sin(a)
            sq = 1 / max(abs(ca), abs(sa))
            pts.append((cx + rx * ca * sq, cy + ry * sa * sq))
        d.polygon(pts, fill=255)
    pm = np.array(pos).astype(np.float32) / 255
    # torn: ragged only near the poster edge, a few rips inward
    inner = cv2.erode((pm > 0.5).astype(np.uint8), np.ones((41, 41), np.uint8)).astype(np.float32)
    pm *= np.maximum(inner, (vnoise(rng, H, W, 9) > 0.45).astype(np.float32))
    pm = cv2.morphologyEx(pm, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    paper = np.array([0.74, 0.83, 0.87], np.float32) * (0.9 + 0.12 * vnoise(rng, H, W, 6))[..., None]
    # faded old print on the posters: grey blocks of headline / text lines
    yy = np.arange(H)[:, None]
    xx0 = np.arange(W)[None]
    lines = ((yy // 22) % 2 == 0) & (vnoise(rng, H, W, 60) > 0.45) & ((xx0 // 7) % 9 != 0)
    paper = np.where(lines[..., None], paper * 0.72, paper)
    edge = cv2.morphologyEx((pm > 0.5).astype(np.uint8), cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8)).astype(np.float32)
    w = w * (1 - pm[..., None]) + paper * pm[..., None]
    w = w * (1 - 0.35 * cv2.GaussianBlur(edge, (0, 0), 2)[..., None])
    # light from the upper left
    xx = np.arange(W)[None]
    w *= (1.08 - 0.18 * (xx / W) * 0.6 - 0.18 * (yy / H) * 0.5)[..., None]
    WALL = w.astype(np.float32)
    return WALL


HEART = None


def heart_slot():
    global HEART
    if HEART is not None:
        return HEART
    path = os.path.join(HERE, "heart_slot.txt")
    if os.path.exists(path):
        HEART = tuple(int(v) for v in open(path).read().split())
        return HEART
    acc = np.zeros((H, W), np.float32)
    for n in range(1, 180, 6):
        acc += cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), 0).astype(np.float32) / 255
    best = None
    for y in range(80, 520, 20):
        for x in range(120, W - 200, 20):
            cost = acc[y - 70:y + 90, x - 90:x + 90].sum()
            if best is None or cost < best[0]:
                best = (cost, x, y)
    HEART = (best[1], best[2])
    open(path, "w").write(f"{HEART[0]} {HEART[1]}")
    return HEART


def heart_mask():
    x, y = heart_slot()
    lay = np.zeros((H, W), np.uint8)
    t = np.linspace(0, 2 * np.pi, 200)
    hx = 16 * np.sin(t) ** 3
    hy = -(13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t))
    pts = np.stack([x + hx * 4.6, y + hy * 4.6], 1).astype(np.int32)
    cv2.fillPoly(lay, [pts], 255)
    # balloon string down-left, and a little knot
    cv2.polylines(lay, [np.array([[x, y + 62], [x - 10, y + 120], [x + 8, y + 190], [x - 6, y + 260]], np.int32)],
                  False, 255, 3, cv2.LINE_AA)
    return lay.astype(np.float32) / 255


def cut_layers(img, m):
    """Three stencil sheets from the frame: base (whole figure), mid tones, darks."""
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    g = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(6, 6)).apply(g)
    g = cv2.bilateralFilter(g, 9, 40, 9)
    g = cv2.GaussianBlur(g, (0, 0), 2.2).astype(np.float32)
    person = cv2.GaussianBlur(m, (0, 0), 2.5) > 0.5
    dark = (g < 78) & person
    mid = (g < 140) & person

    def clean(b, k):
        u = b.astype(np.uint8)
        u = cv2.morphologyEx(u, cv2.MORPH_OPEN, np.ones((k, k), np.uint8))
        u = cv2.morphologyEx(u, cv2.MORPH_CLOSE, np.ones((k, k), np.uint8))
        # knife-cut curves: blur + threshold gives smooth cut edges
        return (cv2.GaussianBlur(u.astype(np.float32), (0, 0), 1.6) > 0.5).astype(np.float32)

    return clean(person, 5), clean(mid, 4), clean(dark, 3)


def spray(canvas, layer, color, rng, halo=7.0, dens=1.0, shift=(0, 0)):
    """Spray one stencil layer: solid core + speckled overspray halo + paint grain."""
    lay = np.roll(layer, shift, (0, 1))
    blur = cv2.GaussianBlur(lay, (0, 0), halo)
    speck = (rng.random((H, W)) < 0.55).astype(np.float32)
    over = np.clip(blur - lay, 0, 1) * 1.6 * speck * dens
    grain = 0.9 + 0.1 * rng.random((H, W)).astype(np.float32)
    a = np.clip(lay * (0.93 + 0.07 * vnoise(rng, H, W, 30)) + over, 0, 1)[..., None]
    canvas[:] = canvas * (1 - a) + (color[None, None] * grain[..., None]) * a


def drips(canvas, layer, color, rng, count):
    """Paint runs falling from the lower edges of a sprayed layer."""
    lu = (layer > 0.5).astype(np.uint8)
    bottom = (lu[:-1] == 1) & (lu[1:] == 0)
    ys, xs = np.nonzero(bottom)
    if not len(ys):
        return
    lay = np.zeros((H, W), np.uint8)
    for k in rng.choice(len(ys), size=min(count, len(ys)), replace=False):
        x, y = int(xs[k]), int(ys[k])
        L = int(rng.gamma(2.0, 28))
        wdt = int(rng.integers(2, 5))
        x2 = x + int(rng.integers(-2, 3))
        cv2.line(lay, (x, y), (x2, min(H - 1, y + L)), 255, wdt, cv2.LINE_AA)
        cv2.circle(lay, (x2, min(H - 1, y + L)), wdt + 1, 255, -1, cv2.LINE_AA)
    a = lay.astype(np.float32)[..., None] / 255 * 0.95
    canvas[:] = canvas * (1 - a) + color * a


def render(n):
    rng = np.random.default_rng(n * 6151)
    img = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png"))
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), 0).astype(np.float32) / 255
    canvas = wall().copy()

    # ghosts of earlier frames, buffed over with slightly different whites
    for k, alpha in ((9, 0.55), (5, 0.7)):
        pn = max(1, n - k)
        if pn == n:
            continue
        pm = cv2.imread(os.path.join(MASKS, f"frame_{pn:03d}.png"), 0).astype(np.float32) / 255
        pimg = cv2.imread(os.path.join(FRAMES, f"frame_{pn:03d}.png"))
        _, _, pdark = cut_layers(pimg, pm)
        buff = cv2.dilate((pm > 0.5).astype(np.uint8), np.ones((25, 25), np.uint8)).astype(np.float32)
        buff = cv2.GaussianBlur(buff, (0, 0), 4) * (0.8 + 0.2 * vnoise(rng, H, W, 12))
        tone = np.array([0.86, 0.87, 0.88], np.float32) * (0.96 + 0.04 * rng.random())
        ab = (buff * alpha)[..., None]
        canvas = canvas * (1 - ab) + tone * ab
        gd = (cv2.GaussianBlur(pdark, (0, 0), 2) * 0.10 * alpha)[..., None]
        canvas = canvas * (1 - gd) + np.float32(0.15) * gd

    # red spot-colour heart balloon
    hm = heart_mask()
    spray(canvas, hm, np.array([0.13, 0.12, 0.80], np.float32), rng, halo=5, dens=0.8,
          shift=tuple(int(v) for v in rng.integers(-1, 2, 2)))
    drips(canvas, hm, np.array([0.13, 0.12, 0.75], np.float32), rng, int(rng.integers(1, 4)))

    base, mid, dark = cut_layers(img, m)
    white = np.array([0.94, 0.95, 0.95], np.float32)
    grey = np.array([0.52, 0.52, 0.53], np.float32)
    black = np.array([0.07, 0.07, 0.08], np.float32)
    j = lambda: tuple(int(v) for v in rng.integers(-3, 4, 2))
    spray(canvas, base, white, rng, halo=4, dens=0.35, shift=j())
    spray(canvas, mid, grey, rng, halo=6, dens=0.8, shift=j())
    spray(canvas, dark, black, rng, halo=5, dens=1.0, shift=(0, 0))
    drips(canvas, dark, black, rng, int(rng.integers(10, 22)))
    drips(canvas, mid, grey, rng, int(rng.integers(3, 8)))

    # stencil tag: small cut lettering with stencil bridges, bottom right
    lay = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(lay)
    f = ImageFont.truetype(IMPACT, 54) if os.path.exists(IMPACT) else ImageFont.load_default()
    tx, ty = 1220, 980
    d.text((tx, ty), "STAY STILL", font=f, fill=255)
    tm = np.array(lay).astype(np.float32) / 255
    for bx in range(tx, tx + 330, 33):                      # stencil bridges
        tm[ty:ty + 75, bx:bx + 4] *= (rng.random() > 0.5)
    spray(canvas, tm, black, rng, halo=3, dens=0.7, shift=j())

    # sunlight across the wall, fine film of dust
    out = np.clip(canvas * 255, 0, 255).astype(np.uint8)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), out)
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    heart_slot()
    nums = list(range(1, 180)) if (not ARGS or ARGS == ["all"]) else [int(a) for a in ARGS]
    with Pool(6) as p:
        for n in p.imap_unordered(render, nums):
            print(n, end=" ", flush=True)
    print()
