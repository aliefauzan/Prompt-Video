"""3D Kawaii Chibi — local approximation of the frame-by-frame restyle.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [all | 13 49 85 ...]

Needs faces.json next to this script (Apple Vision boxes + landmarks for every
source frame): `swift faces.swift ../../_source/frames faces.json`.

Per frame:
  1. chibi proportions: a smooth radial "bulge" warp enlarges every head
     (about 1.35x at the centre, neck squeezed), a second bulge enlarges the
     eyes; image and person mask are warped together. Face boxes are smoothed
     over +-3 frames (and bridged over missed detections) so heads don't pulse.
  2. toy material: edge-preserving smoothing flattens skin, hair and cloth into
     soft vinyl/clay-plastic surfaces; a height field (inflated person mask +
     low-frequency luminance) is lit like a 3D render: warm golden key from the
     upper left, cool lilac fill, golden rim/back light, soft specular sheen,
     warm subsurface tint in the terminator.
  3. kawaii face: two catchlights in each eye, soft pink blush on the cheeks.
  4. dreamy world: room blurred into pastel bokeh with glowing highlight discs,
     golden haze, bloom, lifted creamy pastel grade. No boil — a clean 3D render.
"""
import json
import sys
from pathlib import Path

import cv2
import numpy as np

HERE = Path(__file__).resolve().parent
W, H = 1620, 1080
FACES = json.loads((HERE / "faces.json").read_text())


def face_list(n):
    out = []
    for f in FACES.get(f"frame_{n:03d}.png", []):
        x, y, w, h = f["box"]
        d = {"c": np.array([x + w / 2, y + h / 2]), "w": w}
        eyes = []
        for k in ("leftPupil", "rightPupil"):
            ek = "leftEye" if k == "leftPupil" else "rightEye"
            if ek in f:
                pts = np.array(f[ek])
                ew = pts[:, 0].max() - pts[:, 0].min()
                ctr = np.array(f[k][0]) if k in f else pts.mean(0)
                eyes.append((ctr - d["c"]) / w)       # eye offset in face units
                d.setdefault("ew", []).append(ew / w)
                d.setdefault("open", []).append((pts[:, 1].max() - pts[:, 1].min()) / max(ew, 1))
        d["eyes"] = eyes
        out.append(d)
    return out


def smoothed_faces(n):
    """Average each face over frames n-3..n+3 (matched by centre distance); bridge 1-3 frame dropouts."""
    window = {k: face_list(k) for k in range(max(1, n - 3), min(179, n + 3) + 1)}
    seeds = [dict(f, seen=True) for f in window.get(n, [])]
    # bridge: a face seen both before and after n but not in n
    for k in range(n - 3, n):
        for f in window.get(k, []):
            if any(np.linalg.norm(f["c"] - s["c"]) < 0.6 * f["w"] for s in seeds):
                continue
            after = [g for kk in range(n + 1, n + 4) for g in window.get(kk, [])
                     if np.linalg.norm(g["c"] - f["c"]) < 0.6 * f["w"]]
            if after:
                seeds.append(dict(f, seen=False))
    out = []
    for s in seeds:
        group = [f for k, fs in window.items() for f in fs
                 if np.linalg.norm(f["c"] - s["c"]) < 0.5 * s["w"]]
        c = np.mean([g["c"] for g in group], 0)
        w = float(np.mean([g["w"] for g in group]))
        eyes = s["eyes"]
        eg = [g for g in group if len(g["eyes"]) == len(eyes)]
        if eyes and eg:
            eyes = list(np.mean([g["eyes"] for g in eg], 0))
        ew = float(np.mean([np.mean(g["ew"]) for g in group if "ew" in g])) if any("ew" in g for g in group) else 0.18
        op = float(np.mean([np.mean(g["open"]) for g in group if "open" in g])) if any("open" in g for g in group) else 0.3
        out.append({"c": c, "w": w, "eyes": eyes, "ew": ew, "open": op, "seen": s["seen"]})
    return out


def bulge_inv(px, py, c, R, s):
    """Inverse map of a radial magnifier: output (px,py) -> source coords."""
    dx, dy = px - c[0], py - c[1]
    d2 = (dx * dx + dy * dy) / (R * R)
    f = np.where(d2 < 1, 1 - (1 - 1 / s) * (1 - np.minimum(d2, 1)) ** 2, 1.0)
    return c[0] + dx * f, c[1] + dy * f


def bulge_fwd(p, c, R, s):
    q = np.array(p, float)
    for _ in range(25):
        d2 = ((q - c) ** 2).sum() / (R * R)
        f = 1 - (1 - 1 / s) * (1 - min(d2, 1)) ** 2 if d2 < 1 else 1.0
        q = c + (np.array(p) - c) / f
    return q


def chibi_warp(img, mask, faces):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    qx, qy = xx.copy(), yy.copy()
    heads, eyes_out = [], []
    for f in faces:
        hc = f["c"] + np.array([0, -0.10 * f["w"]])
        heads.append((hc, 1.3 * f["w"], 1.6))
    for hc, R, s in heads:
        qx, qy = bulge_inv(qx, qy, hc, R, s)
    sx, sy = qx.copy(), qy.copy()
    for f in faces:
        if not f["seen"]:
            continue    # bridged: keep the head size steady, but no eye bulge on whatever hides the face
        for e in f["eyes"]:
            ec = f["c"] + e * f["w"]
            R = max(14.0, 1.25 * f["ew"] * f["w"])
            sx, sy = bulge_inv(sx, sy, ec, R, 1.3)
            # where does this eye land in the output?
            p = ec
            for hc, Rh, s in heads:
                p = bulge_fwd(p, hc, Rh, s)
            scale = 1.3 * 1.6
            eyes_out.append((p, f["ew"] * f["w"] * scale, f))
    sx, sy = sx.astype(np.float32), sy.astype(np.float32)
    wi = cv2.remap(img, sx, sy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    wm = cv2.remap(mask, sx, sy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    return wi, wm, eyes_out


def toy_shade(img, mask):
    small = cv2.resize(img, (W // 3, H // 3), interpolation=cv2.INTER_AREA)
    small = cv2.pyrMeanShiftFiltering(small, 7, 22)
    for _ in range(3):
        small = cv2.bilateralFilter(small, 9, 30, 6)
    alb = cv2.resize(small, (W, H), interpolation=cv2.INTER_CUBIC).astype(np.float32)
    alb = cv2.GaussianBlur(alb, (0, 0), 2.0)
    # pastel / toy albedo: lighter, softly saturated, warm
    hsv = cv2.cvtColor(np.clip(alb, 0, 255).astype(np.uint8), cv2.COLOR_RGB2HSV).astype(np.float32)
    hsv[..., 1] = np.clip(hsv[..., 1] * 1.3 + 14, 0, 255)
    hsv[..., 2] = np.clip(hsv[..., 2] * 0.78 + 62, 0, 255)
    alb = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB).astype(np.float32)
    # height field: inflated silhouette + low-frequency luminance relief
    mb = (mask > 0.5).astype(np.uint8)
    dist = cv2.distanceTransform(mb, cv2.DIST_L2, 5)
    D = 70.0
    t = np.clip(dist / D, 0, 1)
    hgt = np.sqrt(1 - (1 - t) ** 2) * D
    lum = cv2.GaussianBlur(alb.mean(2), (0, 0), 16)
    hgt = cv2.GaussianBlur(hgt, (0, 0), 5) + lum * 0.07
    gx = cv2.Sobel(hgt, cv2.CV_32F, 1, 0, ksize=5) / 32
    gy = cv2.Sobel(hgt, cv2.CV_32F, 0, 1, ksize=5) / 32
    nz = 1.0 / np.sqrt(gx * gx + gy * gy + 1)
    nx, ny = -gx * nz, -gy * nz
    key = np.array([-0.55, -0.6, 0.58]); key /= np.linalg.norm(key)
    fill = np.array([0.7, 0.1, 0.7]); fill /= np.linalg.norm(fill)
    lk = np.clip(nx * key[0] + ny * key[1] + nz * key[2], 0, 1)
    lf = np.clip(nx * fill[0] + ny * fill[1] + nz * fill[2], 0, 1)
    rim = (1 - nz) ** 2.2
    halfv = key + np.array([0, 0, 1.0]); halfv /= np.linalg.norm(halfv)
    spec = np.clip(nx * halfv[0] + ny * halfv[1] + nz * halfv[2], 0, 1) ** 28
    shade = (0.42 + 0.62 * lk)[..., None] * np.array([1.06, 0.98, 0.86]) \
        + (0.20 * lf)[..., None] * np.array([0.80, 0.82, 1.0])
    term = np.exp(-((lk - 0.35) / 0.18) ** 2)[..., None] * np.array([0.10, 0.03, 0.0])
    out = alb * (shade + term)
    out += (rim * 110)[..., None] * np.array([1.0, 0.82, 0.45]) * (mask[..., None] > 0.3)
    out += (spec * 45)[..., None]
    return out, alb


def dreamy_bg(img, mask):
    bg = img.astype(np.float32)
    # fill people with surrounding room so they don't smear into the blur
    m = (cv2.GaussianBlur(mask, (0, 0), 3) > 0.15).astype(np.uint8)
    small = cv2.resize(bg, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
    ms = cv2.resize(m, (W // 4, H // 4), interpolation=cv2.INTER_NEAREST)
    small = cv2.inpaint(np.clip(small, 0, 255).astype(np.uint8), ms, 9, cv2.INPAINT_TELEA).astype(np.float32)
    small = cv2.GaussianBlur(small, (0, 0), 5)
    bg = cv2.resize(small, (W, H), interpolation=cv2.INTER_CUBIC)
    # bokeh discs from the brightest areas
    lum = small.mean(2)
    disc = np.zeros((H // 4, W // 4), np.float32)
    rng = np.random.default_rng(7)
    ys, xs = np.nonzero(lum > np.percentile(lum, 88))
    if len(xs):
        for i in rng.choice(len(xs), min(40, len(xs)), replace=False):
            cv2.circle(disc, (int(xs[i]), int(ys[i])), int(rng.integers(6, 14)), float(rng.uniform(0.4, 1.0)), -1, cv2.LINE_AA)
    disc = cv2.GaussianBlur(cv2.resize(disc, (W, H)), (0, 0), 3)
    # pastel grade of the room: warm cream/peach/lilac
    hsv = cv2.cvtColor(np.clip(bg, 0, 255).astype(np.uint8), cv2.COLOR_RGB2HSV).astype(np.float32)
    hsv[..., 1] = np.clip(hsv[..., 1] * 1.3 + 25, 0, 255)
    hsv[..., 2] = np.clip(hsv[..., 2] * 0.62 + 92, 0, 255)
    bg = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB).astype(np.float32)
    bg = bg * np.array([1.05, 0.98, 0.9]) + np.array([12, 4, 0])
    bg += disc[..., None] * np.array([70, 55, 30])
    return bg


def render(frame, mask, n):
    faces = smoothed_faces(n)
    wimg, wmask, eyes = chibi_warp(frame, mask, faces)
    toy, alb = toy_shade(wimg, wmask)
    bg = dreamy_bg(frame, mask)
    # soft contact glow / shadow around the figures
    am = cv2.GaussianBlur(np.clip(wmask * 1.4 - 0.2, 0, 1), (0, 0), 1.5)[..., None]
    halo = cv2.GaussianBlur(wmask, (0, 0), 30)[..., None]
    bg = bg * (1 - 0.18 * halo)
    img = toy * am + bg * (1 - am)
    # kawaii face details
    lay = np.zeros((H, W), np.float32)
    iris = np.zeros((H, W), np.float32)
    lid = np.zeros((H, W), np.float32)
    blush = np.zeros((H, W), np.float32)
    for p, ew, f in eyes:
        if not f["seen"]:
            continue    # bridged dropout: face is likely hidden (hand in front), no drawn eyes
        cx, cy = int(p[0]), int(p[1])
        if f["open"] > 0.2:
            # big glossy chibi eye: dark iris ellipse + two catchlights
            ax, ay = int(ew * 0.34), int(ew * 0.42)
            cv2.ellipse(iris, (cx, cy), (ax, ay), 0, 0, 360, 1.0, -1, cv2.LINE_AA)
            r = max(2.0, ew * 0.11)
            cv2.circle(lay, (int(cx - ew * 0.11), int(cy - ew * 0.16)), int(round(r)), 1.0, -1, cv2.LINE_AA)
            cv2.circle(lay, (int(cx + ew * 0.12), int(cy + ew * 0.12)), int(round(r * 0.5)), 0.85, -1, cv2.LINE_AA)
        else:
            # smiling / squinting: happy arc eye
            cv2.ellipse(lid, (cx, cy + int(ew * 0.12)), (int(ew * 0.30), int(ew * 0.22)), 0, 200, 340, 1.0,
                        max(2, int(ew * 0.07)), cv2.LINE_AA)
        side = np.sign(p[0] - (f["c"][0]))
        bx, by = p[0] + side * ew * 0.25, p[1] + ew * 0.95
        cv2.ellipse(blush, (int(bx), int(by)), (int(ew * 0.55), int(ew * 0.33)), 0, 0, 360, 1.0, -1, cv2.LINE_AA)
    blush = cv2.GaussianBlur(blush, (0, 0), 9)[..., None] * 0.45
    img = img * (1 - blush) + blush * np.array([255, 128, 140])
    iris = cv2.GaussianBlur(iris, (0, 0), 0.9)[..., None]
    yy0 = np.mgrid[0:H, 0:W][0].astype(np.float32)
    iris_col = np.array([42, 26, 20]) + 0 * yy0[..., None]
    img = img * (1 - iris * 0.95) + iris * 0.95 * iris_col
    lid = cv2.GaussianBlur(lid, (0, 0), 0.8)[..., None]
    img = img * (1 - lid) + lid * np.array([50, 32, 24])
    lay = cv2.GaussianBlur(lay, (0, 0), 0.8)[..., None]
    img = img * (1 - lay) + 255 * lay
    # golden sun haze from the upper left + bloom
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    sun = np.exp(-(((xx - W * 0.12) / (W * 0.55)) ** 2 + ((yy + H * 0.1) / (H * 0.75)) ** 2))[..., None]
    img = img + sun * np.array([34, 24, 6])
    img = np.clip(img, 0, 255)
    br = np.clip(img.mean(2) - 190, 0, 65)[..., None] / 65
    img = img + cv2.GaussianBlur(img * br, (0, 0), 22) * 0.25
    # creamy lifted grade
    img = 20 + img * 0.9
    img = img * np.array([1.03, 1.0, 0.93])
    v = 1 - 0.14 * (((xx - W / 2) / (W * 0.6)) ** 2 + ((yy - H / 2) / (H * 0.6)) ** 2)
    img = img * v[..., None]
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
