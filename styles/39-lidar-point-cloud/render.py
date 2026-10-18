"""LiDAR point-cloud scan restyle, frame by frame.

usage: python -I render.py [frame numbers... | all]   (default: the six sheet frames)
       RENDER_OUT=/tmp/prompt-video-render/39-lidar-point-cloud python -I render.py all   -> full clip for make_video.py
Reads ../../_source/frames + ../../_source/masks, writes ./frames/frame_NNN.png.

Pipeline per frame: fake depth (people from the matte, nearer person = bigger head, bodies
bulge toward the camera, room as a far plane) -> resample the frame as tens of thousands of
points (dense on people, sparse on the room, jittered and partly dropped every frame) ->
project through a slowly orbiting virtual camera (parallax) -> colour by depth / RGB / ice mono
per section, depth-slice contour bands, a scan sweep that lights the points it passes ->
splat on black with a soft glow and a thin viewer HUD.
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "..", "_source")
FRAMES, MASKS = os.path.join(SRC, "frames"), os.path.join(SRC, "masks")
OUT = os.environ.get("RENDER_OUT", os.path.join(HERE, "frames"))
ONLY = (list(range(1, 180)) if sys.argv[1:] == ["all"] else [int(a) for a in sys.argv[1:]]) or [13, 49, 85, 109, 145, 178]
W, H = 1620, 1080
# (first, last, mode): depth colormap -> true-colour RGB scan -> ice-blue ghost scan -> depth
SECTIONS = [(1, 60, "depth"), (61, 108, "rgb"), (109, 150, "ice"), (151, 999, "depth")]
SWEEP = 30                                  # frames per top-to-bottom scan pass

TURBO = cv2.applyColorMap(np.arange(256, dtype=np.uint8)[:, None], cv2.COLORMAP_TURBO)[:, 0].astype(np.float32) / 255


def mode_of(n):
    for a, b, m in SECTIONS:
        if a <= n <= b:
            return m
    return "depth"


def font(size):
    try:
        return ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", size, index=0)
    except OSError:
        return ImageFont.load_default()


def heads(m):  # silhouette head finder, adapted from styles/17 render.py
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
        if any(l <= h[0] <= r for h in out):
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
                grow = False
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


def depth_map(bgr, m):
    """0 = near, 1 = far. Not metric: just enough structure for parallax, colour and slices."""
    lum = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    # room: far wall, slightly nearer toward the frame bottom and the sides, faint relief
    room = 0.86 - 0.10 * (yy / H) - 0.05 * np.abs(xx / W - 0.5) + 0.06 * (cv2.GaussianBlur(lum, (0, 0), 20) - 0.5)
    hs = heads(m)
    if hs:
        widths = np.array([h[3] for h in hs], np.float32)
        base = np.clip(0.62 - 0.45 * (widths / widths.max()) ** 1.3, 0.1, 0.6)   # biggest head = nearest
        xcs = np.array([h[0] for h in hs], np.float32)
        dist = np.abs(xx[..., None] - xcs) / widths
        person = base[np.argmin(dist, -1)]
    else:
        person = np.full((H, W), 0.3, np.float32)
    mb = (m > 0.5).astype(np.uint8)
    dt = cv2.distanceTransform(mb, cv2.DIST_L2, 5)
    bulge = np.clip(dt / 90.0, 0, 1) ** 0.6
    person = person - 0.09 * bulge + 0.035 * (cv2.GaussianBlur(lum, (0, 0), 3) - 0.5)
    ms = cv2.GaussianBlur(m, (0, 0), 1.5)
    return np.clip(person * ms + room * (1 - ms), 0, 1), lum


_fixed = np.random.default_rng(39)
GRIDS = []
for _step in (3, 5):
    _gy, _gx = np.mgrid[0:H:_step, 0:W:_step]
    _gx = (_gx + _fixed.integers(0, _step, _gx.shape)).clip(0, W - 1).ravel()
    _gy = (_gy + _fixed.integers(0, _step, _gy.shape)).clip(0, H - 1).ravel()
    GRIDS.append((_gx, _gy, _fixed.random(_gx.size)))


def sample(m, lum, rng):
    """Point positions: a fixed jittered grid (so the cloud is stable), dense on people, sparse on
    the room; about 10% of the points flicker in/out every frame."""
    pts = []
    for (gx, gy, keepv), sel, keep in zip(GRIDS, (m > 0.5, m <= 0.5), (0.80, 0.40)):
        flick = rng.random(gx.size) < 0.10
        kv = np.where(flick, rng.random(gx.size), keepv)
        ok = sel[gy, gx] & (kv < keep)
        pts.append((gx[ok], gy[ok]))
    x = np.concatenate([p[0] for p in pts])
    y = np.concatenate([p[1] for p in pts])
    # missed beams: a few thin full-width rows where this pass returned little
    for _ in range(int(rng.integers(2, 5))):
        cy, rh = rng.integers(0, H), rng.integers(2, 7)
        hole = (np.abs(y - cy) < rh) & (rng.random(x.size) < 0.7)
        x, y = x[~hole], y[~hole]
    return x, y


def splat(canvas, x, y, col, size):
    xi, yi = np.round(x).astype(int), np.round(y).astype(int)
    for dy in range(size):
        for dx in range(size):
            xx, yy = xi + dx, yi + dy
            ok = (xx >= 0) & (xx < W) & (yy >= 0) & (yy < H)
            np.maximum.at(canvas, (yy[ok], xx[ok]), col[ok])


def grid_floor(img, ang):
    """Faint viewer ground grid, drifting with the orbit."""
    g = np.zeros((H, W), np.uint8)
    hz = int(H * 0.70)
    for i in range(-24, 25):
        x0 = W / 2 + i * 70 + ang * 900
        cv2.line(g, (int(W / 2 + (x0 - W / 2) * 0.15), hz), (int(x0 * 1.0 + (x0 - W / 2) * 1.6), H), 255, 1, cv2.LINE_AA)
    for k in range(1, 9):
        y = hz + int((H - hz) * (k / 9) ** 1.8)
        cv2.line(g, (0, y), (W, y), 255, 1, cv2.LINE_AA)
    img += (g.astype(np.float32) / 255 * 0.07)[..., None] * np.array([1.0, 0.9, 0.6], np.float32)


def hud(img, n, npts, mode, scan):
    pil = Image.fromarray((np.clip(img, 0, 1)[..., ::-1] * 255).astype(np.uint8))
    d = ImageDraw.Draw(pil)
    f, fs = font(26), font(20)
    c = (200, 225, 230)
    names = {"depth": "DEPTH", "rgb": "RGB", "ice": "INTENSITY"}
    d.text((40, 34), f"LIDAR SCAN  /  {names[mode]}", font=f, fill=c)
    d.text((40, 68), f"PTS {npts:,}   FRAME {n:03d}   {scan:3d}%", font=fs, fill=(140, 160, 170))
    d.rectangle((40, 100, 240, 106), outline=(90, 110, 120))
    d.rectangle((40, 100, 40 + 2 * scan, 106), fill=c)
    if mode == "depth":
        for i in range(260):
            col = (TURBO[255 - int(i / 259 * 255)][::-1] * 255).astype(int)
            d.line((W - 70, 120 + i, W - 52, 120 + i), fill=tuple(col))
        d.text((W - 160, 104), "0.6 m", font=fs, fill=c)
        d.text((W - 160, 372), "6.0 m", font=fs, fill=c)
    # axis gizmo
    ox, oy = 90, H - 90
    d.line((ox, oy, ox + 56, oy + 8), fill=(235, 70, 70), width=3)
    d.line((ox, oy, ox, oy - 58), fill=(80, 220, 110), width=3)
    d.line((ox, oy, ox - 30, oy + 30), fill=(80, 140, 255), width=3)
    d.text((ox + 62, oy - 2), "X", font=fs, fill=(235, 70, 70))
    d.text((ox - 6, oy - 86), "Y", font=fs, fill=(80, 220, 110))
    d.text((ox - 50, oy + 30), "Z", font=fs, fill=(80, 140, 255))
    return np.asarray(pil)[..., ::-1].astype(np.float32) / 255


def render(n):
    rng = np.random.default_rng(3900 + n)
    mode = mode_of(n)
    bgr = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png"))
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
    dep, lum = depth_map(bgr, m)
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    lum_c = clahe.apply((lum * 255).astype(np.uint8)).astype(np.float32) / 255
    x, y = sample(m, lum, rng)
    z = dep[y, x]
    L = cv2.GaussianBlur(lum_c, (0, 0), 0.8)[y, x]
    # virtual camera orbit: parallax around the people's depth
    t = (n - 1) / 12
    ax, ay = 0.030 * np.sin(t * 0.9), 0.012 * np.sin(t * 0.6 + 1)
    pivot = 0.35
    px = x + (z - pivot) * ax * 1500
    py = y + (z - pivot) * ay * 1500
    # colour
    if mode == "depth":
        base = TURBO[(np.clip(1 - z, 0, 1) * 255).astype(int)]
        inten = 0.12 + 1.15 * L ** 1.25
    elif mode == "rgb":
        base = bgr[y, x].astype(np.float32) / 255
        base = np.clip((base - base.mean(1, keepdims=True)) * 1.35 + base.mean(1, keepdims=True), 0, 1) * 1.15
        inten = np.ones_like(L)
    else:
        base = np.tile(np.array([1.0, 0.86, 0.45], np.float32), (x.size, 1))
        inten = 0.08 + 1.2 * L ** 1.15
    # depth slices: contour bands light up
    band = (np.mod(z * 34, 1.0) < 0.13).astype(np.float32)
    # scan sweep (top -> bottom), recently scanned rows glow and decay
    phase = ((n - 1) % SWEEP) / SWEEP
    ys = phase * (H + 200) - 100
    since = (ys - y) / H                                  # >0 = already passed this pass
    glow = np.where(since >= 0, np.exp(-since * 9), 0.0)
    ahead = since < 0
    inten = inten * np.where(ahead, 0.72, 1.0) + 0.45 * band * (z < 0.7)
    col = base * inten[:, None] + glow[:, None] * np.array([0.9, 1.0, 0.85], np.float32) * 0.9
    col *= np.where(z < 0.7, 1.0, 0.9)[:, None]           # the room is a dimmer, sparser cloud
    col = np.clip(col, 0, 1.4).astype(np.float32)
    canvas = np.zeros((H, W, 3), np.float32)
    near = z < 0.7
    splat(canvas, px[near], py[near], col[near], 2)
    splat(canvas, px[~near], py[~near], col[~near], 2)
    # stray returns floating in the void
    k = 300
    sx, sy = rng.uniform(0, W, k), rng.uniform(0, H, k)
    splat(canvas, sx, sy, np.tile(np.array([0.35, 0.4, 0.4], np.float32), (k, 1)) * rng.random((k, 1)).astype(np.float32), 1)
    img = canvas + 0.55 * cv2.GaussianBlur(canvas, (0, 0), 4) + 0.25 * cv2.GaussianBlur(canvas, (0, 0), 14)
    # the sweep plane itself: a thin line across the frame
    yl = int(ys)
    if 0 <= yl < H:
        line = np.zeros((H, W), np.float32)
        cv2.line(line, (0, yl), (W, yl), 1.0, 2)
        img += cv2.GaussianBlur(line, (0, 0), 3)[..., None] * np.array([0.5, 0.8, 0.55], np.float32) * 0.8
    grid_floor(img, ax)
    img = hud(img, n, int(x.size), mode, int(phase * 100))
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), (np.clip(img, 0, 1) * 255).astype(np.uint8))
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    with Pool(8) as p:
        for n in p.imap_unordered(render, ONLY):
            pass
    print("done", len(ONLY), "->", OUT)
