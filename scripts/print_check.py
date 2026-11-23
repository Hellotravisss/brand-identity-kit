#!/usr/bin/env python3
"""Pre-flight a print PDF: page boxes in mm, CMYK values used, any RGB, embedded fonts.

  pip install pypdf
  python3 print_check.py card.pdf [--trim 90x54] [--bleed 3]

Reads the page content AND every nested Form XObject (Illustrator and merged PDFs put the artwork there —
checking only the top-level stream silently finds nothing). Exits 1 if: RGB fill/stroke operators are
present, fonts are embedded (text not outlined), no color operators were found at all, TrimBox differs
from --trim, or bleed is smaller than --bleed.
"""
import argparse, re, sys
from pypdf import PdfReader
from pypdf.generic import IndirectObject

MM = 72 / 25.4


def size(b): return (float(b[2]) - float(b[0])) / MM, (float(b[3]) - float(b[1])) / MM


def walk(resources, streams, fonts, seen):
    """Collect Form XObject streams and font names recursively."""
    if not resources: return
    res = resources.get_object()
    if "/Font" in res:
        fonts.update(res["/Font"].get_object().keys())
    xo = res.get("/XObject")
    if not xo: return
    for _, ref in xo.get_object().items():
        key = ref.idnum if isinstance(ref, IndirectObject) else id(ref)
        if key in seen: continue
        seen.add(key)
        obj = ref.get_object()
        if obj.get("/Subtype") == "/Form":
            streams.append(obj.get_data().decode("latin1", "ignore"))
            walk(obj.get("/Resources"), streams, fonts, seen)


def check(path, trim=None, bleed=None):
    r = PdfReader(path); ok = True
    for n, pg in enumerate(r.pages, 1):
        tw, th = size(pg.trimbox); bw, bh = size(pg.bleedbox)
        streams, fonts = [], set()
        c = pg.get_contents()
        if c is not None: streams.append(c.get_data().decode("latin1", "ignore"))   # ContentStream can be falsy
        walk(pg.get("/Resources"), streams, fonts, set())
        data = "\n".join(streams)
        cmyk = sorted({" ".join(m[0].split()) for m in re.findall(r'((?:[\d.]+\s+){4})(k|K)\b', data)})
        rgb = len(re.findall(r'(?:[\d.]+\s+){3}(?:rg|RG)\b', data))
        other = len(re.findall(r'\b(?:scn?|SCN?)\b', data))      # colors set via color spaces
        print(f"page {n}: trim {tw:.2f}×{th:.2f} mm · bleed box {bw:.2f}×{bh:.2f} mm "
              f"(≈{(bw - tw) / 2:.2f} mm/side) · CMYK {cmyk} · RGB ops {rgb} · cs/scn ops {other} · fonts {len(fonts)}")
        if rgb: ok = False; print("  ✗ RGB color present")
        if fonts: ok = False; print("  ✗ fonts embedded — outline text for print")
        if not cmyk and not rgb and not other: ok = False; print("  ✗ no color operators found — check the file manually")
        if other and not cmyk: print("  ! colors set via color spaces (scn) — confirm they are DeviceCMYK / spot")
        if trim:
            w, h = map(float, trim.lower().split("x"))
            if abs(tw - w) > 0.05 or abs(th - h) > 0.05: ok = False; print(f"  ✗ trim ≠ {trim}")
        if bleed is not None and (bw - tw) / 2 < bleed - 0.01: ok = False; print(f"  ✗ bleed < {bleed} mm")
    print("PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("pdf", nargs="+")
    ap.add_argument("--trim"); ap.add_argument("--bleed", type=float)
    a = ap.parse_args()
    results = [check(p, a.trim, a.bleed) for p in a.pdf]
    sys.exit(0 if all(results) else 1)
