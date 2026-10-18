"""Papercraft Layered Diorama — local approximation of the frame-by-frame restyle.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [all | 13 49 85 ...]

Every frame is rebuilt as a stack of cut, coloured card:
  * colours are flattened (edge-preserving smoothing) and snapped to a fixed set
    of cardstock colours (k-means once over several frames, then a little brighter
    and more saturated, like coloured card);
  * each colour becomes one cut sheet: the label map is cleaned with a soft
    majority vote so every sheet has smooth, knife-cut curves, no pixel noise;
  * every sheet sits at its own height: the room at the back (light wall lowest,
    darker objects stacked in front of it), the people above the room, and inside
    each group darker sheets on top (hair over face, eyes over skin);
  * each sheet casts a soft drop shadow down-right onto the sheets below it, the
    shadow longer where the height step is bigger; the cut edge facing the light
    gets a thin bright rim (card thickness);
  * a fixed paper-fibre grain per sheet, warm soft key light, slight depth of field
    on the back layers, vignette;
  * a tiny per-frame jitter of the people layers, like cut-outs repositioned by hand
    for each stop-motion frame (the room layers never move).
"""
import sys
from pathlib import Path

import cv2
import numpy as np

cv2.setNumThreads(2)
W, H = 1620, 1080
w, h = W // 2, H // 2
HERE = Path(__file__).resolve().parent
PAL_FILE = HERE / "palette.npz"


def lab(rgb):
    return cv2.cvtColor(np.clip(rgb, 0, 255).astype(np.uint8), cv2.COLOR_RGB2LAB).astype(np.float32)


def flat(rgb, k=0.35):
    f = rgb.astype(np.float32)
    lum = f.mean(-1, keepdims=True) + 8
    big = cv2.GaussianBlur(lum, (0, 0), 30)[..., None]
    return np.clip(f * (big / lum) ** k, 0, 255).astype(np.uint8)


def smooth(rgb):
    s = cv2.resize(flat(rgb), (w, h), interpolation=cv2.INTER_AREA)
    for _ in range(3):
        s = cv2.bilateralFilter(s, 9, 30, 6)
    return cv2.medianBlur(s, 5)


def build_palette(frames_dir, masks_dir):
    pp, bp = [], []
    for n in (1, 13, 49, 85, 109, 145, 178):
        rgb = cv2.cvtColor(cv2.imread(str(frames_dir / f"frame_{n:03d}.png")), cv2.COLOR_BGR2RGB)
        m = cv2.resize(cv2.imread(str(masks_dir / f"frame_{n:03d}.png"), 0), (w, h)) > 128
        L = lab(smooth(rgb)).reshape(-1, 3)
        pp.append(L[m.ravel()][::7])
        bp.append(L[~m.ravel()][::9])
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 40, 0.5)
    _, _, cp = cv2.kmeans(np.concatenate(pp), 14, None, crit, 3, cv2.KMEANS_PP_CENTERS)
    _, _, cb = cv2.kmeans(np.concatenate(bp), 9, None, crit, 3, cv2.KMEANS_PP_CENTERS)
    np.savez(PAL_FILE, people=cp, room=cb)


def card_colours(pal_lab):
    """Lab centres -> RGB card colours: a little lighter and more saturated, matte."""
    c = pal_lab.copy()
    c[:, 1:] = 128 + (c[:, 1:] - 128) * 1.85
    c[:, 0] = 44 + c[:, 0] * 0.9
    rgb = cv2.cvtColor(np.clip(c, 0, 255).astype(np.uint8)[None], cv2.COLOR_LAB2RGB)[0].astype(np.float32)
    return rgb


GRAIN = None


def grain():
    global GRAIN
    if GRAIN is None:
        rng = np.random.default_rng(5)
        fine = cv2.GaussianBlur(rng.standard_normal((H, W)).astype(np.float32), (0, 0), 0.7)
        fib = cv2.GaussianBlur(rng.standard_normal((H, W)).astype(np.float32), (0, 0), 0.6)
        fib = cv2.filter2D(fib, -1, np.ones((1, 9), np.float32) / 9)   # long paper fibres
        mot = cv2.resize(cv2.GaussianBlur(rng.standard_normal((h // 6, w // 6)).astype(np.float32), (0, 0), 2), (W, H))
        GRAIN = (fine / fine.std(), fib / fib.std(), mot / mot.std())
    return GRAIN


def shift(a, dy, dx):
    M = np.float32([[1, 0, dx], [0, 1, dy]])
    return cv2.warpAffine(a, M, (a.shape[1], a.shape[0]), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)


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


def face_zone(m):
    """Half-res soft map of the head ellipses (from the matte), where cut feature pieces are allowed."""
    z = np.zeros((H, W), np.uint8)
    for xc, y0, yn, hw in heads(m):
        cy = int(y0 + (yn - y0) * 0.55)
        cv2.ellipse(z, (int(xc), cy), (int(hw * 0.62), int((yn - y0) * 0.62)), 0, 0, 360, 1, -1)
    return cv2.resize(z, (w, h), interpolation=cv2.INTER_NEAREST) > 0


def render(rgb, m, frame_no, pal):
    rng = np.random.default_rng(frame_no * 131)
    mh = cv2.resize(m, (w, h), interpolation=cv2.INTER_AREA)
    s = lab(smooth(rgb))
    P, R = pal["people"], pal["room"]
    allp = np.concatenate([P, R])
    d = ((s[:, :, None, :] - allp[None, None]) ** 2).sum(-1)
    d[..., :len(P)] += np.where(mh > 0.5, 0, 1e6)[..., None]
    d[..., len(P):] += np.where(mh > 0.5, 1e6, 0)[..., None]
    idx = d.argmin(-1)
    # knife-cut shapes: soft majority vote over each label's one-hot map
    votes = np.stack([cv2.GaussianBlur((idx == k).astype(np.float32), (0, 0), 3.4) for k in range(len(allp))], -1)
    idx = votes.argmax(-1)

    # small cut pieces of dark card for the features: eyes, brows, lashes, mouth, glasses rims, collar
    gr = cv2.cvtColor(cv2.resize(rgb, (w, h), interpolation=cv2.INTER_AREA), cv2.COLOR_RGB2GRAY).astype(np.float32)
    dog = cv2.GaussianBlur(gr, (0, 0), 4) - cv2.GaussianBlur(gr, (0, 0), 1.0)
    inner = cv2.erode((mh > 0.5).astype(np.uint8), np.ones((9, 9), np.uint8)) > 0
    det = (cv2.GaussianBlur(((dog > 9) & inner & face_zone(m)).astype(np.float32), (0, 0), 1.0) > 0.45).astype(np.uint8)
    n, lab_cc, stats, _ = cv2.connectedComponentsWithStats(det, connectivity=8)
    keep = np.zeros(n, bool)
    keep[1:] = stats[1:, cv2.CC_STAT_AREA] >= 10
    idx = np.where(keep[lab_cc], len(allp), idx)

    col_tab = np.concatenate([card_colours(allp), np.float32([[58, 40, 36]])])
    # heights: room 0..len(R)-1 by darkness (light wall at the back), people above, darker on top
    Lr = R[:, 0]
    Lp = P[:, 0]
    hr = np.argsort(np.argsort(-Lr)).astype(np.float32)
    hp = len(R) + 2 + np.argsort(np.argsort(-Lp)).astype(np.float32) * 0.5
    htab = np.concatenate([hp, hr, [hp.max() + 1.0]])

    # stop-motion jitter of the people layers only
    jx, jy = rng.uniform(-1.0, 1.0, 2)
    person = ((idx < len(P)) | (idx == len(allp))).astype(np.float32)
    idx_p = cv2.warpAffine(idx.astype(np.float32), np.float32([[1, 0, jx], [0, 1, jy]]), (w, h), flags=cv2.INTER_NEAREST, borderMode=cv2.BORDER_REPLICATE).astype(np.int64)
    pers_j = cv2.warpAffine(person, np.float32([[1, 0, jx], [0, 1, jy]]), (w, h), flags=cv2.INTER_NEAREST, borderMode=cv2.BORDER_REPLICATE)
    idx = np.where(pers_j > 0.5, idx_p, np.where(person > 0.5, idx, idx))

    hmap = htab[idx]
    # full-res label map so the cut curves stay crisp
    hfull = cv2.resize(hmap, (W, H), interpolation=cv2.INTER_NEAREST)
    idx_full = cv2.resize(idx.astype(np.float32), (W, H), interpolation=cv2.INTER_NEAREST).astype(np.int64)
    hs = cv2.GaussianBlur(hfull, (0, 0), 1.0)
    col = col_tab[idx_full]

    # paper grain: each sheet gets its own grain offset (different card)
    fine, fib, mot = grain()
    off = (idx_full * 37) % 61
    g = 0.035 * np.take_along_axis(np.stack([fine, np.roll(fine, 29, 1)], 0), (off % 2)[None], 0)[0] + 0.03 * fib + 0.025 * mot
    col *= (1 + g)[..., None]

    # drop shadows: each sheet shades the lower sheets down-right of it
    sh = np.zeros((H, W), np.float32)
    for t in range(1, 9):
        up = shift(hs, 2.2 * t, 1.6 * t)
        sh = np.maximum(sh, np.clip((up - hs) - 0.35 * t, 0, 1.5) * (1 - t / 11))
    sh = cv2.GaussianBlur(sh, (0, 0), 4.0)
    col *= (1 - 0.42 * np.clip(sh, 0, 1))[..., None]
    # contact darkening right at each cut edge on the lower sheet
    rim_dark = np.clip(shift(hs, 2, 1.5) - hs, 0, 1)
    col *= (1 - 0.25 * cv2.GaussianBlur(rim_dark, (0, 0), 1.2))[..., None]
    # bright rim on the cut edge that faces the light (card thickness)
    rim = np.clip(hs - shift(hs, 2.5, 2.0), 0, 1)
    col += (cv2.GaussianBlur(rim, (0, 0), 0.8) * 55)[..., None]

    # depth of field: back sheets a bit soft
    blur = cv2.GaussianBlur(col, (0, 0), 1.8)
    near = np.clip(hs / (len(R) + 2), 0, 1)[..., None]
    col = col * near + blur * (1 - near)

    # warm soft key light, vignette
    gy, gx = np.mgrid[0:H, 0:W].astype(np.float32)
    yy, xx = gy / H, gx / W
    key = 1.1 - 0.18 * (0.55 * xx + 0.45 * yy)
    vig = 1 - 0.25 * (((xx - 0.5) / 0.75) ** 2 + ((yy - 0.5) / 0.7) ** 2)
    col *= (key * vig)[..., None] * np.array([1.03, 1.0, 0.95], np.float32)
    col += rng.normal(0, 1.5, (H, W, 1)).astype(np.float32)
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
