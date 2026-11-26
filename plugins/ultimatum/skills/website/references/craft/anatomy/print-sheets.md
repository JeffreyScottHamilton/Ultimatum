# Anatomy: printable sheets from a figure

Read when a client or user asks for a handout, poster or PDF of a figure, or when a print stylesheet is planned.

Only make a sheet when asked. It reuses the figure's model, so every number and sentence on it comes from the same truth as the live figure.

## Three formats

| Format | Pages | Holds | Use for |
|---|---|---|---|
| Poster | 1 | a large title, the question, a brief intro, key figures in a column, the drawing with numbered pins, every part with one line | a wall, a cover sheet |
| Drawing | 1 | a header with a drawing number, the drawing and its pins, a parts list, a spec table, a small inset of a second pose, a strip of steps | a technical handout |
| Detailed | 2 | page 1 as the poster plus close-up circles; page 2 one large still per step with two or three sentences | a manual page or a full explainer |

All three must survive a greyscale printer: thin rules, a single sans face, small uppercase only for labels, black pins, the figure in its light theme on white.

## What a sheet spec needs

- the page to capture and the layers to freeze (back SVG to front SVG);
- the poses to show, each with the actions that reach it and how to reset;
- the figure's name, title, number, one-line question and lead;
- numbers and a spec table, from the model;
- parts, each with a name, one line, and a way to find it in the drawing;
- steps (title of five words or fewer, two or three sentences) and close-ups.

Vector parts stay vector. A WebGL layer cannot, so it is captured at 2x as a raster inside the page.

## Do it by hand

Our own route for a local business or an app needing a printable page:

1. Add a print stylesheet to the page: `@media print`, white ground, the light-theme tokens, controls hidden, the figure at full width, `break-inside: avoid` on the card.
2. Put the readout's true numbers and the parts list under the figure as plain text.
3. Print to PDF from the browser. Check page count and that hairlines stay crisp at 4x zoom.
4. Print one page on an office laser if you can; pale greys must still read.

## Check

Read every page image. Hunt for pins that point at nothing, a close-up showing the wrong part, a lit part hidden by another, and text cut at the foot. Accessibility: a PDF is a separate document; if you ship one, it needs real text, a title, a reading order and tags (https://www.w3.org/WAI/WCAG22/Techniques/pdf/). A figure that exists only as an image of a PDF fails.

Docs: https://developer.mozilla.org/en-US/docs/Web/CSS/@media/print and https://developer.mozilla.org/en-US/docs/Web/CSS/break-inside
