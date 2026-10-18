"""Magazine cover / kinetic editorial typography restyle, frame by frame.

usage: python -I render.py [frame numbers... | all]   (default: the six sheet frames)
       RENDER_OUT=/tmp/prompt-video-render/<slug> python -I render.py all   -> full clip for make_video.py
Reads ../../_source/frames + ../../_source/masks, writes ./frames/frame_NNN.png.
The person matte puts the masthead BEHIND heads and IN FRONT of bodies (woven depth).
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

SUP = "/System/Library/Fonts/Supplemental/"
FONTS = {
    "didot": (SUP + "Didot.ttc", 2), "didot_i": (SUP + "Didot.ttc", 1),
    "bodoni": (SUP + "Bodoni 72.ttc", 2),
    "heavy": ("/System/Library/Fonts/Avenir Next Condensed.ttc", 8),
    "demi": ("/System/Library/Fonts/Avenir Next Condensed.ttc", 2),
    "black": ("/System/Library/Fonts/HelveticaNeue.ttc", 9),
    "futura": (SUP + "Futura.ttc", 4),
}
RED, LIME, YELLOW = (215, 28, 38), (196, 255, 40), (255, 222, 0)
WHITE, INK, CREAM = (250, 248, 242), (14, 14, 16), (238, 230, 214)

# first, last, masthead word, masthead font, masthead colour, photo grade, background, accent, kicker lines
SECTIONS = [
    (1, 24, "MOTION", "didot", RED, "warm", "env", RED,
     [("THE NEW", "demi"), ("OFFICE", "heavy"), ("CREW", "heavy"), ("3 friends, 1 desk", "didot_i")],
     [("GEN Z", "heavy"), ("AT WORK", "heavy"), ("what they", "didot_i"), ("really want", "didot_i")]),
    (25, 60, "TRIO", "black", INK, "mono", "cream", RED,
     [("THE", "demi"), ("FRIENDSHIP", "heavy"), ("ISSUE", "heavy"), ("work, wit & wifi", "didot_i")],
     [("+27", "heavy"), ("STYLE NOTES", "demi"), ("batik is", "didot_i"), ("back", "didot_i")]),
    (61, 100, "FOCUS", "didot", INK, "cool", "env", LIME,
     [("STAY IN", "demi"), ("YOUR", "heavy"), ("LANE", "heavy"), ("the 9-to-5 reset", "didot_i")],
     [("LATE", "heavy"), ("NIGHTS", "heavy"), ("EARLY", "demi"), ("WINS", "demi")]),
    (101, 136, "OFFICE", "black", WHITE, "mono", "red", YELLOW,
     [("WHO", "heavy"), ("RUNS", "heavy"), ("THE ROOM?", "heavy"), ("a cover story", "didot_i")],
     [("DESK", "heavy"), ("CULTURE", "heavy"), ("2026", "demi"), ("special", "didot_i")]),
    (137, 160, "VISUAL", "bodoni", INK, "warm", "env", RED,
     [("IT'S ALL", "demi"), ("ABOUT", "heavy"), ("THE LOOK", "heavy"), ("stripes forever", "didot_i")],
     [("NEW", "heavy"), ("FACES", "heavy"), ("of the", "didot_i"), ("season", "didot_i")]),
    (161, 999, "FOCUS", "didot", LIME, "mono", "env", LIME,
     [("THE", "demi"), ("CLOSE-UP", "heavy"), ("ISSUE", "heavy"), ("one look, all in", "didot_i")],
     [("SHE", "heavy"), ("SAID", "heavy"), ("WHAT?", "heavy"), ("exclusive", "didot_i")]),
]


def section_of(n):
    for i, s in enumerate(SECTIONS):
        if s[0] <= n <= s[1]:
            return i, s
    return len(SECTIONS) - 1, SECTIONS[-1]


def font(key, size):
    p, i = FONTS[key]
    return ImageFont.truetype(p, int(size), index=i)


def ease(t):
    t = min(max(t, 0.0), 1.0)
    return 1 - (1 - t) ** 3


def grade(rgb, mode, rng):
    f = rgb.astype(np.float32) / 255
    if mode == "mono":
        g = f @ np.array([0.30, 0.59, 0.11], np.float32)
        g = np.clip((g - 0.06) / 0.86, 0, 1)
        g = g * g * (3 - 2 * g)
        f = np.repeat(g[..., None], 3, 2) * np.array([1.0, 0.985, 0.96], np.float32)
    else:
        f = np.clip((f - 0.03) / 0.92, 0, 1)
        f = f * f * (3 - 2 * f) * 0.6 + f * 0.4                          # editorial contrast
        lum = f.mean(2, keepdims=True)
        f = lum + (f - lum) * 1.12
        tint = np.array([1.04, 1.0, 0.93] if mode == "warm" else [0.95, 1.0, 1.05], np.float32)
        f = f * tint
    return np.clip(f, 0, 1)


def backdrop(kind, h, w, rng):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    r = np.sqrt(((xx - w * 0.5) / w) ** 2 + ((yy - h * 0.45) / h) ** 2)
    base = np.array(CREAM if kind == "cream" else (196, 38, 44), np.float32) / 255
    sweep = (1.08 - 0.45 * r)[..., None]                                     # studio seamless falloff
    return np.clip(base * sweep, 0, 1)


def text_alpha(h, w, items):
    """items: list of (text, font, (x, y), anchor). Returns float alpha 0..1."""
    im = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(im)
    for txt, fnt, xy, anchor in items:
        d.text(xy, txt, font=fnt, fill=255, anchor=anchor)
    return np.asarray(im, np.float32) / 255


def masthead_alpha(word, fkey, h, w, k, n_in):
    """Huge masthead fitted to the cover width; letters drop in at the start of a section,
    then the tracking keeps opening slowly (kinetic)."""
    target = w * 0.92
    size = 400
    f = font(fkey, size)
    widths = [f.getlength(c) for c in word]
    track0 = -0.02 * size
    total = sum(widths) + track0 * (len(word) - 1)
    size = size * target / total
    cap = f.getbbox("H")[3] - f.getbbox("H")[1]
    size = min(size, 400 * h * 0.34 / cap)                                   # cap the masthead height
    f = font(fkey, size)
    widths = [f.getlength(c) for c in word]
    track = -0.02 * size + 0.35 * k                                          # slow tracking drift
    total = sum(widths) + track * (len(word) - 1)
    x = (w - total) / 2
    top = f.getbbox(word)[1]
    items = []
    for i, c in enumerate(word):
        t = ease((n_in - i * 1.2) / 6.0)                                      # staggered drop-in
        dy = -(1 - t) * size * 0.9
        if t > 0:
            items.append((c, f, (x, 18 - top + dy), "la"))
        x += widths[i] + track
    return text_alpha(h, w, items), f.getbbox(word)[3] - top + 18


def barcode(img, rng, x, y):
    w, h = 190, 120
    img[y:y + h, x:x + w] = 0.98
    r = np.random.default_rng(42)
    bx = x + 12
    while bx < x + w - 14:
        bw = int(r.integers(1, 5))
        if r.random() < 0.55:
            img[y + 10:y + h - 32, bx:bx + bw] = 0.05
        bx += bw + int(r.integers(1, 3))


def over(dst, col, a):
    a = a[..., None]
    return dst * (1 - a) + np.asarray(col, np.float32)[None, None, :] / 255 * a


def render(n):
    si, (first, last, word, mfont, mcol, gmode, bg, accent, left, right) = section_of(n)
    rng = np.random.default_rng(14_000 + n)
    k = n - first                                                            # frames into the section
    bgr = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png"))
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    h, w = rgb.shape[:2]
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
    m = cv2.GaussianBlur(m, (0, 0), 1.2)

    photo = grade(rgb, gmode, rng)
    if bg == "env":
        img = photo.copy()
    else:
        img = backdrop(bg, h, w, rng)
        sh = cv2.GaussianBlur(np.roll(m, (10, 14), (0, 1)), (0, 0), 14) * 0.35   # studio contact shadow
        img = img * (1 - sh[..., None])
        img = img * (1 - m[..., None]) + photo * m[..., None]

    # masthead woven with the people: behind the heads, in front of the bodies
    ma, mh = masthead_alpha(word, mfont, h, w, k, k + 1)
    ys = np.nonzero(m.max(1) > 0.5)[0]
    heads = np.zeros_like(m)
    if len(ys):
        cols = m > 0.5
        topy = np.where(cols.any(0), cols.argmax(0), h)                      # per-column top of the people
        yy = np.arange(h)[:, None]
        heads = ((yy < topy[None, :] + 0.47 * h) & cols).astype(np.float32)  # head + shoulders zone
        heads = cv2.GaussianBlur(heads, (0, 0), 2)
    behind = np.clip(heads * m, 0, 1)
    img = over(img, mcol, ma * (1 - behind))

    # small kicker line above the masthead, issue info
    items = [(f"THE WORKPLACE ISSUE  ·  No. {14 + si}  ·  OCTOBER 2026", font("demi", 26), (w // 2, 10), "ma")]
    img = over(img, accent if mcol != accent else WHITE, text_alpha(h, w, items) * 0.95)

    # cover lines, typed on line by line
    def block(lines, x, anchor, col_main):
        nonlocal img
        y = int(h * 0.40)
        for j, (txt, fk) in enumerate(lines):
            size = {"heavy": 66, "demi": 38, "didot_i": 40}[fk]
            shown = int(np.ceil(len(txt) * ease((k - 1 - j * 0.8) / 3.0)))
            if shown <= 0:
                y += int(size * 1.02)
                continue
            col = accent if (fk == "heavy" and j % 2 == 1) else col_main
            a = text_alpha(h, w, [(txt[:shown], font(fk, size), (x, y), anchor)])
            sh = cv2.GaussianBlur(np.roll(a, (3, 3), (0, 1)), (0, 0), 3) * 0.35
            img = over(img, (0, 0, 0), sh)
            img = over(img, col, a)
            y += int(size * 1.02)

    cl_main = WHITE if bg != "cream" else INK
    block(left, 46, "la", cl_main)
    block(right, w - 46, "ra", cl_main)

    # sticker
    cx, cy, R = int(w * 0.80), int(h * 0.80), 74
    pop = ease((k - 4) / 3.0)
    if pop > 0:
        rr = int(R * (0.6 + 0.4 * pop))
        cv2.circle(img, (cx, cy), rr, tuple(float(c) / 255 for c in RED), -1, cv2.LINE_AA)
        img = over(img, WHITE, text_alpha(h, w, [("NEW", font("heavy", 50 * pop + 1), (cx, cy - 12), "mm"),
                                                 ("ISSUE", font("demi", 24 * pop + 1), (cx, cy + 26), "mm")]))
    # barcode + price
    barcode(img, rng, w - 236, h - 160)
    img = over(img, INK, text_alpha(h, w, [(f"0 14  2026  {first:03d}", font("demi", 18), (w - 141, h - 66), "ma"),
                                           ("$9.99", font("heavy", 22), (w - 141, h - 47), "ma")]))
    # thin rules + bottom line
    img[int(h * 0.385):int(h * 0.385) + 3, 46:300] = np.array(accent, np.float32) / 255
    img = over(img, cl_main, text_alpha(h, w, [("INSIDE: THE STRIPE THAT STARTED IT ALL  /  P. 42", font("demi", 30), (int(w * 0.24), h - 50), "ls")]))

    # print finish: fine grain, slight paper warmth, vignette, tiny registration shift of the masthead colour
    g = cv2.GaussianBlur(rng.normal(0, 1, (h, w)).astype(np.float32), (0, 0), 0.7)
    img = img + g[..., None] * 0.028
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    img = img * (1 - 0.18 * np.clip(r - 0.6, 0, 1))[..., None]
    out = (np.clip(img, 0, 1) * 255).astype(np.uint8)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), cv2.cvtColor(out, cv2.COLOR_RGB2BGR))
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    with Pool(6) as p:
        for n in p.imap_unordered(render, ONLY):
            print("frame", n)
