#!/usr/bin/env python3
"""Rebuild a wordmark on an OFL variable font, matching a reference draft by metrics only.

The reference (e.g. a draft set in a font you can't license) gives: each character's height, its center,
and its ink area. The output uses the variable font's own outlines — never the reference's.

  pip install fonttools skia-pathops pillow numpy
  python3 glyph_match.py --ref draft.svg --path-index 3 --text 品牌 \
      --font SourceHanSansSC-VF.otf --out wordmark.svg

--path-index   which <path> in the reference SVG is the wordmark (0-based)
--weight       skip the search and force a weight
Prints the solved weight and per-character ink ratio (target 1.00 ± 0.03).
"""
import argparse, re
import numpy as np
from PIL import Image, ImageDraw
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
import pathops


# ---------- SVG path → polygons (absolute M/L/H/V/Q/C/Z) ----------
def polys_from_d(d):
    toks = re.findall(r'[MLHVQCZ]|-?\d*\.?\d+(?:e-?\d+)?', d)
    out, cur, i, cmd, last = [], [], 0, None, (0, 0)
    def n():
        nonlocal i; v = float(toks[i]); i += 1; return v
    while i < len(toks):
        t = toks[i]
        if t in "MLHVQCZ":
            cmd = t; i += 1
            if cmd == "Z":
                if cur: out.append(cur); cur = []
                continue
        if cmd == "M":
            if cur: out.append(cur)
            last = (n(), n()); cur = [last]; cmd = "L"
        elif cmd == "L": last = (n(), n()); cur.append(last)
        elif cmd == "H": last = (n(), last[1]); cur.append(last)
        elif cmd == "V": last = (last[0], n()); cur.append(last)
        elif cmd == "Q":
            p1, p2 = (n(), n()), (n(), n())
            for k in range(1, 13):
                u = k / 12; cur.append(((1-u)**2*last[0]+2*(1-u)*u*p1[0]+u*u*p2[0], (1-u)**2*last[1]+2*(1-u)*u*p1[1]+u*u*p2[1]))
            last = p2
        elif cmd == "C":
            p1, p2, p3 = (n(), n()), (n(), n()), (n(), n())
            for k in range(1, 17):
                u = k / 16; v = 1 - u
                cur.append((v**3*last[0]+3*v*v*u*p1[0]+3*v*u*u*p2[0]+u**3*p3[0], v**3*last[1]+3*v*v*u*p1[1]+3*v*u*u*p2[1]+u**3*p3[1]))
            last = p3
    if cur: out.append(cur)
    return out


def bbox(polys):
    xs = [x for p in polys for x, _ in p]; ys = [y for p in polys for _, y in p]
    return min(xs), min(ys), max(xs), max(ys)


def area(p): return sum(p[i][0]*p[(i+1) % len(p)][1] - p[(i+1) % len(p)][0]*p[i][1] for i in range(len(p))) / 2


def ink(polys, box, scale=8):
    """Non-zero winding raster — variable fonts keep overlaps; even-odd would punch holes."""
    x0, y0, x1, y1 = box; W, H = int((x1-x0)*scale)+1, int((y1-y0)*scale)+1
    wind = np.zeros((H, W), np.int16)
    for p in polys:
        if len(p) < 3: continue
        m = Image.new("L", (W, H), 0)
        ImageDraw.Draw(m).polygon([((x-x0)*scale, (y-y0)*scale) for x, y in p], fill=1)
        wind += np.asarray(m, np.int16) * (1 if area(p) > 0 else -1)
    return int((wind != 0).sum())


def split_chars(polys, n):
    """Group subpaths into n characters by horizontal overlap, then merge nearest groups."""
    groups = []
    for p in sorted(polys, key=lambda q: bbox([q])[0]):
        b = bbox([p])
        if groups and b[0] < groups[-1]["x1"]:
            groups[-1]["p"].append(p); groups[-1]["x1"] = max(groups[-1]["x1"], b[2])
        else:
            groups.append({"p": [p], "x0": b[0], "x1": b[2]})
    while len(groups) > n:
        gaps = [groups[k+1]["x0"] - groups[k]["x1"] for k in range(len(groups)-1)]
        k = gaps.index(min(gaps))
        groups[k]["p"] += groups[k+1]["p"]; groups[k]["x1"] = groups[k+1]["x1"]; del groups[k+1]
    if len(groups) != n:
        raise SystemExit(f"found {len(groups)} character groups, expected {n}")
    return [g["p"] for g in groups]


# ---------- font side ----------
class VF:
    def __init__(self, path):
        self.f = TTFont(path); self.cmap = self.f.getBestCmap()

    def ops(self, ch, wght):
        gs = self.f.getGlyphSet(location={"wght": wght})
        p = pathops.Path(); gs[self.cmap[ord(ch)]].draw(p.getPen()); p.simplify(fix_winding=True)
        pen = RecordingPen(); p.draw(pen); return pen.value


def ops_bbox(ops):
    pts = [q for _, ps in ops for q in ps]
    return min(x for x, _ in pts), min(y for _, y in pts), max(x for x, _ in pts), max(y for _, y in pts)


def fit(ops, box):
    """Scale glyph (font units, y up) to the box height and center it on the box center."""
    fb = ops_bbox(ops); s = (box[3]-box[1]) / (fb[3]-fb[1])
    cx, cy = (box[0]+box[2])/2, (box[1]+box[3])/2
    tx, ty = cx - s*(fb[0]+fb[2])/2, cy + s*(fb[1]+fb[3])/2
    return [(o, [(s*x+tx, -s*y+ty) for x, y in ps]) for o, ps in ops]


def to_d(ops):
    f = lambda v: f"{v:.3f}"; s = []
    for o, ps in ops:
        if o == "moveTo": s.append(f"M{f(ps[0][0])},{f(ps[0][1])}")
        elif o == "lineTo": s.append(f"L{f(ps[0][0])},{f(ps[0][1])}")
        elif o == "curveTo": s.append("C" + " ".join(f"{f(x)},{f(y)}" for x, y in ps))
        elif o == "qCurveTo": s.append("Q" + " ".join(f"{f(x)},{f(y)}" for x, y in ps))
        elif o in ("closePath", "endPath"): s.append("Z")
    return " ".join(s)


def ratio(vf, ch, w, ref):
    box = bbox(ref); mine = polys_from_d(to_d(fit(vf.ops(ch, w), box)))
    b = bbox(mine); u = (min(b[0], box[0])-1, min(b[1], box[1])-1, max(b[2], box[2])+1, max(b[3], box[3])+1)
    return ink(mine, u) / ink(ref, u)


def solve(vf, ch, ref, lo, hi):
    for _ in range(12):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if ratio(vf, ch, mid, ref) < 1 else (lo, mid)
    return (lo + hi) / 2


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", required=True); ap.add_argument("--path-index", type=int, required=True)
    ap.add_argument("--text", required=True); ap.add_argument("--font", required=True)
    ap.add_argument("--out", required=True); ap.add_argument("--weight", type=float)
    ap.add_argument("--color", default="#111827")
    a = ap.parse_args()
    svg = open(a.ref, encoding="utf-8").read()
    d = re.findall(r'\sd="([^"]*)"', svg)[a.path_index]
    refs = split_chars(polys_from_d(d), len(a.text))
    vf = VF(a.font)
    axis = next(x for x in vf.f["fvar"].axes if x.axisTag == "wght")
    if a.weight:
        W = a.weight
    else:
        ws = [solve(vf, ch, r, axis.minValue, axis.maxValue) for ch, r in zip(a.text, refs)]
        W = round(sum(ws) / len(ws)); print("per-character weights", [round(w) for w in ws], "→ using", W)
    for ch, r in zip(a.text, refs):
        print(f"  {ch}: ink ratio {ratio(vf, ch, W, r):.3f}")
    path = " ".join(to_d(fit(vf.ops(ch, W), bbox(r))) for ch, r in zip(a.text, refs))
    vb = re.search(r'viewBox="([^"]*)"', svg).group(1)
    open(a.out, "w", encoding="utf-8").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}"><path fill="{a.color}" d="{path}"/></svg>\n')
    print("written", a.out)
