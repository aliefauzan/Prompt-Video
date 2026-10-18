"""Cyberpunk Neon City restyle, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [all | frame numbers...]

Per frame:
  * the room goes to night: crushed blue-violet darkness, the bright window becomes
    a rain-blurred neon megacity (towers, lit window grids, vertical kanji signs)
  * the people stay photographic but are relit: low cold key, MAGENTA rim from the
    left, CYAN rim from the right, wet specular sheen in neon colours
  * holographic signage panels with kanji / katakana float in the room (fixed in
    space, flickering, scanlined), small HUD tags
  * rain streaks + lens droplets + haze, bloom, slight RGB split, grain
The city plate and sign layout are seeded once, so the world holds still while
rain, flicker, haze and grain change every frame.
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
CJK = "/System/Library/Fonts/Hiragino Sans GB.ttc"
MONO = "/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf"

# BGR 0..1
MAGENTA = np.array([0.95, 0.15, 1.0], np.float32)
CYAN = np.array([1.0, 0.92, 0.15], np.float32)
AMBER = np.array([0.15, 0.62, 1.0], np.float32)
VIOLET = np.array([0.55, 0.12, 0.30], np.float32)
SIGNS = ["夜市", "電脳", "東京", "未来", "ラーメン", "薬", "酒", "新宿", "危険", "ネオン", "無限", "情報"]


def font(path, size):
    return ImageFont.truetype(path, size)


def neon_text(draw, xy, text, size, vertical=False):
    f = font(CJK, size)
    x, y = xy
    if vertical:
        for ch in text:
            draw.text((x, y), ch, font=f, fill=255)
            y += int(size * 1.08)
    else:
        draw.text((x, y), text, font=f, fill=255)


def city_plate(seed):
    """Neon skyline seen through rain: returns (rgb plate, glow layer), BGR float."""
    rng = np.random.default_rng(seed)
    yy = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
    sky = (np.array([0.20, 0.04, 0.10], np.float32) * (1 - yy) + np.array([0.35, 0.10, 0.28], np.float32) * yy)
    plate = np.broadcast_to(sky, (H, W, 3)).copy()
    # three layers of towers, far (hazy) to near (dark)
    for layer, (shade, wmin, wmax, hmin, hmax) in enumerate(
            [(0.16, 50, 120, 0.25, 0.65), (0.09, 70, 160, 0.10, 0.45), (0.04, 90, 200, 0.0, 0.3)]):
        x = -40
        while x < W:
            w = int(rng.integers(wmin, wmax))
            top = int(H * rng.uniform(hmin, hmax))
            col = np.array([0.32, 0.10, 0.16], np.float32) * shade * 4
            plate[top:, max(0, x):x + w] = col
            # lit window grid
            win = rng.random() < 0.85
            if win:
                cx = int(rng.integers(6, 11))
                cy = int(rng.integers(9, 15))
                tint = [CYAN, AMBER, MAGENTA, np.array([0.9, 0.9, 0.95], np.float32)][rng.integers(0, 4)]
                for wy in range(top + 8, H, cy):
                    for wx in range(max(0, x) + 4, min(W, x + w) - 4, cx):
                        if rng.random() < 0.55 - 0.12 * layer:
                            plate[wy:wy + 4, wx:wx + 3] = tint * (0.6 + 0.4 * rng.random()) * (1 - 0.2 * layer)
            x += w + int(rng.integers(-10, 25))
    # vertical neon signs on the near towers
    glow = np.zeros((H, W, 3), np.float32)
    for i in range(14):
        img = Image.new("L", (W, H), 0)
        d = ImageDraw.Draw(img)
        size = int(rng.integers(40, 90))
        text = SIGNS[rng.integers(0, len(SIGNS))]
        x, y = int(rng.uniform(0.05, 0.85) * W), int(rng.uniform(0.08, 0.40) * H)
        vertical = rng.random() < 0.65
        d.rectangle((x - 8, y - 8, x + size + 8, y + size * (len(text) + 0.4) * 1.08 if vertical else y + size + 10),
                    outline=255, width=3) if rng.random() < 0.6 and vertical else None
        neon_text(d, (x, y), text, size, vertical)
        a = np.asarray(img, np.float32) / 255
        col = [MAGENTA, CYAN, AMBER, MAGENTA, CYAN][i % 5]
        glow += a[..., None] * col
    plate = plate * (1 - np.clip(glow.max(2, keepdims=True), 0, 1)) + glow * 0.95
    halo = cv2.GaussianBlur(glow, (0, 0), 6) * 0.7 + cv2.GaussianBlur(glow, (0, 0), 26) * 0.6
    plate = plate + halo
    # seen through wet glass: soften
    plate = cv2.GaussianBlur(plate, (0, 0), 1.0)
    return plate.clip(0, 1.5), glow


def holo_layer(seed):
    """Floating holographic panels + kanji overlays in room space. Returns list of (alpha, colour, flicker id)."""
    rng = np.random.default_rng(seed)
    panels = []
    specs = [  # x, y, w, h, text, colour
        (0.02, 0.07, 0.17, 0.22, "情報 // 07", CYAN),
        (0.80, 0.52, 0.18, 0.16, "危険区域", MAGENTA),
        (0.36, 0.02, 0.26, 0.09, "ネオン 新宿 2087", CYAN),
        (0.88, 0.08, 0.10, 0.34, "電脳", MAGENTA),
    ]
    for i, (x, y, w, h, text, col) in enumerate(specs):
        img = Image.new("L", (W, H), 0)
        d = ImageDraw.Draw(img)
        x0, y0, x1, y1 = int(x * W), int(y * H), int((x + w) * W), int((y + h) * H)
        d.rectangle((x0, y0, x1, y1), fill=38)
        d.rectangle((x0, y0, x1, y1), outline=200, width=2)
        for cx, cy in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):
            d.rectangle((cx - 6, cy - 6, cx + 6, cy + 6), outline=255, width=2)
        vertical = (y1 - y0) > 1.8 * (x1 - x0)
        size = int(min(x1 - x0, y1 - y0) * (0.55 if vertical else 0.36))
        if vertical:
            neon_text(d, (x0 + (x1 - x0 - size) // 2, y0 + 12), text, size, True)
        else:
            d.text((x0 + 14, y0 + 10), text, font=font(CJK, size), fill=255)
            mf = font(MONO, max(14, size // 2))
            d.text((x0 + 14, y0 + 16 + size), f"SEC-{rng.integers(100, 999)} ▸ {rng.integers(10, 99)}.{rng.integers(0, 9)}%",
                   font=mf, fill=170)
            yy = y0 + 22 + size + size // 2
            while yy < y1 - 10:
                ww = int((x1 - x0 - 28) * rng.uniform(0.3, 1.0))
                d.rectangle((x0 + 14, yy, x0 + 14 + ww, yy + 3), fill=120)
                yy += 10
        a = np.asarray(img, np.float32) / 255
        panels.append((a, col, i))
    return panels


def relight(img, m, rng, t):
    gray = img.mean(2, keepdims=True)
    base = np.power(img * 0.6 + gray * 0.4, 1.2) * 0.5
    xx = np.linspace(0, 1, W, dtype=np.float32)[None, :, None]
    key = MAGENTA * (1 - xx) * 0.75 + CYAN * xx * 0.7 + 0.12
    lit = base * key * 1.7
    # rims: light from the left (magenta) and right (cyan), and a top kicker
    mb = cv2.GaussianBlur(m, (0, 0), 1.5)
    rl = np.clip(mb - np.roll(mb, 7, axis=1), 0, 1)
    rr = np.clip(mb - np.roll(mb, -7, axis=1), 0, 1)
    rt = np.clip(mb - np.roll(mb, 6, axis=0), 0, 1)
    # light wrap: a broader, weaker falloff into the body behind the hard rim
    wl = np.clip(mb - np.roll(mb, 40, axis=1), 0, 1)
    wr = np.clip(mb - np.roll(mb, -40, axis=1), 0, 1)
    tex = np.power(gray[..., 0], 0.5) * 0.6 + 0.4
    rl = cv2.GaussianBlur(rl, (0, 0), 2.0) * tex + cv2.GaussianBlur(wl, (0, 0), 14) * tex * 0.35
    rr = cv2.GaussianBlur(rr, (0, 0), 2.0) * tex + cv2.GaussianBlur(wr, (0, 0), 14) * tex * 0.35
    rt = cv2.GaussianBlur(rt, (0, 0), 3) * tex
    pulse = 1 + 0.08 * np.sin(t * 2.3)
    lit = lit + rl[..., None] * MAGENTA * 1.0 * pulse + rr[..., None] * CYAN * 0.9 + rt[..., None] * (MAGENTA + CYAN) * 0.2
    # wet specular sheen: local highlights tinted by side
    hp = np.clip(gray[..., 0] - cv2.GaussianBlur(gray[..., 0], (0, 0), 6), 0, 1)
    sheen = np.clip((hp - 0.03) * 5, 0, 1) * m
    lit = lit + sheen[..., None] * (MAGENTA * (1 - xx) + CYAN * xx) * 0.5
    return lit


def rain(rng, n, strength=1.0):
    layer = np.zeros((H, W), np.float32)
    count = int(900 * strength)
    xs = rng.uniform(-100, W + 100, count)
    ys = rng.uniform(-100, H, count)
    ln = rng.uniform(25, 90, count)
    br = rng.uniform(0.15, 0.6, count)
    ang = 0.22  # slanted
    for x, y, l, b in zip(xs, ys, ln, br):
        cv2.line(layer, (int(x), int(y)), (int(x - l * ang), int(y + l)), float(b), 1, cv2.LINE_AA)
    near = np.zeros((H, W), np.float32)
    for _ in range(40):
        x, y = rng.uniform(0, W), rng.uniform(-100, H)
        l = rng.uniform(120, 260)
        cv2.line(near, (int(x), int(y)), (int(x - l * ang), int(y + l)), float(rng.uniform(0.2, 0.45)), 3, cv2.LINE_AA)
    near = cv2.GaussianBlur(near, (0, 0), 2.5)
    return cv2.GaussianBlur(layer, (0, 0), 0.6) + near


def render(n, plate, glow, panels, window, monitor):
    rng = np.random.default_rng(5500 + n)
    t = n / 12 * 2 * np.pi
    img = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png")).astype(np.float32) / 255
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
    msoft = cv2.GaussianBlur(m, (0, 0), 1.8)[..., None]

    # room at night: dark, cold, a little detail left
    g = img.mean(2, keepdims=True)
    room = np.power(img * 0.4 + g * 0.6, 1.6) * 0.30 * (VIOLET * 0.9 + np.array([0.35, 0.12, 0.08], np.float32))
    room = room * 1.6
    # the window becomes the neon city (with a slow parallax drift)
    dx = 6 * np.sin(t * 0.05)
    M = np.float32([[1, 0, dx], [0, 1, 0]])
    city = cv2.warpAffine(plate, M, (W, H), borderMode=cv2.BORDER_REFLECT)
    flick = 0.88 + 0.12 * np.sin(t * 3.1 + rng.normal(0, 0.3))
    if rng.random() < 0.08:
        flick *= 0.6  # a sign stutters
    city = 1.25 * city * (0.85 + 0.15 * flick) + cv2.warpAffine(glow, M, (W, H)) * 0.12 * (flick - 0.88)
    win = window[..., None]
    bg = room * (1 - win) + city * win
    # monitor -> glowing cyan display
    mon = monitor[..., None]
    bg = bg * (1 - mon) + (img * 0.5 + 0.2) * CYAN * 0.9 * mon
    # neon spill on walls near the window
    spill = cv2.GaussianBlur(win[..., 0], (0, 0), 60)
    bg = bg + spill[..., None] * (MAGENTA * 0.25 + CYAN * 0.12)

    ppl = relight(img, m, rng, t)
    out = ppl * msoft + bg * (1 - msoft)

    # holographic signage, behind the people where it overlaps them
    for a, col, i in panels:
        f = 0.75 + 0.25 * np.sin(t * (1.3 + 0.4 * i) + i)
        if rng.random() < 0.06:
            f *= 0.3
        jitter = int(rng.integers(-2, 3)) if rng.random() < 0.3 else 0
        aa = np.roll(a, jitter, axis=1)
        scan = (0.75 + 0.25 * (np.arange(H) % 4 < 2))[:, None].astype(np.float32)
        aa = aa * scan * f * (1 - msoft[..., 0])
        out = out + aa[..., None] * col * 0.9 + cv2.GaussianBlur(aa, (0, 0), 8)[..., None] * col * 0.6

    # haze: neon light scattered in humid air, thicker low in frame
    haze = cv2.GaussianBlur(cv2.resize(out, (W // 8, H // 8), interpolation=cv2.INTER_AREA), (0, 0), 8)
    haze = cv2.resize(haze, (W, H), interpolation=cv2.INTER_CUBIC)
    hv = (0.25 + 0.25 * np.linspace(0, 1, H, dtype=np.float32)[:, None, None])
    out = out + haze * hv * 0.9

    # rain: tinted by the light behind it
    r = rain(rng, n)
    tint = np.clip(cv2.GaussianBlur(bg, (0, 0), 40) * 2.5 + 0.25, 0, 1)
    out = out + r[..., None] * tint * 0.55

    # bloom
    hi = np.clip(out - 0.55, 0, 2)
    out = out + cv2.GaussianBlur(hi, (0, 0), 6) * 0.6 + cv2.GaussianBlur(hi, (0, 0), 22) * 0.5

    # lens: slight RGB split toward the edges, vignette, grain
    b, gch, rch = cv2.split(out)
    S = 1.004
    Mr = cv2.getRotationMatrix2D((W / 2, H / 2), 0, S)
    Mb = cv2.getRotationMatrix2D((W / 2, H / 2), 0, 1 / S)
    rch = cv2.warpAffine(rch, Mr, (W, H), borderMode=cv2.BORDER_REFLECT)
    b = cv2.warpAffine(b, Mb, (W, H), borderMode=cv2.BORDER_REFLECT)
    out = cv2.merge([b, gch, rch])
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    rr = np.sqrt(((xx - W / 2) / (W * 0.6)) ** 2 + ((yy - H / 2) / (H * 0.62)) ** 2)
    out = out * (1 - 0.5 * np.clip(rr - 0.5, 0, 1))[..., None]
    out = out + cv2.GaussianBlur(rng.normal(0, 1, (H, W)).astype(np.float32), (0, 0), 0.7)[..., None] * 0.03
    # soft tone-map so neon clips gracefully
    out = out / (1 + 0.25 * out)
    out = np.clip(out * 1.18, 0, 1)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), (out * 255 + 0.5).astype(np.uint8))
    return n


def static_regions():
    """Window (bright, low-saturation area behind the people) and the TV monitor, from a frame
    where nobody blocks them much, then fixed for the whole clip (static camera)."""
    acc = np.zeros((H, W), np.float32)
    cnt = np.zeros((H, W), np.float32)
    for n in range(1, N + 1, 6):
        img = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png")).astype(np.float32) / 255
        m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
        L = img.mean(2)
        sat = img.max(2) - img.min(2)
        bright = ((L > 0.80) & (sat < 0.10)).astype(np.float32)
        free = (m < 0.1).astype(np.float32)
        acc += bright * free
        cnt += free
    win = np.where(cnt > 0, acc / np.maximum(cnt, 1), 0)
    win = (win > 0.5).astype(np.uint8)
    win = cv2.morphologyEx(win, cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8))
    win = cv2.morphologyEx(win, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
    win[int(H * 0.62):] = 0  # window band only; the floor and desk tops stay room
    win = cv2.GaussianBlur(win.astype(np.float32), (0, 0), 3)
    mon = np.zeros((H, W), np.float32)
    cv2.rectangle(mon, (int(W * 0.82), int(H * 0.08)), (W, int(H * 0.47)), 1.0, -1)
    mon = cv2.GaussianBlur(mon, (0, 0), 4) * (1 - win)
    return win, mon


_G = {}


def _init(plate, glow, panels, win, mon):
    _G.update(plate=plate, glow=glow, panels=panels, win=win, mon=mon)


def _job(n):
    return render(n, _G["plate"], _G["glow"], _G["panels"], _G["win"], _G["mon"])


def main():
    os.makedirs(OUT, exist_ok=True)
    nums = list(range(1, N + 1)) if (not ARGS or ARGS == ["all"]) else [int(a) for a in ARGS]
    plate, glow = city_plate(2087)
    panels = holo_layer(77)
    win, mon = static_regions()
    with Pool(min(6, os.cpu_count() or 4), initializer=_init, initargs=(plate, glow, panels, win, mon)) as p:
        list(p.imap_unordered(_job, nums))
    print("rendered", len(nums), "->", OUT)


if __name__ == "__main__":
    main()
