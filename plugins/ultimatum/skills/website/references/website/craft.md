# Craft: making a direction look designed

Read while building each direction (step 2 of the guide) and again before the build. `design-rules.md` says what to remove; this file says what to put in its place.

For the full craft layer (page plans, heroes, sections, motion, grounds, quality gate), read `../craft/taste/index.md`. This file's rules still win on any conflict.
For floor and gate checks, page shapes, hero postures and themes, read `../craft/hallmark/index.md`.
For design audits, plan reviews and QA runs, read `../craft/design-review-qa/index.md`.
For motion on product UI (timing, springs, gestures, review, mobile web), read `../craft/emil-motion/index.md`.
For explanatory isometric figures (how a product or process works), read `../craft/anatomy/index.md`.
For audits with a score, critique, hardening, interface copy, refine moves, adapting to other contexts and native iOS or Android rules, read `../craft/impeccable/index.md`.
For a logo, favicons, app icons and a small identity kit (cards, signs, social images), read `../craft/identity/index.md`.
For what a landing page, a developer-product landing or a settings area must contain and in what order, read `../craft/pages/index.md`.
For a slide deck (pitch, sales, launch, update or talk), read `../craft/decks/index.md`.

## 1. Pick an extreme, then commit

Before any code, name the direction's tone in two or three words, and make them a real position, not "clean and modern". Some starting points to push from:

| Tone | What it looks like |
|---|---|
| Stark minimal | one typeface, huge sizes, lots of empty space, almost no colour |
| Rich maximal | layered images, many type sizes, dense grids, strong colour |
| Editorial | magazine grid, big serif headlines, captions, pull quotes |
| Raw / utilitarian | monospace, visible grid lines, plain borders, no rounding |
| Playful | bold colour, rounded shapes, bouncy motion, hand-drawn touches |
| Luxury / quiet | fine serif, wide letter spacing, muted palette, slow motion |
| Retro / period | the type, colour and texture of one named decade or medium |
| Industrial | heavy sans, numbers as graphics, hazard-like accents, hard edges |

Halfway between two tones reads as no tone. A quiet site done with care beats a loud one done loosely; what matters is that every choice points the same way.

## 2. Type does most of the work

- Pair a **display face with character** for headlines and a **plain, readable face** for body. Write both names and the reason at the top of the file.
- Avoid the faces every generated page reaches for (Inter, Roboto, Arial, Open Sans, the system stack) as the display face, and do not reuse the same display face across the three directions or from one project to the next by habit.
- Use a real scale: at least three clear steps, with the largest step big enough to be a shape on the page, not just a heading.
- Tune it: tighter letter spacing on big headings, looser on small caps labels, line length 55–75 characters for body text.
- Load only the weights you use, with `font-display: swap`. Licence check for any paid face (`../shared/licenses.md`).

## 3. Colour as a system

- Define every colour once as a CSS variable (`--bg`, `--ink`, `--muted`, `--accent`, `--line`) and use only those.
- One colour owns most of the page; one sharp accent is kept for the main action and a few key moments. Even spreads of four colours look timid.
- Choose light or dark on purpose for the tone; if both are offered, design both, not an inverted copy.
- Check text contrast at WCAG AA on every background it sits on.

## 4. Layout with intent

- Decide where the eye lands first, second and third on each screen, and size things in that order.
- Break the grid on purpose in one or two places: an image bleeding off the edge, a headline overlapping a photo, an off-centre column. Everything else stays aligned so the break reads as a choice.
- Choose generous space or tight density for the tone, and keep it consistent. Equal padding everywhere is the generic middle.
- Vary section shapes down the page so it does not become a stack of same-height bands.

## 5. Surface and depth

A flat solid background is fine for minimal tones; otherwise give the page some material that fits the tone: fine grain or noise, a subtle pattern from the brand, layered transparent shapes, hard offset shadows, thin rules, a paper or print texture. Keep it quiet behind text. Blob and aurora gradients stay banned (`design-rules.md`).

## 6. Motion: one moment over many twitches

- Spend the motion budget on one designed moment, usually the first screen: a staggered reveal of headline, image and action with set delays, so the page arrives rather than flickers.
- Then add only motion that answers the visitor: hover, focus, press, scroll progress. Small, quick, the same easing everywhere (the direction's motion personality in `directions.md`).
- Prefer CSS for simple moves; use GSAP only where the feel bar asks for scroll scenes or sequencing. Always honour `prefers-reduced-motion`.

## 7. Effort matches the idea

A maximal direction needs the code to carry it: layers, real images, detailed states. A minimal one needs precision instead: exact spacing, perfect alignment, careful type. Either way, finish the details a visitor touches: hover and focus states, empty and error states, the footer, the 375 px view.

## 8. Before you hand it to the critic

- Read the top comment back: tone, type pair, palette variables, motion personality. Does the page actually do all four?
- Could this page belong to a different business by swapping the logo? If yes, add something only this one has: its product, place, number or words.
- Then run the lint in `design-rules.md` and screenshot.
