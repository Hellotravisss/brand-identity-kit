#!/usr/bin/env python3
"""Brand color helper: perceptually even tints (OKLCH) and WCAG contrast.

  python3 brandcolor.py "#2F6BFF"                       # tint ramp + contrast vs white/black
  python3 brandcolor.py "#2F6BFF" --ink "#111827"       # also contrast against an ink color
  python3 brandcolor.py "#2F6BFF" --tints 100,60,20,10

Tints keep hue fixed and interpolate OKLCH lightness toward white; chroma shrinks with the tint.
"""
import argparse, math


def _lin(c): return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
def _gam(c): return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def hex2rgb(h): return [int(h.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4)]


def hex2oklch(h):
    r, g, b = (_lin(v) for v in hex2rgb(h))
    l = (0.4122214708*r + 0.5363325363*g + 0.0514459929*b) ** (1/3)
    m = (0.2119034982*r + 0.6806995451*g + 0.1073969566*b) ** (1/3)
    s = (0.0883024619*r + 0.2817188376*g + 0.6299787005*b) ** (1/3)
    L = 0.2104542553*l + 0.7936177850*m - 0.0040720468*s
    a = 1.9779984951*l - 2.4285922050*m + 0.4505937099*s
    bb = 0.0259040371*l + 0.7827717662*m - 0.8086757660*s
    return L, math.hypot(a, bb), math.atan2(bb, a)


def oklch2hex(L, C, H):
    a, b = C * math.cos(H), C * math.sin(H)
    l = (L + 0.3963377774*a + 0.2158037573*b) ** 3
    m = (L - 0.1055613458*a - 0.0638541728*b) ** 3
    s = (L - 0.0894841775*a - 1.2914855480*b) ** 3
    rgb = (4.0767416621*l - 3.3077115913*m + 0.2309699292*s,
           -1.2684380046*l + 2.6097574011*m - 0.3413193965*s,
           -0.0041960863*l - 0.7034186147*m + 1.7076147010*s)
    return "#%02X%02X%02X" % tuple(round(_gam(min(max(v, 0), 1)) * 255) for v in rgb)


def tint(brand, p):
    """p% of the brand color (100 = brand, 0 = white)."""
    if p >= 100: return brand.upper()
    L0, C0, H0 = hex2oklch(brand); t = p / 100
    return oklch2hex(L0 + (1 - L0) * (1 - t), C0 * t, H0)


def contrast(a, b):
    lum = lambda h: sum(w * _lin(v) for w, v in zip((0.2126, 0.7152, 0.0722), hex2rgb(h)))
    x, y = sorted((lum(a), lum(b)), reverse=True)
    return (x + 0.05) / (y + 0.05)


def verdict(r):
    return "AA body ✓" if r >= 4.5 else ("large text only (≥18.7px bold / 24px)" if r >= 3 else "✗ fails")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("brand"); ap.add_argument("--ink"); ap.add_argument("--tints", default="100,80,60,40,20,10,5")
    a = ap.parse_args()
    print("Tints (OKLCH):")
    for p in map(int, a.tints.split(",")):
        print(f"  {p:3d}%  {tint(a.brand, p)}")
    print("Contrast:")
    pairs = [("#FFFFFF", a.brand, "white on brand"), (a.brand, "#FFFFFF", "brand on white")]
    if a.ink:
        pairs += [(a.ink, "#FFFFFF", "ink on white"), ("#FFFFFF", a.ink, "white on ink"), (a.brand, a.ink, "brand on ink")]
    for f, b, n in pairs:
        r = contrast(f, b); print(f"  {r:5.2f}:1  {verdict(r):38s} {n}")
