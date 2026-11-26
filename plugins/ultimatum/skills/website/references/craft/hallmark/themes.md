# Themes: a catalog of materials, and how to write one

Read when picking a theme for a catalog build, or when writing a new theme. The 50 catalog themes are summarised in `../../../../../data/craft/hallmark/themes.csv` (slug, genre, posture, paper band and OKLCH anchor, display class and face, accent band and hue, photo treatment, five routing words). Search it by genre, posture or routing word before inventing a look. Full theme bodies and their reference pictures are not shipped (`later.md`); write the body yourself from the header facts. Existing Ultimatum directions are in `../../website/directions.md`; prefer those for local business unless a CSV row fits better.

## Choosing

1. Name the genre (`genres.md`). 2. Filter the CSV on genre, then on routing words from the prompt. 3. Prefer variety: a second page in the same project takes a different theme unless a design file locks one (`design-file.md`). 4. Check the paper, display class and accent band against recent builds so the combination differs. 5. Write the choice in the stamp: `theme: <slug>`.

## A theme is a material

It says what a page is made of: paper, ink, faces, rules, radius, depth, texture, controls, motion, voice. It leaves out the page's contents, order, shape and spacing, and ships no component (no signature object, no named part a page must include). Space and hero size belong to `layout.md`. Anything the floor or craft files already bind is left out.

## Header facts

```
name, slug, genre, paper (band, lightness, hue), display (class, face),
accent (band, hue), posture, keywords (10 to 25 routing words),
material (one line, materials only), photo (treatment)
```

- Paper band: light over 85% lightness, mid 30 to 85, dark under 30.
- Display classes: roman-serif, high-contrast-serif, slab-serif, grotesk-sans, grotesk-heavy, geometric-sans, rounded-sans, display-condensed, display-heavy, mono, pixel, handwritten, blackletter.
- Accent bands: warm 10 to 60 degrees, cool 200 to 300, neutral under 0.05 chroma, otherwise chromatic with a name.
- Posture: restrained, committed, full-palette, drenched (`craft-type-colour.md`).
- Photo treatment: natural, warm, muted, mono, duotone (two token names) or tint, with optional contrast, saturation, exposure and sepia numbers. Choose what the material would do to a photograph.

## Body, 3 to 8 KB, in order

1. One paragraph: the feel and what it is not; describe the register, not brand names.
2. Tokens: a `:root` block of real OKLCH values (paper steps, ink steps, muted, rule, accent, accent-ink, focus, three font tokens, radii, hairline, card shadow, display tracking and weight), no comments inside.
3. Type: faces, weights, tracking, case, leading; sizes come from the shared scale. Labels are the body face a step smaller, sentence case, untracked; never mono unless mono is the material. A head is one weight and one colour.
4. Surfaces: four to six bullets on rules, radius, depth, bands, photographs, texture budget (`texture.md`).
5. Range: three or four bullets on what the material makes without a photograph, as treatments of shared compositions (`layout.md`), never a mandated component or section order.
6. Controls: the button pair, links, inputs, where the accent may sit.
7. Motion: one to three lines (`microinteractions.md` character).
8. Voice: one or two lines.
9. Do-nots: three to five, specific to this theme's failure modes.
10. Build hint: at most 20 lines of CSS using only tokens.

## A theme may not carry

A component or object; a section sequence or page outline; a mandated nav, footer, hero or imagery; scaffold HTML or class names; space and density rules; verbatim copy; invented brands or people; an eyebrow; tracked-caps labels; a badge that carries no fact; neighbour comparison tables; reference-site lists.

## Contradictions to avoid

Cream paper with a high-contrast serif and a terracotta accent; mono labels on a non-mono theme; tracked-caps labels; one coloured word in a head; middle-dot strings and arrow suffixes; italic display as a flourish; glow on dark themes. A theme that wants one declares it as its material and names the waived gate once.

## Validation (by hand)

The source validates with a Node script, which Ultimatum does not run (`later.md`). Check by hand: header facts complete, body 3 to 8 KB, tokens only (no raw milliseconds, bare `ease`, named colours or raw spacing in the build hint), no forbidden content above, contrast gates pass (`craft-type-colour.md`).
