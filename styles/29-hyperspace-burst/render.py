"""Hyperspace Burst: radial light-speed streak burst with prism fringe, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [frame numbers...]

Every frame is pulled outward from a burst centre on the main subject's face.
The background is radially zoom-smeared and blown out toward white. The
people are repeated as discrete echo copies pushed outward along the burst and
darken-stacked, so hair and clothing leave inky stepped outlines; each copy
splits blue/green/red by zoom (prism fringe). The lead copy stays sharp near
the centre and goes translucent further out. Burst strength pulses per frame.
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np

FRAMES, MASKS, OUT = sys.argv[1:4]
ONLY = [int(a) for a in sys.argv[4:]] or [13, 49, 85, 109, 145, 178]

SAMPLES = 18
ECHOES = 7                      # discrete subject copies pushed outward along the burst
PRISM = (1.10, 1.0, 0.90)       # B, G, R zoom ratio: channels split at the far echoes


def zoom(img, c, s):
    M = np.float32([[s, 0, c[0] * (1 - s)], [0, s, c[1] * (1 - s)]])
    return cv2.warpAffine(img, M, (img.shape[1], img.shape[0]), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


def burst_centre(m, w, h):
    """Face of the main subject: biggest, most central person blob, top of its silhouette."""
    m = cv2.resize(m, (w // 4, h // 4), interpolation=cv2.INTER_AREA)
    w, h = w // 4, h // 4
    num, lab, stats, cents = cv2.connectedComponentsWithStats((m > 0.5).astype(np.uint8))
    if num < 2:
        return w / 2, h * 0.4
    best, score = 1, -1.0
    for k in range(1, num):
        area = stats[k, cv2.CC_STAT_AREA]
        sc = area * (1.15 - abs(cents[k][0] - w / 2) / w)
        if sc > score:
            best, score = k, sc
    ys, xs = np.nonzero(lab == best)
    top = ys < np.percentile(ys, 22)
    return float(np.median(xs[top])) * 4, float(np.percentile(ys, 14)) * 4


def load_mask(n):
    return cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), 0).astype(np.float32) / 255


def smoothed_centres():
    """Burst centre per frame over the whole clip, median + Gaussian filtered in time so
    the burst glides with the main face instead of jumping between people."""
    n_all = len([f for f in os.listdir(MASKS) if f.endswith(".png")])
    raw = []
    for n in range(1, n_all + 1):
        m = load_mask(n)
        raw.append(burst_centre(m, m.shape[1], m.shape[0]))
    raw = np.array(raw, np.float32)
    k = 4
    pad = np.pad(raw, ((k, k), (0, 0)), mode="edge")
    med = np.array([np.median(pad[i:i + 2 * k + 1], 0) for i in range(len(raw))])
    sm = cv2.GaussianBlur(med.reshape(-1, 1, 2), (1, 0), sigmaX=0, sigmaY=2.0).reshape(-1, 2)
    return {n + 1: tuple(sm[n]) for n in range(len(raw))}


CENTRES = {}


def init(c):
    CENTRES.update(c)


def render(n):
    rng = np.random.default_rng(4000 + n)
    img = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png")).astype(np.float32) / 255
    m = load_mask(n)
    h, w = m.shape
    cx, cy = CENTRES[n]
    c = (cx + rng.normal(0, 4), cy + rng.normal(0, 4))
    smax = 1.0 + rng.uniform(0.26, 0.36)          # burst pulses frame to frame

    # background: radial zoom streak, then blown out toward white (the light-speed flash)
    acc = np.zeros_like(img)
    wsum = 0.0
    for i in range(SAMPLES):
        t = i / (SAMPLES - 1)
        wt = np.exp(-1.5 * t)
        acc += zoom(img, c, 1 + (smax - 1) * 1.6 * t) * wt
        wsum += wt
    bg = acc / wsum
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    r = np.sqrt((xx - c[0]) ** 2 + (yy - c[1]) ** 2) / np.hypot(w, h)
    flash = np.clip(0.55 + r * 0.9, 0, 0.93)[..., None] * rng.uniform(0.92, 1.0)
    field = 1 - (1 - bg) * (1 - flash)

    # subject: discrete echo copies pushed outward from the centre, darken-stacked so
    # the darks of clothing and hair repeat as inky outlines; each copy splits R/G/B (prism)
    ms = cv2.GaussianBlur(m, (0, 0), 2.0)[..., None]
    subj = img * ms + field * (1 - ms)
    for k in range(ECHOES, 0, -1):
        t = k / ECHOES
        fade = 0.10 + 0.55 * t                           # far echoes are paler
        layer = np.empty_like(img)
        for ch in range(3):
            sc = 1 + (smax - 1) * t * PRISM[ch]
            layer[..., ch] = zoom(subj[..., ch], c, sc)
        layer = layer + (1 - layer) * fade
        field = np.minimum(field, layer)
    # streaky smear between the echoes so they read as motion, not copies
    sm = np.zeros_like(img)
    for i in range(SAMPLES):
        t = i / (SAMPLES - 1)
        sm += zoom(subj, c, 1 + (smax - 1) * t)
    sm /= SAMPLES
    field = np.minimum(field, sm + (1 - sm) * 0.2)

    # lead copy on top: the person stays sharp near the burst centre, softer further out
    core = np.clip(1 - (r - 0.05) / 0.20, 0, 1)[..., None]
    al = ms * (0.15 + 0.80 * core)
    out = field * (1 - al) + img * al
    # prism fringe on the lead edge
    edge = np.clip(cv2.morphologyEx(m, cv2.MORPH_GRADIENT, np.ones((5, 5), np.uint8)), 0, 1)
    edge = cv2.GaussianBlur(edge, (0, 0), 3)[..., None]
    fringe = np.stack([zoom(out[..., 0], c, 1.012), out[..., 1], zoom(out[..., 2], c, 0.99)], -1)
    out = out * (1 - edge) + fringe * edge
    bloom = cv2.GaussianBlur(np.clip(out - 0.8, 0, 1), (0, 0), 20)
    out = out + bloom * 0.5

    # slight contrast so the subject's darks stay inky against the white-out
    out = np.clip(out, 0, 1)
    out = np.clip((out - 0.05) / 0.97, 0, 1) ** 1.08
    out += rng.normal(0, 0.01, out.shape).astype(np.float32)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), (out.clip(0, 1) * 255).astype(np.uint8))
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    centres = smoothed_centres()
    with Pool(min(6, os.cpu_count() or 2), initializer=init, initargs=(centres,)) as p:
        for n in p.imap_unordered(render, ONLY):
            print("frame", n)
