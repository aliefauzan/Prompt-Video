"""Holographic trading-card restyle, frame by frame.

usage: python -I render.py [frame numbers... | all]   (default: the six sheet frames)
       RENDER_OUT=/tmp/prompt-video-render/41-holographic-trading-card python -I render.py all   -> full clip for make_video.py
Reads ../../_source/frames + ../../_source/masks, writes ./frames/frame_NNN.png.

Each frame becomes the art window of a landscape holo-rare collectible card: the whole frame is
scaled into the window (composition kept), printed with a little extra punch; the room behind the
people carries a rainbow holo-foil (diffraction stripes + glitter) that only lights up where the
moving glare sweeps across, the people get a faint version of it; foil border, name bar, stats
panel, move list, set number. The card tilts very slightly in the hand, glitter twinkles per frame.
Foil sheen idea after simeydotme/pokemon-cards-css (colour-dodge rainbow + glare follow).
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "..", "_source")
FRAMES, MASKS = os.path.join(SRC, "frames"), os.path.join(SRC, "masks")
OUT = os.environ.get("RENDER_OUT", os.path.join(HERE, "frames"))
ONLY = (list(range(1, 180)) if sys.argv[1:] == ["all"] else [int(a) for a in sys.argv[1:]]) or [13, 49, 85, 109, 145, 178]
W, H = 1620, 1080
CARD = (26, 26, 1594, 1054)
ART = (50, 150, 1250, 950)                 # 1200x800, same 3:2 as the clip
PANEL = (1268, 150, 1570, 950)
SUP = "/System/Library/Fonts/Supplemental/"


def font(name, size, index=0):
    try:
        return ImageFont.truetype(SUP + name if not name.startswith("/") else name, size, index=index)
    except OSError:
        return ImageFont.load_default()


YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)


def holo(t, strength_lines=1.0):
    """Rainbow diffraction foil field (BGR 0..1) + glare mask for time t (seconds)."""
    ang = 0.62 + 0.10 * np.sin(t * 0.7)
    proj = XX * np.cos(ang) + YY * np.sin(ang)
    hue = np.mod(proj / 520.0 + t * 0.22, 1.0)
    lines = 0.5 + 0.5 * np.sin(proj * 0.21 + t * 3.0)                  # fine diffraction stripes
    hsv = np.stack([hue * 180, np.full_like(hue, 215), 175 + 80 * lines * strength_lines], -1)
    rainbow = cv2.cvtColor(np.clip(hsv, 0, 255).astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32) / 255
    # glare: a soft band sweeping across the card, crossing it about every 3.5 s
    perp = XX * np.cos(ang + 1.25) + YY * np.sin(ang + 1.25)
    pos = np.mod(t / 3.5, 1.0) * 2600 - 700
    glare = np.exp(-((perp - pos) / 260.0) ** 2)
    return rainbow, glare


_g = np.random.default_rng(41)
GLIT = np.stack([_g.uniform(0, W, 2600), _g.uniform(0, H, 2600), _g.uniform(1, 3.2, 2600), _g.uniform(0, 6.28, 2600)], 1)


def glitter(t, glare, rng):
    """Cosmos-style foil glitter: fixed flecks that flash when the glare passes, twinkling per frame."""
    layer = np.zeros((H, W), np.float32)
    for x, y, r, ph in GLIT:
        g = glare[int(y), int(x)]
        v = (0.25 + 0.75 * g) * (0.5 + 0.5 * np.sin(ph + t * 9.0)) * rng.uniform(0.4, 1.0)
        if v > 0.25:
            cv2.circle(layer, (int(x), int(y)), int(round(r)), float(v), -1, cv2.LINE_AA)
        if v > 0.78 and g > 0.35:
            L = int(r * 7)
            cv2.line(layer, (int(x) - L, int(y)), (int(x) + L, int(y)), float(v), 1, cv2.LINE_AA)
            cv2.line(layer, (int(x), int(y) - L), (int(x), int(y) + L), float(v), 1, cv2.LINE_AA)
    star = cv2.GaussianBlur(layer, (0, 0), 1.2)
    return layer + 0.6 * star


def screen(a, b):
    return 1 - (1 - a) * (1 - b)


def art(bgr, m, rainbow, glare, glit):
    x0, y0, x1, y1 = ART
    aw, ah = x1 - x0, y1 - y0
    f = cv2.resize(bgr, (aw, ah), interpolation=cv2.INTER_AREA).astype(np.float32) / 255
    mm = cv2.resize(m, (aw, ah), interpolation=cv2.INTER_AREA)[..., None]
    # printed card art: a bit more contrast and saturation, slightly warm
    g = f.mean(2, keepdims=True)
    f = np.clip(g + (f - g) * 1.25, 0, 1)
    f = np.clip((f - 0.5) * 1.12 + 0.52, 0, 1)
    rb = rainbow[y0:y1, x0:x1]
    gl = glare[y0:y1, x0:x1, None]
    gt = glit[y0:y1, x0:x1, None]
    # foil: printed ink tinted by the rainbow (multiply, so white walls turn to colour bands),
    # strong on the room, faint on the people; brightest where the glare passes
    amt = (1 - mm) * (0.42 + 0.50 * gl) + mm * (0.05 + 0.13 * gl)
    tint = np.clip(f * (0.45 + 0.85 * rb), 0, 1)
    out = f * (1 - amt) + tint * amt
    out = out + (1 - mm) * gl * 0.30 * rb + gl * 0.10
    out = out + gt * (1 - 0.85 * mm)
    return np.clip(out, 0, 1)


def card(n, bgr, m, rng):
    t = (n - 1) / 12
    rainbow, glare = holo(t)
    glit = glitter(t, glare, rng)
    canvas = np.zeros((H, W, 3), np.float32)
    # card body: deep indigo with a soft foil wash, foil border
    body = np.array([0.30, 0.10, 0.12], np.float32)
    canvas[:] = body
    canvas = canvas * (1 - 0.35 * glare[..., None]) + screen(canvas, rainbow * 0.7) * 0.35 * (0.4 + glare[..., None])
    border = np.zeros((H, W), np.uint8)
    cv2.rectangle(border, CARD[:2], CARD[2:], 1, -1)
    cv2.rectangle(border, (CARD[0] + 18, CARD[1] + 18), (CARD[2] - 18, CARD[3] - 18), 0, -1)
    bmask = border.astype(bool)
    canvas[bmask] = (screen(np.full(3, 0.55, np.float32), rainbow) * (0.75 + 0.5 * glare[..., None]))[bmask]
    x0, y0, x1, y1 = ART
    canvas[y0:y1, x0:x1] = art(bgr, m, rainbow, glare, glit)
    keep = np.ones((H, W), np.float32)
    keep[y0:y1, x0:x1] = 0                                       # art window already has its glitter
    canvas = np.clip(canvas + (glit * keep)[..., None] * 0.35, 0, 1)
    return canvas, glare


def typeset(img, n):
    pil = Image.fromarray((np.clip(img, 0, 1)[..., ::-1] * 255).astype(np.uint8)).convert("RGBA")
    ov = Image.new("RGBA", pil.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    gold, white, ink = (246, 214, 120, 255), (250, 248, 240, 255), (20, 14, 40, 235)
    # name bar
    d.rounded_rectangle((50, 48, 1570, 138), 18, fill=ink, outline=gold, width=3)
    d.text((76, 56), "OFFICE TRIO", font=font("DIN Condensed Bold.ttf", 76), fill=white)
    d.text((470, 78), "STAGE 2  /  TEAM CARD", font=font("DIN Alternate Bold.ttf", 30), fill=gold)
    d.text((1265, 60), "HP", font=font("DIN Condensed Bold.ttf", 40), fill=gold)
    d.text((1312, 52), "270", font=font("Arial Black.ttf", 60), fill=white)
    d.ellipse((1490, 58, 1560, 128), fill=(255, 196, 60, 255), outline=white, width=4)
    d.regular_polygon((1525, 93, 22), 5, rotation=-90, fill=white)
    # art window frame
    d.rectangle((ART[0] - 6, ART[1] - 6, ART[2] + 6, ART[3] + 6), outline=gold, width=6)
    d.rectangle((ART[0] - 1, ART[1] - 1, ART[2] + 1, ART[3] + 1), outline=(40, 30, 60, 255), width=2)
    # stats panel
    px0, py0, px1, py1 = PANEL
    d.rounded_rectangle(PANEL, 16, fill=ink, outline=gold, width=3)
    fs, fn = font("DIN Condensed Bold.ttf", 40), font("Arial Black.ttf", 34)
    y = py0 + 22
    for lab, val in (("ATK", 88), ("DEF", 74), ("SPD", 91), ("VIBE", 99)):
        d.text((px0 + 20, y), lab, font=fs, fill=gold)
        d.text((px1 - 84, y - 2), str(val), font=fn, fill=white)
        d.rounded_rectangle((px0 + 20, y + 48, px1 - 20, y + 60), 6, fill=(70, 60, 110, 255))
        d.rounded_rectangle((px0 + 20, y + 48, px0 + 20 + int((px1 - px0 - 40) * val / 100), y + 60), 6, fill=gold)
        y += 92
    d.line((px0 + 20, y + 4, px1 - 20, y + 4), fill=gold, width=2)
    y += 22
    fm, fd = font("DIN Condensed Bold.ttf", 36), font("DIN Alternate Bold.ttf", 22)
    for mv, dmg, desc in (("SIDE-EYE", "60", "Opponent's next"), ("", "", "attack does -20."),
                          ("GROUP SMILE", "120", "Flip 3 coins. +30"), ("", "", "for each heads.")):
        if mv:
            d.text((px0 + 20, y), mv, font=fm, fill=white)
            d.text((px1 - 70, y), dmg, font=fm, fill=gold)
            y += 44
        else:
            d.text((px0 + 20, y - 4), desc, font=fd, fill=(205, 200, 225, 255))
            y += 28
        if mv:
            continue
        y += 10
    # bottom strip
    d.rounded_rectangle((50, 962, 1570, 1032), 16, fill=ink, outline=gold, width=3)
    d.text((76, 978), "Three coworkers caught mid-take. Rarely seen without a smile.", font=font("Futura.ttc", 30, 0), fill=(225, 220, 240, 255))
    d.text((1238, 974), "041/179", font=font("DIN Condensed Bold.ttf", 46), fill=white)
    d.regular_polygon((1400, 997, 15), 5, rotation=-90, fill=gold)
    d.text((1424, 978), "HOLO RARE", font=font("DIN Condensed Bold.ttf", 38), fill=gold)
    return Image.alpha_composite(pil, ov).convert("RGB")


def tilt(card_rgb, alpha, n):
    """Very slight hand tilt of the card (perspective), over a dark desk."""
    t = (n - 1) / 12
    a, b = 9 * np.sin(t * 1.1), 7 * np.sin(t * 0.8 + 1.3)
    src = np.float32([[0, 0], [W, 0], [W, H], [0, H]])
    dst = np.float32([[0 + a, 0 + b], [W - a, 0 - b], [W + a * 0.6, H + b], [0 - a * 0.6, H - b]])
    M = cv2.getPerspectiveTransform(src, dst)
    c = cv2.warpPerspective(card_rgb, M, (W, H), flags=cv2.INTER_LINEAR)
    al = cv2.warpPerspective(alpha, M, (W, H), flags=cv2.INTER_LINEAR)[..., None]
    sh = cv2.GaussianBlur(np.roll(al, (14, 10), (0, 1)), (0, 0), 14)
    desk = np.zeros((H, W, 3), np.float32) + np.float32([0.07, 0.06, 0.06])
    desk *= (1.25 - 0.5 * np.sqrt(((XX - W / 2) / W) ** 2 + ((YY - H / 2) / H) ** 2))[..., None]
    desk *= 1 - 0.7 * sh[..., None]
    return c * al + desk * (1 - al)


def render(n):
    rng = np.random.default_rng(4100 + n)
    bgr = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png"))
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
    img, glare = card(n, bgr, m, rng)
    pil = typeset(img, n)
    c = np.asarray(pil)[..., ::-1].astype(np.float32) / 255
    # glare also skims across the printed panels
    c = np.clip(c + glare[..., None] * 0.10, 0, 1)
    alpha = np.zeros((H, W), np.float32)
    cv2.rectangle(alpha, CARD[:2], CARD[2:], 1.0, -1)
    r = 40
    for cx, cy in ((CARD[0] + r, CARD[1] + r), (CARD[2] - r, CARD[1] + r), (CARD[0] + r, CARD[3] - r), (CARD[2] - r, CARD[3] - r)):
        sx, sy = np.sign(cx - W / 2), np.sign(cy - H / 2)
        alpha[int(min(cy, cy + sy * r)):int(max(cy, cy + sy * r)) + 1, int(min(cx, cx + sx * r)):int(max(cx, cx + sx * r)) + 1] = 0
        cv2.circle(alpha, (cx, cy), r, 1.0, -1, cv2.LINE_AA)
    out = tilt(c, alpha, n)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), (np.clip(out, 0, 1) * 255).astype(np.uint8))
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    with Pool(8) as p:
        for n in p.imap_unordered(render, ONLY):
            pass
    print("done", len(ONLY), "->", OUT)
