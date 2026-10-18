"""Blob Tracking (TouchDesigner) restyle, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [frame numbers... | all]

The footage is desaturated and pushed to a hard, slightly dark grade. Feature
points (mostly on the people, some in the room) are tracked from frame to
frame with Lucas-Kanade optical flow. Each live tracker draws a thin square
box that rides on its point, with an ID and coordinate label. Some boxes
invert or threshold the picture inside them. Thin lines join each box to its
nearest neighbours. Trackers live 10-40 frames and then respawn, so the boxes
keep flickering in and out the way blob tracking does.
Frames are simulated in order from frame 1 (the trackers need it).
"""
import os
import sys

import cv2
import numpy as np

FRAMES, MASKS, OUT = sys.argv[1:4]
ARGS = sys.argv[4:]
N = len([f for f in os.listdir(FRAMES) if f.endswith(".png")])

WHITE = (245, 245, 245)
RED = (40, 40, 235)
# (first, last, name, max trackers, base saturation, base gain, red share, links per box)
SECTIONS = [
    (1, 60, "mono white", 26, 0.0, 0.92, 0.0, 2),
    (61, 120, "red + white", 34, 0.25, 0.85, 0.45, 2),
    (121, 999, "dense dark", 46, 0.0, 0.55, 0.15, 3),
]
FONT = cv2.FONT_HERSHEY_PLAIN


def section(n):
    for s in SECTIONS:
        if s[0] <= n <= s[1]:
            return s
    return SECTIONS[-1]


class Tracker:
    _next = 1

    def __init__(self, x, y, rng, person):
        self.id = Tracker._next
        Tracker._next += 1
        self.x, self.y = float(x), float(y)
        self.size = int(rng.choice([28, 36, 44, 56, 70, 90, 120, 150], p=[.14, .16, .16, .16, .14, .11, .08, .05]))
        self.life = int(rng.integers(10, 41))
        self.age = 0
        r = rng.random()
        self.fill = "invert" if r < 0.22 else ("thresh" if r < 0.34 else ("zoom" if r < 0.40 else None))
        self.red = False
        self.person = person


def spawn(gray, mask, trackers, want, rng, red_share):
    have = np.zeros_like(gray)
    for t in trackers:
        cv2.circle(have, (int(t.x), int(t.y)), 45, 255, -1)
    need = want - len(trackers)
    if need <= 0:
        return
    pm = ((mask > 128) & (have == 0)).astype(np.uint8) * 255
    bm = ((mask <= 128) & (have == 0)).astype(np.uint8) * 255
    pts = []
    for m, k in ((pm, int(need * 0.75 + 0.5)), (bm, need - int(need * 0.75 + 0.5))):
        if k <= 0:
            continue
        p = cv2.goodFeaturesToTrack(gray, k * 3, 0.02, 40, mask=m, blockSize=7)
        if p is not None:
            p = p.reshape(-1, 2)
            rng.shuffle(p)
            pts += [(x, y, m is pm) for x, y in p[:k]]
    for x, y, person in pts:
        t = Tracker(x, y, rng, person)
        t.red = rng.random() < red_share
        trackers.append(t)


def draw(n, img, mask, trackers, rng):
    _, _, _, _, sat, gain, _, links = section(n)
    h, w = mask.shape
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    base = cv2.cvtColor(g, cv2.COLOR_GRAY2BGR).astype(np.float32)
    base = base + (img.astype(np.float32) - base) * sat
    f = base / 255
    f = np.clip((f - 0.5) * 1.25 + 0.5, 0, 1) * gain          # hard grade
    out = (f * 255).astype(np.uint8)
    src = out.copy()
    live = [t for t in trackers if 0 <= t.x < w and 0 <= t.y < h]
    # cell effects first (they replace the picture inside the box)
    for t in live:
        s = t.size // 2
        x0, y0, x1, y1 = max(0, int(t.x) - s), max(0, int(t.y) - s), min(w, int(t.x) + s), min(h, int(t.y) + s)
        if x1 - x0 < 6 or y1 - y0 < 6:
            continue
        cell = src[y0:y1, x0:x1]
        if t.fill == "invert":
            out[y0:y1, x0:x1] = 255 - cell
        elif t.fill == "thresh":
            gc = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)
            _, th = cv2.threshold(gc, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            out[y0:y1, x0:x1] = cv2.cvtColor(th, cv2.COLOR_GRAY2BGR)
        elif t.fill == "zoom":
            cy, cx = (y0 + y1) // 2, (x0 + x1) // 2
            q = max(3, (x1 - x0) // 4)
            z = src[max(0, cy - q):cy + q, max(0, cx - q):cx + q]
            if z.size:
                out[y0:y1, x0:x1] = cv2.resize(z, (x1 - x0, y1 - y0), interpolation=cv2.INTER_NEAREST)
    # links between nearest boxes, plus a few long ones
    pts = np.array([[t.x, t.y] for t in live], np.float32)
    if len(pts) > 2:
        d = np.linalg.norm(pts[:, None] - pts[None], axis=2)
        np.fill_diagonal(d, 1e9)
        seen = set()
        for i in range(len(pts)):
            for j in np.argsort(d[i])[:links]:
                a, b = min(i, j), max(i, j)
                if (a, b) in seen or d[a, b] > w * 0.45:
                    continue
                seen.add((a, b))
                c = RED if (live[a].red and live[b].red) else WHITE
                cv2.line(out, tuple(pts[a].astype(int)), tuple(pts[b].astype(int)), c, 1, cv2.LINE_AA)
        lr = np.random.default_rng(42000 + n // 3)
        for _ in range(3):
            a, b = lr.integers(0, len(pts), 2)
            cv2.line(out, tuple(pts[a].astype(int)), tuple(pts[b].astype(int)), WHITE, 1, cv2.LINE_AA)
    # boxes, centre ticks, labels
    for t in live:
        s = t.size // 2
        c = RED if t.red else WHITE
        p0, p1 = (int(t.x) - s, int(t.y) - s), (int(t.x) + s, int(t.y) + s)
        cv2.rectangle(out, p0, p1, c, 2 if t.size >= 70 else 1, cv2.LINE_AA)
        cv2.line(out, (int(t.x) - 4, int(t.y)), (int(t.x) + 4, int(t.y)), c, 1)
        cv2.line(out, (int(t.x), int(t.y) - 4), (int(t.x), int(t.y) + 4), c, 1)
        lab = f"{t.id:03d}"
        if t.size >= 44:
            lab += f"  x{t.x / w:.3f} y{t.y / h:.3f}"
        sc = 1.0 if t.size < 90 else 1.3
        (tw, th), _ = cv2.getTextSize(lab, FONT, sc, 1)
        ty = p0[1] - 5 if p0[1] - 5 - th > 0 else p1[1] + th + 5
        if t.red:
            cv2.rectangle(out, (p0[0], ty - th - 3), (p0[0] + tw + 4, ty + 3), RED, -1)
            cv2.putText(out, lab, (p0[0] + 2, ty), FONT, sc, WHITE, 1, cv2.LINE_AA)
        else:
            cv2.putText(out, lab, (p0[0], ty), FONT, sc, c, 1, cv2.LINE_AA)
    # HUD
    hud = f"BLOB_TRACK  blobs:{len(live):02d}  frame:{n:03d}  12fps"
    (hw_, _), _ = cv2.getTextSize(hud, FONT, 1.6, 1)
    cv2.putText(out, hud, (w - hw_ - 24, h - 24), FONT, 1.6, WHITE, 1, cv2.LINE_AA)
    cv2.putText(out, "TD // blobtrack1 -> trace -> render", (24, 40), FONT, 1.6, WHITE, 1, cv2.LINE_AA)
    # light sensor noise so stills are not dead
    noise = rng.normal(0, 4, (h, w, 1)).astype(np.float32)
    return np.clip(out.astype(np.float32) + noise, 0, 255).astype(np.uint8)


def main():
    os.makedirs(OUT, exist_ok=True)
    nums = list(range(1, N + 1)) if (not ARGS or ARGS == ["all"]) else sorted(int(a) for a in ARGS)
    want = set(nums)
    rng = np.random.default_rng(42)
    trackers, prev = [], None
    lk = dict(winSize=(31, 31), maxLevel=4, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01))
    for n in range(1, max(nums) + 1):
        img = cv2.imread(f"{FRAMES}/frame_{n:03d}.png")
        mask = cv2.imread(f"{MASKS}/frame_{n:03d}.png", 0)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if prev is not None and trackers:
            p0 = np.array([[t.x, t.y] for t in trackers], np.float32).reshape(-1, 1, 2)
            p1, st, _ = cv2.calcOpticalFlowPyrLK(prev, gray, p0, None, **lk)
            keep = []
            for t, p, ok in zip(trackers, p1.reshape(-1, 2), st.reshape(-1)):
                t.age += 1
                if ok and t.age < t.life:
                    t.x, t.y = float(p[0]), float(p[1])
                    keep.append(t)
            trackers = keep
        spawn(gray, mask, trackers, section(n)[3], rng, section(n)[6])
        prev = gray
        if n in want:
            out = draw(n, img, mask, trackers, np.random.default_rng(4200 + n))
            cv2.imwrite(f"{OUT}/frame_{n:03d}.png", out)
    print("done", len(nums))


if __name__ == "__main__":
    main()
