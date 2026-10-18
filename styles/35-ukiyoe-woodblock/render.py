"""Ukiyo-e woodblock print restyle, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [frame numbers... | all]
Frames are frame_001.png ... ; masks are person mattes with the same names.
Each frame is "carved and printed" again: mean-shift flattening, snapping to a
small set of traditional pigments (sumi, Prussian blue, indigo, beni, ochre,
tea brown, pale gofun flesh), a black key block from region boundaries and the
person outline, a bokashi gradient across the top of the wall, wood grain and
barren-rubbing mottling in the flat colours, washi paper fibres, colour blocks
slightly out of register with the key block, kento marks in the margin, a title
cartouche and a vermilion seal. Registration, mottling and fibres change every
frame; the key line follows the real pose.
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FRAMES, MASKS, OUT = sys.argv[1:4]
ARGS = sys.argv[4:]
HERE = os.path.dirname(os.path.abspath(__file__))
H, W = 1080, 1620
MARGIN = 26
MINCHO = "/System/Library/Fonts/ヒラギノ明朝 ProN.ttc"


def hexbgr(h):
    h = h.lstrip("#")
    return [int(h[4:6], 16), int(h[2:4], 16), int(h[0:2], 16)]


# pigment set (name, hex). Order matters only for readability.
PIGMENTS = [
    ("sumi", "#231f1d"), ("sumi_grey", "#6f6a62"), ("usuzumi", "#a9a397"),
    ("prussian", "#24466b"), ("indigo", "#33405a"), ("ai_light", "#8aa7b8"),
    ("beni", "#b8412c"), ("beni_light", "#d98b72"), ("ochre", "#c9973f"),
    ("kihada", "#ddc078"), ("tea", "#7c4f33"), ("tea_light", "#a87a55"),
    ("matcha", "#6f7a4b"), ("sage", "#a3a77f"), ("paper", "#ece0c6"),
    ("gofun", "#f1dfc8"),
]
PAL = np.array([hexbgr(h) for _, h in PIGMENTS], np.uint8)
NAMES = [n for n, _ in PIGMENTS]
PAL_LAB = cv2.cvtColor(PAL[None], cv2.COLOR_BGR2LAB)[0].astype(np.float32)
SKIN = NAMES.index("gofun")
PAPER = NAMES.index("paper")
SUMI = NAMES.index("sumi")


def vnoise(rng, h, w, cell):
    a = rng.random((max(2, h // cell + 2), max(2, w // cell + 2))).astype(np.float32)
    return cv2.resize(a, (w, h), interpolation=cv2.INTER_CUBIC)


def quantize(img_bgr):
    lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB).astype(np.float32)
    lab[..., 1:] = 128 + (lab[..., 1:] - 128) * 1.4
    lab[..., 0] = np.clip((lab[..., 0] - 120) * 1.15 + 125, 0, 255)
    d = ((lab[:, :, None, :] - PAL_LAB[None, None]) ** 2 * np.array([1.0, 1.6, 1.6])).sum(-1)
    return d.argmin(-1).astype(np.uint8)


def skin_mask(img, m):
    ycc = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    cr, cb, y = ycc[..., 1].astype(int), ycc[..., 2].astype(int), ycc[..., 0].astype(int)
    s = (cr > 138) & (cr < 175) & (cb > 85) & (cb < 128) & (y > 70) & (m > 0.5)
    s = cv2.morphologyEx(s.astype(np.uint8), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    s = cv2.morphologyEx(s, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    return s.astype(bool)


def carve(mask_u8, rng, width):
    """Turn a thin line mask into a carved key line: thickness varies along the line."""
    thick = cv2.dilate(mask_u8, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (width, width)))
    thin = cv2.dilate(mask_u8, np.ones((2, 2), np.uint8))
    var = vnoise(rng, H, W, 40) > 0.45
    out = np.where(var, thick, thin)
    # chisel nicks: tiny breaks in the line
    nick = vnoise(rng, H, W, 6) > 0.9
    out[nick & (thick > 0) & ~(mask_u8 > 0)] = 0
    return out


CART = None


def cartouche_slot():
    """Pick the top-strip slot that people cover least over the whole clip (cached)."""
    global CART
    if CART is not None:
        return CART
    path = os.path.join(HERE, "cartouche_slot.txt")
    if os.path.exists(path):
        CART = tuple(int(v) for v in open(path).read().split())
        return CART
    acc = np.zeros((H, W), np.float32)
    for n in range(1, 180, 6):
        acc += cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), 0).astype(np.float32) / 255
    best, bw, bh = None, 92, 330
    for x in range(MARGIN + 30, W - MARGIN - bw - 30, 10):
        y = MARGIN + 34
        cost = acc[y:y + bh, x - 20:x + bw + 20].sum()
        if best is None or cost < best[0]:
            best = (cost, x, y)
    CART = (best[1], best[2])
    open(path, "w").write(f"{CART[0]} {CART[1]}")
    return CART


def draw_text_layer(rng):
    """Cartouche with a title in mincho and a small vermilion seal."""
    x, y = cartouche_slot()
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    bw, bh = 92, 330
    d.rectangle((x, y, x + bw, y + bh), fill=(236, 214, 160, 255), outline=(35, 31, 29, 255), width=3)
    d.rectangle((x + 7, y + 7, x + bw - 7, y + bh - 7), outline=(35, 31, 29, 255), width=1)
    f = ImageFont.truetype(MINCHO, 50, index=1) if os.path.exists(MINCHO) else ImageFont.load_default()
    for i, ch in enumerate("浮世三人図"):
        d.text((x + 21, y + 18 + i * 60), ch, font=f, fill=(35, 31, 29, 255))
    # seal below the cartouche
    sx, sy = x + 18, y + bh + 22
    d.rectangle((sx, sy, sx + 56, sy + 56), fill=(184, 56, 40, 235))
    fs = ImageFont.truetype(MINCHO, 24, index=1) if os.path.exists(MINCHO) else ImageFont.load_default()
    for i, ch in enumerate("写画"):
        d.text((sx + 16, sy + 3 + i * 26), ch, font=fs, fill=(240, 220, 190, 255))
    arr = np.array(lay).astype(np.float32) / 255
    return arr[..., [2, 1, 0]], arr[..., 3:]


def washi(rng):
    """Cream paper with long kozo fibres; a new sheet every frame."""
    base = np.array(hexbgr("#efe4cb"), np.float32) / 255
    tone = 1 + 0.035 * (vnoise(rng, H, W, 90) - 0.5) + 0.02 * (vnoise(rng, H, W, 9) - 0.5)
    paper = base[None, None] * tone[..., None]
    fib = np.zeros((H, W), np.uint8)
    for _ in range(420):
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        a = rng.uniform(0, np.pi)
        L = rng.uniform(15, 70)
        pts = []
        for t in np.linspace(0, 1, 8):
            a += rng.normal(0, 0.25)
            x += np.cos(a) * L / 8
            y += np.sin(a) * L / 8
            pts.append((x, y))
        cv2.polylines(fib, [np.array(pts, np.int32)], False, int(rng.integers(90, 255)), 1, cv2.LINE_AA)
    f = fib.astype(np.float32)[..., None] / 255
    return paper, f


def render(n):
    rng = np.random.default_rng(n * 104729)
    img = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png"))
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), 0).astype(np.float32) / 255
    person = m > 0.5

    small = cv2.resize(img, (W // 2, H // 2), interpolation=cv2.INTER_AREA)
    ms = cv2.pyrMeanShiftFiltering(small, 9, 26, maxLevel=1)
    ms = cv2.resize(ms, (W, H), interpolation=cv2.INTER_LINEAR)
    lab = quantize(ms)

    # flesh -> pale gofun, hair -> sumi, garments -> one flat pigment each + printed pattern,
    # background -> paper / pale tints; then flatten the label map
    sk = skin_mask(img, m)
    bg = ~person
    lum = cv2.cvtColor(ms, cv2.COLOR_BGR2GRAY).astype(np.float32)
    near_face = cv2.dilate(sk.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (161, 161))) > 0
    hair = person & (lum < 60) & ~sk & near_face
    hair = cv2.morphologyEx(hair.astype(np.uint8), cv2.MORPH_OPEN, np.ones((7, 7), np.uint8)) > 0
    cloth = person & ~sk & ~hair
    mf = cloth.astype(np.float32)
    w = cv2.GaussianBlur(mf, (0, 0), 22) + 1e-4
    flat = (cv2.GaussianBlur(ms.astype(np.float32) * mf[..., None], (0, 0), 22) / w[..., None]).clip(0, 255).astype(np.uint8)
    flat = quantize(flat)
    flat[(flat == SUMI)] = NAMES.index("indigo")
    lab[cloth] = flat[cloth]
    lab[hair] = SUMI
    lab[sk] = SKIN
    bglab = lab.copy()
    bglab[bg & (lum > 150)] = PAPER
    lab = np.where(bg, bglab, lab).astype(np.uint8)
    lab = cv2.medianBlur(lab, 9)
    lab = cv2.medianBlur(lab, 7)
    # garment pattern (batik, stripes): print the darker detail in a darker pigment
    g0 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)
    det = cv2.GaussianBlur(g0, (0, 0), 1.5) - cv2.GaussianBlur(g0, (0, 0), 9)
    pat = (det < -13) & cloth
    pat = cv2.morphologyEx(pat.astype(np.uint8), cv2.MORPH_OPEN, np.ones((2, 2), np.uint8)) > 0
    darker = {NAMES.index(a): NAMES.index(b) for a, b in [
        ("tea_light", "tea"), ("tea", "sumi"), ("ochre", "tea"), ("kihada", "ochre"), ("paper", "usuzumi"),
        ("gofun", "usuzumi"), ("usuzumi", "sumi_grey"), ("sumi_grey", "sumi"), ("sage", "matcha"),
        ("matcha", "sumi"), ("ai_light", "prussian"), ("prussian", "sumi"), ("indigo", "sumi"),
        ("beni_light", "beni"), ("beni", "sumi")]}
    lut = np.arange(len(PAL), dtype=np.uint8)
    for a, b in darker.items():
        lut[a] = b
    base = lab.copy()
    lab[pat] = lut[lab[pat]]

    # key block: region boundaries (thin), person outline (heavy), face features (fine)
    bnd = np.zeros((H, W), np.uint8)
    bnd[:, 1:] |= (base[:, 1:] != base[:, :-1]).astype(np.uint8)
    bnd[1:, :] |= (base[1:, :] != base[:-1, :]).astype(np.uint8)
    bnd[bg & (vnoise(np.random.default_rng(3), H, W, 30) > 0.62)] = 0      # fewer lines in the room
    mu = (m > 0.5).astype(np.uint8)
    outline = cv2.morphologyEx(mu, cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8))
    g = cv2.GaussianBlur(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), (0, 0), 1.6)
    feat = cv2.Canny(g, 40, 90)
    face = cv2.dilate(sk.astype(np.uint8), np.ones((7, 7), np.uint8)) > 0
    feat = ((feat > 0) & face).astype(np.uint8)
    key = np.maximum(carve(bnd * 255, rng, 4), carve(outline * 255, rng, 7))
    key = np.maximum(key, cv2.dilate(feat * 255, np.ones((2, 2), np.uint8)))

    # colour blocks: flat pigment, out of register with the key block
    col = PAL[lab].astype(np.float32) / 255
    dx, dy = rng.integers(-3, 4, 2)
    col = np.roll(col, (int(dy), int(dx)), (0, 1))

    # bokashi: Prussian blue fading down from the top edge over the room
    yy = np.arange(H, dtype=np.float32)[:, None]
    bok = np.clip(1 - (yy - MARGIN) / (H * 0.38), 0, 1) ** 1.6
    bok = bok * (1 + 0.06 * (vnoise(rng, H, W, 120) - 0.5))
    blue = np.array(hexbgr("#2a4d74"), np.float32) / 255
    bgmask = np.roll(bg, (int(dy), int(dx)), (0, 1)).astype(np.float32)[..., None]
    a_b = (bok[..., None] * 0.92) * bgmask
    col = col * (1 - a_b) + blue * a_b
    # second bokashi: a soft beni glow along the floor
    bok2 = np.clip((yy - H * 0.82) / (H * 0.18), 0, 1) ** 1.4
    beni = np.array(hexbgr("#c9785e"), np.float32) / 255
    a_r = (bok2[..., None] * 0.45) * bgmask
    col = col * (1 - a_r) + beni * a_r

    paper, fib = washi(rng)
    # pigment printed on paper: multiply, with barren mottling + wood grain in big flats
    grain_dir = np.arange(W, dtype=np.float32)[None] * 0.09 + 6 * vnoise(np.random.default_rng(21), H, W, 160)
    wood = 0.975 + 0.025 * np.sin(grain_dir * 0.6 + yy * 0.004)
    mottle = 0.9 + 0.12 * vnoise(rng, H, W, 14) + 0.05 * vnoise(rng, H, W, 3)
    mottle = np.where(lab == SKIN, 1 + (mottle - 1) * 0.3, mottle)
    ink = col * (mottle * wood)[..., None]
    # pigment soaks into paper: tiny bleed at block edges
    ink = cv2.GaussianBlur(ink, (0, 0), 0.8)
    paper_amt = np.where(lab[..., None] == PAPER, 1.0, 0.0)
    bpaper = paper * (1 - a_b - a_r) + paper * (blue * a_b + beni * a_r) / np.maximum(paper.mean(), 1e-3) * 0.95
    out = np.where(paper_amt > 0, bpaper, ink * (0.92 + 0.08 * paper / paper.max()))
    # thin unprinted paper gaps where colour block and key block disagree
    gap = cv2.dilate(key, np.ones((3, 3), np.uint8)) > 0
    gap = gap & (np.roll(key, (2, 2), (0, 1)) == 0) & (vnoise(rng, H, W, 25) > 0.55)
    out[gap] = out[gap] * 0.35 + paper[gap] * 0.65

    # hair: dense sumi with fine combed strands
    if hair.any():
        strands = (np.sin((np.arange(W)[None] * 0.7 + yy * 0.25) + 3 * vnoise(rng, H, W, 30)) > 0.93)
        hs = hair & strands
        out[hs] = out[hs] * 0.7 + 0.3 * np.array([0.35, 0.33, 0.32])

    # key block in sumi, slightly uneven density
    ka = (key.astype(np.float32) / 255 * (0.85 + 0.15 * vnoise(rng, H, W, 8)))[..., None]
    sumi = np.array(hexbgr("#1d1a19"), np.float32) / 255
    out = out * (1 - ka) + sumi * ka

    # fibres show through the ink a little
    out = out * (1 - 0.06 * fib) + 0.04 * fib

    # cartouche + seal
    tb, ta = draw_text_layer(rng)
    out = out * (1 - ta) + tb * ta * (0.95 + 0.05 * paper / paper.max())

    # margin + border line + kento marks
    edge = np.ones((H, W), bool)
    edge[MARGIN:H - MARGIN, MARGIN:W - MARGIN] = False
    out[edge] = paper[edge] * 1.02
    o8 = np.clip(out * 255, 0, 255).astype(np.uint8)
    cv2.rectangle(o8, (MARGIN, MARGIN), (W - MARGIN - 1, H - MARGIN - 1), (29, 26, 25), 3)
    kc = (120, 110, 100)
    cv2.line(o8, (W - MARGIN - 70, H - 10), (W - MARGIN - 10, H - 10), kc, 2)   # kagi (L) mark
    cv2.line(o8, (W - MARGIN - 10, H - 10), (W - MARGIN - 10, H - 22), kc, 2)
    cv2.line(o8, (MARGIN + 20, H - 10), (MARGIN + 110, H - 10), kc, 2)           # hikitsuke mark
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), o8)
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    cartouche_slot()
    nums = list(range(1, 180)) if (not ARGS or ARGS == ["all"]) else [int(a) for a in ARGS]
    with Pool(6) as p:
        for n in p.imap_unordered(render, nums):
            print(n, end=" ", flush=True)
    print()
