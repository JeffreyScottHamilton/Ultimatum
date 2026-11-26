# Dark mode: a second design, not an inversion

Read only when the user asks for light and dark together, or an existing site already has a mode system. A single dark theme is not dual-mode. Never add dual-mode unprompted.

## Stance

Dark is a second, equally designed rendering of the same tokens. No `filter: invert()`, no "flip the greys". Re-derive every token, hold every contrast target in both modes, and keep each hue fixed. If a pairing fails, fix the derivation, not the target.

## Token re-derivation

| Token | Dark value |
|---|---|
| paper | lightness 12 to 18%, faint tint of the anchor hue, never `#000` |
| paper steps | each elevation level 3% lighter (light mode steps darker) |
| ink | lightness 92 to 96%, tinted, never `#fff` |
| ink-2, muted | re-space between new paper and ink; keep tints |
| rule | lightness 26 to 34%; check against paper-2 as well |
| accent | chroma down 0.02 to 0.04, lightness up 5 to 10% |
| accent-ink | re-check 4.5:1 body, 3:1 large on the new fill |
| focus | follows accent; ring 3:1 against both papers |
| hue | never moves |

Also lower body weight about 50 units (400 to 350); light on dark looks heavier.

## Emission

Light block as is, then two additions, and a toggle read before first paint:

```css
:root { color-scheme: light dark; }
[data-mode="dark"] { /* only tokens that move */ }
@media (prefers-color-scheme: dark) {
  :root:not([data-mode]) { /* same overrides for OS auto mode */ }
}
```

```html
<script>
  try { const m = localStorage.getItem("mode"); if (m) document.documentElement.dataset.mode = m; } catch {}
</script>
```

The toggle button sets `document.documentElement.dataset.mode` and stores it. The explicit attribute wins over the media query by construction. Docs: https://developer.mozilla.org/en-US/docs/Web/CSS/color-scheme

## Rules that change

- No drop shadows; elevation is lightness or an inset 1px ring. Glow is allowed only under a theme's declared atmospheric carve-out (`genres.md`).
- Cards lighter than the canvas, never darker.
- All headings in one ink colour.
- Never invert or brighten photos in CSS. Choose photos that hold on dark or seat a light one in a paper-2 well. Duotone or multiply plates need a dark pair.
- Chart marks re-derive like accents; gridlines use the dark rule colour (`data-viz.md`).

## Verify

Run contrast on every pairing in both modes (a render check sees only the default mode, so compute the dark pairs). No pure black or white in the dark block. Record `modes: light+dark` in the stamp. Screenshots in both modes with Playwright: `page.emulate_media(color_scheme="dark")`.
