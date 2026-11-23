# Pitfalls — each one cost a round of rework

## Type & outlines
- **Variable fonts keep overlapping contours.** Rasterizing with even-odd fill punches holes and
  underestimates ink → you pick a weight that is too heavy. Rasterize with non-zero winding.
  Merge overlaps (`pathops.Path.simplify`) before delivering outlines.
- **Static vs variable advance widths.** A variable font's `hmtx` holds the default (often lightest)
  master's widths — Latin text set with them collides. Use static weights for typesetting, or the
  interpolated `glyph.width` from a located glyph set.
- **Size Latin by cap height** (`OS/2.sCapHeight`), not ink bounds — Q/J descenders shrink everything.
- **Space characters by visible gap**, not em boxes, in a wordmark. Measure gaps from the *final* master,
  not from the reference draft (they differ).
- fontTools `SVGPathPen` emits `H`/`V` commands — don't parse its output as x,y pairs.
- Font names starting with a digit token (`Source Sans 3`) **must be quoted** in CSS/SVG `font-family`;
  unquoted, the whole declaration is dropped and you get Times. Inside a Python f-string attribute, use `&apos;`.
- Local installs may register a different family name (`SourceSans3VF`) — include both in the stack.

## Color
- Bright brand blues fail WCAG for small white text (~3.9:1). Don't change the client's color; restrict usage.
- "10% of the CMYK" ≠ 10% tint visually; convert the screen tint through an ICC profile and compare candidates.
- Keynote/CMYK previews look duller than sRGB — that's expected, not a file bug; tell the client to proof.
- Small type in 4-color black misregisters — use K100 / K65.

## Illustrator automation (ExtendScript via `osascript`)
- AppleScript default timeout is 2 min: wrap in `with timeout of 900 seconds`.
- Set `app.userInteractionLevel = DONTDISPLAYALERTS` or a dialog will hang the batch.
- Recolor for CMYK: record each path's RGB first, run `doc-color-cmyk`, then assign specified CMYK.
- PDF bleed offsets round to whole points (8.5 pt → 8 pt). Use 9 pt and paint ≥ 4 mm of art.
- EPS with AI10+ compatibility embeds private data (~0.8 MB/file); AI8 compatibility is small.
- Beta builds have a different bundle id (`com.adobe.illustratorBeta`).

## Office
- Word is sandboxed: the first scripted save to a new folder pops a permission dialog → script hangs.
  Verify `.docx` by rendering through Pages instead.
- PPT/Word won't carry fonts — ship OFL font files with the templates.
- No bleed elements on letterhead; office printers leave a white margin.

## Headless Chrome rendering
- Headless screenshots don't advance CSS animations (`--virtual-time-budget` doesn't help) — verify
  animations in a real browser (`getAnimations()`, measure `getBoundingClientRect()` over time).
- `<path ... fill-opacity=.45/>` unquoted in HTML swallows the slash → the next element nests inside and vanishes.
- Large screenshots occasionally exit with code 2 — retry.
- Python 3.10 f-strings can't contain backslashes — build the substring first.

## Design judgment
- Small shapes in a pattern lose identity (a short door reads as ▶).
- A signature angle applied at full width becomes huge; apply it to corners and edges.
- Don't let the logo's signature detail spread to every character — keep it on the brand name.
- Never invent facts in deliverables (a product description you guessed; a combined slogan the client never wrote).
  Leave blanks and ask.
- When a client document conflicts with an earlier decision (e.g. two slogan variants), flag it; don't silently pick.

## Verifying PDFs with pypdf
- Illustrator / merged PDFs put artwork in nested **Form XObjects**; reading only the page stream finds
  no colors and a checker silently passes. Recurse into `/XObject` resources.
- `page.get_contents()` returns a `ContentStream` that can be **falsy** — test `is not None`, not truthiness.
- A checker that finds *nothing* must fail, not pass.

## Variable fonts
- When outlining text from a variable font, take each glyph's advance from the instanced glyph set (`glyphSet[g].width`), not from `hmtx`. `hmtx` holds the default master's widths, so text set at another weight comes out too loose or too tight.

## CJK wordmarks
- Customize stroke *endings* (cuts, angles), never stroke *structure*. Removing a stroke or swapping a component for a graphic turns the glyph into a misspelling that native readers spot instantly. Put brand graphics next to the characters instead.
- Print rich black as C60 M40 Y40 K100 (240%). A straight ICC conversion of near-black lands around 350% total ink, which is over most printers' 300% limit.

## Delivery
- Gmail caps a message at 25 MB *after* base64 (+~37%). Keep raw attachments ≤ ~18 MB.
- macOS `ditto` zips add `__MACOSX` junk; Python `zipfile` writes UTF-8 names that Windows reads correctly.
- Print `www.` only if it resolves.
