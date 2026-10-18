"""CCTV night-vision security-camera restyle, frame by frame.

usage: python -I render.py [frame numbers... | all]   (default: the six sheet frames)
       RENDER_OUT=/tmp/prompt-video-render/38-cctv-night-vision python -I render.py all   -> full clip for make_video.py
Reads ../../_source/frames + ../../_source/masks, writes ./frames/frame_NNN.png.

Pipeline per frame: IR luminance (skin + plants glow, dye patterns fade) -> night exposure
(IR illuminator hotspot, dark room) -> D1 720x480 sensor with interlace, grain, over-sharpening
and heavy JPEG blocks -> fisheye barrel lens -> DVR OSD (timestamp, CAM ID, REC), person boxes
and red motion-detect cells. Some frames are dropped (held) and a few get macroblock tears.
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "..", "_source")
FRAMES, MASKS = os.path.join(SRC, "frames"), os.path.join(SRC, "masks")
OUT = os.environ.get("RENDER_OUT", os.path.join(HERE, "frames"))
ONLY = (list(range(1, 180)) if sys.argv[1:] == ["all"] else [int(a) for a in sys.argv[1:]]) or [13, 49, 85, 109, 145, 178]
W, H = 1620, 1080
LW, LH = 720, 480                       # D1 analogue CCTV resolution
NV = (67, 132)                          # green-phosphor night-vision section, IR mono elsewhere
SWITCH = {67, 133}                      # IR-cut filter clicks: one washed-out frame


def font(size, bold=True):
    try:
        return ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", size, index=1 if bold else 0)
    except OSError:
        return ImageFont.load_default()


# deterministic dropped frames: the DVR repeats the previous picture, clock keeps running
_r = np.random.default_rng(38)
HELD = {n for n in range(3, 180) if _r.random() < 0.11}
HELD -= {13, 49, 85, 109, 145, 178}
TEAR = {n for n in range(2, 180) if _r.random() < 0.05} - HELD


def src_index(n):
    while n in HELD and n > 1:
        n -= 1
    return n


def load(n):
    n = max(1, min(179, n))
    bgr = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png"))
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
    return bgr, m


def ir_luma(bgr, m):
    """Near-infrared look: skin and plants reflect IR (pale), dye patterns fade, room falls off."""
    f = bgr.astype(np.float32) / 255
    b, g, r = f[..., 0], f[..., 1], f[..., 2]
    ir = 0.60 * r + 0.32 * g + 0.08 * b
    ycc = cv2.cvtColor(bgr, cv2.COLOR_BGR2YCrCb).astype(np.float32)
    cr, cb = ycc[..., 1], ycc[..., 2]
    skin = ((cr > 136) & (cr < 175) & (cb > 85) & (cb < 128) & (ycc[..., 0] > 55)).astype(np.float32)
    skin = cv2.GaussianBlur(skin, (0, 0), 3) * cv2.GaussianBlur(m, (0, 0), 2)
    ir = ir * (1 - 0.55 * skin) + (0.55 + 0.55 * ir) * 0.55 * skin          # skin glows pale and smooth
    plant = np.clip((g - np.maximum(r, b)) * 6, 0, 1) * (1 - m)
    ir = np.maximum(ir, 0.75 * cv2.GaussianBlur(plant, (0, 0), 2))         # chlorophyll is bright in IR
    cloth = m * (1 - skin)
    ir = ir * (1 - 0.55 * cloth) + cv2.GaussianBlur(ir, (0, 0), 3) * 0.55 * cloth + 0.10 * cloth
    # night: the IR illuminator lights the near people, the room falls off into dark grey
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    hot = np.exp(-(((xx - W * 0.5) / (W * 0.55)) ** 2 + ((yy - H * 0.45) / (H * 0.62)) ** 2))
    mm = cv2.GaussianBlur(m, (0, 0), 6)
    room = np.minimum(ir, 0.8) * (0.16 + 0.30 * hot)
    room = room + 0.12 * cv2.GaussianBlur((ir > 0.9).astype(np.float32), (0, 0), 25)   # lamps / window bloom
    lit = np.clip(ir * (0.78 + 0.35 * hot), 0, 1)
    return np.clip(room * (1 - mm) + lit * mm, 0, 1)


def lens_maps():
    """Barrel (fisheye-ish) distortion maps, slightly overscanned so the corners bend in."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    nx, ny = (xx - W / 2) / (W / 2), (yy - H / 2) / (W / 2)
    r2 = nx * nx + ny * ny
    k = 1 + 0.20 * r2 + 0.05 * r2 * r2
    s = 0.86
    mx = (nx * k * s) * (W / 2) + W / 2
    my = (ny * k * s) * (W / 2) + H / 2
    return mx.astype(np.float32), my.astype(np.float32)


MX, MY = lens_maps()


def sensor(lum, prev_lum, rng, nv):
    small = cv2.resize(lum, (LW, LH), interpolation=cv2.INTER_AREA)
    prev = cv2.resize(prev_lum, (LW, LH), interpolation=cv2.INTER_AREA)
    small[1::2] = 0.5 * small[1::2] + 0.5 * prev[1::2]              # interlace combing on motion
    small = np.clip((small - 0.03) * 1.12, 0, 1) ** (0.82 if nv else 0.92)   # AGC lifts the shadows
    grain = rng.normal(0, 0.075 if nv else 0.045, (LH, LW)).astype(np.float32)
    grain = cv2.GaussianBlur(grain, (0, 0), 0.6)
    small = small + grain * (0.55 + 0.6 * (1 - small))
    if nv:                                                            # tube scintillation sparkles
        sp = rng.random((LH, LW)) > 0.9965
        small[sp] = 1.0
    blur = cv2.GaussianBlur(small, (0, 0), 1.6)
    small = np.clip(small + 0.9 * (small - blur), 0, 1)              # cheap DSP over-sharpening halos
    # heavy JPEG / H.264 blocks
    q = int(rng.integers(14, 26))
    ok, enc = cv2.imencode(".jpg", (small * 255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, q])
    small = cv2.imdecode(enc, cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
    return cv2.resize(small, (W, H), interpolation=cv2.INTER_LINEAR)


def colourize(lum, nv, wash=False):
    if wash:
        lum = np.clip(lum * 0.55 + 0.42, 0, 1)
    if nv:      # P43 green phosphor intensifier
        r = 0.10 * lum + 0.55 * lum ** 3
        g = 0.06 + 0.98 * lum
        b = 0.05 + 0.18 * lum + 0.3 * lum ** 4
    else:       # IR mono with the cold grey-green cast of cheap CCTV sensors
        r = 0.86 * lum + 0.02
        g = 0.97 * lum + 0.035
        b = 0.90 * lum + 0.03
    img = np.stack([b, g, r], -1)
    if nv:
        bloom = cv2.GaussianBlur(np.clip(lum - 0.7, 0, 1), (0, 0), 9)[..., None]
        img += bloom * np.array([0.1, 0.55, 0.2], np.float32)
    return np.clip(img, 0, 1)


def vignette():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
    return np.clip(1.15 - 0.55 * d ** 2.2, 0.08, 1)[..., None]


VIG = vignette()


def tear(img, rng):
    """DVR macroblock tear: a band of 16 px blocks smeared sideways and frozen grey."""
    out = img.copy()
    y0 = int(rng.integers(150, H - 300))
    hgt = int(rng.integers(3, 9)) * 16
    band = out[y0:y0 + hgt]
    shift = int(rng.integers(-120, 120))
    band = np.roll(band, shift, axis=1)
    for x in range(0, W, 32):
        if rng.random() < 0.35:
            band[:, x:x + 32] = band[:, x:x + 32].mean((0, 1))
    out[y0:y0 + hgt] = band
    return out


def heads(m):  # silhouette head finder, adapted from styles/17 render.py
    """Find heads from the matte: lowest-y peaks of the silhouette, head width from the row runs,
    stop at the neck dip / shoulder jump. Returns [(xc, y0, yneck, headw)]."""
    cols = m > 0.5
    has = cols.any(0)
    topy = np.where(has, cols.argmax(0), H).astype(np.float32)
    remaining = has.copy()
    out = []
    for _ in range(4):
        cand = np.flatnonzero(remaining & (topy < H * 0.85))
        if len(cand) < 12:
            break
        y0 = int(topy[cand].min())
        xs = cand[topy[cand] <= y0 + 4]
        grp = np.split(xs, np.flatnonzero(np.diff(xs) > 3) + 1)[0]
        x0 = int(grp[len(grp) // 2])
        row = cols[min(H - 1, y0 + 2)]
        l = x0 - (np.flatnonzero(~row[:x0][::-1])[:1].tolist() or [x0])[0]
        r = x0 + (np.flatnonzero(~row[x0:])[:1].tolist() or [W - x0])[0]
        if any(l <= h[0] <= r for h in out):           # a shoulder of a head we already have
            remaining[l:r] = False
            continue
        wmax, yneck, xc, wprev, grow = 1, None, x0, None, True
        for y in range(y0, min(H, y0 + int(H * 0.6))):
            row = cols[y]
            if not row[x0]:
                continue
            l = x0 - (np.flatnonzero(~row[:x0][::-1])[:1].tolist() or [x0])[0]
            r = x0 + (np.flatnonzero(~row[x0:])[:1].tolist() or [W - x0])[0]
            w = r - l
            dy = y - y0
            if wprev is not None and dy > 20 and w > wprev * 1.12 + 10:
                grow = False                            # sudden widening: shoulder or a merged neighbour
                if dy > 0.9 * wmax:
                    yneck = y
                    break
            wprev = w
            if grow and (dy < 1.0 * wmax or dy < 20):
                if w > wmax:
                    wmax, xc = w, (l + r) // 2
            elif dy < 0.9 * wmax:
                continue
            elif w < 0.85 * wmax or w > 1.7 * wmax or dy > 1.25 * wmax:
                yneck = y
                break
        yneck = yneck or min(H - 1, y0 + int(1.25 * wmax))
        if wmax >= 24:
            out.append((xc, y0, yneck, wmax))
        remaining[max(0, xc - int(wmax * 1.1)):xc + int(wmax * 1.1)] = False
        remaining[max(0, x0 - 12):x0 + 12] = False
    return out



def boxes(m):
    """One person box per head found on the (lens-warped) matte: head box + body box."""
    out = []
    for xc, y0, yn, hw in heads(m):
        bw = int(hw * 3.0)
        x0 = max(0, xc - bw // 2)
        cols = m[:, x0:xc + bw // 2] > 0.5
        rows = np.flatnonzero(cols.any(1))
        y1 = int(rows.max()) if len(rows) else H - 1
        out.append(((x0, y0, bw, y1 - y0), (xc - hw // 2, y0, hw, yn - y0)))
    return out


def motion_cells(ma, mb):
    """Old-DVR motion grid: cells where the silhouette changed between frames."""
    d = np.abs((ma > 0.5).astype(np.float32) - (mb > 0.5).astype(np.float32))
    cells = []
    cs = 54
    for y in range(120, H - 90, cs):
        for x in range(30, W - 30, cs):
            if d[y:y + cs, x:x + cs].mean() > 0.16:
                cells.append((x, y, cs))
    return cells


def osd(img, n, nv, held, pboxes, cells, rng):
    pil = Image.fromarray((img[..., ::-1] * 255).astype(np.uint8))
    ov = Image.new("RGBA", pil.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for (x, y, cs) in cells:
        d.rectangle((x + 2, y + 2, x + cs - 2, y + cs - 2), outline=(255, 40, 40, 200), width=2)
        d.rectangle((x + 2, y + 2, x + cs - 2, y + cs - 2), fill=(255, 30, 30, 40))
    f_lab = font(22)
    for i, ((x, y, w, h), (hx, hy, hw, hh)) in enumerate(pboxes):
        j = rng.integers(-2, 3, 4)
        x0, y0, x1, y1 = x + j[0], y - 14 + j[1], x + w + j[2], min(H - 70, y + h + j[3])
        d.rectangle((x0, y0, x1, y1), outline=(235, 255, 235, 230), width=3)
        d.rectangle((hx - 6 + j[2], hy - 6, hx + hw + 6, hy + hh + 4), outline=(235, 255, 235, 200), width=2)
        conf = 0.90 + 0.08 * rng.random()
        ly = y0 - 30 if y0 > 150 else y1 - 32
        d.rectangle((x0, ly, x0 + 196, ly + 30), fill=(0, 0, 0, 150))
        d.text((x0 + 6, ly + 2), f"PERSON {conf:.2f}", font=f_lab, fill=(235, 255, 235, 255))
    pil = Image.alpha_composite(pil.convert("RGBA"), ov)
    d = ImageDraw.Draw(pil)
    fbig, fmid = font(46), font(36)

    def txt(xy, s, f, col=(245, 245, 245)):
        x, y = xy
        for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2), (2, 2)):
            d.text((x + dx, y + dy), s, font=f, fill=(0, 0, 0))
        d.text((x, y), s, font=f, fill=col)

    secs = 2 * 3600 + 14 * 60 + 31 + (n - 1) / 12
    hh, mm_, ss = int(secs // 3600), int(secs % 3600 // 60), int(secs % 60)
    txt((40, 30), f"10-18-2026 SAT {hh:02d}:{mm_:02d}:{ss:02d}", fbig)
    txt((W - 250, 30), "CAM 04", fbig)
    txt((W - 250, 86), "IR  ON" if not nv else "NV  ON", fmid, (200, 255, 200))
    txt((40, H - 78), "3F OFFICE - EAST", fmid)
    if (n // 6) % 2 == 0:
        d.ellipse((W - 232, H - 70, W - 206, H - 44), fill=(255, 30, 30))
    txt((W - 196, H - 78), "REC", fmid)
    if cells:
        txt((40, 90), "MOTION DETECTED", fmid, (255, 70, 70))
    if held:
        txt((W // 2 - 120, H - 78), "FRAME DROP", fmid, (255, 220, 120))
    return np.asarray(pil.convert("RGB"))[..., ::-1].astype(np.float32) / 255


def render(n):
    rng = np.random.default_rng(1000 + n)
    nv = NV[0] <= n <= NV[1]
    s = src_index(n)
    bgr, m = load(s)
    pbgr, pm = load(s - 1)
    lum = ir_luma(bgr, m)
    plum = ir_luma(pbgr, pm)
    img = colourize(sensor(lum, plum, rng, nv), nv, wash=n in SWITCH)
    img = cv2.remap(img, MX, MY, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    img *= VIG
    if n in TEAR:
        img = tear(img, rng)
    wm = cv2.remap(m, MX, MY, cv2.INTER_LINEAR)
    pboxes = boxes(wm)
    _, qm = load(s - 2)
    cells = [] if n in HELD else motion_cells(wm, cv2.remap(qm, MX, MY, cv2.INTER_LINEAR))
    img = osd(img, n, nv, n in HELD, pboxes, cells, rng)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), (np.clip(img, 0, 1) * 255).astype(np.uint8))
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    with Pool(8) as p:
        for n in p.imap_unordered(render, ONLY):
            pass
    print("done", len(ONLY), "->", OUT)
