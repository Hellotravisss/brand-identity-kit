#!/usr/bin/env python3
"""Check a write-on logo animation frame by frame.

In a clean write-on, the only edge that does not lie on the final artwork's outline is the pen tip.
A second such edge, or one much longer than the stroke is wide, means something leaked early
(the root of another stroke) or a mask was cut across the shape.

Usage: check_reveal.py video.mp4 --start 10 --end 165 [--allow allow.png]
  --start/--end  frame range while the mark is being written
  --allow        black/white image; white marks edges you drew on purpose (a stroke's own edge at a crossing)
A flagged frame is a place to zoom in, not automatically a defect. Needs ffmpeg, numpy, scipy, Pillow.
"""
import argparse, subprocess, tempfile
from pathlib import Path
import numpy as np
from PIL import Image
from scipy.ndimage import binary_dilation, distance_transform_edt, label


def tip_edges(shown, shape, allow=None):
    """Connected edges between what is shown and what is still hidden: [(length_px, (x, y)), ...]."""
    edge = shown & binary_dilation(shape & ~shown)
    if allow is not None:
        edge &= ~allow
    lab, n = label(edge, structure=np.ones((3, 3)))
    out = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(ys) >= 6:
            out.append((float(np.hypot(np.ptp(ys), np.ptp(xs))), (int(xs.mean()), int(ys.mean()))))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('video'); ap.add_argument('--start', type=int, default=0); ap.add_argument('--end', type=int, required=True)
    ap.add_argument('--allow'); a = ap.parse_args()
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(['ffmpeg', '-v', 'error', '-i', a.video, f'{d}/%05d.png'], check=True)
        files = sorted(Path(d).glob('*.png'))
        load = lambda f: np.asarray(Image.open(f).convert('RGB')).astype(int)
        last = load(files[-1]); bg = last[2, 2]
        ink = lambda im, ref: np.abs(im - bg).max(2) > ref
        half = np.abs(last - bg).max(2); thr = np.percentile(half[half > 30], 75) / 2
        shape = ink(last, thr)
        width = 2 * distance_transform_edt(shape).max()
        allow = np.asarray(Image.open(a.allow).convert('L')) > 127 if a.allow else None
        bad = 0
        for i in range(a.start, min(a.end, len(files))):
            segs = tip_edges(ink(load(files[i]), thr) & shape, shape, allow)
            if len(segs) > 1 or any(s > width * 1.15 for s, _ in segs):
                bad += 1; print(f'frame {i}: ' + ', '.join(f'{s:.0f}px at {p}' for s, p in segs))
        print(f'checked {max(0, min(a.end, len(files)) - a.start)} frames, flagged {bad} (widest stroke about {width:.0f}px)')


if __name__ == '__main__':
    main()
