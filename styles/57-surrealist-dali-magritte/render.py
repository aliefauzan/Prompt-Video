"""Surrealist (Dali / Magritte) world restyle, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [all | frame numbers...]

The people are kept exactly (mask composite) and given a warm, smooth, oil-glazed
"hyper-real" finish. Everything behind them is replaced by one painted surreal
world, built once and held still like a painting:
  * an endless flat ochre desert under a Dali twilight sky (cream horizon ->
    deep blue zenith), golden cliffs on the horizon, Magritte cumulus clouds
  * a freestanding wall in the desert whose face is a piece of sky (Magritte)
  * melting pocket watches draped over a dead olive branch and a stone plinth (Dali)
  * floating green apples, a bowler hat and a floating rock with a castle (Magritte)
  * long hard low-sun shadows: from the people (their mattes, sheared and stretched
    across the ground) and from every floating object
Per frame only slow things change: objects bob, clouds drift, watch hands creep,
the people's shadows follow their poses; a faint canvas/varnish texture boils.
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np

FRAMES, MASKS, OUT = sys.argv[1:4]
ARGS = sys.argv[4:]
N = len([f for f in os.listdir(FRAMES) if f.startswith("frame_") and f.endswith(".png")])
W, H = 1620, 1080
HZ = int(H * 0.60)           # horizon
YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)
SHADOW = np.array([0.30, 0.25, 0.22], np.float32)   # bluish umber (BGR) multiplier for cast shadows
SKY_WIDE = []
SKY_MASK = []


def vnoise(rng, h, w, cell):
    a = rng.random((max(2, h // cell + 2), max(2, w // cell + 2))).astype(np.float32)
    return cv2.resize(a, (w, h), interpolation=cv2.INTER_CUBIC)


def sky_gradient(h, top, mid, low):
    y = np.linspace(0, 1, h, dtype=np.float32)[:, None, None]
    a = np.clip(y / 0.6, 0, 1)
    b = np.clip((y - 0.6) / 0.4, 0, 1)
    return top * (1 - a) + mid * a * (1 - b) + low * b


def clouds(rng, h, w, density, soft):
    n = vnoise(rng, h, w, 260) * 0.62 + vnoise(rng, h, w, 90) * 0.28 + vnoise(rng, h, w, 30) * 0.10
    c = np.clip((n - density) / soft, 0, 1)
    # puffy: lit tops, shaded bottoms
    shade = np.clip(c - np.roll(c, -18, axis=0), 0, 1)
    return c, shade


def build_world():
    rng = np.random.default_rng(1931)
    # sky (BGR)
    sky = sky_gradient(HZ + 40, np.array([0.55, 0.36, 0.16], np.float32),
                       np.array([0.80, 0.70, 0.55], np.float32), np.array([0.70, 0.88, 0.97], np.float32))
    c, shade = clouds(rng, HZ + 40, W + 160, 0.60, 0.16)
    c = cv2.GaussianBlur(c, (0, 0), 3)
    shade = cv2.GaussianBlur(shade, (0, 0), 6)
    c *= np.clip(1 - np.linspace(0, 1, HZ + 40)[:, None] * 1.1 + 0.25, 0, 1)   # fewer clouds near the horizon
    cloud_col = np.array([0.97, 0.97, 0.98], np.float32) - shade[..., None] * np.array([0.30, 0.25, 0.20], np.float32)
    sky = np.broadcast_to(sky, (HZ + 40, W + 160, 3))
    sky = sky * (1 - c[..., None] * 0.9) + cloud_col * c[..., None] * 0.9
    world = np.zeros((H, W, 3), np.float32)
    world[:HZ + 40] = sky[:, :W]
    SKY_WIDE.append(sky.astype(np.float32))
    # desert floor: lighter at the horizon, deep sienna near camera, faint sand ripples
    gy = np.clip((YY[HZ:] - HZ) / (H - HZ), 0, 1)[..., None]
    sand = np.array([0.50, 0.72, 0.88], np.float32) * (1 - gy) + np.array([0.18, 0.33, 0.52], np.float32) * gy
    rip = vnoise(rng, H - HZ, W, 9)
    rip = cv2.resize(rip[::3], (W, H - HZ))
    sand = sand * (0.94 + 0.08 * rip[..., None])
    world[HZ:] = sand
    # golden cliffs on the right horizon (Cap de Creus) and a far strip of sea on the left
    cliff = np.zeros((H, W), np.float32)
    pts = [(int(W * 0.70), HZ + 2)]
    x = W * 0.70
    while x < W + 20:
        x += rng.uniform(25, 60)
        pts.append((int(x), int(HZ - rng.uniform(25, 95) * np.clip((x - W * 0.70) / (W * 0.12), 0.2, 1))))
    pts += [(W + 20, HZ + 2)]
    cv2.fillPoly(cliff, [np.array(pts, np.int32)], 1.0, cv2.LINE_AA)
    cliff_col = np.array([0.28, 0.55, 0.80], np.float32) * (0.85 + 0.25 * vnoise(rng, H, W, 12)[..., None])
    world = world * (1 - cliff[..., None]) + cliff_col * cliff[..., None]
    sea = (np.abs(YY - (HZ - 4)) < 5) & (XX < W * 0.55)
    world[sea] = np.array([0.62, 0.55, 0.30], np.float32)
    world[HZ - 1:HZ + 1] = world[HZ - 1:HZ + 1] * 0.8 + np.array([0.85, 0.95, 1.0], np.float32) * 0.2
    skym = np.zeros((H, W), np.float32)
    skym[:HZ - 6] = 1
    skym *= 1 - cliff
    SKY_MASK.append(skym)
    return world


def draw_watch(size, angle_h, angle_m, rng):
    """Pocket watch face on transparent RGBA (float, BGR + alpha)."""
    s = size
    img = np.zeros((s, s, 4), np.float32)
    c = (s // 2, s // 2)
    r = int(s * 0.46)
    cv2.circle(img, c, r, (0.20, 0.55, 0.75, 1.0), -1, cv2.LINE_AA)            # gold case
    cv2.circle(img, c, int(r * 0.88), (0.80, 0.90, 0.95, 1.0), -1, cv2.LINE_AA)  # cream face
    for k in range(12):
        a = k / 12 * 2 * np.pi
        p1 = (int(c[0] + np.sin(a) * r * 0.80), int(c[1] - np.cos(a) * r * 0.80))
        p2 = (int(c[0] + np.sin(a) * r * 0.68), int(c[1] - np.cos(a) * r * 0.68))
        cv2.line(img, p1, p2, (0.10, 0.10, 0.12, 1.0), max(2, s // 90), cv2.LINE_AA)
    for a, l, t in ((angle_h, 0.42, s // 45), (angle_m, 0.66, s // 70)):
        p = (int(c[0] + np.sin(a) * r * l), int(c[1] - np.cos(a) * r * l))
        cv2.line(img, c, p, (0.08, 0.08, 0.10, 1.0), max(2, t), cv2.LINE_AA)
    cv2.circle(img, c, max(3, s // 60), (0.1, 0.3, 0.5, 1.0), -1, cv2.LINE_AA)
    # crown
    cv2.circle(img, (c[0], c[1] - r - s // 30), s // 28, (0.20, 0.55, 0.75, 1.0), -1, cv2.LINE_AA)
    # shading: darker toward the bottom right
    sh = 1 - 0.25 * (np.mgrid[0:s, 0:s][0] / s)
    img[..., :3] *= sh[..., None]
    return img


def melt(img, fold_x, droop, drip_x=None, drip_len=0.0):
    """Drape an RGBA sprite: right of fold_x it sags down (curved), plus an optional drip."""
    h, w = img.shape[:2]
    pad = int(h * (droop + drip_len + 0.2))
    canvas = np.zeros((h + pad, w, 4), np.float32)
    canvas[:h] = img
    yy, xx = np.mgrid[0:h + pad, 0:w].astype(np.float32)
    over = np.clip((xx - fold_x * w) / ((1 - fold_x) * w), 0, None)
    dy = droop * h * over ** 1.6
    sy = yy - dy
    # stretch vertically where it hangs (gravity)
    sy = sy - (sy - h * 0.2) * 0.25 * np.clip(over, 0, 1)
    if drip_x is not None:
        d = np.exp(-((xx - drip_x * w) / (w * 0.06)) ** 2)
        sy = np.where(yy > h * 0.7, yy - (yy - h * 0.7) * (1 - 1 / (1 + drip_len * 3 * d)) - dy, sy)
    sx = xx + 0.03 * w * np.sin(yy / h * 6) * np.clip(over, 0, 1)
    return cv2.remap(canvas, sx, sy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)


def paste(dst, spr, x, y, alpha_mul=1.0):
    h, w = spr.shape[:2]
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(W, x + w), min(H, y + h)
    if x1 <= x0 or y1 <= y0:
        return
    s = spr[y0 - y:y1 - y, x0 - x:x1 - x]
    a = s[..., 3:4] * alpha_mul
    dst[y0:y1, x0:x1] = dst[y0:y1, x0:x1] * (1 - a) + s[..., :3] * a


def sprite_from_mask(mask, color_fn):
    a = cv2.GaussianBlur(mask.astype(np.float32), (0, 0), 0.8)
    rgb = color_fn(a.shape)
    return np.dstack([rgb, a])


def apple(size):
    s = size
    m = np.zeros((s, s), np.float32)
    cv2.circle(m, (s // 2, s // 2 + s // 20), int(s * 0.40), 1.0, -1, cv2.LINE_AA)
    cv2.circle(m, (int(s * 0.38), int(s * 0.30)), int(s * 0.18), 1.0, -1, cv2.LINE_AA)
    cv2.circle(m, (int(s * 0.62), int(s * 0.30)), int(s * 0.18), 1.0, -1, cv2.LINE_AA)
    yy, xx = np.mgrid[0:s, 0:s].astype(np.float32) / s
    light = np.clip(1.15 - np.sqrt((xx - 0.35) ** 2 + (yy - 0.35) ** 2) * 1.6, 0.35, 1.1)
    rgb = np.dstack([0.12 * light, 0.62 * light, 0.38 * light])
    hl = np.exp(-(((xx - 0.36) ** 2 + (yy - 0.36) ** 2) / 0.003))
    rgb = rgb + hl[..., None] * 0.5
    spr = np.dstack([rgb, cv2.GaussianBlur(m, (0, 0), 0.8)])
    # stem and leaf
    cv2.line(spr, (s // 2, int(s * 0.22)), (int(s * 0.53), int(s * 0.05)), (0.10, 0.20, 0.30, 1.0), max(2, s // 25), cv2.LINE_AA)
    leaf = cv2.ellipse2Poly((int(s * 0.64), int(s * 0.10)), (int(s * 0.12), int(s * 0.05)), -25, 0, 360, 10)
    cv2.fillPoly(spr, [leaf], (0.15, 0.50, 0.20, 1.0), cv2.LINE_AA)
    return spr


def bowler(size):
    s = size
    spr = np.zeros((s, s, 4), np.float32)
    cv2.ellipse(spr, (s // 2, int(s * 0.62)), (int(s * 0.46), int(s * 0.10)), 0, 0, 360, (0.06, 0.06, 0.07, 1.0), -1, cv2.LINE_AA)
    cv2.ellipse(spr, (s // 2, int(s * 0.58)), (int(s * 0.28), int(s * 0.36)), 0, 180, 360, (0.08, 0.08, 0.09, 1.0), -1, cv2.LINE_AA)
    cv2.rectangle(spr, (int(s * 0.22), int(s * 0.50)), (int(s * 0.78), int(s * 0.58)), (0.12, 0.12, 0.14, 1.0), -1)
    cv2.ellipse(spr, (int(s * 0.42), int(s * 0.36)), (int(s * 0.07), int(s * 0.12)), -20, 0, 360, (0.35, 0.33, 0.33, 0.6), -1, cv2.LINE_AA)
    return spr


def rock_castle(size, rng):
    s = size
    spr = np.zeros((s, s, 4), np.float32)
    # inverted-cone floating rock
    pts = [(int(s * 0.05), int(s * 0.48)), (int(s * 0.25), int(s * 0.40)), (int(s * 0.55), int(s * 0.42)),
           (int(s * 0.92), int(s * 0.47)), (int(s * 0.75), int(s * 0.70)), (int(s * 0.55), int(s * 0.95)),
           (int(s * 0.35), int(s * 0.80)), (int(s * 0.15), int(s * 0.62))]
    cv2.fillPoly(spr, [np.array(pts, np.int32)], (0.40, 0.48, 0.55, 1.0), cv2.LINE_AA)
    yy, xx = np.mgrid[0:s, 0:s].astype(np.float32) / s
    tex = 0.75 + 0.35 * vnoise(rng, s, s, 6) - 0.35 * np.clip(xx - 0.4, 0, 1)
    spr[..., :3] *= tex[..., None]
    # castle on top
    for (x0, x1, top) in ((0.30, 0.42, 0.18), (0.42, 0.62, 0.26), (0.62, 0.72, 0.14)):
        cv2.rectangle(spr, (int(s * x0), int(s * top)), (int(s * x1), int(s * 0.43)), (0.55, 0.62, 0.68, 1.0), -1)
        for k in range(3):
            cx = int(s * (x0 + (x1 - x0) * (k + 0.5) / 3))
            cv2.rectangle(spr, (cx - s // 70, int(s * top) - s // 40), (cx + s // 70, int(s * top)), (0.55, 0.62, 0.68, 1.0), -1)
    cv2.rectangle(spr, (int(s * 0.50), int(s * 0.34)), (int(s * 0.54), int(s * 0.43)), (0.15, 0.15, 0.18, 1.0), -1)
    return spr


def branch(dst, shadow_list):
    """Dead olive branch reaching in from the left, from a stump on the ground."""
    col = (0.10, 0.17, 0.25)
    pts = [(int(W * 0.0), int(H * 0.52)), (int(W * 0.06), int(H * 0.47)), (int(W * 0.12), int(H * 0.44)),
           (int(W * 0.17), int(H * 0.43))]
    for i in range(len(pts) - 1):
        cv2.line(dst, pts[i], pts[i + 1], col, 18 - 4 * i, cv2.LINE_AA)
    cv2.line(dst, (int(W * 0.08), int(H * 0.46)), (int(W * 0.10), int(H * 0.38)), col, 7, cv2.LINE_AA)
    return pts[-1]


def place_static(world):
    """Objects that never move: sky-wall, plinth, branch with its watch. Returns world + ground-shadow casters."""
    rng = np.random.default_rng(1964)
    # Magritte sky-wall on the right, standing on the sand
    x0, x1, top, bot = int(W * 0.80), int(W * 0.985), int(H * 0.30), HZ + 30
    wall = world.copy()
    cv2.rectangle(wall, (x0 - 14, top - 10), (x1, bot), (0.42, 0.55, 0.62), -1)      # stone edge / thickness
    face = sky_gradient(bot - top, np.array([0.92, 0.66, 0.35], np.float32), np.array([0.95, 0.80, 0.60], np.float32),
                        np.array([0.95, 0.88, 0.80], np.float32))[:, 0]
    patch = np.broadcast_to(face[:, None, :], (bot - top, x1 - x0, 3)).copy()
    c, sh = clouds(rng, bot - top, x1 - x0, 0.52, 0.10)
    patch = patch * (1 - c[..., None] * 0.9) + (0.98 - sh[..., None] * 0.25) * c[..., None] * 0.9
    wall[top:bot, x0:x1] = patch
    world = wall
    # stone plinth (Dali's box) on the ground, left-centre, with a watch melting over its edge
    px0, px1, ptop, pbot = int(W * 0.03), int(W * 0.17), int(H * 0.80), int(H * 0.95)
    cv2.rectangle(world, (px0, ptop), (px1, pbot), (0.30, 0.42, 0.52), -1)
    cv2.rectangle(world, (px0, ptop - 18), (px1 + 22, ptop), (0.45, 0.60, 0.72), -1)
    cv2.rectangle(world, (px1, ptop), (px1 + 22, pbot), (0.22, 0.32, 0.42), -1)
    tip = branch(world, None)
    SKY_MASK[0][top - 12:bot, x0 - 16:x1 + 2] = 0
    return world, dict(wall=(x0 - 14, x1, bot), walltop=(x0, top), plinth=(px0, px1 + 22, pbot, ptop), tip=tip)


def cast_people_shadow(m):
    """Long hard low-sun shadow from the people. The sun is low behind the camera, to the
    left, so each body throws its shadow back across the sand toward the horizon and to
    the right: squash the matte toward its foot line (ground perspective) and shear it.
    Only on the ground below the horizon (the bodies themselves cover the rest)."""
    rows = np.where((m > 0.5).sum(1) > 10)[0]
    if len(rows) == 0:
        return np.zeros((H, W), np.float32)
    foot = float(max(rows[-1], H - 1))
    # x' = x + (foot - y) * shear ; y' = foot - (foot - y) * k
    k, shear = 0.42, 0.95
    M = np.float32([[1, -shear, shear * foot], [0, k, foot * (1 - k)]])
    sh = cv2.warpAffine(m, M, (W, H), flags=cv2.INTER_LINEAR, borderValue=0)
    sh = (sh > 0.4).astype(np.float32)
    sh = cv2.GaussianBlur(sh, (0, 0), 1.5)
    sh *= np.clip((YY - HZ) / 6, 0, 1)
    return sh


def finish_people(img):
    """Hyper-real oil-glazed look: smooth skin/cloth, warm low-sun light, crisp detail kept."""
    u8 = (np.clip(img, 0, 1) * 255).astype(np.uint8)
    sm = cv2.bilateralFilter(u8, 9, 40, 7).astype(np.float32) / 255
    detail = img - cv2.GaussianBlur(img, (0, 0), 1.2)
    out = sm + detail * 0.8
    # warm golden key from the left, cool fill from the right
    key = 1.08 - 0.22 * (XX / W)
    out = out * key[..., None]
    out = out * np.array([0.86, 0.98, 1.10], np.float32)
    g = out.mean(2, keepdims=True)
    out = g + (out - g) * 1.12
    out = 0.5 + (out - 0.5) * 1.08
    return np.clip(out, 0, 1)


def render(n, world, info):
    rng = np.random.default_rng(5700 + n)
    t = n / 12.0
    img = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png")).astype(np.float32) / 255
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
    cnt, lab, stats, _ = cv2.connectedComponentsWithStats((m > 0.3).astype(np.uint8))
    for i in range(1, cnt):
        blob = lab == i
        if stats[i, cv2.CC_STAT_AREA] < 4000 or m[blob].mean() < 0.80:
            m[blob] = 0
    m = np.clip((m - 0.45) / 0.4, 0, 1)
    m = cv2.erode(m, np.ones((3, 3), np.uint8))
    msoft = cv2.GaussianBlur(m, (0, 0), 1.4)[..., None]

    bg = world.copy()
    # clouds drift: shift the upper sky slowly
    off = int(160 - t * 6.0)
    sk = SKY_WIDE[0][:, off:off + W]
    smk = SKY_MASK[0][:HZ + 40, :, None]
    bg[:HZ + 40] = bg[:HZ + 40] * (1 - smk) + sk * smk

    shadows = np.zeros((H, W), np.float32)
    # watch melting over the branch tip
    tx, ty = info["tip"]
    w1 = melt(draw_watch(220, 1.2 + t * 0.02, 5.0 + t * 0.25, rng), 0.45, 0.85, drip_x=0.82, drip_len=0.5)
    paste(bg, w1, tx - 100, ty - 60)
    # watch melting over the plinth edge
    px0, px1, pbot, ptop = info["plinth"]
    w2 = melt(draw_watch(260, 3.9 + t * 0.02, 0.6 + t * 0.25, rng), 0.55, 1.1, drip_x=0.75, drip_len=0.7)
    paste(bg, w2, px1 - 170, ptop - 40)
    # a third watch lying flat on the sand, sagging into it
    w3 = melt(draw_watch(150, 2.2, 4.4 + t * 0.25, rng), 0.0, 0.25)
    w3 = cv2.resize(w3, (150, int(w3.shape[0] * 0.45)))
    paste(bg, w3, int(W * 0.60), int(H * 0.86))
    # plinth shadow (static), same low sun as the people's shadows
    poly = np.array([(px0, pbot), (px1, pbot), (px1 + 150, pbot - 70), (px0 + 150, pbot - 70)], np.int32)
    cv2.fillPoly(shadows, [poly], 1.0, cv2.LINE_AA)

    # floating objects (bob slowly) + their shadows on the sand
    floaters = [
        (rock_castle(260, np.random.default_rng(3)), 0.215, 0.02, 0.0, 260),
        (apple(100), 0.655, 0.06, 1.3, 100),
        (apple(70), 0.29, 0.40, 2.1, 70),
        (apple(85), 0.94, 0.05, 0.7, 85),
        (bowler(140), 0.50, 0.09, 2.8, 140),
    ]
    fsh = np.zeros((H, W), np.float32)
    for k, (spr, fx, fy, ph, s) in enumerate(floaters):
        x = int(fx * W)
        y = int(fy * H + 10 * np.sin(t * 0.9 + ph))
        paste(bg, spr, x, y)
        if k == 0:  # a watch slides off the floating rock's edge
            w4 = melt(draw_watch(150, 0.4, 2.0 + t * 0.25, rng), 0.5, 1.0, drip_x=0.8, drip_len=0.6)
            paste(bg, w4, x + int(s * 0.62), y + int(s * 0.36))
        sx = x + s // 2 + int(s * 1.2)
        sy = int(HZ + 14 + fy * 90)
        cv2.ellipse(fsh, (sx, sy), (int(s * 0.5), max(3, int(s * 0.05))), 0, 0, 360, 0.6, -1, cv2.LINE_AA)
    shadows = shadows + cv2.GaussianBlur(fsh, (0, 0), 3)
    # a big watch draped over the top edge of the sky-wall, dripping down its face
    wx, wy = info["walltop"]
    w5 = melt(draw_watch(230, 2.6, 0.2 + t * 0.25, rng), 0.42, 1.25, drip_x=0.78, drip_len=0.8)
    paste(bg, w5, wx - 60, wy - 95)

    shadows = np.clip(shadows + cast_people_shadow(m), 0, 1) * np.clip((YY - HZ) / 4, 0, 1)
    bg = bg * (1 - shadows[..., None] * (1 - SHADOW))

    ppl = finish_people(img)
    out = ppl * msoft + bg * (1 - msoft)

    # unify like one oil painting: soft glaze, canvas weave, varnish warmth, vignette
    yy, xx = YY, XX
    weave = (np.sin(xx * 1.9) * np.sin(yy * 1.9)) * 0.012
    tooth = cv2.GaussianBlur(rng.normal(0, 1, (H, W)).astype(np.float32), (0, 0), 0.9) * 0.012
    out = out + (weave + tooth)[..., None]
    out = out * np.array([0.95, 0.99, 1.03], np.float32)
    r = np.sqrt(((xx - W / 2) / (W * 0.65)) ** 2 + ((yy - H / 2) / (H * 0.7)) ** 2)
    out = out * (1 - 0.30 * np.clip(r - 0.55, 0, 1))[..., None]
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), (np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8))
    return n


_G = {}


def _init(world, info, sky_wide, sky_mask):
    _G.update(world=world, info=info)
    SKY_WIDE[:] = [sky_wide]
    SKY_MASK[:] = [sky_mask]


def _job(n):
    return render(n, _G["world"], _G["info"])


def main():
    os.makedirs(OUT, exist_ok=True)
    nums = list(range(1, N + 1)) if (not ARGS or ARGS == ["all"]) else [int(a) for a in ARGS]
    world, info = place_static(build_world())
    with Pool(min(6, os.cpu_count() or 4), initializer=_init, initargs=(world, info, SKY_WIDE[0], SKY_MASK[0])) as p:
        list(p.imap_unordered(_job, nums))
    print("rendered", len(nums), "->", OUT)


if __name__ == "__main__":
    main()
