"""Build a clean background plate (people removed) from all frames.

usage: python plate.py <frames_dir> <masks_dir> <out_png>
Per pixel: median over the frames where no person (generously dilated) covers
it. Pixels seen in too few frames are inpainted from their surroundings.
"""
import os
import sys

import cv2
import numpy as np

FRAMES, MASKS, OUT = sys.argv[1:4]
names = sorted(f for f in os.listdir(FRAMES) if f.endswith(".png"))
k = np.ones((71, 71), np.uint8)
imgs, frees = [], []
for f in names:
    imgs.append(cv2.imread(os.path.join(FRAMES, f)))
    m = cv2.imread(os.path.join(MASKS, f), cv2.IMREAD_GRAYSCALE)
    frees.append(cv2.dilate((m > 25).astype(np.uint8), k) == 0)
imgs = np.stack(imgs)            # N,H,W,3 uint8
frees = np.stack(frees)          # N,H,W bool
N, h, w, _ = imgs.shape
cnt = frees.sum(0)
plate = np.zeros((h, w, 3), np.float32)
for y0 in range(0, h, 60):       # chunked masked median
    blk = imgs[:, y0:y0 + 60].astype(np.float32)
    fr = frees[:, y0:y0 + 60]
    blk[~fr] = np.nan
    with np.errstate(all="ignore"):
        plate[y0:y0 + 60] = np.nan_to_num(np.nanmedian(blk, 0))
hole = (cnt < 6).astype(np.uint8)
hole = cv2.dilate(hole, np.ones((9, 9), np.uint8))
print("hole fraction", hole.mean())
# room is mostly horizontal structure (planter, cabinet, window): fill each
# covered run along the row by blending its two visible ends; runs that touch
# the frame edge fall back to Telea inpainting
small = cv2.resize(plate.clip(0, 255).astype(np.uint8), (w // 4, h // 4), interpolation=cv2.INTER_AREA)
hs = cv2.resize(hole * 255, (w // 4, h // 4), interpolation=cv2.INTER_NEAREST)
fill = cv2.inpaint(small, hs, 30, cv2.INPAINT_TELEA)
fill = cv2.resize(cv2.GaussianBlur(fill, (0, 0), 2), (w, h), interpolation=cv2.INTER_CUBIC).astype(np.float32)
for y in range(h):
    row = hole[y]
    x = 0
    while x < w:
        if row[x]:
            x1 = x
            while x1 < w and row[x1]:
                x1 += 1
            if x > 2 and x1 < w - 2:
                a = plate[y, max(0, x - 6):x - 1].mean(0)
                b = plate[y, x1 + 1:x1 + 6].mean(0)
                t = np.linspace(0, 1, x1 - x)[:, None]
                fill[y, x:x1] = a * (1 - t) + b * t
            x = x1
        else:
            x += 1
fill = cv2.GaussianBlur(fill, (0, 0), sigmaX=1.0, sigmaY=4.0)
soft = cv2.GaussianBlur(hole.astype(np.float32), (0, 0), 5)[..., None]
out = plate * (1 - soft) + fill * soft
cv2.imwrite(OUT, out.clip(0, 255).astype(np.uint8))
