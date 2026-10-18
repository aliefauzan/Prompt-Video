"""Windows 95 Desktop UI: the clip playing inside a 1995 desktop.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [all | frame numbers...]

Everything is drawn on an 810x540 canvas with no anti-aliasing and blown up 2x
with nearest neighbour, so the UI stays pixel-crisp:
  * flat teal desktop, a column of original pixel-art desktop icons with labels
  * a grey bevelled media-player window (navy title bar, menu bar, sunken video
    well, play/pause/stop buttons, a seek bar that moves with the clip, a time
    readout)
  * the footage inside the window at 300x200 (shown 2x), reduced to a
    256-colour palette (6x6x6 cube plus greys) with an 8x8 ordered dither
  * error dialogs pop up one by one as the clip plays and pile up in a cascade
    over the lower right (never over the faces), with an original stop icon
  * a black-outlined white arrow cursor drifts around and "clicks"
  * a grey taskbar: Start button (original computer glyph, no logo), the
    pressed media-player task button, and a sunken tray with a clock
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FRAMES, MASKS, OUT = sys.argv[1:4]
ARGS = sys.argv[4:]
W, H = 1620, 1080
CW, CH = 810, 540
TEAL = (0, 128, 128)
GREY = (192, 192, 192)
DGREY = (128, 128, 128)
NAVY = (0, 0, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SUP = "/System/Library/Fonts/Supplemental/"
TOTAL = 179

# window + video well geometry on the 810x540 canvas
WX0, WY0, WX1, WY1 = 96, 10, 716, 494
VX0, VY0 = 106, 50
VW, VH = 600, 400


def f(size, bold=False):
    try:
        return ImageFont.truetype(SUP + ("Tahoma Bold.ttf" if bold else "Microsoft Sans Serif.ttf"), size)
    except OSError:
        return ImageFont.truetype(SUP + "Arial.ttf", size)


def load(n):
    img = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png"))
    return img


def bayer8():
    b = np.array([[0]])
    for _ in range(3):
        b = np.block([[4 * b, 4 * b + 2], [4 * b + 3, 4 * b + 1]])
    return (b.astype(np.float32) + 0.5) / 64 - 0.5


PAL = np.array([(r, g, b) for r in range(6) for g in range(6) for b in range(6)], np.float32) * 51


def quantize256(rgb):
    """6x6x6 colour cube with ordered dither (plus near-grey snapping), like a 256-colour display."""
    x = rgb.astype(np.float32)
    h, w = x.shape[:2]
    d = np.tile(bayer8(), (h // 8 + 1, w // 8 + 1))[:h, :w][..., None]
    q = np.floor(x / 51 + 0.5 + d * 0.9)
    q = np.clip(q, 0, 5) * 51
    # snap low-chroma pixels to a 16-step grey ramp (the extra system greys)
    gray = x.mean(2, keepdims=True)
    lowc = (x.max(2) - x.min(2) < 14)[..., None]
    gq = np.clip(np.floor(gray / 17 + 0.5 + d[..., :1] * 0.9), 0, 15) * 17
    q = np.where(lowc, np.repeat(gq, 3, 2), q)
    return q.astype(np.uint8)


def bevel(d, x0, y0, x1, y1, raised=True, face=GREY):
    d.rectangle((x0, y0, x1, y1), fill=face)
    lt, rb = (WHITE, BLACK) if raised else (BLACK, WHITE)
    lt2, rb2 = (GREY, DGREY) if raised else (DGREY, GREY)
    d.line((x0, y0, x1, y0), fill=lt)
    d.line((x0, y0, x0, y1), fill=lt)
    d.line((x0, y1, x1, y1), fill=rb)
    d.line((x1, y0, x1, y1), fill=rb)
    d.line((x0 + 1, y0 + 1, x1 - 1, y0 + 1), fill=lt2 if not raised else (223, 223, 223))
    d.line((x0 + 1, y0 + 1, x0 + 1, y1 - 1), fill=lt2 if not raised else (223, 223, 223))
    d.line((x0 + 1, y1 - 1, x1 - 1, y1 - 1), fill=rb2)
    d.line((x1 - 1, y0 + 1, x1 - 1, y1 - 1), fill=rb2)


def title_buttons(d, x1, y):
    for i, g in enumerate(("x", "box", "_")):
        bx = x1 - 4 - 16 * (i + 1) - (2 if i else 0)
        bevel(d, bx, y + 2, bx + 15, y + 15)
        if g == "x":
            d.line((bx + 4, y + 5, bx + 10, y + 11), fill=BLACK, width=2)
            d.line((bx + 10, y + 5, bx + 4, y + 11), fill=BLACK, width=2)
        elif g == "box":
            d.rectangle((bx + 3, y + 4, bx + 11, y + 11), outline=BLACK)
            d.line((bx + 3, y + 5, bx + 11, y + 5), fill=BLACK)
        else:
            d.line((bx + 4, y + 11, bx + 9, y + 11), fill=BLACK, width=2)


def window(d, x0, y0, x1, y1, title, active=True):
    bevel(d, x0, y0, x1, y1)
    d.rectangle((x0 + 3, y0 + 3, x1 - 3, y0 + 20), fill=NAVY if active else DGREY)
    d.text((x0 + 8, y0 + 5), title, font=f(11, True), fill=WHITE if active else GREY)
    title_buttons(d, x1 - 2, y0 + 2)


def stop_icon(d, x, y):
    d.ellipse((x, y, x + 31, y + 31), fill=(255, 0, 0), outline=(128, 0, 0))
    d.line((x + 9, y + 9, x + 22, y + 22), fill=WHITE, width=4)
    d.line((x + 22, y + 9, x + 9, y + 22), fill=WHITE, width=4)


def dialog(d, x, y, lines):
    w, h = 250, 112
    window(d, x, y, x + w, y + h, "Error")
    stop_icon(d, x + 14, y + 32)
    for i, ln in enumerate(lines):
        d.text((x + 58, y + 34 + i * 14), ln, font=f(11), fill=BLACK)
    for i, lab in enumerate(("OK", "Cancel")):
        bx = x + 52 + i * 84
        bevel(d, bx, y + h - 30, bx + 72, y + h - 8)
        if i == 0:
            d.rectangle((bx - 1, y + h - 31, bx + 73, y + h - 7), outline=BLACK)
        tw = d.textlength(lab, font=f(11))
        d.text((bx + 36 - tw / 2, y + h - 26), lab, font=f(11), fill=BLACK)


# ---- original pixel-art desktop icons (drawn with rectangles) ----

def icon_pc(d, x, y):
    d.rectangle((x + 4, y, x + 27, y + 18), fill=GREY, outline=BLACK)
    d.rectangle((x + 7, y + 3, x + 24, y + 15), fill=(0, 0, 160))
    d.rectangle((x + 9, y + 5, x + 16, y + 9), fill=(0, 160, 160))
    d.rectangle((x + 12, y + 19, x + 19, y + 21), fill=DGREY)
    d.rectangle((x + 2, y + 22, x + 29, y + 29), fill=GREY, outline=BLACK)
    d.line((x + 18, y + 25, x + 25, y + 25), fill=BLACK)


def icon_folder(d, x, y):
    d.rectangle((x + 2, y + 6, x + 12, y + 10), fill=(255, 255, 128), outline=BLACK)
    d.rectangle((x + 2, y + 9, x + 29, y + 27), fill=(255, 255, 0), outline=BLACK)
    d.line((x + 3, y + 10, x + 28, y + 10), fill=(255, 255, 192))


def icon_trash(d, x, y):
    d.rectangle((x + 7, y + 4, x + 24, y + 7), fill=GREY, outline=BLACK)
    d.polygon([(x + 8, y + 8), (x + 23, y + 8), (x + 21, y + 29), (x + 10, y + 29)], fill=(224, 224, 224), outline=BLACK)
    for k in (12, 16, 20):
        d.line((x + k, y + 11, x + k - 0.5, y + 26), fill=DGREY)


def icon_doc(d, x, y):
    d.polygon([(x + 6, y + 1), (x + 20, y + 1), (x + 26, y + 7), (x + 26, y + 30), (x + 6, y + 30)], fill=WHITE, outline=BLACK)
    for k in range(9, 28, 4):
        d.line((x + 9, y + k, x + 23, y + k), fill=(0, 0, 128))


def icon_globe(d, x, y):
    d.ellipse((x + 3, y + 2, x + 28, y + 27), fill=(0, 96, 192), outline=BLACK)
    d.polygon([(x + 9, y + 7), (x + 16, y + 6), (x + 15, y + 14), (x + 9, y + 15)], fill=(0, 160, 0))
    d.polygon([(x + 18, y + 16), (x + 24, y + 14), (x + 22, y + 23)], fill=(0, 160, 0))


ICONS = [(icon_pc, "My PC"), (icon_folder, "Clips"), (icon_doc, "notes.txt"), (icon_globe, "The Web"),
         (icon_folder, "New Folder"), (icon_trash, "Bin")]

DIALOGS = [  # (appears at frame, text)
    (30, ["Cannot find FRIENDS.EXE.", "Make sure the path is correct."]),
    (54, ["Too much fun detected.", "Continue anyway?"]),
    (78, ["office_clip.avi is not", "responding."]),
    (98, ["Not enough memory to", "display this vibe."]),
    (118, ["Unexpected smile at", "0x0000F00D."]),
    (138, ["Error copying file.", "Disk is full of memories."]),
    (156, ["Are you sure you want to", "end the fun?"]),
]


def cursor(d, x, y):
    pts = [(0, 0), (0, 16), (4, 12), (7, 19), (9, 18), (6, 11), (11, 11)]
    poly = [(x + px, y + py) for px, py in pts]
    d.polygon(poly, fill=WHITE, outline=BLACK)


def render(n):
    frame = load(n)
    # 300x200 playback (shown at 2x in the 600x400 well), 256 colours
    rgb = cv2.cvtColor(cv2.resize(frame, (VW // 2, VH // 2), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2RGB)
    vid = cv2.resize(quantize256(rgb), (VW, VH), interpolation=cv2.INTER_NEAREST)

    im = Image.new("RGB", (CW, CH), TEAL)
    d = ImageDraw.Draw(im)
    d.fontmode = "1"     # no anti-aliasing: bitmap-style text

    # desktop icons
    for i, (fn, lab) in enumerate(ICONS):
        x, y = 22, 14 + i * 70
        fn(d, x, y)
        tw = d.textlength(lab, font=f(11))
        d.text((x + 16 - tw / 2, y + 36), lab, font=f(11), fill=WHITE)

    # a second, inactive window peeking out behind the player (top-right)
    window(d, 640, 48, 800, 250, "Clips", active=False)
    d.rectangle((644, 70, 796, 246), fill=WHITE)
    for k in range(3):
        icon_folder(d, 724, 80 + k * 52)

    # media-player window
    window(d, WX0, WY0, WX1, WY1, "office_clip.avi - Media Player")
    for i, lab in enumerate(("File", "Edit", "View", "Play", "Help")):
        d.text((WX0 + 10 + i * 40, WY0 + 23), lab, font=f(11), fill=BLACK)
        d.line((WX0 + 10 + i * 40, WY0 + 35, WX0 + 15 + i * 40, WY0 + 35), fill=BLACK)
    bevel(d, VX0 - 2, VY0 - 2, VX0 + VW + 1, VY0 + VH + 1, raised=False)
    im.paste(Image.fromarray(vid), (VX0, VY0))
    # transport controls
    cy = VY0 + VH + 8
    for i in range(3):
        bx = VX0 + i * 28
        bevel(d, bx, cy, bx + 24, cy + 22)
    d.polygon([(VX0 + 9, cy + 6), (VX0 + 9, cy + 16), (VX0 + 17, cy + 11)], fill=BLACK)      # play
    d.rectangle((VX0 + 28 + 8, cy + 6, VX0 + 28 + 10, cy + 16), fill=BLACK)                  # pause
    d.rectangle((VX0 + 28 + 14, cy + 6, VX0 + 28 + 16, cy + 16), fill=BLACK)
    d.rectangle((VX0 + 56 + 7, cy + 6, VX0 + 56 + 17, cy + 16), fill=BLACK)                  # stop
    tx0, tx1 = VX0 + 96, VX0 + 470
    bevel(d, tx0, cy + 9, tx1, cy + 13, raised=False, face=WHITE)
    for k in range(11):
        xk = tx0 + (tx1 - tx0) * k / 10
        d.line((xk, cy + 17, xk, cy + 20), fill=BLACK)
    p = (n - 1) / (TOTAL - 1)
    th = int(tx0 + (tx1 - tx0) * p)
    bevel(d, th - 5, cy + 2, th + 5, cy + 20)
    sec = (n - 1) / 12
    d.text((VX0 + 488, cy + 5), f"0:{int(sec):02d} / 0:14", font=f(11), fill=BLACK)

    # error dialogs pile up as the clip plays (lower right, below the faces)
    k = 0
    for start, lines in DIALOGS:
        if n >= start:
            dialog(d, 440 + k * 16, 286 + k * 16, lines)
            k += 1

    # taskbar
    d.rectangle((0, CH - 28, CW, CH), fill=GREY)
    d.line((0, CH - 28, CW, CH - 28), fill=GREY)
    d.line((0, CH - 27, CW, CH - 27), fill=WHITE)
    bevel(d, 2, CH - 24, 58, CH - 3)
    # original start glyph: a tiny grey monitor (no logo)
    d.rectangle((7, CH - 20, 18, CH - 11), fill=(0, 128, 128), outline=BLACK)
    d.rectangle((10, CH - 10, 15, CH - 8), fill=BLACK)
    d.text((22, CH - 20), "Start", font=f(11, True), fill=BLACK)
    bevel(d, 64, CH - 24, 240, CH - 3, raised=False, face=(224, 224, 224))
    d.text((72, CH - 20), "office_clip.avi - Media...", font=f(11, True), fill=BLACK)
    bevel(d, 244, CH - 24, 400, CH - 3)
    d.text((252, CH - 20), "Clips", font=f(11), fill=BLACK)
    bevel(d, CW - 82, CH - 24, CW - 3, CH - 3, raised=False)
    d.polygon([(CW - 76, CH - 16), (CW - 72, CH - 16), (CW - 68, CH - 20), (CW - 68, CH - 7), (CW - 72, CH - 11),
               (CW - 76, CH - 11)], fill=BLACK)
    d.text((CW - 58, CH - 20), "12:40 PM", font=f(11), fill=BLACK)

    # cursor drifts and visits each new dialog's OK button
    t = n / 12.0
    cx = 400 + 220 * np.sin(t * 0.7) + 40 * np.sin(t * 2.3)
    cy2 = 380 + 90 * np.sin(t * 0.9 + 1) + 20 * np.cos(t * 1.7)
    for start, _ in DIALOGS:
        if 0 <= n - start < 8:
            kk = [s for s, _ in DIALOGS].index(start)
            tx = 440 + kk * 16 + 52 + 30
            ty = 286 + kk * 16 + 112 - 20
            a = (n - start) / 7
            cx, cy2 = cx * (1 - a) + tx * a, cy2 * (1 - a) + ty * a
    cursor(d, int(cx), int(cy2))

    out = im.resize((W, H), Image.NEAREST)
    return cv2.cvtColor(np.array(out), cv2.COLOR_RGB2BGR)


def job(n):
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), render(n))
    return n


def main():
    os.makedirs(OUT, exist_ok=True)
    total = len([f for f in os.listdir(FRAMES) if f.startswith("frame_") and f.endswith(".png")])
    nums = list(range(1, total + 1)) if (not ARGS or ARGS == ["all"]) else [int(a) for a in ARGS]
    with Pool(3) as p:
        for _ in p.imap_unordered(job, nums):
            pass
    print("done", len(nums))


if __name__ == "__main__":
    main()
