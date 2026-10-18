"""X-Ray Skeleton Scan: local approximation of style 94.

usage: python -I render.py <out_dir> [frame numbers...]   (default: all 179)

Needs pose.json next to this script (Apple Vision body + hand joints for every
source frame): `swift pose.swift ../../_source/frames pose.json`.

The room becomes a dim inverted blue negative. Each person (from the masks) is
a translucent glowing body with a bright rim, a faint inverted trace of the
face and clothes, and a procedural skeleton built from the pose joints: skull
with orbits / nasal hole / teeth / jaw, cervical + thoracic + lumbar vertebrae,
clavicles, rib cage hoops, pelvis, humerus, radius + ulna, hand bones (finger
chains when Vision finds the hand), femur, tibia. Joints are matched across
+-2 frames and averaged so the bones do not jitter. Then bloom, a cyan
scanner bar that sweeps down every 3 s, a short exposure flash at the top of
each sweep, radiograph film grain, a vignette and a lead "R" marker.
"""
import json
import sys
from pathlib import Path

import cv2
import numpy as np

HERE = Path(__file__).resolve().parent
SRC = HERE.parent.parent / "_source"
POSE = json.loads((HERE / "pose.json").read_text())
H, W = 1080, 1620
COUNT = 179


def load_frame(n):
    return cv2.imread(str(SRC / "frames" / f"frame_{n:03d}.png"))


def raw_mask(n):
    return cv2.imread(str(SRC / "masks" / f"frame_{n:03d}.png"), 0).astype(np.float32) / 255


def load_mask(n):
    m = raw_mask(n)
    # frames 023 / 068 have broken mattes (motion blur): patch from neighbours
    if 1 < n < COUNT:
        a, b = raw_mask(n - 1), raw_mask(n + 1)
        if m.sum() < 0.85 * min(a.sum(), b.sum()):
            m = np.maximum(m, np.minimum(a, b))
    # drop small blobs (office chair pieces)
    k, lab, st, _ = cv2.connectedComponentsWithStats((m > 0.5).astype(np.uint8))
    keep = np.zeros(k, bool)
    keep[1:] = st[1:, cv2.CC_STAT_AREA] > 0.012 * H * W
    m = m * cv2.dilate(keep[lab].astype(np.uint8), np.ones((9, 9), np.uint8))
    return m


# ---------------------------------------------------------------- pose
def bodies_raw(n, mask):
    out = []
    md = cv2.dilate((mask > 0.5).astype(np.uint8), np.ones((31, 31), np.uint8))
    for b in POSE[f"frame_{n:03d}.png"]["bodies"]:
        j = {k: np.array(v[:2]) for k, v in b.items() if v[2] > 0.15}
        ref = j.get("neck_1_joint", j.get("head_joint"))
        if ref is None:
            continue
        x, y = int(np.clip(ref[0], 0, W - 1)), int(np.clip(ref[1], 0, H - 1))
        if not md[y, x]:
            continue          # people on the TV screen
        ls, rs = j.get("left_shoulder_1_joint"), j.get("right_shoulder_1_joint")
        if ls is not None and rs is not None and np.linalg.norm(ls - rs) < 70:
            continue
        ears = j.get("left_ear_joint") is not None and j.get("right_ear_joint") is not None
        if (ls is None or rs is None) and not ears:
            continue          # too little to build a skeleton; the face pass may catch it
        out.append(j)
    # faces with no body pose (people bent close to the lens): build a pseudo body
    for f in POSE[f"frame_{n:03d}.png"].get("faces", []):
        x, y, w, h = f["box"]
        if "leftPupil" not in f or "rightPupil" not in f or w < 60:
            continue
        cx, cy = int(np.clip(x + w / 2, 0, W - 1)), int(np.clip(y + h / 2, 0, H - 1))
        if not md[cy, cx]:
            continue
        covered = False
        for j in out:
            e = j.get("head_joint", j.get("left_eye_joint"))
            if e is not None and x < e[0] < x + w and y < e[1] < y + h:
                covered = True
        if covered:
            continue
        a, b = np.array(f["leftPupil"]), np.array(f["rightPupil"])
        across = (a - b) / (np.linalg.norm(a - b) + 1e-6)
        down = np.array([-across[1], across[0]])
        if down[1] < 0:
            down = -down
        eye = (a + b) / 2
        sw = 2.4 * w
        neck = eye + down * 1.25 * h
        out.append({"left_eye_joint": a, "right_eye_joint": b, "neck_1_joint": neck,
                    "left_shoulder_1_joint": neck + across * sw / 2 + down * 0.1 * sw,
                    "right_shoulder_1_joint": neck - across * sw / 2 + down * 0.1 * sw})
    return out


_cache = {}


def bodies(n):
    if n not in _cache:
        _cache[n] = bodies_raw(n, load_mask(n))
    return _cache[n]


def anchor(j):
    return j.get("neck_1_joint", j.get("head_joint"))


def smoothed_bodies(n):
    """Average every joint over matched bodies in frames n-2..n+2."""
    res = []
    for j in bodies(n):
        a = anchor(j)
        acc = {k: [v * 4.0] for k, v in j.items()}
        wts = {k: [4.0] for k in j}
        for dn, w in ((-2, 1.0), (-1, 2.0), (1, 2.0), (2, 1.0)):
            m = n + dn
            if not 1 <= m <= COUNT:
                continue
            cands = [(np.linalg.norm(anchor(o) - a), o) for o in bodies(m)]
            if not cands:
                continue
            d, o = min(cands, key=lambda t: t[0])
            if d > 120:
                continue
            for k, v in o.items():
                if k in acc:
                    acc[k].append(v * w)
                    wts[k].append(w)
        res.append({k: sum(acc[k]) / sum(wts[k]) for k in acc})
    # bridge 1-2 frame detection dropouts so skeletons do not blink off
    for dp, dq in ((1, 1), (1, 2), (2, 1)):
        if n - dp < 1 or n + dq > COUNT:
            continue
        for p in bodies(n - dp):
            if any(np.linalg.norm(anchor(r) - anchor(p)) < 150 for r in res):
                continue
            qs = [q for q in bodies(n + dq) if np.linalg.norm(anchor(q) - anchor(p)) < 150]
            if not qs:
                continue
            q, t = qs[0], dp / (dp + dq)
            res.append({k: p[k] * (1 - t) + q[k] * t for k in p if k in q})
    return res


def hands(n):
    return [{k: np.array(v[:2]) for k, v in h.items() if v[2] > 0.2}
            for h in POSE[f"frame_{n:03d}.png"]["hands"]]


# ---------------------------------------------------------------- bone drawing
class Canvas:
    def __init__(self):
        self.fill = np.zeros((H, W), np.uint8)   # bone (255)
        self.hole = np.zeros((H, W), np.uint8)   # cavities cut out of bone
        self.soft = np.zeros((H, W), np.uint8)   # thin flat bone (skull vault, scapula, pelvis)

    @staticmethod
    def P(p):
        return (int(round(p[0] * 4)), int(round(p[1] * 4)))

    def line(self, a, b, t, img=None):
        img = self.fill if img is None else img
        cv2.line(img, self.P(a), self.P(b), 255, max(1, int(t)), cv2.LINE_AA, 2)

    def circle(self, c, r, img=None):
        img = self.fill if img is None else img
        cv2.circle(img, self.P(c), max(1, int(r * 4)), 255, -1, cv2.LINE_AA, 2)

    def ellipse(self, c, ax, ang, a0, a1, t=-1, img=None):
        img = self.fill if img is None else img
        cv2.ellipse(img, self.P(c), (max(1, int(ax[0] * 4)), max(1, int(ax[1] * 4))),
                    ang, a0, a1, 255, t if t < 0 else max(1, int(t)), cv2.LINE_AA, 2)

    def poly(self, pts, img=None):
        img = self.fill if img is None else img
        cv2.fillPoly(img, [np.array([self.P(p) for p in pts], np.int32)], 255, cv2.LINE_AA, 2)

    def long_bone(self, a, b, t, two=False):
        a, b = np.asarray(a, float), np.asarray(b, float)
        if two:   # radius + ulna / tibia + fibula
            d = b - a
            nrm = np.array([-d[1], d[0]]) / (np.linalg.norm(d) + 1e-6)
            for s, tt in ((-1, 0.55), (1, 0.42)):
                off = nrm * t * 0.55 * s
                self.line(a + off, b + off, t * tt)
            self.circle(a, t * 0.75)
            self.circle(b, t * 0.6)
        else:
            self.line(a, b, t)
            self.circle(a, t * 0.8)
            self.circle(b, t * 0.75)


def unit(v):
    return v / (np.linalg.norm(v) + 1e-6)


def draw_skeleton(cv, j):
    g = j.get
    ls, rs = g("left_shoulder_1_joint"), g("right_shoulder_1_joint")
    neck = g("neck_1_joint")
    le, re = g("left_eye_joint"), g("right_eye_joint")
    if ls is not None and rs is not None:
        sw = np.linalg.norm(ls - rs)
        across = unit(ls - rs)
    else:
        ears = [g("left_ear_joint"), g("right_ear_joint")]
        if ears[0] is None or ears[1] is None:
            return
        sw = 2.6 * np.linalg.norm(ears[0] - ears[1])
        across = unit(ears[0] - ears[1])
    down = np.array([-across[1], across[0]])
    if down[1] < 0:
        down = -down
    if neck is None:
        neck = (ls + rs) / 2 if ls is not None and rs is not None else None
    if neck is None:
        return

    # ---------------- skull
    if le is not None and re is not None:
        eye = (le + re) / 2
        d = max(np.linalg.norm(le - re), 0.2 * sw)
        ex = unit(le - re)
    elif g("head_joint") is not None:
        eye = g("head_joint") - down * 0.15 * sw
        d, ex = 0.22 * sw, across
    else:
        eye, d, ex = None, 0, across
    if eye is not None:
        up = np.array([ex[1], -ex[0]])
        if up[1] > 0:
            up = -up
        ang = np.degrees(np.arctan2(ex[1], ex[0]))
        cc, ca = eye + up * 0.62 * d, (1.18 * d, 1.42 * d)
        cv.ellipse(cc, ca, ang, 0, 360, img=cv.soft)                                  # cranium vault
        cv.ellipse(cc, ca, ang, 0, 360, t=max(3, 0.16 * d))                           # dense outer table
        cv.ellipse(cc - up * 0.1 * d, (ca[0] * 0.86, ca[1] * 0.86), ang, 200, 340, t=max(2, 0.06 * d))
        cv.ellipse(eye - up * 0.5 * d, (0.95 * d, 0.85 * d), ang, 0, 360, img=cv.soft)  # face block
        cv.ellipse(eye + up * 0.3 * d, (1.0 * d, 0.2 * d), ang, 0, 360)               # brow ridge
        jaw = [eye + ex * 1.15 * d - up * 0.25 * d, eye + ex * 1.0 * d - up * 1.35 * d,
               eye + ex * 0.45 * d - up * 1.95 * d, eye - ex * 0.45 * d - up * 1.95 * d,
               eye - ex * 1.0 * d - up * 1.35 * d, eye - ex * 1.15 * d - up * 0.25 * d]
        cv.ellipse(eye - up * 0.75 * d, (1.0 * d, 1.15 * d), ang, 8, 172, t=max(3, 0.24 * d))  # mandible
        for s_ in (-1, 1):
            cv.line(jaw[0 if s_ > 0 else 5], eye + ex * s_ * 0.98 * d - up * 0.95 * d, max(3, 0.2 * d))  # ramus
        cv.poly([eye - ex * 0.72 * d - up * 1.0 * d, eye + ex * 0.72 * d - up * 1.0 * d,
                 eye + ex * 0.72 * d - up * 1.42 * d, eye - ex * 0.72 * d - up * 1.42 * d])   # tooth rows
        for s in (-1, 1):                                                            # orbits
            c = eye + ex * s * 0.52 * d + up * 0.02 * d
            cv.ellipse(c, (0.36 * d, 0.32 * d), ang, 0, 360, img=cv.hole)
            cv.ellipse(c, (0.38 * d, 0.34 * d), ang, 0, 360, t=max(2, 0.07 * d))         # orbit rim
            cv.ellipse(eye + ex * s * 1.12 * d - up * 0.3 * d, (0.42 * d, 0.1 * d), ang, 0, 360)  # zygoma
        cv.poly([eye - up * 0.25 * d, eye + ex * 0.2 * d - up * 0.78 * d,
                 eye - up * 0.86 * d, eye - ex * 0.2 * d - up * 0.78 * d], img=cv.hole)  # nasal
        # teeth: dark gap line with bright tooth blocks
        tl = eye - up * 1.22 * d
        cv.line(tl - ex * 0.62 * d, tl + ex * 0.62 * d, 0.07 * d, img=cv.hole)
        for i in range(-5, 6):
            c = tl + ex * i * 0.115 * d
            cv.line(c - up * 0.04 * d, c - up * 0.2 * d, 1.2, img=cv.hole)
            cv.line(c + up * 0.04 * d, c + up * 0.2 * d, 1.2, img=cv.hole)
        skull_base = eye - up * 1.2 * d
    else:
        skull_base = neck - down * 0.35 * sw

    # ---------------- spine
    root = g("root")
    if root is None:
        lh, rh = g("left_upLeg_joint"), g("right_upLeg_joint")
        root = (lh + rh) / 2 if lh is not None and rh is not None else neck + down * 1.9 * sw
    vt = 0.11 * sw
    pts = [skull_base + (neck - skull_base) * t for t in np.linspace(0.1, 1, 5)]   # cervical
    pts += [neck + (root - neck) * t for t in np.linspace(0.06, 1, 17)]             # thoracic+lumbar
    for i, p in enumerate(pts):
        w = vt * (0.7 if i < 5 else 0.8 + 0.6 * i / len(pts))
        cv.ellipse(p, (w, w * 0.45), np.degrees(np.arctan2(across[1], across[0])), 0, 360)
        cv.line(p - across * w * 1.2, p + across * w * 1.2, 2.5)

    # ---------------- clavicles + ribs + sternum
    if ls is not None and rs is not None:
        top = neck + down * 0.08 * sw
        for s in (ls, rs):
            mid = (top + s) / 2 - down * 0.05 * sw
            cv.line(top, mid, 0.065 * sw)
            cv.line(mid, s, 0.06 * sw)
            cv.circle(s, 0.07 * sw)                                                   # humeral head
            sc = s + down * 0.25 * sw + (neck - s) * 0.25                             # scapula
            cv.ellipse(sc, (0.16 * sw, 0.26 * sw), np.degrees(np.arctan2(down[1], down[0])), 0, 360, img=cv.soft)
        ang = np.degrees(np.arctan2(across[1], across[0]))
        for i in range(11):
            f = i / 10
            c = neck + down * (0.2 + 0.11 * i) * sw
            ww = (0.26 + 0.2 * np.sin(np.pi * min(1, 0.25 + f))) * sw
            cv.ellipse(c + down * 0.2 * sw, (ww, 0.26 * sw), ang, 198, 342, t=0.045 * sw)
        cv.line(neck + down * 0.15 * sw, neck + down * 0.95 * sw, 0.07 * sw)   # sternum

    # ---------------- pelvis
    lh, rh = g("left_upLeg_joint"), g("right_upLeg_joint")
    if lh is not None and rh is not None:
        hw = np.linalg.norm(lh - rh)
        hc = (lh + rh) / 2
        for s, hp in ((1, lh), (-1, rh)):
            cv.ellipse(hc + across * s * 0.42 * hw - down * 0.35 * hw, (0.42 * hw, 0.3 * hw),
                       ang + s * 25, 0, 360, img=cv.soft)                             # iliac wing
            cv.ellipse(hc + across * s * 0.42 * hw - down * 0.35 * hw, (0.42 * hw, 0.3 * hw),
                       ang + s * 25, 180, 360, t=max(3, 0.05 * hw))                   # iliac crest
            cv.circle(hp, 0.16 * hw)
            cv.ellipse(hp - across * s * 0.1 * hw + down * 0.22 * hw, (0.16 * hw, 0.12 * hw), ang, 0, 360,
                       img=cv.hole)                                                   # obturator
        cv.ellipse(hc - down * 0.1 * hw, (0.2 * hw, 0.3 * hw), ang, 0, 360, img=cv.soft)  # sacrum

    # ---------------- limbs
    for side in ("left", "right"):
        sh, el, wr = g(f"{side}_shoulder_1_joint"), g(f"{side}_forearm_joint"), g(f"{side}_hand_joint")
        hp, kn, an = g(f"{side}_upLeg_joint"), g(f"{side}_leg_joint"), g(f"{side}_foot_joint")
        if sh is not None and el is not None:
            cv.long_bone(sh, el, 0.085 * sw)
        if el is not None and wr is not None:
            cv.long_bone(el, wr, 0.07 * sw, two=True)
        if hp is not None and kn is not None:
            cv.long_bone(hp, kn, 0.11 * sw)
        if kn is not None and an is not None:
            cv.long_bone(kn, an, 0.09 * sw, two=True)
        if el is not None and wr is not None:
            j[f"_{side}_wrist_dir"] = (wr, unit(wr - el), sw)


FINGERS = [["wrist", "thumbCMC", "thumbMP", "thumbIP", "thumbTip"],
           ["wrist", "indexMCP", "indexPIP", "indexDIP", "indexTip"],
           ["wrist", "middleMCP", "middlePIP", "middleDIP", "middleTip"],
           ["wrist", "ringMCP", "ringPIP", "ringDIP", "ringTip"],
           ["wrist", "littleMCP", "littlePIP", "littleDIP", "littleTip"]]
HAND_KEYS = {"wrist": "VNHLKWRI"}


def hand_point(h, name):
    for k, v in h.items():
        if k.lower().endswith(name.lower()) or k == name:
            return v
    return None


def draw_hand(cv, h):
    pts = {}
    for f in FINGERS:
        for nm in f:
            for k, v in h.items():
                if nm == "wrist" and "WRI" in k:
                    pts[nm] = v
                code = {"thumbCMC": "TCMC", "thumbMP": "TMP", "thumbIP": "TIP", "thumbTip": "TTIP",
                        "indexMCP": "IMCP", "indexPIP": "IPIP", "indexDIP": "IDIP", "indexTip": "ITIP",
                        "middleMCP": "MMCP", "middlePIP": "MPIP", "middleDIP": "MDIP", "middleTip": "MTIP",
                        "ringMCP": "RMCP", "ringPIP": "RPIP", "ringDIP": "RDIP", "ringTip": "RTIP",
                        "littleMCP": "PMCP", "littlePIP": "PPIP", "littleDIP": "PDIP", "littleTip": "PTIP"}.get(nm)
                if code and k.endswith(code) and not (code == "TIP" and k.endswith("TTIP")):
                    pts[nm] = v
    if "wrist" not in pts or "middleMCP" not in pts:
        return False
    size = np.linalg.norm(pts["middleMCP"] - pts["wrist"])
    t = max(3, 0.13 * size)
    for f in FINGERS:
        chain = [pts[k] for k in f if k in pts]
        for i, (a, b) in enumerate(zip(chain, chain[1:])):
            # shorten each phalanx so the joints show as gaps
            a2, b2 = a + (b - a) * 0.1, b - (b - a) * 0.12
            cv.line(a2, b2, t * (1.0 if i else 1.15))
            cv.circle(a2, t * 0.6)
            cv.circle(b2, t * 0.55)
    for k in ("wrist",):     # carpals
        c = pts[k] + (pts["middleMCP"] - pts[k]) * 0.18
        for dx in (-1, 0, 1):
            for dy in (0, 1):
                cv.circle(c + np.array([dx, dy]) * t * 1.1, t * 0.6)
    return True


def draw_generic_hand(cv, wr, dirv, sw):
    nrm = np.array([-dirv[1], dirv[0]])
    L = 0.42 * sw
    for i, s in enumerate(np.linspace(-1, 1, 5)):
        base = wr + dirv * 0.12 * sw + nrm * s * 0.12 * sw
        spread = unit(dirv + nrm * s * 0.25)
        a = base
        for k, frac in enumerate((0.42, 0.28, 0.2, 0.14)):
            b = a + spread * L * frac * (0.75 if i == 0 else 1.0)
            cv.line(a + (b - a) * 0.08, b - (b - a) * 0.1, max(3, 0.035 * sw))
            a = b


# ---------------------------------------------------------------- tone + colour
def lut():
    x = np.linspace(0, 1, 256)
    stops = [(0.0, (6, 4, 2)), (0.18, (52, 22, 6)), (0.42, (150, 90, 20)),
             (0.68, (245, 200, 90)), (0.86, (255, 238, 190)), (1.0, (255, 255, 255))]   # BGR
    out = np.zeros((256, 3), np.float32)
    for c in range(3):
        out[:, c] = np.interp(x, [s[0] for s in stops], [s[1][c] for s in stops])
    return out.astype(np.uint8)


LUT = lut()


def render(n):
    img = load_frame(n)
    m = load_mask(n)
    ms = cv2.GaussianBlur(m, (0, 0), 1.5)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
    inv = 1 - gray

    # room: dim inverted negative with edge relief
    hp = gray - cv2.GaussianBlur(gray, (0, 0), 6)
    edges = np.abs(cv2.Sobel(cv2.GaussianBlur(gray, (0, 0), 1.2), cv2.CV_32F, 1, 0)) + \
        np.abs(cv2.Sobel(cv2.GaussianBlur(gray, (0, 0), 1.2), cv2.CV_32F, 0, 1))
    bg = 0.07 + 0.16 * inv ** 1.5 + 0.55 * np.clip(edges * 1.6, 0, 0.6)

    # body: translucent flesh, thick in the middle, bright rim, faint inverted detail
    mb = (m > 0.5).astype(np.uint8)
    dist = cv2.distanceTransform(mb, cv2.DIST_L2, 5)
    rim = np.exp(-dist / 14) * mb
    thick = 1 - np.exp(-dist / 90)
    flesh = 0.12 + 0.2 * thick + 0.4 * rim + 0.5 * np.clip(-hp * 2.0 + edges * 0.6, -0.15, 0.4)
    flesh += 0.08 * (inv - 0.5)

    # skeleton (drawn at 4x subpixel precision)
    cv = Canvas()
    hand_done = []
    for h in hands(n):
        if draw_hand(cv, h):
            hand_done.append(next(v for k, v in h.items() if "WRI" in k))
    for j in smoothed_bodies(n):
        draw_skeleton(cv, j)
        for side in ("left", "right"):
            if f"_{side}_wrist_dir" in j:
                wr, dv, sw = j[f"_{side}_wrist_dir"]
                if not any(np.linalg.norm(wr - hw) < 0.4 * sw for hw in hand_done):
                    draw_generic_hand(cv, wr, dv, sw)
    fill = cv.fill.astype(np.float32) / 255
    soft = cv.soft.astype(np.float32) / 255
    hole = cv2.GaussianBlur(cv.hole.astype(np.float32) / 255, (0, 0), 1.0)
    clip = cv2.GaussianBlur(cv2.dilate(mb, np.ones((25, 25), np.uint8)).astype(np.float32), (0, 0), 6)
    fill *= clip
    soft *= clip
    core = cv2.erode(fill, np.ones((5, 5), np.uint8))
    cortex = np.clip(fill - core, 0, 1)
    rng = np.random.default_rng(7)                    # fixed trabecular texture
    trab = cv2.GaussianBlur(rng.random((H, W)).astype(np.float32), (0, 0), 2.2)
    trab = (trab - trab.mean()) / (trab.std() + 1e-6)
    bone = fill * (0.5 + 0.06 * trab) + cortex * 0.35
    bone = np.maximum(bone, soft * (0.24 + 0.05 * trab))
    bone *= 1 - 0.9 * hole
    bone = cv2.GaussianBlur(bone, (0, 0), 0.8)

    v = bg * (1 - ms) + flesh * ms
    v = 1 - (1 - np.clip(v, 0, 1)) * (1 - np.clip(bone, 0, 1) * 0.95)
    v -= 0.25 * hole * ms                              # cavities read dark

    # bloom
    v = np.clip(v, 0, 1)
    v += 0.3 * cv2.GaussianBlur(v ** 2.4, (0, 0), 14) + 0.2 * cv2.GaussianBlur(v ** 3, (0, 0), 60)

    # scanner bar: sweeps top to bottom every 36 frames (3 s), flash at its start
    ph = ((n - 1) % 36) / 36
    yb = -80 + ph * (H + 160)
    yy = np.arange(H, dtype=np.float32)[:, None]
    band = np.exp(-((yy - yb) / 26) ** 2) + 0.35 * np.exp(-np.clip(yy - yb, 0, None) / 120) * (yy > yb)
    v += 0.22 * band * (0.4 + 0.6 * ms)
    v += 0.6 * bone * np.exp(-((yy - yb) / 70) ** 2)
    flash = {0: 0.35, 1: 0.15}.get((n - 1) % 36, 0)
    v = v * (1 + flash) + flash * 0.12

    # radiograph grain + vignette
    g = np.random.default_rng(n).normal(0, 1, (H // 2, W // 2)).astype(np.float32)
    g = cv2.resize(cv2.GaussianBlur(g, (0, 0), 0.7), (W, H))
    v += 0.035 * g
    xx = np.linspace(-1, 1, W)[None, :]
    yv = np.linspace(-1, 1, H)[:, None]
    v *= 1 - 0.35 * np.clip((xx ** 2 + yv ** 2) / 2, 0, 1) ** 1.3

    out = LUT[np.clip(v * 255, 0, 255).astype(np.uint8)]

    # thin scan line itself, white core
    yi = int(round(yb))
    if 0 <= yi < H:
        cv2.line(out, (0, yi), (W, yi), (255, 250, 220), 2, cv2.LINE_AA)
    # lead marker
    cv2.rectangle(out, (W - 118, H - 118), (W - 52, H - 52), (230, 220, 170), 3, cv2.LINE_AA)
    cv2.putText(out, "R", (W - 104, H - 66), cv2.FONT_HERSHEY_DUPLEX, 1.6, (245, 240, 210), 3, cv2.LINE_AA)
    return out


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    nums = [int(a) for a in sys.argv[2:]] or range(1, COUNT + 1)
    for n in nums:
        cv2.imwrite(str(out / f"frame_{n:03d}.png"), render(n))
        print(n, end=" ", flush=True)
    print()


if __name__ == "__main__":
    main()
