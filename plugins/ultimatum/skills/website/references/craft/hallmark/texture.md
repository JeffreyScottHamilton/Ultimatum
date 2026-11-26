# Texture: a budgeted set of print artifacts

Read only when the chosen theme names a texture, or a bespoke direction descends from print (risograph, letterpress, ticket stock, line printer). Treat texture as a budgeted treatment rather than mood. A page that feels empty needs better type and spacing, not grain.

## Budget

- Pick one family per page from grain, halftone, misregistration, scanlines and deckle. Halftone applied to a photograph belongs to that image and is not counted.
- Declare `--texture-opacity` in the tokens: 0.08 or less page-wide, 0.15 or less inside one card, 0.05 or nothing under running text. A very low-frequency wash (base frequency 0.02 or lower) may reach 0.12.
- Never animated. No drifting grain.
- Every overlay has `pointer-events: none` and `aria-hidden="true"`.
- No image requests: CSS or a data-URI SVG filter only.
- Check text contrast against the textured result instead of the flat token (WCAG 1.4.3, https://www.w3.org/TR/WCAG22/#contrast-minimum).

## Recipes

**Grain.** Speck noise from an SVG filter. The colour matrix turns noise into specks, which is why it reads at normal zoom:

```css
:root { --texture-opacity: 0.07; }
.speckled { position: relative; isolation: isolate; }
.speckled::before {
  inset: 0; position: absolute; content: "";
  opacity: var(--texture-opacity); pointer-events: none;
  background: center / 180px url("data:image/svg+xml,%3Csvg height='180' width='180' xmlns='http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg'%3E%3Cfilter id='g'%3E%3CfeTurbulence stitchTiles='stitch' baseFrequency='0.85' numOctaves='3' type='fractalNoise'/%3E%3CfeColorMatrix type='matrix' values='0 0 0 0 .12  0 0 0 0 .12  0 0 0 0 .12  0 0 0 8 -3.5'/%3E%3C/filter%3E%3Crect height='100%25' width='100%25' style='filter:url(%23g)'/%3E%3C/svg%3E");
}
```

On dark grounds make the specks light (first three matrix rows end in `1` instead of `0`).

**Halftone.** A dot screen from a radial gradient, with size and dot tokens. For plates and bands; never under type; ink or one spot colour.

```css
.dots { --pitch: 14px; background: radial-gradient(circle, var(--color-ink) 0 1.4px, transparent 1.5px) 0 0 / var(--pitch) var(--pitch); }
```

**Misregistration.** Two offset copies behind one focal word, 1–3px apart, in the theme's two spot inks. One word per page, usually in the hero; it may settle once on load and is static under reduced motion.

```css
.offset-ink { position: relative; display: inline-block; isolation: isolate; }
.offset-ink::before, .offset-ink::after {
  content: attr(data-text); white-space: nowrap; pointer-events: none;
  position: absolute; inset: 0; z-index: -1;
}
.offset-ink::before { color: var(--color-accent); translate: -2px -1px; }
.offset-ink::after {
  translate: 2px 1px; color: var(--color-accent-2, currentColor);
}
```

**Scanline.** Faint horizontal stripes fixed over the page, for arcade-like directions only. Atmosphere, never a drawn monitor frame.

```css
body::after { content: ""; position: fixed; inset: 0; pointer-events: none; background: repeating-linear-gradient(0deg, rgb(0 0 0 / .05) 0 1px, transparent 1px 3px); }
```

**Deckle.** A scalloped paper edge on one element class (ticket, stub). An artifact, never a border style for cards.

## Who earns it

Only a theme whose surfaces section names a texture may use one. Cases: riso (grain plus misregistration), halftone (dots), paste-up (fibre wash), darkroom (film grain), arcade (scanlines). Not on a modern-minimal page, never two families, never a texture the theme did not name. For a local business with warm print character (a bakery, a print shop) grain on one hero plate fits; on a clinic or law site it does not.
