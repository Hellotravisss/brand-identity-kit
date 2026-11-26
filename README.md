# brand-identity-kit

**From "the client picked a logo" to a full brand system — with an AI agent, by script, verified by machine.**

An agent skill (Claude Code / Codex compatible `SKILL.md`) plus a written method and small tools, extracted
from a real engagement: a Chinese tech brand went from an approved logo draft to

- a wordmark rebuilt on an open (SIL OFL) font so the logo is legally clean,
- 55 logo lockups × RGB/CMYK × AI/EPS/PDF/SVG/PNG,
- a 39-page brand manual (concept · basics · applications) compiled to vector PDF,
- print-ready business cards (PDF/X-1a, bleed, outlined text),
- PPT and Word letterhead templates, envelopes, badges, merch, event banners,
- favicon / share card / WeChat covers / avatars / email signatures / `tokens.css` / icon sprite.

No client material is included here — only the method and generic tools.

## What's inside

| Path | What |
|---|---|
| `SKILL.md` | The skill: when to use it and the 10-phase workflow |
| `docs/METHOD.md` | The playbook — why each phase works the way it does |
| `docs/PITFALLS.md` | Traps that each cost a round of rework (type, color, Illustrator, Office, headless Chrome) |
| `docs/CHECKLIST.md` | Deliverable checklist |
| `docs/REVIEW.md` + `docs/review-prompt*.txt` | The acceptance gate: Behance-portfolio quality; design gate then presentation gate, blind-reviewed by two vision models; scores only gate if calibration shows they can |
| `scripts/stitch_boards.py` | Stack case-study boards into one long image |
| `scripts/glyph_match.py` | Rebuild a wordmark on an OFL variable font, matching a draft's size, center and ink area |
| `scripts/brandcolor.py` | OKLCH tint ramp + WCAG contrast verdicts |
| `scripts/ai_export.jsx` | Illustrator batch export: RGB + brand-specified CMYK, AI/EPS(AI8)/PDF |
| `scripts/print_check.py` | Pre-flight a print PDF: trim/bleed boxes, CMYK values, RGB, fonts |
| `scripts/split_for_email.py` | Pack a delivery folder into zips that fit email limits, verify nothing is missing |

## Install as a skill

```bash
git clone https://github.com/Hellotravisss/brand-identity-kit ~/.claude/skills/brand-identity-kit
pip install fonttools skia-pathops pillow numpy pypdf python-pptx python-docx
```

## Quick examples

```bash
# Color: tints and contrast for a brand color
python3 scripts/brandcolor.py "#2F6BFF" --ink "#111827"

# Wordmark: rebuild a draft (path #3 in draft.svg) on Source Han Sans VF
python3 scripts/glyph_match.py --ref draft.svg --path-index 3 --text 品牌 \
    --font SourceHanSansSC-VF.otf --out wordmark.svg

# Print: pre-flight a business card
python3 scripts/print_check.py card.pdf --trim 90x54 --bleed 3

# Deliver: split for email
python3 scripts/split_for_email.py ./delivery --limit 18 --out ./mail
```

## The one habit that matters

Render it and look, or measure it — after every step. Most defects in the source project
(a font falling back to Times, a CMYK tint turning purple, a slogan running off a banner,
a bleed rounded down to 2.82 mm) were invisible until checked.

## License

MIT © Travis Zhang. Fonts referenced (Source Han Sans, Source Sans 3) are © Adobe under SIL OFL 1.1.
