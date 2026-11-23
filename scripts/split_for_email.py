#!/usr/bin/env python3
"""Pack a delivery folder into numbered zips that each fit an email attachment limit.

  python3 split_for_email.py ./delivery --limit 18 --out ./mail

--limit is the RAW size in MB (Gmail caps the whole message at 25 MB after base64, which adds ~37%,
so 18 MB raw is a safe default). Files are packed largest-first (first-fit decreasing); a single file
larger than the limit is reported, never silently dropped. UTF-8 names (readable on Windows), no __MACOSX.
Verifies at the end that every file landed in exactly one zip.
"""
import argparse, pathlib, sys, zipfile


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("folder")
    ap.add_argument("--limit", type=float, default=18); ap.add_argument("--out", default="mail")
    ap.add_argument("--name", help="zip name prefix (default: folder name)")
    a = ap.parse_args()
    root = pathlib.Path(a.folder).resolve(); out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
    limit = a.limit * 1e6; prefix = a.name or root.name
    files = sorted((f for f in root.rglob("*") if f.is_file() and not f.name.startswith(".")),
                   key=lambda f: f.stat().st_size, reverse=True)
    too_big = [f for f in files if f.stat().st_size > limit]
    if too_big:
        print("✗ larger than the limit on its own (send another way):", *[f.relative_to(root) for f in too_big], sep="\n  ")
        files = [f for f in files if f not in too_big]
    bins = []
    for f in files:                                   # first-fit decreasing on raw size (zip only shrinks)
        s = f.stat().st_size
        for b in bins:
            if b[0] + s <= limit: b[0] += s; b[1].append(f); break
        else:
            bins.append([s, [f]])
    seen = {}
    for i, (_, group) in enumerate(bins, 1):
        z = out / f"{prefix}-{i}of{len(bins)}.zip"
        with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
            for f in sorted(group):
                arc = f"{root.name}/{f.relative_to(root).as_posix()}"; zf.write(f, arc); seen[arc] = seen.get(arc, 0) + 1
        mb = z.stat().st_size / 1e6
        print(f"{z.name}: {len(group)} files · {mb:.1f} MB · ≈{mb * 1.37:.1f} MB as email")
    expected = {f"{root.name}/{f.relative_to(root).as_posix()}" for f in files}
    missing = expected - set(seen); dup = [k for k, v in seen.items() if v > 1]
    print("all files packed ✓" if not missing and not dup else f"✗ missing {len(missing)}, duplicated {len(dup)}")
    sys.exit(1 if (missing or dup or too_big) else 0)


if __name__ == "__main__":
    main()
