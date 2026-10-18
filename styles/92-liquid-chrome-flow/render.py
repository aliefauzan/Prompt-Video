"""Liquid Chrome Flow, frame by frame.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [all | frame numbers...]

Per frame:
  * liquid-metal shapes are built as height fields: drifting metaballs that
    merge and split, two thick sine-wave tubes that flow across the frame,
    and drips hanging from the top edge that stretch and shrink
  * each pixel of metal is shaded as a perfect chrome mirror: a normal from
    the height field picks a reflection direction that looks up a studio
    environment (white sky, sharp dark horizon, grey floor, softboxes) mixed
    with a blurred, warped copy of the frame itself, so the metal reflects
    the room and the people; hard specular glints and dark silhouette rims
  * layering from the masks: drips, blobs and the upper tube flow BEHIND the
    people; the lower tube wraps round the group at waist height (in front
    of the middle person, behind the two at the sides), never over a face
  * the room gets a cool, slightly desaturated grade so the chrome pops;
    soft contact shadows on the wall under the metal
"""
import os
import sys
from multiprocessing import Pool

import cv2
import numpy as np

FRAMES, MASKS, OUT = sys.argv[1:4]
ARGS = sys.argv[4:]
N = len([f for f in os.listdir(FRAMES) if f.startswith("frame_") and f.endswith(".png")])
W, H = 1620, 1080
S = 2                                   # field resolution divisor
FW, FH = W // S, H // S
YF, XF = np.mgrid[0:FH, 0:FW].astype(np.float32)


def load(n):
    img = cv2.imread(os.path.join(FRAMES, f"frame_{n:03d}.png")).astype(np.float32) / 255
    m = cv2.imread(os.path.join(MASKS, f"frame_{n:03d}.png"), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
    return img, m


def bead(f, x, y, r):
    """Add one smooth compact metaball (Wyvill kernel) whose surface radius is ~r."""
    R = r / 0.61
    x0, x1 = int(max(0, x - R)), int(min(FW, x + R + 1))
    y0, y1 = int(max(0, y - R)), int(min(FH, y + R + 1))
    if x1 <= x0 or y1 <= y0:
        return
    d2 = (XF[y0:y1, x0:x1] - x) ** 2 + (YF[y0:y1, x0:x1] - y) ** 2
    f[y0:y1, x0:x1] += np.clip(1 - d2 / (R * R), 0, 1) ** 3


def height(f):
    """Field (full res) -> smooth dome height in px plus an AA alpha.
    The Wyvill field rises roughly linearly from the surface, so sqrt gives a
    round edge that tilts to vertical at the silhouette and a smooth crown."""
    T = 0.25
    h = 46 * np.sqrt(np.clip(f - T, 0, None))
    gx = cv2.Sobel(f, cv2.CV_32F, 1, 0, ksize=3) / 8
    gy = cv2.Sobel(f, cv2.CV_32F, 0, 1, ksize=3) / 8
    alpha = np.clip(0.5 + (f - T) / (np.sqrt(gx * gx + gy * gy) + 1e-4), 0, 1)
    return h.astype(np.float32), alpha.astype(np.float32)


def blobs(f, t):
    """Merging liquid-metal blobs drifting across the upper background."""
    rng = np.random.default_rng(92)
    for i in range(7):
        x0, y0 = rng.random() * FW, (0.08 + 0.42 * rng.random()) * FH
        vx = rng.choice([-1, 1]) * (0.7 + 0.8 * rng.random())
        r = float((20 + 24 * rng.random()) * (1 + 0.18 * np.sin(t * 0.09 + i * 1.7)))
        x = float((x0 + vx * t) % (FW + 240) - 120)
        y = float(y0 + 22 * np.sin(t * 0.05 + i))
        bead(f, x, y, r)
        # satellite droplets orbiting each blob: they pinch off and merge back
        for j, (a, rr) in enumerate(((1.15, 0.55), (-1.4, 0.35))):
            ang = t * 0.07 * a + i + j * 2.1
            bead(f, x + r * 1.35 * np.cos(ang), y + r * 0.9 * np.sin(ang), r * rr)


def tube(f, t, y0, amp, k, w, radius, phase):
    """Flowing liquid ribbon: a chain of beads along a travelling double sine;
    the radius swells and pinches so bulges travel along it."""
    xs = np.arange(-60, FW + 60, 5, dtype=np.float32)
    ys = y0 + amp * np.sin(xs * k - w * t + phase) + 0.45 * amp * np.sin(xs * k * 2.3 + 0.6 * w * t + phase)
    rad = radius * (0.45 + 0.55 * np.sin(xs * k * 1.7 - 0.8 * w * t + phase * 2) ** 2) * 0.62
    for x, y, r in zip(xs, ys, rad):
        bead(f, float(x), float(y), float(r))
    return ys, xs


def drips(f, t):
    """Liquid chrome hanging from the top edge: pool, thinning neck, fat drop."""
    rng = np.random.default_rng(29)
    for i in range(3):
        x = float(FW * (0.16 + 0.33 * i) + 30 * rng.random() + 10 * np.sin(t * 0.03 + i))
        L = float(FH * (0.20 + 0.10 * rng.random()) * (1 + 0.35 * np.sin(t * 0.045 + 2 * i)))
        w = float(10 + 4 * rng.random())
        for xx in np.linspace(x - 3 * w, x + 3 * w, 9):
            bead(f, float(xx), 0.0, w * 1.6 * (1 - abs(xx - x) / (4 * w)))
        for yy in np.arange(0, L, 2):
            bead(f, x + 2 * np.sin(yy * 0.05 + t * 0.1), float(yy), w * (1 - 0.5 * yy / L) * 0.62)
        bead(f, x, L + w * 0.8, w * 1.55)


def env_map(img):
    """Reflection environment: studio sphere + blurred copy of the room."""
    E = 256
    v = np.linspace(-1, 1, E, dtype=np.float32)[:, None]
    u = np.linspace(-1, 1, E, dtype=np.float32)[None, :]
    # the sphere-map centre is what sits behind the camera: keep it bright;
    # horizon below centre, so crowns read white and flanks pick up the dark band
    hz = 0.30
    sky = 1.0 - 0.35 * np.clip(-v, 0, 1)
    floor = 0.05 + 0.35 * np.clip((v - hz) / (1 - hz), 0, 1) ** 1.5
    horizon = np.where(v < hz, sky, floor) * np.ones_like(u)
    horizon = horizon - 0.85 * np.exp(-((v - hz - 0.01) / 0.035) ** 2)   # sharp dark horizon line
    # two softboxes
    for cx, cy, s in ((-0.40, -0.45, 0.20), (0.50, -0.20, 0.14), (0.05, -0.80, 0.25)):
        horizon = horizon + 0.9 * np.exp(-(((u - cx) / s) ** 2 + ((v - cy) / (s * 0.6)) ** 2) ** 2)
    studio = np.repeat(np.clip(horizon, 0, 1.3)[..., None], 3, 2) * np.array([1.0, 0.98, 0.95], np.float32)
    room = cv2.resize(cv2.GaussianBlur(img, (0, 0), 6), (E, E), interpolation=cv2.INTER_AREA)
    room = cv2.cvtColor(cv2.cvtColor(room, cv2.COLOR_BGR2HSV) * np.array([1, 0.55, 1], np.float32), cv2.COLOR_HSV2BGR)
    env = 0.75 * studio + 0.32 * room
    # cool steel cast
    return (env * np.array([1.06, 1.0, 0.94], np.float32)).astype(np.float32)


def chrome(h, env, rng_t):
    """Shade a height field (full res) as polished liquid chrome."""
    hs = h
    gx = cv2.Sobel(hs, cv2.CV_32F, 1, 0, ksize=3) / 8
    gy = cv2.Sobel(hs, cv2.CV_32F, 0, 1, ksize=3) / 8
    nz = 1 / np.sqrt(gx * gx + gy * gy + 1)
    nx, ny = -gx * nz, -gy * nz
    # reflection of the view ray (0,0,-1): r = v - 2 (v.n) n
    rx, ry, rz = 2 * nz * nx, 2 * nz * ny, 2 * nz * nz - 1
    # sphere-map lookup
    E = env.shape[0]
    mm = np.sqrt(rx * rx + ry * ry + (rz + 1) ** 2) + 1e-5
    u = ((rx / mm) * 0.5 + 0.5) * (E - 1)
    v = ((ry / mm) * 0.5 + 0.5) * (E - 1)
    col = cv2.remap(env, u.astype(np.float32), v.astype(np.float32), cv2.INTER_LINEAR,
                    borderMode=cv2.BORDER_REFLECT)
    # hard specular glints from a key light up-left
    L = np.array([-0.45, -0.6, 0.66], np.float32)
    L /= np.linalg.norm(L)
    spec = np.clip(rx * L[0] + ry * L[1] + rz * L[2], 0, 1) ** 90
    col = col + spec[..., None] * 1.4
    # silhouette rim goes dark (grazing reflections of the horizon / room)
    col = col * (0.35 + 0.65 * np.clip(nz * 1.25, 0, 1) ** 0.6)[..., None]
    a = np.clip(h / 1.2, 0, 1)
    return np.clip(col, 0, 1.4), a


def up(a):
    return cv2.resize(a, (W, H), interpolation=cv2.INTER_CUBIC)


def render(n):
    rng = np.random.default_rng(9200 + n)
    img, m = load(n)
    t = float(n)
    env = env_map(img)
    # ----- behind the people: blobs, drips, upper tube
    fb = np.zeros((FH, FW), np.float32)
    blobs(fb, t)
    drips(fb, t)
    tube(fb, t, FH * 0.30, 46, 0.010, 0.06, 30, 0.0)
    back, aback = height(up(fb))
    # ----- wrapping tube at waist height
    ff = np.zeros((FH, FW), np.float32)
    tube(ff, t, FH * 0.86, 30, 0.008, -0.05, 40, 1.3)
    hf, afront = height(up(ff))
    hb_up, hf_up = back, hf
    # the wrap: in front of the middle person, behind the side people
    ms = cv2.GaussianBlur(m, (0, 0), 1.5)
    # the middle person: the contiguous mask run at waist height that is
    # nearest the frame centre (plus a small margin), smoothed
    row = cv2.GaussianBlur(m, (0, 0), 3)[int(H * 0.84)] > 0.5
    cols = np.where(row)[0]
    mid1 = np.zeros(W, np.float32)
    if len(cols):
        c0 = int(cols[np.argmin(np.abs(cols - W / 2))])
        a0 = c0
        while a0 > 0 and row[a0 - 1]:
            a0 -= 1
        b0 = c0
        while b0 < W - 1 and row[b0 + 1]:
            b0 += 1
        mid1[max(0, a0 - 25):b0 + 26] = 1
    mid = cv2.GaussianBlur(mid1[None, :], (0, 0), sigmaX=6, sigmaY=0.1) * np.ones((H, 1), np.float32)
    # keep the front tube off faces: fade it out above the lowest head line
    front_ok = np.clip((np.arange(H, dtype=np.float32)[:, None] - H * 0.62) / 40, 0, 1)
    # ----- room grade: cool, a bit desaturated, slightly darker
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv[..., 1] *= 0.80
    room = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR) * np.array([1.04, 1.0, 0.95], np.float32)
    room = room * (1 - ms[..., None]) + img * ms[..., None]
    # contact shadows of the metal on the wall
    occ = cv2.GaussianBlur(np.clip(hb_up / 6, 0, 1), (0, 0), 18)
    occ = np.roll(occ, 14, axis=0)
    room = room * (1 - 0.35 * (occ * (1 - ms))[..., None])
    cb, _ = chrome(hb_up, env, t)
    ab = aback * (1 - ms)
    out = room * (1 - ab[..., None]) + cb * ab[..., None]
    cf, _ = chrome(hf_up, env, t)
    af = afront * (1 - ms * (1 - mid * front_ok))
    # reflection of the person the tube passes in front of: darker local contact shadow
    sh = cv2.GaussianBlur(np.clip(hf_up / 6, 0, 1), (0, 0), 12)
    out = out * (1 - 0.30 * (np.roll(sh, 10, axis=0) * (1 - af))[..., None])
    out = out * (1 - af[..., None]) + cf * af[..., None]
    # tiny sensor noise
    out = out + rng.normal(0, 0.008, (H, W, 1)).astype(np.float32)
    out = np.clip(out, 0, 1)
    out = (out * 255 + rng.random(out.shape) - 0.5).clip(0, 255).astype(np.uint8)
    cv2.imwrite(os.path.join(OUT, f"frame_{n:03d}.png"), out)
    return n


def main():
    os.makedirs(OUT, exist_ok=True)
    nums = list(range(1, N + 1)) if (not ARGS or ARGS == ["all"]) else [int(a) for a in ARGS]
    with Pool(4) as p:
        for _ in p.imap_unordered(render, nums):
            pass
    print("rendered", len(nums), "->", OUT)


if __name__ == "__main__":
    main()
