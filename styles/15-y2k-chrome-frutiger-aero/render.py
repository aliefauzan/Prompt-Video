"""Y2K chrome / Frutiger Aero restyle, frame by frame.

usage: python -I render.py [frame numbers... | all]   (default: the six sheet frames)
       RENDER_OUT=/tmp/prompt-video-render/<slug> python -I render.py all   -> full clip for make_video.py
Reads ../../_source/frames + ../../_source/masks, writes ./frames/frame_NNN.png.
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "..", "_source")
FRAMES, MASKS, OUT = os.path.join(SRC, "frames"), os.path.join(SRC, "masks"), os.path.join(HERE, "frames")
OUT = os.environ.get("RENDER_OUT", OUT)        # e.g. /tmp/prompt-video-render/<slug> for the full clip
ONLY = (list(range(1, 180)) if sys.argv[1:] == ["all"] else [int(a) for a in sys.argv[1:]]) or [13, 49, 85, 109, 145, 178]
H, W = 1080, 1620

ROUND = ("/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf", 0)
UI = ("/System/Library/Fonts/Supplemental/Tahoma.ttf", 0) if os.path.exists(
    "/System/Library/Fonts/Supplemental/Tahoma.ttf") else ("/System/Library/Fonts/Helvetica.ttc", 0)

# first, last, background ('sky' or 'env'), chrome word, word position (x, y as fraction), window title
SECTIONS = [
    (1, 30, "sky", "AERO", (0.05, 0.62), "aero_dreams.exe"),
    (31, 66, "sky", "Y2K", (0.70, 0.60), "bubble_mail.exe"),
    (67, 100, "env", "2000s", (0.05, 0.66), "dreamscape.wmv"),
    (101, 136, "sky", "AQUA", (0.36, 0.06), "aero_dreams.exe"),
    (137, 160, "env", "AERO", (0.50, 0.66), "skyline.exe"),
    (161, 999, "sky", "Y2K", (0.05, 0.62), "bubble_mail.exe"),
]


def section_of(n):
    for i, s in enumerate(SECTIONS):
        if s[0] <= n <= s[1]:
            return i, s
    return len(SECTIONS) - 1, SECTIONS[-1]


def vnoise(rng, h, w, cell):
    a = rng.random((max(2, h // cell + 2), max(2, w // cell + 2))).astype(np.float32)
    return cv2.resize(a, (w, h), interpolation=cv2.INTER_CUBIC).clip(0, 1)


def fbm(seed, h, w, shift):
    rng = np.random.default_rng(seed)
    out = np.zeros((h, w), np.float32)
    amp, cell = 0.5, 360
    for _ in range(5):
        big = vnoise(rng, h, w + 400, cell)
        s = int(shift * cell / 360) % 400
        out += amp * big[:, s:s + w]
        amp *= 0.5
        cell = max(8, cell // 2)
    return out


def sky(n, si):
    """Vista-wallpaper sky: cobalt to aqua gradient, soft cumulus, green hill, sun glow. RGB 0..1."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    t = yy / H
    top, mid, hor = np.array([0.05, 0.30, 0.85]), np.array([0.25, 0.62, 0.98]), np.array([0.78, 0.93, 1.0])
    col = np.where(t[..., None] < 0.5, top + (mid - top) * (t[..., None] / 0.5),
                   mid + (hor - mid) * ((t[..., None] - 0.5) / 0.5).clip(0, 1))
    c = fbm(900 + si, H, W, n * 0.8)
    cloud = np.clip((c - 0.48) * 3.2, 0, 1) * np.clip(1.2 - t * 0.6, 0, 1)
    shade = np.clip((c - 0.55) * 2, 0, 1)
    ccol = np.array([1.0, 1.0, 1.0]) - shade[..., None] * np.array([0.18, 0.12, 0.02])
    col = col * (1 - cloud[..., None]) + ccol * cloud[..., None]
    # rolling grass hill
    hill_y = H * 0.80 + 70 * np.sin(xx[0] / W * 2.6 + 0.6) - 40 * np.cos(xx[0] / W * 6.1)
    d = yy - hill_y[None, :]
    hill = np.clip(d / 3, 0, 1)
    g = np.clip(d / 260, 0, 1)
    gcol = np.stack([0.30 - 0.22 * g, 0.80 - 0.35 * g, 0.18 - 0.10 * g], -1)
    gcol += (np.clip(1 - np.abs(d - 18) / 30, 0, 1) * 0.25)[..., None]     # glossy rim light on the hill
    col = col * (1 - hill[..., None]) + gcol * hill[..., None]
    # sun glow top-left
    sx, sy = W * 0.14, H * 0.10
    r = np.sqrt((xx - sx) ** 2 + (yy - sy) ** 2)
    col += (np.exp(-r / 260) * 0.55)[..., None] * np.array([1.0, 0.98, 0.9])
    return np.clip(col, 0, 1).astype(np.float32)


def aqua_grade(rgb):
    f = rgb.astype(np.float32) / 255
    f = np.clip((f - 0.02) / 0.9, 0, 1) ** 0.9
    lum = f.mean(2, keepdims=True)
    f = lum + (f - lum) * 1.25
    f = f * np.array([0.92, 1.0, 1.10]) + np.array([0.0, 0.02, 0.05])
    return np.clip(f, 0, 1).astype(np.float32)


def text_alpha(txt, fnt, h, w, xy, anchor="la"):
    im = Image.new("L", (w, h), 0)
    ImageDraw.Draw(im).text(xy, txt, font=fnt, fill=255, anchor=anchor)
    return np.asarray(im, np.float32) / 255


def chrome(alpha, bevel=26):
    """Liquid chrome shading for an alpha shape (RGB 0..1, alpha)."""
    a8 = (alpha > 0.5).astype(np.uint8)
    d = cv2.distanceTransform(a8, cv2.DIST_L2, 5)
    hgt = np.clip(d / bevel, 0, 1)
    hgt = np.sin(hgt * np.pi / 2)
    hgt = cv2.GaussianBlur(hgt, (0, 0), 2.5)
    gy = cv2.Sobel(hgt, cv2.CV_32F, 0, 1, ksize=5)
    gx = cv2.Sobel(hgt, cv2.CV_32F, 1, 0, ksize=5)
    ys = np.nonzero(a8.any(1))[0]
    y0, y1 = (ys.min(), ys.max()) if len(ys) else (0, 1)
    yrel = (np.arange(alpha.shape[0], dtype=np.float32)[:, None] - y0) / max(1, y1 - y0)
    u = np.clip(yrel + gy * 0.06 + gx * 0.02, 0, 1)                         # reflected horizon
    stops = np.array([0, 0.22, 0.42, 0.47, 0.60, 0.80, 1.0])
    cols = np.array([[0.98, 1.0, 1.0], [0.45, 0.70, 0.98], [0.95, 0.98, 1.0],
                     [0.05, 0.12, 0.38], [0.18, 0.40, 0.80], [0.70, 0.86, 1.0], [0.98, 1.0, 1.0]])
    rgb = np.stack([np.interp(u, stops, cols[:, i]) for i in range(3)], -1).astype(np.float32)
    spec = np.clip(-(gx + gy) * 0.25, 0, 1) ** 2
    rgb = np.clip(rgb + spec[..., None] * 0.9, 0, 1)
    rim = np.clip(1 - d / 3, 0, 1) * (alpha > 0.5)
    rgb = rgb * (1 - rim[..., None] * 0.8) + np.array([0.04, 0.12, 0.40]) * rim[..., None] * 0.8
    return rgb, cv2.GaussianBlur(alpha, (0, 0), 0.8)


def sparkle(img, x, y, s, a):
    """4-point twinkle star with soft glow."""
    yy, xx = np.ogrid[-int(s * 1.2):int(s * 1.2) + 1, -int(s * 1.2):int(s * 1.2) + 1]
    ax, ay = np.abs(xx).astype(np.float32), np.abs(yy).astype(np.float32)
    star = np.clip(1 - (np.sqrt(ax) * np.sqrt(ay) * 1.6 / np.sqrt(s) + (ax + ay) / (s * 1.1)), 0, 1)
    glow = np.exp(-(ax ** 2 + ay ** 2) / (s * s * 0.08)) * 0.6
    v = np.clip(star + glow, 0, 1) * a
    paste_add(img, v[..., None] * np.array([1.0, 1.0, 1.0], np.float32), x, y)


def paste_add(img, patch, x, y):
    h, w = patch.shape[:2]
    x0, y0 = int(x - w // 2), int(y - h // 2)
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
    if xa >= xb or ya >= yb:
        return
    img[ya:yb, xa:xb] = np.clip(img[ya:yb, xa:xb] + patch[ya - y0:yb - y0, xa - x0:xb - x0], 0, 1)


def bubble(img, cx, cy, R, phase):
    """Glossy soap/glass bubble: lens refraction, thin-film rim, specular highlights."""
    x0, y0, x1, y1 = int(cx - R - 3), int(cy - R - 3), int(cx + R + 4), int(cy + R + 4)
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x1), min(H, y1)
    if xa >= xb or ya >= yb:
        return
    yy, xx = np.mgrid[ya:yb, xa:xb].astype(np.float32)
    dx, dy = (xx - cx) / R, (yy - cy) / R
    r = np.sqrt(dx * dx + dy * dy)
    inside = r < 1
    # refraction: sample the image magnified + flipped toward the centre
    k = 0.55 + 0.45 * r ** 2
    sx = np.clip(cx - dx * R * k * 0.8, 0, W - 1).astype(np.float32)
    sy = np.clip(cy - dy * R * k * 0.8, 0, H - 1).astype(np.float32)
    ref = cv2.remap(img, sx, sy, cv2.INTER_LINEAR)
    ref = ref * 0.75 + np.array([0.75, 0.92, 1.0], np.float32) * 0.25
    ang = np.arctan2(dy, dx)
    film = np.stack([0.5 + 0.5 * np.sin(ang * 2 + phase), 0.5 + 0.5 * np.sin(ang * 2 + phase + 2.1),
                     0.5 + 0.5 * np.sin(ang * 2 + phase + 4.2)], -1)
    rim = np.clip((r - 0.80) / 0.2, 0, 1) ** 2 * inside
    col = ref * (1 - rim[..., None] * 0.7) + (0.55 * film + 0.45) * rim[..., None] * 0.7
    hl = np.exp(-(((dx + 0.38) / 0.30) ** 2 + ((dy + 0.42) / 0.18) ** 2))
    hl2 = np.exp(-(((dx - 0.45) / 0.14) ** 2 + ((dy - 0.48) / 0.10) ** 2)) * 0.6
    col = np.clip(col + (hl + hl2)[..., None] * 0.95, 0, 1)
    edge = np.clip(1 - np.abs(r - 1) * R / 1.6, 0, 1)
    col = col * (1 - edge[..., None] * 0.6) + edge[..., None] * 0.6
    a = np.clip((1 - r) * R / 1.5, 0, 1)
    a = np.maximum(a, edge)
    reg = img[ya:yb, xa:xb]
    img[ya:yb, xa:xb] = reg * (1 - a[..., None]) + col * a[..., None]


def glass_window(img, x, y, w, h, title, prog):
    """Frosted Aero glass window with a glossy title bar."""
    reg = img[y:y + h, x:x + w]
    blur = cv2.GaussianBlur(reg, (0, 0), 14)
    yy = np.linspace(0, 1, h, dtype=np.float32)[:, None, None]
    frost = blur * 0.55 + np.array([0.80, 0.92, 1.0], np.float32) * 0.45
    frost = frost + (0.18 * (1 - yy) * (yy < 0.5))                        # top gloss
    mask = np.zeros((h, w), np.float32)
    cv2.rectangle(mask, (8, 8), (w - 9, h - 9), 1.0, -1, cv2.LINE_AA)
    mask = cv2.GaussianBlur(cv2.dilate(mask, np.ones((15, 15), np.uint8)), (0, 0), 1.5)
    out = reg * (1 - mask[..., None]) + frost * mask[..., None]
    # title bar
    tb = 46
    bar = np.linspace(0, 1, tb, dtype=np.float32)[:, None, None]
    bcol = np.where(bar < 0.5, np.array([0.55, 0.80, 1.0]) * (1 - bar) + 0.3 * (1 - bar),
                    np.array([0.10, 0.42, 0.88]) + (bar - 0.5) * np.array([0.1, 0.2, 0.1]))
    out[4:4 + tb, 4:w - 4] = bcol * 0.9 + out[4:4 + tb, 4:w - 4] * 0.1
    cv2.rectangle(out, (4, 4), (w - 5, h - 5), (0.9, 0.97, 1.0), 2, cv2.LINE_AA)
    for i, c in enumerate([(0.85, 0.2, 0.15), (0.3, 0.6, 1.0), (0.3, 0.6, 1.0)]):
        bx = w - 38 - i * 40
        cv2.rectangle(out, (bx, 12), (bx + 30, 40), c, -1, cv2.LINE_AA)
        cv2.rectangle(out, (bx, 12), (bx + 30, 25), tuple(min(1, v + 0.3) for v in c), -1)
    # progress bar
    py = h - 46
    cv2.rectangle(out, (24, py), (w - 24, py + 22), (0.95, 0.98, 1.0), -1, cv2.LINE_AA)
    cv2.rectangle(out, (24, py), (w - 24, py + 22), (0.3, 0.5, 0.75), 1, cv2.LINE_AA)
    pw = int((w - 52) * prog)
    for bx in range(26, 26 + pw, 18):
        cv2.rectangle(out, (bx, py + 3), (min(bx + 14, 26 + pw), py + 19), (0.25, 0.85, 0.35), -1)
    img[y:y + h, x:x + w] = np.clip(out, 0, 1)
    f = ImageFont.truetype(UI[0], 26, index=UI[1])
    a = text_alpha(title, f, h, w, (18, 16))
    a2 = text_alpha("loading good vibes...", ImageFont.truetype(UI[0], 24, index=UI[1]), h, w, (24, py - 36))
    reg = img[y:y + h, x:x + w]
    reg = reg * (1 - a[..., None]) + a[..., None]
    reg = reg * (1 - a2[..., None]) + np.array([0.08, 0.2, 0.45]) * a2[..., None]
    img[y:y + h, x:x + w] = reg


def lens_flare(img, n):
    sx, sy = W * 0.14, H * 0.10
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    streak = np.exp(-((yy - sy) / 5) ** 2) * np.exp(-np.abs(xx - sx) / 520) * 0.7
    img += streak[..., None] * np.array([0.8, 0.9, 1.0], np.float32)
    vx, vy = W / 2 - sx, H / 2 - sy
    for t, R, c in [(0.6, 40, (0.4, 0.9, 0.7)), (1.1, 70, (0.5, 0.7, 1.0)), (1.5, 26, (1.0, 0.8, 0.5)),
                    (1.9, 110, (0.4, 0.6, 1.0))]:
        cx, cy = sx + vx * t, sy + vy * t
        r = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
        ring = np.clip(1 - r / R, 0, 1) ** 0.6 * 0.10 * (1 + 0.15 * np.sin(n * 0.7 + t))
        img += ring[..., None] * np.array(c, np.float32)


def render(n):
    si, (first, last, bgk, word, wpos, title) = section_of(n)
    rng = np.random.default_rng(15_000 + n)
    bgr = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png"))
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
    m = cv2.GaussianBlur(m, (0, 0), 1.0)
    person = aqua_grade(rgb)

    if bgk == "sky":
        img = sky(n, si)
        # soft white Aero outer glow around the people
        glow = np.clip(cv2.GaussianBlur(m, (0, 0), 16) * 1.6 - m, 0, 1)
        img = np.clip(img + glow[..., None] * np.array([0.6, 0.85, 1.0], np.float32) * 0.8, 0, 1)
    else:
        img = person * 0.7 + np.array([0.35, 0.75, 1.0], np.float32) * 0.3     # aqua wash on the room

    # head zone of the people (bubbles and type must never cover faces)
    cols = m > 0.5
    topy = np.where(cols.any(0), cols.argmax(0), H)
    heads = ((np.arange(H)[:, None] < topy[None, :] + 0.48 * H) & cols).astype(np.float32)
    heads = cv2.dilate(heads, np.ones((41, 41), np.uint8))

    # bubbles drifting upward (fixed per section, moving every frame); big ones behind the people
    br = np.random.default_rng(300 + si)
    k = n - first
    front = []
    for b in range(30):
        R = br.uniform(18, 80) if b > 3 else br.uniform(100, 170)
        bx = br.uniform(0, W) + 14 * np.sin(k * 0.25 + b)
        by = (br.uniform(0, H + 300) - k * br.uniform(4, 10)) % (H + 300) - 150
        if R < 70 and b % 2 == 0:
            front.append((bx, by, R, k * 0.3 + b))
        else:
            bubble(img, bx, by, R, k * 0.3 + b)

    # people on top, with a glossy sheen
    img = img * (1 - m[..., None]) + person * m[..., None]
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    sheen = np.clip(1 - (xx / W + yy / H), 0, 1) * 0.10
    img = np.clip(img + (sheen * m)[..., None], 0, 1)
    for bx, by, R, ph in front:                                              # a few small bubbles in front
        y0, y1, x0, x1 = int(max(0, by - R)), int(min(H, by + R)), int(max(0, bx - R)), int(min(W, bx + R))
        if y1 > y0 and x1 > x0 and heads[y0:y1, x0:x1].mean() < 0.02:
            bubble(img, bx, by, R, ph)

    # glass window
    # glass window: the corner that covers the least of the heads and the chrome word
    faces = ((np.arange(H)[:, None] < topy[None, :] + 0.25 * H) & cols).astype(np.float32)
    occ = cv2.dilate(faces, np.ones((41, 41), np.uint8)) * 6 + (m > 0.5) * 0.5
    occ[int(H * wpos[1]):int(H * wpos[1]) + 260, int(W * wpos[0]):int(W * wpos[0]) + 640] += 3
    best = min([(int(W * 0.03), int(H * 0.05)), (int(W * 0.66), int(H * 0.05)),
                (int(W * 0.03), int(H * 0.74)), (int(W * 0.66), int(H * 0.74))],
               key=lambda c: occ[c[1]:c[1] + 210, c[0]:c[0] + 500].mean())
    glass_window(img, best[0], best[1], 500, 210, title, ((k * 0.045) % 1.0))

    # chrome word
    f = ImageFont.truetype(ROUND[0], 250, index=ROUND[1])
    bob = 8 * np.sin(k * 0.35)
    a = text_alpha(word, f, H, W, (int(W * wpos[0]), int(H * wpos[1] + bob)))
    rgbc, ac = chrome(a)
    shadow = cv2.GaussianBlur(np.roll(ac, (14, 10), (0, 1)), (0, 0), 10) * 0.35
    img = img * (1 - shadow[..., None] * np.array([0.9, 0.6, 0.2]))
    outer = np.clip(cv2.GaussianBlur(ac, (0, 0), 10) * 2 - ac, 0, 1)
    img = np.clip(img + outer[..., None] * np.array([0.5, 0.8, 1.0]) * 0.35, 0, 1)
    img = img * (1 - ac[..., None]) + rgbc * ac[..., None]

    # sparkles twinkle every frame
    sr = np.random.default_rng(700 + si)
    for s in range(14):
        x, y, base = sr.uniform(0, W), sr.uniform(0, H * 0.85), sr.uniform(14, 46)
        tw = 0.5 + 0.5 * np.sin(n * sr.uniform(0.8, 1.6) + s)
        sparkle(img, x, y, base * (0.5 + 0.7 * tw), 0.35 + 0.65 * tw)
    # sparkles on the chrome letters
    ys, xs = np.nonzero(ac > 0.9)
    if len(xs):
        for _ in range(3):
            i = rng.integers(len(xs))
            sparkle(img, xs[i], ys[i], rng.uniform(20, 40), 0.9)

    if bgk == "sky":
        lens_flare(img, n)
    # bloom + soft digital-camera glow, slight chromatic aberration at the edges
    bright = np.clip(img - 0.75, 0, 1)
    img = img + cv2.GaussianBlur(bright, (0, 0), 18) * 0.8
    img = np.clip(img, 0, 1)
    out = (img * 255).astype(np.uint8)
    out[..., 0] = np.roll(out[..., 0], 1, 1)
    out[..., 2] = np.roll(out[..., 2], -1, 1)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), cv2.cvtColor(out, cv2.COLOR_RGB2BGR))
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    with Pool(6) as p:
        for n in p.imap_unordered(render, ONLY):
            print("frame", n)
