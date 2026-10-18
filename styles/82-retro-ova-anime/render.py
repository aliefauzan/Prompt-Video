"""Retro 80s-90s OVA anime restyle, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [all | frame numbers...]

Built like a late-80s / early-90s OVA shot on film:
  CEL LAYER (people): a fixed cel colour model (k-means over the clip), flat
    fills, ONE hard shadow tone that is hue-shifted to violet (not just
    darker), a sharp hair sheen band, thin dark-brown ink lines (silhouette +
    colour boundaries), facial features as dark shapes. Lines get a tiny
    per-frame boil (1-2 px) like hand-traced cels.
  BACKGROUND: a matte painting, not cels: heavily smoothed posterised gouache,
    airbrushed gradients, painted texture, no ink lines, graded to dusk
    (violet shadows, warm amber light). Blown-out window light becomes a
    painted city-pop dusk sky (violet -> magenta -> amber with streaked
    clouds), anchored to the window shape every frame.
  FILM: halation + bloom on highlights, faded print (lifted blacks, magenta /
    cyan cast), coarse 35 mm grain new every frame, gate weave, dust, soft
    vignette, 4:3 pillarbox.
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np

FRAMES, MASKS, OUT = sys.argv[1:4]
ARGS = sys.argv[4:]
H, W = 1080, 1620
h, w = 540, 810
yy0, xx0 = np.mgrid[0:h, 0:w].astype(np.float32)
LW = np.array([0.55, 1.0, 1.0], np.float32)


def frame_list():
    if not ARGS or ARGS == ["all"]:
        return list(range(1, 180))
    return [int(a) for a in ARGS]


def fbm(seed, hh, ww, octaves=4, base=6):
    rng = np.random.default_rng(seed)
    out = np.zeros((hh, ww), np.float32)
    amp, tot = 1.0, 0.0
    for o in range(octaves):
        c = base * 2 ** o
        n = rng.random((max(2, hh * c // ww), c)).astype(np.float32)
        out += amp * cv2.resize(n, (ww, hh), interpolation=cv2.INTER_CUBIC)
        tot += amp
        amp *= 0.5
    return out / tot


PAINT_TEX = (fbm(11, h, w, 5, 40) - 0.5).astype(np.float32)
CLOUD_TEX = fbm(23, 256, 512, 5, 4)


def read(n):
    src = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png"))
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE)
    src = cv2.resize(src, (w, h), interpolation=cv2.INTER_AREA)
    m = cv2.resize(m, (w, h), interpolation=cv2.INTER_AREA).astype(np.float32) / 255
    return src, m


# ---------------------------------------------------------------- palette
def _people_lab(n):
    src, mask = read(n)
    ms = cv2.pyrMeanShiftFiltering(src, 8, 26)
    lab = cv2.cvtColor(ms, cv2.COLOR_BGR2LAB).reshape(-1, 3).astype(np.float32)
    return lab[mask.reshape(-1) > 0.5]


def build_palette(k=12):
    data = np.concatenate([_people_lab(n)[::7] for n in (13, 49, 109, 160)]) * LW
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 40, 0.5)
    cv2.setRNGSeed(5)
    _, lab_, cent = cv2.kmeans(data, k, None, crit, 4, cv2.KMEANS_PP_CENTERS)
    cnt = np.bincount(lab_.ravel(), minlength=k).astype(np.float32)
    merged = True
    while merged:
        merged = False
        dd = np.sqrt(((cent[:, None] - cent[None]) ** 2).sum(-1)) + np.eye(len(cent)) * 1e9
        i, j = np.unravel_index(dd.argmin(), dd.shape)
        if dd[i, j] < 18:
            cent[i] = (cent[i] * cnt[i] + cent[j] * cnt[j]) / (cnt[i] + cnt[j])
            cnt[i] += cnt[j]
            cent = np.delete(cent, j, 0)
            cnt = np.delete(cnt, j)
            merged = True
    raw = (cent / LW).astype(np.float32)
    paint = raw.copy()
    # OVA cel paint: richer chroma, warm skin, slightly lifted values
    paint[:, 1:] = 128 + (paint[:, 1:] - 128) * 1.7
    paint[:, 0] = np.clip(paint[:, 0] * 1.05 + 10, 0, 255)
    bgr = cv2.cvtColor(np.clip(paint, 0, 255).astype(np.uint8)[None], cv2.COLOR_LAB2BGR)[0]
    return raw, paint, bgr.astype(np.float32) / 255


PAL = None


def init(pal, win):
    global PAL, WIN
    PAL, WIN = pal, win


# ---------------------------------------------------------------- background
def dusk_sky(hh, ww, n):
    """Painted city-pop dusk: violet top -> magenta -> amber horizon, streak clouds."""
    t = np.linspace(0, 1, hh, dtype=np.float32)[:, None]
    keys = np.array([[120, 50, 60], [150, 70, 150], [140, 95, 225], [120, 170, 250], [170, 215, 255]], np.float32) / 255
    tt = np.clip(t, 0, 1) * (len(keys) - 1)
    i = np.clip(tt.astype(int), 0, len(keys) - 2)
    f = (tt - i)[..., None]
    sky = keys[i] * (1 - f) + keys[i + 1] * f
    sky = np.repeat(sky, ww, axis=1)
    # horizontal streak clouds: stretched noise, drifting very slowly
    cl = cv2.resize(CLOUD_TEX, (ww * 3, hh), interpolation=cv2.INTER_CUBIC)
    off = int(n * 0.6) % (ww * 2)
    cl = cl[:, off:off + ww]
    cl = cv2.GaussianBlur(cl, (0, 0), sigmaX=9, sigmaY=1.5)
    band = np.clip((cl - 0.52) * 7, 0, 1) * (0.25 + 0.75 * np.sin(np.pi * np.clip(t * 1.1, 0, 1)))
    cloud_col = np.array([120, 90, 200], np.float32) / 255 * (1 - t[..., None]) + np.array([150, 200, 255], np.float32) / 255 * t[..., None]
    sky = sky * (1 - band[..., None] * 0.85) + cloud_col * band[..., None] * 0.85
    # thin bright rim on cloud bottoms (sunset light)
    rim = np.clip(band - np.roll(band, 2, axis=0), 0, 1)
    sky += rim[..., None] * np.array([0.3, 0.55, 0.7], np.float32)
    return np.clip(sky, 0, 1)


def window_mask(src):
    """Blown, low-saturation highlights = the window light."""
    lum = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV).astype(np.float32)
    win = ((lum > 0.80) & (hsv[..., 1] < 50)).astype(np.uint8)
    win = cv2.morphologyEx(win, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    win = cv2.morphologyEx(win, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    num, lb, st, _ = cv2.connectedComponentsWithStats(win, connectivity=8)
    ok = st[:, cv2.CC_STAT_AREA] > 1500
    ok[0] = False
    return ok[lb].astype(np.float32)


def window_extents():
    """Vertical extent of the window per frame, median-smoothed over time so
    the painted sky gradient does not jump."""
    ext = []
    for n in range(1, 180):
        src = cv2.resize(cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png")), (w, h), interpolation=cv2.INTER_AREA)
        ys, _ = np.nonzero(window_mask(src))
        ext.append((np.percentile(ys, 1), np.percentile(ys, 99)) if len(ys) > 200 else (np.nan, np.nan))
    ext = np.array(ext, np.float32)
    for c in range(2):
        v = ext[:, c]
        good = ~np.isnan(v)
        v[~good] = np.interp(np.flatnonzero(~good), np.flatnonzero(good), v[good])
        pad = np.pad(v, 6, mode="edge")
        v = np.array([np.median(pad[i:i + 13]) for i in range(len(v))])
        k = np.ones(5) / 5
        ext[:, c] = np.convolve(np.pad(v, 2, mode="edge"), k, mode="valid")
    return {n: tuple(ext[n - 1]) for n in range(1, 180)}


WIN = None


def background(src, mask, n):
    ms = cv2.pyrMeanShiftFiltering(src, 14, 34)
    ms = cv2.medianBlur(ms, 9)
    f = ms.astype(np.float32) / 255
    # airbrushed gradients: blend with a big blur
    f = 0.6 * f + 0.4 * cv2.GaussianBlur(f, (0, 0), 14)
    # dusk grade: violet shadows, amber light
    L = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)[..., None]
    shadow = np.array([0.74, 0.50, 0.58], np.float32)
    light = np.array([0.72, 0.86, 1.04], np.float32)
    f = f * (shadow * (1 - L) + light * L) * 1.22
    f *= (1 + 0.07 * PAINT_TEX)[..., None]
    win = window_mask(src)
    y0, y1 = WIN[n]
    if win.sum() > 200:
        sky = dusk_sky(h, w, n)
        # map the gradient onto the window's own vertical extent
        ty = np.clip((yy0[:, :1] - y0) / max(1, y1 - y0), 0, 1)
        idx = (ty * (h - 1)).astype(int)[:, 0]
        sky = sky[idx]
        wm = cv2.GaussianBlur(win, (0, 0), 1.5)[..., None]
        f = f * (1 - wm) + sky * wm
        # warm light spill from the window onto the room
        spill = cv2.GaussianBlur(win, (0, 0), 40)[..., None]
        f += spill * np.array([0.02, 0.07, 0.16], np.float32)
    return np.clip(f, 0, 1), win


def heads(m):
    """Heads from the matte alone (pattern from style 17): lowest silhouette
    peaks, head width from row runs, stop at the neck dip / shoulder jump.
    Returns [(xc, y0, yneck, headw)] in working resolution."""
    cols = m > 0.5
    has = cols.any(0)
    topy = np.where(has, cols.argmax(0), h).astype(np.float32)
    remaining = has.copy()
    out = []
    for _ in range(4):
        cand = np.flatnonzero(remaining & (topy < h * 0.85))
        if len(cand) < 6:
            break
        y0 = int(topy[cand].min())
        xs = cand[topy[cand] <= y0 + 2]
        grp = np.split(xs, np.flatnonzero(np.diff(xs) > 2) + 1)[0]
        x0 = int(grp[len(grp) // 2])
        row = cols[min(h - 1, y0 + 1)]
        l = x0 - (np.flatnonzero(~row[:x0][::-1])[:1].tolist() or [x0])[0]
        r = x0 + (np.flatnonzero(~row[x0:])[:1].tolist() or [w - x0])[0]
        if any(l <= hd[0] <= r for hd in out):
            remaining[l:r] = False
            continue
        wmax, yneck, xc, wprev, grow = 1, None, x0, None, True
        for y in range(y0, min(h, y0 + int(h * 0.6))):
            row = cols[y]
            if not row[x0]:
                continue
            l = x0 - (np.flatnonzero(~row[:x0][::-1])[:1].tolist() or [x0])[0]
            r = x0 + (np.flatnonzero(~row[x0:])[:1].tolist() or [w - x0])[0]
            ww_ = r - l
            dy = y - y0
            if wprev is not None and dy > 10 and ww_ > wprev * 1.12 + 5:
                grow = False
                if dy > 0.9 * wmax:
                    yneck = y
                    break
            wprev = ww_
            if grow and (dy < 1.0 * wmax or dy < 10):
                if ww_ > wmax:
                    wmax, xc = ww_, (l + r) // 2
            elif dy < 0.9 * wmax:
                continue
            elif ww_ < 0.85 * wmax or ww_ > 1.7 * wmax or dy > 1.25 * wmax:
                yneck = y
                break
        yneck = yneck or min(h - 1, y0 + int(1.25 * wmax))
        if wmax >= 12:
            out.append((xc, y0, yneck, wmax))
        remaining[max(0, xc - int(wmax * 1.1)):xc + int(wmax * 1.1)] = False
        remaining[max(0, x0 - 6):x0 + 6] = False
    return out


def hair_mask(dark, mask, lab):
    """Dark paint inside each head box that reaches up to the top of the head
    (so a dark shirt next to a head is not painted as hair)."""
    out = np.zeros((h, w), bool)
    for xc, y0, yn, hw in heads(mask):
        hh_ = yn - y0
        z = np.zeros((h, w), np.uint8)
        cv2.rectangle(z, (int(xc - 0.75 * hw), int(y0 - 4)), (int(xc + 0.75 * hw), int(yn + 0.25 * hh_)), 1, -1)
        cand = dark & z.astype(bool)
        top = cand.copy()
        top[int(y0 + 0.35 * hh_):] = False
        if top.sum() < 30:
            continue
        ref = np.median(lab[top], axis=0)
        cand = (cand & (np.sqrt(((lab - ref) ** 2).sum(-1)) < 24)).astype(np.uint8)
        cand = cv2.morphologyEx(cand, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        num, lb, st, _ = cv2.connectedComponentsWithStats(cand, connectivity=8)
        ok = (st[:, cv2.CC_STAT_TOP] <= y0 + 0.35 * hh_) & (st[:, cv2.CC_STAT_AREA] > 40)
        ok[0] = False
        out |= ok[lb]
    return out


# ---------------------------------------------------------------- cels
def characters(src, mask, n):
    raw, paint, pbgr = PAL
    rng = np.random.default_rng(1000 + n)
    ms = cv2.pyrMeanShiftFiltering(src, 8, 26)
    lab = cv2.cvtColor(ms, cv2.COLOR_BGR2LAB).astype(np.float32)
    d = (((lab[:, :, None, :] - raw[None, None]) * LW) ** 2).sum(-1)
    votes = np.exp(-(d - d.min(-1, keepdims=True)) / 120.0)
    votes = cv2.GaussianBlur(votes, (0, 0), 4.2)
    lbl = votes.argmax(-1).astype(np.uint8)
    lbl = cv2.medianBlur(cv2.medianBlur(lbl, 7), 5)
    big = cv2.GaussianBlur(votes, (0, 0), 8).argmax(-1).astype(np.uint8)
    for c in np.unique(lbl):
        num, lb, st, _ = cv2.connectedComponentsWithStats((lbl == c).astype(np.uint8), connectivity=8)
        small = st[:, cv2.CC_STAT_AREA] < 700
        small[0] = False
        sm = small[lb]
        lbl[sm] = big[sm]
    cel = pbgr[lbl].copy()
    # one shadow tone, hue-shifted to violet
    lum = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY).astype(np.float32)
    local = cv2.GaussianBlur(lum, (0, 0), 14)
    sh = (cv2.GaussianBlur(lum, (0, 0), 5) < local - 15).astype(np.uint8)
    sh = cv2.morphologyEx(sh, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
    sh = (cv2.GaussianBlur(sh.astype(np.float32), (0, 0), 5) > 0.5)
    num, lb, st, _ = cv2.connectedComponentsWithStats(sh.astype(np.uint8), connectivity=8)
    ok = st[:, cv2.CC_STAT_AREA] > 600
    ok[0] = False
    sh = ok[lb]
    cel[sh] = cel[sh] * np.array([0.86, 0.66, 0.72], np.float32)
    # hard highlight
    hi = (cv2.GaussianBlur(lum, (0, 0), 2.5) > local + 22) & (lum > 150)
    hi = cv2.medianBlur(hi.astype(np.uint8) * 255, 5) > 127
    cel[hi] = np.clip(cel[hi] * 1.12 + np.array([0.08, 0.07, 0.04]), 0, 1)
    # hair sheen: dark (hair) regions in upper part of a person, locally brighter streaks
    hsv0 = cv2.cvtColor(src, cv2.COLOR_BGR2HSV).astype(np.float32)
    skin = ((hsv0[..., 0] < 22) & (hsv0[..., 1] > 45) & (hsv0[..., 1] < 180) & (hsv0[..., 2] > 80)).astype(np.float32)
    dark = (cv2.GaussianBlur(lum, (0, 0), 2) < 80) & (mask > 0.5)
    hair = hair_mask(dark & (cv2.GaussianBlur(skin, (0, 0), 2.5) < 0.3), mask, lab)
    hair = cv2.morphologyEx(hair.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8)).astype(bool) & (mask > 0.5)
    cel[hair] = np.array([0.20, 0.10, 0.16], np.float32)   # deep violet-black hair paint
    sheen = hair & (cv2.GaussianBlur(lum, (0, 0), 1.5) > cv2.GaussianBlur(lum, (0, 0), 7) + 7)
    sheen = cv2.morphologyEx(sheen.astype(np.uint8), cv2.MORPH_OPEN, np.ones((2, 3), np.uint8)).astype(bool)
    cel[sheen] = np.array([0.62, 0.42, 0.52], np.float32)  # mauve sheen band
    # ink lines: colour boundaries between clearly different paints + silhouette
    pd = np.sqrt((((paint[:, None] - paint[None]) * LW) ** 2).sum(-1))
    inner = np.zeros((h, w), np.uint8)
    for sy, sx in ((0, 1), (1, 0)):
        a, b = lbl[: h - sy, : w - sx], lbl[sy:, sx:]
        inner[: h - sy, : w - sx] |= (pd[a, b] > 30).astype(np.uint8)
    num, lb, st, _ = cv2.connectedComponentsWithStats(inner, connectivity=8)
    ok = st[:, cv2.CC_STAT_AREA] > 60
    ok[0] = False
    inner = ok[lb].astype(np.uint8)
    feat = ((lum < np.minimum(95, 0.62 * cv2.GaussianBlur(lum, (0, 0), 8))) & (cv2.GaussianBlur(skin, (0, 0), 6) > 0.25)).astype(np.uint8)
    num, lb, st, _ = cv2.connectedComponentsWithStats(feat, connectivity=8)
    ok = (st[:, cv2.CC_STAT_AREA] > 5) & (st[:, cv2.CC_STAT_AREA] < 500)
    ok[0] = False
    feat = ok[lb].astype(np.uint8)
    m8 = (mask > 0.5).astype(np.uint8)
    inside = cv2.erode(m8, np.ones((5, 5), np.uint8))
    sil = cv2.dilate(m8, np.ones((3, 3), np.uint8)) - cv2.erode(m8, np.ones((3, 3), np.uint8))
    ink = np.maximum(np.maximum(inner * inside * (cv2.GaussianBlur(skin, (0, 0), 4) < 0.2), feat), sil).astype(np.float32)
    dx = cv2.resize(rng.normal(0, 1, (h // 40, w // 40)).astype(np.float32), (w, h), interpolation=cv2.INTER_CUBIC) * 0.7
    dy = cv2.resize(rng.normal(0, 1, (h // 40, w // 40)).astype(np.float32), (w, h), interpolation=cv2.INTER_CUBIC) * 0.7
    ink = cv2.remap(ink, xx0 + dx, yy0 + dy, cv2.INTER_LINEAR)
    ink = np.clip(cv2.GaussianBlur(ink, (0, 0), 0.5) * 1.3, 0, 1)
    return np.clip(cel, 0, 1), ink


# ---------------------------------------------------------------- film
def film(img, n):
    rng = np.random.default_rng(9000 + n)
    big = cv2.resize(img, (W, H), interpolation=cv2.INTER_CUBIC)
    # halation (red-orange, wide) + bloom (warm, tight) from highlights
    lum = cv2.cvtColor(big, cv2.COLOR_BGR2GRAY)
    hl = np.clip((lum - 0.62) / 0.38, 0, 1)
    hal = cv2.GaussianBlur(hl, (0, 0), 22)[..., None] * np.array([0.10, 0.22, 0.55], np.float32)
    bloom = cv2.GaussianBlur(big * hl[..., None], (0, 0), 7) * 0.45
    out = big + hal * 0.9 + bloom
    # faded film print: lifted blacks, soft shoulder, magenta-cyan cast
    out = 0.035 + 0.95 * out
    out = out / (1 + 0.18 * out)
    out = np.clip(out, 0, None) ** 1.12 * 1.08
    out = out * np.array([1.06, 0.96, 1.08], np.float32)
    # 4:3 pillarbox window with gate weave
    gx, gy = rng.normal(0, 1.0), rng.normal(0, 1.2)
    M = np.float32([[1, 0, gx], [0, 1, gy]])
    out = cv2.warpAffine(out, M, (W, H), borderMode=cv2.BORDER_REFLECT)
    # vignette
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - W / 2) / (W * 0.48)) ** 2 + ((yy - H / 2) / (H * 0.62)) ** 2)
    out *= np.clip(1.08 - 0.32 * r ** 2, 0.55, 1)[..., None]
    # coarse film grain, new every frame
    g = rng.normal(0, 1, (H // 2, W // 2)).astype(np.float32)
    g = cv2.resize(g, (W, H), interpolation=cv2.INTER_LINEAR)
    lumo = cv2.cvtColor(np.clip(out, 0, 1).astype(np.float32), cv2.COLOR_BGR2GRAY)
    out += (g * (0.022 + 0.02 * (1 - np.abs(lumo - 0.5) * 2)))[..., None]
    out += rng.normal(0, 0.008, (H, W, 3)).astype(np.float32)
    # dust specks and the odd hair (on screen for one frame only)
    dust = np.zeros((H, W), np.float32)
    for _ in range(int(rng.integers(3, 9))):
        cv2.circle(dust, (int(rng.integers(0, W)), int(rng.integers(0, H))), int(rng.integers(1, 4)), 1.0, -1, cv2.LINE_AA)
    if rng.random() < 0.3:
        p = [(int(rng.integers(0, W)), int(rng.integers(0, H)))]
        a = rng.uniform(0, 6.28)
        for _ in range(8):
            a += rng.normal(0, 0.4)
            p.append((int(p[-1][0] + 9 * np.cos(a)), int(p[-1][1] + 9 * np.sin(a))))
        cv2.polylines(dust, [np.array(p, np.int32)], False, 1.0, 1, cv2.LINE_AA)
    out = out * (1 - 0.6 * dust[..., None]) + 0.0
    out = np.clip(out, 0, 1)
    # 4:3 pillarbox (1440 wide picture)
    bar = (W - 1440) // 2
    out[:, :bar] = 0.02
    out[:, W - bar:] = 0.02
    return (out * 255).astype(np.uint8)


def render(n):
    src, mask = read(n)
    bg, _ = background(src, mask, n)
    cel, ink = characters(src, mask, n)
    m = cv2.GaussianBlur(mask, (0, 0), 0.8)[..., None]
    img = bg * (1 - m) + cel * m
    img = img * (1 - ink[..., None]) + np.array([0.10, 0.08, 0.16], np.float32) * ink[..., None]
    # cel softness: slight blur so it reads as film of painted cels, not vector
    img = cv2.GaussianBlur(img.astype(np.float32), (0, 0), 0.6)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), film(img, n))
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    nums = frame_list()
    pal = build_palette()
    with Pool(3, initializer=init, initargs=(pal, window_extents())) as p:
        for n in p.imap_unordered(render, nums):
            print(n, end=" ", flush=True)
    print()
