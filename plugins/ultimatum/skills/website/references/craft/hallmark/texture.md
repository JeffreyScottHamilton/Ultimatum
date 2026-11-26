# Texture: a budgeted set of print artifacts

Read only when the chosen theme names a texture or a custom direction comes from print (risograph, letterpress, ticket stock, line printer). Texture is a treatment with a budget, never ambience. Flat pages that feel empty need better type and spacing, not grain.

## Budget

- One artifact family per page: grain, halftone, misregistration, scanline or deckle. A photo's own halftone belongs to the image and does not count.
- Declare `--texture-opacity` in the tokens: 0.08 or less page-wide, 0.15 or less inside one card, 0.05 or nothing under running text. A very low-frequency wash (base frequency 0.02 or lower) may reach 0.12.
- Never animated. No drifting grain.
- Every overlay has `pointer-events: none` and `aria-hidden="true"`.
- No image requests: CSS or a data-URI SVG filter only.
- Measure text contrast on the textured result, not the flat token (WCAG 1.4.3, https://www.w3.org/TR/WCAG22/#contrast-minimum).

## Recipes

**Grain.** Speck noise from an SVG filter. The colour matrix turns noise into specks, which is why it reads at normal zoom:

```css
:root { --texture-opacity: 0.08; }
.grained { position: relative; isolation: isolate; }
.grained::after {
  content: ""; position: absolute; inset: 0; pointer-events: none;
  background-size: 200px 200px; opacity: var(--texture-opacity);
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg' width='200' height='200'%3E%3Cfilter id='g'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 9 -4'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23g)'/%3E%3C/svg%3E");
}
```

On dark grounds make the specks light (first three matrix rows end in `1` instead of `0`).

**Halftone.** A dot screen from a radial gradient, with size and dot tokens. For plates and bands; never under type; ink or one spot colour.

```css
.halftone { background-image: radial-gradient(var(--color-ink) 1.5px, transparent 1.5px); background-size: 12px 12px; }
```

**Misregistration.** Two offset copies behind one focal word, 1 to 3px apart, in the theme's two spot inks. One word per page, usually in the hero; it may settle once on load and is static under reduced motion.

```css
.misreg { position: relative; display: inline-block; isolation: isolate; }
.misreg::before, .misreg::after { content: attr(data-text); position: absolute; inset: 0; z-index: -1; pointer-events: none; white-space: nowrap; }
.misreg::before { color: var(--color-accent); transform: translate(-2px, -2px); }
.misreg::after { color: var(--color-accent-2, var(--color-focus)); transform: translate(2px, 2px); }
```

**Scanline.** Faint horizontal stripes fixed over the page, for arcade-like directions only. Atmosphere, never a drawn monitor frame.

```css
body::after { content: ""; position: fixed; inset: 0; pointer-events: none; background: repeating-linear-gradient(transparent 0 2px, rgb(0 0 0 / .06) 2px 3px); }
```

**Deckle.** A scalloped paper edge on one element class (ticket, stub). An artifact, never a border style for cards.

## Who earns it

A theme earns texture when its surfaces section names one. Examples: riso (grain plus misregistration), halftone (dots), paste-up (fibre wash), darkroom (film grain), arcade (scanlines). Never on a modern-minimal page, never two families, never a texture the theme did not name. For a local business with warm print character (a bakery, a print shop) grain on one hero plate fits; on a clinic or law site it does not.
