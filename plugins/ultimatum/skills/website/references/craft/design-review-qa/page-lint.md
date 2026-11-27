# Page lint: run the checkable design tells against pages, stylesheets and components

Read after building or changing a page and before the design review, to catch what a script can see; then do the judged review in `slop-tells.md` and `../hallmark/gates.md` by eye.

## Run it

```
python3 ../../../../../data/craft/design-review-qa/page_lint.py dist/
python3 .../page_lint.py src/components/ --only purple-gradient,generic-copy
python3 .../page_lint.py site/ --format json > lint.json
python3 .../page_lint.py site/ --format github      # annotations in a CI log
python3 .../page_lint.py site/ --genre atmospheric  # skip that genre's allowed moves
python3 .../page_lint.py --rules
```

From the plugin root: `data/craft/design-review-qa/page_lint.py`. Standard library only, no network. Exit 1 when it finds something, 0 when clean, 2 on bad arguments.

What it reads:

- `.html` and `.htm` pages, with every local stylesheet they link (remote URLs are never fetched). A page and its sheets are judged together, so page-wide checks such as focus styles or reduced motion see all of them.
- `.css` files no page in the run links, on their own.
- Component files: `.jsx`, `.tsx`, `.vue`, `.svelte`, `.astro`. String literals inside `className={...}`, `cn()`, `clsx()` and `:class` are read as classes, `<style>` blocks as CSS, and icon imports are noted. Tailwind utilities are mapped onto the same rules (for example `bg-clip-text` with a gradient, `outline-none` with no focus ring, `min-h-screen` on a hero, `animate-*` with no `motion-safe:` variant).
- `var()` is resolved from the token block (`:root`, `html`, `:host`, theme selectors, or a rule holding only custom properties), so contrast and colour checks see the real values.

## Waivers and genres

A deliberate exception goes in a comment next to the code, in any comment style:

```
/* page-lint: allow glow, frosted-glass: the night-sky hero is the brand; one layer only */
```

It applies to that page and the sheets it links. A waiver with no reason after the second colon, or naming an unknown rule, is reported as `waiver-no-reason` and waives nothing. Paste the waivers into the review report so the reviewer can disagree.

`--genre` drops the rules that genre is allowed to break: `atmospheric` (glow, frosted glass, background texture), `playful` (bounce, blobs, hard sticker shadows), `modern-minimal` (pure white paper and zero-chroma greys), `editorial` (italic display type).

## What it checks

87 rules. Tell ids come from the first column of `../../../../../data/craft/design-review-qa/slop-tells.csv`; gate numbers are rows of `../../../../../data/craft/hallmark/gates.csv`.

| Rule | Severity | Tell or gate |
|---|---|---|
| **Colour** | | |
| `purple-gradient` | medium | `classic-purple-gradient`, gate 2a |
| `gradient-text` | medium | `gradient-text`, gate 2b |
| `pure-black-white` | low | gate 7a |
| `pure-black-surface` | low | gate 7b |
| `framework-swatch` | medium | gate 74 |
| `grey-neutral` | low | gate 22 |
| `colour-literal` | low | gate 48 |
| `low-contrast` | high | gate 40 |
| `gray-on-colour` | medium | gate 41 |
| `cream-look` | medium | `cream-palette`, gate 65 |
| **Type** | | |
| `system-font-main` | medium | `classic-system-font` |
| `default-font` | low | `overused-font`, gate 1 |
| `too-many-fonts` | medium | gate 37 |
| `flat-type-scale` | medium | `flat-type-hierarchy` |
| `oversized-h1` | medium | `oversized-h1` |
| `italic-word` | low | gate 38i |
| `italic-display` | medium | `italic-serif-display`, gate 38ii |
| `caps-tight-leading` | medium | gate 55a |
| `mono-costume` | low | gate 64 |
| `tracked-caps` | low | gate 67 |
| `extreme-tracking` | medium | gate 75 |
| `tiny-text` | medium | gate 75 |
| `tight-leading` | medium | gate 75 |
| `prose-width` | medium | gate 25 |
| `justified-text` | low | gate 75 |
| `all-caps-body` | medium | gate 75 |
| `heading-order` | medium | accessibility |
| `display-no-wrap` | low | gate 50 |
| **Layout** | | |
| `uniform-radius` | medium | `classic-uniform-radius` |
| `left-border-card` | medium | `classic-left-border-card`, `border-accent-on-rounded` |
| `nested-cards` | medium | `nested-cards`, gate 4 |
| `hero-vh` | medium | gate 6a |
| `raw-spacing` | low | gate 24a |
| `off-scale-spacing` | low | gate 24b |
| `horizontal-scroll` | high | gate 34 |
| `bare-fr-images` | low | gate 50 |
| `double-sticky` | medium | gate 56 |
| `wordy-hero` | medium | gate 58 |
| `cramped-padding` | low | gate 59 |
| `icon-card-trio` | medium | `classic-three-column-grid`, `icon-tile-stack`, gate 3 |
| `empty-slots` | medium | gate 68 |
| `fake-chrome` | medium | gate 47a |
| `device-frame` | low | gate 47b |
| **Effects** | | |
| `glow` | medium | `dark-glow`, `radial-halo`, `radial-spotlight-glow`, gate 29 |
| `frosted-glass` | medium | `judge-frosted-glass` |
| `hard-offset-shadow` | low | gate 29 |
| `thin-border-wide-shadow` | low | gate 29 |
| `pattern-background` | low | `classic-blobs-waves` |
| `organic-shape` | low | `classic-blobs-waves`, `shape-assembled-illustration` |
| `marquee` | medium | `marquee` |
| **Copy** | | |
| `generic-copy` | high | `classic-generic-hero-copy`, `marketing-buzzword`, gate 19 |
| `theater-phrase` | medium | `theater-slop-phrase` |
| `rebuttal-cadence` | medium | `aphoristic-cadence`, gate 19 |
| `em-dash` | low | gate 19 |
| `template-punctuation` | low | gate 63 |
| `needs-source` | high | `judge-fake-stats`, `judge-fake-testimonials`, gate 46a |
| `numbered-labels` | low | gate 54 |
| `stock-newsletter` | low | gate 85 |
| `vague-cta` | medium | `judge-vague-cta` |
| `eyebrow-chip` | low | `hero-eyebrow-chip`, `kicker-above-heading`, gate 54 |
| `emoji-heading` | medium | `classic-emoji-design` |
| `emoji-icon` | medium | `classic-emoji-design`, gate 30a |
| `placeholder` | high | `judge-stock-hero`, gate 19 |
| **Motion** | | |
| `transition-all` | medium | gate 10a |
| `layout-transition` | low | gate 10b |
| `bounce-easing` | medium | gate 12 |
| `focus-fade` | medium | gate 15 |
| `autoplay-carousel` | medium | gate 18 |
| `no-reduced-motion` | high | gate 27 |
| `hidden-at-rest` | high | gate 62 |
| `pulsing-dot` | low | gate 63 |
| `blinking-cursor` | low | gate 63 |
| **Access and states** | | |
| `img-no-alt` | medium | accessibility |
| `focus-removed` | high | gate 26a |
| `no-focus-style` | medium | gate 26a |
| `missing-states` | low | gate 26b |
| `input-focus-border` | low | gate 39a |
| `control-height` | low | gate 39b |
| `unlabelled-svg` | low | gate 33 |
| `autoplay-sound` | high | gate 28a |
| `lazy-hero-image` | medium | gate 28a |
| `video-poster` | low | gate 28b |
| `form-no-action` | medium | gate 70 |
| **Images and icons** | | |
| `broken-image` | high | gate 76 |
| `stock-photo` | low | gate 76 |
| `two-icon-libraries` | low | gate 30b |
| **Waivers** | | |
| `waiver-no-reason` | low | linter |

Aggregate rules (`uniform-radius`, `frosted-glass`, `colour-literal`, `off-scale-spacing`, `too-many-fonts`, `empty-slots`) report once per page, at the first place they apply, with a count.

## What it cannot see

- Anything judged: whether a testimonial is real, a default hero layout, cards for unequal content, the happy path only, theme by cliche. Those stay in the review.
- Layout after rendering: overflow at 320px, overlaps, real line lengths, tap target sizes, what the first screen shows. Check those in a browser with the Playwright recipes in `design-audit-recipes.md`.
- Styles built at run time (CSS-in-JS objects, class names from variables) and pages built by script after load. Lint a saved, rendered copy for those.
- Contrast where the background is an image, a gradient or set on an ancestor in another file; it compares only a rule's own colour and background, or body text against the page colour.

## Using the result

1. Fix every `high` before showing the page to anyone.
2. For each `medium`, fix it or add a waiver with a one-line reason that is specific to this brand.
3. `low` rows are questions for the review, not defects.
4. Lint again; paste the final `no findings` line, or the remaining rows and waivers, into the review report.

A clean lint is not a passed review: it means none of these 87 patterns were found, nothing more.
