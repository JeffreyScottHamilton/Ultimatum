# Audit checklist, part 1: hierarchy, type, colour, space, responsive

Read while auditing a page's look. Part 2 (`checklist-behaviour.md`) covers states, motion, copy and speed; `slop-tells.md` is category 9. Rate each finding high, medium or polish. The same rows are in `../../../../../data/craft/design-review-qa/design-checks.csv` for lookup.

## 1. Visual hierarchy and composition

- One clear focal point and one primary action per view.
- The eye can travel in a sensible order across the page.
- No competing elements fighting for the same attention.
- Information density suits the content type.
- Nothing overlaps by accident; stacking order is clear.
- Above the fold says the purpose within three seconds.
- Squint test: blur the screenshot; the hierarchy must still show.
- White space looks chosen, not left over.

## 2. Typography

- At most 3 font families (flag more).
- A scale with a ratio (1.25 or 1.333 are typical), not arbitrary sizes.
- Line height about 1.5 for body, 1.15 to 1.25 for headings.
- Line length 45 to 75 characters, near 66 ideal.
- Heading levels never skip (h1 to h3 with no h2).
- At least two weights create the hierarchy.
- No novelty or banned faces (script and brush fonts, Papyrus, Comic Sans, Impact, Courier New as body).
- An overused display face is flagged (`slop-tells.md` § Fonts); the exception is body or interface text on an Operate or Read page where the design doc assigns it that job.
- `text-wrap: balance` (or `pretty`) on headings. Check: `getComputedStyle(h1).textWrap`.
- Curly quotes and the single ellipsis character instead of straight quotes and three full stops.
- Digits that line up (`font-variant-numeric: tabular-nums`) in number columns and prices.
- Body at least 16 px; captions and labels at least 12 px.
- No letter-spacing on lowercase running text.

Docs: [text-wrap](https://developer.mozilla.org/en-US/docs/Web/CSS/text-wrap), [font-variant-numeric](https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-numeric).

## 3. Colour and contrast

- A coherent palette: no more than about 12 distinct non-grey colours; neutrals all warm or all cool.
- WCAG 2.2 AA: 4.5:1 for body text, 3:1 for large text (18 px and up, or 14 px bold) and for interface component edges and icons ([contrast minimum](https://www.w3.org/TR/WCAG22/#contrast-minimum), [non-text contrast](https://www.w3.org/TR/WCAG22/#non-text-contrast)).
- Semantic colours stay consistent: success green, error red, warning amber.
- Colour is never the only signal; add a label, icon or pattern. Red against green alone fails roughly 1 in 12 men.
- Dark mode: elevation, not plain inversion; body text off-white (around `#e0e0e0`), not pure white; accent desaturated 10 to 20 per cent; `color-scheme: dark` set so form controls and scrollbars follow ([color-scheme](https://developer.mozilla.org/en-US/docs/Web/CSS/color-scheme)).

## 4. Spacing and layout

- A grid that holds at every breakpoint; nothing floats off it.
- Spacing from a scale on a 4 or 8 px base, not one-off values (the extraction in `design-audit-recipes.md` lists the values in use).
- Related items sit close; distinct sections sit apart (rhythm).
- A radius hierarchy, not one big radius everywhere. A nested element's radius is the outer radius minus the gap.
- A cap on content width, so body text never runs edge to edge.
- `env(safe-area-inset-*)` where notches matter ([env()](https://developer.mozilla.org/en-US/docs/Web/CSS/env)).
- Filters, tabs and pages live in the URL so links and the back button work.
- Layout uses flex or grid, not script measurement.
- Breakpoints tested at 375, 768, 1024 and 1440 (the taste folder's full run adds 320 for reflow: `../taste/quality-gate.md` § Widths).

## 6. Responsive design

(Numbered as in the source list; category 5 is in part 2.)

- The phone layout is designed, not stacked desktop columns.
- No sideways scroll at any width, down to 320 ([reflow](https://www.w3.org/TR/WCAG22/#reflow)).
- Images respond (`srcset` and `sizes`, or contained by CSS).
- Navigation collapses sensibly (menu button, bottom bar).
- Forms use the right input types and do not steal focus on load on phones.
- The viewport meta never blocks zoom (`user-scalable=no`, `maximum-scale=1`); that fails WCAG 1.4.4 resize.

## Where it overlaps

Interface basics in `../../website/design-rules.md` § 7 (focus ring, 44 px, 16 px) are the same checks; here they carry thresholds and a place in the scoring.
