# Responsive: widths, breakpoints, units and tables

Read when a layout is unusual or a page breaks on a phone. Every page must work from 320 to 1920 CSS px with no sideways scroll and no desktop-only interaction.

## Check by eye at each width

Widths: 320, 375, 414, 768, 1024, 1280, 1440, 1920. A script catches horizontal scroll, wrapping buttons and stacked sticky bars; your eyes must check that sidebars and filters collapse into a menu or disclosure, section heads stack, and any per-theme override carries its own mobile rule. Screenshot recipe in `redesign.md`; Playwright viewport use in `imagery.md`.

## Breakpoints

Two, in `rem` so they follow the user's font size, shared page-wide:

- Under 60rem (about 960px): grids go to one column, tilts and clips drop, sticky panes unstick, heroes collapse to content height (a poster hero may stay full-bleed); gutters 24px, section gaps 80/96/120.
- Under 40rem (about 640px): display type steps down, margin notes move inline; gutters 16px, section gaps 56/72/96, column gaps 16px.

Add a third only where the content itself breaks. Write all rules in one direction.

## Fluid and discrete

`clamp()` for continuous sizes; media queries for layout jumps. Detect capability, not width:

```css
@media (hover: hover) { .link:hover { text-decoration-thickness: 2px; } }
@media (pointer: coarse) { .btn { min-height: 48px; } }
```

## Clickable text never wraps

Buttons, primary nav and CTAs stay on one line from 320 to 1920. Fix order: shorten the label ("Start free"), then `white-space: nowrap` and let the row reflow, then collapse the row so extra links go behind a menu. A call-now button on a local site keeps its number visible in the label on phones and uses `tel:`.

## Units and safe areas

- `dvh` or `svh` where a block meets browser chrome; never `vh` on a hero; `width: 100%` not `100vw`.
- With `viewport-fit=cover`: `--gutter: max(16px, env(safe-area-inset-left))`.

## Tables, images, languages

- Tables on phones: restack each row as a labelled block or pin the first column. Ten columns on a phone is a redesign. Dashboards get a card list under 40rem.
- Images: `srcset` with widths, `<picture>` for a different crop, width and height attributes, `loading="lazy"` below the fold and never on the LCP image.
- Languages: logical properties, room for 30 to 40% longer strings, no hard-coded date or number formats.

Never: device sniffing, hover-only features, `px` breakpoints.
