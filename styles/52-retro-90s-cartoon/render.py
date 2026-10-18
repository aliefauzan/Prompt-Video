"""Retro 90s TV cartoon restyle, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [all | frame numbers...]

Built like a 90s TV cel episode, at standard-definition resolution:
  CEL LAYER (people): flat, punchy fills from mean-shift, ONE hard shadow
    layer + one hard highlight, thick black wobbly ink outlines (silhouette)
    and thinner black inner lines; eyes / brows / mouth as solid black shapes.
    The ink lines are displaced by a new noise field every frame (line boil),
    and the cel paint gets a tiny per-frame gain/hue flicker.
  BACKGROUND: a separately painted plate — posterised gouache in a muted 90s
    production palette (mustard, teal, brick, dusty purple), soft brush
    texture, slightly warped "wonky" perspective, no black outlines, held
    still (backgrounds were one painting under the moving cels).
  FILM/TAPE: cel dust and hairs that sit on the cel for a few frames, then
    SD softness, chroma bleed, a light sharpening halo and grain, upscaled
    back to 1620x1080.
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np

FRAMES, MASKS, OUT = sys.argv[1:4]
ARGS = sys.argv[4:]
H, W = 1080, 1620
h, w = 540, 810          # working (SD-ish) resolution


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


# background palette ramp (BGR), dark -> light: dusty purple, teal, brick, mustard, cream
RAMP_KEYS = np.array([
    [70, 40, 55], [110, 95, 45], [70, 95, 165], [60, 160, 215], [175, 220, 240]], np.float32)


def ramp(t):
    t = np.clip(t, 0, 1) * (len(RAMP_KEYS) - 1)
    i = np.clip(t.astype(int), 0, len(RAMP_KEYS) - 2)
    f = (t - i)[..., None]
    return RAMP_KEYS[i] * (1 - f) + RAMP_KEYS[i + 1] * f


BG_TEX = (fbm(3, h, w, 5, 30) - 0.5).astype(np.float32)
yy0, xx0 = np.mgrid[0:h, 0:w].astype(np.float32)
# wonky perspective: slow sinusoidal warp of the background plate
WARP_X = xx0 + 6 * np.sin(yy0 / 70.0) + 4 * np.sin(xx0 / 150.0)
WARP_Y = yy0 + 5 * np.sin(xx0 / 90.0)


WB = np.array([1.10, 1.0, 0.91], np.float32)


def read(n):
    src = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png"))
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE)
    src = cv2.resize(src, (w, h), interpolation=cv2.INTER_AREA)
    # fixed partial grey-world white balance: lift the warm room cast so the
    # cel paints get their own clear hues
    src = np.clip(src.astype(np.float32) * WB, 0, 255).astype(np.uint8)
    m = cv2.resize(m, (w, h), interpolation=cv2.INTER_AREA).astype(np.float32) / 255
    return src, m


def background(src):
    ms = cv2.pyrMeanShiftFiltering(src, 10, 30)
    ms = cv2.medianBlur(ms, 7)
    f = ms.astype(np.float32) / 255
    lum = cv2.cvtColor(ms, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
    # posterise to 6 painted values, map through the 90s palette, keep a bit of
    # the original hue so the room still reads (wood stays warm, screen stays blue)
    q = np.floor(lum * 6) / 5
    q = cv2.GaussianBlur(q, (0, 0), 1.2)
    pal = ramp(q * 0.95 + 0.03) / 255
    f = 0.38 * pal + 0.62 * f * np.array([1.02, 1.0, 0.98], np.float32)
    hsv = cv2.cvtColor(f.astype(np.float32), cv2.COLOR_BGR2HSV)
    hsv[..., 1] = np.clip(hsv[..., 1] * 1.1, 0, 1)
    hsv[..., 2] = np.clip(hsv[..., 2] * 1.08 + 0.03, 0, 1)
    f = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    f *= (1 + 0.06 * BG_TEX)[..., None]
    f = cv2.remap(f, WARP_X, WARP_Y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    return np.clip(f, 0, 1)


def _people_lab(n):
    src, mask = read(n)
    ms = cv2.pyrMeanShiftFiltering(src, 8, 28)
    lab = cv2.cvtColor(ms, cv2.COLOR_BGR2LAB).reshape(-1, 3).astype(np.float32)
    return lab[mask.reshape(-1) > 0.5]


def build_palette(k=14):
    """One fixed cel palette for the whole episode (stable colours, no flicker)."""
    data = np.concatenate([_people_lab(n)[::7] for n in (13, 49, 109, 160)]) * LW
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 40, 0.5)
    cv2.setRNGSeed(7)
    _, lab_, cent = cv2.kmeans(data, k, None, crit, 4, cv2.KMEANS_PP_CENTERS)
    # merge near-duplicate colours (one skin tone, one shirt tone...) like a
    # real cel colour model with few paints
    cnt = np.bincount(lab_.ravel(), minlength=k).astype(np.float32)
    merged = True
    while merged:
        merged = False
        dd = np.sqrt(((cent[:, None] - cent[None]) ** 2).sum(-1)) + np.eye(len(cent)) * 1e9
        i, j = np.unravel_index(dd.argmin(), dd.shape)
        if dd[i, j] < 20:
            cent[i] = (cent[i] * cnt[i] + cent[j] * cnt[j]) / (cnt[i] + cnt[j])
            cnt[i] += cnt[j]
            cent = np.delete(cent, j, 0)
            cnt = np.delete(cnt, j)
            merged = True
    cent = cent / LW
    # punch up the paint: more chroma, slightly lifted values
    cent[:, 1:] = 128 + (cent[:, 1:] - 128) * 2.1
    cent[:, 0] = np.clip(cent[:, 0] * 1.08 + 16, 0, 255)
    bgr = cv2.cvtColor(np.clip(cent, 0, 255).astype(np.uint8)[None], cv2.COLOR_LAB2BGR)[0]
    return cent.astype(np.float32), bgr.astype(np.float32) / 255


PAL_LAB, PAL_BGR = None, None
LW = np.array([0.55, 1.0, 1.0], np.float32)   # cluster on hue more than on light


def characters(src, mask, n):
    global PAL_LAB, PAL_BGR
    if PAL_LAB is None:
        PAL_LAB, PAL_BGR = build_palette()
    rng = np.random.default_rng(1000 + n)
    ms = cv2.pyrMeanShiftFiltering(src, 8, 28)
    lab = cv2.cvtColor(ms, cv2.COLOR_BGR2LAB).astype(np.float32)
    # match against the un-boosted palette (undo the boost for distance)
    raw = PAL_LAB.copy()
    raw[:, 1:] = 128 + (raw[:, 1:] - 128) / 2.1
    raw[:, 0] = (raw[:, 0] - 16) / 1.08
    d = (((lab[:, :, None, :] - raw[None, None]) * LW) ** 2).sum(-1)
    # despeckle: soft-vote the labels over a small neighbourhood
    votes = np.exp(-(d - d.min(-1, keepdims=True)) / 120.0)
    votes = cv2.GaussianBlur(votes, (0, 0), 3.6)
    lbl = votes.argmax(-1)
    lbl = cv2.medianBlur(cv2.medianBlur(lbl.astype(np.uint8), 7), 7)
    # absorb small paint islands into the surrounding colour (cel painters
    # fill big closed shapes, not texture)
    big = cv2.GaussianBlur(votes, (0, 0), 9).argmax(-1).astype(np.uint8)
    for c in np.unique(lbl):
        num, lb, st, _ = cv2.connectedComponentsWithStats((lbl == c).astype(np.uint8), connectivity=8)
        small = (st[:, cv2.CC_STAT_AREA] < 500)
        small[0] = False
        sm = small[lb]
        lbl[sm] = big[sm]
    # one skin paint for the whole episode: fold every skin-tone paint into the
    # lightest one (fixed choice, so skin never flickers between paints)
    sk = np.where((PAL_LAB[:, 0] > 110) & (PAL_LAB[:, 0] < 200) & (PAL_LAB[:, 1] > 130) & (PAL_LAB[:, 2] > 140))[0]
    if len(sk) > 1:
        lbl[np.isin(lbl, sk)] = sk[PAL_LAB[sk, 0].argmax()]
    cel = PAL_BGR[lbl] * rng.uniform(0.975, 1.025)            # flat paint + tiny gain flicker
    # ONE hard shadow layer (no ink on shadow edges, like real cel shadows)
    lum = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY).astype(np.float32)
    local = cv2.GaussianBlur(lum, (0, 0), 16)
    sh = (cv2.GaussianBlur(lum, (0, 0), 4) < local - 14).astype(np.uint8)
    sh = cv2.morphologyEx(sh, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
    sh = (cv2.GaussianBlur(sh.astype(np.float32), (0, 0), 4.5) > 0.5).astype(np.uint8)
    num, lb, st, _ = cv2.connectedComponentsWithStats(sh, connectivity=8)
    ok = st[:, cv2.CC_STAT_AREA] > 400
    ok[0] = False
    sh = ok[lb]
    cel[sh] = cel[sh] * np.array([0.74, 0.64, 0.70], np.float32)
    hi = (cv2.GaussianBlur(lum, (0, 0), 3) > local + 26) & (lum > 160)
    hi = cv2.medianBlur(hi.astype(np.uint8) * 255, 7) > 127
    cel[hi] = np.clip(cel[hi] * 1.15 + 0.07, 0, 1)
    # inner ink: only between palette colours that are clearly different
    pd = np.sqrt((((PAL_LAB[:, None] - PAL_LAB[None]) * LW) ** 2).sum(-1))
    inner = np.zeros((h, w), np.uint8)
    for sy, sx in ((0, 1), (1, 0)):
        a = lbl[: h - sy, : w - sx]
        b = lbl[sy:, sx:]
        e = pd[a, b] > 34
        inner[: h - sy, : w - sx] |= e
    inner = cv2.dilate(inner, np.ones((2, 2), np.uint8))
    num, lb, st, _ = cv2.connectedComponentsWithStats(inner, connectivity=8)
    ok = st[:, cv2.CC_STAT_AREA] > 90
    ok[0] = False
    inner = ok[lb].astype(np.uint8)
    # facial features as solid black shapes
    hsv0 = cv2.cvtColor(src, cv2.COLOR_BGR2HSV).astype(np.float32)
    skin = ((hsv0[..., 0] < 22) & (hsv0[..., 1] > 50) & (hsv0[..., 1] < 175) & (hsv0[..., 2] > 80)).astype(np.float32)
    near_skin = cv2.GaussianBlur(skin, (0, 0), 6) > 0.25
    feat = ((lum < np.minimum(100, 0.62 * cv2.GaussianBlur(lum, (0, 0), 8))) & near_skin).astype(np.uint8)
    num, lb, st, _ = cv2.connectedComponentsWithStats(feat, connectivity=8)
    ok = (st[:, cv2.CC_STAT_AREA] > 6) & (st[:, cv2.CC_STAT_AREA] < 600)
    ok[0] = False
    feat = ok[lb].astype(np.uint8)
    m8 = (mask > 0.5).astype(np.uint8)
    inside = cv2.erode(m8, np.ones((5, 5), np.uint8))
    ink_in = np.maximum(inner * inside * (cv2.GaussianBlur(skin, (0, 0), 5) < 0.15), feat)
    # thick silhouette line
    sil = cv2.dilate(m8, np.ones((7, 7), np.uint8)) - cv2.erode(m8, np.ones((3, 3), np.uint8))
    ink = np.maximum(ink_in, sil).astype(np.float32)
    # line boil: new small displacement each frame
    dx = cv2.resize(rng.normal(0, 1, (h // 30, w // 30)).astype(np.float32), (w, h), interpolation=cv2.INTER_CUBIC) * 1.3
    dy = cv2.resize(rng.normal(0, 1, (h // 30, w // 30)).astype(np.float32), (w, h), interpolation=cv2.INTER_CUBIC) * 1.3
    ink = cv2.remap(ink, xx0 + dx, yy0 + dy, cv2.INTER_LINEAR)
    # brush-pen weight variation along the line
    weight = 0.8 + 0.4 * cv2.resize(rng.random((h // 20, w // 20)).astype(np.float32), (w, h))
    ink = np.clip(cv2.GaussianBlur(ink, (0, 0), 0.6) * 1.6 * weight, 0, 1)
    return np.clip(cel, 0, 1), ink, cv2.dilate(m8, np.ones((7, 7), np.uint8))


def cel_dirt(n):
    """Dust specks + hairs that live on the cel for a few frames."""
    layer = np.zeros((h, w), np.float32)
    for k in range(3):
        epoch = (n + k * 2) // 5 + k * 100
        rng = np.random.default_rng(epoch)
        for _ in range(int(rng.integers(2, 6))):
            x, y = rng.integers(0, w), rng.integers(0, h)
            cv2.circle(layer, (int(x), int(y)), int(rng.integers(1, 3)), 1.0, -1, cv2.LINE_AA)
        if rng.random() < 0.6:
            pts = [(int(rng.integers(0, w)), int(rng.integers(0, h)))]
            a = rng.uniform(0, 2 * np.pi)
            for _ in range(6):
                a += rng.normal(0, 0.5)
                pts.append((int(pts[-1][0] + 6 * np.cos(a)), int(pts[-1][1] + 6 * np.sin(a))))
            cv2.polylines(layer, [np.array(pts, np.int32)], False, 1.0, 1, cv2.LINE_AA)
    return layer


def sd_video(img, n):
    """Standard-definition broadcast feel: chroma bleed, ringing, grain, upscale."""
    u8 = (np.clip(img, 0, 1) * 255).astype(np.uint8)
    ycc = cv2.cvtColor(u8, cv2.COLOR_BGR2YCrCb).astype(np.float32)
    for c in (1, 2):
        ch = cv2.resize(ycc[..., c], (w // 2, h), interpolation=cv2.INTER_AREA)
        ch = cv2.resize(ch, (w, h), interpolation=cv2.INTER_LINEAR)
        ycc[..., c] = np.roll(cv2.GaussianBlur(ch, (5, 1), 0), 2, axis=1)
    y = ycc[..., 0]
    ycc[..., 0] = y + 0.45 * (y - cv2.GaussianBlur(y, (0, 0), 1.6))     # sharpening halo
    ycc[..., 0] += np.random.default_rng(5000 + n).normal(0, 2.2, (h, w))
    out = cv2.cvtColor(np.clip(ycc, 0, 255).astype(np.uint8), cv2.COLOR_YCrCb2BGR)
    out = cv2.resize(out, (W, H), interpolation=cv2.INTER_CUBIC)
    return cv2.GaussianBlur(out, (0, 0), 0.7)


def render(n):
    src, mask = read(n)
    bg = background(src)
    cel, ink, cover = characters(src, mask, n)
    m = cv2.GaussianBlur(cover.astype(np.float32), (0, 0), 0.7)[..., None]
    m = np.maximum(m, cv2.GaussianBlur(mask, (0, 0), 0.7)[..., None])
    img = bg * (1 - m) + cel * m
    img = img * (1 - ink[..., None]) + np.array([0.05, 0.04, 0.06], np.float32) * ink[..., None]
    dirt = cel_dirt(n)
    img = img * (1 - 0.55 * dirt[..., None])
    out = sd_video(img, n)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), out)
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    nums = frame_list()
    with Pool(min(8, os.cpu_count() or 4)) as p:
        for n in p.imap_unordered(render, nums):
            print(n, end=" ", flush=True)
    print()
