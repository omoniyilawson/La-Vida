"""Watercolour botanical collection for La Vida.

A small pigment simulator: each wash is a stack of slightly different deformed polygons,
pigment pools at the drying edge, settles into the paper grain, and glazes subtractively
(Beer-Lambert absorbance), so overlapping layers deepen like real transparent watercolour.
Output is RGBA meant to be multiplied onto paper.
"""
import numpy as np
from scipy import ndimage as ndi
from PIL import Image, ImageDraw
import sys, os, math

OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/la-vida-site/assets/img"
os.makedirs(OUT, exist_ok=True)

# palette (target colour at full density)
BLUSH = (238, 196, 186)
BLUSH_MID = (226, 166, 156)
ROSE_DEEP = (192, 116, 112)
PEACH = (240, 196, 170)
IVORY_SHADOW = (214, 204, 182)
IVORY_EDGE = (196, 184, 158)
OLIVE = (128, 136, 86)
SAGE = (128, 156, 122)
EUCALYPT = (132, 160, 150)
FOREST = (62, 92, 68)
STEM = (104, 112, 70)
GOLD = (176, 141, 70)
GOLD_DEEP = (140, 104, 44)
CENTRE = (196, 170, 90)


def absorb(c):
    c = np.clip(np.array(c, np.float32) / 255, .03, 1)
    return -np.log(c)


class Paper:
    def __init__(self, W, H, seed):
        self.W, self.H = W, H
        self.A = np.zeros((H, W, 3), np.float32)
        self.r = np.random.default_rng(seed)
        g = ndi.gaussian_filter(self.r.standard_normal((H, W)), 1.4)
        g2 = ndi.gaussian_filter(self.r.standard_normal((H, W)), 6)
        g = (g - g.min()) / (g.max() - g.min()); g2 = (g2 - g2.min()) / (g2.max() - g2.min())
        self.grain = (.65 * g + .35 * g2).astype(np.float32)

    # -- geometry helpers
    def deform(self, pts, depth, var):
        p = pts
        for _ in range(depth):
            a = p; b = np.roll(p, -1, axis=0)
            L = np.linalg.norm(b - a, axis=1, keepdims=True)
            mid = (a + b) / 2 + self.r.normal(0, 1, a.shape) * L * var
            o = np.empty((len(p) * 2, 2)); o[0::2] = a; o[1::2] = mid
            p = o; var *= .65
        return p

    def _bbox(self, pts, pad):
        x0 = int(max(0, pts[:, 0].min() - pad)); x1 = int(min(self.W, pts[:, 0].max() + pad))
        y0 = int(max(0, pts[:, 1].min() - pad)); y1 = int(min(self.H, pts[:, 1].max() + pad))
        return x0, y0, x1, y1

    def _poly_mask(self, polys, box):
        x0, y0, x1, y1 = box
        img = Image.new("L", (x1 - x0, y1 - y0), 0)
        d = ImageDraw.Draw(img)
        for p in polys:
            d.polygon([(float(x - x0), float(y - y0)) for x, y in p], fill=255)
        return np.asarray(img, np.float32) / 255

    # -- painting primitives
    def wash(self, poly, colour, strength=1.0, layers=7, var=.06, edge=1.0, soft=1.0, bleed=0.0, cover=0.0):
        poly = np.asarray(poly, np.float64)
        if len(poly) < 3: return
        span = max(np.ptp(poly[:, 0]), np.ptp(poly[:, 1]))
        if span < 1.5: return
        base = self.deform(poly, 2, var)
        box = self._bbox(base, 8 + span * .12 + bleed * 3)
        x0, y0, x1, y1 = box
        if x1 <= x0 or y1 <= y0: return
        acc = np.zeros((y1 - y0, x1 - x0), np.float32)
        for _ in range(layers):
            acc += self._poly_mask([self.deform(base, 2, var * .55)], box)
        m = acc / layers
        m = ndi.gaussian_filter(m, soft * max(.6, span * .004) + bleed)
        e = np.clip(m - ndi.gaussian_filter(m, 2.2 + span * .01), 0, None) * 2.6
        if cover > 0:
            self.A[y0:y1, x0:x1] *= (1 - cover * np.clip(m * 1.3, 0, 1))[..., None]
        g = self.grain[y0:y1, x0:x1]
        dens = (m * .62 + e * edge) * (.78 + .44 * g) * strength
        self.A[y0:y1, x0:x1] += dens[..., None] * absorb(colour)

    def stroke(self, pts, width, colour, strength=1.0, taper=True):
        pts = np.asarray(pts, np.float64)
        box = self._bbox(pts, width * 2 + 4)
        x0, y0, x1, y1 = box
        if x1 <= x0 or y1 <= y0: return
        img = Image.new("L", (x1 - x0, y1 - y0), 0)
        d = ImageDraw.Draw(img)
        n = len(pts)
        for i in range(n - 1):
            t = i / max(1, n - 2)
            w = width * ((1 - .75 * t) if taper else 1)
            d.line([(pts[i, 0] - x0, pts[i, 1] - y0), (pts[i + 1, 0] - x0, pts[i + 1, 1] - y0)], fill=255, width=max(1, int(round(w))))
        m = ndi.gaussian_filter(np.asarray(img, np.float32) / 255, .7)
        g = self.grain[y0:y1, x0:x1]
        self.A[y0:y1, x0:x1] += (m * (.8 + .3 * g) * strength)[..., None] * absorb(colour)

    def reserve(self, poly, cover=.97):
        poly = np.asarray(poly, np.float64)
        box = self._bbox(poly, 6)
        x0, y0, x1, y1 = box
        if x1 <= x0 or y1 <= y0: return
        m = ndi.gaussian_filter(self._poly_mask([self.deform(poly, 2, .05)], box), 1.5)
        self.A[y0:y1, x0:x1] *= (1 - cover * m)[..., None]

    def dot(self, x, y, r, colour, strength=1.0):
        self.wash(ellipse(x, y, r, r, 0, 10), colour, strength, layers=3, var=.08, edge=.6)

    def rgba(self):
        rgb = np.exp(-self.A)
        a = 1 - rgb.min(axis=2)
        a = np.clip(a, 0, 1)
        safe = np.maximum(a, 1e-4)[..., None]
        c = np.clip((rgb - (1 - a)[..., None]) / safe, 0, 1)
        out = np.dstack([c, a])
        return Image.fromarray((out * 255).astype(np.uint8), "RGBA")


# ---------------------------------------------------------------- shapes
def ellipse(x, y, rx, ry, ang, n=14):
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    c, s = math.cos(ang), math.sin(ang)
    px, py = np.cos(t) * rx, np.sin(t) * ry
    return np.stack([x + px * c - py * s, y + px * s + py * c], 1)


def leaf_shape(x, y, ang, L, W, bend=0.0, n=10, round_=False):
    pts_l, pts_r = [], []
    for i in range(n + 1):
        t = i / n
        prof = math.sin(math.pi * t) ** (0.6 if round_ else 0.85) * (1 - .25 * t)
        cx = t * L
        cy = bend * L * (t * t - t) * -1
        pts_l.append((cx, cy + prof * W / 2))
        pts_r.append((cx, cy - prof * W / 2))
    pts = pts_l + pts_r[::-1][1:-1]
    c, s = math.cos(ang), math.sin(ang)
    return np.array([(x + px * c - py * s, y + px * s + py * c) for px, py in pts])


def along(p0, ang, L, bend, n):
    """points along a gently bending stem"""
    pts = []
    a = ang
    x, y = p0
    for i in range(n + 1):
        pts.append((x, y))
        a += bend / n
        x += math.cos(a) * L / n
        y += math.sin(a) * L / n
    return np.array(pts)


# ---------------------------------------------------------------- botanical elements
def leaf(P, x, y, ang, L, colour=None, kind="olive"):
    r = P.r
    if kind == "euc":
        L = L * .7
        W = L * (.75 + r.random() * .15)
        poly = leaf_shape(x, y, ang, L, W, bend=(r.random() - .5) * .3, round_=True)
        col = colour or EUCALYPT
    else:
        W = L * (.26 + r.random() * .1)
        poly = leaf_shape(x, y, ang, L, W, bend=(r.random() - .5) * .5)
        col = colour or (OLIVE if r.random() < .5 else SAGE)
    P.wash(poly, col, .38 + r.random() * .22, var=.04, edge=1.1, cover=.55)
    # darker glaze on one half for form
    c, s = math.cos(ang), math.sin(ang)
    half = leaf_shape(x + (-s) * L * .04, y + c * L * .04, ang, L * .9, (L * .13 if kind != "euc" else L * .35), bend=0)
    P.wash(half, FOREST if r.random() < .5 else col, .12 + r.random() * .12, var=.05, edge=.6)
    if kind != "euc":
        mid = along((x, y), ang, L * .85, 0, 6)
        P.stroke(mid, max(1, L * .014), FOREST, .22)


def stem(P, pts, w, colour=STEM, strength=.8):
    P.stroke(pts, w, colour, strength)


def rose(P, x, y, R, deep=False):
    r = P.r
    P.reserve(ellipse(x, y, R * .96, R * .9, 0, 18), .9)
    P.wash(ellipse(x, y, R * 1.0, R * .92, r.random(), 16), BLUSH, .42, var=.09, edge=.7, bleed=1.5)
    a0 = r.random() * 6.28
    # outer petals: irregular cupped shapes of different sizes, painted wet-on-dry
    n = 5 + int(r.random() * 2)
    for i in range(n):
        a = a0 + i * 2 * math.pi / n + (r.random() - .5) * .5
        d = R * (.42 + r.random() * .14)
        px, py = x + math.cos(a) * d, y + math.sin(a) * d
        rx, ry = R * (.38 + r.random() * .18), R * (.26 + r.random() * .12)
        P.wash(ellipse(px, py, rx, ry, a + math.pi / 2 + (r.random() - .5) * .4, 16), BLUSH_MID if r.random() < .5 else BLUSH, .26 + r.random() * .2, var=.09, edge=2.0)
    # cupped centre: one darker crescent and the heart
    P.wash(ellipse(x + R * .05, y + R * .08, R * .42, R * .3, a0 + 1.2, 14), BLUSH_MID, .4, var=.08, edge=1.8)
    P.wash(ellipse(x + R * .06, y + R * .02, R * .2, R * .15, a0, 12), ROSE_DEEP, .45 if not deep else .7, var=.1, edge=1.4)
    for k in range(2):
        rr = R * (.14 + k * .16)
        aa = a0 + k * 2.1
        arc = np.array([(x + math.cos(aa + t) * rr, y + math.sin(aa + t) * rr * .8) for t in np.linspace(0, 1.6 + r.random(), 12)])
        P.stroke(arc, max(1.2, R * .024), ROSE_DEEP, .35, taper=True)


def blossom(P, x, y, R):
    r = P.r
    rot = r.random() * 6.28
    P.reserve(ellipse(x, y, R * 1.05, R * 1.05, 0, 16), .9)
    for i in range(5):
        a = rot + i * 2 * math.pi / 5
        px, py = x + math.cos(a) * R * .52, y + math.sin(a) * R * .52
        petal = ellipse(px, py, R * .52, R * .4, a, 14)
        P.wash(petal, IVORY_SHADOW, .32, var=.05, edge=2.2)
        # shadow near the centre gives volume on ivory paper
        P.wash(ellipse(x + math.cos(a) * R * .3, y + math.sin(a) * R * .3, R * .22, R * .15, a, 10), IVORY_EDGE, .3, var=.08, edge=.6)
    P.wash(ellipse(x, y, R * .17, R * .17, 0, 10), CENTRE, .8, var=.06, edge=1)
    for i in range(7):
        a = r.random() * 6.28; d = R * (.12 + r.random() * .14)
        P.dot(x + math.cos(a) * d, y + math.sin(a) * d, max(1.2, R * .035), GOLD_DEEP, .9)


def bud(P, x, y, R, ang):
    r = P.r
    c, s = math.cos(ang), math.sin(ang)
    P.reserve(leaf_shape(x, y, ang, R * 2.2, R * 1.3, round_=True), .9)
    P.wash(leaf_shape(x, y, ang, R * 2.2, R * 1.3, round_=True), BLUSH_MID, .6, var=.05, edge=1.3)
    for k in (-1, 1):
        P.wash(leaf_shape(x, y, ang + k * .5, R * 1.3, R * .45), SAGE, .7, var=.05, edge=1)
    stem(P, along((x, y), ang + math.pi, R * 2.5, (r.random() - .5) * .8, 6), max(1.5, R * .12))


def gold_sprig(P, x, y, ang, L):
    r = P.r
    pts = along((x, y), ang, L, (r.random() - .5) * .9, 10)
    P.stroke(pts, max(1.2, L * .012), GOLD, .9)
    for i in range(2, len(pts), 2):
        P.dot(pts[i][0] + (r.random() - .5) * L * .06, pts[i][1] + (r.random() - .5) * L * .06, max(1.4, L * .014), GOLD, 1.0)


def breath(P, x, y, s, n=10):
    r = P.r
    for _ in range(n):
        a = r.random() * 6.28; d = s * r.random()
        P.dot(x + math.cos(a) * d, y + math.sin(a) * d, s * (.04 + r.random() * .04), IVORY_EDGE, .7)


def branch(P, p0, ang, L, scale, leafy=1.0, tip="bud", kind=None):
    """a stem with alternating leaves and an optional tip"""
    r = P.r
    pts = along(p0, ang, L, (r.random() - .5) * 1.0, 22)
    stem(P, pts, max(1.5, scale * .02))
    k = kind or ("euc" if r.random() < .35 else "olive")
    for i in range(2, len(pts) - 1):
        if r.random() > leafy: continue
        a = math.atan2(pts[i + 1][1] - pts[i][1], pts[i + 1][0] - pts[i][0])
        side = 1 if i % 2 else -1
        ll = scale * (.09 + r.random() * .05) * (1 - .4 * i / len(pts)) * (1.2 if k == "euc" else 1)
        leaf(P, pts[i][0], pts[i][1], a + side * (.6 + r.random() * .4), ll, kind=k)
    end = pts[-1]
    a = math.atan2(pts[-1][1] - pts[-2][1], pts[-1][0] - pts[-2][0])
    if tip == "bud": bud(P, end[0], end[1], scale * .045, a)
    elif tip == "blossom": blossom(P, end[0], end[1], scale * .07)
    elif tip == "leaf": leaf(P, end[0], end[1], a, scale * .1, kind=k)
    return pts


def cluster(P, x, y, s, ang=0.0, roses=2, blossoms=2):
    r = P.r
    # back foliage
    for i in range(9):
        a = ang + (r.random() - .5) * 2.6
        leaf(P, x + math.cos(a) * s * .05, y + math.sin(a) * s * .05, a, s * (.17 + r.random() * .1), kind="euc" if i % 3 == 0 else "olive")
    for i in range(roses):
        a = ang + (r.random() - .5) * 1.4
        d = 0 if i == 0 else s * (.2 + r.random() * .1)
        rose(P, x + math.cos(a) * d, y + math.sin(a) * d, s * (.16 if i == 0 else .11))
    for i in range(blossoms):
        a = ang + (r.random() - .5) * 2.4
        d = s * (.2 + r.random() * .14)
        blossom(P, x + math.cos(a) * d, y + math.sin(a) * d, s * (.09 + r.random() * .03))
    # front foliage tucked around the flowers
    for i in range(7):
        a = ang + (r.random() - .5) * 3.0
        d = s * (.2 + r.random() * .12)
        leaf(P, x + math.cos(a) * d, y + math.sin(a) * d, a + (r.random() - .5) * .6, s * (.1 + r.random() * .07), kind="euc" if i % 3 == 0 else "olive")
    breath(P, x + math.cos(ang) * s * .3, y + math.sin(ang) * s * .3, s * .12, 8)


# ---------------------------------------------------------------- compositions
def corner(seed, W=1200, H=1200):
    """arrangement anchored in the top-left, spraying right and down"""
    P = Paper(W, H, seed)
    r = P.r
    s = W
    # long trailing branches along both edges
    branch(P, (40, 70), .05 + r.random() * .1, s * .78, s, .9, "bud")
    branch(P, (70, 40), 1.45 + r.random() * .1, s * .7, s, .9, "bud")
    branch(P, (60, 60), .55, s * .48, s, .8, "blossom")
    branch(P, (60, 60), .95, s * .42, s, .8, "leaf", kind="euc")
    branch(P, (90, 50), .25, s * .55, s * .9, .7, "leaf", kind="euc")
    branch(P, (50, 90), 1.2, s * .5, s * .9, .7, "blossom")
    for _ in range(3):
        gold_sprig(P, s * (.12 + r.random() * .2), s * (.12 + r.random() * .2), .2 + r.random() * 1.1, s * .2)
    # focal bouquet
    cluster(P, s * .16, s * .15, s * .9, ang=.78, roses=3, blossoms=3)
    rose(P, s * .33, s * .1, s * .08)
    rose(P, s * .1, s * .34, s * .075)
    blossom(P, s * .42, s * .2, s * .06)
    blossom(P, s * .2, s * .42, s * .055)
    bud(P, s * .5, s * .08, s * .03, .1)
    return P.rgba()


def garland(seed, W=2000, H=560):
    P = Paper(W, H, seed)
    r = P.r
    pts = np.array([(t, H * .2 + math.sin(t / W * math.pi) * H * .45) for t in np.linspace(40, W - 40, 60)])
    stem(P, pts, 3)
    for i in range(1, len(pts) - 1):
        a = math.atan2(pts[i + 1][1] - pts[i - 1][1], pts[i + 1][0] - pts[i - 1][0])
        for side in (-1, 1):
            if r.random() < .8:
                leaf(P, pts[i][0], pts[i][1], a + side * (.7 + r.random() * .4), H * (.14 + r.random() * .08), kind="euc" if r.random() < .3 else "olive")
    mid = pts[len(pts) // 2]
    cluster(P, mid[0], mid[1], H * .9, ang=math.pi / 2, roses=3, blossoms=3)
    for f in (.22, .78):
        p = pts[int(len(pts) * f)]
        rose(P, p[0], p[1], H * .085); blossom(P, p[0] + 40, p[1] + 30, H * .06)
    for f in (.08, .92):
        p = pts[int(len(pts) * f)]
        bud(P, p[0], p[1], H * .03, -math.pi / 2)
    for _ in range(4):
        p = pts[r.integers(5, len(pts) - 5)]
        gold_sprig(P, p[0], p[1], r.random() * 6.28, H * .25)
    return P.rgba()


def wreath(seed, S=1400):
    P = Paper(S, S, seed)
    r = P.r
    cx = cy = S / 2
    R = S * .37
    angs = np.linspace(0, 2 * math.pi, 120)
    pts = np.array([(cx + math.cos(a) * R, cy + math.sin(a) * R) for a in angs])
    stem(P, pts, 2.5)
    for i, a in enumerate(angs[:-1]):
        dens = .55 + .45 * (math.cos(a - 3.6) ** 2)  # fuller at upper-left and lower-right
        if r.random() > dens: continue
        tang = a + math.pi / 2
        for side in (-1, 1):
            if r.random() < .75:
                leaf(P, pts[i][0], pts[i][1], tang + side * (.6 + r.random() * .5) + (math.pi if i % 2 else 0), S * (.05 + r.random() * .035), kind="euc" if r.random() < .35 else "olive")
    for a, sc in [(3.75, 1.0), (.62, .85)]:
        x, y = cx + math.cos(a) * R, cy + math.sin(a) * R
        cluster(P, x, y, S * .5 * sc, ang=a + math.pi / 2, roses=3, blossoms=3)
    for a in (1.9, 5.3):
        x, y = cx + math.cos(a) * R, cy + math.sin(a) * R
        blossom(P, x, y, S * .035); rose(P, x + 20, y + 15, S * .03)
    for a in np.linspace(0, 6.28, 7)[:-1]:
        gold_sprig(P, cx + math.cos(a) * R, cy + math.sin(a) * R, a + 1.6, S * .08)
    return P.rgba()


def arch(seed, W=1400, H=1900):
    P = Paper(W, H, seed)
    r = P.r
    cx = W / 2
    R = W * .4
    top = R + W * .06
    pts = [(cx - R + math.sin(y / 60) * 6, y) for y in np.linspace(H - 60, top, 40)]
    pts += [(cx + math.cos(a) * R, top + math.sin(a) * R) for a in np.linspace(math.pi, 2 * math.pi, 70)]
    pts += [(cx + R + math.sin(y / 60) * 6, y) for y in np.linspace(top, H - 60, 40)]
    pts = np.array(pts)
    stem(P, pts, 3)
    for i in range(1, len(pts) - 1):
        a = math.atan2(pts[i + 1][1] - pts[i - 1][1], pts[i + 1][0] - pts[i - 1][0])
        for side in (-1, 1):
            if r.random() < .7:
                leaf(P, pts[i][0], pts[i][1], a + side * (.7 + r.random() * .5), W * (.045 + r.random() * .035), kind="euc" if r.random() < .35 else "olive")
    # heavy at the base corners and the crown
    cluster(P, cx - R, H - 160, W * .62, ang=-1.2, roses=3, blossoms=3)
    cluster(P, cx + R, H - 180, W * .55, ang=-1.9, roses=3, blossoms=3)
    cluster(P, cx - R * .55, top - R * .82, W * .42, ang=.6, roses=2, blossoms=2)
    cluster(P, cx + R * .2, top - R * 1.0, W * .22, ang=1.6, roses=1, blossoms=2)
    for k in range(6):
        p = pts[int(len(pts) * (k + .5) / 6)]
        (rose if k % 2 else blossom)(P, p[0], p[1], W * .03)
    for _ in range(6):
        p = pts[r.integers(0, len(pts))]
        gold_sprig(P, p[0], p[1], r.random() * 6.28, W * .09)
    return P.rgba()


def separator(seed, W=900, H=220):
    P = Paper(W, H, seed)
    r = P.r
    cx, cy = W / 2, H / 2
    for side in (-1, 1):
        pts = np.array([(cx + side * t, cy + math.sin(t / 70) * 10 * side) for t in np.linspace(20, W * .44, 24)])
        stem(P, pts, 2)
        for i in range(1, len(pts) - 1, 1):
            a = math.atan2(pts[i + 1][1] - pts[i - 1][1], pts[i + 1][0] - pts[i - 1][0])
            sd = 1 if i % 2 else -1
            leaf(P, pts[i][0], pts[i][1], a + sd * .75, H * (.22 - .12 * i / len(pts)), kind="olive" if i % 3 else "euc")
        bud(P, pts[-1][0], pts[-1][1], H * .05, 0 if side > 0 else math.pi)
    rose(P, cx, cy, H * .2)
    blossom(P, cx - H * .3, cy + H * .12, H * .13)
    blossom(P, cx + H * .32, cy - H * .1, H * .11)
    return P.rgba()


def posy(seed, S=520):
    P = Paper(S, S, seed)
    cluster(P, S / 2, S / 2, S * .8, ang=-math.pi / 2, roses=2, blossoms=2)
    return P.rgba()


def save(img, name, q=88, sizes=()):
    img = trim(img)
    img.save(f"{OUT}/{name}.webp", quality=q, method=6)
    for w in sizes:
        h = round(img.height * w / img.width)
        img.resize((w, h), Image.LANCZOS).save(f"{OUT}/{name}-{w}.webp", quality=q, method=6)


def trim(img, pad=6):
    a = np.asarray(img)[..., 3]
    ys, xs = np.nonzero(a > 6)
    if len(xs) == 0: return img
    return img.crop((max(0, xs.min() - pad), max(0, ys.min() - pad), min(img.width, xs.max() + pad), min(img.height, ys.max() + pad)))


if __name__ == "__main__":
    which = sys.argv[2] if len(sys.argv) > 2 else "all"
    if which in ("all", "corner"):
        save(corner(101), "floral-corner-a", sizes=(600,))
        save(corner(202), "floral-corner-b", sizes=(600,))
    if which in ("all", "garland"): save(garland(303), "floral-garland", sizes=(1000,))
    if which in ("all", "wreath"): save(wreath(404), "floral-wreath", sizes=(800,))
    if which in ("all", "arch"): save(arch(505), "floral-arch", sizes=(800,))
    if which in ("all", "separator"): save(separator(606), "floral-separator", sizes=(450,))
    if which in ("all", "posy"):
        for i in range(4): save(posy(700 + i), f"floral-posy-{i+1}", sizes=(260,))
    print("done", which)
