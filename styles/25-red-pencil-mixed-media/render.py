"""Red-pencil mixed-media restyle, frame by frame.

usage: python render.py <frames_dir> <masks_dir> <out_dir> [frame numbers...]
The room stays a full-colour photograph. Each person becomes a black-and-white
graphite drawing on white paper (photo tones kept underneath so faces stay
recognisable), with RED colored-pencil hatching on their clothes, a red pencil
contour, and a torn white paper rim against the colour background. Strokes are
redrawn every frame so the drawing boils.
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np

FRAMES, MASKS, OUT = sys.argv[1:4]
ONLY = [int(a) for a in sys.argv[4:]]
N = len([f for f in os.listdir(FRAMES) if f.endswith(".png")])

RED = np.array([0.16, 0.12, 0.86], np.float32)     # BGR colored-pencil red
PAPER = np.array([0.93, 0.95, 0.96], np.float32)


def vnoise(rng, h, w, cell):
    a = rng.random((max(2, h // cell + 2), max(2, w // cell + 2))).astype(np.float32)
    return cv2.resize(a, (w, h), interpolation=cv2.INTER_CUBIC)


def strokes(rng, h, w, angle, length, density):
    """Pencil hatch texture: noise smeared along one direction -> streaks in 0..1."""
    k = np.zeros((length, length), np.float32)
    c = length // 2
    dx, dy = np.cos(np.radians(angle)), np.sin(np.radians(angle))
    for t in np.linspace(-c, c, length * 2):
        k[int(round(c + t * dy)) % length, int(round(c + t * dx)) % length] = 1
    k /= k.sum()
    nz = (rng.random((h, w)) < density).astype(np.float32)
    s = cv2.filter2D(nz, -1, k)
    return np.clip(s * length * 0.9, 0, 1)


def torn_cut(mask_u8, rng):
    m = cv2.GaussianBlur(mask_u8.astype(np.float32) / 255, (0, 0), 2.0)
    h, w = m.shape
    jag = (vnoise(rng, h, w, 18) - 0.5) * 0.3 + (vnoise(rng, h, w, 5) - 0.5) * 0.12
    cut = ((m + jag) > 0.5).astype(np.uint8)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(cut, 8)
    keep = np.zeros(n, bool)
    keep[1:] = stats[1:, cv2.CC_STAT_AREA] > 4000
    return keep[lab]


def pencil_outline(region, rng, h, w):
    """Broken, slightly doubled red pencil contour around the cut-out."""
    lay = np.zeros((h, w), np.uint8)
    contours, _ = cv2.findContours(region.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for c in contours:
        if len(c) < 200:
            continue
        p = c[:, 0, :].astype(np.float32)
        k = 9
        p = np.stack([np.convolve(np.r_[p[-k:, i], p[:, i], p[:k, i]], np.ones(k) / k, "same")[k:-k]
                      for i in range(2)], 1)[::3]
        edge = (p[:, 0] < 4) | (p[:, 0] > w - 5) | (p[:, 1] < 4) | (p[:, 1] > h - 5)
        i = 0
        while i < len(p):
            L = int(rng.integers(10, 45))
            seg = p[i:i + L + 1] + rng.normal(0, 1.2, 2)
            i += L - int(rng.integers(0, 4))                  # strokes overlap a little
            if rng.random() < 0.18 or edge[i - L:i].any() or len(seg) < 3:
                continue
            cv2.polylines(lay, [seg.astype(np.int32)], False, 255, int(rng.integers(2, 5)), cv2.LINE_AA)
            if rng.random() < 0.35:
                cv2.polylines(lay, [(seg + rng.normal(0, 2.5, 2)).astype(np.int32)], False, 255, 2, cv2.LINE_AA)
    a = lay.astype(np.float32) / 255
    return a * (0.55 + 0.45 * (rng.random((h, w)) > 0.3))   # pencil grain on paper tooth



def heads(bgr, mask_u8):
    """Head zones (face + hair) to keep in graphite: the topmost skin blob under each head of the mask."""
    h, w = mask_u8.shape
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    ycc = cv2.cvtColor(bgr, cv2.COLOR_BGR2YCrCb)
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    m = mask_u8 > 127
    sk = ((ycc[..., 1] > 140) & (ycc[..., 1] < 170) & (ycc[..., 2] > 90) & (ycc[..., 2] < 122)
          & (hsv[..., 1] > 40) & (hsv[..., 1] < 170) & (gray > 80) & m).astype(np.uint8)
    sk = cv2.morphologyEx(sk, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    sk = cv2.morphologyEx(sk, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8))
    top = np.where(m.any(0), m.argmax(0), h).astype(np.float32)
    top = cv2.erode(top[None], np.ones((1, 61), np.uint8))[0]          # local highest point of the silhouette
    n, lab, st, _ = cv2.connectedComponentsWithStats(sk, 8)
    head = np.zeros((h, w), np.uint8)
    taken = []
    for i in sorted(range(1, n), key=lambda i: st[i][1]):
        x, y, bw, bh, a = st[i]
        if a < 1500:
            continue
        blob = lab == i
        rows = blob[y:y + 60, x:x + bw]
        cx = int(x + np.nonzero(rows)[1].mean())
        if y - top[cx] > 260:
            continue
        # head width = the mask run (hair included) through cx just below the skin top
        row = m[min(h - 1, y + 20)]
        l = r = cx
        while l > 0 and row[l - 1]:
            l -= 1
        while r < w - 1 and row[r + 1]:
            r += 1
        Wh = r - l + 1
        if Wh < 50 or Wh > 0.62 * w:
            continue
        if any(a0 <= cx <= a1 and y > b0 for a0, a1, b0 in taken):    # under a face already found
            continue
        tw = np.median(rows.sum(1)[rows.sum(1) > 0])
        if tw < 0.22 * Wh or y - top[cx] > 0.8 * Wh:
            continue
        # a face has dark hair right above it (or touches the frame top); an arm has shirt above
        if y > 15:
            sl = (slice(max(0, y - 40), y), slice(max(0, cx - int(Wh * 0.3)), cx + int(Wh * 0.3)))
            am = m[sl]
            if am.sum() < 50 or (gray[sl][am] < 80).mean() < 0.35:
                continue
        x0, x1 = max(0, int(cx - 0.6 * Wh)), min(w, int(cx + 0.6 * Wh))
        y1 = min(h, int(y + 1.15 * Wh))
        face = np.zeros((h, w), np.uint8)
        face[y:y1, x0:x1] = blob[y:y1, x0:x1]
        cv2.fillConvexPoly(head, cv2.convexHull(cv2.findNonZero(face)), 1)
        yh = int(y + 0.3 * Wh)
        head[:yh, x0:x1] |= m[:yh, x0:x1].astype(np.uint8)
        taken.append((x0, x1, y))
    head = cv2.dilate(head, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 31)))
    return cv2.GaussianBlur(head.astype(np.float32), (0, 0), 6)


def render(n):
    rng = np.random.default_rng(5500 + n)
    bgr = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png"))
    mask_u8 = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE)
    h, w = mask_u8.shape
    img = bgr.astype(np.float32) / 255

    # background: the real colour photo, a touch richer
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[..., 1] = np.clip(hsv[..., 1] * 1.2, 0, 255)
    bg = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32) / 255

    # graphite drawing of the person
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    g = cv2.createCLAHE(clipLimit=2.2, tileGridSize=(8, 8)).apply(gray).astype(np.float32) / 255
    blur = cv2.GaussianBlur(1 - g, (0, 0), 9)
    dodge = np.clip(g / np.maximum(1 - blur, 0.05), 0, 1)               # classic pencil-sketch dodge
    tone = np.clip(0.5 * dodge + 0.5 * np.clip((g - 0.08) / 0.85, 0, 1), 0, 1)
    dark = 1 - tone
    hatch = strokes(rng, h, w, 48 + rng.normal(0, 3), 17, 0.035)
    cross = strokes(rng, h, w, -42 + rng.normal(0, 3), 13, 0.03)
    graphite = 1 - hatch * np.clip(dark * 1.6 - 0.15, 0, 1) * 0.55 - cross * np.clip(dark * 1.8 - 0.9, 0, 1) * 0.5
    g1, g2 = cv2.GaussianBlur(g, (0, 0), 1.0), cv2.GaussianBlur(g, (0, 0), 2.2)
    dog = g1 - g2
    lines = np.clip(-dog * 9 - 0.12, 0, 1) * (0.6 + 0.4 * vnoise(rng, h, w, 7))
    paper_t = 0.97 + (vnoise(rng, h, w, 3) - 0.5) * 0.06
    draw = (tone * 0.85 + 0.15) * graphite * (1 - lines * 0.8) * paper_t
    sketch = PAPER[None, None] * draw[..., None]
    sketch = sketch * np.array([1.0, 0.99, 0.97], np.float32)            # faint warm graphite sheen

    # red colored pencil on the clothes (not faces, not hair)
    head = heads(bgr, mask_u8)
    # dark hair only near a head (long hair hangs below the face); a black shirt still gets red
    hz = np.zeros((h, w), np.uint8)
    nh, hlab, hst, _ = cv2.connectedComponentsWithStats((head > 0.5).astype(np.uint8), 8)
    for i in range(1, nh):
        k = max(9, int(hst[i][3] * 0.2)) | 1                         # zone scales with the head's size
        z = cv2.dilate((hlab == i).astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))
        z[k:] |= z[:-k]                                                  # long hair hangs below the face
        hz |= z
    hair = cv2.GaussianBlur(cv2.dilate(((gray < 48) & (hz > 0)).astype(np.uint8), np.ones((7, 7), np.uint8))
                            .astype(np.float32), (0, 0), 4)
    cloth = np.clip(1 - head * 1.5 - hair * 1.2, 0, 1)
    rhatch = strokes(rng, h, w, 62 + rng.normal(0, 4), 23, 0.06)
    rh = np.clip((rhatch - 0.25) * 2.2, 0, 1)                             # visible pencil strokes
    press = 0.3 + 0.7 * np.clip(dark * 1.6 - 0.05, 0, 1)                # light clothes get pale red, dark ones dense
    ra = np.clip(cloth * (press * (0.35 + 0.65 * rh)), 0, 1) * 0.92
    pigment = RED[None, None] * (0.55 + 0.45 * tone[..., None]) * paper_t[..., None]
    sketch = sketch * (1 - ra[..., None]) + pigment * ra[..., None]
    rl = np.clip(lines * cloth * 1.2, 0, 1)                                 # fold lines in red too
    sketch = sketch * (1 - rl[..., None] * 0.6) + RED * 0.6 * rl[..., None] * 0.6

    # torn paper cut-out with white rim, laid on the colour photo
    cut = torn_cut(mask_u8, rng)
    dist = cv2.distanceTransform((~cut).astype(np.uint8), cv2.DIST_L2, 5)
    width = 5 + 9 * vnoise(np.random.default_rng(77), h, w, 120) + (vnoise(rng, h, w, 9) - 0.5) * 4
    rim = (dist > 0) & (dist < width)
    region = cut | rim
    shadow = cv2.GaussianBlur(np.roll(region.astype(np.float32), (6, 5), (0, 1)), (0, 0), 5) * 0.4
    out = bg * (1 - shadow[..., None])
    fib = PAPER * (0.97 + rng.normal(0, 0.012, (h, w, 1)))
    out = np.where(rim[..., None], fib, out)
    out = np.where(cut[..., None], sketch, out)
    ol = pencil_outline(region, rng, h, w)
    out = out * (1 - ol[..., None] * 0.9) + RED * ol[..., None] * 0.9

    out += rng.normal(0, 0.008, (h, w, 1))
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), (out.clip(0, 1) * 255).astype(np.uint8))
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    todo = ONLY or list(range(1, N + 1))
    with Pool(min(8, os.cpu_count() or 4)) as pool:
        for n in pool.imap_unordered(render, todo):
            print(n, end=" ", flush=True)
    print()
