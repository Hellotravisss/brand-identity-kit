# Deliverable checklist

## Acceptance — before calling any visual version done
- [ ] Defect hunt run on the final version (`defect-hunt-prompt.txt`); scores, if any, recorded for reference only
- [ ] Gate 1 (flat design sheets only) passed, or the owner chose to move on, before any mockups
- [ ] Every image opened and compared side by side with strong Behance case studies
- [ ] Gate 2: full case study, privacy-checked; two different models review it with the unchanged prompt to find shared problems
- [ ] Table shown to the owner: problem · proposed fix · what you will do
- [ ] Factual criticisms verified against image + source; hard errors fixed
- [ ] No verified hard errors left; remaining points diagnosed (structural vs taste/detail); at most 3 rounds per gate
- [ ] `STANDARD.md`: every required item present and zero verified defects (that is the pass, nothing else)
- [ ] Defect table saved with the version (report · verified or false alarm · action), plus raw replies

## Before starting
- [ ] Current website / app / social accounts audited (logo, colors, fonts in use)
- [ ] `dig` www + MX for every domain that will be printed
- [ ] Logo font license confirmed (OFL or purchased)
- [ ] Legal name, short name, English name, slogan, people's card data collected

## Logo package
- [ ] Master SVG (icon + wordmark) with outlines, overlaps merged
- [ ] Layouts: horizontal / vertical / icon / wordmark / slogan ×2 / bilingual / English wordmark (/ long name)
- [ ] Modes: full color / reverse / mono black / mono white (knockout)
- [ ] Formats: SVG, PNG (transparent), AI, PDF — RGB; AI, EPS (AI8), PDF — CMYK with specified values
- [ ] One-page usage guide (clear space, min size, colors, which version on which background)

## Manual (A / B / C)
- [ ] A: name meaning, positioning line vs slogan, logo meaning, scenario copy, wording rules
- [ ] B: standard logo, construction grid, clear space & min size, lockups, color modes, bilingual,
      misuse, long/short name, typography, color (+contrast table), auxiliary graphics
- [ ] C: digital, social avatars, web (icons, sub-brands, components, illustration), business card,
      letterhead & envelope, PPT, badge, merch, event
- [ ] Cover, TOC with computed page numbers, section dividers, back cover — vector PDF

## Print
- [ ] Text outlined, 0 fonts in PDF
- [ ] TrimBox = finished size, BleedBox ≥ 3 mm, art covers bleed
- [ ] Only specified CMYK values; small text single-black
- [ ] Safe zone measured, not eyeballed
- [ ] Printer notes (size, paper, colors, proof first)

## Templates
- [ ] PPT (.pptx) editable, previewed
- [ ] Letterhead (.docx), envelope
- [ ] Font files + install note + licenses

## Logo motion
- [ ] Storyboard approved before animating; each animation has a stated use
- [ ] Last frame diffed against the official lockup; frame 0 checked as a still
- [ ] Smoothness measured; every writing frame through `check_reveal.py`; flagged frames zoomed in
- [ ] Frames extracted from the encoded video looked at (also on a phone if the owner will watch there)

## Portfolio case study
- [ ] Publishable client facts confirmed **before** they go on a board or to an external model
- [ ] Public variant used for anything with contact details; client files unchanged (compare bytes)
- [ ] Specimens do not set the brand name in the uncustomized base font; stated rules match the applications
- [ ] Credits: AI use and required attribution; fictional names, phones, emails

## Handover
- [ ] "Read me first" index
- [ ] Split for email if needed, every file accounted for
- [ ] Open questions listed separately (not guessed into the files)
