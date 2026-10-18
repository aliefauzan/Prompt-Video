"""Mucha Art Nouveau poster restyle, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [all | frame numbers...]

Per frame:
  * the people become a pale colour lithograph: edge-preserving smoothing,
    soft-posterised light, muted chroma pushed into Mucha's palette (peach skin,
    auburn hair, sage / ochre / dusty-rose cloth), dark sepia contour lines:
    a thick outer contour from the matte, finer flowing inner lines (DoG)
  * the room becomes flat poster ground in three muted sage / cream tones
  * a big ornamental halo (concentric rings, bead band, radiating spokes)
    sits behind the central woman's head and follows her (Apple Vision face
    boxes from faces.json, tracked and smoothed over time)
  * an arched Art Nouveau frame: rounded top corners, gold band with beads,
    whiplash corner curls, a title cartouche at the bottom
  * cream lithograph paper with a slightly changing speckle
"""
import json
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FRAMES, MASKS, OUT = sys.argv[1:4]
ARGS = sys.argv[4:]
HERE = os.path.dirname(os.path.abspath(__file__))
N = len([f for f in os.listdir(FRAMES) if f.startswith("frame_") and f.endswith(".png")])
W, H = 1620, 1080


def bgr(rgb):
    return np.array(rgb[::-1], np.float32) / 255


INK = bgr((74, 48, 34))          # sepia contour
GOLD = bgr((200, 160, 88))
GOLD_D = bgr((150, 112, 58))
CREAM = bgr((242, 230, 202))
SAGE = bgr((170, 178, 142))
SAGE_D = bgr((118, 128, 98))
ROSE = bgr((214, 160, 138))
HALO_IN = bgr((236, 218, 170))
HALO_BAND = bgr((182, 190, 150))


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


def halo_track():
    """Centre (x, y) and radius of the halo per frame: the central woman's face, smoothed."""
    faces = json.load(open(os.path.join(HERE, "faces.json")))
    pts, prev = [], None
    for n in range(1, N + 1):
        fs = [f["box"] for f in faces.get(f"frame_{n:03d}.png", [])]
        cand = [(x + w / 2, y + h / 2, w) for x, y, w, h in fs]
        if prev is None:
            pick = min(cand, key=lambda c: abs(c[0] - W / 2))
        else:
            near = [c for c in cand if abs(c[0] - prev[0]) < max(160, prev[2] * 0.8)]
            pick = min(near, key=lambda c: abs(c[0] - prev[0])) if near else prev
        pts.append(pick)
        prev = pick
    p = np.array(pts, np.float32)
    k = 4
    pad = np.pad(p, ((k, k), (0, 0)), mode="edge")
    sm = np.stack([np.convolve(pad[:, i], np.ones(2 * k + 1) / (2 * k + 1), mode="same")[k:-k] for i in range(3)], 1)
    return sm


def paper(rng):
    base = cv2.GaussianBlur(rng.normal(0, 1, (H // 2, W // 2)).astype(np.float32), (0, 0), 1.0)
    fib = cv2.resize(base, (W, H)) * 0.018
    speck = (rng.random((H, W)) > 0.9985).astype(np.float32) * -0.10
    return 1 + fib + cv2.GaussianBlur(speck, (0, 0), 0.7)


def litho(img):
    """Pale, muted, soft-posterised colour for the people."""
    small = cv2.resize(img, (W // 2, H // 2), interpolation=cv2.INTER_AREA)
    for _ in range(3):
        small = cv2.bilateralFilter(small, 9, 0.12, 6)
    sm = cv2.resize(small, (W, H), interpolation=cv2.INTER_LINEAR)
    lab = cv2.cvtColor(sm, cv2.COLOR_BGR2Lab)
    L, a, b = lab[..., 0], lab[..., 1], lab[..., 2]
    # soft posterise into 5 bands, then lift: pale lithograph values
    q = L / 100 * 4
    f = q - np.floor(q)
    q = np.floor(q) + np.clip((f - 0.35) / 0.3, 0, 1)
    L2 = 42 + q / 4 * 54
    neutral = np.clip(1 - np.hypot(a, b) / 18, 0, 1)        # greys -> sage green, not grey
    a2 = a * 0.55 + 4 - 11 * neutral
    b2 = b * 0.60 + 10 + 2 * neutral
    out = cv2.cvtColor(np.dstack([L2, a2, b2]).astype(np.float32), cv2.COLOR_Lab2BGR)
    return np.clip(out, 0, 1), sm


def ground(img):
    """Room -> flat poster ground: sage-to-cream wash, a faint ghost of the room,
    and a repeating Art Nouveau rosette-and-stem wallpaper (static, like print)."""
    global GROUND
    if GROUND is None:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        t = np.clip(1 - np.hypot((xx - W / 2) / W, (yy - H * 0.35) / H) * 1.6, 0, 1)[..., None]
        wash = SAGE * (1 - t) + CREAM * t
        pat = Image.new("L", (W, H), 0)
        d = ImageDraw.Draw(pat)
        for j, y in enumerate(range(40, H, 120)):
            for x in range(40 + (j % 2) * 70, W, 140):
                d.line((x, y + 18, x, y + 100), fill=150, width=3)            # stem
                d.arc((x - 30, y + 40, x, y + 90), 270, 90, fill=150, width=3)  # whiplash leaf
                d.arc((x, y + 50, x + 30, y + 100), 90, 270, fill=150, width=3)
                for k in range(5):
                    u = k / 5 * 2 * np.pi - np.pi / 2
                    d.ellipse((x + np.cos(u) * 10 - 8, y + np.sin(u) * 10 - 8, x + np.cos(u) * 10 + 8, y + np.sin(u) * 10 + 8), outline=255, width=2)
        pat = cv2.GaussianBlur(np.array(pat).astype(np.float32) / 255, (0, 0), 0.8)[..., None]
        GROUND = wash * (1 - pat * 0.22) + SAGE_D * pat * 0.22
    small = cv2.resize(img, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
    g = cv2.GaussianBlur(cv2.cvtColor(small, cv2.COLOR_BGR2GRAY), (0, 0), 4)
    g = cv2.resize(g, (W, H), interpolation=cv2.INTER_CUBIC)
    ghost = np.clip((0.55 - g) / 0.3, 0, 1)[..., None] * 0.22     # dark furniture/screen as faint sage shapes
    return GROUND * (1 - ghost) + SAGE_D * ghost


def halo(cx, cy, r):
    """RGBA-ish halo: returns colour image and alpha."""
    s = 2
    im = Image.new("RGBA", (W * s // 2, H * s // 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    k = s / 2
    X, Y, R = cx * k, cy * k, r * k

    def c(rgb, a=255):
        return tuple(int(v) for v in rgb) + (a,)
    ink = c((74, 48, 34))
    d.ellipse((X - R, Y - R, X + R, Y + R), fill=c((182, 190, 150)), outline=ink, width=max(2, int(4 * k)))
    # radiating spokes in the outer band
    for i in range(48):
        t = i / 48 * 2 * np.pi
        r0, r1 = R * 0.80, R * 0.97
        d.line((X + np.cos(t) * r0, Y + np.sin(t) * r0, X + np.cos(t) * r1, Y + np.sin(t) * r1),
               fill=c((150, 112, 58)), width=max(1, int(2 * k)))
    d.ellipse((X - R * 0.80, Y - R * 0.80, X + R * 0.80, Y + R * 0.80), fill=c((200, 160, 88)), outline=ink, width=max(1, int(3 * k)))
    # bead band
    for i in range(36):
        t = i / 36 * 2 * np.pi
        bx, by, br = X + np.cos(t) * R * 0.72, Y + np.sin(t) * R * 0.72, R * 0.035
        d.ellipse((bx - br, by - br, bx + br, by + br), fill=c((242, 230, 202)), outline=ink, width=1)
    d.ellipse((X - R * 0.64, Y - R * 0.64, X + R * 0.64, Y + R * 0.64), fill=c((236, 218, 170)), outline=ink, width=max(1, int(3 * k)))
    for f in (0.52, 0.40):
        d.ellipse((X - R * f, Y - R * f, X + R * f, Y + R * f), outline=c((200, 160, 88)), width=max(1, int(2 * k)))
    # small quatrefoil flowers around the inner disc
    for i in range(8):
        t = i / 8 * 2 * np.pi + np.pi / 8
        fx, fy, fr = X + np.cos(t) * R * 0.58, Y + np.sin(t) * R * 0.58, R * 0.05
        for j in range(4):
            u = j / 4 * 2 * np.pi
            px, py = fx + np.cos(u) * fr, fy + np.sin(u) * fr
            d.ellipse((px - fr * 0.8, py - fr * 0.8, px + fr * 0.8, py + fr * 0.8), fill=c((214, 160, 138)), outline=ink, width=1)
    arr = np.array(im.resize((W, H), Image.LANCZOS)).astype(np.float32) / 255
    return arr[..., [2, 1, 0]], arr[..., 3]


def frame_overlay():
    """Arched Art Nouveau border + title cartouche (static, drawn once)."""
    s = 2
    im = Image.new("RGBA", (W * s, H * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    ink, gold, gold_d, cream, sage = (74, 48, 34, 255), (200, 160, 88, 255), (150, 112, 58, 255), (242, 230, 202, 255), (170, 178, 142, 255)
    m, band, rad = 22 * s, 30 * s, 230 * s
    # panel shape (arched top corners): everything outside it is border
    panel = Image.new("L", (W * s, H * s), 0)
    pd = ImageDraw.Draw(panel)
    x0, y0, x1, y1 = m + band, m + band, W * s - m - band, H * s - m - band - 70 * s
    pd.rounded_rectangle((x0, y0, x1, y1 + rad), radius=rad, fill=255)
    pd.rectangle((x0, y0 + rad, x1, y1), fill=255)
    pd.rectangle((x0, y1 - 4, x1, y1 + rad + 10), fill=0)
    border = Image.new("RGBA", (W * s, H * s), gold)
    bd = ImageDraw.Draw(border)
    bd.rectangle((0, 0, W * s - 1, H * s - 1), outline=ink, width=m)
    bd.rectangle((m, m, W * s - m, H * s - m), outline=ink, width=4 * s)
    # beads along the band
    for x in range(m + band // 2, W * s - m, 34 * s):
        for y in (m + band // 2, H * s - m - band // 2):
            bd.ellipse((x - 6 * s, y - 6 * s, x + 6 * s, y + 6 * s), fill=cream, outline=ink, width=s)
    for y in range(m + band // 2, H * s - m, 34 * s):
        for x in (m + band // 2, W * s - m - band // 2):
            bd.ellipse((x - 6 * s, y - 6 * s, x + 6 * s, y + 6 * s), fill=cream, outline=ink, width=s)
    # spandrels above the arch: sage with whiplash curls and a flower
    for side in (0, 1):
        cx = x0 + rad if side == 0 else x1 - rad
        sx = x0 if side == 0 else x1
        sgn = 1 if side == 0 else -1
        bd.pieslice((x0 - 2, y0 - 2, x0 + 2 * rad, y0 + 2 * rad) if side == 0 else (x1 - 2 * rad, y0 - 2, x1 + 2, y0 + 2 * rad),
                    0, 360, fill=None)
        for k, rr in enumerate((rad * 0.75, rad * 0.5, rad * 0.28)):
            ax = sx + sgn * rr * 0.55
            ay = y0 + rr * 0.55
            bd.arc((ax - rr * 0.5, ay - rr * 0.5, ax + rr * 0.5, ay + rr * 0.5), 180 if side == 0 else 270, 90 if side == 0 else 180,
                   fill=gold_d, width=3 * s)
        fx, fy, fr = sx + sgn * rad * 0.22, y0 + rad * 0.22, 18 * s
        for j in range(5):
            u = j / 5 * 2 * np.pi
            px, py = fx + np.cos(u) * fr, fy + np.sin(u) * fr
            bd.ellipse((px - fr * 0.7, py - fr * 0.7, px + fr * 0.7, py + fr * 0.7), fill=(214, 160, 138, 255), outline=ink, width=s)
        bd.ellipse((fx - fr * 0.5, fy - fr * 0.5, fx + fr * 0.5, fy + fr * 0.5), fill=gold, outline=ink, width=s)
    # title cartouche
    ty0, ty1 = y1 + 8 * s, H * s - m - band + 12 * s
    bd.rectangle((x0, ty0, x1, ty1), fill=cream, outline=ink, width=4 * s)
    bd.rectangle((x0 + 10 * s, ty0 + 10 * s, x1 - 10 * s, ty1 - 10 * s), outline=gold_d, width=2 * s)
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Herculanum.ttf", 46 * s)
    txt = "ATELIER  ·  MCMXXVI"
    tw = bd.textlength(txt, font=font)
    bd.text(((W * s - tw) / 2, (ty0 + ty1) / 2 - 26 * s), txt, font=font, fill=ink)
    for side in (-1, 1):
        cx = W * s / 2 + side * (tw / 2 + 50 * s)
        bd.ellipse((cx - 10 * s, (ty0 + ty1) / 2 - 10 * s, cx + 10 * s, (ty0 + ty1) / 2 + 10 * s), fill=gold, outline=ink, width=s)
    alpha = 255 - np.array(panel)
    arr = np.array(border)
    arr[..., 3] = alpha
    # inner contour line of the panel
    edge = cv2.morphologyEx(np.array(panel), cv2.MORPH_GRADIENT, np.ones((7 * s, 7 * s), np.uint8))
    arr[edge > 0] = ink
    out = Image.fromarray(arr).resize((W, H), Image.LANCZOS)
    o = np.array(out).astype(np.float32) / 255
    return o[..., [2, 1, 0]], o[..., 3]


TRACK = None
BORDER = None
GROUND = None


def init(track):
    global TRACK, BORDER
    TRACK = track
    BORDER = frame_overlay()


def render(n):
    rng = np.random.default_rng(700 + n)
    img, m = load(n)
    ms = cv2.GaussianBlur(m, (0, 0), 1.2)

    col, sm = litho(img)
    out = ground(img)
    cx, cy, fw = TRACK[n - 1]
    r = float(np.clip(fw * 1.75, 180, 440))
    hc, ha = halo(cx, cy - fw * 0.05, r)
    out = out * (1 - ha[..., None]) + hc * ha[..., None]
    out = out * (1 - ms[..., None]) + col * ms[..., None]

    # contour lines: thick outer from the matte, fine inner from DoG of the smoothed image
    hard = (m > 0.5).astype(np.uint8) * 255
    outer = cv2.morphologyEx(hard, cv2.MORPH_GRADIENT, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))
    outer = cv2.GaussianBlur(outer.astype(np.float32) / 255, (0, 0), 1.0)
    g = cv2.cvtColor(sm, cv2.COLOR_BGR2GRAY)
    dog = cv2.GaussianBlur(g, (0, 0), 1.4) - cv2.GaussianBlur(g, (0, 0), 3.2)
    inner = np.clip((-dog - 0.010) / 0.016, 0, 1)
    inner = cv2.GaussianBlur(inner, (0, 0), 0.7) * cv2.erode(m, np.ones((5, 5), np.uint8))
    line = np.clip(outer + inner * 0.85, 0, 1)
    out = out * (1 - line[..., None]) + INK * line[..., None]

    # border + paper
    bc, ba = BORDER
    out = out * (1 - ba[..., None]) + bc * ba[..., None]
    out = out * paper(rng)[..., None]
    out = np.clip(out, 0, 1)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), (out * 255).astype(np.uint8))
    return n


def main():
    os.makedirs(OUT, exist_ok=True)
    nums = list(range(1, N + 1)) if (not ARGS or ARGS == ["all"]) else [int(a) for a in ARGS]
    track = halo_track()
    with Pool(min(5, os.cpu_count() or 4), initializer=init, initargs=(track,)) as p:
        for _ in p.imap_unordered(render, nums):
            pass
    print("rendered", len(nums), "->", OUT)


if __name__ == "__main__":
    main()
