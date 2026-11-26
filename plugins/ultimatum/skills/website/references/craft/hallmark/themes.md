# Themes: a catalog of materials, and how to write one

Read when picking a theme for a catalog build, or when writing a new theme. The 50 catalog themes are summarised in `../../../../../data/craft/hallmark/themes.csv` (slug, genre, posture, paper band and OKLCH anchor, display class and face, accent band and hue, photo treatment, five routing words). Search it by genre, posture or routing word before inventing a look. Full theme bodies and their reference pictures are not shipped (`later.md`); write the body yourself from the header facts. Existing Ultimatum directions are in `../../website/directions.md`; prefer those for local business unless a CSV row fits better.

## Choosing

1. Name the genre (`genres.md`). 2. Filter the CSV on genre, then on routing words from the prompt. 3. Prefer variety: a second page in the same project takes a different theme unless a design file locks one (`design-file.md`). 4. Check the paper, display class and accent band against recent builds so the combination differs. 5. Write the choice in the stamp: `theme: <slug>`.

## A theme is a material

A theme describes the stuff of the page: paper, ink, typefaces, rules, corner radius, depth, texture, buttons, movement and voice. It leaves out the page's contents, order, shape and spacing, and ships no component (no signature object, no named part a page must include). Space and hero size belong to `layout.md`. Whatever the floor or craft files already govern stays out.

## Header facts

```
name, slug, genre, paper (band, lightness, hue), display (class, face),
accent (band, hue), posture, keywords (10 to 25 routing words),
material (one line, materials only), photo (treatment)
```

- Paper band: light over 85% lightness, mid 30–85, dark under 30.
- Display classes: blackletter, handwritten, pixel, mono, display-heavy, display-condensed, rounded-sans, geometric-sans, grotesk-heavy, grotesk-sans, slab-serif, high-contrast-serif, roman-serif.
- Accent bands: warm 10–60 degrees, cool 200–300, neutral under 0.05 chroma, otherwise chromatic with a name.
- Posture: restrained, committed, full-palette, drenched (`craft-type-colour.md`).
- Photo treatment: natural, warm, muted, mono, duotone (two token names) or tint, optionally with contrast, saturation, exposure and sepia values. Match what the material itself would do to a photo.

## Body, 3–8 KB, in order

1. One paragraph: the feel and what it is not; describe the register, not brand names.
2. Tokens: a `:root` block of real OKLCH values (paper steps, ink steps, muted, rule, accent, accent-ink, focus, three font tokens, radii, hairline, card shadow, display tracking and weight), no comments inside.
3. Type: typefaces, weights, tracking, case and leading, with sizes from the shared scale. Labels use the body face one step down in sentence case without tracking, and never mono unless mono is the material. Headings keep a single weight and colour.
4. Surfaces: 4–6 bullets on rules, radius, depth, bands, photographs, texture budget (`texture.md`).
5. Range: 3–4 bullets about what the material can produce without a photograph, expressed as treatments of shared compositions (`layout.md`) and not as required components or section order.
6. Controls: the pair of buttons, links, inputs and the places the accent is allowed.
7. Motion: 1–3 lines (`microinteractions.md` character).
8. Voice: 1–2 lines.
9. Do-nots: 3–5, specific to this theme's failure modes.
10. Build hint: up to 20 lines of CSS, tokens only.

## A theme may not carry

Components or objects, section order or an outline, required nav, footer, hero or imagery, ready-made HTML or class names, rules on space and density, fixed copy, made-up brands or people, eyebrows, labels in tracked capitals, badges with no fact behind them, comparison tables against other themes, and lists of reference sites.

## Contradictions to avoid

Watch for cream paper under a high-contrast serif with a terracotta accent, mono labels where mono is not the material, labels in tracked caps, a single coloured word inside a heading, strings split by middle dots, arrow suffixes, italic display text used as decoration, and glows on dark themes. A theme that truly wants one states it as part of its material and names the waived gate once.

## Validation (by hand)

The source validates with a Node script, which Ultimatum does not run (`later.md`). Check by hand: header facts complete, body 3–8 KB, tokens only (no raw milliseconds, bare `ease`, named colours or raw spacing in the build hint), no forbidden content above, contrast gates pass (`craft-type-colour.md`).
