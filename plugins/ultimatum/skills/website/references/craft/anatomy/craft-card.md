# Anatomy: framing the figure as a card

Read when placing a figure on a page or in an app and writing its surrounding text.

## Parts of the card

| Part | What it holds |
|---|---|
| Figure label | "Fig 2" and a short title in plain words |
| Hint | one line telling the reader what to do or watch |
| Readout | live true numbers, plain units, updated when state changes |
| Legend keys | the controls, named as the figure names them |
| Caption | one or two sentences saying what the figure shows |

## Rules

- The title names the idea, not the object. "How a queue forms", not "Valve manifold".
- The readout shows the model's real values. It is also text, so assistive tech can read it.
- Controls are real buttons or a labelled slider, large enough to tap (24 by 24 CSS pixels at least, WCAG 2.2 target size).
- Keep the card on the page's tokens: its radius, border and spacing, not a new style. No card nested in a card, and no decorative badge on the label (`../../website/design-rules.md` §2).
- Set a width and aspect ratio so nothing shifts when the SVG loads (`../taste/performance.md`).
- At phone width the figure scales down as a whole; the readout and legend go below it.

## Words

Write the hint and caption in the voice of the page (`../taste/voice.md`). Say what happens, not that it is "interactive".

## Light and dark

The figure's ground follows the page. On a light page the figure is ink on paper: strong edge lines, light faces. On a dark page the faces carry the light and edges soften. Do not leave a dark card on a light page unless the brand uses that on purpose.
