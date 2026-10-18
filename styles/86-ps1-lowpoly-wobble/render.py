"""PS1 Low-Poly Wobble: the clip as a 1996 PlayStation game frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [all | frame numbers...]

Per frame, rendered at 270x180 (a chunky 240p-class frame) and blown up 6x with
nearest neighbour so every pixel stays square:
  * the image is cut into a triangle mesh (people get a finer mesh than the
    room) and the texture inside each triangle is mapped AFFINELY from its
    three corners, so a smooth swim field turns into kinks along the triangle
    seams, like PS1 affine texture mapping
  * every vertex is snapped to the integer pixel grid and jitters by up to one
    pixel each frame (PS1 vertex wobble); the swim field drifts slowly
  * textures are low-res and point-sampled (blocky texels, no filtering);
    the room texture is half the resolution of the people texture
  * people are cut out as hard polygon silhouettes (approxPolyDP of the mask),
    no anti-aliasing
  * Gouraud-style vertex lighting from a fake rounded height field
  * linear distance fog: the room sits deep in grey-teal fog, people get a
    little fog when they stand far back (small in frame)
  * 15-bit colour with the fixed 4x4 ordered dither (exaggerated to ~4 bits per
    channel so it reads at sheet size); the dither is screen-space and does
    not boil
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np

FRAMES, MASKS, OUT = sys.argv[1:4]
ARGS = sys.argv[4:]
W, H = 1620, 1080
S = 6
LW, LH = W // S, H // S            # 270 x 180
FOG = np.array([0.20, 0.17, 0.13], np.float32)   # BGR dark blue-grey fog
PAL = None                                       # shared 4-bit-style CLUT, set per worker
BAYER = (np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]], np.float32) + 0.5) / 16 - 0.5


def load(n):
    img = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png")).astype(np.float32) / 255
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
    return img, m


def mesh_field(step, vx, vy):
    """Piecewise-linear (per triangle) interpolation of vertex values over the low-res frame.
    vx, vy: (gh, gw) vertex values on a grid with spacing `step`. Cells are split by
    alternating diagonals, so the field has kinks along triangle edges."""
    ys, xs = np.mgrid[0:LH, 0:LW].astype(np.float32)
    gx, gy = xs / step, ys / step
    i, j = np.floor(gy).astype(int), np.floor(gx).astype(int)
    i = np.clip(i, 0, vx.shape[0] - 2)
    j = np.clip(j, 0, vx.shape[1] - 2)
    u, v = gx - j, gy - i
    flip = ((i + j) % 2).astype(bool)
    uu = np.where(flip, 1 - u, u)            # mirror the cell so the diagonal alternates
    j0, j1 = np.where(flip, j + 1, j), np.where(flip, j, j + 1)
    out = []
    for f in (vx, vy):
        a, b = f[i, j0], f[i, j1]
        c, d = f[i + 1, j0], f[i + 1, j1]
        lower = uu + v <= 1
        r = np.where(lower, a + (b - a) * uu + (c - a) * v,
                     d + (c - d) * (1 - uu) + (b - d) * (1 - v))
        out.append(r.astype(np.float32))
    return out


def warp_maps(step, n, seed, amp_swim, amp_jit):
    gh, gw = LH // step + 2, LW // step + 2
    gy, gx = np.mgrid[0:gh, 0:gw].astype(np.float32) * step
    t = n / 12.0
    # smooth swim, like perspective-incorrect texture interpolation drifting with the camera
    sx = amp_swim * np.sin(gy / 37.0 + t * 1.3 + seed) * np.cos(gx / 53.0 - t * 0.7)
    sy = amp_swim * np.cos(gx / 41.0 + t * 1.1 + seed) * np.sin(gy / 29.0 + t * 0.9)
    rng = np.random.default_rng(seed * 1000 + n)
    jx = rng.integers(-1, 2, (gh, gw)) * amp_jit
    jy = rng.integers(-1, 2, (gh, gw)) * amp_jit
    # vertex positions snap to whole pixels
    px = np.round(gx + sx + jx) - gx
    py = np.round(gy + sy + jy) - gy
    dx, dy = mesh_field(step, px, py)
    ys, xs = np.mgrid[0:LH, 0:LW].astype(np.float32)
    return xs + dx, ys + dy


def clut(t):
    """Snap texels to the shared palette (PS1 textures were 4/8-bit CLUT images)."""
    flat = t.reshape(-1, 3)
    d = ((flat[:, None, :] - PAL[None]) ** 2).sum(2)
    return PAL[d.argmin(1)].reshape(t.shape)


def texture(img, scale):
    """Low-res point-sampled CLUT texture at `scale` of the low-res frame, returned at LW x LH."""
    tw, th = max(8, int(LW * scale)), max(8, int(LH * scale))
    t = clut(cv2.resize(img, (tw, th), interpolation=cv2.INTER_AREA))
    return cv2.resize(t, (LW, LH), interpolation=cv2.INTER_NEAREST)


def make_palette(k=28):
    smp = []
    for n in (13, 49, 85, 109, 145, 178):
        img, _ = load(n)
        smp.append(grade(cv2.resize(img, (90, 60), interpolation=cv2.INTER_AREA)).reshape(-1, 3))
    smp = np.concatenate(smp).astype(np.float32)
    _, _, c = cv2.kmeans(smp, k, None, (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 40, 1e-3),
                         4, cv2.KMEANS_PP_CENTERS)
    return c.astype(np.float32)


def init(pal):
    global PAL
    PAL = pal


def grade(img):
    # slight PS1-ish grade: contrast up, saturation a little down
    g = np.clip((img - 0.5) * 1.15 + 0.47, 0, 1)
    gray = g.mean(2, keepdims=True)
    return gray + (g - gray) * 0.9


def poly_mask(m):
    small = cv2.resize(m, (LW, LH), interpolation=cv2.INTER_AREA)
    b = (small > 0.5).astype(np.uint8)
    cs, _ = cv2.findContours(b, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    out = np.zeros((LH, LW), np.uint8)
    for c in cs:
        if cv2.contourArea(c) < 6:
            continue
        a = cv2.approxPolyDP(c, 2.2, True)
        cv2.fillPoly(out, [a], 1, lineType=cv2.LINE_8)
    return out.astype(np.float32)


def gouraud(pm, step, light):
    """Vertex lighting from a fake rounded height field (distance transform of the silhouette)."""
    d = cv2.distanceTransform((pm > 0).astype(np.uint8), cv2.DIST_L2, 3)
    hgt = np.sqrt(np.clip(d, 0, 12) / 12)
    hgt = cv2.GaussianBlur(hgt, (0, 0), 2)
    gy_, gx_ = np.gradient(hgt * 8)
    nz = 1.0
    norm = np.sqrt(gx_ ** 2 + gy_ ** 2 + nz)
    lam = (-gx_ * light[0] - gy_ * light[1] + nz * light[2]) / norm
    lam = 0.5 + 0.8 * np.clip(lam, 0, 1)
    gh, gw = LH // step + 2, LW // step + 2
    vy = np.clip(np.arange(gh) * step, 0, LH - 1)
    vx = np.clip(np.arange(gw) * step, 0, LW - 1)
    v = lam[np.ix_(vy, vx)]
    f, _ = mesh_field(step, v, v)
    return f


def render(n, rng_seed=7):
    img, m = load(n)
    g = grade(img)
    tex_bg = texture(g, 0.4)
    tex_fg = texture(g, 0.7)
    mx, my = warp_maps(18, n, rng_seed, 4.2, 1)
    bg = cv2.remap(tex_bg, mx, my, cv2.INTER_NEAREST, borderMode=cv2.BORDER_REFLECT)
    mx, my = warp_maps(12, n, rng_seed + 1, 2.1, 1)
    fg = cv2.remap(tex_fg, mx, my, cv2.INTER_NEAREST, borderMode=cv2.BORDER_REFLECT)

    pm = poly_mask(m)
    # vertex-lit people, lit from upper left
    fg = fg * gouraud(pm, 12, (-0.45, -0.55, 0.7))[..., None]
    # room: flat vertex lighting falling off to the floor and sides
    ys, xs = np.mgrid[0:LH, 0:LW].astype(np.float32)
    room_l = 1.0 - 0.25 * (ys / LH) - 0.18 * np.abs(xs / LW - 0.5)
    bg = bg * room_l[..., None]

    # distance fog: room far, people near (more fog when they are small in frame)
    area = pm.mean()
    fog_fg = float(np.clip(0.30 - area * 0.8, 0.04, 0.28))
    fog_bg = 0.38 + 0.22 * (1 - ys / LH) + 0.12 * np.abs(xs / LW - 0.5)   # thicker toward the back wall
    bg = bg * (1 - fog_bg[..., None]) + FOG * fog_bg[..., None]
    fg = fg * (1 - fog_fg) + FOG * fog_fg

    lo = bg * (1 - pm[..., None]) + fg * pm[..., None]

    # 15-bit colour with screen-space ordered dither (exaggerated: 4 bits / channel)
    levels = 18
    d = np.tile(BAYER, (LH // 4 + 1, LW // 4 + 1))[:LH, :LW][..., None]
    q = np.floor(np.clip(lo, 0, 1) * levels + 0.5 + d * 1.0) / levels
    q = np.clip(q, 0, 1)
    out = cv2.resize(q, (W, H), interpolation=cv2.INTER_NEAREST)
    return (out * 255).astype(np.uint8)


def job(n):
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), render(n))
    return n


def main():
    os.makedirs(OUT, exist_ok=True)
    total = len([f for f in os.listdir(FRAMES) if f.startswith("frame_") and f.endswith(".png")])
    nums = list(range(1, total + 1)) if (not ARGS or ARGS == ["all"]) else [int(a) for a in ARGS]
    pal = make_palette()
    with Pool(3, initializer=init, initargs=(pal,)) as p:
        for n in p.imap_unordered(job, nums):
            pass
    print("done", len(nums))


if __name__ == "__main__":
    main()
