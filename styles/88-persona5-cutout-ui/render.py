"""Persona 5 Red-Black Cutout UI: the clip as a stylish red/black/white game menu.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [all | frame numbers...]

Per frame:
  * the room becomes a two-tone graphic: hot red where it is light, black where
    it is dark (deep red in between), with a black halftone dot gradient
  * big black jagged lightning shards and small white/black stars sit behind
    the people; they jitter a few px every frame
  * people become flat high-contrast 3-tone (black / grey / white) cutouts with
    a thick white paper-cut rim, a black rim outside it and a red offset shadow
  * slanted UI on top, drawn as original shapes and ransom-note lettering
    (every letter a different font, size, tilt and box colour): a date box
    along the top edge (it slides, smoothed over time, to where no head is), a stacked command menu bottom-right with the highlight cycling,
    and a slanted caption bottom-left; letters wobble slightly every frame
  * heads (the top ~260 px of each silhouette) stay in front of the UI
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
RED = (230, 18, 30)          # RGB
DRED = (120, 6, 14)
SUP = "/System/Library/Fonts/Supplemental/"
FONTS = [SUP + f for f in ("Arial Black.ttf", "Impact.ttf", "Georgia Bold.ttf", "Courier New Bold.ttf",
                           "Arial Bold Italic.ttf", "DIN Condensed Bold.ttf", "Copperplate.ttc",
                           "AmericanTypewriter.ttc", "Didot.ttc", "Futura.ttc", "Bodoni 72.ttc")]
_FC = {}
DATE_X = None                # per-frame x offset of the date box, set per worker


def date_positions(total):
    """Slide the date box along the top edge to where the heads are not, smoothed over time."""
    xs = np.arange(0, W - 420, 20)
    best = []
    for n in range(1, total + 1):
        m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE)
        top = (m[:240] > 128).astype(np.float32)
        csum = np.concatenate([[0], np.cumsum(top.sum(0))])
        cov = (csum[xs + 420] - csum[xs]) / (420 * 240)
        best.append(xs[np.argmin(cov + 0.12 * xs / W)])
    b = np.array(best, np.float32)
    k = 4
    pad = np.pad(b, k, mode="edge")
    med = np.array([np.median(pad[i:i + 2 * k + 1]) for i in range(len(b))])
    pad = np.pad(med, 6, mode="edge")
    return np.convolve(pad, np.ones(13) / 13, mode="same")[6:-6].round().astype(int)


def init(dx):
    global DATE_X
    DATE_X = dx


def font(i, size):
    key = (i, size)
    if key not in _FC:
        try:
            _FC[key] = ImageFont.truetype(FONTS[i % len(FONTS)], size)
        except OSError:
            _FC[key] = ImageFont.truetype(FONTS[0], size)
    return _FC[key]


def load(n):
    img = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png")).astype(np.float32) / 255
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
    return img, m


# ---------- ransom-note lettering ----------

def ransom(text, height, seed, n, wobble=1.5):
    """Return an RGBA image of `text`, every letter in its own font, size, tilt and box."""
    rng = np.random.default_rng(seed)
    jit = np.random.default_rng(seed * 7919 + n)
    tiles = []
    for ch in text:
        if ch == " ":
            tiles.append(None)
            continue
        fi = int(rng.integers(0, len(FONTS)))
        size = int(height * rng.uniform(0.75, 1.15))
        kind = int(rng.integers(0, 4))   # 0 white/black box, 1 black/white box, 2 red letter, 3 white letter
        f = font(fi, size)
        bb = f.getbbox(ch)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        pad = max(4, size // 8)
        tile = Image.new("RGBA", (tw + 2 * pad, th + 2 * pad), (0, 0, 0, 0))
        d = ImageDraw.Draw(tile)
        if kind == 0:
            d.rectangle((0, 0, tile.width, tile.height), fill=(0, 0, 0, 255))
            fg = (255, 255, 255, 255)
        elif kind == 1:
            d.rectangle((0, 0, tile.width, tile.height), fill=(255, 255, 255, 255))
            fg = (0, 0, 0, 255)
        elif kind == 2:
            d.rectangle((0, 0, tile.width, tile.height), fill=(0, 0, 0, 255))
            fg = RED + (255,)
        else:
            d.rectangle((0, 0, tile.width, tile.height), fill=RED + (255,))
            fg = (255, 255, 255, 255)
        d.text((pad - bb[0], pad - bb[1]), ch, font=f, fill=fg)
        ang = rng.uniform(-14, 14) + jit.uniform(-wobble, wobble)
        tiles.append(tile.rotate(ang, expand=True, resample=Image.BICUBIC))
    total = sum((t.width * 0.88 if t else height * 0.35) for t in tiles) + height
    canvas = Image.new("RGBA", (int(total), int(height * 2.2)), (0, 0, 0, 0))
    x = height * 0.2
    for t in tiles:
        if t is None:
            x += height * 0.35
            continue
        y = canvas.height // 2 - t.height // 2 + int(rng.integers(-height // 10, height // 10 + 1))
        canvas.alpha_composite(t, (int(x), max(0, y)))
        x += t.width * 0.88
    return canvas


def jag_poly(cx, cy, w, h, ang, rng, spikes=0.18):
    """Slanted parallelogram with jagged, torn corners."""
    pts = [(-w / 2, -h / 2), (w / 2, -h / 2 - h * 0.15), (w / 2 + h * 0.2, h / 2), (-w / 2 - h * 0.1, h / 2 + h * 0.1)]
    out = []
    for i in range(4):
        a, b = np.array(pts[i]), np.array(pts[(i + 1) % 4])
        out.append(a)
        for t in (0.3, 0.7):
            p = a + (b - a) * t
            nrm = np.array([-(b - a)[1], (b - a)[0]])
            nrm = nrm / (np.linalg.norm(nrm) + 1e-6)
            out.append(p + nrm * rng.uniform(-spikes, spikes) * h)
    out = np.array(out)
    c, s = np.cos(np.deg2rad(ang)), np.sin(np.deg2rad(ang))
    R = np.array([[c, -s], [s, c]])
    return [tuple(p) for p in (out @ R.T + [cx, cy])]


def bolt(cx, cy, size, ang, rng):
    """A jagged lightning-bolt shard."""
    pts = [(0, -1.0), (0.32, -0.25), (0.12, -0.2), (0.45, 0.55), (0.05, 0.05), (0.22, 0.1), (-0.3, -0.6)]
    pts = np.array(pts) * size + rng.uniform(-0.04, 0.04, (len(pts), 2)) * size
    c, s = np.cos(np.deg2rad(ang)), np.sin(np.deg2rad(ang))
    R = np.array([[c, -s], [s, c]])
    return [tuple(p) for p in (pts @ R.T + [cx, cy])]


def star(cx, cy, r, ang):
    pts = []
    for k in range(10):
        rr = r if k % 2 == 0 else r * 0.42
        a = np.deg2rad(ang + k * 36 - 90)
        pts.append((cx + rr * np.cos(a), cy + rr * np.sin(a)))
    return pts


# ---------- image layers ----------

def room_layer(img, n):
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    g = cv2.GaussianBlur(g, (0, 0), 2.0)
    out = np.empty((H, W, 3), np.float32)
    red, dred = np.array(RED, np.float32) / 255, np.array(DRED, np.float32) / 255
    t1 = g > 0.62
    t2 = (g > 0.40) & ~t1
    out[:] = 0.02
    out[t2] = dred
    out[t1] = red
    # halftone dot gradient in the lower-left / upper-right corners
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    cell = 22
    cxs, cys = (xs % cell) - cell / 2, (ys % cell) - cell / 2
    r = np.hypot(cxs, cys)
    amt = np.clip(1.25 - np.hypot(xs / W, (H - ys) / H) * 1.6, 0, 1)
    amt = np.maximum(amt, np.clip(1.1 - np.hypot((W - xs) / W, ys / H) * 1.7, 0, 1))
    dots = (r < amt * cell * 0.55) & t1
    out[dots] = 0.02
    return out[..., ::-1]   # -> BGR


def people_layer(img):
    s = img.copy()
    for _ in range(2):
        s = cv2.bilateralFilter(s, 9, 0.1, 5)
    g = cv2.cvtColor(s, cv2.COLOR_BGR2GRAY)
    g = np.clip((g - 0.5) * 1.5 + 0.55, 0, 1)
    tone = np.where(g < 0.30, 0.03, np.where(g < 0.62, 0.55, 0.97)).astype(np.float32)
    return np.dstack([tone] * 3)


def render(n):
    img, m = load(n)
    rng_fixed = np.random.default_rng(88)
    jit = np.random.default_rng(10_000 + n)
    room = room_layer(img, n)
    base = Image.fromarray((room[..., ::-1] * 255).astype(np.uint8)).convert("RGBA")

    # background shards and stars (behind people)
    sh = ImageDraw.Draw(base)
    for (cx, cy, sz, ang) in ((170, 820, 520, 20), (1480, 260, 480, -160), (830, 1030, 380, 75), (1450, 900, 300, 200)):
        p = bolt(cx + jit.integers(-4, 5), cy + jit.integers(-4, 5), sz, ang + jit.uniform(-1, 1), rng_fixed)
        sh.polygon(p, fill=(0, 0, 0, 255))
    for (cx, cy, r, col) in ((95, 600, 34, (255, 255, 255)), (1530, 520, 26, (0, 0, 0)), (720, 70, 22, (255, 255, 255)),
                             (1190, 980, 30, (0, 0, 0)), (420, 1000, 18, (255, 255, 255))):
        sh.polygon(star(cx, cy, r, 12 + n * 3), fill=col + (255,))

    # people cutout: red offset shadow, black rim, white paper rim, 3-tone person
    mb = (m > 0.5).astype(np.uint8)
    white_rim = cv2.dilate(mb, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (23, 23)))
    black_rim = cv2.dilate(white_rim, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15)))
    shadow = np.zeros_like(black_rim)
    shadow[16:, 22:] = black_rim[:-16, :-22]
    arr = np.array(base).astype(np.float32) / 255
    arr[shadow > 0, :3] = np.array((180, 0, 10), np.float32) / 255
    arr[black_rim > 0, :3] = 0.0
    arr[white_rim > 0, :3] = 1.0
    ppl = people_layer(img)[..., ::-1]
    mm = cv2.GaussianBlur(m, (0, 0), 0.8)[..., None]
    arr[..., :3] = arr[..., :3] * (1 - mm) + ppl * mm
    base = Image.fromarray((arr * 255).astype(np.uint8))
    pre = np.array(base)
    d = ImageDraw.Draw(base)

    # ---- UI layer ----
    # date box, top-left
    r1 = np.random.default_rng(1)
    ox = int(DATE_X[n - 1]) if DATE_X is not None else 0
    d.polygon(jag_poly(ox + 215 + jit.integers(-2, 3), 92, 360, 120, -8, r1), fill=(0, 0, 0, 255))
    d.polygon(jag_poly(ox + 330, 138, 160, 52, -8, r1, 0.25), fill=RED + (255,))
    t = ransom("10/18", 92, 5, n, 1.2)
    base.alpha_composite(t.rotate(8, expand=True, resample=Image.BICUBIC), (ox + 36, 10))
    t = ransom("SUN", 40, 6, n, 1.5)
    base.alpha_composite(t.rotate(8, expand=True, resample=Image.BICUBIC), (ox + 262, 100))
    t = ransom("AFTER SCHOOL", 30, 7, n, 1.0)
    base.alpha_composite(t.rotate(8, expand=True, resample=Image.BICUBIC), (ox + 40, 168))

    # stacked command menu, bottom-right; highlight cycles every second
    items = ["TALK", "PARTY", "SKILL", "ITEM", "SYSTEM"]
    hl = (n // 12) % len(items)
    r2 = np.random.default_rng(2)
    for i, word in enumerate(items):
        cx = 1380 + i * 26 + jit.integers(-2, 3)
        cy = 640 + i * 84
        if i == hl:
            d.polygon(jag_poly(cx + 12, cy + 10, 340, 78, -12, r2, 0.3), fill=RED + (255,))
            d.polygon(jag_poly(cx, cy, 320, 70, -12, r2, 0.2), fill=(255, 255, 255, 255))
        else:
            d.polygon(jag_poly(cx, cy, 280, 62, -12, r2, 0.2), fill=(0, 0, 0, 255))
        t = ransom(word, 50 if i == hl else 40, 20 + i, n, 1.8 if i == hl else 1.0)
        t = t.rotate(12, expand=True, resample=Image.BICUBIC)
        base.alpha_composite(t, (int(cx - t.width / 2), int(cy - t.height / 2)))

    # slanted caption, bottom-left
    r3 = np.random.default_rng(3)
    d.polygon(jag_poly(330 + jit.integers(-3, 4), 975, 640, 120, -7, r3, 0.22), fill=RED + (255,))
    d.polygon(jag_poly(318, 962, 600, 98, -7, r3, 0.15), fill=(0, 0, 0, 255))
    t = ransom("SHOW TIME!", 78, 9, n, 2.0).rotate(7, expand=True, resample=Image.BICUBIC)
    base.alpha_composite(t, (int(318 - t.width / 2), int(962 - t.height / 2)))

    # heads stay in front of the UI: the top ~260 px of every silhouette column (plus its rims)
    out = np.array(base)
    cols = white_rim > 0
    top = np.where(cols.any(0), cols.argmax(0), H).astype(np.float32)
    top = cv2.erode(top[None], np.ones((1, 61), np.float32))[0]      # widen to cover the whole head
    ys = np.arange(H)[:, None]
    zone = (black_rim > 0) & (ys - top[None] < 260)
    out[zone] = pre[zone]
    return cv2.cvtColor(out[..., :3], cv2.COLOR_RGB2BGR)


def job(n):
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), render(n))
    return n


def main():
    os.makedirs(OUT, exist_ok=True)
    total = len([f for f in os.listdir(FRAMES) if f.startswith("frame_") and f.endswith(".png")])
    nums = list(range(1, total + 1)) if (not ARGS or ARGS == ["all"]) else [int(a) for a in ARGS]
    dx = date_positions(total)
    with Pool(3, initializer=init, initargs=(dx,)) as p:
        for _ in p.imap_unordered(job, nums):
            pass
    print("done", len(nums))


if __name__ == "__main__":
    main()
