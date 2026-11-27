# Craft: type, colour and surfaces as numbers

Read on every page build when setting the tokens and base styles. It gives numbers wherever a number exists. Sizes of sections and heroes are in `layout.md`; pictures in `imagery.md`; the theme supplies the material (`themes.md`).

## Type

- **Families:** no more than two: one for display and one for body, or a single family doing both. A third is an outlier and gets exactly one job (wordmark, headline figure or code); a mono face for code and measured figures takes that slot. Gates 37 and F13.
- **Weights:** three at most across the page, chosen as extremes (300 with 800, or 400 with 700). F19.
- **Scale:** a 1.25 ratio starting from a 16px body, with an extra wordmark size when the theme specifies one. Hierarchy past the scale comes from weight and colour.
- **Display:** tracking of -0.02em to -0.04em on regular-width faces, and 0 to -0.015em on condensed or very heavy ones (letters that touch are a fault). Line-height 1.0–1.15, tighter as size grows; 1.2 looks inherited. An uppercase head that can wrap never drops under 1.0 (gate 55a).
- **One head, one voice:** one weight, one style, one colour. Marking a lone word by italics, colour, extra weight or highlight is the accent tic (38i, 38iii). To stress something, break the line or drop a second line at a different size.
- **Display size follows length** (count characters in the rendered h1): up to 20 gets full display size (a single word may reach 7rem); 21–50 gets display; 51–90 drops a step or splits where the sense breaks; above 90, rewrite it. Insert a manual `<br>` only between phrases and test it at 375px.
- **Poster scale** (manifesto, marquee, poster hero): `clamp(4rem, 10vw, 9rem)`, reaching full size at 1440 and staying there at 1920. A wide face goes a step down.
- **Wrapping:** `text-wrap: balance` on heads, `pretty` on body (MDN: https://developer.mozilla.org/en-US/docs/Web/CSS/text-wrap). Heading measure sits on the element in `ch` (h1 about 20ch, h2 30ch, h3 40ch), never on a group wrapper.
- **Body:** 16px or more, line-height 1.5–1.65, measure 45–75ch. Never all caps, never justified without hyphenation, never tracked past 0.05em. Long prose pages: leading 1.65–1.75, measure 60–75ch.
- **Small text:** labels, captions, table heads, meta, tags, chips and nav links use the body face a step smaller, in sentence case (lower case on a lowercase-voiced theme), untracked. Mono only for code, figures, measurements, or when mono is the theme's material.
- **Required:** `font-display: swap`; a fallback with the same build (grotesk falls back to `system-ui`, serif to Georgia); `font-synthesis: none`; load only the weights in use; `font-variant-numeric: tabular-nums` for figures compared side by side; typographic quotes, a real ellipsis character, and a non-breaking space between a number and its unit (`10 MB`).
- **Wordmark:** may take another face; tone-rich themes should (see `fonts.md`). A single family throughout suits pages where the reading voice is the brand (a letter, a long document).

## Colour

- **OKLCH everywhere** (MDN: https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/oklch).
- **Four layers:** paper (light: L 92–98, chroma 0.005–0.015, leaning to the anchor hue; dark: L 12–18, chroma 0.008–0.015); ink (L 16–24 on light, 88–96 on dark, tinted 0.005–0.014); 5–9 neutrals between, each tinted 0.005–0.018; one accent at chroma 0.12–0.22 with a paired accent-ink token. The focus colour shares the accent's hue at chroma 0.18–0.22, lightness within 5% of it.
- **No pure absolutes** as surface or improvised value (7a, 7b). Every grey takes a slight tint from the anchor hue.
- **The accent is a signal:** by default it covers under roughly 5% of any viewport. Typical uses: the active nav item, the focus ring, a hover underline, the primary control, and the one chart series that makes the argument.
- **Postures** are declared in the stamp before any code. Restrained is the one above. Committed: one colour holds 30–60% of the surface through a field or paper token while the accent stays a signal. Full palette: 3–4 named roles, each given a stated footprint (field, signal, seal and ink are typical). Drenched: the surface itself is the colour, and ink and rules derive from it. A surface you declared does not count toward the accent footprint.
- **Contrast:** body text 4.5:1 (7:1 is better) or APCA Lc 60; use 3:1 or Lc 45 for large text, icons, rings and field edges (WCAG 2.2: https://www.w3.org/TR/WCAG22/#contrast-minimum). Any rule that paints a dark surface must switch its text colour in that same rule, and never put grey text on a coloured surface. Accessibility tie-in: `../taste/accessibility.md`.
- **Bans:** gradients with more than three stops; purple-blue, purple-pink, cyan-on-dark anywhere; glow shadows on dark, halos, spotlights; defining a colour through alpha (alpha is reserved for overlays and shadows); red versus green as the sole signal.
- **Dark mode** must be requested, and is derived from the palette rather than inverted (`dark-mode.md`).

## Surfaces

- **A primary axis:** left-, right-, top- or bottom-heavy. A centre bias is the default to avoid.
- **Spacing scale (px):** 144, 96, 64, 40, 24, 16, 12, 8, 4 and 2 as the tokens `--space-4xl` down to `--space-3xs`. A raw length used where a token exists fails (24a), and optical nudges are capped at three (24b). `gap` between siblings, `margin` only to break flow.
- **Grids:** use CSS Grid for page structure and Flexbox within components. Give shrinkable flex children `min-width: 0` and icons and images `flex-shrink: 0`. Avoid a lone item on the last row by changing the count. Hold column counts above 1440; cap any `vw` visual.
- **Surface ladder:** whitespace, then a 1px hairline, then a tinted well (no border), then a card (border or shadow, never both). Cards suit content that stands alone as interactive, or that is a different kind of thing. Do not put white cards on a tinted page, nest a card in a card, or put a bordered box in a well. Use a different rung at each seam. Sibling stats divide with a hairline, no leading padding on the first and no trailing padding on the last, recalculated when the column count changes.
- **Depth comes from weight and scale.** Allow one shadow at most, for instance a 2px blur at 5% of a hue-tinted `oklch(20% 0.01 <hue>)`; otherwise use a 1px ring. A raised surface is never darker than the canvas behind it.
- **Z levels**: tooltip 600, toast 500, modal 400, sticky nav 300, sticky 200, dropdown 100, raised 10, base 1. One number per layer.
- **Clipping:** prefer `overflow-x: clip`, because `hidden` breaks sticky and fixed positioning, which clip leaves working (MDN: https://developer.mozilla.org/en-US/docs/Web/CSS/overflow). A section with deliberate overflow keeps visible.
- **Radii:** one per nesting depth and concentric (inner radius is outer minus padding, floor 2px); image radius `min(1vw, var(--radius-card))`.

## Overlap with house rules

Merged with `../../website/craft.md` §§ 2–5 (type, colour, layout, depth) and `../../website/design-rules.md` § 2 (caps, italics, gradients, glows, cards). Added here: the numeric ranges, the postures, the ladder and the z scale.
