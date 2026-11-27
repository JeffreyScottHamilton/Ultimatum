# Render check: measure the built page in a real browser

Read after `page-lint.md` passes, when the page can be opened locally; it measures what only a rendered page shows, then the judged review in `slop-tells.md` and `../hallmark/gates.md` still happens by eye.

## Run it

```
python3 ../../../../../data/craft/design-review-qa/render_check.py dist/index.html
python3 .../render_check.py http://localhost:4321/ --widths 375,1440
python3 .../render_check.py site/ --format github           # CI annotations
python3 .../render_check.py site/ --json > render.json
python3 .../render_check.py page.html --shots shots/       # a full-page PNG per width
python3 .../render_check.py page.html --genre atmospheric  # that genre's allowances
python3 .../render_check.py --rules                         # the table below
```

It needs the Python `playwright` package and a Chromium it can start. It tries `RENDER_CHECK_CHROMIUM`, then Playwright's own browser, then `chromium`, `chromium-browser`, `google-chrome` on the path. With none it prints `render-check: skipped, no browser` and exits 3: report the pass as not run, never as passed.

Exit codes: 0 clean, 1 findings, 2 bad arguments (missing file, non-local URL), 3 skipped.

## Safety

- It opens files and `localhost`, `127.0.0.1` or `[::1]` only. Any other URL is refused unless `--allow-remote` is passed, and every request to another host is blocked while the page runs. Use the flag only for a page you own.
- With remote requests blocked, remote images fail to load. Boxes that held them can then read as `empty-picture`; the finding says the images were blocked. Serve the images locally, or rerun with `--allow-remote` on your own site.
- It reads nothing back but measurements and screenshots you asked for. Page scripts run, so open only pages you built or trust.

## Widths

Every pass runs at 320, 375, 414, 768, 1024, 1280, 1440 and 1920 wide (800 to 1080 tall on desktop sizes, 780 on phones). Overflow, wrapping, clipping and edge text are checked at all of them. Covered text is checked while scrolling at 375 and 1440. Type, contrast, spacing and section checks run at 1440; the first-screen checks at 1280; the wide-screen width check at 1920. A finding lists the widths where it showed.

## Rules

| Rule | Severity | Gate | What it means |
|---|---|---|---|
| `h-scroll` | high | gate 34 | the page scrolls sideways at this width; find the element wider than the window |
| `label-wrap` | high | gate 49a | a button or top-menu link wraps to a second line |
| `minor-link-wrap` | medium | gate 49b | a footer link, tab or breadcrumb runs past two lines |
| `low-contrast` | high | gate 40 | rendered text against its rendered background is under 4.5:1 (3:1 for large text) |
| `tiny-text` | medium | gate 75 | running text renders under 12px, or other text under 11px |
| `tight-leading` | medium | gate 75 | multi-line prose with line height under 1.3 of its size |
| `line-length` | medium | gate 25 | prose lines average over 88 characters, or under 35 on a long paragraph |
| `hero-out-of-view` | high | gate 44b | at 1280 x 800 the headline, lede, main action or the visual's centre is below the fold |
| `dead-band` | medium | gate 79 | over 160px of nothing between the hero's last content and the fold at 1440 x 900 |
| `next-section-position` | low | gate 44c | on a 1440 x 900 screen the following block's top edge lands above 760 (cramped hero) or past 900 (no sign there is more) |
| `no-max-width` | medium | gate 44d | at 1920 prose runs within 120px of the window edge; the container has no cap |
| `section-gap` | low | gate 59 | sections closer than 120px apart at 1440 (64px across a colour change), or every gap identical |
| `crowded-head` | medium | gate 71 | a heading sits closer to what precedes it than to what it introduces |
| `cramped-box` | medium | gate 72 | a tinted panel, or one with a left rule, has its words pressed against the edge |
| `small-section-heads` | low | gate 78 | median section heading under 40px at 1440 |
| `empty-picture` | medium | gate 81 | a 300 x 200 or larger block that shows only a fill or gradient |
| `counting-marks` | low | gate 82 | 24 or more identical empty marks in a row standing for a number |
| `photo-wall` | low | gate 83 | under the hero, pictures take more than one third of the page area |
| `stock-close` | low | gate 85 | the last block asks only for an email; confirm a newsletter is really what this page is for |
| `text-covered` | high | gate 73 | text is painted under another element (sticky bars excepted) |
| `accent-flood` | low | gate 23 | saturated fills cover over 8% of the first screen (30% atmospheric, 60% playful) |
| `edge-text` | medium | small screens | text within 12px of the window edge on a phone width |
| `clipped-text` | medium | states | text cut off by a box that hides its overflow |
| `hidden-at-rest` | high | motion | a large share of the text is still invisible after scrolling the whole page |
| `straggler-heading` | low | type | a heading's last line is one word |
| `script-error` | high | states | the page threw an error while loading |
| `broken-image` | high | assets | an image failed to load |
| `waiver-no-reason` | medium | linter | a render-check waiver with no reason or an unknown rule; it waives nothing |

Gates are the numbered gates in `../hallmark/gates.md`; rows marked otherwise come from this pass's own checks.

## Waivers

A deliberate exception is written in the page, in an HTML comment or a stylesheet comment, with a reason:

```
<!-- render-check: allow photo-wall: a photographer's portfolio, the pictures are the content -->
/* render-check: allow accent-flood: festival poster brief */
```

A waiver without a reason, or naming a rule that does not exist, is reported as `waiver-no-reason` and silences nothing. A page whose header comment declares `posture: full-palette` is treated as a deliberate loud palette for `accent-flood`.

## What it gets right that a reader misses

- Real contrast: text colour over the painted background, after transparency, at the size the text renders. A background image or gradient behind the text is skipped, not guessed.
- Real wrapping: a button that breaks onto two lines at 375 but not at 1440.
- The first screen as a visitor sees it: whether the hero fits, how much empty band sits above the fold, whether the next section peeks in.
- Text hidden at rest by a scroll animation that never ran, and text painted under another element.

## What it cannot see

- Anything judged: tone, whether the copy is true, whether the layout suits the business. That stays in the review.
- Hover, focus and pressed states beyond what is visible at rest. Use the Playwright recipes in `design-audit-recipes.md` for those, and `qa-playwright-recipes.md` for flows.
- Pages that need a login or data to render. Save a rendered copy, or point it at a local dev server that has the data.
- Motion over time: it measures settled frames, not whether an animation is smooth.

## Using the result

Fix high findings before the design review. Medium findings are fixed or waived with a reason. Low findings are questions for the reviewer, not defects: `stock-close`, for example, asks whether an email sign-up is really the page's job. Quote the command and its exit code in the report, and name the widths you ran.
