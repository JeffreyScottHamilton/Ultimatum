# Craft: type, colour and surfaces as numbers

Read on every page build when setting the tokens and base styles. It gives numbers wherever a number exists. Sizes of sections and heroes are in `layout.md`; pictures in `imagery.md`; the theme supplies the material (`themes.md`).

## Type

- **Families:** two at most, a display face and a body face (one family may do both). A third is an outlier with exactly one job (a wordmark, a headline figure, code). Mono for code and measured figures counts as that one. Gates 37 and F13.
- **Weights:** three at most across the page, chosen as extremes (300 with 800, or 400 with 700). F19.
- **Scale:** a ratio of 1.25 from a 16px body, plus a wordmark size when the theme names one. Hierarchy past the scale comes from weight and colour.
- **Display:** letter-spacing -0.02 to -0.04em on a regular-width face, 0 to -0.015em on condensed or very heavy ones (touching letters are a fault). Line-height 1.0–1.15, tighter as size grows; 1.2 looks inherited. An uppercase head that can wrap never drops under 1.0 (gate 55a).
- **One head, one voice:** one weight, one style, one colour. A single word set apart by italic, colour, weight or highlight is the accented word (38i, 38iii). Stress with a line break or a second line at a second size.
- **Display size by length** (count the rendered h1): 20 characters or fewer, full display (one word may reach 7rem); 21–50, display; 51–90, the smaller display step or a split at the sense break; over 90, rewrite. A manual `<br>` goes only between phrases and is checked at 375px.
- **Poster scale** (manifesto, marquee, poster hero): `clamp(4rem, 10vw, 9rem)`, full size at 1440 and held at 1920. A wide face goes a step down.
- **Wrapping:** `text-wrap: balance` on heads, `pretty` on body (MDN: https://developer.mozilla.org/en-US/docs/Web/CSS/text-wrap). Heading measure sits on the element in `ch` (h1 about 20ch, h2 30ch, h3 40ch), never on a group wrapper.
- **Body:** 16px or more, line-height 1.5–1.65, measure 45–75ch. Never all caps, never justified without hyphenation, never tracked past 0.05em. Long prose pages: leading 1.65–1.75, measure 60–75ch.
- **Small text:** labels, captions, table heads, meta, tags, chips and nav links use the body face a step smaller, in sentence case (lower case on a lowercase-voiced theme), untracked. Mono only for code, figures, measurements, or when mono is the theme's material.
- **Required:** `font-display: swap`; a fallback of the same build (grotesk to `system-ui`, serif to Georgia); `font-synthesis: none`; load only used weights; `font-variant-numeric: tabular-nums` on figures that compare; curly quotes, a true ellipsis, a non-breaking space inside unit pairs (`10 MB`).
- **Wordmark:** may take another face; tone-rich themes should (see `fonts.md`). One family throughout only when body voice is the brand (a letter, a long document).

## Colour

- **OKLCH everywhere** (MDN: https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/oklch).
- **Four layers:** paper (light L 92–98 with chroma 0.005–0.015 toward the anchor hue; dark L 12–18, chroma 0.008–0.015); ink (L 16–24 on light, 88–96 on dark, tinted 0.005–0.014); 5–9 neutrals between, each tinted 0.005–0.018; one accent at chroma 0.12–0.22 with a paired accent-ink token. The focus colour shares the accent's hue at chroma 0.18–0.22, lightness within 5% of it.
- **No pure absolutes** as surface or improvised value (7a, 7b). Tint every grey toward the anchor.
- **The accent is a signal:** under about 5% of any viewport by default: an active nav item, a focus ring, a hover underline, the primary control, the one chart series that argues.
- **Postures,** declared in the stamp before code: Restrained (above); Committed (one colour carries 30–60% of the surface through a field or paper token, the accent stays a signal); Full palette (3–4 named roles such as field, signal, seal, ink, each with a footprint); Drenched (the surface is the colour, ink and rules derive from it). A declared surface is not accent footprint.
- **Contrast:** body 4.5:1 (aim 7:1) or APCA Lc 60; large text, icons, rings, field edges 3:1 or Lc 45 (WCAG 2.2: https://www.w3.org/TR/WCAG22/#contrast-minimum). Every rule that paints a dark surface swaps its text colour in the same rule; grey text never sits on colour. Accessibility tie-in: `../taste/accessibility.md`.
- **Bans:** gradients with more than three stops; purple-blue, purple-pink, cyan-on-dark anywhere; glow shadows on dark, halos, spotlights; alpha as a colour's definition (alpha is for overlays and shadows); red and green as the only signal.
- **Dark mode** is opt-in and derived, never inverted (`dark-mode.md`).

## Surfaces

- **A primary axis:** left-, right-, top- or bottom-weighted. Centre-biased is a default.
- **Spacing scale (px):** 2, 4, 8, 12, 16, 24, 40, 64, 96, 144 as `--space-3xs` through `--space-4xl`. A raw length where a token exists fails (24a); three optical nudges at most (24b). `gap` between siblings, `margin` only to break flow.
- **Grids:** CSS Grid for the page, Flexbox inside components. Flex children that must shrink get `min-width: 0`; icons and images `flex-shrink: 0`. No orphan on a last row (change the count). Hold column counts above 1440; cap any `vw` visual.
- **Surface ladder:** whitespace, then a 1px hairline, then a tinted well (no border), then a card (border or shadow, never both). Cards are for content that is independently interactive or a different kind. Never white cards on a tinted page, a card in a card, or a bordered box in a well. Climb different rungs at different seams. Sibling stats part with a hairline, with no leading padding on the first and no trailing on the last, reset when the column count changes.
- **Depth is weight and scale:** one shadow at most, such as `0 1px 2px oklch(20% 0.01 <hue> / 0.05)` or a 1px ring. Elevated surfaces are never darker than their canvas.
- **Z levels:** base 1, raised 10, dropdown 100, sticky 200, sticky nav 300, modal 400, toast 500, tooltip 600.
- **Clipping:** `overflow-x: clip` keeps sticky and fixed working where hidden breaks them (MDN: https://developer.mozilla.org/en-US/docs/Web/CSS/overflow). A section with deliberate overflow keeps visible.
- **Radii:** one per nesting level, concentric (inner = outer - padding, at least 2px); image radius `min(1vw, var(--radius-card))`.

## Overlap with house rules

Merged with `../../website/craft.md` §§ 2–5 (type, colour, layout, depth) and `../../website/design-rules.md` § 2 (caps, italics, gradients, glows, cards). Added here: the numeric ranges, the postures, the ladder and the z scale.
