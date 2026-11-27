# Review with vision models — find defects, not verdicts

**Acceptance line: the work is good enough to publish on Behance as a portfolio piece.**
"All assets exist" and "usable" are not done. Whether a version passes is decided by [`STANDARD.md`](STANDARD.md).
Models are used for two things, and neither of them is the verdict:

| Pass | Prompt | Output used for |
|---|---|---|
| **Defect hunt** (needed for `STANDARD.md` part B) | `docs/defect-hunt-prompt.txt` — no scores, no taste | A list of suspects to verify |
| **Blind critique** (while the design is still moving) | the two gate prompts below | Shared problems and proposed fixes; scores are recorded for reference only |

The maker never grades their own work alone.

## Running a defect hunt

1. Run your own pass with the `STANDARD.md` B list first, zooming in on every image.
2. Send boards with zoom tiles and copy sheet, mockups a few per call, to two models. Split into batches
   so one call does not time out. For motion, also run `scripts/check_reveal.py`; a video model may sample
   only 1 frame per second.
3. Treat every report as a suspect. Confirm it on the pixels **and** the source before changing anything.
   Settle geometry and color claims with numbers (tangent angle at a joint, the fill value in the file, the
   lightness of a pixel), not with another look at a downscaled image.
4. Keep a table per version: *report · verified or false alarm (how you know) · what you did*. False alarms
   are worth writing down so nobody "fixes" them later.
5. After fixing, open every changed page again. Say plainly which fixes did not go back to a model.

## Two gates: design first, presentation second

Mockups and photographs lift the overall impression and can hide a weak system. Judge them separately.

| Gate | What the judge sees | Prompt |
|---|---|---|
| **1 · Design** | Flat design sheets only: mark, graphic system, several layout skeletons, type, color. No photos, no mockups | `docs/review-prompt-design.txt` |
| **2 · Presentation** | The full case study: boards plus applications and mockups | `docs/review-prompt.txt` |

Do not start mockups while the design sheets still have verified defects (`STANDARD.md`, part B). The review
sits on top of your own check. Pass or fail is decided by `STANDARD.md`.

## Calibrate before you read anything into a score

A score means nothing until you know what the judge gives to work that is already good.

1. Pick 3 projects from a curated or featured gallery and 1 ordinary one, same category.
2. Capture only the project images. **Crop out everything that reveals status**: platform chrome, feature
   ribbons, like and view counts, author names. Attach them the same way you attach your own work.
3. Score all four with every judge model, same prompt, blind.
4. If the featured work does not score clearly above the ordinary one (gap larger than the run-to-run
   noise), the score tells you nothing about quality with that judge: use it only to find problems. In
   neither case does a score decide pass or fail; `STANDARD.md` does.
5. Use the captures only for this internal check; do not publish or commit them. Record URLs and scores.
   Recalibrate when the prompt, the model or the way of attaching files changes.

## Steps

1. **Give the judge enough pixels.** Find out what your tool really delivers: one agent CLI shrank a
   2800×1960 board to 1223×856, and a stitched long page shrinks far more. Prefer every board separately,
   plus near-full-size zoom tiles for anything over ~1.6 MP, plus the **copy sheet** (the `<text>` strings
   from the source SVG, or the copy doc) so typos and values are checked against text, not guessed from
   pixels. A stitched long image (`python3 scripts/stitch_boards.py long.png board1.png …`) is the fallback
   for a judge that takes only one image.
2. **Privacy check.** Open what you are about to send. Unless the owner has decided otherwise, send only
   finished boards with fictional sample people: no real names, phones, faces or client documents, and ask
   before sending a project that is not cleared to be public. Never send credentials or whole project folders.
3. **Blind prompt.** Send the gate's prompt unchanged, in a fresh conversation each time. Never say who
   made it, what the last score was, what changed, or what score you hope for.
4. **Who judges, how many times.** Two different models disagree in more useful ways than one model twice.

   | Situation | Runs |
   |---|---|
   | Every version | one run from each of two models |
   | One model unavailable (quota, error) | two runs of the other; do not wait |

   Compare versions only between runs of the **same model, prompt and way of attaching files**. With a
   single run per model, a change of about 0.5 or less is not progress.
5. **Confirm the judge can see.** The first time you use a model or a new way of attaching images, ask it for
   details only visible in the picture (a row of color names, captions). A judge that only got text will
   still happily return scores.
6. **Save** the images, prompt, raw replies and a score table per version (`review/<date_version>/`).

## What decides pass or fail

**Pass or fail comes from [`STANDARD.md`](STANDARD.md)**: all required items present and zero verified
defects. It does not come from a model score (the first calibration showed scores cannot gate) and it does
not depend on anyone's taste. Record scores for reference; use the reviews to find defects and shared problems.

The seven score dimensions fit a brand case study. For other visual work (store screenshots, posters, UI),
swap out the dimensions that cannot apply **before the first run**, then keep that prompt for every version.

## Handling the criticism

The prompts ask for a fix with every problem. **Show the owner the fixes, not only the complaints**, every
round, as a table: *problem · fix the judge proposed · what you will do* (do it / don't, with the reason /
owner decides).

Check every factual claim against the image **and the source files**, then sort it:

| Kind | Action |
|---|---|
| Verified hard error (typo, wrong value, rules that contradict each other) | Fix now |
| Fair weakness | Fix; start with what both models raise |
| Conflicts with a locked decision (approved logo, client color, glyph structure) | Don't do it; record why |
| Built on something the judge misread | Discard |

A proposed fix is advice from a judge that has not drawn it. Test it; it is not guaranteed to raise anything.

## Rounds and stopping

At most **3 rounds per gate**. Judge progress by the problems, not by score changes. When the last round left
no verified hard error to fix, **stop polishing and diagnose** what remains:

- **Structural** (for example the graphic system does not belong to the mark): propose a change of direction
  to the owner; start a new round only after they agree.
- **Only matters of taste left and `STANDARD.md` passes:** ship; list the open points.

Report every run, never only the best one. Never edit a prompt or its anchors to raise a score.

## How much to trust the number (first calibration, one project, small sample)

A four-board brand sheet without any application mockups, scored with the prompt here:

| Run | Total |
|---|---|
| Model A, run 1 | 5.2 |
| Model A, run 2 (same image) | 5.7 |
| Model B | 5.0 |
| Model A, same content with the layout deliberately broken | 4.9 |

- All three honest runs agreed on the biggest gap (no applications: 1–2 of 10). **The ranked problems were
  more useful than the total.**
- The same image moved 0.5 in total and up to 1 point per dimension. **Treat smaller differences as noise.**
- Breaking the layout badly cost only 0.3–0.8 in total, but the layout dimension fell from 6–6.5 to 5.
  **The total is insensitive — read the dimensions.**
- On that broken version the judge **misread the cover headline and built one of its top three problems on a
  word that was not there**. In a sight test it also got one digit of a hex value wrong.
- One model caught a real contradiction (a color rule on one board broken on another) that the other model and
  the maker had both missed. It also proposed redrawing an approved logo, which was rejected.

**After switching to separate boards + zoom tiles:** the two misread items (the headline and the hex digit)
were read correctly in a sight test **without** the copy sheet. A full review with tiles and copy sheet gave
more specific craft findings, including a palette color that was listed but never used on the other boards
(verified in the source files). One retest each, so treat this as a direction, not a measurement.
Scores from different input methods are not comparable.

## Second calibration: the judges did not separate featured from ordinary work

Same presentation prompt, project images only, one run per judge per project.

| Work | Judge A | Judge B |
|---|---|---|
| Curated gallery project 1 | 5.7 | 7.3 |
| Curated gallery project 2 | 5.7 | 5.3 |
| Curated gallery project 3 | 5.4 | 5.1 |
| Ordinary project | 6.0 | 4.9 |
| Our own case study, after two rounds of revising to these judges | 6.3 | 6.0 |

- Judge A put the ordinary project above all three curated ones. Judge B clearly separated only one of the three.
- **No curated project reached a total of 8.** An uncalibrated "8.0 to pass" had been used before this; nothing
  had ever shown it was reachable.
- Our own higher score is not evidence that it is better: it had been revised against these judges' notes.
  A guess, not tested: the rubric favors manual-style cases with rule boards over art-direction-led ones.
- **They were good at hard errors.** Both judges independently found a broken printed slogan in one curated
  project and a malformed email address in another; both were confirmed on the images.

Four projects and one run each is a small sample. The design-gate prompt has not been calibrated.
