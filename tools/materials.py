"""Paper, wax seal and silk ribbon assets for La Vida (rendered with numpy)."""
import numpy as np
from scipy import ndimage as ndi
from PIL import Image, ImageDraw, ImageFont
import sys, os

OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/la-vida-site/assets/img"
FONTS = "/home/claude/vendor/node_modules/@fontsource"
os.makedirs(OUT, exist_ok=True)


def wblur(a, s):
    return ndi.gaussian_filter(a, s, mode="wrap")


def norm(a):
    a = a - a.mean()
    return a / (a.std() + 1e-9)


# ---------------------------------------------------------------- cotton paper
def fibres(S, n, rng, lo=30, hi=150):
    img = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(img)
    for _ in range(n):
        x, y = rng.random() * S, rng.random() * S
        a = rng.random() * np.pi * 2
        L = lo + rng.random() * (hi - lo)
        bend = (rng.random() - .5) * 1.6
        v = int(60 + rng.random() * 195)
        pts = []
        for t in np.linspace(0, 1, 12):
            aa = a + bend * t
            pts.append((x + np.cos(aa) * L * t, y + np.sin(aa) * L * t))
        for ox in (-S, 0, S):
            for oy in (-S, 0, S):
                d.line([(p[0] + ox, p[1] + oy) for p in pts], fill=v, width=1)
    return np.asarray(img, np.float32) / 255


def paper(S, base, fibre_tone, seed, dark=False):
    rng = np.random.default_rng(seed)
    mott = norm(wblur(rng.standard_normal((S, S)), 60))
    mid = norm(wblur(rng.standard_normal((S, S)), 5))
    tooth = norm(wblur(rng.standard_normal((S, S)), 1.2))
    fib = wblur(fibres(S, 1800, rng), .6) + .5 * wblur(fibres(S, 900, rng, 8, 40), .5)
    h = .55 * mid + .35 * tooth + 2.2 * fib
    gx = (np.roll(h, -1, 1) - np.roll(h, 1, 1)) * .5
    gy = (np.roll(h, -1, 0) - np.roll(h, 1, 0)) * .5
    k = .9
    n = np.dstack([-gx * k, -gy * k, np.ones_like(h)])
    n /= np.linalg.norm(n, axis=2, keepdims=True)
    L = np.array([-.55, -.6, .58]); L /= np.linalg.norm(L)
    shade = (n @ L) / L[2]
    base = np.array(base, np.float32) / 255
    ft = np.array(fibre_tone, np.float32) / 255
    col = base[None, None, :] * (1 + .018 * mott[..., None]) * (1 + .09 * (shade[..., None] - 1))
    fmask = np.clip(fib * 1.4, 0, 1)[..., None]
    col = col * (1 - .35 * fmask) + ft * .35 * fmask
    return Image.fromarray((np.clip(col, 0, 1) * 255).astype(np.uint8))


def build_paper():
    paper(1024, (250, 246, 236), (255, 255, 252), 7).save(f"{OUT}/paper-ivory.webp", quality=86)
    paper(1024, (241, 233, 216), (252, 249, 240), 9).save(f"{OUT}/paper-envelope.webp", quality=86)
    paper(1024, (36, 57, 44), (70, 96, 78), 11).save(f"{OUT}/paper-forest.webp", quality=86)
    paper(1024, (235, 223, 202), (247, 240, 226), 13).save(f"{OUT}/paper-backdrop.webp", quality=84)


# ---------------------------------------------------------------- wax seal
def smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


def build_seal(S=1024, SS=2):
    N = S * SS
    rng = np.random.default_rng(42)
    yy, xx = np.mgrid[0:N, 0:N].astype(np.float32)
    cx = cy = N / 2
    dx, dy = xx - cx, yy - cy
    rho = np.hypot(dx, dy)
    th = np.arctan2(dy, dx)
    R = N * .41
    # poured, irregular outline
    k = 1 + .022 * np.sin(5 * th + 1.3) + .014 * np.sin(9 * th + .4) + .008 * np.sin(17 * th + 2.0)
    for ba, bh, bw in [(.6, .085, .05), (2.25, .06, .03), (3.95, .1, .06), (5.25, .05, .025)]:
        dd = np.arctan2(np.sin(th - ba), np.cos(th - ba))
        k = k + bh * np.exp(-dd * dd / bw)
    rr = R * k
    d = rr - rho  # distance inside edge (approx)
    inside = d > 0
    T = N * .05  # wax thickness
    w = R * .16
    t = np.clip(d / w, 0, 1)
    h = T * np.sqrt(1 - (1 - t) ** 2)
    h += T * .12 * smoothstep(0, R * .5, d)  # slightly domed body
    # stamp impression
    Ri = R * .72
    wall = R * .025
    rec = 1 - smoothstep(Ri - wall, Ri + wall, rho)
    h -= T * .55 * rec
    h += T * .22 * np.exp(-((rho - Ri - R * .045) / (R * .035)) ** 2)  # displaced wax ridge
    # fine ring + bead ring inside impression
    h += T * .1 * np.exp(-((rho - Ri * .935) / (R * .008)) ** 2)
    for i in range(40):
        a = i / 40 * np.pi * 2
        bx, by = cx + np.cos(a) * Ri * .85, cy + np.sin(a) * Ri * .85
        h += T * .16 * np.exp(-((xx - bx) ** 2 + (yy - by) ** 2) / (2 * (R * .011) ** 2))
    # monogram: L and V as vector glyphs, optically centred
    fpath = f"{FONTS}/cormorant-garamond/files/cormorant-garamond-latin-600-italic.woff"
    fs = int(R * .95)
    font = ImageFont.truetype(fpath, fs)
    canvas = Image.new("L", (N, N), 0)
    dr = ImageDraw.Draw(canvas)
    bl = font.getbbox("L"); bv = font.getbbox("V")
    wl, wv = bl[2] - bl[0], bv[2] - bv[0]
    overlap = fs * .16
    total = wl + wv - overlap
    x0 = cx - total / 2
    dr.text((x0 - bl[0], 0), "L", font=font, fill=255)
    dr.text((x0 + wl - overlap - bv[0], 0), "V", font=font, fill=255)
    m = np.asarray(canvas, np.float32) / 255
    ys, xs = np.nonzero(m > .5)
    bx0, bx1, by0, by1 = xs.min(), xs.max(), ys.min(), ys.max()
    com_x, com_y = (m * xx).sum() / m.sum(), (m * yy).sum() / m.sum()
    # optical centre: halfway between ink-box centre and centre of mass, nudged up slightly
    ox = .5 * ((bx0 + bx1) / 2) + .5 * com_x
    oy = .5 * ((by0 + by1) / 2) + .5 * com_y + R * .015
    m = ndi.shift(m, (cy - oy, cx - ox), order=1)
    letters = ndi.gaussian_filter(m, N * .0028)
    h += T * .42 * np.clip(letters * 1.25, 0, 1)
    # imperfections: low ripple, tiny bubbles
    h += T * .018 * norm(ndi.gaussian_filter(rng.standard_normal((N, N)), N * .025))
    h += T * .0025 * norm(ndi.gaussian_filter(rng.standard_normal((N, N)), N * .004))
    for _ in range(18):
        a, r0 = rng.random() * 6.28, R * (.78 + rng.random() * .22)
        px, py, pr = cx + np.cos(a) * r0, cy + np.sin(a) * r0, R * (.006 + rng.random() * .01)
        h -= T * .2 * np.exp(-((xx - px) ** 2 + (yy - py) ** 2) / (2 * pr ** 2))
    h *= inside
    # lighting
    gy, gx = np.gradient(h)
    n = np.dstack([-gx, -gy, np.ones_like(h)])
    n /= np.linalg.norm(n, axis=2, keepdims=True)
    L = np.array([-.5, -.62, .6]); L /= np.linalg.norm(L)
    V = np.array([0, 0, 1.0])
    Hh = (L + V); Hh /= np.linalg.norm(Hh)
    diff = np.clip(n @ L, 0, 1)
    nh = np.clip(n @ Hh, 0, 1)
    spec = .55 * nh ** 28 + .9 * nh ** 140
    ao = np.clip((ndi.gaussian_filter(h, N * .012) - h) / (T * .25), 0, 1)
    tone = norm(ndi.gaussian_filter(rng.standard_normal((N, N)), N * .03))
    gold = np.array([178, 140, 66]) / 255
    bronze = np.array([104, 74, 32]) / 255
    light_gold = np.array([226, 190, 118]) / 255
    mix = np.clip(.45 + .55 * diff[..., None] + .04 * tone[..., None], 0, 1)
    albedo = bronze * (1 - mix) + gold * mix
    albedo = albedo * (1 - .5 * ao[..., None])
    col = albedo * (.38 + .85 * diff[..., None]) + spec[..., None] * light_gold * 1.05
    fres = (1 - n[..., 2]) ** 2
    col += fres[..., None] * np.array([.22, .17, .08])
    alpha = smoothstep(-1.2, 1.2, d)
    rgba = np.dstack([np.clip(col, 0, 1), alpha])
    img = Image.fromarray((rgba * 255).astype(np.uint8), "RGBA").resize((S, S), Image.LANCZOS)
    img.save(f"{OUT}/wax-seal.png", optimize=True)
    img.save(f"{OUT}/wax-seal.webp", quality=92)
    img.resize((512, 512), Image.LANCZOS).save(f"{OUT}/wax-seal-512.webp", quality=90)


# ---------------------------------------------------------------- silk ribbon
def build_ribbon(W=200, H=2400):
    rng = np.random.default_rng(5)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    core = W * .74
    left = (W - core) / 2
    u = (xx - left) / core  # 0..1 across the ribbon
    # gentle twist: the highlight band wanders along the length
    wander = .18 * np.sin(yy / 260 + 1) + .08 * np.sin(yy / 97)
    band = np.exp(-((u - .38 - wander) / .13) ** 2)
    band2 = .5 * np.exp(-((u - .78 + wander * .6) / .08) ** 2)
    edge_dark = np.exp(-(u / .07) ** 2) + np.exp(-((1 - u) / .07) ** 2)
    folds = .06 * np.sin(yy / 41 + 3 * np.sin(yy / 300)) * np.sin(u * 3.1)
    weave = .025 * norm(rng.standard_normal((H, W))) + .03 * np.sin(yy * 2.1) * .5
    weave = ndi.gaussian_filter(weave, (0.3, 1.2))
    base = np.array([226, 178, 168]) / 255
    hi = np.array([250, 228, 222]) / 255
    lo = np.array([176, 120, 112]) / 255
    lum = .5 + .45 * band + .3 * band2 - .3 * edge_dark + folds + weave
    lum = np.clip(lum, 0, 1.2)[..., None]
    col = np.where(lum > .5, base + (hi - base) * (lum - .5) * 1.6, lo + (base - lo) * lum * 2)
    # frayed edges: core is opaque, outer threads stick out irregularly
    alpha = ((u >= 0) & (u <= 1)).astype(np.float32)
    fr = np.zeros((H, W), np.float32)
    img = Image.new("L", (W, H), 0); d = ImageDraw.Draw(img)
    for side in (0, 1):
        for _ in range(900):
            y = rng.random() * H
            ln = 3 + rng.random() ** 2 * (left * .95)
            x0 = left if side == 0 else left + core
            x1 = x0 - ln if side == 0 else x0 + ln
            d.line([(x0, y), (x1, y + (rng.random() - .5) * 6)], fill=int(90 + rng.random() * 140), width=1)
    fr = np.asarray(img, np.float32) / 255
    alpha = np.clip(alpha + fr * .8, 0, 1)
    edge_ragged = ndi.gaussian_filter(rng.standard_normal((H,)), 3)[:, None] * 2.5
    alpha *= smoothstep(-2, 1, np.minimum(xx - left + edge_ragged, left + core - xx - edge_ragged) + fr * 30)
    alpha = np.clip(alpha, 0, 1) * .97
    thread_col = np.array([240, 212, 205]) / 255
    col = np.where((fr[..., None] > 0) & ((u < 0) | (u > 1))[..., None], thread_col, col)
    rgba = np.dstack([np.clip(col, 0, 1), alpha])
    Image.fromarray((rgba * 255).astype(np.uint8), "RGBA").save(f"{OUT}/ribbon-silk.webp", quality=90)


if __name__ == "__main__":
    which = sys.argv[2] if len(sys.argv) > 2 else "all"
    if which in ("all", "paper"): build_paper()
    if which in ("all", "seal"): build_seal()
    if which in ("all", "ribbon"): build_ribbon()
    print("done")
