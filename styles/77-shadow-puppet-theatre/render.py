"""Shadow Puppet Theatre (皮影) — local approximation of the frame-by-frame restyle.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [all | 13 49 85 ...]

Every frame becomes a Chinese shadow-puppet play seen from the audience side:
  * a glowing paper / silk screen lit by a warm lamp from behind (hot spot, warm falloff,
    fine cloth weave, a slight oil-lamp flicker);
  * the room becomes carved scenery further behind the screen: soft, blurred,
    semi-transparent brown shadows (window frame, plants, chair, TV);
  * the people become translucent dyed-leather puppets pressed flat on the screen:
    hair and dark clothes = black leather, skin = carved-open pale amber face
    (空脸) with black-lined features, other clothes dyed in the traditional
    vermilion / green / ochre / indigo, every colour patch outlined in black;
  * punched ornament (rosettes, dots, scallops) is cut through the clothing so the
    lamp shines through; the pattern is anchored to each puppet's head so it moves
    with the puppet instead of swimming;
  * a control rod runs from each puppet's neck down out of frame, rivets mark the
    neck and shoulder joints.
"""
import sys
from pathlib import Path

import cv2
import numpy as np

cv2.setNumThreads(2)
W, H = 1620, 1080
GY, GX = np.mgrid[0:H, 0:W].astype(np.float32)


def heads(m):
    """Find heads from the matte: lowest-y peaks of the silhouette, head width from the row runs,
    stop at the neck dip / shoulder jump. Returns [(xc, y0, yneck, headw)]. (from styles/17)"""
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
        if any(l <= h[0] <= r for h in out):
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
                grow = False
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


def ornament_tile(n=44):
    """One tile of punched leather ornament: a four-petal rosette, dots and a scallop row."""
    t = np.zeros((n * 4, n * 4), np.uint8)       # 4x supersampled
    c = n * 2
    for a in range(4):
        ang = a * 90 + 45
        cv2.ellipse(t, (c, c), (int(n * 0.62), int(n * 0.26)), ang, 0, 360, 255, -1, cv2.LINE_AA)
    cv2.circle(t, (c, c), int(n * 0.22), 0, -1, cv2.LINE_AA)
    cv2.circle(t, (c, c), int(n * 0.10), 255, -1, cv2.LINE_AA)
    for (x, y) in ((0, 0), (n * 4, 0), (0, n * 4), (n * 4, n * 4)):
        cv2.circle(t, (x, y), int(n * 0.32), 255, -1, cv2.LINE_AA)
        cv2.circle(t, (x, y), int(n * 0.18), 0, -1, cv2.LINE_AA)
    for x in (0, n * 4):
        cv2.circle(t, (x, c), int(n * 0.12), 255, -1, cv2.LINE_AA)
        cv2.circle(t, (c, x), int(n * 0.12), 255, -1, cv2.LINE_AA)
    return cv2.resize(t, (n, n), interpolation=cv2.INTER_AREA).astype(np.float32) / 255


TILE = ornament_tile(60)
WEAVE = None


def weave():
    global WEAVE
    if WEAVE is None:
        rng = np.random.default_rng(3)
        x = np.sin(GX * 2.1) * 0.5 + np.sin(GY * 2.3) * 0.5
        n = cv2.GaussianBlur(rng.standard_normal((H, W)).astype(np.float32), (0, 0), 0.8)
        leather = cv2.resize(cv2.GaussianBlur(rng.standard_normal((H // 6, W // 6)).astype(np.float32), (0, 0), 1.5), (W, H))
        fib = cv2.filter2D(n, -1, np.ones((1, 11), np.float32) / 11)
        WEAVE = (x * 0.5 + n * 0.5, leather / leather.std(), fib / fib.std())
    return WEAVE


# translucent dyes (transmission per channel)
BLACK = np.float32([0.07, 0.045, 0.03])
FACE = np.float32([1.0, 0.86, 0.60])
RED = np.float32([0.88, 0.16, 0.07])
GREEN = np.float32([0.24, 0.55, 0.30])
OCHRE = np.float32([0.98, 0.70, 0.22])
INDIGO = np.float32([0.22, 0.30, 0.66])
BROWN = np.float32([0.62, 0.30, 0.10])


def render(rgb, m, frame_no):
    rng = np.random.default_rng(frame_no * 389)
    cloth, leather, fib = weave()
    # --- the lit screen
    fl = 1 + 0.025 * np.sin(frame_no * 2.3) + 0.015 * np.sin(frame_no * 5.1 + 1)
    cx = W * 0.5 + 8 * np.sin(frame_no * 0.7)
    cy = H * 0.42 + 6 * np.sin(frame_no * 0.53)
    r = np.sqrt(((GX - cx) / (W * 0.6)) ** 2 + ((GY - cy) / (H * 0.62)) ** 2)
    hot = np.clip(1 - r * 0.7, 0, 1)[..., None]
    lamp = (np.float32([255, 240, 205]) * hot + np.float32([196, 112, 48]) * (1 - hot)) * fl
    lamp *= (1 + 0.035 * cloth)[..., None]

    # --- scenery shadows: the room as carved props further back (soft, half transparent)
    sm = cv2.resize(rgb, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
    sm = cv2.bilateralFilter(sm, 9, 40, 6)
    g = cv2.cvtColor(sm, cv2.COLOR_RGB2GRAY).astype(np.float32)
    prop = np.clip((150 - g) / 60, 0, 1)
    prop = cv2.resize(cv2.GaussianBlur(prop, (0, 0), 1.2), (W, H))
    prop = cv2.GaussianBlur(prop, (0, 0), 5) * 0.55
    col = lamp * (1 - prop[..., None] * (1 - np.float32([0.30, 0.18, 0.10])))

    # --- puppets
    sp = cv2.resize(rgb, (W // 2, H // 2), interpolation=cv2.INTER_AREA)
    for _ in range(2):
        sp = cv2.bilateralFilter(sp, 9, 30, 5)
    sp = cv2.resize(sp, (W, H))
    hsv = cv2.cvtColor(sp, cv2.COLOR_RGB2HSV).astype(np.float32)
    hue, sat, val = hsv[..., 0] * 2, hsv[..., 1] / 255, hsv[..., 2] / 255
    labc = cv2.cvtColor(sp, cv2.COLOR_RGB2LAB).astype(np.float32)
    L = labc[..., 0] / 2.55
    hs = heads(m)
    face = np.zeros((H, W), np.uint8)
    for xc, y0, yn, hw in hs:
        cv2.ellipse(face, (int(xc), int(y0 + (yn - y0) * 0.58)), (int(hw * 0.47), int((yn - y0) * 0.5)), 0, 0, 360, 1, -1)
    skin = (L > 28) & (((hue < 35) | (hue > 340)) & (sat > 0.15) & (sat < 0.7)) & (labc[..., 1] > 134)
    skin |= (face > 0) & (L > 22)
    skin = cv2.morphologyEx(skin.astype(np.uint8), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    skin = cv2.GaussianBlur(skin.astype(np.float32), (0, 0), 3) > 0.5
    black = (L < 19) | ((L < 27) & (sat < 0.3))
    cls = np.full((H, W), 3, np.int32)                      # default: green
    warm = ((hue < 45) | (hue > 330)) & (sat > 0.2)
    cls[warm & (L < 55)] = 2                                # vermilion (batik, browns)
    cls[warm & (L >= 55)] = 4                               # ochre
    cls[~warm & (L >= 62)] = 4                              # light neutrals -> ochre
    cls[(hue > 190) & (hue < 260) & (sat > 0.25)] = 5       # indigo
    cls[black] = 0
    cls[skin] = 1
    # clean patches: majority vote
    votes = np.stack([cv2.GaussianBlur((cls == k).astype(np.float32), (0, 0), 2.5) for k in range(6)], -1)
    cls = votes.argmax(-1)
    dyes = np.stack([BLACK, FACE, RED, GREEN, OCHRE, INDIGO])
    T = dyes[cls]
    thick = np.where(cls == 1, 0.045, 0.10)
    T *= (1 + thick * leather + 0.05 * fib)[..., None]       # uneven leather thickness

    mm = (cv2.GaussianBlur(m, (0, 0), 1.2) > 0.5).astype(np.uint8)
    # punched ornament through clothing, anchored to the nearest head
    if hs:
        ax = np.array([h[0] for h in hs], np.float32)
        ay = np.array([h[1] for h in hs], np.float32)
        near = np.abs(GX[..., None] - ax[None, None]).argmin(-1)
        ox, oy = ax[near], ay[near]
    else:
        ox = oy = np.zeros((H, W), np.float32)
    n = TILE.shape[0]
    tx = ((GX - ox).astype(np.int32) % n)
    ty = ((GY - oy).astype(np.int32) % n)
    holes = TILE[ty, tx]
    cloth_zone = ((cls >= 2) & (mm > 0)).astype(np.uint8)
    cloth_zone = cv2.erode(cloth_zone, np.ones((15, 15), np.uint8))
    holes *= cv2.GaussianBlur(cloth_zone.astype(np.float32), (0, 0), 2)
    # black carved outlines: around every patch, the features, and the puppet edge
    edge = np.zeros((H, W), np.uint8)
    edge[:, 1:] |= (cls[:, 1:] != cls[:, :-1]).astype(np.uint8)
    edge[1:, :] |= (cls[1:, :] != cls[:-1, :]).astype(np.uint8)
    edge = cv2.dilate(edge, np.ones((3, 3), np.uint8))
    gr = cv2.cvtColor(sp, cv2.COLOR_RGB2GRAY).astype(np.float32)
    dog = cv2.GaussianBlur(gr, (0, 0), 3.5) - cv2.GaussianBlur(gr, (0, 0), 1.0)
    feat = (dog > 6) & skin
    outline = cv2.morphologyEx(mm, cv2.MORPH_GRADIENT, np.ones((7, 7), np.uint8))
    ink = np.maximum.reduce([edge.astype(np.float32), feat.astype(np.float32), outline.astype(np.float32)])
    ink = cv2.GaussianBlur(ink, (0, 0), 0.9)
    T = T * (1 - holes[..., None]) + holes[..., None] * np.float32([1.0, 0.95, 0.82])
    T = T * (1 - ink[..., None]) + BLACK * ink[..., None]

    # rods and rivets
    rods = np.zeros((H, W), np.uint8)
    rivets = []
    for xc, y0, yn, hw in hs:
        neck = (int(xc), int(yn + hw * 0.3))
        foot = (int(xc + (xc - W / 2) * 0.12 + 30), H + 40)
        cv2.line(rods, neck, foot, 255, 6, cv2.LINE_AA)
        rivets.append(neck)
        for sgn in (-1, 1):
            p = (int(xc + sgn * hw * 1.05), int(yn + hw * 0.45))
            if 0 <= p[0] < W and 0 <= p[1] < H and m[p[1], p[0]] > 0.5:
                rivets.append(p)
    rod = cv2.GaussianBlur(rods.astype(np.float32) / 255, (0, 0), 1.2)
    a = cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 0.8)
    puppet = lamp * T
    col = col * (1 - a[..., None]) + puppet * a[..., None]
    # leather pressed on the screen: a faint soft shadow just around it
    halo = cv2.GaussianBlur(a, (0, 0), 6) - a
    col *= (1 - 0.35 * np.clip(halo, 0, 1))[..., None]
    col = col * (1 - rod[..., None] * 0.9) + np.float32([20, 12, 6]) * rod[..., None] * 0.9
    for p in rivets:
        cv2.circle(col, p, 9, (25, 15, 8), -1, cv2.LINE_AA)
        cv2.circle(col, p, 4, (150, 110, 60), -1, cv2.LINE_AA)

    # glow of the lit screen, warm theatre vignette
    bloom = cv2.GaussianBlur(np.clip(col - 170, 0, None), (0, 0), 10)
    col += bloom * 0.4
    vig = np.clip(1 - 0.55 * np.clip(r - 0.6, 0, None) ** 1.4, 0, 1)
    col *= vig[..., None]
    col += rng.normal(0, 1.8, (H, W, 1)).astype(np.float32)
    return np.clip(col, 0, 255).astype(np.uint8)


def main():
    frames, masks, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    out.mkdir(parents=True, exist_ok=True)
    args = sys.argv[4:] or ["13", "49", "85", "109", "145", "178"]
    nums = range(1, 180) if args == ["all"] else [int(a) for a in args]
    for n in nums:
        rgb = cv2.cvtColor(cv2.imread(str(frames / f"frame_{n:03d}.png")), cv2.COLOR_BGR2RGB)
        m = cv2.imread(str(masks / f"frame_{n:03d}.png"), 0).astype(np.float32) / 255
        res = render(rgb, m, n)
        cv2.imwrite(str(out / f"frame_{n:03d}.png"), cv2.cvtColor(res, cv2.COLOR_RGB2BGR))
        print(n, flush=True)


if __name__ == "__main__":
    main()
