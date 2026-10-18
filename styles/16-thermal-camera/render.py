"""Thermal camera / infrared heat-map restyle, frame by frame.

usage: python -I render.py [frame numbers... | all]   (default: the six sheet frames)
       RENDER_OUT=/tmp/prompt-video-render/<slug> python -I render.py all   -> full clip for make_video.py
Reads ../../_source/frames + ../../_source/masks, writes ./frames/frame_NNN.png.
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "..", "_source")
FRAMES, MASKS, OUT = os.path.join(SRC, "frames"), os.path.join(SRC, "masks"), os.path.join(HERE, "frames")
OUT = os.environ.get("RENDER_OUT", OUT)        # e.g. /tmp/prompt-video-render/<slug> for the full clip
ONLY = (list(range(1, 180)) if sys.argv[1:] == ["all"] else [int(a) for a in sys.argv[1:]]) or [13, 49, 85, 109, 145, 178]

T_MIN, T_MAX = 17.0, 38.5          # temperature span of the colour scale, deg C


def ramp(stops):
    """List of (pos, (r,g,b)) -> 256x3 BGR float LUT."""
    xs = np.array([s[0] for s in stops])
    cols = np.array([s[1] for s in stops], np.float32) / 255
    t = np.linspace(0, 1, 256)
    lut = np.stack([np.interp(t, xs, cols[:, i]) for i in range(3)], 1)
    return lut[:, ::-1].astype(np.float32)


PALETTES = {
    "iron": ramp([(0, (0, 0, 10)), (0.13, (20, 0, 90)), (0.3, (110, 0, 150)), (0.45, (190, 20, 110)),
                  (0.6, (235, 80, 30)), (0.75, (255, 150, 0)), (0.9, (255, 225, 60)), (1, (255, 255, 235))]),
    "rainbow": ramp([(0, (10, 0, 60)), (0.15, (30, 20, 200)), (0.32, (0, 160, 255)), (0.47, (0, 220, 120)),
                     (0.6, (180, 240, 0)), (0.72, (255, 210, 0)), (0.85, (255, 70, 0)), (0.95, (230, 0, 30)),
                     (1, (255, 230, 230))]),
    "whitehot": ramp([(0, (8, 8, 10)), (0.5, (110, 110, 112)), (1, (250, 250, 245))]),
}

# (first, last, palette)
SECTIONS = [(1, 36, "iron"), (37, 72, "rainbow"), (73, 100, "iron"), (101, 128, "whitehot"),
            (129, 160, "rainbow"), (161, 999, "iron")]


def section_of(n):
    for s in SECTIONS:
        if s[0] <= n <= s[1]:
            return s
    return SECTIONS[-1]


def vnoise(rng, h, w, cell):
    a = rng.random((max(2, h // cell + 2), max(2, w // cell + 2))).astype(np.float32)
    return cv2.resize(a, (w, h), interpolation=cv2.INTER_CUBIC).clip(0, 1)


def heat_field(bgr, mask, rng):
    """Map the photo to a 0..1 'temperature' field: people hot, skin hottest, room cold."""
    h, w = mask.shape
    f = bgr.astype(np.float32) / 255
    lum = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
    ycc = cv2.cvtColor(bgr, cv2.COLOR_BGR2YCrCb).astype(np.float32)
    cr, cb = ycc[..., 1], ycc[..., 2]
    skin = ((cr > 135) & (cr < 175) & (cb > 85) & (cb < 130) & (ycc[..., 0] > 60)).astype(np.float32)
    skin = cv2.GaussianBlur(cv2.morphologyEx(skin, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8)), (0, 0), 14)
    skin = np.clip((skin - 0.35) / 0.4, 0, 1)                   # big solid skin areas survive, fabric stripes average out
    m = cv2.GaussianBlur(mask, (0, 0), 3)
    skin *= m
    # room: cold, walls slightly warmer where lit, screen + ceiling lights warm
    room = 0.05 + 0.20 * cv2.GaussianBlur(lum, (0, 0), 12)
    bright = cv2.GaussianBlur((lum > 0.93).astype(np.float32), (0, 0), 10)
    room += 0.25 * bright
    sat = f.max(2) - f.min(2)
    room += 0.06 * cv2.GaussianBlur(sat, (0, 0), 8)
    room += (vnoise(rng, h, w, 260) - 0.5) * 0.03
    # body: clothes warm, skin hot, dark hair a bit cooler, core of the body hottest
    core = cv2.GaussianBlur(cv2.erode(mask, np.ones((25, 25), np.uint8)), (0, 0), 40)
    body = 0.50 + 0.12 * core + 0.04 * (cv2.GaussianBlur(lum, (0, 0), 14) - 0.4)
    body = body * (1 - skin) + (0.80 + 0.18 * cv2.GaussianBlur(lum, (0, 0), 2)) * skin
    hair = cv2.GaussianBlur(((lum < 0.16) & (mask > 0.5)).astype(np.float32), (0, 0), 4)
    body -= 0.10 * hair * (1 - skin)
    heat = room * (1 - m) + body * m
    # thermal halo: bodies warm the air right around them
    halo = cv2.GaussianBlur(m, (0, 0), 28)
    heat = np.maximum(heat, 0.10 + 0.32 * halo)
    # microbolometer optics: low resolution, soft
    small = cv2.resize(heat, (w // 5, h // 5), interpolation=cv2.INTER_AREA)
    heat = cv2.resize(small, (w, h), interpolation=cv2.INTER_CUBIC)
    # MSX-style edge detail: a faint visible-light edge layer embossed in
    edges = cv2.Laplacian(cv2.GaussianBlur(lum, (0, 0), 1.6), cv2.CV_32F, ksize=3)
    emask = 0.35 + 0.65 * skin                                  # faces keep their features, fabric detail fades
    heat += np.clip(edges, -0.2, 0.2) * 0.28 * emask
    return heat.clip(0, 1), skin


def sensor_noise(rng, h, w, n):
    fpn = np.random.default_rng(7).normal(0, 1, (1, w)).astype(np.float32)        # fixed column pattern
    fpn = cv2.GaussianBlur(fpn, (0, 0), 0.8) * 0.010
    temporal = cv2.GaussianBlur(rng.normal(0, 1, (h // 2, w // 2)).astype(np.float32), (0, 0), 0.7)
    temporal = cv2.resize(temporal, (w, h), interpolation=cv2.INTER_LINEAR) * 0.022
    drift = 0.012 * np.sin(n * 0.37) + rng.normal(0, 0.004)                        # AGC breathing
    return fpn + temporal + drift


FONT = cv2.FONT_HERSHEY_SIMPLEX
MONO = cv2.FONT_HERSHEY_PLAIN


def put(img, txt, org, sc=1.0, th=2, col=(255, 255, 255)):
    sc *= 1.35
    th += 1
    cv2.putText(img, txt, (org[0] + 2, org[1] + 2), FONT, sc, (0, 0, 0), th + 2, cv2.LINE_AA)
    cv2.putText(img, txt, org, FONT, sc, col, th, cv2.LINE_AA)


def temp_of(v):
    return T_MIN + v * (T_MAX - T_MIN)


def people_boxes(m8):
    """Split the combined person matte into one box per person using gaps in the head/shoulder band."""
    h, w = m8.shape
    boxes = []
    k, lab, stats, _ = cv2.connectedComponentsWithStats(m8, 8)
    for i in range(1, k):
        x, y, bw, bh, area = stats[i]
        if area < 12000:
            continue
        comp = (lab == i)
        band = comp[y:y + max(40, int(bh * 0.3))]
        prof = cv2.GaussianBlur(band.sum(0).astype(np.float32)[None], (0, 0), 8)[0]
        on = prof > prof.max() * 0.12
        xs = np.nonzero(on)[0]
        segs, start = [], None
        for c in range(w):
            if on[c] and start is None:
                start = c
            if (not on[c] or c == w - 1) and start is not None:
                if c - start > 60:
                    segs.append((start, c))
                start = None
        for a, b in segs or [(x, x + bw)]:
            sub = comp[:, a:b]
            rows = np.nonzero(sub.any(1))[0]
            boxes.append((a, rows.min(), b - a, rows.max() - rows.min()))
    return boxes


def hud(img, heat, mask, lut, n, rng, pal):
    h, w = heat.shape
    W = (242, 242, 242)
    # frame corner brackets
    L = 60
    for (x, y, dx, dy) in [(30, 30, 1, 1), (w - 30, 30, -1, 1), (30, h - 30, 1, -1), (w - 30, h - 30, -1, -1)]:
        cv2.line(img, (x, y), (x + dx * L, y), W, 3, cv2.LINE_AA)
        cv2.line(img, (x, y), (x, y + dy * L), W, 3, cv2.LINE_AA)
    # top-left status block
    sec = (n - 1) / 12
    put(img, "IR-CAM 02   LWIR 8-14um", (60, 80), 0.8, 2, W)
    put(img, f"{pal.upper()}   E 0.98   {int(sec // 60):02d}:{sec % 60:05.2f}", (60, 115), 0.8, 2, W)
    if (n // 6) % 2 == 0:
        cv2.circle(img, (w - 190, 72), 10, (25, 25, 242), -1, cv2.LINE_AA)
    put(img, "REC", (w - 170, 82), 0.9, 2, W)
    # colour scale bar on the right
    x0, y0, y1 = w - 75, 190, h - 230
    bar = lut[np.linspace(255, 0, y1 - y0).astype(int)]
    img[y0:y1, x0:x0 + 22] = (bar[:, None, :] * 255).astype(np.uint8)
    cv2.rectangle(img, (x0 - 1, y0 - 1), (x0 + 23, y1), W, 2)
    put(img, f"{T_MAX:.1f}", (x0 - 70, y0 + 8), 0.65, 2, W)
    put(img, f"{T_MIN:.1f}", (x0 - 70, y1), 0.65, 2, W)
    put(img, "C", (x0 + 2, y0 - 14), 0.7, 2, W)
    # centre spot meter
    cx, cy = w // 2, h // 2
    t = temp_of(heat[cy - 4:cy + 5, cx - 4:cx + 5].mean()) + rng.normal(0, 0.05)
    cv2.line(img, (cx - 34, cy), (cx - 10, cy), W, 2, cv2.LINE_AA)
    cv2.line(img, (cx + 10, cy), (cx + 34, cy), W, 2, cv2.LINE_AA)
    cv2.line(img, (cx, cy - 34), (cx, cy - 10), W, 2, cv2.LINE_AA)
    cv2.line(img, (cx, cy + 10), (cx, cy + 34), W, 2, cv2.LINE_AA)
    put(img, f"SP1 {t:.1f}C", (cx + 42, cy - 14), 0.8, 2, W)
    # hottest point marker
    sm = cv2.GaussianBlur(heat, (0, 0), 6)
    my, mx = np.unravel_index(np.argmax(sm), sm.shape)
    tri = np.array([[mx, my - 6], [mx - 14, my - 30], [mx + 14, my - 30]], np.int32)
    cv2.fillPoly(img, [tri], (38, 38, 242), cv2.LINE_AA)
    put(img, f"MAX {temp_of(sm[my, mx]) + rng.normal(0, 0.05):.1f}C", (mx - 70, my - 42), 0.7, 2, W)
    # person detection boxes from the matte
    m8 = (mask > 0.5).astype(np.uint8)
    G = (90, 242, 115)
    for x, y, bw, bh in people_boxes(m8):
        x, y = x - 6 + int(rng.normal(0, 1.2)), y - 6 + int(rng.normal(0, 1.2))
        bw, bh = bw + 12, min(bh + 12, h - y - 4)
        c = 26
        for (px, py, dx, dy) in [(x, y, 1, 1), (x + bw, y, -1, 1), (x, y + bh, 1, -1), (x + bw, y + bh, -1, -1)]:
            cv2.line(img, (px, py), (px + dx * c, py), G, 3, cv2.LINE_AA)
            cv2.line(img, (px, py), (px, py + dy * c), G, 3, cv2.LINE_AA)
        reg = heat[max(y, 0):y + bh, max(x, 0):x + bw][m8[max(y, 0):y + bh, max(x, 0):x + bw] > 0]
        tt = temp_of(np.percentile(reg, 97)) + rng.normal(0, 0.06)
        ty = y - 14 if y > 60 else y + 44
        put(img, f"HUMAN {tt:.1f}C", (x + 4, ty), 0.7, 2, G)
    # bottom data strip
    put(img, f"MIN {temp_of(heat.min()):.1f}C   AVG {temp_of(heat.mean()):.1f}C   DIST 2.4m   NUC OK",
        (int(w * 0.30), h - 52), 0.7, 2, W)


def render(n):
    rng = np.random.default_rng(16_000 + n)
    _, _, pal = section_of(n)
    lut = PALETTES[pal]
    bgr = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png"))
    mask = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
    h, w = mask.shape
    heat, _ = heat_field(bgr, mask, rng)
    heat = (heat + sensor_noise(rng, h, w, n)).clip(0, 1)
    img = lut[(heat * 255).astype(np.uint8)]
    # slight lens bloom on the hottest areas, vignette
    hot = np.clip(heat - 0.8, 0, 1)[..., None] * 2.5
    img = img + cv2.GaussianBlur(img * hot, (0, 0), 14) * 0.6
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    img *= (1 - 0.22 * np.clip(r - 0.55, 0, 1))[..., None]
    img = (img.clip(0, 1) * 255).astype(np.uint8)
    hud(img, heat, mask, lut, n, rng, pal)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), img)
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    with Pool(6) as p:
        for n in p.imap_unordered(render, ONLY):
            print("frame", n)
