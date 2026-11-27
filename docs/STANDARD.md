# Release standard — pass or fail without anyone's taste

A version **passes** when every item in A is present **and** B has zero verified defects. Nobody votes.
Passing means *complete and clean enough to publish*. It does **not** mean the design is at featured level
(see C).

## A · Required (all of them)

| # | Item | Check |
|---|---|---|
| 1 | **Story** | The images answer: who is the brand, what does it do, why do the graphics look like this. A slogan alone fails |
| 2 | **Logo** | Main lockup, other lockups and one-color version, clear space, minimum size |
| 3 | **Business card** | Front and back, shown as an object |
| 4 | **Graphic system / pattern** | Elements that grow out of the mark or the brand; the same element appears in **5 or more** application images (count them) |
| 5 | **Motion** | At least one video or GIF built from the brand's own elements |
| 6 | **In-situ outdoor or spatial application** | Poster in place, signage, vehicle, storefront or wall |
| 7 | **Volume** | 15 or more images and videos |

Items 1–4 are house rules (a delivery floor). Items 5–7 are also supported by data (below). Color and type
spec pages belong in the client delivery but are **not** a mark of featured work, so they are not pass items.

## B · Zero verified defects (any one fails)

- Typos, broken sentences, malformed email / phone / URL
- Placeholder content
- The same image used twice
- Text that is unreadable at display size, clipped, or fighting the picture underneath
- Generated-image artifacts (gibberish lettering, warped objects)
- A stated rule that the applications contradict
- Fonts that did not load; the mark redrawn or recolored
- Visible kinks or joins in curves and letterforms — **in any single frame of motion too**, transients
  included (viewers pause); frame 0 is judged as a still
- Graphics chopped into fragments by a plate, edge or fixing
- Contact details, addresses or client facts shown without being cleared for publication

How: your own pass with this list, then ask two vision models to hunt **only for these**
(`defect-hunt-prompt.txt`), then zoom in and confirm each one in the image and the source. For a write-on
animation also run `scripts/check_reveal.py` over every writing frame. Only confirmed defects count.
The last item is not something a model can settle: ask the client or the owner.

## C · Design quality — no validated test yet

Do not claim a quality verdict. What failed so far: absolute model scores did not separate curated from
ordinary work, and two coders could not agree on what counts as a "graphic system" or "consistent art
direction". Candidate to calibrate before use: **logo-off recognition** — hide the mark on your application
images, mix them with other brands, and ask a model that has never seen the brand to group them.

## Where 5–7 come from

20 projects from a curated branding gallery (taken in page order) and 14 recent uncurated "brand identity"
search results with 8+ items. Every third project in each group was held out. One coder knew the groups; a
second, a vision model, coded the same thumbnail sheets blind (shuffled). Motion was counted from the page.

| Trait (derivation set: 14 curated, 10 ordinary) | Curated | Ordinary | Coder agreement (kappa) |
|---|---|---|---|
| Motion (counted from the page) | 71% | 0% | not coded by eye |
| In-situ outdoor / spatial | 79% | 40% | 0.81 |
| Digital touchpoints | 86% | 70% | 0.74 |
| 15+ images and videos | 11/14 | 3/10 | counted |
| Color spec page | 36% | 90% | 0.35 |
| Written story | 43% | 70% | 0.82 |
| Business card | 36% | 50% | 0.47 |

Rule fixed on the derivation set, then run **once** on the held-out set: *two of {motion, outdoor/spatial,
15+ items}* → curated **5/6** pass, ordinary **1/4** pass (both coders gave the same result).

Read with care:
- Spec boards and written stories were **more common in ordinary work**. This may be why score-based
  rubrics rewarded manual-style cases.
- Only **1 of 20** curated projects had all of story + logo + business card + pattern + motion. Items 1–4
  are a floor this kit chooses, not a description of featured work.
- These traits show completeness and production effort. They can be satisfied by weak design, and curation
  may follow studio resources as much as quality. Correlation, small sample.
- The order rule was broken for two gallery positions that were skipped by mistake; whether the
  "ordinary" projects were never featured could not be verified from the page.
