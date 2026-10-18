"""Pixel Sort Glitch, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [all | frame numbers...]

Per frame (Kim Asendorf's ASDF "brightness mode", vertical):
  * every pixel column is split into intervals: runs of pixels inside a
    luminance band (the window, wall, plants, wood, clothes), broken at the
    person-mask boundary and at random break points
  * inside each interval the pixels are sorted by luminance, brightest at the
    top, so those areas melt down into smooth vertical gradient drips with
    hard ends, while near-black areas (hair, the TV frame, the chair, deep
    shadows) stay intact
  * on the people only the brighter half is sorted (cream stripes, light
    fabric, highlights), and faces (Apple Vision boxes from faces.json, made
    by faces.swift) are protected as solid ellipses, so identity holds while
    clothes and the room drip around them
  * the random interval breaks are re-drawn every frame, so the sorted streaks
    shimmer and re-cut themselves like real pixel-sort video
"""
import json
import os
import sys
from pathlib import Path

import cv2
import numpy as np

FRAMES, MASKS, OUT = sys.argv[1:4]
ARGS = sys.argv[4:]
N = len([f for f in os.listdir(FRAMES) if f.startswith("frame_") and f.endswith(".png")])
BAND = (52, 252)       # room: sort every pixel whose luminance is inside this band
P_BAND = (138, 252)    # people: only the brighter half (cream stripes, light fabric, highlights)
MEAN_RUN = 700         # mean interval length before a random break (px)
HERE = Path(__file__).resolve().parent
FACES = json.loads((HERE / "faces.json").read_text())   # Apple Vision boxes (faces.swift)


def face_boxes(n):
    """Face boxes for frame n, falling back to the nearest frame with faces
    (Vision misses a face now and then), so protection never blinks off."""
    for d in (0, -1, 1, -2, 2, -3, 3):
        f = FACES.get(f"frame_{n + d:03d}.png")
        if f:
            return [x["box"] for x in f]
    return []


def load(n):
    img = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png"))
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE)
    return img, m


def render(n):
    img, m8 = load(n)
    H, W = m8.shape
    rng = np.random.default_rng(1000 + n)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lum = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)
    lum = cv2.GaussianBlur(lum, (0, 0), 1.2)           # cleaner interval edges
    person = cv2.morphologyEx((m8 > 127).astype(np.uint8), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8)) > 0

    # faces are never sorted: a solid ellipse over each Vision face box
    # (forehead to chin, ear to ear) so eyes, glasses and mouth stay intact
    face = np.zeros((H, W), np.uint8)
    for x, y, w, h in face_boxes(n):
        cv2.ellipse(face, (int(x + w / 2), int(y + h * 0.45)), (int(w * 0.68), int(h * 0.80)), 0, 0, 360, 1, -1)
    face = (face > 0) & person
    room_band = (lum > BAND[0]) & (lum < BAND[1])
    person_band = (lum > P_BAND[0]) & (lum < P_BAND[1])
    inb = np.where(person, person_band, room_band) & ~face

    # work column-wise: transpose so each column is a contiguous row
    T = np.ascontiguousarray(img.transpose(1, 0, 2))
    key = lum.T
    ib = inb.T
    pm = (person.astype(np.uint8) + face).T
    start = np.ones_like(ib)
    start[:, 1:] = (~ib[:, 1:]) | (~ib[:, :-1]) | (pm[:, 1:] != pm[:, :-1])
    # random breaks, but with a per-column bias so neighbouring columns differ
    col_len = MEAN_RUN * rng.uniform(0.35, 1.6, size=(W, 1))
    start |= rng.random((W, H)) < (1.0 / col_len)
    start[:, 0] = True
    seg = np.cumsum(start.ravel()).astype(np.float64)
    order = np.argsort(seg + (1.0 - key.ravel() / 256.0) * 0.999, kind="stable")
    sorted_T = T.reshape(-1, 3)[order].reshape(W, H, 3)
    out = sorted_T.transpose(1, 0, 2)

    # a touch of digital crispness: slight contrast on sorted areas only
    o = out.astype(np.float32)
    o = np.where(inb[..., None], np.clip((o - 128) * 1.08 + 128, 0, 255), o)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), o.astype(np.uint8))
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    todo = range(1, N + 1) if not ARGS or ARGS == ["all"] else [int(a) for a in ARGS]
    for n in todo:
        render(n)
        print(n, end=" ", flush=True)
    print()
