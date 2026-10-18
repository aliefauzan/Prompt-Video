"""Needle-Felt Wool World — local approximation of the frame-by-frame restyle.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [all | 13 49 85 ...]

Every frame is rebuilt as a handmade needle-felted wool diorama:
  * colours are simplified (edge-preserving smoothing) and snapped to a fixed
    "dyed wool" palette (k-means once over several frames, so colours never flicker);
  * each colour patch becomes a soft pillowy wool lump: darker felted seams where
    patches meet, a rounded bulge lit from the upper left (distance-transform puff);
  * a procedural fibre field (short wool fibres following a slowly turning
    direction field) mottles every surface and displaces the image a few pixels,
    so every edge — above all the silhouettes — turns into a fuzzy fibre halo;
  * the room is felted coarser and sits behind a macro tabletop depth of field;
  * warm tabletop key light, lifted matte blacks, vignette.
The fibre field changes every frame (4 pre-made variants + a small random offset),
like a stop-motion puppet that is re-shot every frame: the fuzz boils, the
colours, shapes and motion do not.
"""
import sys
from pathlib import Path

import cv2
import numpy as np

cv2.setNumThreads(2)
W, H = 1620, 1080
HERE = Path(__file__).resolve().parent
PAL_FILE = HERE / "palette.npz"


def lab(rgb):
    return cv2.cvtColor(np.clip(rgb, 0, 255).astype(np.uint8), cv2.COLOR_RGB2LAB).astype(np.float32)


def flatten(rgb, k):
    """Take out part of the photographic shading: felt colour comes from the dye, not the light."""
    f = rgb.astype(np.float32)
    lum = f.mean(-1, keepdims=True) + 8
    big = cv2.GaussianBlur(lum, (0, 0), 40)[..., None]
    f = f * (big / lum) ** k
    return np.clip(f, 0, 255).astype(np.uint8)


def smooth(rgb, strong):
    s = cv2.resize(flatten(rgb, 0.45 if not strong else 0.25), (W // 2, H // 2), interpolation=cv2.INTER_AREA)
    for _ in range(3 if strong else 2):
        s = cv2.bilateralFilter(s, 9, 28, 7)
    s = cv2.medianBlur(s, 7 if strong else 5)
    return s


def build_palette(frames_dir, masks_dir):
    pp, bp = [], []
    for n in (1, 13, 49, 85, 109, 145, 178):
        rgb = cv2.cvtColor(cv2.imread(str(frames_dir / f"frame_{n:03d}.png")), cv2.COLOR_BGR2RGB)
        m = cv2.resize(cv2.imread(str(masks_dir / f"frame_{n:03d}.png"), 0), (W // 2, H // 2)) > 128
        L = lab(smooth(rgb, False)).reshape(-1, 3)
        pp.append(L[m.ravel()][::7])
        bp.append(L[~m.ravel()][::9])
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 40, 0.5)
    _, _, cp = cv2.kmeans(np.concatenate(pp), 22, None, crit, 3, cv2.KMEANS_PP_CENTERS)
    _, _, cb = cv2.kmeans(np.concatenate(bp), 12, None, crit, 3, cv2.KMEANS_PP_CENTERS)
    np.savez(PAL_FILE, people=cp, room=cb)


def quantise(L, pal):
    d = ((L[:, :, None, :] - pal[None, None]) ** 2).sum(-1)
    idx = d.argmin(-1)
    return idx, pal[idx]


def fibre_field(seed, length):
    """Short straight-ish fibres that follow a slowly turning direction field, ~N(0,1)."""
    rng = np.random.default_rng(seed)
    noise = rng.standard_normal((H, W)).astype(np.float32)
    theta = cv2.GaussianBlur(rng.standard_normal((H // 8, W // 8)).astype(np.float32), (0, 0), 6)
    theta = cv2.resize(theta, (W, H)) * 9.0 + rng.standard_normal((H, W)).astype(np.float32) * 0.5  # swirls + jitter
    out = np.zeros((H, W), np.float32)
    wsum = np.zeros((H, W), np.float32)
    for k in range(8):
        a = np.pi * k / 8
        ker = np.zeros((length, length), np.float32)
        c = length // 2
        dx, dy = np.cos(a) * c, np.sin(a) * c
        cv2.line(ker, (int(round(c - dx)), int(round(c - dy))), (int(round(c + dx)), int(round(c + dy))), 1.0, 1, cv2.LINE_AA)
        ker /= ker.sum()
        r = cv2.filter2D(noise, -1, ker)
        w = np.exp(4.0 * np.cos(2 * (theta - a)))
        out += r * w
        wsum += w
    out /= wsum
    return out / (out.std() + 1e-6)


FIB = None


def fibres():
    global FIB
    if FIB is None:
        FIB = []
        for v in range(4):
            fine = fibre_field(100 + v, 7)
            coarse = fibre_field(200 + v, 15)
            dxf = fibre_field(300 + v, 11)
            dyf = fibre_field(400 + v, 11)
            FIB.append((0.65 * fine + 0.35 * coarse, dxf, dyf))
    return FIB


def puff(idx, scale):
    """0 at seams between colour patches, -> 1 inside; plus a light-from-upper-left bulge."""
    edge = np.zeros(idx.shape, np.uint8)
    edge[:, 1:] |= (idx[:, 1:] != idx[:, :-1])
    edge[1:, :] |= (idx[1:, :] != idx[:-1, :])
    d = cv2.distanceTransform((1 - edge).astype(np.uint8), cv2.DIST_L2, 3)
    p = 1 - np.exp(-d / scale)
    pb = cv2.GaussianBlur(p, (0, 0), scale * 0.6)
    gy, gx = np.gradient(pb)
    light = np.clip(-(gx + gy) * scale * 1.1, -0.6, 0.6)  # upper-left facing slopes brighter
    return p, light


def strands(col, mm, rng):
    edge = (cv2.GaussianBlur(mm, (0, 0), 2) - 0.5)
    ys, xs = np.nonzero(np.abs(edge) < 0.3)
    pick = rng.integers(0, len(ys), 520) if len(ys) else []
    pts = [(xs[i], ys[i]) for i in pick]
    pts += [tuple(p) for p in np.stack([rng.integers(0, W, 160), rng.integers(0, H, 160)], 1)]
    over = col.copy()
    for x, y in pts:
        c = col[y, x] * 1.18 + 14
        a = rng.uniform(0, 2 * np.pi)
        L = rng.uniform(6, 16)
        curve = rng.uniform(-0.5, 0.5)
        poly = []
        px, py = float(x), float(y)
        for _ in range(5):
            poly.append((int(px * 4), int(py * 4)))
            px += np.cos(a) * L / 4
            py += np.sin(a) * L / 4
            a += curve
        cv2.polylines(over, [np.array(poly, np.int32)], False, tuple(float(v) for v in c), 1, cv2.LINE_AA, 2)
    return col * 0.35 + over * 0.65


def render(rgb, m, frame_no, pal):
    rng = np.random.default_rng(frame_no * 7919)
    fib, dxf, dyf = fibres()[frame_no % 4]
    ox, oy = rng.integers(-6, 7, 2)
    fib = np.roll(fib, (oy, ox), (0, 1))

    mh = cv2.resize(m, (W // 2, H // 2), interpolation=cv2.INTER_AREA)
    # --- people: finer wool lumps
    sp = smooth(rgb, False)
    ip, qp = quantise(lab(sp), pal["people"])
    sb = smooth(cv2.GaussianBlur(rgb, (0, 0), 3), True)
    ib, qb = quantise(lab(sb), pal["room"])
    idx = np.where(mh > 0.5, ip, 100 + ib)
    q = np.where(mh[..., None] > 0.5, qp, qb)
    q = cv2.cvtColor(np.clip(q, 0, 255).astype(np.uint8), cv2.COLOR_LAB2RGB).astype(np.float32)
    # keep a little of the real tonal variation inside each patch (wool is never flat)
    raw = np.where(mh[..., None] > 0.5, sp, sb).astype(np.float32)
    q = 0.72 * q + 0.28 * raw
    # wool lumps from a coarser label map (one lump per face / sleeve / hair mass, not per freckle)
    s4 = cv2.medianBlur(cv2.resize(np.where(mh[..., None] > 0.5, sp, sb), (W // 4, H // 4), interpolation=cv2.INTER_AREA), 5)
    i4, _ = quantise(lab(s4), np.concatenate([pal['people'][::2], pal['room']]))
    i4 = cv2.medianBlur(i4.astype(np.uint8), 5)
    p, light = puff(i4.astype(np.int32), 4.0)
    p = cv2.resize(p, (W // 2, H // 2)); light = cv2.resize(light, (W // 2, H // 2))
    q *= (0.80 + 0.20 * p)[..., None]
    q += (light * 55)[..., None] * np.array([1.0, 0.95, 0.85], np.float32)
    col = cv2.resize(q, (W, H), interpolation=cv2.INTER_CUBIC)
    # needle-punched dark wool details: eyes, brows, lashes, mouth, glasses rims, collar, pattern lines
    gr = cv2.GaussianBlur(cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY).astype(np.float32), (0, 0), 1.6)
    dog = cv2.GaussianBlur(gr, (0, 0), 5) - gr
    det = np.clip((dog - 5) / 14, 0, 1) * cv2.GaussianBlur(m, (0, 0), 3)
    det = cv2.GaussianBlur(det, (0, 0), 1.2)
    col *= (1 - 0.55 * det)[..., None]

    # --- matte wool: soft pastel, lifted blacks, softened highlights
    g = col.mean(-1, keepdims=True)
    col = g + (col - g) * 1.3
    col = 30 + col * 0.95
    # fibre mottling: dark gaps between fibres, light fibre tips
    col *= (1 + 0.10 * fib)[..., None]
    tips = np.clip(fib - 1.2, 0, None)[..., None]
    col += tips * 30
    lump = cv2.resize(cv2.GaussianBlur(rng.standard_normal((H // 12, W // 12)).astype(np.float32), (0, 0), 1.0), (W, H))
    col *= (1 + 0.035 * lump)[..., None]

    # --- fuzzy fibre halo: displace everything along the fibres
    band = cv2.GaussianBlur(np.abs(cv2.Laplacian(cv2.GaussianBlur(m, (0, 0), 3), cv2.CV_32F)) * 60, (0, 0), 4).clip(0, 1)
    amp = 1.6 + 6.5 * band
    gx, gy = np.meshgrid(np.arange(W, dtype=np.float32), np.arange(H, dtype=np.float32))
    mx = gx + np.roll(dxf, (oy, ox), (0, 1)) * amp
    my = gy + np.roll(dyf, (oy, ox), (0, 1)) * amp
    col = cv2.remap(col.astype(np.float32), mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    mm = cv2.remap(m, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

    # --- stray wool fibres: thin curly strands, most of them standing off the silhouettes
    col = strands(col, mm, rng)

    # --- macro tabletop depth of field: the felted room is soft, the puppets sharp
    bg = cv2.GaussianBlur(col, (0, 0), 2.6)
    a = cv2.GaussianBlur(mm, (0, 0), 1.5)[..., None]
    col = col * a + bg * (1 - a)
    # contact shadow of the felt figures on the backdrop
    sh = cv2.GaussianBlur(np.roll(mm, (14, 10), (0, 1)), (0, 0), 14)
    col *= (1 - 0.28 * sh * (1 - a[..., 0]))[..., None]

    # --- warm key light from the upper left, vignette, soft bloom
    yy, xx = gy / H, gx / W
    key = 1.12 - 0.16 * (0.6 * xx + 0.4 * yy)
    vig = 1 - 0.22 * (((xx - 0.5) / 0.75) ** 2 + ((yy - 0.48) / 0.7) ** 2)
    col *= (key * vig)[..., None]
    col *= np.array([1.03, 1.0, 0.95], np.float32)
    bloom = cv2.GaussianBlur(np.clip(col - 200, 0, None), (0, 0), 12)
    col += bloom * 0.35
    col = 255 * (np.clip(col, 0, 255) / 255) ** 0.85      # airy, soft tabletop exposure
    col += rng.normal(0, 2.2, (H, W, 1)).astype(np.float32)
    return np.clip(col, 0, 255).astype(np.uint8)


def main():
    frames, masks, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    out.mkdir(parents=True, exist_ok=True)
    if not PAL_FILE.exists():
        build_palette(frames, masks)
    pal = dict(np.load(PAL_FILE))
    args = sys.argv[4:] or ["13", "49", "85", "109", "145", "178"]
    nums = range(1, 180) if args == ["all"] else [int(a) for a in args]
    for n in nums:
        rgb = cv2.cvtColor(cv2.imread(str(frames / f"frame_{n:03d}.png")), cv2.COLOR_BGR2RGB)
        m = cv2.imread(str(masks / f"frame_{n:03d}.png"), 0).astype(np.float32) / 255
        res = render(rgb, m, n, pal)
        cv2.imwrite(str(out / f"frame_{n:03d}.png"), cv2.cvtColor(res, cv2.COLOR_RGB2BGR))
        print(n, flush=True)


if __name__ == "__main__":
    main()
