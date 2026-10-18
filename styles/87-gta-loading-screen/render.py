"""GTA Loading-Screen Illustration: the clip as an airbrushed vector poster.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [all | frame numbers...]

Per frame:
  * colour is flattened with repeated bilateral filtering (vector-like shapes)
  * lightness is soft-posterised into a few cel bands and mixed with a heavily
    blurred copy, so each band keeps an airbrushed gradient
  * saturation up; shadows lean violet-blue, lights lean warm amber
  * a warm sunset key light rims the people from the left (from the mask)
  * the window recess (tracked from frame 085 by an ORB homography on the
    room only) becomes a hot sunset sky (purple -> pink -> orange ->
    yellow) with palm and skyline silhouettes anchored to the window
  * the room gets a warm golden-hour wash
  * thick clean black outline around every person, thinner black ink lines
    inside (XDoG on the flattened image, smoothed so they read as vector lines)
  * a small white loading spinner turns in the bottom-right corner
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np

FRAMES, MASKS, OUT = sys.argv[1:4]
ARGS = sys.argv[4:]
W, H = 1620, 1080


def load(n):
    img = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png")).astype(np.float32) / 255
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
    return img, m


def smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


def flatten_people(img):
    """Lighter full-res flattening for the people, so faces keep their features."""
    s = img.copy()
    for _ in range(3):
        s = cv2.bilateralFilter(s, 9, 0.08, 4)
    return s


def flatten(img):
    """Edge-preserving flattening at half res -> vector-art colour shapes."""
    s = cv2.resize(img, (W // 2, H // 2), interpolation=cv2.INTER_AREA)
    for _ in range(6):
        s = cv2.bilateralFilter(s, 11, 0.12, 8)
    return cv2.resize(s, (W, H), interpolation=cv2.INTER_CUBIC)


def cel_airbrush(flat, bands=(28, 46, 62, 78), w=3.0, blur=7, mix=0.62):
    lab = cv2.cvtColor(np.clip(flat, 0, 1), cv2.COLOR_BGR2Lab)
    L, A, B = lab[..., 0], lab[..., 1], lab[..., 2]
    post = np.full_like(L, 14.0)
    steps = [14, 36, 54, 70, 88]
    for t, lo, hi in zip(bands, steps[:-1], steps[1:]):
        post += (hi - lo) * smoothstep(t - w, t + w, L)
    soft = cv2.GaussianBlur(L, (0, 0), blur)
    L2 = mix * post + (1 - mix) * soft
    # saturate mid-tones and lights, but keep darks low-chroma (no red streaks in creases)
    chroma = 0.55 + 0.95 * smoothstep(22, 55, L2)
    A2, B2 = A * chroma, B * chroma * 1.05 + 4
    # violet-blue shadows, amber lights
    sh = 1 - smoothstep(25, 55, L2)
    hi = smoothstep(60, 90, L2)
    A2 += 3 * sh + 6 * hi
    B2 += -16 * sh + 16 * hi
    out = cv2.cvtColor(np.dstack([L2, A2, B2]).astype(np.float32), cv2.COLOR_Lab2BGR)
    return np.clip(out, 0, 1), L2


def ink_lines(flat, sigma=1.6, thr=0.012, min_area=0):
    g = cv2.cvtColor(flat, cv2.COLOR_BGR2GRAY)
    g1 = cv2.GaussianBlur(g, (0, 0), sigma)
    g2 = cv2.GaussianBlur(g, (0, 0), sigma * 1.6)
    d = g1 - 0.98 * g2
    e = 1 - (1 + np.tanh(60 * (d + thr)))  # dark where d < -thr
    e = np.clip(e, 0, 1)
    if min_area:
        b = (e > 0.5).astype(np.uint8)
        n, lab, st, _ = cv2.connectedComponentsWithStats(b)
        keep = np.zeros(n, bool)
        keep[1:] = st[1:, cv2.CC_STAT_AREA] >= min_area
        e = e * keep[lab]
    e = cv2.GaussianBlur(e, (0, 0), 1.0)
    return smoothstep(0.35, 0.6, e)


def sky_gradient(h, w, y0):
    ys = (np.arange(h, dtype=np.float32) - y0)[:, None] / max(h - y0, 1)
    ys = np.clip(ys, 0, 1)
    stops = [(0.0, (120, 60, 110)), (0.35, (110, 90, 235)), (0.62, (60, 140, 255)), (0.85, (110, 210, 255)),
             (1.0, (170, 235, 255))]   # BGR: violet -> hot pink -> orange -> yellow
    out = np.zeros((h, 1, 3), np.float32)
    for (p0, c0), (p1, c1) in zip(stops[:-1], stops[1:]):
        t = np.clip((ys - p0) / (p1 - p0), 0, 1)
        sel = (ys >= p0) & (ys <= p1)
        col = np.array(c0, np.float32) + (np.array(c1, np.float32) - np.array(c0, np.float32)) * t[..., None]
        out[sel[:, 0]] = col[sel[:, 0]]
    return np.repeat(out, w, 1) / 255


def palm(canvas, x, base, hgt, lean, col):
    pts = []
    for i in range(12):
        t = i / 11
        pts.append((x + lean * t * t * hgt, base - t * hgt))
    pts = np.array(pts)
    for i in range(11):
        th = int(max(3, hgt * 0.035 * (1.2 - pts.shape[0] and i / 14)))
        cv2.line(canvas, tuple(np.int32(pts[i])), tuple(np.int32(pts[i + 1])), col, th, cv2.LINE_AA)
    top = pts[-1]
    for ang in np.linspace(-170, 10, 7):
        a = np.deg2rad(ang)
        L = hgt * 0.42
        fr = []
        for k in range(9):
            t = k / 8
            dx = np.cos(a) * L * t
            dy = np.sin(a) * L * t + (L * 0.55) * t * t   # fronds droop
            fr.append((top[0] + dx, top[1] + dy))
        fr = np.array(fr)
        nrm = np.array([-np.sin(a), np.cos(a)])
        widths = np.sin(np.linspace(0, np.pi, 9)) * hgt * 0.045
        poly = np.concatenate([fr + nrm * widths[:, None], (fr - nrm * widths[:, None])[::-1]])
        cv2.fillPoly(canvas, [np.int32(poly)], col, cv2.LINE_AA)


REF_N = 85
# inner corners of the window recess in frame 085 (TL, TR, BR, BL)
REF_QUAD = np.float32([[325, 22], [1125, 125], [1125, 495], [320, 498]])
_REF = None


def features(img, m):
    g = (cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) * 255).astype(np.uint8)
    bgm = (cv2.dilate((m > 0.3).astype(np.uint8), np.ones((31, 31), np.uint8)) == 0).astype(np.uint8) * 255
    orb = cv2.ORB_create(3000)
    return orb.detectAndCompute(g, bgm)


def window_quad(img, m):
    """Track the window recess with a homography from frame 085 (background features only)."""
    global _REF
    if _REF is None:
        _REF = features(*load(REF_N))
    k0, d0 = _REF
    k1, d1 = features(img, m)
    if d1 is None or len(k1) < 30:
        return None
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    pairs = bf.knnMatch(d0, d1, k=2)
    good = [a for a, b in (p for p in pairs if len(p) == 2) if a.distance < 0.75 * b.distance]
    if len(good) < 25:
        return None
    src = np.float32([k0[g.queryIdx].pt for g in good])
    dst = np.float32([k1[g.trainIdx].pt for g in good])
    Hm, inl = cv2.findHomography(src, dst, cv2.RANSAC, 4.0)
    if Hm is None or inl.sum() < 20:
        return None
    return cv2.perspectiveTransform(REF_QUAD[None], Hm)[0]


def window_box(img, m):
    q = window_quad(img, m)
    if q is None:
        return None, None
    reg = np.zeros((H, W), np.uint8)
    cv2.fillPoly(reg, [np.int32(q)], 1)
    # keep the plants in front of the window: only pale, unsaturated pixels become sky
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    pale = (hsv[..., 1] < 0.22) & (hsv[..., 2] > 0.5)
    lower = np.zeros((H, W), bool)
    ys = np.arange(H)[:, None]
    lower[:] = ys > (q[:, 1].min() + 0.7 * (q[:, 1].max() - q[:, 1].min()))
    reg = (reg.astype(bool) & (~lower | pale) & (m < 0.5)).astype(np.uint8)
    x, y, w, h = cv2.boundingRect(np.int32(q))
    return (x, y, w, h), reg


def sunset_window(img, m):
    box, region = window_box(img, m)
    if box is None:
        return None, None
    x, y, w, h = box
    reg = cv2.morphologyEx(region, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    reg = cv2.GaussianBlur(reg.astype(np.float32), (0, 0), 1.2)
    sky = sky_gradient(H, W, y)
    # sun low in the window
    sun = np.zeros((H, W), np.float32)
    cx, cy = x + int(w * 0.62), y + int(h * 0.78)
    cv2.circle(sun, (cx, cy), int(min(w, h) * 0.16), 1.0, -1, cv2.LINE_AA)
    glow = cv2.GaussianBlur(sun, (0, 0), min(w, h) * 0.12)
    sky = sky + glow[..., None] * np.array([0.2, 0.45, 0.6], np.float32)
    sky = sky * (1 - sun[..., None]) + np.array([0.75, 0.93, 1.0], np.float32) * sun[..., None]
    sil = np.zeros((H, W, 3), np.uint8)
    col = (70, 30, 75)
    # skyline along the bottom of the window
    rng = np.random.default_rng(3)
    bx = x
    while bx < x + w:
        bw = int(rng.integers(w // 20, w // 9))
        bh = int(rng.integers(h // 10, h // 3))
        cv2.rectangle(sil, (bx, y + h - bh), (bx + bw, y + h + 5), col, -1)
        bx += bw + int(rng.integers(0, w // 30))
    palm(sil, x + int(w * 0.12), y + h + 10, int(h * 1.05), 0.18, col)
    palm(sil, x + int(w * 0.3), y + h + 10, int(h * 0.8), -0.12, col)
    palm(sil, x + int(w * 0.88), y + h + 10, int(h * 0.95), -0.2, col)
    silm = (sil.max(2) > 0).astype(np.float32)
    silm = cv2.GaussianBlur(silm, (0, 0), 0.8)
    sky = sky * (1 - silm[..., None]) + (np.array(col, np.float32) / 255) * silm[..., None]
    return sky, reg


def spinner(out, n):
    cx, cy, r = W - 70, H - 62, 24
    for k in range(10):
        a = np.deg2rad(k * 36 - n * 30)
        alpha = (k + 1) / 10
        p = (int(cx + r * np.cos(a)), int(cy + r * np.sin(a)))
        ov = out.copy()
        cv2.circle(ov, p, 5, (1.0, 1.0, 1.0), -1, cv2.LINE_AA)
        out[:] = out * (1 - alpha) + ov * alpha


def render(n):
    img, m = load(n)
    flat = flatten(img)
    cel, L2 = cel_airbrush(flat)
    pflat = flatten_people(img)
    pcel, _ = cel_airbrush(pflat, w=2.5, blur=3, mix=0.72)

    # golden-hour wash on the room: warm top-left, violet toward the floor
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    warm = np.dstack([np.full((H, W), 0.55), np.full((H, W), 0.75), np.full((H, W), 1.0)]).astype(np.float32)
    cool = np.dstack([np.full((H, W), 0.75), np.full((H, W), 0.45), np.full((H, W), 0.55)]).astype(np.float32)
    t = np.clip(ys / H * 0.9 + (xs / W) * 0.25, 0, 1)[..., None]
    wash = warm * (1 - t) + cool * t
    room = cel * (0.45 + 0.55 * wash) + 0.08 * wash
    sky, reg = sunset_window(img, m)
    if sky is not None:
        room = room * (1 - reg[..., None]) + sky * reg[..., None]

    # people: warm sunset rim from the left
    mm = cv2.GaussianBlur(m, (0, 0), 1.0)
    shifted = np.zeros_like(mm)
    shifted[:, 14:] = mm[:, :-14]
    rim = np.clip(mm - shifted, 0, 1)
    rim = cv2.GaussianBlur(rim, (0, 0), 4) * mm
    people = pcel + rim[..., None] * np.array([0.05, 0.35, 0.65], np.float32) * 1.4
    people = np.clip(people, 0, 1)

    out = room * (1 - mm[..., None]) + people * mm[..., None]

    # ink: interior lines (stronger on people) + thick outline around people
    ink = ink_lines(flat) * 0.35 * (1 - mm)
    ink = np.maximum(ink, ink_lines(pflat, 1.3, 0.010, 90) * 0.9 * mm)
    # outline from the filled outer contours only (holes in the mask would leave ink blobs)
    filled = np.zeros((H, W), np.uint8)
    cs, _ = cv2.findContours((m > 0.5).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(filled, [c for c in cs if cv2.contourArea(c) > 400], -1, 1, -1)
    edge = cv2.morphologyEx(filled, cv2.MORPH_GRADIENT, np.ones((9, 9), np.uint8)).astype(np.float32)
    edge = smoothstep(0.3, 0.7, cv2.GaussianBlur(edge, (0, 0), 1.5))
    ink = np.maximum(ink, edge)
    out = out * (1 - ink[..., None]) + np.array([0.06, 0.04, 0.07], np.float32) * ink[..., None]

    spinner(out, n)
    return (np.clip(out, 0, 1) * 255).astype(np.uint8)


def job(n):
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), render(n))
    return n


def main():
    os.makedirs(OUT, exist_ok=True)
    total = len([f for f in os.listdir(FRAMES) if f.startswith("frame_") and f.endswith(".png")])
    nums = list(range(1, total + 1)) if (not ARGS or ARGS == ["all"]) else [int(a) for a in ARGS]
    with Pool(3) as p:
        for _ in p.imap_unordered(job, nums):
            pass
    print("done", len(nums))


if __name__ == "__main__":
    main()
