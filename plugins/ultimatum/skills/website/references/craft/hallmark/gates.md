# Gates: tiers, waivers, the stamp, finish checks and judged clauses

Read before building (tiers and critique) and again at the sweep (finish checks, judged clauses, reviews). The 90-row table of every gate is `../../../../../data/craft/hallmark/gates.csv`; where the table and this file disagree, this file wins.

## Tiers

- **Floor:** never waived. Either no admired page breaks it on purpose (correctness, access, honesty, bans), or it is a house rule: the eyebrow (54), the screen budget (58), template punctuation (63), the tracked-caps label (67).
- **Reflex:** a default a model slides into. A real reason, on the record, waives it. More than three waivers means the page has a house style, which belongs in a locked design file (`design-file.md`).
- **Finish:** craft detail you cannot see at arm's length (the F-checks below). Reported and answered, never blocking.
- **Ledger:** repetition bookkeeping (gate 32). Notes only.
- **Checked by:** M is a static scan of CSS and markup (Tailwind class strings included); R needs a rendered page; J is judged by eye. With a lint run, walk only the R/J and J gates by hand.
- **Grades:** FAIL (Floor, nothing ships), REFLEX (unanswered: fix or waive), WAIVED, WARN (suspected: confirm and fix, or dismiss on the record), ANSWERED, NOTE.
- Gate numbers once retired stay retired so old stamps still read: 5, 13, 14, 21, 31, 35, 36, 43, 45, 51, 52, 57, 60, 61.
- Nothing ships with an open FAIL or open REFLEX. Our checks for the same ground are in `../taste/quality-gate.md`; run those as the render route.

## Stamp, waivers and answers

The stamp is the first CSS comment: build name and version, genre, theme or "custom", shape, hero posture, nav, footer, job, colour posture, then the critique line, then waivers.

```css
/* waive 47b | one frame with a real terminal capture inside | the terminal is the product on sale */
/* answered F3 | the display head is a single word and cannot wrap */
/* dismissed 58 | the window holds one five-row table, counted twice across a sticky pane */
```

- A waiver has three fields: the gate clause (47b, not 47), the evidence that its guard holds, and a reason about this page that shares a word with it. A reason under 24 characters, boilerplate, or reused on another waiver is rejected. One waiver per clause.
- A waiver naming a Floor gate is void and the gate fires.
- Words the user insists on are material: mark `copy: verbatim` and the copy gates (19, 58, 69) become notes.
- A redesign records what it knowingly drops (`redesign.md`).

## Pre-emit critique

Before building, score the planned page 1 to 5 on six axes; any score under 3 forces a revision first.

| Axis | A 3 looks like | A 5 looks like |
|---|---|---|
| Philosophy | has a tone | has an argument someone could dispute |
| Hierarchy | needs a second look | survives the squint test |
| Execution | two or three loose details | passes the gates first time |
| Specificity | fits the category | could belong to no other product |
| Restraint | one decoration too many | something you liked was cut |
| Variety | differs from the log on three of six structural axes | shares almost nothing with the last three runs |

Record the scores, name the weakest axis and the fix taken. Straight 5s say what was cut to earn them. Never invent a weakness to fill the field.

## Finish checks (F1 to F26)

- F1 straight quotes in prose. F2 three dots instead of an ellipsis. F3 no balanced wrapping on display heads.
- F4 more than one filled-primary button recipe on a page (a dialog counts as its own page), or two filled buttons side by side.
- F5 an icon in a coloured coin. F6 display-size figures without tabular numerals.
- F7 one container recipe on six or more selectors, or a pill radius on five or more non-control selectors.
- F8 more than one scroll-choreography pattern. F9 fake-human avatar hotlinks (a failure) or person-keyword stock URLs. F10 an animation file where CSS or SVG would do.
- F11 a highlighter band at the baseline instead of behind the x-height, an underline over 2px or offset over 0.25em.
- F12 a flex row of unequal heights without centre alignment. F13 the outlier face carrying two roles. F14 a helper-text slot with no reserved line of height.
- F15 page invariants broken: one primary button style, one container width, one column gap below the hero, one radius per nesting level, no more centred heading groups than left ones.
- F16 browser surfaces unthemed (selection, caret, scrollbar colour) on a committed palette.
- F17 a text block squeezed into a sliver at 1440. F18 a slot under 40px in either dimension, or slots with no fill script.
- F19 over three font weights in running use. F20 a lone item on the last row of a grid under a fuller row.
- F21 a skipped heading level. F22 justified text without hyphenation. F23 a document missing `lang`, `<title>` or meta description.
- F24 a hairline border under a wide soft shadow on one surface. F25 content a phone never gets: about 40 words shown at 1440 and hidden at 375, or a table with columns off-screen.
- F26 a paragraph ending on one word, or a two- or three-line head ending on a stub, at 375 or 1280.

## Judged clauses

- **6b hero shape:** one centred object is a composition; four things stacked on the centre line is a default. At most two centred elements, one breaking alignment. A hero with a stamped posture fills its screen; an unstamped one stops short of 92dvh.
- **8 and 32 repetition:** compare against the log's fingerprint, newest first, never memory. Same composition twice in a row on one page is the template; across pages a different order or lead composition suffices.
- **9 rhythm:** whitespace, hairline, tinted well, card. A page that climbs the same rung at every seam reads as a template.
- **11 hover:** one signal per element; feedback belongs to the container, never an image; inert things ignore the pointer.
- **16 toasts:** if the effect is visible, no toast; toasts are for failures and invisible effects.
- **23 accent footprint:** count solid fills, large accent heads and full-bleed accent bands against the 1280 x 800 fold. A declared surface colour moves into tokens; undeclared sprawl fails.
- **29 glow:** the bloom is the tell whether drawn with shadow or gradient. Elsewhere depth is lightness steps and offset shadows.
- **38iii accented word:** one word in colour, bold or on a highlight is the most common machine head after the eyebrow. Three catalogue themes (see `themes.md`) carry it as their signature, stamped and used once, in the hero.
- **44 the fold:** at 1280 x 800 is everything the hero says inside the screen; at 1440 x 900 is it exactly one screen with the visual beside the text; at 1920 x 1080 does the container hold. Fill a short hero with the visual or the headline, never with copy.
- **46b bare number:** a figure may be a headline only if the page is built around it with its unit and its source.
- **47c imitation:** the question is whether the thing pretends. A product sample in a slot with sample-looking values, named in the handoff, does not; a styled-div dashboard with invented figures does. Geometry that is geometry (diagram, chart, line) is fine; geometry posing as a picture is the tell. Grids and stripes need a canvas, map or measuring tool under them.
- **54 eyebrow test:** small type before a heading stays only if it carries a fact, a destination or an identifier. Delete it and read the page; if only a name for the next block was lost, it was an eyebrow. The fix is never bare deletion.
- **58 screen budget:** one idea per screen; about 80 words per 900px window, labels and cells included.
- **62 hidden at rest:** safe shapes are a script-added class gating the hidden state, a CSS animation starting from visible, or `@starting-style`.
- **63 punctuation:** the middle dot, arrow suffix and coloured dot prefix are generated-page punctuation. One dot in a byline, a marquee separator and a live-state dot are legal.
- **65 named look:** cream, high-contrast serif, terracotta. A catalogue theme carrying it is dealt only on its keywords; custom builds refuse it first.
- **66 decoration text:** agency tics (rotated labels, scroll cues, version pills, weather strips, caps strips, credit lines under stock) say "designed" without carrying a fact. A fact stays; decoration goes.
- **67 tracked caps:** delete the transform and tracking and reread; the body face a step smaller says it without announcing a machine. Capitals live in wordmarks and in themes built on uppercase display.
- **68 wireframe page:** six blank portraits or four grey bottles are each honest and together look unfinished. Set the set in type; keep one or two slots holding photos or the built product.
- **69 echo:** a thin prompt tempts repeating its few facts (the price in hero, cards, FAQ, footer). Say it once.
- **70 fake send:** a form answering "Sent" to nobody is an invented outcome. Until wired it validates, posts nowhere and says so ("Nothing was sent; this form is not connected yet").
- **77 to 79 a full page:** the opposite failure to clutter: small things on a wide canvas. The fix is mass (a bigger visual, wider body, head at section size, a set statement), never more words or a smaller gap.
- **80 to 82 pictures:** a page with nothing real reaches for drawings, coloured boxes and rows of counting marks. The library has photos, the product can be built, the number can be set large.
- **83 photo wall:** all photographs reads as a stock gallery; keep the ones carrying facts, set big, and build between them from the theme's material.
- **84 fake product:** ask where the product is before building a mock. A named app, site, folder or URL means capture it: main screen, a detail, a second screen, the phone view. A mock is right only for an unbuilt product, and the handoff names the screens to capture later.
- **85 stock anatomy:** hero beside a picture, a figure row, three steps, a split, an email band is a habit. Judge the whole page against `anatomy.md`: is the action where the category puts it, are the category's own sections present, could this sequence sit under a different business's name?

## The two reviews, in fresh context

The builder is the weakest reviewer. Run a hero review once, before sections below the fold exist, and a finish review at the sweep, each in a subagent that inherits no transcript (otherwise in-thread, and say so). Prompts are in `review-prompts.md`.

- Pass screenshots as file paths and stamp lines as quoted text. Hero review: four hero screenshots, the stamp's first two lines, the Material and Signature rows, the theme picture. Finish review: all screenshots, the page source, the theme file and picture, the hero findings and how each was settled, the gate list, and on a redesign the before shots.
- Run in the foreground; the build waits on its first word.
- First word `recapture` means the screenshots were wrong (fallback font, blank frame): retake and restart, no round used. Otherwise fix what is real, recapture, and score each finding resolved, partial or unresolved with a reason. A second scoring round only after a `rebuild` verdict or a Floor finding.
- Record the outcome in the stamp, hero first.

Merged: our own critic checklist for the same questions is `../../../../../agents/taste-critic.md`; this file adds the numbered gates, it does not replace it.
