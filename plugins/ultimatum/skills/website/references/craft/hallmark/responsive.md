# Responsive: widths, breakpoints, units and tables

Read when a layout is unusual or a page breaks on a phone. Every page must work from 320–1920 CSS px with no sideways scroll and no desktop-only interaction.

## Check by eye at each width

Test eight widths in pixels: 320, 375, 414, then 768, 1024, 1280, 1440 and finally 1920. Automation can catch sideways scroll, wrapped buttons and stacked sticky bars; by eye, confirm sidebars and filters fold into a menu or disclosure, section heads stack, and every theme-specific override brings its own phone rule. Screenshot recipe in `redesign.md`; Playwright viewport use in `imagery.md`.

## Breakpoints

Use two, written in `rem` so they track the reader's font size, for the whole page:

- Under 60rem (about 960px): grids go to one column, tilts and clips drop, sticky panes unstick, heroes collapse to content height (a poster hero may stay full-bleed); gutters 24px, section gaps 80/96/120.
- Under 40rem (about 640px): display type steps down, margin notes move inline; gutters 16px, section gaps 56/72/96, column gaps 16px.

A third is justified only when the content itself breaks. Keep every rule going the same direction.

## Fluid and discrete

Use `clamp()` where sizes glide and media queries where layouts jump. Ask about the device's abilities rather than its width:

```css
@media (pointer: coarse) { .btn { min-height: 48px; } }
@media (hover: hover) { a.link:hover { text-decoration-thickness: 2px; } }
```

## Clickable text never wraps

Buttons, primary nav and CTAs stay on one line from 320–1920. Fix order: shorten the label ("Start free"), then `white-space: nowrap` and let the row reflow, then collapse the row so extra links go behind a menu. A call-now button on a local site keeps its number visible in the label on phones and uses `tel:`.

## Units and safe areas

- `dvh` or `svh` where a block meets browser chrome; never `vh` on a hero; `width: 100%` not `100vw`.
- When the page runs edge to edge (`viewport-fit=cover`), fold the notch inset into the gutter: `--gutter: max(16px, env(safe-area-inset-right))`.

## Tables, images, languages

- Tables on phones: turn each row into a labelled block, or keep the first column fixed. A ten-column table needs a redesign for a phone, not shrinking. Dashboards switch to a card list below 40rem.
- Images: `srcset` with widths, `<picture>` for another crop, intrinsic width and height attributes, and `loading="lazy"` for below-fold images, never the largest contentful one.
- Languages: logical properties, space for text that grows by a third or more, and locale-aware date and number formatting.

Never: device sniffing, hover-only features, `px` breakpoints.

Deeper: `../impeccable/adapt-contexts.md` covers input detection, print, email and touch checks for custom controls.
