"""Soft scrapbook / journal sticker collage restyle, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [frame numbers...]

The people stay full-colour photographic, graded soft and pastel, and become
die-cut stickers: a clean, thick, rounded white border and a soft paper
shadow. They sit on a journal page (grid paper, gingham, kraft with torn
pastel paper, or the room itself as a taped photo print), decorated with
washi tape, puffy heart / star / daisy stickers, gel-pen doodles and
handwritten captions. Decorations nudge a pixel or two and the pen lines
wobble every frame, like stop-motion.
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FRAMES, MASKS, OUT = sys.argv[1:4]
ONLY = [int(a) for a in sys.argv[4:]]
N = len([f for f in os.listdir(FRAMES) if f.endswith(".png")])


def bgr(r, g, b):
    return np.array([b, g, r], np.float32) / 255


CREAM = bgr(252, 247, 236)
PINK = bgr(248, 196, 210)
BUTTER = bgr(253, 234, 160)
MINT = bgr(184, 228, 206)
LILAC = bgr(212, 196, 240)
SKY = bgr(186, 216, 245)
KRAFT = bgr(206, 172, 128)
WHITE = bgr(255, 254, 250)
PLUM = bgr(120, 72, 96)
GRIDBLUE = bgr(170, 200, 235)
PASTELS = [PINK, BUTTER, MINT, LILAC, SKY]

# (first, last, page, photo print?, caption)
SECTIONS = [
    (1, 30, "gingham", True, "best day ever"),
    (31, 66, "grid", False, "office besties"),
    (67, 100, "grid", True, "us :)"),
    (101, 136, "kraft", False, "little moments"),
    (137, 160, "gingham", False, "say cheese!"),
    (161, 999, "lilac", True, "core memory"),
]
FONT = "/System/Library/Fonts/Noteworthy.ttc"


def section_of(n):
    for i, s in enumerate(SECTIONS):
        if s[0] <= n <= s[1]:
            return i, s
    return len(SECTIONS) - 1, SECTIONS[-1]


def vnoise(rng, h, w, cell):
    a = rng.random((max(2, h // cell + 2), max(2, w // cell + 2))).astype(np.float32)
    return cv2.resize(a, (w, h), interpolation=cv2.INTER_CUBIC).clip(0, 1)


def grain(rng, h, w, sigma=0.7):
    return cv2.GaussianBlur(rng.normal(0, 1, (h, w)).astype(np.float32), (0, 0), sigma)


def over(dst, colour, alpha):
    a = alpha[..., None]
    return dst * (1 - a) + colour * a


def read_mask(n):
    return cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE)


# ---------------------------------------------------------------- pages
def page(kind, rng, h, w):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    if kind == "grid":
        img = np.broadcast_to(CREAM, (h, w, 3)).copy()
        g = ((np.mod(xx, 44) < 1.6) | (np.mod(yy, 44) < 1.6)).astype(np.float32)
        img = over(img, GRIDBLUE, cv2.GaussianBlur(g, (0, 0), 0.6) * 0.55)
        img = over(img, PINK * 0.9, ((xx > 120) & (xx < 123.5)).astype(np.float32) * 0.8)   # margin line
    elif kind == "gingham":
        a = (np.mod(xx, 56) < 28).astype(np.float32)
        b = (np.mod(yy, 56) < 28).astype(np.float32)
        img = np.broadcast_to(CREAM, (h, w, 3)).copy()
        img = over(img, PINK, (a + b) * 0.33)
    elif kind == "kraft":
        img = KRAFT[None, None, :] * (0.94 + 0.08 * vnoise(rng, h, w, 7)[..., None])
        for _ in range(500):                                   # kraft fibres
            x, y = rng.integers(0, w), rng.integers(0, h)
            a = rng.uniform(0, np.pi)
            L = rng.integers(5, 18)
            cv2.line(img, (x, y), (int(x + L * np.cos(a)), int(y + L * np.sin(a))),
                     tuple(float(c) for c in KRAFT * 0.82), 1, cv2.LINE_AA)
    else:
        img = np.broadcast_to(LILAC, (h, w, 3)).copy()
        img = over(img, WHITE, ((np.mod(xx + yy * 0.0, 60) < 4) | (np.mod(yy, 60) < 4)).astype(np.float32) * 0.0)
        dots = ((np.mod(xx, 48) - 24) ** 2 + (np.mod(yy, 48) - 24) ** 2 < 25).astype(np.float32)
        img = over(img, WHITE, dots * 0.6)
    tex = 0.985 + grain(rng, h, w, 1.2) * 0.012 - np.clip(vnoise(rng, h, w, 260) - 0.6, 0, 1) * 0.05
    return (img * tex[..., None]).astype(np.float32)


def torn_edge_poly(x0, y0, x1, y1, rng, amp=6, step=14):
    """Rectangle whose edges are torn (small random zig-zag)."""
    pts = []
    for (ax, ay), (bx, by) in [((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))]:
        L = int(np.hypot(bx - ax, by - ay) / step) + 1
        for k in range(L):
            t = k / L
            px, py = ax + (bx - ax) * t, ay + (by - ay) * t
            nx, ny = -(by - ay), (bx - ax)
            nn = np.hypot(nx, ny) + 1e-6
            j = rng.normal(0, amp)
            pts.append((px + nx / nn * j, py + ny / nn * j))
    return np.array(pts, np.float32)


# ---------------------------------------------------------------- shapes
def heart_pts(cx, cy, s, rot=0.0):
    t = np.linspace(0, 2 * np.pi, 90)
    x = 16 * np.sin(t) ** 3
    y = -(13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t))
    c, sn = np.cos(rot), np.sin(rot)
    return np.stack([cx + s / 32 * (x * c - y * sn), cy + s / 32 * (x * sn + y * c)], 1)


def star_pts(cx, cy, s, rot=0.0, k=5, inner=0.48):
    pts = []
    for i in range(2 * k):
        a = rot + i * np.pi / k - np.pi / 2
        r = s / 2 * (1 if i % 2 == 0 else inner)
        pts.append((cx + r * np.cos(a), cy + r * np.sin(a)))
    return np.array(pts)


def fill_alpha(h, w, polys):
    a = np.zeros((h, w), np.uint8)
    for p in polys:
        cv2.fillPoly(a, [np.round(p).astype(np.int32)], 255, cv2.LINE_AA)
    return a.astype(np.float32) / 255


def sticker(img, shape_a, colour_img, border, rng, shadow=0.22):
    """Die-cut sticker: white rounded border + soft shadow, then the art."""
    h, w = shape_a.shape
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * border + 1, 2 * border + 1))
    rim = cv2.dilate((shape_a > 0.5).astype(np.uint8), k).astype(np.float32)
    rim = cv2.GaussianBlur(rim, (0, 0), 2.0)
    rim = np.clip((rim - 0.5) * 3 + 0.5, 0, 1)                 # smooth rounded die-cut edge
    sh = cv2.GaussianBlur(np.roll(rim, (7, 5), (0, 1)), (0, 0), 7) * shadow
    img = over(img, np.zeros(3, np.float32), sh)
    img = over(img, WHITE * (0.985 + grain(rng, h, w, 1.0)[..., None] * 0.01), rim)
    if colour_img.ndim == 1:
        img = over(img, colour_img, shape_a)
    else:
        img = img * (1 - shape_a[..., None]) + colour_img * shape_a[..., None]
    return img


def washi(img, rng, cx, cy, length, width, ang, colour, pattern):
    h, w = img.shape[:2]
    tw, th = int(length), int(width)
    yy, xx = np.mgrid[0:th, 0:tw].astype(np.float32)
    tile = np.broadcast_to(colour, (th, tw, 3)).copy()
    if pattern == "stripes":
        tile = over(tile, WHITE, (np.mod(xx + yy, 24) < 9).astype(np.float32) * 0.85)
    elif pattern == "dots":
        tile = over(tile, WHITE, ((np.mod(xx, 20) - 10) ** 2 + (np.mod(yy, 20) - 10) ** 2 < 14).astype(np.float32))
    elif pattern == "gingham":
        tile = over(tile, WHITE, ((np.mod(xx, 16) < 8).astype(np.float32) + (np.mod(yy, 16) < 8)) * 0.3)
    a = np.ones((th, tw), np.float32)
    zig = (np.abs(np.mod(yy, 10) - 5) / 5) * 6                   # torn zig-zag ends
    a[(xx < zig + 2) | (xx > tw - 3 - zig)] = 0
    a *= 0.82                                                    # tape is translucent
    M = cv2.getRotationMatrix2D((tw / 2, th / 2), np.degrees(ang), 1.0)
    M[:, 2] += (cx - tw / 2, cy - th / 2)
    T = cv2.warpAffine(tile, M, (w, h))
    A = cv2.warpAffine(a, M, (w, h))
    return img * (1 - A[..., None]) + T * A[..., None]


def daisy_layer(h, w, cx, cy, s, rot):
    petals = []
    for i in range(10):
        a = rot + i * 2 * np.pi / 10
        t = np.linspace(0, 2 * np.pi, 30)
        px = s * 0.30 + s * 0.22 * np.cos(t)
        py = s * 0.10 * np.sin(t)
        petals.append(np.stack([cx + px * np.cos(a) - py * np.sin(a), cy + px * np.sin(a) + py * np.cos(a)], 1))
    centre = np.stack([cx + s * 0.13 * np.cos(np.linspace(0, 6.3, 30)), cy + s * 0.13 * np.sin(np.linspace(0, 6.3, 30))], 1)
    return fill_alpha(h, w, petals), fill_alpha(h, w, [centre])


def text_layer(h, w, text, x, y, size, ang, colour_rgb):
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    f = ImageFont.truetype(FONT, size, index=1) if FONT.endswith(".ttc") else ImageFont.truetype(FONT, size)
    tmp = Image.new("RGBA", (int(size * len(text) * 0.7) + 40, int(size * 1.6)), (0, 0, 0, 0))
    ImageDraw.Draw(tmp).text((20, 4), text, font=f, fill=colour_rgb + (255,))
    tmp = tmp.rotate(np.degrees(ang), expand=True, resample=Image.BICUBIC)
    lay.paste(tmp, (int(x), int(y)), tmp)
    a = np.array(lay)[..., 3].astype(np.float32) / 255
    return a


def doodles(rng, plan, h, w):
    """Gel-pen doodles as alpha; geometry fixed per section, wobble per frame."""
    lay = np.zeros((h, w), np.uint8)
    for d in plan["doodles"]:
        kind, x, y, s = d
        x, y = x + rng.normal(0, 1.2), y + rng.normal(0, 1.2)
        if kind == "heart":
            p = heart_pts(x, y, s, rng.normal(0, 0.03)) + rng.normal(0, 0.8, (90, 2))
            cv2.polylines(lay, [p.astype(np.int32)], True, 255, 4, cv2.LINE_AA)
        elif kind == "sparkle":
            p = star_pts(x, y, s, 0, k=4, inner=0.22)
            cv2.polylines(lay, [p.astype(np.int32)], True, 255, 4, cv2.LINE_AA)
        elif kind == "squiggle":
            t = np.linspace(0, 1, 80)
            px = x + t * s * 2.4
            py = y + 16 * np.sin(t * 14) + t * s * 0.4 + rng.normal(0, 0.6, 80)
            cv2.polylines(lay, [np.stack([px, py], 1).astype(np.int32)], False, 255, 4, cv2.LINE_AA)
        elif kind == "arrow":
            t = np.linspace(0, 1, 40)
            px = x + t * s * 1.8
            py = y - np.sin(t * np.pi) * s * 0.5 + t * s * 0.5
            cv2.polylines(lay, [np.stack([px, py], 1).astype(np.int32)], False, 255, 4, cv2.LINE_AA)
            ex, ey = px[-1], py[-1]
            cv2.line(lay, (int(ex), int(ey)), (int(ex - 26), int(ey - 10)), 255, 4, cv2.LINE_AA)
            cv2.line(lay, (int(ex), int(ey)), (int(ex - 12), int(ey - 26)), 255, 4, cv2.LINE_AA)
        elif kind == "dots":
            for k in range(7):
                cv2.circle(lay, (int(x + k * s * 0.3), int(y + 6 * np.sin(k))), 4, 255, -1, cv2.LINE_AA)
    return lay.astype(np.float32) / 255


def free_spots(mask, h, w, count, rng, size=150):
    """Positions where decorations don't cover the people."""
    m = cv2.dilate((mask > 128).astype(np.uint8), np.ones((61, 61), np.uint8))
    spots = []
    for _ in range(4000):
        x, y = rng.uniform(size * 0.6, w - size * 0.6), rng.uniform(size * 0.6, h - size * 0.6)
        if m[int(y), int(x)]:
            continue
        if all(np.hypot(x - a, y - b) > size * 1.3 for a, b in spots):
            spots.append((x, y))
        if len(spots) >= count:
            break
    while len(spots) < count:
        spots.append((rng.uniform(80, w - 80), rng.choice([70, h - 70])))
    return spots


def section_plan(si, sec, h, w):
    rng = np.random.default_rng(1200 + si * 13)
    first, last = sec[0], min(sec[1], N)
    # union of masks across the section so decorations never land on anyone
    union = np.zeros((h, w), np.uint8)
    for k in range(first, last + 1, 4):
        union = np.maximum(union, read_mask(k))
    spots = free_spots(union, h, w, 11, rng)
    plan = dict(rot=rng.uniform(-0.035, 0.035) if sec[3] else 0.0)
    kinds = ["heart", "star", "daisy", "heart", "sparkle_sticker"]
    plan["stickers"] = [(kinds[i % len(kinds)], *spots[i], rng.uniform(90, 145), rng.uniform(-0.4, 0.4),
                         PASTELS[int(rng.integers(len(PASTELS)))]) for i in range(4)]
    dk = ["heart", "sparkle", "squiggle", "arrow", "dots", "sparkle"]
    plan["doodles"] = [(dk[(i + si) % len(dk)], *spots[4 + i], rng.uniform(45, 75)) for i in range(6)]
    # caption goes in the emptiest 520x130 box across the whole section
    u = cv2.dilate((union > 128).astype(np.uint8), np.ones((41, 41), np.uint8)).astype(np.float32)
    # heads (top ~300 px of every silhouette column) cost far more than torsos
    yy_, _ = np.mgrid[0:h, 0:w]
    heads = np.zeros((h, w), np.float32)
    for k in range(first, last + 1, 4):
        mk = read_mask(k) > 128
        top = np.where(mk.any(0), mk.argmax(0), h)
        heads = np.maximum(heads, ((yy_ >= top - 40) & (yy_ < top + 320)).astype(np.float32))
    u = u + heads * 6
    best, cap = 1e9, (60, 60)
    for yy in range(50, h - 200, 30):
        for xx in range(50, w - 600, 30):
            cost = u[yy:yy + 130, xx:xx + 520].mean() + 0.0001 * abs(yy - 120)
            if cost < best:
                best, cap = cost, (xx, yy)
    plan["caption"] = (cap[0], cap[1], rng.uniform(-0.1, 0.1))
    plan["tapes"] = []
    if sec[3]:
        for (tx, ty) in [(0.07, 0.07), (0.93, 0.07), (0.93, 0.93), (0.07, 0.93)][: 2 + si % 3]:
            plan["tapes"].append((tx * w, ty * h, rng.uniform(230, 300), 62, rng.uniform(-0.9, -0.5) * np.sign((tx - 0.5) * (ty - 0.5)),
                                  PASTELS[int(rng.integers(len(PASTELS)))], ["stripes", "dots", "gingham"][int(rng.integers(3))]))
    else:
        for i in range(2):
            x, y = spots[i * 3 + 1]
            plan["tapes"].append((x, y, rng.uniform(200, 280), 58, rng.uniform(-0.7, 0.7),
                                  PASTELS[int(rng.integers(len(PASTELS)))], ["stripes", "dots", "gingham"][int(rng.integers(3))]))
    if sec[2] == "kraft":
        plan["torn"] = [(rng.uniform(-0.1, 0.5) * w, rng.uniform(-0.1, 0.5) * h, rng.uniform(0.45, 0.7) * w,
                         rng.uniform(0.4, 0.6) * h, PASTELS[int(rng.integers(len(PASTELS)))], int(rng.integers(1e6)))
                        for _ in range(3)]
    return plan


def pastel_grade(bgr_u8):
    """Soft, airy, slightly faded colour: lifted blacks, gentle desat, warm-pink highlights."""
    x = bgr_u8.astype(np.float32) / 255
    g = x.mean(2, keepdims=True)
    x = g + (x - g) * 0.82
    x = 0.10 + x * 0.88
    x = x ** 0.88
    x = x * np.array([0.98, 0.99, 1.03], np.float32)
    glow = cv2.GaussianBlur(x, (0, 0), 6)
    x = 1 - (1 - x) * (1 - glow * 0.18)                          # soft screen glow
    return x.clip(0, 1)


def render(n):
    si, sec = section_of(n)
    _, _, kind, photo, caption = sec
    rng = np.random.default_rng(60_000 + n)
    src = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png"))
    h, w = src.shape[:2]
    plan = section_plan(si, sec, h, w)
    mask_u8 = read_mask(n)
    graded = pastel_grade(src)

    img = page(kind, np.random.default_rng(80 + si), h, w)

    for tx, ty, tw_, th_, col, seed in plan.get("torn", []):
        r = np.random.default_rng(seed)
        p = torn_edge_poly(tx, ty, tx + tw_, ty + th_, r, amp=5)
        a = fill_alpha(h, w, [p])
        rim = fill_alpha(h, w, [p + r.normal(0, 3, p.shape)]) - a
        img = over(img, np.zeros(3, np.float32), cv2.GaussianBlur(np.roll(a, (5, 4), (0, 1)), (0, 0), 5) * 0.12)
        img = over(img, WHITE, np.clip(rim, 0, 1))                # torn white fibre edge
        img = over(img, col * (0.97 + vnoise(r, h, w, 9)[..., None] * 0.04), a)

    if photo:
        # the room becomes a white-bordered photo print taped onto the page
        rot = plan["rot"] + rng.normal(0, 0.002)
        s = 0.90
        M = cv2.getRotationMatrix2D((w / 2, h / 2), np.degrees(rot), s)
        M[:, 2] += rng.normal(0, 0.8, 2)
        ph = cv2.warpAffine(graded, M, (w, h))
        pa = cv2.warpAffine(np.ones((h, w), np.float32), M, (w, h))
        bw = 24
        border = cv2.warpAffine(np.pad(np.ones((h - 2 * int(bw / s), w - 2 * int(bw / s)), np.float32),
                                       int(bw / s)), M, (w, h))
        pa_outer = cv2.warpAffine(np.pad(np.ones((h, w), np.float32), 0), cv2.getRotationMatrix2D(
            (w / 2, h / 2), np.degrees(rot), s * 1.045), (w, h))
        img = over(img, np.zeros(3, np.float32), cv2.GaussianBlur(np.roll(pa_outer, (8, 6), (0, 1)), (0, 0), 9) * 0.25)
        img = over(img, WHITE, pa_outer)
        img = img * (1 - (pa * border)[..., None]) + ph * (pa * border)[..., None]

    for tx, ty, tl, tw_, ang, col, pat in plan["tapes"]:
        img = washi(img, rng, tx + rng.normal(0, 1), ty + rng.normal(0, 1), tl, tw_, ang + rng.normal(0, 0.006), col, pat)

    # pen doodles under the people
    img = over(img, PLUM, doodles(rng, plan, h, w) * 0.9)

    # decoration stickers
    for kind_s, x, y, s, rot, col in plan["stickers"]:
        x, y, rot = x + rng.normal(0, 1.2), y + rng.normal(0, 1.2), rot + rng.normal(0, 0.012)
        if kind_s == "heart":
            a = fill_alpha(h, w, [heart_pts(x, y, s, rot)])
            img = sticker(img, a, PINK * 0.93, 9, rng, 0.18)
            hi = fill_alpha(h, w, [heart_pts(x - s * 0.15, y - s * 0.12, s * 0.25, rot)])
            img = over(img, WHITE, hi * 0.55)                    # puffy highlight
        elif kind_s == "star":
            p = star_pts(x, y, s * 1.2, rot)
            a = cv2.GaussianBlur(fill_alpha(h, w, [p]), (0, 0), 2.5)
            a = np.clip((a - 0.5) * 3 + 0.5, 0, 1)
            img = sticker(img, a, BUTTER * 0.97, 9, rng, 0.18)
        elif kind_s == "daisy":
            pet, ctr = daisy_layer(h, w, x, y, s * 1.2, rot)
            img = sticker(img, np.maximum(pet, ctr), WHITE, 8, rng, 0.18)
            img = over(img, BUTTER * 0.92, ctr)
            img = over(img, PLUM, cv2.morphologyEx((pet > 0.5).astype(np.uint8), cv2.MORPH_GRADIENT,
                                                   np.ones((3, 3), np.uint8)).astype(np.float32) * 0.35)
        else:
            a = fill_alpha(h, w, [star_pts(x, y, s * 1.1, rot, k=4, inner=0.3)])
            img = sticker(img, a, col, 8, rng, 0.18)

    # the people: soft photographic die-cut sticker with a thick white border
    m = cv2.GaussianBlur((mask_u8 > 128).astype(np.float32), (0, 0), 2.5)
    m = cv2.morphologyEx((m > 0.5).astype(np.uint8), cv2.MORPH_CLOSE,
                         cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21)))
    n_, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    keep = np.zeros(n_, bool)
    keep[1:] = st[1:, cv2.CC_STAT_AREA] > 3000
    m = cv2.GaussianBlur(keep[lab].astype(np.float32), (0, 0), 1.2)
    border = 17 + int(rng.integers(-1, 2))
    img = sticker(img, m, graded, border, rng, 0.30)
    # subtle glossy sheen across the sticker
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    sheen = np.clip(1 - np.abs((xx + yy * 0.6) - w * 0.55) / 90, 0, 1) * 0.06
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * border + 1, 2 * border + 1))
    whole = cv2.dilate((m > 0.5).astype(np.uint8), k).astype(np.float32)
    img = over(img, WHITE, sheen * whole)

    # handwritten caption on a little torn label, kept clear of faces
    cx, cy, ang = plan["caption"]
    cx, cy = cx + rng.normal(0, 1), cy + rng.normal(0, 1)
    ta = text_layer(h, w, caption, cx, cy, 64, ang, (120, 72, 96))
    ys, xs = np.nonzero(ta > 0.1)
    if len(xs):
        r = np.random.default_rng(si)
        p = torn_edge_poly(xs.min() - 24, ys.min() - 16, xs.max() + 24, ys.max() + 16, r, amp=2.5, step=10)
        la = fill_alpha(h, w, [p])
        img = over(img, np.zeros(3, np.float32), cv2.GaussianBlur(np.roll(la, (5, 4), (0, 1)), (0, 0), 5) * 0.18)
        img = over(img, WHITE * 0.99, la)
        img = over(img, PLUM, ta)
        hx, hy = xs.max() + 34, ys.min() - 4                     # little puffy heart pinned to the label
        a = fill_alpha(h, w, [heart_pts(hx, hy, 52, 0.25 + rng.normal(0, 0.02))])
        img = sticker(img, a, PINK * 0.9, 6, rng, 0.15)

    # gentle paper grain over everything (scanned journal page)
    img = img * (0.99 + grain(rng, h, w, 0.9)[..., None] * 0.01)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), (img.clip(0, 1) * 255).astype(np.uint8))
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    todo = ONLY or list(range(1, N + 1))
    with Pool(min(8, os.cpu_count() or 4)) as pool:
        for n in pool.imap_unordered(render, todo):
            print(n, end=" ", flush=True)
    print()
