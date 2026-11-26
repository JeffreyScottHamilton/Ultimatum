# Gates: tiers, waivers, the stamp, finish checks and judged clauses

Read before building (tiers and critique) and again at the sweep (finish checks, judged clauses, reviews). The 90-row table of every gate is `../../../../../data/craft/hallmark/gates.csv`; where the table and this file disagree, this file wins.

## Tiers

- **Floor:** cannot be waived. Each one is either something no admired page breaks deliberately (correctness, access, honesty, bans) or an Ultimatum house rule: the eyebrow (54), the screen budget (58), template punctuation (63) and the tracked-caps label (67).
- **Reflex:** a default a model slides into. A real reason, on the record, waives it. More than three waivers means the page has a house style, which belongs in a locked design file (`design-file.md`).
- **Finish:** craft detail you cannot see at arm's length (the F-checks below). Reported and answered, never blocking.
- **Ledger:** repetition bookkeeping (gate 32). Notes only.
- **Checked by:** M is a static scan of CSS and markup (Tailwind class strings included); R needs a rendered page; J is judged by eye. With a lint run, walk only the R/J and J gates by hand.
- **Grades:** FAIL (Floor, nothing ships), REFLEX (unanswered: fix or waive), WAIVED, WARN (suspected: confirm and fix, or dismiss on the record), ANSWERED, NOTE.
- Retired numbers are never reused, so older stamps still parse. Retired: 61, 60, 57, 52, 51, 45, 43, 36, 35, 31, 21, 14, 13 and 5.
- Nothing ships with an open FAIL or open REFLEX. Our checks for the same ground are in `../taste/quality-gate.md`; run those as the render route.

## Stamp, waivers and answers

The stamp is the first CSS comment: build name and version, genre, theme or "custom", shape, hero posture, nav, footer, job, colour posture, then the critique line, then waivers.

```css
/* waive 47b | one frame holding a real terminal capture | the terminal is what we sell */
/* answered F3 | the display head is a single word and cannot wrap */
/* dismissed 58 | the window holds one five-row table, counted twice across a sticky pane */
```

- A waiver has three fields: the gate clause (47b, not 47), the evidence that its guard holds, and a reason about this page that shares a word with it. A reason under 24 characters, boilerplate, or reused on another waiver is rejected. One waiver per clause.
- A waiver naming a Floor gate is void and the gate fires.
- Words the user insists on are material: mark `copy: verbatim` and the copy gates (19, 58, 69) become notes.
- A redesign records what it knowingly drops (`redesign.md`).

## Pre-emit critique

Before building, score the planned page 1–5 on six axes; any score under 3 forces a revision first.

| Axis | A 3 looks like | A 5 looks like |
|---|---|---|
| Philosophy | has a tone | has an argument someone could dispute |
| Hierarchy | wants another look | passes the squint test |
| Execution | 2–3 loose details | passes the gates first time |
| Specificity | suits the category | would fit no other product |
| Restraint | one decoration too many | something you liked was cut |
| Variety | differs from the log on 3 of 6 structural axes | has almost nothing in common with the last 3 runs |

Write the scores, name the weakest axis and say what you did about it. A run of straight 5s must say what was cut to earn them. Do not make up a weakness to fill the field.

## Finish checks (F1 to F26)

- F1 straight quotes inside prose. F2 three full stops where an ellipsis belongs. F3 display heads without balanced wrapping.
- F4 a page with several filled-primary button recipes (a dialog counts separately), or two filled buttons adjacent.
- F5 icon sitting in a coloured coin. F6 figures at display size lacking tabular numerals.
- F7 one container recipe on six or more selectors, or a pill radius on five or more non-control selectors.
- F8 a second scroll-choreography pattern. F9 hotlinked avatars of fake humans (an outright fail) or stock URLs picked by searching for a person. F10 an animation file used where CSS or SVG suffices.
- F11 a highlighter stripe drawn on the baseline rather than behind the x-height, an underline thicker than 2px, or an offset beyond 0.25em.
- F12 a flex row with unequal heights and no centre alignment. F13 an outlier typeface doing two jobs. F14 a helper-text slot with no line of height held back.
- F15 broken page invariants: a single primary button style, a single container width, a single column gap beneath the hero, one radius at each nesting depth, and centred heading groups never outnumbering left-aligned ones.
- F16 selection, caret or scrollbar colour left at browser defaults although the palette is committed.
- F17 at 1440, a text block crushed to a narrow sliver. F18 a slot under 40px in either dimension, or slots with no fill script.
- F19 over three font weights in running use. F20 a lone item on the last row of a grid under a fuller row.
- F21 skipped heading level. F22 hyphenless justified text. F23 a document with no `lang`, `<title>` or meta description.
- F24 a hairline border sitting beneath a wide soft shadow on a single surface. F25 content phones never receive: about 40 words visible at 1440 yet hidden at 375, or a table whose columns fall off-screen.
- F26 a paragraph, or a 2–3 line heading, whose last line is a lone word at 375 or at 1280.

## Judged clauses

- **6b hero shape:** a single centred object counts as composition, whereas four items stacked on the centre line is the default. Allow two centred elements at most, with one breaking alignment. A stamped posture fills its screen; an unstamped hero stops below 92dvh.
- **8 and 32 repetition:** check against the log fingerprint, newest entry first, and never from memory. One composition used twice running on a page is the template. Between pages, a changed order or opening composition is sufficient.
- **9 rhythm:** whitespace, hairline, tinted well, card. If a page climbs the identical step at every seam it reads as a template.
- **11 hover:** a single signal per element. The container gives feedback, never the image, and things that do nothing ignore the pointer entirely.
- **16 toasts:** skip the toast when the result is visible; reserve toasts for failures and effects the visitor cannot see.
- **23 accent footprint:** against the 1280×800 fold, count solid fills, big accent headings and full-bleed accent bands. A surface colour that was declared moves into tokens; spread nobody declared fails.
- **29 glow:** the bloom is the tell whether drawn with shadow or gradient. Elsewhere depth is lightness steps and offset shadows.
- **38iii accented word:** one word in colour, bold or on a highlight is the most common machine head after the eyebrow. Three catalogue themes (see `themes.md`) carry it as their signature, stamped and used once, in the hero.
- **44 the fold:** at 1280×800 the whole hero message must fit on screen; at 1440×900 it is exactly one screen with the visual next to the text; at 1920×1080 the container must hold. Fill a short hero by enlarging the visual or headline, not by adding copy.
- **46b bare number:** a figure may be a headline only if the page is built around it with its unit and its source.
- **47c imitation:** ask whether the object pretends. A product sample in a slot, using sample-looking values and a handoff note, is honest. A dashboard of styled divs with invented figures does. Geometry that is honestly geometry (a diagram, chart or line) passes; geometry dressed up as a picture gives it away. Any grid or stripe pattern needs a canvas, map or measuring tool under it.
- **54 eyebrow test:** small type ahead of a heading survives only when it holds a fact, a destination or an identifier. Remove it and reread; if all that disappeared is a label for the next block, it was an eyebrow. Never fix it by bare deletion alone.
- **58 screen budget:** each screen carries one idea and roughly 80 words per 900px window, counting labels and table cells.
- **62 hidden at rest:** safe shapes are a script-added class gating the hidden state, a CSS animation starting from visible, or `@starting-style`.
- **63 punctuation:** the middle dot, arrow suffix and coloured dot prefix are generated-page punctuation. One dot in a byline, a marquee separator and a live-state dot are legal.
- **65 named look:** cream paper, high-contrast serif, terracotta. A catalogue theme using it appears only when the brief's keywords call for it; custom builds decline it first.
- **66 decoration text:** agency habits (rotated labels, scroll cues, version pills, weather strips, caps strips, credit lines beneath stock) signal "designed" without stating a fact. Facts stay and decoration goes.
- **67 tracked caps:** delete the transform and tracking and reread; the body face a step smaller says it without announcing a machine. Capitals live in wordmarks and in themes built on uppercase display.
- **68 wireframe page:** six blank portraits or four grey bottles are each honest and together look unfinished. Set the set in type; keep 1–2 slots holding photos or the built product.
- **69 echo:** a thin prompt tempts repeating its few facts (the price in hero, cards, FAQ, footer). Say it once.
- **70 fake send:** a form that reports success to nobody invents an outcome. Until wired, it validates, posts nowhere and states that plainly (for example: "Not connected yet, so nothing left this page").
- **77–79 a full page:** the opposite failure to clutter: small things on a wide canvas. The fix is mass (a bigger visual, wider body, head at section size, a set statement), never more words or a smaller gap.
- **80–82 pictures:** a page with nothing real grabs for drawings, coloured boxes and rows of tally marks. Photos exist, the product can be built, and a number can be set large.
- **83 photo wall:** all photographs reads as a stock gallery; keep the ones carrying facts, set big, and build between them from the theme's material.
- **84 fake product:** find out where the product lives before mocking it. If the brief names an app, site, folder or URL, capture it: main screen, one detail, a second screen and the phone view. Mock only a product that is not built yet, with the handoff listing screens to capture later.
- **85 stock anatomy:** hero plus picture, figure row, three steps, split, email band is a habit. Judge the page as a whole against `anatomy.md`: does the action sit where the category puts it, are the category's own sections here, and could this order sit beneath another business's name?

## The two reviews, in fresh context

The builder is the weakest reviewer. Run a hero review once, before sections below the fold exist, and a finish review at the sweep, each in a subagent that inherits no transcript (otherwise in-thread, and say so). Prompts are in `review-prompts.md`.

- Hand over screenshots as file paths and stamp lines as quoted text. Hero review gets the four hero screenshots, the first two stamp lines, the Material and Signature rows and the theme picture. Finish review gets every screenshot, the page source, the theme file and picture, the hero findings with how each ended, the gate list and, for redesigns, the before shots.
- Run in the foreground; the build waits on its first word.
- A reply starting `recapture` means the screenshots were faulty (fallback font, empty frame): retake them and restart without spending a round. Otherwise repair what is real, recapture, and mark each finding resolved, partial or unresolved with a reason. A second scoring round happens only after a `rebuild` verdict or a Floor finding.
- Log the outcome in the stamp, hero first.

Merged: our own critic checklist for the same questions is `../../../../../agents/taste-critic.md`; this file adds the numbered gates, it does not replace it.
