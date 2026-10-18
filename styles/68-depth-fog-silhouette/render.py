"""Depth-Style Fog Silhouette (the CapCut "depth style" trend), frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [all | frame numbers...]

Per frame:
  * the people (masks) become a depth-map silhouette: near/thick parts dark
    charcoal, thin parts and edges lighter grey, a faint relief of the face
    and clothes folds kept from the source; fog light wraps into the edges
  * the room dissolves into white fog: only ghost shapes of the window, TV
    and furniture survive as pale grey, the floor fades to a soft grey ground
  * two drifting fog layers (low ground fog + thin veil) roll over everything
  * slow push-in over the whole clip
  * from frame 133 the faces get glowing laser-red eyes (Apple Vision pupils
    from faces.json, gaps of a few frames held from the last seen position)
"""
import json
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np

FRAMES, MASKS, OUT = sys.argv[1:4]
ARGS = sys.argv[4:]
HERE = os.path.dirname(os.path.abspath(__file__))
N = len([f for f in os.listdir(FRAMES) if f.startswith("frame_") and f.endswith(".png")])
W, H = 1620, 1080
LASER_FROM = 133


def mask(n):
    return cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255


def load(n):
    img = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png")).astype(np.float32) / 255
    m = mask(n)
    # the matte drops a motion-blurred hand on a few frames (23, 68): fill from the neighbours
    if 1 < n < N:
        a, b = mask(n - 1), mask(n + 1)
        if (m > 0.5).mean() < 0.8 * min((a > 0.5).mean(), (b > 0.5).mean()):
            m = np.maximum(m, np.maximum(a, b))
    return img, m


def eye_tracks():
    """Per frame: list of (x, y, size) laser-eye points; faces missing for <=3 frames are held."""
    faces = json.load(open(os.path.join(HERE, "faces.json")))
    out, live = {}, []           # live: [cx, w, pupils, age]
    for n in range(1, N + 1):
        cur = []
        for f in faces.get(f"frame_{n:03d}.png", []):
            if f["leftPupil"] and f["rightPupil"]:
                x, y, w, h = f["box"]
                cur.append([x + w / 2, w, [f["leftPupil"], f["rightPupil"]], 0])
        for t in live:            # keep faces that vanished for a moment
            if t[3] < 3 and all(abs(t[0] - c[0]) > max(t[1], c[1]) * 0.6 for c in cur):
                cur.append([t[0], t[1], t[2], t[3] + 1])
        live = cur
        out[n] = [(p[0], p[1], c[1]) for c in cur for p in c[2]]
    return out


def noise(rng, h, w, cell):
    a = rng.random((h // cell + 2, w // cell + 2)).astype(np.float32)
    return cv2.resize(a, (w, h), interpolation=cv2.INTER_CUBIC)


def fog_field(seed, w, h):
    rng = np.random.default_rng(seed)
    return sum(noise(rng, h, w, c) * a for c, a in ((340, 0.6), (150, 0.3), (60, 0.1)))


FOG_A = fog_field(11, W + 900, H)       # ground fog, drifts left
FOG_B = fog_field(12, W + 900, H)       # thin veil, drifts right, slower
EYES = None


def render(n):
    global EYES
    if EYES is None:
        EYES = eye_tracks()
    rng = np.random.default_rng(300 + n)
    img, m = load(n)
    lum = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ms = cv2.GaussianBlur(m, (0, 0), 2.5)
    yy = np.linspace(0, 1, H, dtype=np.float32)[:, None]

    # --- background: white fog with ghost shapes of the room
    bl = cv2.GaussianBlur(lum, (0, 0), 7)
    ghost = 0.97 - 0.20 * (1 - bl) ** 1.6
    ghost = ghost - 0.10 * np.clip((yy - 0.62) / 0.38, 0, 1)          # soft grey ground
    ghost = cv2.GaussianBlur(ghost, (0, 0), 3)

    # --- people: depth-map silhouette from body thickness
    hard = (m > 0.5).astype(np.uint8)
    dt = cv2.distanceTransform(hard, cv2.DIST_L2, 5).astype(np.float32)
    dt = cv2.GaussianBlur(dt, (0, 0), 6)
    near = np.clip(dt / 150, 0, 1) ** 0.55
    tone = 0.36 - 0.31 * near
    relief = lum - cv2.GaussianBlur(lum, (0, 0), 8)                     # faint features / folds
    tone = tone + relief * 0.22 + (cv2.GaussianBlur(lum, (0, 0), 5) - 0.5) * 0.04
    # fog light wrapping into the silhouette edge
    wrap = cv2.GaussianBlur(1 - ms, (0, 0), 14) * ms
    tone = tone * (1 - wrap * 0.8) + ghost * wrap * 0.8
    tone = np.clip(tone, 0.03, 1)
    out = ghost * (1 - ms) + tone * ms

    # --- laser eyes (later part of the clip)
    if n >= LASER_FROM:
        glow = np.zeros((H, W), np.float32)
        core = np.zeros((H, W), np.float32)
        ramp_in = min(1.0, (n - LASER_FROM + 1) / 4)
        for x, y, fw in EYES[n]:
            r = max(3, fw * 0.035)
            cv2.circle(core, (int(x), int(y)), int(r), 1.0, -1, cv2.LINE_AA)
            cv2.ellipse(glow, (int(x), int(y)), (int(r * 9), int(r * 1.2)), 0, 0, 360, 0.6, -1, cv2.LINE_AA)
            cv2.circle(glow, (int(x), int(y)), int(r * 3), 1.0, -1, cv2.LINE_AA)
        flick = (0.9 + 0.1 * rng.random()) * ramp_in
        glow = (cv2.GaussianBlur(glow, (0, 0), 7) + cv2.GaussianBlur(core, (0, 0), 22) * 2.5) * flick
        core = cv2.GaussianBlur(core, (0, 0), 1.2) * flick
        col = np.stack([out, out, out], -1)
        red = np.array([0.10, 0.08, 1.0], np.float32)
        col = col * (1 - np.clip(glow, 0, 1)[..., None]) + red * np.clip(glow, 0, 1)[..., None]
        col = col + core[..., None] * np.array([0.75, 0.75, 1.0], np.float32)
    else:
        col = np.stack([out, out, out], -1)

    # --- drifting fog: ground fog + veil
    sa = int(n * 3.2) % 900
    sb = 900 - int(n * 1.6) % 900
    fa = FOG_A[:, sa:sa + W]
    fb = FOG_B[:, sb:sb + W]
    ground = np.clip((yy - 0.50) / 0.50, 0, 1) ** 1.4 * np.clip((fa - 0.25) / 0.45, 0, 1) * 0.9
    veil = 0.05 + np.clip((fb - 0.35) / 0.4, 0, 1) * 0.12
    fog = np.clip(ground + veil * (1 - ground), 0, 0.92)[..., None]
    col = col * (1 - fog) + 0.95 * fog

    # --- slow push-in
    z = 1 + 0.12 * (n - 1) / (N - 1)
    cx, cy = W / 2, H * 0.42
    M = np.float32([[z, 0, cx - z * cx], [0, z, cy - z * cy]])
    col = cv2.warpAffine(col, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)

    # soft bloom, neutral-cool tint, fine grain, faint dark vignette
    col = col + cv2.GaussianBlur(np.clip(col - 0.8, 0, 1), (0, 0), 20) * 0.5
    col = col * np.array([1.02, 1.0, 0.98], np.float32)
    col += rng.normal(0, 0.012, (H, W, 1)).astype(np.float32)
    xx = np.linspace(-1, 1, W, dtype=np.float32)[None, :]
    col *= (1 - 0.10 * (xx ** 2 + ((yy - 0.5) * 2) ** 2) ** 1.5)[..., None]
    col = np.clip(col, 0, 1)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), (col * 255).astype(np.uint8))
    return n


def main():
    os.makedirs(OUT, exist_ok=True)
    nums = list(range(1, N + 1)) if (not ARGS or ARGS == ["all"]) else [int(a) for a in ARGS]
    with Pool(min(5, os.cpu_count() or 4)) as p:
        for _ in p.imap_unordered(render, nums):
            pass
    print("rendered", len(nums), "->", OUT)


if __name__ == "__main__":
    main()
