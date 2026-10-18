"""Claymation / plasticine stop-motion restyle, frame by frame, shot on twos.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [frame numbers... | all]
Frames are frame_001.png ... ; masks are person mattes with the same names.
Each pose (one per two output frames, "on twos") is flattened by mean shift and
snapped to a fixed plasticine palette (k-means over the clip, cached in
palette.npy). Every colour patch becomes a separate rounded clay piece: a height
map from the distance to the piece edge plus a big body bulge, thumbprint dents
and lumps, creases between pieces, lit by a soft warm studio key with a waxy
sheen. Boundaries wobble and thumbprints move from pose to pose (the clay is
re-sculpted), the set behind is softly out of focus like a miniature.
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np

FRAMES, MASKS, OUT = sys.argv[1:4]
ARGS = sys.argv[4:]
HERE = os.path.dirname(os.path.abspath(__file__))
H, W = 1080, 1620
NPAL = 22


def vnoise(rng, h, w, cell):
    a = rng.random((max(2, h // cell + 2), max(2, w // cell + 2))).astype(np.float32)
    return cv2.resize(a, (w, h), interpolation=cv2.INTER_CUBIC)


def clayify_lab(lab):
    lab = lab.astype(np.float32).copy()
    lab[..., 1:] = 128 + (lab[..., 1:] - 128) * 1.45
    lab[..., 0] = 48 + lab[..., 0] * 0.78          # clay never goes truly black or white
    return lab


def palette():
    path = os.path.join(HERE, "palette.npy")
    if os.path.exists(path):
        return np.load(path)
    samp = []
    for n in range(1, 180, 8):
        im = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png"))
        sm = cv2.resize(im, (W // 8, H // 8), interpolation=cv2.INTER_AREA)
        sm = cv2.bilateralFilter(sm, 7, 40, 7)
        samp.append(clayify_lab(cv2.cvtColor(sm, cv2.COLOR_BGR2LAB)).reshape(-1, 3))
    data = np.concatenate(samp).astype(np.float32)
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 60, 0.5)
    cv2.setRNGSeed(5)
    _, _, cen = cv2.kmeans(data, NPAL, None, crit, 4, cv2.KMEANS_PP_CENTERS)
    np.save(path, cen)
    return cen


def warp(img, rng, amp, cell, interp=cv2.INTER_NEAREST):
    """Smooth random displacement: the clay is pushed around a little between poses."""
    dx = (vnoise(rng, H, W, cell) - 0.5) * 2 * amp
    dy = (vnoise(rng, H, W, cell) - 0.5) * 2 * amp
    gx, gy = np.meshgrid(np.arange(W, dtype=np.float32), np.arange(H, dtype=np.float32))
    return cv2.remap(img, gx + dx, gy + dy, interp, borderMode=cv2.BORDER_REPLICATE)


def thumbprints(rng, count, area):
    """Height dents: concentric fingerprint ridges inside soft oval presses."""
    h = np.zeros((H, W), np.float32)
    ys, xs = np.nonzero(area[::6, ::6])
    if not len(ys):
        return h
    for k in rng.choice(len(ys), size=min(count, len(ys)), replace=False):
        cx, cy = xs[k] * 6, ys[k] * 6
        r = rng.uniform(22, 46)
        x0, x1 = int(max(0, cx - r * 1.4)), int(min(W, cx + r * 1.4))
        y0, y1 = int(max(0, cy - r * 1.4)), int(min(H, cy + r * 1.4))
        yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
        a = rng.uniform(0, np.pi)
        u = ((xx - cx) * np.cos(a) + (yy - cy) * np.sin(a)) / 1.0
        v = (-(xx - cx) * np.sin(a) + (yy - cy) * np.cos(a)) / 0.7
        d = np.sqrt(u ** 2 + v ** 2)
        fall = np.clip(1 - d / r, 0, 1) ** 1.5
        ridges = np.sin(d * 0.9 + rng.uniform(0, 6)) * 0.35
        h[y0:y1, x0:x1] += (-1.0 + ridges) * fall * 3.0
    return h


def skin_pieces(img, person):
    """Skin as one smooth piece per face/arm: YCrCb skin, closed, holes (eyes, mouth) kept."""
    ycc = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb).astype(int)
    y, cr, cb = ycc[..., 0], ycc[..., 1], ycc[..., 2]
    sk = (cr > 144) & (cr < 178) & (cb > 82) & (cb < 130) & (y > 60) & person
    sk = cv2.morphologyEx(sk.astype(np.uint8), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    sk = cv2.morphologyEx(sk, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    num, comp = cv2.connectedComponents(sk)
    return sk > 0, num, comp


def render(n):
    pose = n if n % 2 == 1 else n - 1                # shot on twos
    rng = np.random.default_rng(pose * 31337)
    pal = palette()
    pal_bgr = cv2.cvtColor(np.clip(pal[None], 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)[0].astype(np.float32) / 255

    img = cv2.imread(os.path.join(FRAMES, f"frame_{pose:03d}.png"))
    m = cv2.imread(os.path.join(MASKS, f"frame_{pose:03d}.png"), 0).astype(np.float32) / 255
    person = m > 0.5

    small = cv2.resize(img, (W // 2, H // 2), interpolation=cv2.INTER_AREA)
    ms = cv2.pyrMeanShiftFiltering(small, 12, 30, maxLevel=1)
    ms = cv2.bilateralFilter(ms, 9, 50, 9)
    ms = cv2.resize(ms, (W, H), interpolation=cv2.INTER_LINEAR)
    lab = clayify_lab(cv2.cvtColor(ms, cv2.COLOR_BGR2LAB))
    d = ((lab[:, :, None, :] - pal[None, None]) ** 2).sum(-1)
    lbl = d.argmin(-1).astype(np.uint8)
    # bigger, simpler pieces in the set than on the puppets
    lbl_bg = cv2.medianBlur(cv2.medianBlur(lbl, 21), 15)
    lbl_fg = cv2.medianBlur(cv2.medianBlur(lbl, 11), 7)
    lbl = np.where(person, lbl_fg, lbl_bg).astype(np.uint8)
    sk, num, comp = skin_pieces(img, person)
    for c in range(1, num):
        cm = comp == c
        if cm.sum() < 400:
            continue
        vals = np.bincount(lbl[cm], minlength=NPAL)
        lbl[cm] = vals.argmax()
    # facial features as separate little dark clay pieces pressed into the face
    face = sk.astype(np.uint8)
    ff = face.copy()
    cnts, _ = cv2.findContours(face, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(ff, cnts, -1, 1, -1)
    g0 = cv2.GaussianBlur(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32), (0, 0), 1.5)
    det = g0 - cv2.GaussianBlur(g0, (0, 0), 7)
    inner = cv2.erode(ff, np.ones((9, 9), np.uint8)) > 0
    feat = ((det < -9) | ((ff > 0) & (face == 0))) & inner
    feat = cv2.morphologyEx(feat.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    feat = cv2.morphologyEx(feat, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8)) > 0
    dark = clayify_lab(np.array([[[60, 142, 140]]], np.uint8))[0, 0]
    lbl[feat] = int(((pal - dark) ** 2).sum(-1).argmin())
    # puppet silhouette gets its own id range so it separates from the set
    lbl16 = lbl.astype(np.int32) + person.astype(np.int32) * 64
    lbl16 = warp(lbl16.astype(np.float32), rng, 2.5, 60).astype(np.int32)

    # piece boundaries -> distance -> rounded clay profile
    bnd = np.zeros((H, W), np.uint8)
    bnd[:, 1:] |= (lbl16[:, 1:] != lbl16[:, :-1])
    bnd[1:, :] |= (lbl16[1:, :] != lbl16[:-1, :])
    dt = cv2.distanceTransform((1 - bnd).astype(np.uint8), cv2.DIST_L2, 5)
    pm = (lbl16 >= 64).astype(np.uint8)
    r = np.where(pm > 0, 16.0, 30.0).astype(np.float32)
    t = np.clip(dt / r, 0, 1)
    hpiece = r * np.sqrt(1 - (1 - t) ** 2) * 0.55
    dtp = cv2.distanceTransform(pm, cv2.DIST_L2, 5)
    hbody = 90 * np.sqrt(np.clip(dtp / 110, 0, 1)) * pm
    lumps = (vnoise(rng, H, W, 70) - 0.5) * 7 + (vnoise(rng, H, W, 18) - 0.5) * 2.5
    hprint = thumbprints(rng, int(rng.integers(26, 40)), dtp > 12)
    hprint += thumbprints(rng, 14, pm == 0) * 0.8
    tool = (np.sin((np.arange(W)[None] * 0.21 + np.arange(H)[:, None] * 0.07) + vnoise(rng, H, W, 40) * 5) * 0.4) * (pm == 0)
    h = hpiece + hbody + lumps + hprint + tool
    h = cv2.GaussianBlur(h.astype(np.float32), (0, 0), 1.6)

    # normals + soft studio light (warm key upper-left, cool fill, waxy sheen)
    gy, gx = np.gradient(h)
    nz = np.ones_like(h)
    nrm = np.stack([-gx, -gy, nz], -1)
    nrm /= np.linalg.norm(nrm, axis=-1, keepdims=True)
    key = np.array([-0.55, -0.6, 0.58]); key /= np.linalg.norm(key)
    fill = np.array([0.6, 0.1, 0.8]); fill /= np.linalg.norm(fill)
    diff = np.clip(nrm @ key, 0, 1)
    dfil = np.clip(nrm @ fill, 0, 1)
    half = key + np.array([0, 0, 1.0]); half /= np.linalg.norm(half)
    spec = np.clip(nrm @ half, 0, 1) ** 22 * 0.22
    ao = 1 - 0.45 * np.exp(-dt / 3.5)
    lbl_w = np.clip(lbl16 % 64, 0, NPAL - 1)
    alb = pal_bgr[lbl_w]
    # keep a little of the real shading so faces stay readable
    g = cv2.cvtColor(ms, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
    gb = cv2.GaussianBlur(g, (0, 0), 25) + 1e-3
    alb = alb * np.clip(0.72 + 0.28 * g / gb, 0.5, 1.3)[..., None]
    warm = np.array([0.86, 0.95, 1.05], np.float32)
    cool = np.array([1.05, 0.98, 0.9], np.float32)
    shade = (0.42 + 0.72 * diff)[..., None] * warm + (0.2 * dfil)[..., None] * cool
    out = alb * shade * ao[..., None] + spec[..., None] * np.array([0.9, 0.95, 1.0])

    # contact shadow of the puppets on the set
    sh = cv2.GaussianBlur(pm.astype(np.float32), (0, 0), 18)
    sh = np.roll(sh, (14, 22), (0, 1))
    out *= (1 - 0.35 * sh * (pm == 0))[..., None]
    # miniature set: background softly out of focus
    bgb = cv2.GaussianBlur(out, (0, 0), 2.6)
    pmf = cv2.GaussianBlur(pm.astype(np.float32), (0, 0), 1.2)[..., None]
    out = out * pmf + bgb * (1 - pmf)
    # studio vignette + slight exposure flicker between poses
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    vig = 1 - 0.28 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) ** 1.4
    out *= (vig * 1.08 * (1 + rng.normal(0, 0.012)))[..., None]
    o8 = np.clip(out * 255, 0, 255).astype(np.uint8)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), o8)
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    palette()
    nums = list(range(1, 180)) if (not ARGS or ARGS == ["all"]) else [int(a) for a in ARGS]
    with Pool(6) as p:
        for n in p.imap_unordered(render, nums):
            print(n, end=" ", flush=True)
    print()
