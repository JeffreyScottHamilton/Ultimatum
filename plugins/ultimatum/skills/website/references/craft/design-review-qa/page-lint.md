# Page lint: run the checkable slop tells against built HTML and CSS

Read after building or changing a page and before the design review, to catch the tells a script can see; then do the judged review in `slop-tells.md` and `../hallmark/gates.md` by eye.

## Run it

```
python3 ../../../../../data/craft/design-review-qa/page_lint.py dist/
python3 .../page_lint.py index.html --only purple-gradient,generic-copy
python3 .../page_lint.py site/ --json > lint.json
python3 .../page_lint.py --rules
```

From the plugin root: `data/craft/design-review-qa/page_lint.py`. It reads `.html`, `.htm` and `.css` files, follows `<link rel="stylesheet">` to local files, and never fetches a remote URL. Standard library only. Exit 1 when it finds something, 0 when clean, 2 on an unknown rule.

Run it on the built output (`dist/`, `out/`, `.next/server/app` HTML), not on JSX source: class names and styles are only final after the build. For a framework that renders on request, save the page with the browser or `curl` first and lint the saved file.

## What it checks

| Rule | Severity | Tell it checks |
|---|---|---|
| `purple-gradient` | medium | `classic-purple-gradient`, gate 2a |
| `gradient-text` | medium | `gradient-text`, gate 2b |
| `pure-black-white` | low | gate 7a (outside `:root` tokens) |
| `system-font-main` | medium | `classic-system-font` |
| `default-font` | low | `overused-font` (Inter, Poppins, Roboto and similar as the main face) |
| `uniform-radius` | medium | `classic-uniform-radius` (80% or more of six or more radius rules share one value) |
| `left-border-card` | medium | `classic-left-border-card`, `border-accent-on-rounded` |
| `glow` | medium | `dark-glow`, `radial-halo` (coloured shadow blur 40px or more) |
| `frosted-glass` | medium | `judge-frosted-glass` (backdrop blur on three or more rules) |
| `marquee` | medium | `marquee` |
| `flat-type-scale` | medium | `flat-type-hierarchy` (h1 under 1.2 times h2, fixed sizes only) |
| `emoji-heading` | medium | `classic-emoji-design` |
| `generic-copy` | high | `classic-generic-hero-copy`, `marketing-buzzword` |
| `vague-cta` | medium | `judge-vague-cta` (every button and button-styled link is generic) |
| `eyebrow-chip` | low | `hero-eyebrow-chip`, `kicker-above-heading` |
| `nested-cards` | medium | `nested-cards` (by class name) |
| `placeholder` | high | `judge-stock-hero` (lorem ipsum, placeholder image hosts, `[your company]`) |
| `img-no-alt` | medium | accessibility basics |

Tell ids come from the first column of `../../../../../data/craft/design-review-qa/slop-tells.csv`; gate numbers are rows of `../../../../../data/craft/hallmark/gates.csv`.

## What it cannot see

- Anything judged: fake testimonials or stats, a default hero layout, cards for unequal content, the happy path only, theme by cliche. Those stay in the review.
- Computed styles. It reads declared CSS, so a colour set through a variable, Tailwind utilities compiled elsewhere, or a `clamp()` font size is not resolved. For those, use the Playwright recipes in `design-audit-recipes.md`, which read computed values in a real browser.
- Pages built by JavaScript after load. Lint a saved, rendered copy.

## Using the result

1. Fix every `high` before showing the page to anyone.
2. For each `medium`, fix it or write one line on why it is right for this brand (for example a purple gradient that is the owner's real logo colour).
3. `low` rows are questions for the review, not defects.
4. Lint again; paste the final `no findings` line, or the remaining rows with their reasons, into the review report.

A clean lint is not a passed review: it means none of these eighteen patterns were found, nothing more.
