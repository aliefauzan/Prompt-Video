"""Wes Anderson Pastel Symmetry, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [all | frame numbers...]

  * the room is replaced by one flat, perfectly symmetrical pastel set built
    once (locked-off camera): a pink upper wall with a cream cornice, a mint
    panelled wainscot under a mustard chair rail, a centred mustard window
    with pale sky panes, matching sconces and framed pictures either side,
    a burgundy sign in Futura, a burgundy carpet strip
  * the people come from the masks, untouched in pose and identity, graded
    into the same world: lifted blacks, low contrast, warm flat front light,
    pastel-leaning saturation
  * a faint soft shadow of the people falls straight back onto the wall
  * a centred Futura chapter caption, a fine film grain
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
CX = W // 2
FUTURA = "/System/Library/Fonts/Supplemental/Futura.ttc"

# palette (RGB)
PINK = (239, 182, 186)
PINK_D = (214, 150, 158)
MINT = (160, 206, 190)
MINT_D = (128, 178, 162)
MINT_L = (190, 226, 212)
MUSTARD = (226, 178, 74)
MUSTARD_D = (190, 140, 52)
CREAM = (246, 232, 204)
SKY = (178, 214, 228)
BURGUNDY = (128, 44, 58)
RED = (196, 70, 64)

SET = None
CAPTION = None


def font(size, idx=0):
    return ImageFont.truetype(FUTURA, size, index=idx)


def sym_rect(d, x0, y0, x1, y1, **kw):
    """Draw a rectangle and its mirror about the centre line."""
    d.rectangle([x0, y0, x1, y1], **kw)
    d.rectangle([W - 1 - x1, y0, W - 1 - x0, y1], **kw)


def build_set():
    im = Image.new("RGB", (W, H), PINK)
    d = ImageDraw.Draw(im)
    rail = 640
    # cornice
    d.rectangle([0, 0, W, 34], fill=CREAM)
    d.rectangle([0, 34, W, 42], fill=PINK_D)
    d.rectangle([0, 42, W, 48], fill=CREAM)
    # pink wall: vertical pilasters, symmetric
    for x in (70, 330):
        sym_rect(d, x, 48, x + 46, rail, fill=PINK_D)
        sym_rect(d, x + 8, 48, x + 38, rail, fill=(244, 196, 198))
    # wainscot
    d.rectangle([0, rail, W, H], fill=MINT)
    d.rectangle([0, rail - 18, W, rail + 6], fill=MUSTARD)
    d.rectangle([0, rail + 6, W, rail + 12], fill=MUSTARD_D)
    # panels in the wainscot, mirrored
    pw, gap, x = 170, 34, 30
    while x + pw < CX - 20:
        sym_rect(d, x, rail + 50, x + pw, H - 110, outline=MINT_D, width=6)
        sym_rect(d, x + 14, rail + 64, x + pw - 14, H - 124, outline=MINT_L, width=3)
        x += pw + gap
    d.rectangle([0, H - 80, W, H], fill=BURGUNDY)
    d.rectangle([0, H - 86, W, H - 80], fill=MUSTARD)
    # centred window with mustard frame
    wx0, wx1, wy0, wy1 = CX - 300, CX + 300, 120, 520
    d.rectangle([wx0 - 26, wy0 - 26, wx1 + 26, wy1 + 26], fill=MUSTARD_D)
    d.rectangle([wx0 - 18, wy0 - 18, wx1 + 18, wy1 + 18], fill=MUSTARD)
    d.rectangle([wx0, wy0, wx1, wy1], fill=SKY)
    for i in range(1, 3):
        x = wx0 + i * (wx1 - wx0) // 3
        d.rectangle([x - 7, wy0, x + 7, wy1], fill=CREAM)
    d.rectangle([wx0, (wy0 + wy1) // 2 - 7, wx1, (wy0 + wy1) // 2 + 7], fill=CREAM)
    # half-drawn pink curtains, mirrored
    for k in range(5):
        sym_rect(d, wx0 - 60 + k * 14, wy0 - 40, wx0 - 50 + k * 14, wy1 + 50,
                 fill=RED if k % 2 == 0 else (176, 58, 56))
    d.rectangle([wx0 - 80, wy0 - 52, wx1 + 80, wy0 - 30], fill=RED)
    # sign above the window
    f = font(40, 2)
    txt = "BUREAU  OF  ACCOUNTS"
    tw = d.textlength(txt, font=f)
    d.rectangle([CX - tw / 2 - 30, 62, CX + tw / 2 + 30, 108], fill=BURGUNDY)
    d.text((CX - tw / 2, 64), txt, font=f, fill=MUSTARD)
    # framed pictures and sconces, mirrored
    sym_rect(d, 150, 200, 290, 380, fill=MUSTARD)
    sym_rect(d, 162, 212, 278, 368, fill=CREAM)
    sym_rect(d, 180, 236, 260, 344, fill=MINT)
    for sx in (430, W - 1 - 430):
        d.rectangle([sx - 6, 300, sx + 6, 360], fill=MUSTARD_D)
        d.ellipse([sx - 34, 250, sx + 34, 310], fill=CREAM, outline=MUSTARD_D, width=4)
    # a little paint texture
    arr = np.asarray(im).astype(np.float32) / 255
    rng = np.random.default_rng(64)
    tex = cv2.GaussianBlur(rng.normal(0, 1, (H, W)).astype(np.float32), (0, 0), 6) * 0.02
    arr = arr * (1 + tex[..., None])
    return np.clip(arr[..., ::-1], 0, 1).astype(np.float32)        # BGR


def build_caption():
    """Centred two-line chapter card, returned as (alpha, colour) layers."""
    im = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(im)
    f1, f2 = font(30, 2), font(54, 2)
    l1, l2 = "CHAPTER ONE", "The Three Colleagues"
    d.text((CX - d.textlength(l1, font=f1) / 2, H - 170), l1, font=f1, fill=255)
    d.text((CX - d.textlength(l2, font=f2) / 2, H - 130), l2, font=f2, fill=255)
    a = np.asarray(im).astype(np.float32) / 255
    shadow = cv2.GaussianBlur(a, (0, 0), 3)
    return a, shadow


def init(s, c):
    global SET, CAPTION
    SET, CAPTION = s, c


def grade_people(img):
    """Flat warm pastel light: lifted blacks, low contrast, warm, soft chroma."""
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2Lab)
    L = lab[..., 0]
    L = 22 + L * 0.74 + 6                                   # lift + compress
    lab[..., 0] = np.clip(L, 0, 100)
    lab[..., 1] = lab[..., 1] * 0.95 + 3                    # a touch pink
    lab[..., 2] = lab[..., 2] * 0.95 + 9                    # warm yellow
    out = cv2.cvtColor(lab, cv2.COLOR_Lab2BGR)
    return np.clip(out, 0, 1)


def render(n):
    rng = np.random.default_rng(6400 + n)
    img = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png")).astype(np.float32) / 255
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE)
    m = cv2.erode(m, np.ones((3, 3), np.uint8))
    m = cv2.GaussianBlur(m.astype(np.float32) / 255, (0, 0), 1.6)[..., None]

    bg = SET.copy()
    # soft shadow straight back onto the wall (flat front light)
    sh = cv2.GaussianBlur(m[..., 0], (0, 0), 18)
    sh = np.roll(sh, (10, 14), (0, 1))
    bg *= (1 - 0.22 * sh)[..., None]

    ppl = grade_people(img)
    out = bg * (1 - m) + ppl * m
    # unify: very slight warm haze over everything, gentle softness
    out = out * 0.96 + np.array([0.80, 0.90, 1.0], np.float32) * 0.04
    out = cv2.GaussianBlur(out, (0, 0), 0.5)
    # caption
    a, s = CAPTION
    out = out * (1 - 0.6 * s[..., None])
    out = out * (1 - a[..., None]) + a[..., None] * np.array([0.36, 0.84, 0.98], np.float32)
    out += rng.normal(0, 0.012, (H, W, 1)).astype(np.float32)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), (np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8))
    return n


def main():
    os.makedirs(OUT, exist_ok=True)
    nums = list(range(1, N + 1)) if not ARGS or ARGS == ["all"] else [int(a) for a in ARGS]
    s, c = build_set(), build_caption()
    with Pool(3, initializer=init, initargs=(s, c)) as p:
        for n in p.imap(render, nums):
            print(n, end=" ", flush=True)
    print()


if __name__ == "__main__":
    main()
