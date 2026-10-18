"""Anime cel-shade restyle, frame by frame.

usage: python -I render.py [frame numbers...]   (default: the 6 sheet frames)
Reads ../../_source/frames + masks, writes ./frames/frame_NNN.png.

Look: flat 2-3 tone cel shading (base / cool shadow / highlight) on the people,
clean dark line art, painted background, the bright window replaced by a
painted anime sky with cel clouds, manga focus/speed lines on fast motion.
"""
import json
import os
import sys
from multiprocessing import Pool
from pathlib import Path

import cv2
import numpy as np

HERE = Path(__file__).resolve().parent
SRC = HERE.parent.parent / "_source"
FRAMES, MASKS, OUT = SRC / "frames", SRC / "masks", HERE / "frames"
SHEET = [13, 49, 85, 109, 145, 178]
LINE = np.array([0.16, 0.10, 0.14], np.float32)          # BGR, dark plum-brown ink
SHADOW_TINT = np.array([0.86, 0.66, 0.70], np.float32)   # cool lavender multiply
N = len(list(FRAMES.glob("frame_*.png")))


def read(n):
    img = cv2.imread(str(FRAMES / f"frame_{n:03d}.png"))
    m = cv2.imread(str(MASKS / f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE)
    return img, m.astype(np.float32) / 255


def flatten(img, sp, sr, passes):
    """Edge-preserving flattening at half res (mean shift + bilateral), back to full res."""
    h, w = img.shape[:2]
    s = cv2.resize(img, (w // 2, h // 2), interpolation=cv2.INTER_AREA)
    s = cv2.pyrMeanShiftFiltering(s, sp, sr)
    for _ in range(passes):
        s = cv2.bilateralFilter(s, 9, 30, 7)
    return cv2.resize(s, (w, h), interpolation=cv2.INTER_LINEAR)


def mode_filter(labels, k, size):
    """Majority filter on a label map so cel regions get clean shapes."""
    best = np.zeros(labels.shape, np.float32)
    out = labels.copy()
    for c in range(k):
        v = cv2.blur((labels == c).astype(np.float32), (size, size))
        sel = v > best
        out[sel] = c
        best[sel] = v[sel]
    return out


def drop_small(b, min_area):
    n, lab, stats, _ = cv2.connectedComponentsWithStats(b.astype(np.uint8), 8)
    keep = np.zeros(n, bool)
    keep[1:] = stats[1:, cv2.CC_STAT_AREA] >= min_area
    return keep[lab]


PALETTE = HERE / "palette.npy"                               # one cel palette for the whole clip


def lab_feat(img):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB).reshape(-1, 3).astype(np.float32)
    feat = lab.copy()
    feat[:, 0] *= 0.6                                           # cluster by material, not by light
    return lab, feat


def build_palette(k=16):
    """k-means once over person pixels from every 6th frame, so the cel colours
    (and the region split) do not jump from frame to frame."""
    rng = np.random.default_rng(7)
    samples = []
    for n in range(1, N + 1, 6):
        img, m = read(n)
        _, feat = lab_feat(flatten(img, 8, 22, 2))
        idx = np.flatnonzero(m.reshape(-1) > 0.5)
        samples.append(feat[rng.choice(idx, min(6000, len(idx)), replace=False)])
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 40, 0.5)
    _, _, centers = cv2.kmeans(np.vstack(samples), k, None, crit, 4, cv2.KMEANS_PP_CENTERS)
    np.save(PALETTE, centers)


def cel(img, mask, shade_lo, shade_hi, sat):
    """Snap the people to the fixed clip palette of flat material colours, then give
    each one exactly one cool shadow shape and (on big areas) one highlight shape."""
    h, w = img.shape[:2]
    lab, feat = lab_feat(img)
    centers = np.load(PALETTE).astype(np.float32)
    k = len(centers)
    d = ((feat[:, None, :] - centers[None]) ** 2).sum(-1)
    labels = mode_filter(d.argmin(1).reshape(h, w).astype(np.int32), k, 21)
    centers[:, 0] /= 0.6

    base = cv2.cvtColor(centers.reshape(1, k, 3).astype(np.uint8), cv2.COLOR_LAB2BGR)[0]
    hsv = cv2.cvtColor(base[None], cv2.COLOR_BGR2HSV).astype(np.float32)[0]
    skin = np.zeros(k, bool)
    hot = (hsv[:, 0] >= 3) & (hsv[:, 0] <= 22) & (hsv[:, 1] > 100) & (hsv[:, 2] > 120)   # over-orange skin
    hsv[hot, 1] *= 0.62
    hsv[hot, 2] = np.minimum(hsv[hot, 2] * 1.08 + 10, 250)
    hsv[:, 1] = np.where(skin | hot, hsv[:, 1], np.clip(hsv[:, 1] * sat, 0, 255))
    hsv[:, 2] = np.where(skin | hot, hsv[:, 2], np.clip(hsv[:, 2] * 1.06 + 8, 0, 255))
    base = cv2.cvtColor(hsv[None].astype(np.uint8), cv2.COLOR_HSV2BGR)[0].astype(np.float32) / 255
    peach = np.float32([0.78, 0.86, 0.99])
    base[skin] = base[skin] * 0.55 + peach * 0.45               # anime skin: light, clean peach

    L = cv2.GaussianBlur(lab[:, 0].reshape(h, w) / 255, (0, 0), 11)
    out = base[labels]
    kern = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
    min_area = h * w * 0.0006
    for c in range(k):
        sel = labels == c
        if sel.sum() < min_area:
            continue
        med = np.median(L[sel])
        lo = shade_lo * (1.4 if skin[c] else 1.0)
        sh = cv2.morphologyEx(((L < med - lo) & sel).astype(np.uint8), cv2.MORPH_OPEN, kern)
        sh = drop_small(cv2.GaussianBlur(sh.astype(np.float32), (0, 0), 4) > 0.5, min_area) & sel
        out[sh] = base[c] * (SHADOW_TINT if not skin[c] else np.float32([0.84, 0.78, 0.92]))
        if sel.sum() > min_area * 8:
            hi = cv2.morphologyEx(((L > med + shade_hi) & sel).astype(np.uint8), cv2.MORPH_OPEN, kern)
            hi = drop_small(cv2.GaussianBlur(hi.astype(np.float32), (0, 0), 4) > 0.5, min_area) & sel
            out[hi] = np.clip(base[c] * 1.12 + 0.07, 0, 1)
    return out


FACES = json.loads((HERE / "faces.json").read_text())        # from faces.swift (Apple Vision)


def face_regions(n, fp, hard):
    """Per detected face: skin region (ellipse in the box, minus dark hair) + landmarks."""
    h, w = hard.shape
    L = cv2.cvtColor(fp, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
    out = []
    for f in FACES.get(f"frame_{n:03d}.png", []):
        x, y, bw, bh = f["box"]
        reg = np.zeros((h, w), np.uint8)
        if "faceContour" in f:
            jaw = np.array(f["faceContour"], np.float32)
            top = np.array([[jaw[-1][0], y - bh * 0.28], [jaw[0][0], y - bh * 0.28]], np.float32)
            cv2.fillPoly(reg, [np.vstack([jaw, top]).astype(np.int32)], 1, cv2.LINE_AA)
        else:
            cv2.ellipse(reg, (int(x + bw / 2), int(y + bh * 0.55)), (int(bw * 0.45), int(bh * 0.55)), 0, 0, 360, 1, -1)
        lum_ok = cv2.GaussianBlur(L, (0, 0), 5) > 0.30
        reg = (reg > 0) & (hard > 0.5) & lum_ok
        reg = cv2.morphologyEx(reg.astype(np.uint8), cv2.MORPH_OPEN, np.ones((9, 9), np.uint8)) > 0
        if reg.sum() > 400:
            out.append((reg, f, bw))
    return out


def body_skin(fp, img, hard, faces):
    if not faces:
        return np.zeros(hard.shape, bool)
    lab = cv2.cvtColor(fp, cv2.COLOR_BGR2LAB).astype(np.float32)
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)
    tex = np.sqrt(np.clip(cv2.blur(g * g, (15, 15)) - cv2.blur(g, (15, 15)) ** 2, 0, None))
    any_face = np.zeros(hard.shape, bool)
    out = np.zeros(hard.shape, bool)
    for reg, _, _ in faces:
        any_face |= reg
        ref = np.median(lab[reg], 0)
        d = np.sqrt(((lab[..., 1:] - ref[1:]) ** 2).sum(-1)) + np.abs(lab[..., 0] - ref[0]) * 0.25
        out |= d < 9
    out &= (hard > 0.5) & (tex < 6) & ~any_face
    out = cv2.morphologyEx(out.astype(np.uint8), cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
    out = cv2.morphologyEx(out, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    return drop_small(out > 0, hard.size * 0.0015)


def paint_faces(ppl, fp, faces, extra):
    """One clean anime skin tone + one cel shadow + blush on each face."""
    src = fp.astype(np.float32) / 255
    L = cv2.GaussianBlur(cv2.cvtColor(fp, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255, (0, 0), 9)
    peach = np.float32([0.80, 0.88, 1.0])
    for reg, f, bw in faces:
        med = np.median(src[reg], 0)
        tone = np.clip(np.clip(med * 1.2 + 0.08, 0, 1) * 0.55 + peach * (0.33 + 0.15 * med.mean()), 0, 1)
        soft = cv2.GaussianBlur(reg.astype(np.float32), (0, 0), 2)[..., None]
        ppl[:] = ppl * (1 - soft) + tone * soft
        lm = np.median(L[reg])
        sh = cv2.GaussianBlur(((L < lm - 0.07) & reg).astype(np.float32), (0, 0), 6) > 0.5
        sh = drop_small(sh, 300) & reg
        ppl[sh] = tone * np.float32([0.86, 0.76, 0.90])
        if extra is not None and extra.any():                   # hands / neck in the same skin
            ex = extra.copy()
            exs = cv2.GaussianBlur(ex.astype(np.float32), (0, 0), 1.5)[..., None]
            ppl[:] = ppl * (1 - exs) + tone * exs
            esh = cv2.GaussianBlur(((L < np.median(L[ex]) - 0.08) & ex).astype(np.float32), (0, 0), 6) > 0.5
            ppl[esh & ex] = tone * np.float32([0.86, 0.76, 0.90])
            extra = None
        if "leftEye" in f and "rightEye" in f:                   # blush under each eye
            for k in ("leftEye", "rightEye"):
                e = np.array(f[k], np.float32)
                cx, cy = e[:, 0].mean(), e[:, 1].mean() + bw * 0.14
                bl = np.zeros(reg.shape, np.float32)
                cv2.ellipse(bl, (int(cx), int(cy)), (int(bw * 0.09), int(bw * 0.045)), 0, 0, 360, 1, -1)
                bl = cv2.GaussianBlur(bl, (0, 0), bw * 0.02)[..., None] * 0.45 * reg[..., None]
                ppl[:] = ppl * (1 - bl) + np.float32([0.62, 0.55, 0.98]) * bl
    return ppl


def draw_features(out, faces, rng):
    """Anime line work from the real landmarks: heavy upper lid, iris + catchlight,
    brows, a small nose tick, mouth line. Positions follow the footage exactly."""
    ink = tuple(float(v) for v in LINE)
    for reg, f, bw in faces:
        t = max(2, int(bw * 0.022))
        aa = cv2.LINE_AA
        for side in ("left", "right"):
            if f"{side}Eye" not in f:
                continue
            e = np.array(f[f"{side}Eye"], np.float32)
            c0 = e.mean(0)
            e = (e - c0) * np.float32([1.18, 2.1]) + c0 - np.float32([0, bw * 0.006])
            ew = e[:, 0].max() - e[:, 0].min()
            eh = e[:, 1].max() - e[:, 1].min()
            cy = e[:, 1].mean()
            upper = e[e[:, 1] <= cy + 0.5]
            upper = upper[np.argsort(upper[:, 0])]
            lower = e[e[:, 1] > cy]
            lower = lower[np.argsort(lower[:, 0])]
            if eh / max(ew, 1) > 0.40:                            # open eye
                hull = cv2.convexHull(e.astype(np.int32))
                cv2.fillConvexPoly(out, hull, (0.97, 0.97, 0.98), aa)
                p = np.array(f.get(f"{side}Pupil", [[e[:, 0].mean(), cy]])[0], np.float32)
                r = max(2, int(eh * 0.55))
                eye_clip = np.zeros(out.shape[:2], np.uint8)
                cv2.fillConvexPoly(eye_clip, hull, 1)
                iris = np.zeros(out.shape[:2], np.uint8)
                cv2.circle(iris, (int(p[0]), int(p[1])), r, 1, -1, aa)
                sel = (iris & eye_clip) > 0
                out[sel] = (0.20, 0.17, 0.28)
                pup = np.zeros(out.shape[:2], np.uint8)
                cv2.circle(pup, (int(p[0]), int(p[1])), max(1, int(r * 0.45)), 1, -1, aa)
                out[(pup & eye_clip) > 0] = (0.06, 0.04, 0.08)
                cv2.circle(out, (int(p[0] - r * 0.35), int(p[1] - r * 0.35)), max(1, int(r * 0.28)), (1, 1, 1), -1, aa)
                if len(lower) > 1:
                    cv2.polylines(out, [lower.astype(np.int32)], False, ink, max(1, t // 2), aa)
            if len(upper) > 1:
                cv2.polylines(out, [upper.astype(np.int32)], False, ink, int(t * 1.8), aa)
        for k in ("leftEyebrow", "rightEyebrow"):
            if k in f:
                b = np.array(f[k], np.float32)
                b = b[np.argsort(b[:, 0])]
                cv2.polylines(out, [b[: max(2, len(b) // 2 + 1)].astype(np.int32)], False, ink, t, aa)
        if "nose" in f:
            nz = np.array(f["nose"], np.float32)
            tip = nz[nz[:, 1].argmax()]
            cv2.line(out, (int(tip[0] - bw * 0.02), int(tip[1])), (int(tip[0] + bw * 0.015), int(tip[1] - bw * 0.01)), ink, max(1, t // 2), aa)
        if "innerLips" in f and "outerLips" in f:
            il = np.array(f["innerLips"], np.float32)
            ol = np.array(f["outerLips"], np.float32)
            open_h = il[:, 1].max() - il[:, 1].min()
            if open_h > bw * 0.05:
                cv2.fillPoly(out, [il.astype(np.int32)], (0.32, 0.25, 0.62), aa)
                cv2.polylines(out, [il.astype(np.int32)], True, ink, max(1, t // 2), aa)
            else:
                xs = np.argsort(ol[:, 0])
                l, r = ol[xs[0]], ol[xs[-1]]
                mid = il[:, 1].mean()
                pts = np.array([l, [(l[0] * 2 + r[0]) / 3, mid + 1], [(l[0] + r[0] * 2) / 3, mid + 1], r], np.int32)
                cv2.polylines(out, [pts], False, ink, max(1, int(t * 0.8)), aa)
    return out


def dog_lines(gray, sigma, k, t):
    """Thin cartoon line art: dark side of a difference of gaussians. 1 = ink."""
    g1 = cv2.GaussianBlur(gray, (0, 0), sigma)
    g2 = cv2.GaussianBlur(gray, (0, 0), sigma * k)
    return np.clip(((g2 - g1) - t) / t, 0, 1)


def clean_lines(ink, min_area):
    n, lab, stats, _ = cv2.connectedComponentsWithStats((ink > 0.5).astype(np.uint8), 8)
    keep = np.zeros(n, bool)
    keep[1:] = stats[1:, cv2.CC_STAT_AREA] >= min_area
    return keep[lab].astype(np.float32)


def vnoise(rng, h, w, cell):
    a = rng.random((h // cell + 2, w // cell + 2)).astype(np.float32)
    return cv2.resize(a, (w, h), interpolation=cv2.INTER_CUBIC)


def sky(h, w, n):
    """Painted anime sky: deep blue gradient + cel-shaded cumulus that drift slowly."""
    t = np.linspace(0, 1, h, dtype=np.float32)[:, None, None]
    top = np.array([0.86, 0.52, 0.18], np.float32)
    bot = np.array([0.98, 0.86, 0.66], np.float32)
    out = np.broadcast_to(top * (1 - t) + bot * t, (h, w, 3)).copy()
    rng = np.random.default_rng(7)
    cloud = np.zeros((h, w), np.uint8)
    shade = np.zeros((h, w), np.uint8)
    drift = n * 1.5
    for _ in range(7):                                           # cumulus banks, flat bottoms
        bx, by = rng.uniform(-100, w), rng.uniform(0.12, 0.55) * h
        s = rng.uniform(50, 110)
        for _ in range(int(rng.integers(6, 11))):
            x = bx + drift + rng.normal(0, s * 1.3)
            y = by - abs(rng.normal(0, s * 0.6))
            r = s * rng.uniform(0.5, 1.0)
            cv2.circle(cloud, (int(x) % (w + 200) - 100, int(y)), int(r), 1, -1, cv2.LINE_AA)
            cv2.circle(shade, (int(x) % (w + 200) - 100 + int(r * 0.15), int(y + r * 0.45)), int(r * 0.8), 1, -1, cv2.LINE_AA)
        cv2.rectangle(cloud, (0, int(by)), (w, h), 0, -1) if False else None
    c = cloud.astype(bool)
    out[c] = (0.99, 0.98, 0.97)
    out[c & shade.astype(bool)] = (0.92, 0.78, 0.80)
    return out


def focus_lines(h, w, rng, mask, strength):
    """Manga concentration lines from the frame edge toward the centre, behind the subject."""
    lay = np.zeros((h, w), np.float32)
    cx, cy = w * rng.uniform(0.45, 0.55), h * rng.uniform(0.40, 0.50)
    R = np.hypot(w, h)
    for _ in range(int(140 * strength)):
        a = rng.uniform(0, 2 * np.pi)
        r0 = R * rng.uniform(0.30, 0.48)
        half = rng.uniform(0.002, 0.007)
        pts = np.array([
            [cx + np.cos(a - half) * R, cy + np.sin(a - half) * R],
            [cx + np.cos(a + half) * R, cy + np.sin(a + half) * R],
            [cx + np.cos(a) * r0, cy + np.sin(a) * r0],
        ], np.int32)
        cv2.fillConvexPoly(lay, pts, 1.0, cv2.LINE_AA)
    return lay * (1 - mask)


def motion(n):
    if n < 3:
        return 0.0
    _, a = read(n)
    _, b = read(n - 2)
    return float(np.abs(a - b).mean())


def calm_background(n, img):
    """Average the room with the neighbour frames where nobody stands, so the painted
    background holds still instead of shimmering with sensor noise."""
    acc, wsum = img.astype(np.float32) * 2, 2.0
    _, m0 = read(n)
    for j in (n - 1, n + 1):
        if 1 <= j <= N:
            nb, mj = read(j)
            free = cv2.dilate(((m0 + mj) > 0.1).astype(np.uint8), np.ones((31, 31), np.uint8)) == 0
            acc[free] += nb.astype(np.float32)[free]
            wsum = wsum + free[..., None].astype(np.float32)
    return np.clip(acc / wsum, 0, 255).astype(np.uint8)


def render(n):
    rng = np.random.default_rng(1000 + n)
    img, m = read(n)
    h, w = m.shape
    hard = (m > 0.5).astype(np.float32)
    msoft = cv2.GaussianBlur(hard, (0, 0), 1.2)[..., None]

    # people: flatter colour fields, 3-tone cel shading, crisp line art
    fp = flatten(img, 8, 22, 2)
    ppl = cel(fp, hard, 0.07, 0.15, 1.25)
    faces = face_regions(n, fp, hard)
    ppl = paint_faces(ppl, fp, faces, body_skin(fp, img, hard, faces))
    gray = cv2.cvtColor(fp, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
    ink_p = clean_lines(dog_lines(gray, 1.4, 2.2, 0.022), 60) * hard
    face_in = np.zeros_like(hard)
    for reg, _, _ in faces:
        face_in = np.maximum(face_in, cv2.erode(reg.astype(np.uint8), np.ones((15, 15), np.uint8)).astype(np.float32))
    strong = clean_lines(dog_lines(gray, 1.2, 2.2, 0.06), 40)       # keeps glasses frames
    ink_p = ink_p * (1 - face_in) + strong * face_in

    # background: painted look, fewer lines, window -> anime sky
    fb = cv2.edgePreservingFilter(flatten(calm_background(n, img), 14, 34, 3), flags=1, sigma_s=60, sigma_r=0.35)
    bh = cv2.cvtColor(fb, cv2.COLOR_BGR2HSV).astype(np.float32)
    bh[..., 1] = np.clip(bh[..., 1] * 1.45, 0, 255)
    bh[..., 2] = np.clip(bh[..., 2] * 1.04 + 6, 0, 255)
    bg = cv2.cvtColor(bh.astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32) / 255
    bg = bg * 0.92 + np.float32([0.10, 0.04, 0.0]) * 0.08 + 0.02         # airy, slightly cool
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32) / 255
    yy = np.linspace(0, 1, h, dtype=np.float32)[:, None]
    win = ((hsv[..., 2] > 0.80) & (hsv[..., 1] < 0.16) & (yy < 0.62)).astype(np.uint8)
    win = cv2.morphologyEx(win, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
    win = cv2.morphologyEx(win, cv2.MORPH_CLOSE, np.ones((61, 61), np.uint8)).astype(np.float32)
    win = cv2.GaussianBlur(win * (1 - hard), (0, 0), 1.5)[..., None]
    bg = bg * (1 - win) + sky(h, w, n) * win
    gb = cv2.cvtColor(fb, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
    ink_b = clean_lines(dog_lines(gb, 1.8, 2.0, 0.035), 150) * (1 - win[..., 0])
    bg = bg * (1 - 0.55 * ink_b[..., None]) + LINE * 0.55 * ink_b[..., None]

    # speed / focus lines when the subject moves fast (behind the people)
    mv = np.mean([motion(j) for j in range(max(1, n - 2), min(N, n + 2) + 1)])   # smoothed: lines hold, no on/off flicker
    if mv > 0.09:                                      # only the fast moments (~25% of the clip)
        fl = focus_lines(h, w, rng, hard, min(1.6, mv / 0.03))
        bg = bg * (1 - fl[..., None]) + np.float32(0.99) * fl[..., None]

    out = bg * (1 - msoft) + ppl * msoft

    # bold outer contour around each person + inner line art
    k = np.ones((3, 3), np.uint8)
    hm = (hard * 255).astype(np.uint8)
    w_out = int(rng.integers(4, 6))
    contour = (cv2.dilate(hm, k, iterations=w_out) - cv2.erode(hm, k, iterations=1)).astype(np.float32) / 255
    contour = cv2.GaussianBlur(contour, (0, 0), 0.8)
    ink = np.maximum(ink_p, contour)
    ink = cv2.GaussianBlur(ink, (0, 0), 0.6)[..., None]
    out = out * (1 - ink) + LINE * ink

    out = draw_features(np.ascontiguousarray(out), faces, rng)

    # soft bloom on highlights (anime compositing glow), tiny paper/cel grain
    bright = np.clip(out - 0.78, 0, 1)
    out = out + cv2.GaussianBlur(bright, (0, 0), 12) * 0.6
    out += rng.normal(0, 0.008, out.shape).astype(np.float32)
    cv2.imwrite(str(OUT / f"frame_{n:03d}.png"), (np.clip(out, 0, 1) * 255).astype(np.uint8))
    return n, round(mv, 4)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    if not PALETTE.exists():
        build_palette()
    todo = [int(a) for a in sys.argv[1:]] or SHEET
    with Pool(min(6, os.cpu_count() or 4)) as pool:
        for r in pool.imap_unordered(render, todo):
            print(r, end=" ", flush=True)
    print()
