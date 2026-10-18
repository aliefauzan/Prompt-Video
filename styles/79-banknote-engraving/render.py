"""Banknote (intaglio line engraving) restyle, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [all | frame numbers...]

Built like a steel-plate currency engraving printed in one green ink:
  LINES ONLY: every tone is made of fine engraved lines whose WIDTH carries the
    value (swelling where it is dark, thinning to a hair where it is light).
  FORM-FOLLOWING: the line field is bent by the smoothed brightness of the
    picture, so lines curve over cheeks, hair and folds like a burin following
    the form. People get a 35-degree hatch plus a cross-hatch in the darks;
    faces get a finer, tighter hatch; the room is a lighter horizontal wavy
    line field, like the vignette background of a bill.
  SECURITY PRINT: a pale guilloche rosette underprint and lathe-work wave lines
    sit in the paper behind everything; a guilloche border band with corner
    rosettes and a fictional "12" denomination frames the note.
  INK + PAPER: dark currency green on pale green-cream rag paper with fibres,
    a faint plate-tone wipe and a slight ink spread. Engraved lines are fixed
    to the plate (they do not boil); only ink density and wipe flicker a little.
"""
import json
import os
import sys
from multiprocessing import Pool
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FRAMES, MASKS, OUT = sys.argv[1:4]
ARGS = sys.argv[4:]
H, W = 1080, 1620
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
HERE = Path(__file__).resolve().parent
FACES = json.loads((HERE / "faces.json").read_text())

INK = np.array([38, 58, 22], np.float32) / 255       # BGR: dark currency green
PAPER = np.array([214, 238, 236], np.float32) / 255  # BGR: pale green-cream
UNDER = np.array([150, 200, 205], np.float32) / 255  # BGR: pale ochre-green underprint
BAND = 58


def frame_list():
    if not ARGS or ARGS == ["all"]:
        return list(range(1, 180))
    return [int(a) for a in ARGS]


def read(n):
    src = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png"))
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
    return src, m


def lines(angle, period, bend, cover, aa=0.10, wave=None):
    """Engraved line field. bend: per-pixel phase offset (in periods). cover: 0..1 ink."""
    a = np.deg2rad(angle)
    u = (xx * np.cos(a) + yy * np.sin(a)) / period + bend
    if wave is not None:
        u = u + wave
    f = 0.5 + 0.5 * np.cos(2 * np.pi * u)              # 1 on the line centre
    # line width grows with cover: ink where f > 1 - cover'
    thr = 1 - np.clip(cover, 0, 0.97) ** 0.8
    return np.clip((f - thr) / aa + 0.5, 0, 1)


def _security():
    """Pale guilloche rosette underprint + lathe-work waves (static, part of the paper)."""
    cx, cy = W * 0.5, H * 0.52
    r = np.hypot(xx - cx, yy - cy)
    th = np.arctan2(yy - cy, xx - cx)
    ros = np.zeros((H, W), np.float32)
    for k, (m, amp, rr) in enumerate([(24, 18, 9.0), (36, 12, 7.0), (18, 26, 11.0)]):
        g = np.cos(2 * np.pi * (r + amp * np.sin(m * th + k)) / rr)
        ros = np.maximum(ros, np.clip((g - 0.86) / 0.1, 0, 1))
    ros *= np.clip(1 - r / (H * 0.9), 0, 1) ** 0.5
    lathe = np.zeros((H, W), np.float32)
    for k in range(3):
        g = np.cos(2 * np.pi * (yy + 14 * np.sin(2 * np.pi * xx / (210 + 40 * k) + k * 2.1)) / 9.0)
        lathe = np.maximum(lathe, np.clip((g - 0.9) / 0.08, 0, 1))
    return ros, lathe


ROSETTE, LATHE = _security()


def _fibres():
    rng = np.random.default_rng(3)
    f = cv2.GaussianBlur(rng.normal(0, 1, (H, W)).astype(np.float32), (0, 0), 0.7)
    f = cv2.GaussianBlur(f, (15, 1), 0) * 0.7 + f * 0.3
    blot = cv2.resize(rng.random((9, 14)).astype(np.float32), (W, H), interpolation=cv2.INTER_CUBIC)
    return f * 0.02 + (blot - 0.5) * 0.03


FIBRES = _fibres()


def _border():
    """Guilloche border band, corner rosettes, denomination and legend (ink alpha)."""
    s = 2
    img = Image.new("L", (W * s, H * s), 0)
    d = ImageDraw.Draw(img)
    lw = 2

    def rect(o, width):
        d.rectangle([o * s, o * s, (W - o) * s - 1, (H - o) * s - 1], outline=255, width=width)

    d.rectangle([6 * s, 6 * s, (W - 6) * s - 1, (H - 6) * s - 1], fill=255)
    d.rectangle([(BAND - 6) * s, (BAND - 6) * s, (W - BAND + 6) * s - 1, (H - BAND + 6) * s - 1], fill=0)
    rect(BAND, lw)
    # interlaced sine waves along every side of the band
    mid0, amp = 6 + (BAND - 12 - 6) / 2 + 2, (BAND - 12 - 6) / 2 - 3
    for k in range(5):
        ph = k * 2 * np.pi / 5
        t = np.arange(0, W, 1.5)
        for yb in (mid0, H - mid0):
            pts = [(x * s, (yb + amp * np.sin(2 * np.pi * x / 46 + ph)) * s) for x in t]
            d.line(pts, fill=0, width=lw)
        t = np.arange(0, H, 1.5)
        for xb in (mid0, W - mid0):
            pts = [((xb + amp * np.sin(2 * np.pi * y / 46 + ph)) * s, y * s) for y in t]
            d.line(pts, fill=0, width=lw)
    # corner rosettes with the denomination
    f_num = ImageFont.truetype("/System/Library/Fonts/Supplemental/Copperplate.ttc", 46 * s, index=1)
    R = 70
    for cx, cy in ((R + 2, R + 2), (W - R - 2, R + 2), (R + 2, H - R - 2), (W - R - 2, H - R - 2)):
        d.ellipse([(cx - R) * s, (cy - R) * s, (cx + R) * s, (cy + R) * s], fill=255)
        th = np.linspace(0, 2 * np.pi, 720)
        for k in range(6):
            rr = R - 8 - 9 * np.abs(np.sin(9 * th + k * np.pi / 6))
            pts = [((cx + r_ * np.cos(a)) * s, (cy + r_ * np.sin(a)) * s) for r_, a in zip(rr, th)]
            d.line(pts + pts[:1], fill=0, width=lw)
        d.ellipse([(cx - 32) * s, (cy - 32) * s, (cx + 32) * s, (cy + 32) * s], fill=0, outline=255, width=3 * s)
        d.text((cx * s, cy * s + 2 * s), "12", fill=255, font=f_num, anchor="mm")
    # legend plaques on the bottom band
    f_txt = ImageFont.truetype("/System/Library/Fonts/Supplemental/Copperplate.ttc", 28 * s, index=1)
    for txt, cx in (("TWELVE FRAMES", W * 0.27), ("ONE SECOND", W * 0.73)):
        tw = d.textlength(txt, font=f_txt) / s
        d.rectangle([(cx - tw / 2 - 14) * s, (H - BAND + 2) * s, (cx + tw / 2 + 14) * s, (H - 8) * s], fill=255)
        d.text((cx * s, (H - BAND / 2 - 3) * s), txt, fill=0, font=f_txt, anchor="mm")
    img = img.resize((W, H), Image.LANCZOS)
    return np.asarray(img, np.float32) / 255


BORDER = _border()
CLAHE = cv2.createCLAHE(clipLimit=2.2, tileGridSize=(6, 9))


def face_mask(n):
    fm = np.zeros((H, W), np.uint8)
    for f in FACES.get(f"frame_{n:03d}.png", []):
        x, y, w, h = f["box"]
        pts = [tuple(p) for p in f.get("faceContour", [])]
        pts += [(x + 0.12 * w, y - 0.12 * h), (x + 0.88 * w, y - 0.12 * h)]
        hull = cv2.convexHull(np.array(pts, np.float32)).astype(np.int32)
        cv2.fillPoly(fm, [hull], 255, cv2.LINE_AA)
    return cv2.GaussianBlur(fm.astype(np.float32) / 255, (0, 0), 5)


def render(n):
    src, mask = read(n)
    rng = np.random.default_rng(n)
    g = CLAHE.apply(cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)).astype(np.float32) / 255
    g = cv2.bilateralFilter(g, 9, 0.10, 5)
    m = cv2.GaussianBlur(mask, (0, 0), 1.5)
    fm = cv2.GaussianBlur(face_mask(n), (0, 0), 8) * m

    # value for the people: contrasty, faces kept light and open
    t = 1 - g
    t = np.clip((t - 0.16) / 0.66, 0, 1) ** 1.1
    t = t * (1 - 0.15 * fm)
    ts = cv2.GaussianBlur(t, (0, 0), 1.2)
    bend = cv2.GaussianBlur(g, (0, 0), 7) * 2.6          # lines curve over the form

    hatch = lines(35, 8.0, bend, 0.03 + 0.92 * ts)
    cross = lines(-40, 8.4, bend * 0.8, np.clip((ts - 0.5) / 0.5, 0, 1) * 0.75) * (ts > 0.5)
    third = lines(80, 8.8, bend * 0.6, np.clip((ts - 0.8) / 0.2, 0, 1) * 0.7) * (ts > 0.8)
    people = np.maximum(np.maximum(hatch, cross), third)

    # contour line: thin engraved outline from edges + a firm silhouette
    a = cv2.GaussianBlur(g, (0, 0), 1.2)
    b = cv2.GaussianBlur(g, (0, 0), 1.9)
    edge = np.clip(-(a - 0.985 * b + 0.01) * 50, 0, 1) * 0.8
    a2 = cv2.GaussianBlur(g, (0, 0), 0.9)
    b2 = cv2.GaussianBlur(g, (0, 0), 1.5)
    edge = np.maximum(edge, np.clip(-(a2 - 0.99 * b2 + 0.006) * 70, 0, 1) * fm)   # eyes, brows, lips
    sil = cv2.morphologyEx((m > 0.5).astype(np.uint8), cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8)).astype(np.float32)
    people = np.maximum(people, np.maximum(edge, cv2.GaussianBlur(sil, (0, 0), 0.7)))

    # background: lighter horizontal wavy line field (the bill's vignette ground)
    gb = cv2.GaussianBlur(g, (0, 0), 2.5)
    tb = np.clip((1 - gb - 0.25) / 0.75, 0, 1) ** 1.5
    wave = 0.35 * np.sin(2 * np.pi * xx / 420)
    bg = lines(90, 6.5, cv2.GaussianBlur(gb, (0, 0), 10) * 0.8, 0.04 + 0.75 * tb, wave=wave)
    eb = cv2.GaussianBlur(gb, (0, 0), 1.5)
    bg = np.maximum(bg, np.clip(-(eb - 0.985 * cv2.GaussianBlur(gb, (0, 0), 3) + 0.012) * 35, 0, 1) * 0.55)

    ink = people * m + bg * (1 - m)

    # ink spread + per-print density flicker
    ink = cv2.GaussianBlur(ink, (0, 0), 0.55)
    dens = 0.94 + 0.03 * rng.random()
    # paper with security underprint and plate-tone wipe
    wipe = cv2.resize(rng.random((4, 6)).astype(np.float32), (W, H), interpolation=cv2.INTER_CUBIC)
    paper = PAPER[None, None] * (1 + FIBRES)[..., None]
    under = np.clip(ROSETTE * 0.10 + LATHE * 0.05, 0, 1) * (1 - m * 0.9)
    paper = paper * (1 - under[..., None]) + UNDER * under[..., None] * 0.92 + 0 * paper
    paper = paper * (1 - 0.035 * wipe[..., None])
    a_ink = np.clip(np.maximum(ink * dens, BORDER), 0, 1)[..., None]
    out = paper * (1 - a_ink) + INK[None, None] * a_ink
    out = (np.clip(out, 0, 1) * 255).astype(np.uint8)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), out)
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    with Pool(4) as p:
        for n in p.imap_unordered(render, frame_list()):
            print(n, end=" ", flush=True)
    print()
