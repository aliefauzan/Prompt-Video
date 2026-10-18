"""Sand Animation Lightbox — local approximation of the frame-by-frame restyle.

usage: python -I render.py <frames_dir> <masks_dir> <out_dir> [all | 13 49 85 ...]

Every frame becomes a sand drawing on a glowing light table, filmed from above:
  * the frame is simplified to a few tones; dark areas = thick sand (light blocked),
    light areas = bare glass (light shines through); the room is drawn sparser and
    softer than the people, with a cleared ring of glass around the figures;
  * sand coverage is stochastic: a grain field turns mid-tones into scattered
    grains, plus loose single grains on the bare glass;
  * contours are "drawn with a fingertip": bright scraped lines through thick sand,
    thin trickled sand lines across bare glass (eyes, brows, mouth, glasses, outlines);
  * the light table glows warm amber, hotter in the middle, falling to orange at
    the edges; light bleeds (bloom) around bare glass and grain edges;
  * the sand around the people is re-poured every frame (grain boil), the sand
    of the room stays put, like a live sand artist redrawing only the figures.
"""
import sys
from pathlib import Path

import cv2
import numpy as np

cv2.setNumThreads(2)
W, H = 1620, 1080
GY, GX = np.mgrid[0:H, 0:W].astype(np.float32)


def grain_field(rng):
    g = cv2.GaussianBlur(rng.standard_normal((H, W)).astype(np.float32), (0, 0), 0.95)
    g /= g.std()
    return 0.5 + 0.5 * np.tanh(g * 0.9)            # ~uniform 0..1, grain-sized blobs


STATIC = grain_field(np.random.default_rng(11))
COARSE = cv2.resize(cv2.GaussianBlur(np.random.default_rng(12).standard_normal((H // 8, W // 8)).astype(np.float32), (0, 0), 1.5), (W, H))


def density(rgb):
    g = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    s = cv2.resize(g, (W // 2, H // 2), interpolation=cv2.INTER_AREA)
    for _ in range(3):
        s = cv2.bilateralFilter(s, 9, 30, 6)
    s = cv2.resize(s, (W, H), interpolation=cv2.INTER_LINEAR).astype(np.float32)
    lo, hi = np.percentile(s, 3), np.percentile(s, 97)
    d = 1 - np.clip((s - lo) / (hi - lo), 0, 1)
    return d, s


def render(rgb, m, frame_no):
    rng = np.random.default_rng(frame_no * 977)
    d, s = density(rgb)
    # a few hand-made tone steps (an artist spreads thin / medium / thick sand)
    q = np.round(d * 4) / 4
    d = 0.55 * q + 0.45 * d
    d = cv2.GaussianBlur(d, (0, 0), 2.0)

    ms = cv2.GaussianBlur(m, (0, 0), 3)
    halo = cv2.GaussianBlur(cv2.dilate(m, np.ones((41, 41), np.uint8)), (0, 0), 14)
    # people: own tonal stretch (faces = thin sand, hair / dark clothes = thick); room: sparser,
    # softer, cleared around the figures
    inside = m > 0.5
    if inside.sum() > 500:
        lo, hi = np.percentile(s[inside], 4), np.percentile(s[inside], 96)
        dp = 1 - np.clip((s - lo) / max(hi - lo, 1), 0, 1)
    else:
        dp = d
    dp = np.round(dp * 4) / 4 * 0.5 + dp * 0.5
    dp = cv2.GaussianBlur(dp, (0, 0), 1.6) ** 1.7
    db = cv2.GaussianBlur(d, (0, 0), 5) * 0.62 * (1 - 0.75 * np.clip(halo - ms, 0, 1))
    D = dp * ms + db * (1 - ms)

    # grain field: the room's sand stays put, the sand of the figures is re-poured each frame
    live = grain_field(rng)
    zone = cv2.GaussianBlur(cv2.dilate(m, np.ones((25, 25), np.uint8)), (0, 0), 6)
    G = STATIC * (1 - zone) + (0.35 * STATIC + 0.65 * live) * zone
    # sand is either poured (dark) or swept away (glass); grains show where it thins out
    c0 = np.clip((D - 0.08) / 0.75, 0, 1)
    c0 = c0 * c0 * (3 - 2 * c0)
    cover = np.clip(c0 + (G - 0.5) * 0.55 * 4 * c0 * (1 - c0) + 0.04 * COARSE, 0, 1)
    # loose single grains on the bare glass
    loose = ((G > 0.985) & (D < 0.35)).astype(np.float32)
    cover = np.maximum(cover, cv2.GaussianBlur(loose, (0, 0), 0.6) * 0.8)

    # fingertip lines: scraped bright through thick sand, trickled dark across bare glass
    sh = cv2.resize(s, (W // 2, H // 2), interpolation=cv2.INTER_AREA).astype(np.uint8)
    edges = cv2.Canny(sh, 22, 60)
    edges = cv2.resize(edges, (W, H), interpolation=cv2.INTER_NEAREST).astype(np.float32) / 255
    dog = cv2.GaussianBlur(s, (0, 0), 4) - cv2.GaussianBlur(s, (0, 0), 1.2)
    feat = np.clip((dog - 3) / 7, 0, 1) * ms
    sil = cv2.GaussianBlur(np.abs(cv2.Laplacian(cv2.GaussianBlur(m, (0, 0), 1.5), cv2.CV_32F)) * 8, (0, 0), 0.8).clip(0, 1)
    lines = cv2.GaussianBlur(edges * 0.45 * (1 - ms), (0, 0), 1.3)
    lines = np.clip(lines * 1.6, 0, 1) * (0.75 + 0.25 * (G > 0.3))   # grainy line edges
    thick = np.clip((cover - 0.45) / 0.3, 0, 1)
    cover = cover * (1 - lines * thick * 0.85) + lines * (1 - thick) * 0.75
    # the figures' features and outlines are trickled in dark sand
    dark = cv2.GaussianBlur(np.maximum(feat, sil * 0.8), (0, 0), 1.2)
    dark = np.clip(dark * 1.7, 0, 1) * (0.8 + 0.2 * (G > 0.3))
    cover = np.maximum(cover, dark * 0.92)

    # light table: warm amber, hottest in the middle, orange towards the frame edge
    r = np.sqrt(((GX - W * 0.5) / (W * 0.62)) ** 2 + ((GY - H * 0.47) / (H * 0.62)) ** 2)
    hot = np.clip(1 - r * 0.55, 0, 1)[..., None]
    light = np.float32([255, 236, 190]) * hot + np.float32([214, 128, 52]) * (1 - hot)
    flick = 1 + 0.012 * np.sin(frame_no * 1.7)
    T = np.clip(1 - cover, 0, 1)[..., None]
    sand = light * np.float32([0.16, 0.11, 0.07])   # thick sand: deep brown, a little warm light through
    col = light * T * flick + sand * (1 - T)
    # light bleeds around bare glass and grain edges
    bloom = cv2.GaussianBlur(np.clip(col - 150, 0, None), (0, 0), 9)
    col += bloom * 0.45 * np.float32([1.0, 0.85, 0.6])
    vig = 1 - 0.35 * np.clip(r - 0.55, 0, None) ** 1.5
    col *= vig[..., None]
    col += rng.normal(0, 2.0, (H, W, 1)).astype(np.float32)
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
