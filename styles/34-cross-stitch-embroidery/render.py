"""Cross-stitch embroidery restyle, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [frame numbers... | all]
Frames are frame_001.png ... ; masks are person mattes with the same names.
The frame is charted onto a fixed 15 px aida grid, every cell snapped to a fixed
stranded-cotton palette (k-means over the whole clip, cached in palette.npy) and
sewn as two crossing threads with sheen and twist. People get a dark backstitch
outline; one corner of the room is left unfinished (bare aida, half stitches).
The cloth sits in a wooden hoop. Stitch variants, dither and loose threads are
re-drawn every frame, so the embroidery is "re-sewn" 12 times a second.
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np

FRAMES, MASKS, OUT = sys.argv[1:4]
ARGS = sys.argv[4:]
HERE = os.path.dirname(os.path.abspath(__file__))
C = 15                       # stitch cell in px (aida 'count')
H, W = 1080, 1620
GH, GW = H // C, W // C
NPAL = 30
SS = 4                       # sprite supersampling


def build_palette():
    path = os.path.join(HERE, "palette.npy")
    if os.path.exists(path):
        return np.load(path)
    samp = []
    for n in range(1, 180, 8):
        im = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png"))
        sm = cv2.resize(im, (GW, GH), interpolation=cv2.INTER_AREA)
        samp.append(cv2.cvtColor(sm, cv2.COLOR_BGR2LAB).reshape(-1, 3))
    data = np.concatenate(samp).astype(np.float32)
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 60, 0.5)
    cv2.setRNGSeed(7)
    _, _, cen = cv2.kmeans(data, NPAL, None, crit, 4, cv2.KMEANS_PP_CENTERS)
    lab = cen[np.argsort(cen[:, 0])]
    # stranded cotton is a little more saturated than the video
    lab[:, 1:] = 128 + (lab[:, 1:] - 128) * 1.5
    lab[:, 0] = np.clip((lab[:, 0] - 128) * 1.15 + 134, 0, 255)
    np.save(path, lab)
    return lab


def thread_sprite(rng, diag):
    """Shade (0..~1.3) and alpha of one diagonal thread inside a C x C cell."""
    s = C * SS
    yy, xx = np.mgrid[0:s, 0:s].astype(np.float32) + 0.5
    j = rng.normal(0, 0.06 * s, 4)
    if diag == 0:   # '/' bottom-left -> top-right
        p0, p1 = np.array([0.6 + j[0], s - 0.6 + j[1]]), np.array([s - 0.6 + j[2], 0.6 + j[3]])
    else:           # '\' top-left -> bottom-right
        p0, p1 = np.array([0.6 + j[0], 0.6 + j[1]]), np.array([s - 0.6 + j[2], s - 0.6 + j[3]])
    d = p1 - p0
    L = np.linalg.norm(d)
    u = d / L
    nrm = np.array([-u[1], u[0]])
    t = (xx - p0[0]) * u[0] + (yy - p0[1]) * u[1]
    q = (xx - p0[0]) * nrm[0] + (yy - p0[1]) * nrm[1]
    half = s * rng.uniform(0.27, 0.31)
    # thread tapers where it dives into the hole
    taper = np.clip(np.minimum(t, L - t) / (0.22 * s), 0.55, 1.0)
    hw = half * taper
    a = np.clip((hw - np.abs(q)) / (0.5 * SS), 0, 1)
    # round cross-section: bright ridge slightly off-centre (light from top-left)
    r = np.clip(q / np.maximum(hw, 1e-3), -1, 1)
    shade = 0.62 + 0.5 * np.sqrt(np.clip(1 - (r + 0.25) ** 2, 0, 1))
    # 2-ply twist striations across the thread
    ph = rng.uniform(0, 6.28)
    shade *= 0.86 + 0.14 * np.cos((t * 0.9 + q * 1.6) / SS * 1.2 + ph)
    shade *= np.clip(0.75 + 0.25 * taper, 0, 1)
    sh = cv2.resize(shade, (C, C), interpolation=cv2.INTER_AREA)
    al = cv2.resize(a, (C, C), interpolation=cv2.INTER_AREA)
    return sh, al


SPRITES = None


def sprites(nv=8):
    global SPRITES
    if SPRITES is None:
        rng = np.random.default_rng(3)
        out = []
        for _ in range(nv):
            sb, ab = thread_sprite(rng, 0)
            st, at = thread_sprite(rng, 1)
            out.append((sb, ab, st, at))
        SPRITES = [np.stack([o[k] for o in out]) for k in range(4)]
    return SPRITES


def tile(arr, idx):
    """arr: (V, C, C); idx: (GH, GW) -> (GH*C, GW*C)."""
    t = arr[idx]                       # GH, GW, C, C
    return t.transpose(0, 2, 1, 3).reshape(GH * C, GW * C)


def aida(rng):
    """Cream aida cloth: square thread blocks, dark holes at the cell corners."""
    yy, xx = np.mgrid[0:H, 0:W]
    fx, fy = (xx % C) / C, (yy % C) / C
    block = (np.sin(fx * np.pi) * np.sin(fy * np.pi)) ** 0.35
    weave = 0.93 + 0.07 * np.sign(np.sin(xx * np.pi * 2 / (C / 2.5))) * np.sign(np.sin(yy * np.pi * 2 / (C / 2.5)))
    dx = np.minimum(fx, 1 - fx)
    dy = np.minimum(fy, 1 - fy)
    hole = np.exp(-((dx ** 2 + dy ** 2) / 0.012))
    base = np.array([196, 222, 232], np.float32) / 255  # BGR cream
    lum = (0.78 + 0.22 * block) * weave * (1 - 0.55 * hole)
    lum *= 1 + 0.04 * cv2.GaussianBlur(rng.normal(0, 1, (H, W)).astype(np.float32), (0, 0), 6) * 6
    return base[None, None] * lum[..., None]


def grid_mask(m):
    return cv2.resize(m, (GW, GH), interpolation=cv2.INTER_AREA)


def chart(img, m, lab_pal, rng):
    """Cell colours -> palette indices; small per-frame dither re-sews boundary stitches."""
    sm = cv2.resize(img, (GW, GH), interpolation=cv2.INTER_AREA)
    lab = cv2.cvtColor(sm, cv2.COLOR_BGR2LAB).astype(np.float32)
    lab[..., 1:] = 128 + (lab[..., 1:] - 128) * 1.5
    lab[..., 0] = np.clip((lab[..., 0] - 128) * 1.15 + 134, 0, 255)
    lab += rng.normal(0, 2.2, lab.shape).astype(np.float32)
    d = ((lab[:, :, None, :] - lab_pal[None, None]) ** 2).sum(-1)
    return d.argmin(-1)


def backstitch(canvas, mg, rng, color):
    """Dark backstitch along the person outline, on cell edges, one stitch per cell side."""
    inside = mg > 0.5
    segs = []
    h, w = inside.shape
    vert = inside[:, 1:] != inside[:, :-1]
    hor = inside[1:, :] != inside[:-1, :]
    for y, x in zip(*np.nonzero(vert)):
        segs.append(((x + 1) * C, y * C, (x + 1) * C, (y + 1) * C))
    for y, x in zip(*np.nonzero(hor)):
        segs.append((x * C, (y + 1) * C, (x + 1) * C, (y + 1) * C))
    lay = np.zeros((H, W), np.uint8)
    hi = np.zeros((H, W), np.uint8)
    for x0, y0, x1, y1 in segs:
        j = rng.integers(-1, 2, 4)
        cv2.line(lay, (x0 + j[0], y0 + j[1]), (x1 + j[2], y1 + j[3]), 255, 2, cv2.LINE_AA)
        cv2.line(hi, (x0 + j[0] - 1, y0 + j[1] - 1), (x1 + j[2] - 1, y1 + j[3] - 1), 255, 1, cv2.LINE_AA)
    a = lay.astype(np.float32)[..., None] / 255
    hl = hi.astype(np.float32)[..., None] / 255 * a
    sh = cv2.GaussianBlur(lay, (0, 0), 1.5).astype(np.float32)[..., None] / 255
    canvas[:] = canvas * (1 - 0.35 * np.roll(sh, (2, 2), (0, 1)))
    canvas[:] = canvas * (1 - a) + color * a
    canvas[:] = canvas + hl * 0.25


def bezier(p, n=60):
    t = np.linspace(0, 1, n)[:, None]
    return ((1 - t) ** 3 * p[0] + 3 * (1 - t) ** 2 * t * p[1] + 3 * (1 - t) * t ** 2 * p[2] + t ** 3 * p[3])


def loose_threads(canvas, rng, pal_bgr, n_threads, region):
    """Thread ends left hanging in the unfinished corner (region: bool pixel mask)."""
    ys, xs = np.nonzero(region[::8, ::8])
    if not len(ys):
        return
    for _ in range(n_threads):
        k = rng.integers(0, len(ys))
        x0, y0 = xs[k] * 8.0, ys[k] * 8.0
        pts = np.array([[x0, y0]] + [[x0 + rng.uniform(-140, 140), y0 + rng.uniform(-60, 160)] for _ in range(3)])
        curve = bezier(pts).astype(np.int32)
        col = pal_bgr[rng.integers(len(pal_bgr) // 3, len(pal_bgr))]
        lay = np.zeros((H, W), np.uint8)
        cv2.polylines(lay, [curve], False, 255, 4, cv2.LINE_AA)
        a = lay.astype(np.float32)[..., None] / 255
        sh = np.roll(cv2.GaussianBlur(lay, (0, 0), 2.5), (4, 3), (0, 1)).astype(np.float32)[..., None] / 255
        canvas[:] = canvas * (1 - 0.4 * sh)
        twist = 0.85 + 0.25 * (np.sin((np.arange(W)[None] + np.arange(H)[:, None]) * 0.9) > 0)
        canvas[:] = canvas * (1 - a) + (col[None, None] * twist[..., None]) * a


def needle(canvas, rng, t, region, m):
    """A needle parked in the bare cloth, its thread trailing; moves every two seconds."""
    r = np.random.default_rng(1000 + t // 24)
    keep = cv2.dilate((m > 0.3).astype(np.uint8), np.ones((61, 61), np.uint8)) == 0
    ok = region & keep
    x, y = 1300, 200
    for _ in range(80):
        cx_, cy_ = int(r.uniform(260, 1360)), int(r.uniform(60, 300))
        if ok[cy_, cx_] and ok[min(H - 1, cy_ + 60), min(W - 1, cx_ + 150)]:
            x, y = cx_, cy_ + 120
            break
    ang = r.uniform(-0.7, -0.35)
    L = 220
    x1, y1 = int(x + L * np.cos(ang)), int(y + L * np.sin(ang))
    lay = np.zeros((H, W), np.uint8)
    cv2.line(lay, (x, y), (x1, y1), 255, 6, cv2.LINE_AA)
    sh = np.roll(cv2.GaussianBlur(lay, (0, 0), 4), (8, 6), (0, 1)).astype(np.float32)[..., None] / 255
    canvas[:] = canvas * (1 - 0.45 * sh)
    a = lay.astype(np.float32)[..., None] / 255
    steel = np.array([0.42, 0.40, 0.38], np.float32)
    canvas[:] = canvas * (1 - a) + steel * a
    hi = np.zeros((H, W), np.uint8)
    cv2.line(hi, (x, y - 2), (x1, y1 - 2), 255, 1, cv2.LINE_AA)
    canvas[:] = np.minimum(1.2, canvas + hi.astype(np.float32)[..., None] / 255 * 0.5)
    # eye of the needle
    ex, ey = int(x + (L - 22) * np.cos(ang)), int(y + (L - 22) * np.sin(ang))
    cv2.ellipse(canvas, (ex, ey), (8, 2), np.degrees(ang), 0, 360, (0.2, 0.2, 0.22), 1, cv2.LINE_AA)
    # thread from the eye back into the cloth
    pts = np.array([[ex, ey], [ex + 60, ey - 90], [x - 120, y - 140 + rng.uniform(-8, 8)], [x - 160, y - 30]])
    curve = bezier(pts).astype(np.int32)
    tl = np.zeros((H, W), np.uint8)
    cv2.polylines(tl, [curve], False, 255, 3, cv2.LINE_AA)
    ta = tl.astype(np.float32)[..., None] / 255
    canvas[:] = canvas * (1 - ta) + np.array([0.18, 0.16, 0.62], np.float32) * ta


def hoop(canvas, rng):
    """Wooden embroidery hoop: cloth inside, gathered cloth + wooden table outside."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    cx, cy = W / 2, H / 2 + 20
    R = 890
    d = np.sqrt(((xx - cx) * 1.0) ** 2 + ((yy - cy) * 1.0) ** 2)
    # table outside
    grain = 0.5 + 0.5 * np.sin(yy * 0.05 + 8 * cv2.GaussianBlur(rng.normal(0, 1, (H, W)).astype(np.float32), (0, 0), 25) * 6)
    table = np.stack([0.20 + 0.06 * grain, 0.30 + 0.08 * grain, 0.44 + 0.10 * grain], -1)
    out = d > R + 34
    canvas[out] = table[out]
    ring = (d > R - 4) & (d <= R + 34)
    tt = np.clip((d - (R - 4)) / 38, 0, 1)
    wood = np.array([0.42, 0.62, 0.80], np.float32)
    prof = (0.65 + 0.55 * np.clip(np.sin(tt * np.pi), 0, 1) ** 0.6)[..., None]
    wgrain = (0.93 + 0.07 * np.sin(np.arctan2(yy - cy, xx - cx) * 40 + tt * 3 + 2 * np.sin(np.arctan2(yy - cy, xx - cx) * 7)))[..., None]
    canvas[ring] = (wood * prof * wgrain)[ring]
    # shadow of the ring on the cloth and the cloth dip near the ring
    inner = np.clip((R - d) / 60, 0, 1)
    canvas *= np.where(d <= R - 4, 0.72 + 0.28 * inner, 1)[..., None]
    # brass screw clasp at the top
    cv2.rectangle(canvas, (int(cx - 34), int(cy - R - 70)), (int(cx + 34), int(cy - R + 6)), (0.25, 0.55, 0.70), -1)
    cv2.rectangle(canvas, (int(cx - 34), int(cy - R - 70)), (int(cx + 34), int(cy - R + 6)), (0.12, 0.25, 0.32), 2)
    cv2.circle(canvas, (int(cx), int(cy - R - 34)), 16, (0.35, 0.72, 0.86), -1)


def render(n):
    rng = np.random.default_rng(n * 7919)
    lab_pal = build_palette()
    pal_bgr = cv2.cvtColor(np.clip(lab_pal[None], 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)[0].astype(np.float32) / 255
    img = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png"))
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), 0).astype(np.float32) / 255
    mg = grid_mask(m)
    idx = chart(img, m, lab_pal, rng)

    sb, ab, st, at = sprites()
    vb = rng.integers(0, len(sb), (GH, GW))
    vt = rng.integers(0, len(st), (GH, GW))
    SB, AB, ST, AT = tile(sb, vb), tile(ab, vb), tile(st, vt), tile(at, vt)

    # stitched / half-stitched / bare cells: the top band of the room is still unfinished,
    # the heads are stitched first and emerge from bare cloth
    gy, gx = np.mgrid[0:GH, 0:GW].astype(np.float32)
    lowf = cv2.resize(np.random.default_rng(11).random((6, 9)).astype(np.float32), (GW, GH), interpolation=cv2.INTER_CUBIC)
    field = 1.0 - (gy / GH) * 2.4 + 0.45 * (lowf - 0.5) + rng.normal(0, 0.025, (GH, GW))
    person = mg > 0.3
    bare = (field > 0.62) & ~person
    half = (field > 0.52) & ~bare & ~person
    full_b = np.kron(~bare, np.ones((C, C), bool))
    full_t = np.kron(~bare & ~half, np.ones((C, C), bool))

    col = pal_bgr[idx]                                     # GH, GW, 3
    colp = np.repeat(np.repeat(col, C, 0), C, 1)
    canvas = aida(np.random.default_rng(5))
    # contact shadow of the threads on the cloth
    cover = np.maximum(AB * full_b, AT * full_t)
    shadow = np.roll(cv2.GaussianBlur(cover, (0, 0), 1.6), (2, 2), (0, 1))
    canvas *= (1 - 0.45 * shadow)[..., None]
    a1 = (AB * full_b)[..., None]
    canvas = canvas * (1 - a1) + colp * SB[..., None] * a1
    # top thread a hair darker where it crosses (shadow of the crossing)
    a2 = (AT * full_t)[..., None]
    canvas = canvas * (1 - a2) + colp * ST[..., None] * 1.02 * a2

    dark = pal_bgr[0] * 0.6
    backstitch(canvas, mg, rng, dark)
    loose_threads(canvas, rng, pal_bgr, rng.integers(2, 5), np.kron(bare | half, np.ones((C, C), bool)))
    needle(canvas, rng, n, np.kron(bare | half, np.ones((C, C), bool)), m)
    hoop(canvas, np.random.default_rng(9))
    # soft raking daylight from the upper left
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    light = 1.06 - 0.16 * ((xx / W) * 0.6 + (yy / H) * 0.7) + rng.normal(0, 0.006)
    canvas *= light[..., None]
    out = np.clip(canvas * 255, 0, 255).astype(np.uint8)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), out)
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    build_palette()
    nums = list(range(1, 180)) if (not ARGS or ARGS == ["all"]) else [int(a) for a in ARGS]
    with Pool(8) as p:
        for n in p.imap_unordered(render, nums):
            print(n, end=" ", flush=True)
    print()
