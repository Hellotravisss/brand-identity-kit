---
name: brand-identity-kit
description: Build a complete brand identity system (VI / 品牌视觉识别 / 品牌手册) end to end — wordmark rebuilt on a licensable open font, logo lockups in every color mode (RGB + print CMYK), color and contrast rules, auxiliary graphics, business cards with bleed, Office templates (PPT / Word letterhead), digital and web assets, merch, and a compiled brand manual PDF. Use whenever someone asks for a logo package, brand manual / brand guidelines / VI 手册, business card print files, a 品牌全套 / 整套视觉, or to "make the rest of the brand" from an existing logo — even if they only mention one piece. Especially strong for Chinese / bilingual brands (CJK type, 国内印刷, WeChat assets).
---

# brand-identity-kit

A method plus small tools for producing a whole brand system with an agent, where **every file is generated
by script and verified by machine**. Read `docs/METHOD.md` before starting; it is the playbook.
`docs/PITFALLS.md` lists the traps that each cost a round of rework. `docs/CHECKLIST.md` is the deliverable list.

## Workflow (one line per phase — details in METHOD.md)

0. **Three checks first**: what the client's website/social already use; `dig` every domain/email you'll print;
   is the logo font licensable for logos (system fonts are not; OFL fonts are).
1. **Wordmark**: rebuild the approved draft on an OFL variable font by matching size, center and ink area
   (`scripts/glyph_match.py`) — borrow metrics, never outlines. Add one signature detail taken from the icon.
2. **Signature parameter**: measure one property of the icon (angle / ratio / radius) and reuse it across the
   system — only where it reads naturally.
3. **Lockup matrix**: layouts × {full color, reverse, mono black, mono white (knockout)}, generated from one
   master; export RGB + specified-CMYK with Illustrator (`scripts/ai_export.jsx`).
4. **Color**: never change a client-specified color; fix contrast with usage rules (`scripts/brandcolor.py`).
5. **Auxiliary graphics** derived from the icon: sequence, pattern, hatch, badge, line icons, animation.
6. **Print**: outlined text, art with 4 mm bleed, PDF/X-1a with 9 pt bleed, single-black small text;
   verify with `scripts/print_check.py`.
7. **Digital / web**: favicon set, share card, WeChat covers, avatars, email signature, `tokens.css`, icon sprite.
8. **Office**: `.pptx` (python-pptx) and Word letterhead (python-docx) + the OFL font files.
9. **Manual**: HTML pages → PNG (review) + vector PDF → compiled with computed TOC. Few words per page.
10. **Deliver**: folders by use + "read me first"; `scripts/split_for_email.py` for attachment limits.

## Rules

- Verify everything you generate: render and look, or measure. "Looks done" is not done.
- Never invent client facts (product descriptions, slogans, phone numbers). Leave blanks, list questions.
- Flag conflicts between client documents and earlier decisions instead of silently picking one.
- Show copy/emails to the person you work for before anything goes out.

## Requirements

Python 3.10+: `fonttools skia-pathops pillow numpy pypdf python-pptx python-docx`.
Headless Chrome for HTML → PNG/PDF. Adobe Illustrator for AI/EPS/CMYK (optional; SVG/PDF work without it).

**Cross-cutting**: at every stage, generate references with an image model (`scripts/gemini_image.py`), then redraw as vectors in Illustrator. Never ship raw AI output; proof every word of text in it. See METHOD.md.
