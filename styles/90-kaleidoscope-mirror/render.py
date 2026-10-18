"""Kaleidoscope Mirror, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [all | frame numbers...]

Per frame:
  * the WHOLE source frame (people included) is folded through a polar mirror
    remap into an 8-fold mandala (16 mirrored wedges) centred above the middle
    of the frame; the mandala turns slowly and the source wedge drifts, so the
    pattern keeps changing like a real tube kaleidoscope being rotated
  * alternate wedges are slightly darker and cooler (each mirror bounce loses
    light), the wedge seams get a thin bright glass edge, rings of the tube
    fall off into a dark round vignette
  * colour is pushed rich and jewel-like
  * the real people are laid back on top from the masks, exact, with a soft
    contact shadow so they stand in front of the mandala
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np

FRAMES, MASKS, OUT = sys.argv[1:4]
ARGS = sys.argv[4:]
N = len([f for f in os.listdir(FRAMES) if f.startswith("frame_") and f.endswith(".png")])
W, H = 1620, 1080
FOLD = 8                      # 8-fold symmetry -> 16 mirrored wedges
SEG = np.pi / FOLD            # angle of one mirrored wedge
CX, CY = W * 0.5, H * 0.40    # mandala centre in the output frame

YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)
DX, DY = XX - CX, YY - CY
R = np.sqrt(DX * DX + DY * DY)
TH = np.arctan2(DY, DX)


def load(n):
    img = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png")).astype(np.float32) / 255
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
    return img, m


def saturate(img, s, c):
    hsv = cv2.cvtColor(np.clip(img, 0, 1), cv2.COLOR_BGR2HSV)
    hsv[..., 1] = np.clip(hsv[..., 1] * s + 0.06, 0, 1)
    v = hsv[..., 2]
    hsv[..., 2] = np.clip(v + c * (v - 0.5) * (1 - np.abs(2 * v - 1)), 0, 1)
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)


def mandala(img, t):
    rot = 0.030 * t                                   # whole mandala turns ~1.7 deg / frame
    phi = np.mod(TH - rot, 2 * SEG)
    flip = phi > SEG                                  # odd wedges are mirror images
    phi = np.where(flip, 2 * SEG - phi, phi)
    # radial breathing + slow zoom so the petals flow outward a little
    zoom = 0.78 + 0.06 * np.sin(t * 0.05)
    rr = R * zoom
    # source wedge: starts on the centre person's face and sweeps slowly from
    # the right person through the striped shirt to the batik on the left
    alpha = np.pi / 2 - 1.25 * np.cos(t * 0.022)
    sx = W * (0.5 + 0.04 * np.sin(t * 0.017))
    sy = H * (0.36 + 0.03 * np.cos(t * 0.013))
    mx = (sx + rr * np.cos(phi + alpha)).astype(np.float32)
    my = (sy + rr * np.sin(phi + alpha)).astype(np.float32)
    k = cv2.remap(img, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)
    # every mirror bounce loses a little light and picks up a cool cast
    k = np.where(flip[..., None], k * np.array([1.0, 0.95, 0.90], np.float32) * 0.9, k)
    # bright glass edges on the wedge seams
    ang = np.mod(TH - rot, SEG)
    dist = np.minimum(ang, SEG - ang) * np.maximum(R, 1)   # px distance to nearest seam
    seam = np.exp(-(dist / 1.1) ** 2) * np.clip(R / 60, 0, 1)
    glow = np.exp(-(dist / 7.0) ** 2) * np.clip(R / 60, 0, 1)
    k = k + seam[..., None] * 0.45 + glow[..., None] * np.array([0.10, 0.08, 0.06], np.float32)
    # concentric "tube" falloff: the mirrored image dims ring by ring outward
    ring = 0.5 + 0.5 * np.cos(R / 340 * 2 * np.pi)
    k = k * (0.88 + 0.12 * ring[..., None])
    # bright jewel centre
    core = np.exp(-(R / 26) ** 2)
    k = k + core[..., None] * 0.6
    return k


def render(n):
    rng = np.random.default_rng(9000 + n)
    img, m = load(n)
    t = float(n)
    # tame the blown window so the mandala stays jewel-coloured, not white
    src = saturate(img, 1.6, 0.35)
    v = src.max(2, keepdims=True)
    src = src * (1 - 0.35 * np.clip((v - 0.75) / 0.25, 0, 1))
    k = mandala(src, t)
    # round eyepiece vignette
    vr = R / (0.62 * W)
    k = k * np.clip(1.15 - vr ** 2.2, 0.08, 1)[..., None]
    # people in front: exact pixels, tiny lift in saturation so they match the mandala
    subj = saturate(img, 1.12, 0.10)
    ms = cv2.GaussianBlur(m, (0, 0), 1.6)[..., None]
    sh = cv2.GaussianBlur(cv2.dilate(m, np.ones((9, 9), np.uint8)), (0, 0), 14)[..., None]
    k = k * (1 - 0.45 * sh)
    out = subj * ms + k * (1 - ms)
    out = np.clip(out, 0, 1)
    out = (out * 255 + rng.random(out.shape) - 0.5).clip(0, 255).astype(np.uint8)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), out)
    return n


def main():
    os.makedirs(OUT, exist_ok=True)
    nums = list(range(1, N + 1)) if (not ARGS or ARGS == ["all"]) else [int(a) for a in ARGS]
    with Pool(4) as p:
        for _ in p.imap_unordered(render, nums):
            pass
    print("rendered", len(nums), "->", OUT)


if __name__ == "__main__":
    main()
