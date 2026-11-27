# Canvas design: posters and single-image pieces

Read when the job is one composed visual rather than an interface: a poster, a cover, an event visual, a large hero artwork, a print piece, or a set of pages that share one look. Interfaces follow the token and component guides in this folder; this file is for work judged as an image. Fonts are linked from their host or self-hosted with their licence; we never ship font files with this plugin.

## Two passes: decide the idea, then make it

Work in two separate passes, and write the first one down before drawing anything.

**Pass 1, the idea (a short paragraph and a few constraints).** State in plain words what the piece should make someone feel or understand, and pick a visual approach that serves it. Then fix three to five constraints that will hold through the whole piece, for example:

- one colour family plus a neutral, nothing else;
- a single typeface in two weights;
- a grid of 12 columns with every element snapped to it;
- one shape repeated at three scales;
- text no more than seven words.

The constraints are what make a piece look made rather than assembled. Name the approach in our own terms for the brief at hand ("a single heavy word cropped by the frame", "dense small marks that thin out toward one bright point"); do not reach for a stock style label.

**Pass 2, the making.** Build the piece inside those constraints. When something does not work, change the element, not the constraint. Change a constraint only on purpose, and write the change into the idea paragraph so the set stays consistent.

## Principles

- **The image carries the meaning.** Text is a label or a single line, not an explanation. If the piece needs a paragraph to make sense, the image is not done.
- **One focal point.** Decide where the eye lands first, second and third; make the first unmistakable by size, contrast or isolation.
- **Space is a material.** Empty areas are part of the composition; fill them only with intent.
- **System over decoration.** Repeated measures (margins, gutters, a type scale, a shape scale) make a piece feel deliberate. Effects added at the end (glows, gradients, drop shadows) usually make it feel generic; see `../../website/design-rules.md` § 2. Anti-generic lint.
- **Finish matters.** Alignment to the pixel, kerning of large type, consistent stroke weights, no accidental tangents where shapes nearly touch.

## Making it

- **Colour.** Start from the brand palette if there is one (`brand-visual.md` § Colour: roles before values), or from a single hue with its ramp. Limit the piece to what the idea needs; check text contrast even on art (4.5:1, or 3:1 for large type, WCAG 2.2 SC 1.4.3) when the piece carries information people must read.
- **Type.** Large type is image as much as text: set it tight, check its spacing by eye, and let it crop at the edge if the idea allows. Pick from the house font guide (`../hallmark/fonts.md`) and link it (for example from Google Fonts) or self-host with its licence; never embed an unlicensed font in an exported file.
- **Composition.** Pick a grid or a single dominant line first. Common structures that hold up: a strong off-centre axis, a single element at the golden or thirds point, a full-bleed field with one small counterpoint, a dense pattern broken by one gap.
- **Edges.** Keep a margin that matches the grid unless the idea is to bleed; for print, add the printer's bleed (usually 3 mm) and keep text inside the safe area.
- **Tools.** For screen pieces, HTML with CSS grid and inline SVG, or a `<canvas>` drawing script, keeps everything editable and exportable. Export PNG at 2x for screens and PDF (vector, fonts embedded only when the licence allows) for print.

## A series of pages

When the job is several pieces (a poster series, a multi-page report cover set, social tiles for one campaign):

- keep the constraints fixed and vary one thing per piece (the focal image, the colour step, the word);
- hold the same grid and the same type positions, so the set reads as one;
- lay out all the pieces side by side before finishing any one; fix the weakest first.

## Before calling it finished

1. The idea paragraph still describes what is on the page.
2. Every element obeys the constraints, or the paragraph explains the exception.
3. The focal point is the first thing a fresh viewer looks at (ask someone, or squint).
4. Nothing is there "to fill space".
5. Text is spelt right, kerned at display sizes, and readable at the size it will be seen.
6. Colours match the brand tokens where a brand exists.
7. Fonts are licensed for the use, and linked or embedded only as their licence allows.
8. The export has the right size, format, colour profile (sRGB for screens; the printer's profile for print) and bleed.

## Refining

Do at least one pass that only removes: take away one element, one colour or one effect, and keep the change if the piece holds. Then one pass that only aligns: snap every edge to the grid. Then look at it at the size it will be seen (a phone screen for social, across a room for a poster).

## Output and hand-back

Deliver the export files, the editable source, and the idea paragraph with its constraints, so the next piece in the series can follow them. Record font names, sources and licences alongside, and list any image used with its rights (`brand-assets.md` § A record per asset (when the library grows)).
