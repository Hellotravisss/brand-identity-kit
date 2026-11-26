# Blind review — the acceptance gate for visual work

**Acceptance line: the work is good enough to publish on Behance as a portfolio piece.**
"All assets exist" and "usable" are not done. After **each complete version**, a second vision model scores it.
If the score is low, optimize and score again. The maker never grades their own work alone.

## When

After a whole version (full case-study long image or board set), not after single fragments.
It sits on top of your own check — open every image and compare it side by side with strong Behance
case studies first. It does not replace that, and the person you work for still has the final say.

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
3. **Blind prompt.** Send `docs/review-prompt.txt` unchanged, in a fresh conversation each time. Never say who
   made it, what the last score was, what changed, or what score you hope for.
4. **Two runs** with the same model and the same way of attaching files. If the model is unavailable (quota, error), switch to another vision model
   instead of waiting. Compare versions only between runs of the **same model and the same prompt**.
5. **Confirm the judge can see.** The first time you use a model or a new way of attaching images, ask it for
   details only visible in the picture (a row of color names, captions). A judge that only got text will
   still happily return scores.
6. **Save** the image, prompt, raw replies and a score table per version (`review/<date_version>/`).

## Pass line (default — the owner can change it)

- Mean total of two runs **≥ 8.0**, **and**
- no dimension with a mean **below 7**.

The seven dimensions fit a brand case study. For other visual work (store screenshots, posters, UI), swap
out the dimensions that cannot apply **before the first run**, then keep that prompt for every version.

## Handling the criticism

Check every claim against the image **and the source files**, then sort it:

| Kind | Action |
|---|---|
| Verified hard error (typo, wrong value, rules that contradict each other) | Fix now |
| Fair weakness | Fix; start with what both runs (or both models) raise |
| Conflicts with a locked decision (approved logo, client color, glyph structure) | Don't do it; record why |
| Built on something the judge misread | Discard |

## Rounds

At most **3 rounds**. If the mean does not rise by more than the noise between rounds, stop and bring the
owner the scores, what was tried and what is still weak. Report every run, never only the best one.
Never edit the prompt or the anchors to raise a score.

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
