"""Low-poly 3D / PS1-era render restyle, frame by frame.

usage: python -I render.py [frame numbers... | all]   (default: the six sheet frames)
       RENDER_OUT=/tmp/prompt-video-render/40-low-poly-3d python -I render.py all   -> full clip for make_video.py
Reads ../../_source/frames + ../../_source/masks, writes ./frames/frame_NNN.png.

Pipeline per frame:
* room: a coarse fixed triangle mesh, each triangle texture-mapped from a tiny nearest-neighbour
  texture with plain affine mapping, vertices wobbling a pixel or two per frame (PS1 texture swim),
  plus distance fog;
* people: re-triangulated every frame (silhouette polygon + jittered interior grid, denser on skin,
  corner features on faces), each triangle flat-shaded with its mean colour and lit by a fake
  normal from a bulged depth, so bodies read as faceted polyhedra;
* the whole frame is snapped to a 540x360 framebuffer, 15-bit colour with 4x4 ordered dither,
  shown with nearest-neighbour upscale.
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "..", "_source")
FRAMES, MASKS = os.path.join(SRC, "frames"), os.path.join(SRC, "masks")
OUT = os.environ.get("RENDER_OUT", os.path.join(HERE, "frames"))
ONLY = (list(range(1, 180)) if sys.argv[1:] == ["all"] else [int(a) for a in sys.argv[1:]]) or [13, 49, 85, 109, 145, 178]
W, H = 1620, 1080
FB = 3                                     # framebuffer = 540x360
FOG = np.array([0.42, 0.34, 0.30], np.float32)   # BGR, dusty blue-grey
BAYER = (np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]], np.float32) + 0.5) / 16 - 0.5


def delaunay(pts):
    sub = cv2.Subdiv2D((-2, -2, W + 4, H + 4))
    for p in pts:
        sub.insert((float(p[0]), float(p[1])))
    tri = sub.getTriangleList().reshape(-1, 3, 2)
    ok = (tri[..., 0].min(1) >= -1) & (tri[..., 0].max(1) <= W + 1) & (tri[..., 1].min(1) >= -1) & (tri[..., 1].max(1) <= H + 1)
    return tri[ok]


# ---------- room: fixed mesh, affine texture swim ----------
_r = np.random.default_rng(40)
_gy, _gx = np.mgrid[0:H + 1:105, 0:W + 1:105].astype(np.float32)
_gx[:, 1:-1] += _r.uniform(-34, 34, _gx[:, 1:-1].shape)
_gy[1:-1] += _r.uniform(-34, 34, _gy[1:-1].shape)
_gx[:, -1], _gy[-1] = W - 1, H - 1
BG_PTS = np.stack([_gx.ravel(), _gy.ravel()], 1).clip(0, [W - 1, H - 1])
BG_TRI_IDX = None


def bg_triangles():
    global BG_TRI_IDX
    if BG_TRI_IDX is None:
        tri = delaunay(BG_PTS)
        idx = []
        for t in tri:
            d = ((BG_PTS[None] - t[:, None]) ** 2).sum(-1)
            idx.append(d.argmin(1))
        BG_TRI_IDX = np.array(idx)
    return BG_TRI_IDX


def room(bgr, n, rng):
    tex = cv2.resize(bgr, (W // 12, H // 12), interpolation=cv2.INTER_AREA)
    tex = cv2.resize(tex, (W, H), interpolation=cv2.INTER_NEAREST)        # chunky low-res texture, no filtering
    edge = (BG_PTS[:, 0] <= 0) | (BG_PTS[:, 0] >= W - 1) | (BG_PTS[:, 1] <= 0) | (BG_PTS[:, 1] >= H - 1)
    wob = np.round(rng.normal(0, 1.0, BG_PTS.shape) * (rng.random((len(BG_PTS), 1)) < 0.5)) * FB
    wob[edge] = 0
    dst_pts = BG_PTS + wob
    out = np.zeros_like(bgr)
    lab = np.zeros((H, W), np.int32)
    for i, t in enumerate(bg_triangles()):
        s = BG_PTS[t].astype(np.float32)
        d = dst_pts[t].astype(np.float32)
        # PS1 affine texture: each triangle maps its texture with a plain affine, sampled nearest,
        # from slightly skewed texture coordinates so straight lines kink at triangle seams
        skew = s + rng.normal(0, 4, s.shape).astype(np.float32)
        M = cv2.getAffineTransform(skew, d)
        x0, y0 = np.floor(d.min(0)).astype(int)
        x1, y1 = np.ceil(d.max(0)).astype(int)
        x0, y0, x1, y1 = max(0, x0), max(0, y0), min(W, x1 + 1), min(H, y1 + 1)
        if x1 <= x0 or y1 <= y0:
            continue
        M2 = M.copy()
        M2[:, 2] -= (x0, y0)
        patch = cv2.warpAffine(tex, M2, (x1 - x0, y1 - y0), flags=cv2.INTER_NEAREST, borderMode=cv2.BORDER_REFLECT)
        msk = np.zeros((y1 - y0, x1 - x0), np.uint8)
        cv2.fillConvexPoly(msk, np.round(d - (x0, y0)).astype(np.int32), 1)
        sub = out[y0:y1, x0:x1]
        sub[msk > 0] = patch[msk > 0]
        cv2.fillConvexPoly(lab, np.round(d).astype(np.int32), int(i + 1))
    f = out.astype(np.float32) / 255
    # fixed-function flat lighting per room triangle: a soft per-face brightness step
    shade = np.random.default_rng(41).uniform(0.80, 1.12, len(bg_triangles()) + 1).astype(np.float32)
    f *= shade[lab][..., None]
    # distance fog toward the top/back of the room
    yy = np.linspace(1, 0, H, dtype=np.float32)[:, None, None]
    fog = 0.22 + 0.18 * yy
    return f * (1 - fog) + FOG * fog


# ---------- people: re-triangulated flat-shaded polyhedra ----------
def person_points(bgr, m, rng):
    mb = (m > 0.5).astype(np.uint8)
    pts = []
    cnts, _ = cv2.findContours(mb, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for c in cnts:
        if cv2.contourArea(c) < 1500:
            continue
        ap = cv2.approxPolyDP(c, 10.0, True)[:, 0, :]
        pts.append(ap.astype(np.float32))
    ycc = cv2.cvtColor(bgr, cv2.COLOR_BGR2YCrCb)
    skin = ((ycc[..., 1] > 136) & (ycc[..., 1] < 175) & (ycc[..., 2] > 85) & (ycc[..., 2] < 128)) & (mb > 0)
    skin = cv2.morphologyEx(skin.astype(np.uint8), cv2.MORPH_OPEN, np.ones((7, 7), np.uint8))
    inner = cv2.erode(mb, np.ones((9, 9), np.uint8))
    for step, sel in ((80, inner), (40, skin)):
        gy, gx = np.mgrid[0:H:step, 0:W:step].astype(np.float32)
        gx += rng.uniform(0, step, gx.shape)
        gy += rng.uniform(0, step, gy.shape)
        gx, gy = gx.clip(0, W - 1).ravel(), gy.clip(0, H - 1).ravel()
        ok = sel[gy.astype(int), gx.astype(int)] > 0
        pts.append(np.stack([gx[ok], gy[ok]], 1))
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    fm = cv2.dilate(skin, np.ones((15, 15), np.uint8)) & inner
    # vertices on image edges (one per cell), so facets follow brows, eyes, mouth, jaw, folds
    edges = cv2.Canny(cv2.GaussianBlur(gray, (0, 0), 1.6), 40, 100) > 0
    for cell, sel in ((15, fm > 0), (40, (inner > 0) & (fm == 0))):
        ey, ex = np.nonzero(edges & sel)
        if len(ex):
            key = (ey // cell) * (W // cell + 1) + ex // cell
            order = rng.permutation(len(ex))
            _, first = np.unique(key[order], return_index=True)
            pick = order[first]
            pts.append(np.stack([ex[pick], ey[pick]], 1).astype(np.float32))
    c = cv2.goodFeaturesToTrack(gray, 120, 0.03, 17, mask=fm)
    if c is not None:
        pts.append(c[:, 0, :].astype(np.float32))
    c = cv2.goodFeaturesToTrack(gray, 70, 0.05, 48, mask=inner)
    if c is not None:
        pts.append(c[:, 0, :].astype(np.float32))
    p = np.concatenate(pts, 0)
    p += rng.normal(0, 1.2, p.shape)                                  # vertex wobble
    p = np.round(p / FB) * FB                                         # integer framebuffer snapping
    return np.unique(p.clip(0, [W - 1, H - 1]), axis=0)


def person_layer(bgr, m, rng):
    mb = (m > 0.5).astype(np.uint8)
    tri = delaunay(person_points(bgr, m, rng))
    cen = tri.mean(1)
    inside = cv2.dilate(mb, np.ones((5, 5), np.uint8))[cen[:, 1].astype(int).clip(0, H - 1), cen[:, 0].astype(int).clip(0, W - 1)] > 0
    tri = tri[inside]
    lab = np.zeros((H, W), np.int32)
    for i, t in enumerate(tri):
        cv2.fillConvexPoly(lab, np.round(t).astype(np.int32), int(i + 1))
    k = len(tri) + 1
    f = bgr.astype(np.float32) / 255
    cnt = np.bincount(lab.ravel(), minlength=k).astype(np.float32) + 1e-6
    mean = np.stack([np.bincount(lab.ravel(), f[..., c].ravel(), k) / cnt for c in range(3)], 1)
    # fake depth: bodies bulge toward the camera -> per-face normal -> flat lambert shade
    dt = cv2.distanceTransform(mb, cv2.DIST_L2, 5)
    z = np.sqrt(np.clip(dt / 110.0, 0, 1)) * 110.0
    z = cv2.GaussianBlur(z, (0, 0), 6)
    gx = cv2.Sobel(z, cv2.CV_32F, 1, 0, ksize=5) / 32
    gy = cv2.Sobel(z, cv2.CV_32F, 0, 1, ksize=5) / 32
    cx = np.bincount(lab.ravel(), gx.ravel(), k) / cnt
    cy = np.bincount(lab.ravel(), gy.ravel(), k) / cnt
    nrm = np.stack([-cx, -cy, np.ones_like(cx) * 0.9], 1)
    nrm /= np.linalg.norm(nrm, axis=1, keepdims=True)
    light = np.array([-0.45, -0.55, 0.70], np.float32)
    light /= np.linalg.norm(light)
    shade = 0.50 + 0.72 * np.clip(nrm @ light, 0, 1)
    shade *= rng.uniform(0.96, 1.04, k)                               # faceting
    col = np.clip(mean * shade[:, None] * 1.04, 0, 1)
    col[0] = 0
    return col[lab], lab > 0, tri


def framebuffer(img):
    small = cv2.resize(img, (W // FB, H // FB), interpolation=cv2.INTER_AREA)
    h, w = small.shape[:2]
    th = np.tile(BAYER, (h // 4 + 1, w // 4 + 1))[:h, :w][..., None]
    q = np.floor(np.clip(small + th / 31, 0, 1) * 31 + 0.5) / 31          # 15-bit colour, ordered dither
    return cv2.resize(q.astype(np.float32), (W, H), interpolation=cv2.INTER_NEAREST)


def render(n):
    rng = np.random.default_rng(4000 + n)
    bgr = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png"))
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
    img = room(bgr, n, rng)
    col, cover, tri = person_layer(bgr, m, rng)
    img = np.where(cover[..., None], col, img)
    img = framebuffer(img)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), (np.clip(img, 0, 1) * 255).astype(np.uint8))
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    with Pool(8) as p:
        for n in p.imap_unordered(render, ONLY):
            pass
    print("done", len(ONLY), "->", OUT)
