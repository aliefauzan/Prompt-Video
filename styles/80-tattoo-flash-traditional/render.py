"""American Traditional tattoo flash restyle, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [all | frame numbers...]

Built like a hand-painted flash sheet hanging on a tattoo-shop wall:
  PEOPLE AS FLASH: each person is simplified into flat fills from a strict
    traditional palette (black, red, mustard yellow, kelly green, teal blue,
    brown, skin, cream), wrapped in a HEAVY black outline with bold interior
    lines; shadows are black WHIP SHADING (stippled black that tapers off from
    the lines into the colour). Faces get flash-style bold features drawn from
    Apple Vision landmarks: black brows, outlined eyes with solid pupils and
    red-filled lips.
  SHEET: the room is gone; the people sit on aged, stained cream paper with
    classic filler motifs painted around them (swallows, roses, stars, a heart,
    a ribbon banner with lettering, sparkles and dots) and a faint sepia trace
    of the room like a transfer drawing.
  The colours sit in the paper (multiplied, a little uneven); outlines wobble a
    pixel every 2 frames like re-painted flash. Motifs are static on the sheet.
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

# traditional flash palette (RGB)
PAL = {
    "black": (24, 20, 18),
    "cream": (244, 234, 206),
    "skin": (243, 196, 150),
    "red": (196, 34, 30),
    "yellow": (236, 178, 38),
    "green": (36, 122, 62),
    "teal": (26, 104, 140),
    "brown": (132, 70, 36),
}
NAMES = list(PAL)
PAL_RGB = np.array([PAL[k] for k in NAMES], np.float32) / 255
BLACK = np.array(PAL["black"], np.float32)[::-1] / 255
RED = PAL["red"]
SKIN_I, BLACK_I, CREAM_I = NAMES.index("skin"), NAMES.index("black"), NAMES.index("cream")


def frame_list():
    if not ARGS or ARGS == ["all"]:
        return list(range(1, 180))
    return [int(a) for a in ARGS]


def read(n):
    src = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png"))
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
    return src, m


def fbm(seed, octaves=4, base=4):
    rng = np.random.default_rng(seed)
    out = np.zeros((H, W), np.float32)
    amp, tot = 1.0, 0.0
    for o in range(octaves):
        c = base * 2 ** o
        n = rng.random((max(2, H * c // W), c)).astype(np.float32)
        out += amp * cv2.resize(n, (W, H), interpolation=cv2.INTER_CUBIC)
        tot += amp
        amp *= 0.5
    return out / tot


def _paper():
    """Aged cream flash paper: tea stains, darker edges, fibre grain (BGR float)."""
    base = np.array(PAL["cream"][::-1], np.float32) / 255
    stain = fbm(21, 5, 3)
    p = base[None, None] * (1 - 0.10 * np.clip((stain - 0.45) * 2.2, 0, 1))[..., None]
    p = p * (1 - np.array([0.10, 0.04, 0.0], np.float32) * np.clip((stain - 0.5) * 3, 0, 1)[..., None])
    edge = np.clip(((xx / W - 0.5) ** 2 + (yy / H - 0.5) ** 2) * 2.6, 0, 1)
    p = p * (1 - 0.22 * edge ** 1.6)[..., None] * (1 - np.array([0.12, 0.05, 0], np.float32) * edge[..., None])
    grain = cv2.GaussianBlur(np.random.default_rng(5).normal(0, 1, (H, W)).astype(np.float32), (0, 0), 0.8)
    return np.clip(p * (1 + 0.025 * grain)[..., None], 0, 1)


PAPER = _paper()


# ---------- flash motifs (drawn once at 2x, static on the sheet) ----------
S2 = 2
OUTW = 5 * S2


def _star(d, cx, cy, r, fill):
    pts = []
    for k in range(10):
        a = -np.pi / 2 + k * np.pi / 5
        rr = r if k % 2 == 0 else r * 0.45
        pts.append(((cx + rr * np.cos(a)) * S2, (cy + rr * np.sin(a)) * S2))
    d.polygon(pts, fill=fill, outline=PAL["black"], width=OUTW)


def _sparkle(d, cx, cy, r):
    pts = []
    for k in range(8):
        a = k * np.pi / 4
        rr = r if k % 2 == 0 else r * 0.18
        pts.append(((cx + rr * np.cos(a)) * S2, (cy + rr * np.sin(a)) * S2))
    d.polygon(pts, fill=PAL["black"])


def _swallow(d, cx, cy, s, flip):
    """Traditional swallow in side view: teal back and wings, red breast, forked tail."""
    f = -1 if flip else 1

    def P(pts):
        return [((cx + f * x * s) * S2, (cy + y * s) * S2) for x, y in pts]
    tail = [(-28, -4), (-92, -30), (-62, 0), (-94, 26), (-28, 6)]
    wing_up = [(8, -10), (-8, -46), (-58, -88), (-34, -34), (-16, -8)]
    wing_dn = [(8, 8), (-4, 44), (-48, 92), (-28, 36), (-14, 8)]
    body = [(-36, 0), (-10, -13), (24, -15), (46, -11), (54, 1), (34, 13), (0, 15), (-26, 9)]
    breast = [(22, 3), (50, 1), (52, 5), (32, 13), (2, 14), (12, 5)]
    for poly, col in ((tail, PAL["teal"]), (wing_up, PAL["teal"]), (body, PAL["teal"]),
                      (breast, PAL["red"]), (wing_dn, PAL["teal"])):
        d.polygon(P(poly), fill=col, outline=PAL["black"], width=OUTW)
    for poly in ((-2, -18, -40, -66), (-2, 20, -34, 68)):            # feather lines
        d.line(P([poly[:2], poly[2:]]), fill=PAL["black"], width=3 * S2)
    d.polygon(P([(52, -6), (70, 0), (52, 4)]), fill=PAL["yellow"], outline=PAL["black"], width=3 * S2)
    ex, ey = P([(40, -5)])[0]
    d.ellipse([ex - 4 * S2, ey - 4 * S2, ex + 4 * S2, ey + 4 * S2], fill=PAL["black"])


def _rose(d, cx, cy, r):
    for a in (-0.5, 2.6):
        lx, ly = cx + np.cos(a) * r * 1.25, cy + np.sin(a) * r * 1.0
        leaf = []
        for t in np.linspace(0, np.pi, 12):
            leaf.append((np.cos(t) * r * 0.7, np.sin(t) * r * 0.32))
        for t in np.linspace(np.pi, 2 * np.pi, 12):
            leaf.append((np.cos(t) * r * 0.7, np.sin(t) * r * 0.32))
        ca, sa = np.cos(a), np.sin(a)
        pts = [((lx + x * ca - y * sa) * S2, (ly + x * sa + y * ca) * S2) for x, y in leaf]
        d.polygon(pts, fill=PAL["green"], outline=PAL["black"], width=OUTW)
        d.line([((lx - r * 0.6 * ca) * S2, (ly - r * 0.6 * sa) * S2), ((lx + r * 0.55 * ca) * S2, (ly + r * 0.55 * sa) * S2)],
               fill=PAL["black"], width=3 * S2)
    d.ellipse([(cx - r) * S2, (cy - r * 0.92) * S2, (cx + r) * S2, (cy + r * 0.92) * S2],
              fill=PAL["red"], outline=PAL["black"], width=OUTW)
    for k, rr in enumerate((0.72, 0.48, 0.26)):
        st = 200 + k * 70
        d.arc([(cx - r * rr) * S2, (cy - r * rr * 0.9) * S2, (cx + r * rr) * S2, (cy + r * rr * 0.9) * S2],
              st, st + 250, fill=PAL["black"], width=4 * S2)
    d.arc([(cx - r * 0.9) * S2, (cy - r * 0.2) * S2, (cx + r * 0.9) * S2, (cy + r * 0.85) * S2],
          10, 170, fill=PAL["black"], width=4 * S2)


def _heart(d, cx, cy, r):
    t = np.linspace(0, 2 * np.pi, 80)
    x = 16 * np.sin(t) ** 3
    y = -(13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t))
    pts = [((cx + xi * r / 16) * S2, (cy + yi * r / 16) * S2) for xi, yi in zip(x, y)]
    d.polygon(pts, fill=PAL["red"], outline=PAL["black"], width=OUTW)
    d.arc([(cx - r * 0.75) * S2, (cy - r * 0.62) * S2, (cx - r * 0.15) * S2, (cy - r * 0.0) * S2],
          190, 260, fill=PAL["cream"], width=4 * S2)


def _banner(d, cx, cy, w, text):
    h = 52
    x0, x1 = cx - w / 2, cx + w / 2
    # folded tails
    for side in (-1, 1):
        xe = x0 if side < 0 else x1
        tail = [(xe, cy - h / 2 + 14), (xe + side * 70, cy - h / 2 + 14), (xe + side * 44, cy + 10),
                (xe + side * 70, cy + h / 2 + 18), (xe, cy + h / 2 + 18)]
        d.polygon([(x * S2, y * S2) for x, y in tail], fill=PAL["red"], outline=PAL["black"], width=OUTW)
    body = []
    for xi in np.linspace(x0, x1, 40):
        body.append((xi, cy - h / 2 - 10 * np.sin(np.pi * (xi - x0) / w)))
    for xi in np.linspace(x1, x0, 40):
        body.append((xi, cy + h / 2 - 10 * np.sin(np.pi * (xi - x0) / w)))
    d.polygon([(x * S2, y * S2) for x, y in body], fill=PAL["cream"], outline=PAL["black"], width=OUTW)
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Rockwell.ttc", 40 * S2, index=1)
    d.text((cx * S2, (cy - 8) * S2), text, fill=PAL["black"], font=font, anchor="mm",
           stroke_width=0)


def _motifs():
    img = Image.new("RGBA", (W * S2, H * S2), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    rng = np.random.default_rng(8)
    for _ in range(46):
        x, y = rng.uniform(70, W - 70), rng.uniform(60, H - 60)
        rr = rng.uniform(3, 6)
        d.ellipse([(x - rr) * S2, (y - rr) * S2, (x + rr) * S2, (y + rr) * S2], fill=PAL["black"])
    for x, y, r in ((560, 300, 16), (1080, 110, 14), (270, 600, 20), (1520, 330, 15), (700, 640, 12),
                    (1350, 690, 18), (90, 420, 14), (980, 540, 12)):
        _sparkle(d, x, y, r)
    for x, y, r, c in ((470, 470, 30, "yellow"), (1140, 300, 26, "yellow"), (120, 160, 24, "red"),
                       (1500, 520, 28, "yellow"), (620, 120, 20, "red"), (1290, 880, 26, "red"),
                       (330, 860, 24, "yellow")):
        _star(d, x, y, r, PAL[c])
    _swallow(d, 370, 200, 1.25, False)
    _swallow(d, 1250, 210, 1.25, True)
    _rose(d, 1500, 140, 62)
    _rose(d, 160, 720, 56)
    _heart(d, 1080, 440, 46)
    _banner(d, 810, 86, 470, "TRUE TO LIFE")
    img = img.resize((W, H), Image.LANCZOS)
    a = np.asarray(img, np.float32) / 255
    return a[..., :3][..., ::-1].copy(), a[..., 3].copy()


MOTIF_RGB, MOTIF_A = _motifs()
MOTIF_RGB = np.ascontiguousarray(MOTIF_RGB)
MOTIF_A = np.ascontiguousarray(MOTIF_A)


# ---------- people ----------
def to_lab(rgb01):
    return cv2.cvtColor(rgb01.reshape(1, -1, 3).astype(np.float32), cv2.COLOR_RGB2Lab).reshape(-1, 3)


PAL_LAB = to_lab(PAL_RGB)


def face_mask(n):
    fm = np.zeros((H, W), np.uint8)
    for f in FACES.get(f"frame_{n:03d}.png", []):
        x, y, w, h = f["box"]
        pts = [tuple(p) for p in f.get("faceContour", [])]
        pts += [(x + 0.12 * w, y - 0.12 * h), (x + 0.88 * w, y - 0.12 * h)]
        hull = cv2.convexHull(np.array(pts, np.float32)).astype(np.int32)
        cv2.fillPoly(fm, [hull], 255)
    return fm.astype(np.float32) / 255


def head_zone(fm):
    """Area around and above each face where dark = hair."""
    hz = np.zeros((H, W), np.uint8)
    ys, xs = np.nonzero(fm > 0.5)
    if not len(xs):
        return hz
    n_lab, lab, stats, _ = cv2.connectedComponentsWithStats((fm > 0.5).astype(np.uint8))
    for k in range(1, n_lab):
        x, y, w, h, _a = stats[k]
        cv2.ellipse(hz, (int(x + w / 2), int(y + h * 0.35)), (int(w * 0.85), int(h * 0.85)), 0, 0, 360, 1, -1)
    return hz * (fm < 0.5)


def classify(src, mask, fm):
    """Map every person pixel to one flash palette colour with hue/value rules."""
    small = cv2.resize(src, (W // 3, H // 3), interpolation=cv2.INTER_AREA)
    ms = cv2.pyrMeanShiftFiltering(small, 10, 24)
    ms = cv2.medianBlur(ms, 5)
    f = cv2.resize(ms, (W, H), interpolation=cv2.INTER_LINEAR).astype(np.float32) / 255
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
    h, sat, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    L = {k: NAMES.index(k) for k in NAMES}
    lab_i = np.full((H, W), L["cream"], np.int32)
    grey = sat < 0.20
    lum = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
    lums = cv2.GaussianBlur(lum, (0, 0), 2)
    light = lums > cv2.GaussianBlur(lums, (0, 0), 9) + 0.03          # stripes, highlights
    lab_i[grey & (v > 0.42)] = L["yellow"]
    lab_i[grey & (v > 0.42) & (light | (v > 0.86))] = L["cream"]
    dg = grey & (v <= 0.42)
    lab_i[dg] = np.where((h[dg] >= 170) & (h[dg] < 280), L["teal"], L["green"])
    col = ~grey
    hh = h
    red = col & ((hh < 18) | (hh >= 300) | ((hh < 45) & (v < 0.55)))
    lab_i[red] = np.where(v[red] < 0.28, L["brown"], L["red"])
    lab_i[col & (hh >= 18) & (hh < 70) & (v >= 0.55)] = L["yellow"]
    lab_i[col & (hh >= 18) & (hh < 70) & (v >= 0.55) & light & (sat < 0.4)] = L["cream"]
    lab_i[col & (hh >= 45) & (hh < 70) & (v < 0.55)] = L["yellow"]
    lab_i[col & (hh >= 70) & (hh < 170)] = L["green"]
    lab_i[col & (hh >= 170) & (hh < 300)] = L["teal"]
    lab_i[v < 0.17] = L["black"]
    lab_i[(head_zone(fm) > 0) & (v < 0.42)] = L["black"]               # hair
    # skin: YCrCb + saturation test on the source, plus the face hulls
    ycc = cv2.cvtColor(cv2.GaussianBlur(src, (0, 0), 2), cv2.COLOR_BGR2YCrCb).astype(np.float32)
    sat_s = cv2.cvtColor(cv2.GaussianBlur(src, (0, 0), 2), cv2.COLOR_BGR2HSV)[..., 1].astype(np.float32) / 255
    skin = ((ycc[..., 1] > 140) & (ycc[..., 1] < 178) & (ycc[..., 2] > 80) & (ycc[..., 2] < 122)
            & (lums > 0.40) & (sat_s > 0.40))
    skin |= (ycc[..., 1] > 150) & (lums > 0.45) & (sat_s > 0.25)
    near = np.zeros((H, W), np.uint8)                                  # face + neck zone
    n_lab, _lab, stats, _ = cv2.connectedComponentsWithStats((fm > 0.5).astype(np.uint8))
    for k in range(1, n_lab):
        x, y, w, h, _a = stats[k]
        cv2.ellipse(near, (int(x + w / 2), int(y + h)), (int(w * 0.38), int(h * 0.45)), 0, 0, 360, 1, -1)
    near = near > 0
    skin |= near & (ycc[..., 1] > 138) & (ycc[..., 2] < 122) & (lums > 0.24) & (sat_s > 0.30)
    skin |= (fm > 0.5) & (lums > 0.22)
    lab_i[skin] = L["skin"]
    # smooth the label map: per-label soft votes
    votes = np.stack([cv2.GaussianBlur((lab_i == k).astype(np.float32), (0, 0), 2.5) for k in range(len(NAMES))], -1)
    return np.argmax(votes, -1).astype(np.int32), lum


def wobble(img, seed, amp=1.0):
    rng = np.random.default_rng(seed)
    dx = cv2.resize(rng.normal(0, 1, (H // 70, W // 70)).astype(np.float32), (W, H), interpolation=cv2.INTER_CUBIC)
    dy = cv2.resize(rng.normal(0, 1, (H // 70, W // 70)).astype(np.float32), (W, H), interpolation=cv2.INTER_CUBIC)
    return cv2.remap(img, (xx + amp * dx).astype(np.float32), (yy + amp * dy).astype(np.float32),
                     cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)


def face_features(n):
    """Bold flash features from landmarks: (ink alpha, red lip alpha)."""
    s = 2
    ink = Image.new("L", (W * s, H * s), 0)
    lip = Image.new("L", (W * s, H * s), 0)
    di, dl = ImageDraw.Draw(ink), ImageDraw.Draw(lip)
    for f in FACES.get(f"frame_{n:03d}.png", []):
        x, y, w, h = f["box"]
        lw = max(2, int(w / 40)) * s

        def P(k):
            return [(px * s, py * s) for px, py in f.get(k, [])]
        for k in ("leftEyebrow", "rightEyebrow"):
            if len(P(k)) > 1:
                di.line(P(k), fill=255, width=int(lw * 1.5), joint="curve")
        for k, pk in (("leftEye", "leftPupil"), ("rightEye", "rightPupil")):
            pts = P(k)
            if len(pts) > 2:
                di.line(pts + pts[:1], fill=255, width=lw, joint="curve")
                ex = [p[0] for p in pts]
                r = (max(ex) - min(ex)) * 0.2
                c = P(pk)[0] if P(pk) else (sum(ex) / len(ex), sum(p[1] for p in pts) / len(pts))
                di.ellipse([c[0] - r, c[1] - r, c[0] + r, c[1] + r], fill=255)
        ol = P("outerLips")
        if len(ol) > 2:
            dl.polygon(ol, fill=255)
            di.line(ol + ol[:1], fill=255, width=int(lw * 0.9), joint="curve")
        il = P("innerLips")
        if len(il) > 1:
            di.line(il + il[:1], fill=255, width=int(lw * 0.7), joint="curve")
        nose = P("nose")
        if len(nose) > 4:
            di.line(nose[2:-2], fill=255, width=int(lw * 0.8), joint="curve")
    ink = np.asarray(ink.resize((W, H), Image.LANCZOS), np.float32) / 255
    lip = np.asarray(lip.resize((W, H), Image.LANCZOS), np.float32) / 255
    return ink, lip


def render(n):
    src, mask = read(n)
    boil = n // 2
    m = cv2.GaussianBlur(mask, (0, 0), 1.5)
    mb = (m > 0.5).astype(np.uint8)
    fm = face_mask(n)
    labels, lum = classify(src, mask, fm)
    labels = np.where(mb > 0, labels, CREAM_I)
    fill = PAL_RGB[labels][..., ::-1].astype(np.float32)        # BGR

    # whip shading: black stipple where a region is darker than its own average,
    # tapering away from the lines
    lums = cv2.GaussianBlur(lum, (0, 0), 3)
    reg_mean = np.zeros_like(lum)
    for k in np.unique(labels):
        sel = labels == k
        reg_mean[sel] = lums[sel].mean()
    shade = np.clip((reg_mean - lums) / 0.16, 0, 1)
    shade[labels == BLACK_I] = 0
    shade *= 1 - 0.75 * cv2.GaussianBlur(fm, (0, 0), 6)        # faces stay clean
    edges = cv2.Canny((labels * 30).astype(np.uint8), 10, 20)
    edges = np.maximum(edges, cv2.morphologyEx(mb, cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8)) * 255)
    dist = cv2.distanceTransform(255 - edges, cv2.DIST_L2, 5)
    whip = shade * (0.35 + 0.65 * np.exp(-dist / 16)) * np.exp(-dist / 60)
    rng = np.random.default_rng(1000 + boil)
    noise = cv2.resize(rng.random((H // 2, W // 2)).astype(np.float32), (W, H), interpolation=cv2.INTER_NEAREST)
    stip = np.clip((whip * 0.95 - noise) * 6, 0, 1) * (mb > 0)

    # outlines: heavy silhouette + bold interior lines
    sil = cv2.dilate(cv2.morphologyEx(mb, cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8)),
                     cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
    inner = cv2.dilate((edges > 0).astype(np.uint8) * (mb > 0), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4)))
    g = cv2.GaussianBlur(lum, (0, 0), 1.4)
    xd = np.clip(-(g - 0.98 * cv2.GaussianBlur(lum, (0, 0), 2.4) + 0.012) * 40, 0, 1) * (mb > 0)
    xd = (cv2.GaussianBlur(xd, (0, 0), 1.0) > 0.45).astype(np.float32) * 0.9
    line = np.maximum(np.maximum(sil, inner).astype(np.float32), xd)
    line = cv2.GaussianBlur(line, (0, 0), 1.2)
    line = np.clip((line - 0.35) * 4, 0, 1)                     # smooth, round ink edges
    line = wobble(line, 300 + boil, 0.9)
    feat, lip = face_features(n)

    # composite: paper -> faint room trace -> motifs -> people
    out = PAPER.copy()
    room = cv2.GaussianBlur(lum, (0, 0), 1.5)
    trace = np.clip(-(room - 0.985 * cv2.GaussianBlur(lum, (0, 0), 3) + 0.01) * 30, 0, 1) * 0.22
    out = out * (1 - trace[..., None] * np.array([0.55, 0.65, 0.75], np.float32))
    out = out * (1 - MOTIF_A[..., None]) + MOTIF_RGB * MOTIF_A[..., None] * (0.92 + 0.08 * out)
    paper_t = PAPER / PAPER.mean((0, 1), keepdims=True)
    people = fill * np.clip(paper_t, 0.85, 1.1) * (1 + 0.04 * (fbm(40 + boil % 3, 3, 8) - 0.5))[..., None]
    lipc = np.array((182, 62, 50)[::-1], np.float32) / 255
    people = people * (1 - lip[..., None]) + lipc * lip[..., None]
    pm = np.clip(cv2.dilate(m, np.ones((5, 5), np.uint8)) * 1.0, 0, 1)[..., None]
    out = out * (1 - pm) + people * pm
    ink = np.clip(np.maximum(np.maximum(line, stip), feat * (mb > 0)), 0, 1)[..., None]
    out = out * (1 - ink) + BLACK * ink
    out = (np.clip(out, 0, 1) * 255).astype(np.uint8)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), out)
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    with Pool(4) as p:
        for n in p.imap_unordered(render, frame_list()):
            print(n, end=" ", flush=True)
    print()
