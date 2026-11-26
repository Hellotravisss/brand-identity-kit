#!/usr/bin/env python3
"""Stack case-study boards into one long image for review or upload.

Usage: stitch_boards.py out.png board1.png board2.png ... [--width 1400]
"""
import argparse
from PIL import Image


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("out")
    ap.add_argument("boards", nargs="+")
    ap.add_argument("--width", type=int, default=1400)
    a = ap.parse_args()
    tiles = []
    for path in a.boards:
        im = Image.open(path).convert("RGB")
        tiles.append(im.resize((a.width, round(im.height * a.width / im.width)), Image.LANCZOS))
    long = Image.new("RGB", (a.width, sum(t.height for t in tiles)), "white")
    y = 0
    for t in tiles:
        long.paste(t, (0, y))
        y += t.height
    long.save(a.out)
    print(a.out, f"{long.width}x{long.height}", f"{len(tiles)} boards")


if __name__ == "__main__":
    main()
