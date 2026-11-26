# Page modes: classify the surface before judging a pixel

Read before applying any design rule to a page. The same rule can be right on a landing page and wrong in an admin screen, so decide the mode first and write it at the top of the audit.

## The classifier

Classify by what a visit succeeds at on this surface, never by what the company sells. A landing page for a developer tool is Persuade, while the help centre of a fashion label is Read.

| Mode | Visitor's job | Examples (ours) |
|---|---|---|
| Persuade | decide and act | landing page, pricing, campaign, a local business home page (call, book, quote) |
| Operate | finish a task | dashboard, settings, editor, checkout, sign-in, admin |
| Read | understand something | docs, article, guide, changelog, policy page |
| Experience | be inside the work | portfolio, gallery, showcase, case study |
| Hybrid | mixed | classify each section, not the page |

## Persuade rules

- The first viewport reads as one composition: brand, one headline, one supporting sentence, one call-to-action group, one image. No dashboard look.
- Order of weight: brand, then headline, then body, then action.
- Type is chosen for the brand, not left at a default stack (`slop-tells.md` § Fonts).
- Hero is full-bleed; no inset, tiled or rounded-frame hero. No cards inside the hero.
- Background has a reason: a real photo, a brand colour, a texture from the brand. No halo, spotlight, stripes or grid-paper gradient unless the brief asks.
- One job per section: one purpose, one heading, one short supporting line.
- One authored motion moment on the first screen, easing out from a state already visible; hover effects only where they carry information (`checklist-behaviour.md` § Motion and animation).
- Colour lives in CSS variables; one accent; no purple-on-white default.
- Copy is product language, not design commentary. If cutting a third of the words improves it, cut.
- Local business adds: phone, address, hours and a booking or quote action visible on the first screen at 390 wide, a tappable `tel:` link, real photos of the place or work, and proof (reviews, licences) only from the owner.

## Operate rules

- Calm surfaces, strong type, few colours, dense but readable, minimal chrome.
- Layout: main workspace, navigation, secondary context, one accent.
- Avoid mosaics of KPI cards, thick borders, decorative gradients, ornamental icons.
- Copy is utility language: where you are, what state, what action. Section headings say what the area is or what you can do there ("Plan status", "Selected rows").
- Cards only when the card is the thing you interact with.
- Auth, pricing and checkout screens add: one primary button per step, errors beside the field, visible total before paying, a way back at every step.

## Read rules

- Line length about 65 to 75 characters, one reading column, headings sit nearer the text they introduce than the text before.
- Wayfinding is part of the product: show where the reader is, what comes next and how to search.
- A docs index has no hero and no call-to-action theatre.

## Experience rules

- Let the work take over the first viewport; any surrounding chrome must justify its pixels.
- Use a single authored transition rather than a scroll-hijacked tour.
- Show the artefact whole; do not crop it to fit a template.

## Hard rejections (any one is a major finding)

1. A generic card grid as the first impression.
2. A good image with a weak brand.
3. A forceful headline with nothing to click.
4. Text laid over a busy picture.
5. Several sections repeating the same mood line.
6. A carousel with no story reason.
7. App UI built from stacked cards instead of layout.

## Seven yes/no checks

Answer each with evidence; they back findings, they are not a score.

1. Is the brand or product unmistakable on the first screen?
2. Is there one strong visual anchor?
3. Can the page be understood from its headings alone?
4. Does each section have one job?
5. Are the cards necessary?
6. Does the motion improve hierarchy or atmosphere?
7. Would it still feel premium with every decorative shadow removed?

## Reflexes no automated check catches

Check each by hand on every audit.

- **Browser surfaces are themed.** Selection colour (`::selection`), caret (`caret-color`), scrollbars, focus ring, link underline offset and tabular figures all come from the palette instead of the browser default.
- **Depth has an offset.** A shadow is offset plus soft blur. A zero-offset coloured halo is decoration.
- **Secondary text on a coloured surface is tinted from that surface's hue,** not neutral grey.
- **Headings hug the content they introduce.** The computed gap below should be smaller than the gap above.
- **Light or dark follows the use scene:** who uses it, where, under what light. One sentence. Never "dark because it is a developer tool".

## Calibration: three looks to distrust

Generated interfaces drift into one of three looks whatever the product: (1) cream paper, a sharp serif and terracotta highlights; (2) a near-black page, a single neon accent and glowing borders; (3) newspaper-style hairlines, an italic serif display face and small widely spaced monospace captions. Each is acceptable if the brief requested it. When the brief left the look open and the page ended up in one, check it: could a stranger guess the look from the category alone, or from "the category but avoiding the obvious"? If yes to either, restart the direction (`../../website/directions.md`).

## Merge note

The Persuade, Operate and Read rules extend `../../website/design-rules.md` § 3 (page kind and effect caps); that table decides how much may move, this file decides how the page is composed.
