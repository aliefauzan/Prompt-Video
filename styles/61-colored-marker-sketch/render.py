"""Colored Marker Sketch — local approximation of the frame-by-frame restyle.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [all | 13 49 85 ...]

Per frame (re-drawn on twos — the seed changes every 2 frames, so lines and
strokes "boil" like a hand-drawn animation at 12 fps):
  1. warm sketchbook paper with tooth.
  2. alcohol-marker fills, multiply-blended like real marker ink:
       * a light base tone laid in long diagonal chisel strokes (about -30 deg)
         that overlap, so the overlaps read as darker streak bands;
       * a darker shadow tone in the dark areas, strokes at a steeper angle;
       * highlights are left as bare paper, fills stop short of / overshoot the
         lines, and the room fades out toward the frame edges (unfinished
         sketch), while the people are fully coloured.
  3. coloured-pencil work: XDoG linework from the photo plus a stronger
     silhouette contour from the person mask, in warm sepia/indigo pencil,
     broken by the paper tooth, with a faint doubled construction line;
     loose diagonal hatching in the shadows.
"""
import math
import sys
from pathlib import Path

import cv2
import numpy as np

W, H = 1620, 1080
PAPER = np.array([250, 247, 240], np.float32)


def tooth():
    rng = np.random.default_rng(11)
    g = rng.random((H, W)).astype(np.float32)
    g = cv2.GaussianBlur(g, (0, 0), 0.7)
    return (g - g.min()) / (g.max() - g.min())


TOOTH = tooth()


def streaks(rng, angle, width, spacing, seg=(160, 520), gap=(0, 40)):
    """Marker strokes as an ink-count field: 0 = paper, 1 = one stroke, 2 = two overlapping.

    Neighbouring rows go to alternate layers, so where a stroke is wider than the
    row spacing it overlaps the next one and the overlap gets a second coat of ink.
    """
    layers = [np.zeros((H, W), np.uint8), np.zeros((H, W), np.uint8)]
    ca, sa = math.cos(angle), math.sin(angle)
    diag = math.hypot(W, H)
    v = -diag / 2 + rng.uniform(0, spacing)
    row = 0
    while v < diag / 2:
        layer = layers[row % 2]
        t = -diag / 2 + rng.uniform(-200, 0)
        while t < diag / 2:
            L = rng.uniform(*seg)
            vv = v + rng.normal(0, width * 0.1)
            dv = rng.normal(0, 4)
            x0, y0 = W / 2 + t * ca - vv * sa, H / 2 + t * sa + vv * ca
            x1, y1 = W / 2 + (t + L) * ca - (vv + dv) * sa, H / 2 + (t + L) * sa + (vv + dv) * ca
            cv2.line(layer, (int(x0), int(y0)), (int(x1), int(y1)), 255, int(width * rng.uniform(0.7, 1.15)), cv2.LINE_AA)
            t += L + rng.uniform(*gap)
        v += spacing * rng.uniform(0.8, 1.25)
        row += 1
    return (layers[0].astype(np.float32) + layers[1].astype(np.float32)) / 255


def xdog(gray, sigma=1.1, k=1.6, p=22, eps=-0.02, phi=12):
    g1 = cv2.GaussianBlur(gray, (0, 0), sigma)
    g2 = cv2.GaussianBlur(gray, (0, 0), sigma * k)
    d = (1 + p) * g1 - p * g2
    e = np.where(d >= eps, 1.0, 1 + np.tanh(phi * (d - eps)))
    return 1 - np.clip(e, 0, 1)            # 1 = line


def warp(a, rng, amp, sig):
    nx = cv2.GaussianBlur(rng.normal(0, 1, (H // 4, W // 4)).astype(np.float32), (0, 0), sig)
    ny = cv2.GaussianBlur(rng.normal(0, 1, (H // 4, W // 4)).astype(np.float32), (0, 0), sig)
    nx = cv2.resize(nx, (W, H)) * amp / (nx.std() + 1e-6)
    ny = cv2.resize(ny, (W, H)) * amp / (ny.std() + 1e-6)
    gy, gx = np.mgrid[0:H, 0:W].astype(np.float32)
    return cv2.remap(a, gx + nx, gy + ny, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)


def marker_layer(img, cov, col, rng, angle, width, spacing, alpha):
    """Multiply one marker colour over img inside cov, as overlapping chisel strokes."""
    st = streaks(rng, angle, width, spacing)
    a = np.clip(cov * alpha, 0, 1)[..., None]
    coat = 1 - a * (1 - col)                     # one coat of this marker
    return img * coat ** st[..., None]


def render(frame, mask, n):
    rng = np.random.default_rng(300 + n // 2)
    small = cv2.resize(frame, (W // 3, H // 3), interpolation=cv2.INTER_AREA)
    small = cv2.pyrMeanShiftFiltering(small, 6, 24)
    small = cv2.bilateralFilter(small, 7, 30, 5)
    sm = cv2.resize(small, (W, H), interpolation=cv2.INTER_CUBIC).astype(np.float32)
    # marker colours: clean, saturated, light enough to stack (multiply)
    hsv = cv2.cvtColor(np.clip(sm, 0, 255).astype(np.uint8), cv2.COLOR_RGB2HSV).astype(np.float32)
    hsv[..., 1] = np.clip(hsv[..., 1] * 1.05 + 6, 0, 255)
    hsv[..., 2] = np.clip(hsv[..., 2] * 0.3 + 182, 0, 255)
    col = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB).astype(np.float32) / 255
    lum = cv2.GaussianBlur(sm.mean(2) / 255, (0, 0), 1.5)
    m = cv2.GaussianBlur(mask, (0, 0), 2)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    # people fully coloured; the room only loosely, fading to bare paper at the edges
    edge = np.clip(1.0 - (((xx - W / 2) / (W * 0.55)) ** 2 + ((yy - H * 0.45) / (H * 0.6)) ** 2) ** 1.5, 0, 1)
    reach = warp(np.maximum(m, 0.5 * edge), rng, 9, 3)
    step = lambda t, s=14: np.clip((t - lum) * s, 0, 1)
    img = np.ones((H, W, 3), np.float32) * PAPER
    # 1st pass: light tone everywhere but the highlights (left as paper)
    img = marker_layer(img, warp(step(0.80) * reach, rng, 6, 2), col, rng, -0.55 + rng.normal(0, 0.03), 46, 34, 0.62)
    # 2nd pass: same marker again in the mid-shadows, steeper strokes -> darker
    img = marker_layer(img, warp(step(0.45) * reach, rng, 6, 2), col, rng, -1.0 + rng.normal(0, 0.04), 36, 27, 0.6)
    # 3rd pass: a darker cool-grey marker in the deepest darks
    grey = np.array([0.62, 0.60, 0.66], np.float32) * 0.7 + col * 0.3
    img = marker_layer(img, warp(step(0.28) * np.maximum(m, 0.35 * edge), rng, 5, 2), grey, rng, -0.62, 28, 24, 0.85)
    img = marker_layer(img, warp(step(0.15) * np.maximum(m, 0.3 * edge), rng, 5, 2), grey * 0.8, rng, -0.3, 24, 22, 0.7)
    # coloured-pencil hatching in the shadows, broken by the paper tooth
    ha = 0.8 + rng.normal(0, 0.05)
    hv = (xx * math.cos(ha) + yy * math.sin(ha) + rng.uniform(0, 8)) % 8
    hatch = np.clip(1 - np.abs(hv - 4) / 0.9, 0, 1)
    hcov = warp(step(0.46, 4) * np.maximum(m, 0.5 * edge), rng, 6, 2)
    h_ = hatch * hcov * (TOOTH > 0.3) * 0.5
    hcol = np.where(m[..., None] > 0.5, np.array([110, 54, 58]), np.array([72, 80, 128])).astype(np.float32)
    img = img * (1 - h_[..., None]) + hcol * h_[..., None]
    # linework: XDoG + silhouette contour, wobbly, broken by tooth, doubled faintly
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255
    gray = cv2.bilateralFilter(gray, 7, 0.12, 4)
    lines = np.maximum(xdog(gray, sigma=0.9), 0.8 * xdog(gray, sigma=1.8)) * np.maximum(m, 0.2 + 0.55 * edge)
    contour = cv2.morphologyEx((mask > 0.5).astype(np.uint8), cv2.MORPH_GRADIENT, np.ones((4, 4), np.uint8)).astype(np.float32)
    contour = cv2.GaussianBlur(contour, (0, 0), 0.8) * 1.6
    ln = np.clip(np.maximum(lines, contour), 0, 1)
    ln1 = warp(ln, rng, 1.4, 4)
    ln2 = warp(ln, rng, 3.5, 6) * 0.3
    pencil = np.clip(np.maximum(ln1, ln2) * (0.5 + 0.7 * TOOTH), 0, 1)
    lcol = np.where(m[..., None] > 0.5, np.array([58, 34, 30]), np.array([62, 64, 96])).astype(np.float32)
    img = img * (1 - pencil[..., None] * 0.9) + lcol * pencil[..., None] * 0.9
    # paper tooth shows through everything (matte)
    img = img * (0.95 + 0.07 * TOOTH[..., None])
    return np.clip(img, 0, 255).astype(np.uint8)


def main():
    fdir, mdir, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    out.mkdir(parents=True, exist_ok=True)
    args = sys.argv[4:] or ["13", "49", "85", "109", "145", "178"]
    nums = list(range(1, 180)) if args == ["all"] else [int(a) for a in args]
    for n in nums:
        f = cv2.cvtColor(cv2.imread(str(fdir / f"frame_{n:03d}.png")), cv2.COLOR_BGR2RGB)
        m = cv2.imread(str(mdir / f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
        img = render(f, m, n)
        cv2.imwrite(str(out / f"frame_{n:03d}.png"), cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
        print(n, end=" ", flush=True)
    print()


if __name__ == "__main__":
    main()
