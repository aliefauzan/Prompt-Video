"""Weirdcore / Dreamcore restyle, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [all | frame numbers...]

Per frame:
  * over-bright, over-saturated pastel grade with a soft bloom
  * the bright window and white wall become a pasted clip-art blue sky with
    fluffy clouds, a faint rainbow arcs across the room
  * clip-art daisies with human eyes in the middle "grow" in the plant row and
    a couple of loose eyes float on the wall; the pupils drift and blink
  * small plain-font captions ("WAKE UP", "do you remember this place?") that
    change every few seconds
  * everything is composited at low resolution and pushed through heavy JPEG
    compression, then upscaled: the crunchy "found on an old forum" quality
  * the people (from the masks) always sit in front of the pasted elements
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FRAMES, MASKS, OUT = sys.argv[1:4]
ARGS = sys.argv[4:]
N = len([f for f in os.listdir(FRAMES) if f.startswith("frame_") and f.endswith(".png")])
W, H = 1620, 1080
LW, LH = 648, 432          # working resolution (2.5x down) -> crunchy low-res look
S = LW / W
FONTS = "/System/Library/Fonts/Supplemental/"

# (first frame, last frame, text, font file, size, colour RGB, stroke RGB or None, x, y)
CAPTIONS = [
    (1, 36, "do you remember this place?", "Times New Roman.ttf", 22, (255, 255, 255), None, 0.50, 0.90),
    (37, 72, "WAKE UP", "Arial Bold.ttf", 30, (230, 20, 20), None, 0.50, 0.12),
    (73, 108, "you are not alone here", "Comic Sans MS.ttf", 20, (255, 255, 255), (0, 0, 0), 0.30, 0.88),
    (109, 144, "it's okay. you can stay.", "Times New Roman.ttf", 22, (230, 20, 20), None, 0.62, 0.10),
    (145, 179, "something isn't right", "Arial.ttf", 22, (255, 255, 255), (0, 0, 0), 0.50, 0.90),
]
# daisy eyes in the plant row and loose eyes on the wall: (x, y, radius) in low-res px, iris BGR
DAISIES = [(112, 236, 36, (150, 110, 40)), (268, 222, 28, (60, 120, 40)),
           (525, 232, 33, (170, 90, 30)), (402, 252, 22, (40, 80, 120))]
FLOATERS = [(62, 46, 24, (160, 120, 50)), (600, 52, 20, (60, 100, 40)), (330, 30, 15, (40, 70, 130))]


def mask(n):
    return cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255


def load(n):
    img = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png")).astype(np.float32) / 255
    m = mask(n)
    # the matte drops a motion-blurred hand on a few frames (23, 68): fill from the neighbours
    if 1 < n < N:
        a, b = mask(n - 1), mask(n + 1)
        if (m > 0.5).mean() < 0.8 * min((a > 0.5).mean(), (b > 0.5).mean()):
            m = np.maximum(m, np.maximum(a, b))
    return img, m


def noise(rng, h, w, cell):
    a = rng.random((h // cell + 2, w // cell + 2)).astype(np.float32)
    return cv2.resize(a, (w, h), interpolation=cv2.INTER_CUBIC)


def make_sky():
    """Clip-art sky: saturated blue gradient + fluffy white cumulus (low-res, BGR)."""
    rng = np.random.default_rng(7)
    t = np.linspace(0, 1, LH, dtype=np.float32)[:, None, None]
    top, bot = np.array([0.98, 0.55, 0.20]), np.array([1.0, 0.88, 0.62])
    sky = np.broadcast_to(top * (1 - t) + bot * t, (LH, LW + 400, 3)).astype(np.float32).copy()
    n = sum(noise(rng, LH, LW + 400, c) * a for c, a in ((90, 0.55), (40, 0.28), (16, 0.12), (6, 0.05)))
    cl = np.clip((n - 0.50) / 0.14, 0, 1)
    shade = np.clip(1 - (cv2.GaussianBlur(cl, (0, 0), 6) - cl) * 1.5, 0.75, 1)   # grey-blue undersides
    cloud = np.stack([shade, shade * 0.96, shade * 0.94], -1)
    return sky * (1 - cl[..., None]) + cloud * cl[..., None]


def rainbow_layer():
    wsum = np.zeros((LH, LW), np.float32)
    col = np.zeros((LH, LW, 3), np.float32)
    cols = [(0, 0, 255), (0, 140, 255), (0, 235, 255), (40, 220, 40), (255, 160, 0), (200, 40, 40), (200, 40, 150)]
    cx, cy, r0, bw = LW * 0.56, LH * 1.15, LH * 0.98, 7
    for i, c in enumerate(cols):
        ring = np.zeros((LH, LW), np.uint8)
        cv2.circle(ring, (int(cx), int(cy)), int(r0 - i * bw), 255, bw, cv2.LINE_AA)
        ring = cv2.GaussianBlur(ring.astype(np.float32) / 255, (0, 0), 1.2)
        col += ring[..., None] * (np.array(c, np.float32) / 255)
        wsum += ring
    a = np.clip(wsum, 0, 1) * 0.62
    return col / np.maximum(wsum, 1e-3)[..., None], a


def eye(r, iris, look, lid):
    """RGBA clip-art human eye, r = half width. look = (dx, dy) in -1..1, lid = 0 open .. 1 shut."""
    s = 4
    w, h = int(r * 2 * s), int(r * 1.3 * s)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    box = (2 * s, h * 0.12, w - 2 * s, h * 0.88)
    almond = Image.new("L", (w, h), 0)
    ImageDraw.Draw(almond).ellipse(box, fill=255)
    d.ellipse(box, fill=(250, 246, 240, 255))
    ir = h * 0.36
    cx, cy = w / 2 + look[0] * w * 0.14, h / 2 + look[1] * h * 0.08
    b, g, rr = iris
    for k in range(10, 0, -1):            # radial iris gradient
        f = k / 10
        d.ellipse((cx - ir * f, cy - ir * f, cx + ir * f, cy + ir * f),
                  fill=(int(rr * (0.5 + 0.6 * (1 - f))), int(g * (0.5 + 0.6 * (1 - f))), int(b * (0.5 + 0.6 * (1 - f))), 255))
    d.ellipse((cx - ir * 0.42, cy - ir * 0.42, cx + ir * 0.42, cy + ir * 0.42), fill=(8, 8, 8, 255))
    d.ellipse((cx - ir * 0.55, cy - ir * 0.62, cx - ir * 0.15, cy - ir * 0.22), fill=(255, 255, 255, 235))
    a = np.minimum(np.array(im)[..., 3], np.array(almond))
    if lid > 0:                            # eyelid closes from the top
        a[: int(h * (0.12 + 0.76 * lid)), :] = 0
    rgba = np.array(im)
    rgba[..., 3] = a
    im = Image.fromarray(rgba)
    d = ImageDraw.Draw(im)
    d.arc(box, 0, 180, fill=(60, 40, 40, 255), width=s)                 # lower lid
    if lid < 0.5:
        d.arc(box, 180, 360, fill=(30, 20, 20, 255), width=2 * s)       # upper lid line
        for k in range(7):                                               # lashes
            t = np.pi * (1.1 + 0.8 * k / 6)
            x0 = w / 2 + np.cos(t) * (w / 2 - 2 * s)
            y0 = h / 2 + np.sin(t) * (h * 0.38)
            d.line((x0, y0, x0 + np.cos(t) * 3 * s, y0 + np.sin(t) * 3 * s), fill=(20, 15, 15, 255), width=s)
    else:                                                                # shut: a dark lash line
        y = box[1] + (box[3] - box[1]) * min(lid, 0.85)
        d.line((box[0], y, box[2], y), fill=(30, 20, 20, 255), width=2 * s)
    im = im.resize((w // s, h // s), Image.LANCZOS)
    arr = np.array(im).astype(np.float32) / 255
    return arr[..., [2, 1, 0]], arr[..., 3]


def daisy(r):
    """RGBA white daisy (petals + yellow ring) of outer radius r*2.1."""
    s = 4
    R = int(r * 2.2 * s)
    im = Image.new("RGBA", (2 * R, 2 * R), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for k in range(16):
        t = k / 16 * 2 * np.pi
        pl = Image.new("RGBA", (2 * R, 2 * R), (0, 0, 0, 0))
        ImageDraw.Draw(pl).ellipse((R - r * 0.32 * s, R - R * 0.98, R + r * 0.32 * s, R), fill=(252, 252, 248, 255),
                                   outline=(150, 150, 170, 255), width=2 * s)
        im.alpha_composite(pl.rotate(np.degrees(t), resample=Image.BICUBIC))
    d = ImageDraw.Draw(im)
    d.ellipse((R - r * 1.15 * s, R - r * 1.15 * s, R + r * 1.15 * s, R + r * 1.15 * s), fill=(255, 205, 30, 255))
    im = im.resize((2 * R // s, 2 * R // s), Image.LANCZOS)
    arr = np.array(im).astype(np.float32) / 255
    return arr[..., [2, 1, 0]], arr[..., 3]


def paste(dst, alpha_bg, rgb, a, x, y):
    """Paste rgb/a centred at x,y onto dst, weighted by alpha_bg (1 = background visible)."""
    h, w = a.shape
    x0, y0 = int(x - w / 2), int(y - h / 2)
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(LW, x0 + w), min(LH, y0 + h)
    if xa >= xb or ya >= yb:
        return
    sa = a[ya - y0:yb - y0, xa - x0:xb - x0] * alpha_bg[ya:yb, xa:xb]
    dst[ya:yb, xa:xb] = dst[ya:yb, xa:xb] * (1 - sa[..., None]) + rgb[ya - y0:yb - y0, xa - x0:xb - x0] * sa[..., None]


def text(dst, n):
    for a, b, s, f, size, col, stroke, fx, fy in CAPTIONS:
        if a <= n <= b:
            pil = Image.fromarray((dst[..., ::-1] * 255).clip(0, 255).astype(np.uint8))
            d = ImageDraw.Draw(pil)
            font = ImageFont.truetype(FONTS + f, int(size * 1.3))
            kw = dict(stroke_width=2, stroke_fill=stroke) if stroke else {}
            tw = d.textlength(s, font=font)
            d.text((fx * LW - tw / 2, fy * LH - size / 2), s, font=font, fill=col, **kw)
            dst[:] = np.array(pil)[..., ::-1].astype(np.float32) / 255


SKY = None
RAIN = None
DAISY = {}


def render(n):
    global SKY, RAIN
    if SKY is None:
        SKY = make_sky()
        RAIN = rainbow_layer()
        for x, y, r, _ in DAISIES:
            DAISY[r] = daisy(r)
    rng = np.random.default_rng(1000 + n)
    img, m = load(n)
    small = cv2.resize(img, (LW, LH), interpolation=cv2.INTER_AREA)
    ms = cv2.resize(m, (LW, LH), interpolation=cv2.INTER_AREA)
    ms = cv2.GaussianBlur(ms, (0, 0), 0.8)
    bg = 1 - ms

    # over-bright, over-saturated pastel grade
    hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)
    hsv[..., 1] = np.clip(hsv[..., 1] * 1.4 + 0.03, 0, 1)
    hsv[..., 2] = np.clip(hsv[..., 2] * 1.18 + 0.07, 0, 1)
    out = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    out = out * 0.86 + np.array([0.15, 0.09, 0.11], np.float32)   # milky lavender-pink lift

    # bright window + white wall -> pasted clip-art sky (drifts slowly)
    v = small.max(2)
    sat = small.max(2) - small.min(2)
    skym = np.clip((v - 0.72) / 0.12, 0, 1) * np.clip((0.16 - sat) / 0.08, 0, 1)
    yy = np.linspace(1, 0, LH, dtype=np.float32)[:, None]
    skym *= np.clip(yy * 2.2 - 0.25, 0, 1)                 # only upper part of the room
    skym = cv2.morphologyEx(skym, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    skym = cv2.GaussianBlur(skym, (0, 0), 1.5) * bg
    sx = int(n * 0.6) % 400
    sky = SKY[:, sx:sx + LW]
    out = out * (1 - skym[..., None]) + sky * skym[..., None]

    # rainbow behind the people
    rc, ra = RAIN
    ra = ra * bg * (0.92 + 0.08 * np.sin(n * 0.7))
    out = out * (1 - ra[..., None]) + rc * ra[..., None]

    # daisies with eyes + loose floating eyes (behind people), slow pupil drift + blinks
    for i, (x, y, r, iris) in enumerate(DAISIES + FLOATERS):
        look = (np.sin(n * 0.045 + i * 1.7), 0.5 * np.cos(n * 0.06 + i))
        blink_at = (23 + i * 37) % 60
        ph = (n + i * 11) % 60
        lid = {blink_at: 0.6, (blink_at + 1) % 60: 1.0, (blink_at + 2) % 60: 0.5}.get(ph, 0.0)
        bob = np.sin(n * 0.12 + i) * (1.2 if i >= len(DAISIES) else 0.5)
        if i < len(DAISIES):
            drgb, da = DAISY[r]
            paste(out, bg, drgb, da, x, y + bob)
        ergb, ea = eye(r, iris, look, lid)
        paste(out, bg, ergb, ea, x, y + bob)

    text(out, n)

    # bloom + glow
    hot = np.clip(out - 0.70, 0, 1)
    out = out + cv2.GaussianBlur(hot, (0, 0), 9) * 0.9 + cv2.GaussianBlur(out, (0, 0), 4) * 0.10
    out = np.clip(out, 0, 1)

    # heavy JPEG at low res, then a second smaller re-save (re-uploaded meme)
    q = int(16 + rng.integers(0, 5))
    _, enc = cv2.imencode(".jpg", (out * 255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, q])
    low = cv2.imdecode(enc, cv2.IMREAD_COLOR)
    tiny = cv2.resize(low, (LW * 3 // 4, LH * 3 // 4), interpolation=cv2.INTER_AREA)
    _, enc = cv2.imencode(".jpg", tiny, [cv2.IMWRITE_JPEG_QUALITY, 30])
    low = cv2.resize(cv2.imdecode(enc, cv2.IMREAD_COLOR), (LW, LH), interpolation=cv2.INTER_LINEAR)
    big = cv2.resize(low, (W, H), interpolation=cv2.INTER_LINEAR).astype(np.float32) / 255

    # faint sensor grain + soft vignette
    big += rng.normal(0, 0.018, (H, W, 1)).astype(np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    vig = 1 - 0.18 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
    big = np.clip(big * vig[..., None], 0, 1)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), (big * 255).astype(np.uint8))
    return n


def main():
    os.makedirs(OUT, exist_ok=True)
    nums = list(range(1, N + 1)) if (not ARGS or ARGS == ["all"]) else [int(a) for a in ARGS]
    with Pool(min(5, os.cpu_count() or 4)) as p:
        for _ in p.imap_unordered(render, nums):
            pass
    print("rendered", len(nums), "->", OUT)


if __name__ == "__main__":
    main()
