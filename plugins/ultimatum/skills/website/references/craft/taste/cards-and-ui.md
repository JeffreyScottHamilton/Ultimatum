# Cards, panels and interface fragments

Read when a section uses cards, or shows bits of a software product's interface inside a card.

## The card

- Keep the card itself faint: a hairline border, roomy padding, a fill a single step away from the page ground. Any colour goes in the panel inside, never on the card.
- Card fill `--card`: near-white on a light grey page, a step lighter than near-black on a dark page. No border when a photograph is the whole card.
- Border 1 px at 8–14% ink; on dark, a 5–7% top highlight. No blur shadow at rest; a hover shadow only on linked cards. Never tilted.
- Rows: 6+6, 4+4+4 or 3+3+3+3, one height per row. Edges, radii and titles line up across the row.
- Radius `--r-lg` (20 px, 18 on phone). Padding 32 px from 1024 up, 28 below, 24 on phone, never under 24. A split panel takes 48.
- Title one line at 20/18 px, weight 500. Body 16/24 in ink at about 84%, at most 46 characters per line. Muted small text only for labels.
- 32 px from the last text line to the panel; one panel height per group (`--p-h`).
- One thing moves per card group; cards never move by themselves; linked cards lift 2 px on hover.
- The panel holds a real picture (a photo, a lit ground, real UI). Never a flat gradient, a line pattern or a dot pattern on its own.

## Depth

Two box levels at most: card → panel → fragment.

- Never a patterned panel with a white card inside it, never card text inside another card, never glassmorphism.
- A card that holds UI drops its own box (`card--open`) or runs its panel flush to its edges (`panel--flush`).
- Panel variants:
  - default: aligned left and right with the text column and cropped by the card's lower edge, it takes up the bottom 60–65% of the card (`--p-h` between 264 and 340 px).
  - inset: an 8 px margin all round; inner radius = 20 − 8 = 12 (never under 6); one ratio per row (4:3 or 16:10).
  - flush: runs to the card's sides and bottom, an image band.
  - top: on top with an 8 px margin, for tall cards.
  - device: a status row on the card and the ground as the screen, radius 12.
- A 1 px inner edge sits over the ground and fragments. Optional vignette variables soften the panel corners; none on a lit ground.

```css
.card { --edge: color-mix(in oklab, transparent, var(--ink) 11%); border: 1px solid var(--edge); background: var(--card);
        border-radius: var(--r-lg); padding: 32px 32px 0; display: grid; grid-template-rows: auto 1fr; }
.panel { position: relative; height: var(--p-h, 300px); margin-top: 32px; overflow: hidden;
         border-radius: calc(var(--r-lg) - 8px) calc(var(--r-lg) - 8px) 0 0; }
.panel--inset { margin: 32px -24px 8px; border-radius: calc(var(--r-lg) - 8px); }
@media (max-width: 639px) { .card { padding: 24px 24px 0; } }
```

## Widths

- Card widths follow the grid spans (`layout-and-heroes.md`); a card is never narrower than 304 px.
- Fragments have minimum widths: from about 140 px for a single chat bubble to about 456 px for a full app window. Measure each one; if the slot is narrower, pick a smaller fragment instead of shrinking it.
- Typical slot floors: 324 px for a list or form fragment, 256 px for a control or stat.
- On phones, fragments are inset 16 px inside their panel.
- A phone mockup can overflow its panel only on a side where the panel crops it, and must stay inside the wrap.

## Interface fragments

- A fragment shows the product's own subject as its users see it: a diff under review, an invoice list, a booking calendar, a pipeline board, a terminal run. Never a generic dashboard or chat.
- Rewrite every name, number, subject and logo to the client's. Leave no "sample" or "example" note and no placeholder such as "Example Street 1".
- The product itself is shown once, large, in the app-frame (`sections.md` § App screens). Small centred fragments read as fragments.
- Live HTML at true size: 13 px text, 12 px meta, never under 11 px; weights 400 and 500; real data and real icons. Never scaled down with `transform`.
- Fragment surface: white on light, a raised near-black on dark; 1 px border at 12%; radius 12; shadow only inside the panel.
- The primary button inside a fragment is ink. Each fragment uses the accent a single time; dates and chips take tints of ink. No row of green status dots; one success mark at most.
- Real brand icons in their own colours on a light tile, glyph marks only (wordmarks are illegible at tile size), one treatment per set (`icons-and-diagrams.md`).
- Edges: every fragment edge keeps 24 px of ground around it or is cut by the panel by 24 px or more (16 on phone). Check at 1440, 1024, 768 and 390.
- Fades dissolve the last 64 px (40 on tall cards) only where an edge cuts. A fade never covers the point of the card.

```css
.stage--fade-b { -webkit-mask-image: linear-gradient(#000 calc(100% - var(--fade-h, 64px)), transparent);
                         mask-image: linear-gradient(#000 calc(100% - var(--fade-h, 64px)), transparent); }
```

## Placements

Vary placements across a group; a 2×2 uses at least three.

| Placement | Where | Good for |
|---|---|---|
| corner | 28–40 px from the panel's top-left, cut by right and bottom | windows, diffs, tables |
| rise | centred low, rising from the bottom edge | terminals, boards, short lists |
| right | against the right edge, cut by it | wide lists, timelines |
| stack | a low stack of two or three notifications | alerts, messages |
| over | a small dialog over a window fragment only | confirm, cursor menus |
| center | only for a small control (about 250×130) | a toggle, a slider |

- `fit` keeps a fragment at its true width up to a maximum (`--fit-max`); `wide` lets a fluid grid run off the right edge; `to-edge` lets a fragment reach 72 px past the bottom.
- Worked sizes: a diff review at the corner, up to 480 px (760 in a wide panel), cut at the bottom with a fade, its comment and Apply button in the top 250 px. A terminal run rising, up to 440 px (560 wide), never cut. A pipeline board rising at 420 px, or at the corner from 680 px in a large panel, with real tool marks on light tiles.

## Grounds

- Lit shader grounds behind UI are tech only, one per card group, from the page's effect family, with a new seed per panel and never the hero's own effect (`grounds-and-effects.md`). Product and service pages use a photo or a diagram on a flat panel.
- Behind UI, use soft fields: silk folds, gradient mesh, grain gradient or painterly landscape. Avoid busy dot and line fields such as Bayer dither, halftone, ridgeline, dot terrain, contour lines, ruled grounds or grid pulse.
- Panels holding UI get a ground at 3:1 or more against a dark card, or a step darker than white UI on light.
- At most one painterly panel per group; the rest use calm sand, sky or sage tones from the palette. No violet or lavender.
- Hold grounds still (speed and drift 0). A ground shows something behind something; no decorative strips under stats.
- GPU budget on laptops: render each still ground once to an image at up to 2 device pixels, one at a time, then release its WebGL context. A live ground renders at 1 device pixel only while near the viewport, and becomes a baked still when motion is reduced.
- Live contexts at once: the hero effect, one driven ground, a voice orb (dark only), a hover light, or one object. Never two of these in one group; never one WebGL context per panel; at most four on the page (`performance.md`).
- Releasing a context: https://developer.mozilla.org/en-US/docs/Web/API/WEBGL_lose_context/loseContext

Special panels (tech only): a slider that drives a ground parameter; a stat whose bars are cut out so the ground shows through; white numbers over a still canvas with `mix-blend-mode`; a voice orb (lit sphere on dark, a soft CSS pearl on light, never a dark glass ball); a real 3D object as the whole picture of a top panel, turning, never tilting (`objects.md`); a featured plan with an edge light that laps once on hover or focus.

## Loops

Tech pages only. Everything else shows its finished picture.

- One loop per card group, on the card that shows the point; the others hold still. Under 640 px every fragment is still except a voice orb.
- After the hero, a single screen never holds more than one loop.
- A loop starts on its finished picture, runs one 2.5–4 s cycle, and restarts on pointer enter or focus. A card of held fragments plays its top one while hovered.
- Changing text swaps in under 0.8 s and never drops below 4.5:1 contrast mid-change.
- Anything moving longer than 5 s gets a pause button: a 32 px disc beside the title (keeping a 44 px clear zone) or 12 px in from the panel's bottom right (WCAG 2.2.2).
- Fragment text comes from markup attributes, so the words are reviewable; a loop never invents copy. A cut tile hides its label rather than show half a word.
- Reduced motion: every loop shows its finished state and stays still.

```js
// One loop per group: play on hover/focus, pausable, still under reduced motion.
function loopCard(card, step, ms = 3200) {
  const still = matchMedia('(prefers-reduced-motion: reduce)');
  let timer = null;
  const play = () => { if (still.matches || timer) return; step(); timer = setInterval(step, ms); };
  const stop = () => { clearInterval(timer); timer = null; };
  card.addEventListener('pointerenter', play);
  card.addEventListener('focusin', play);
  card.addEventListener('pointerleave', stop);
  card.addEventListener('focusout', stop);
  const btn = card.querySelector('.pause');
  btn?.addEventListener('click', () => {
    const paused = btn.getAttribute('aria-pressed') === 'true';
    btn.setAttribute('aria-pressed', String(!paused));
    paused ? play() : stop();
  });
}
```

## Calendar

A booking calendar fragment (software only; never a calendar card on a place) shows a real month:

```js
// Build the cells of a month view: lead-in days from the previous month, then real days.
function monthCells(year, month, weekStartsMonday = true) {
  const first = new Date(year, month, 1);
  const lead = (first.getDay() + (weekStartsMonday ? 6 : 0)) % 7;
  const days = new Date(year, month + 1, 0).getDate();
  const today = new Date();
  const cells = [];
  for (let i = lead; i > 0; i--) cells.push({ day: new Date(year, month, 1 - i).getDate(), outside: true });
  for (let d = 1; d <= days; d++) cells.push({ day: d, today:
    today.getFullYear() === year && today.getMonth() === month && today.getDate() === d });
  return cells;
}
```

- Lead-in days are muted and not interactive; "today" appears only when the shown month is the current one.
- Fixed height beside its text, so the section does not jump between months.
- A real date picker in the product follows the grid pattern: https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/examples/datepicker-dialog/

## Never

A big fragment dead centre; a dialog alone with no window under it; three box levels; a pattern behind a list; a fade over the point; dark UI on a dark ground; the accent on every chip; brand colours mixed with ink icons; shiny 3D blob shapes; a loop longer than 5 s with no pause; a spinner in a still picture; cards moving with scroll; small grey 15 px card titles.
