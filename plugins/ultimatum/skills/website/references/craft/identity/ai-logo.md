# Logo ideas from an image model

Read before using an image generator for a logo. Generating costs the owner credits: ask first, and say how many images you plan.

## What the models are good and bad at

- Good: quick mood boards, symbol ideas, badge and character sketches to react to.
- Bad: exact lettering (letters come out misspelt or wobbly), consistent stroke widths, clean geometry, and anything that must scale down to 16 px.
- So: use the model for the idea, then redraw the chosen idea as a clean vector by hand (`logo.md` §3). Never ship a generated raster as the logo.

## Writing the prompt

Say, in plain words:
- the kind of mark (`logo.md` §1) and what it shows;
- flat vector style, solid shapes, no gradients, no shadows, no 3D, no photo detail;
- one or two named colours (or black only), on a plain white background;
- centred, with space around it;
- what to leave out: text (add the name later in a real typeface), extra symbols, frames, mockups.

Example: `flat vector logo symbol for a family bakery: a simple loaf shape made of three curved strokes, solid dark green on plain white, no text, no gradient, no shadow, centred with empty space around it`.

Ask for several variations, pick the best two or three, and show them to the owner as sketches, not as finished logos.

## Rights and risks

- **Copyright:** in the US, material made by an AI model without enough human creative input is not protected by copyright (US Copyright Office guidance on AI, from 2023 on). A generated mark may be copyable by anyone. Redrawing and changing it by hand adds human authorship; how much is enough is a legal question. Other countries differ.
- **Trademark** protection comes from use and registration, not authorship, so a clean, distinctive mark can still be registered. Run the search in `../../app/legal-risk.md` step 7 before the owner commits.
- **Look-alikes:** models reproduce famous marks. Never prompt with another brand's name or logo, and compare the result against well-known marks in the same trade.
- **Terms:** read the generator's terms for commercial use and ownership; note them in the launch report's licence list (`../../app/legal-risk.md` step 10).
