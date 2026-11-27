# Layout, screens and heroes

Read when planning section heights, placing things on the grid, or choosing and building the hero.

## Screens

Why: recordings of large product-company sites show a hero that fills the first screen and sections of roughly half a screen to just over one, separated by about a quarter screen of space. A study the source ran over 327 company sites at 1440×900 and 390×844 found the hero stands alone on the first screen on most of them (78%), and that a section is far more likely to be seen alone when it is close to one screen tall and has a wide gap above it. We turn that into a hard rule because it is easy to check.

- Every section is exactly one screen or two screens tall. Nothing in between, nothing taller (one exception below).
- A screenshot taken at `scrollY = k × viewport height` shows exactly one section, hero included. Keep `scroll-padding-top: 0` and `scroll-behavior: auto` so anchor links land on those boundaries.
- Shell: `header.nav`, then `main`, then `footer.closing`, plus the phone action bar below 640 px, and nothing else. No pop-ups, modals on load, chat bubbles, badges or back-to-top buttons.
- Section box: `height: calc(var(--screens, 1) * 100svh)` where `--screens` is 1 or 2. Under 640 px use `100lvh` and a separate `--screens-phone` so a phone can take two screens where desktop takes one. Never `min-height` alone, never `dvh` (it jumps as the address bar moves), never a third screen.
- Exception: a photo-chapter moment (`moments-and-scenes.md`) may run three or four screens, with `position: sticky` only inside its own box. Nothing else on the page is sticky except the header.

```html
<section id="menu" class="sec" style="--screens:2">
  <div class="wrap">
    <h2>Menu</h2>
    <!-- content -->
  </div>
</section>
<style>
  .sec {
    overflow: clip;
    block-size: calc(var(--screens, 1) * 100svh);
    padding-block: var(--pad-top) calc(var(--pad-bottom) + var(--bar));
  }
  @media (max-width: 639px) {
    .sec { block-size: calc(var(--screens-phone, var(--screens, 1)) * 100lvh); }
  }
</style>
```

Viewport units: https://developer.mozilla.org/en-US/docs/Web/CSS/length#relative_length_units_based_on_viewport

### Fitting content into one or two screens

Measure the content height `c` (heading plus everything under it) at 1440×900 with the tokens from `system.md`:

| `c` at 1440×900 | Screens | Do |
|---|---|---|
| under 360 px | — | too thin: merge with a neighbour or add a picture |
| 360–708 | 1 | fine |
| 708–780 | — | no legal height: cut or add up to 72 px |
| 780–1,320 | 2 | split into two rows (below) |
| 1,320–1,608 | 2 | cut copy or tighten the grid |
| over 1,608 | — | two sections |

- Phones (390 wide): one screen holds roughly 464–700 px of content minus the action bar; two hold about 1,268–1,544. Otherwise cut words or give the phone two screens with `--hm: 2`.
- Tablets (640–1023, judged at 768×1024 and 820×1180): an oversized section pushes every later one off its screen line. Up to about 832 px is one screen; 832–1,130 cut to one; 1,130–1,856 set two screens with a page rule for that width.
- A two-screen section splits into two rows of up to 708 px each: row one is the heading and the first group, row two the rest. It never gets a second `h2`.
- Content is top-aligned: the `h2` sits `--pad-top` below the section's top. Never vertically centred.
- Fill: content covers at least 55% of the box. Short blocks merge or gain a picture; no thin strip sections.
- Space or a new ground marks where one section ends; rules, shadows and hairlines inside the section never do. A list may end each row with a 1 px rule inside the content edges.
- No scroll tricks: no `scroll-snap`, no scroll-jacking, no smooth-scroll library. The only scroll-driven pieces are the tech big scene and dealt scroll moments, each in its own section.

## Picking a hero

- The hero is exactly the first screen: `100svh`, header laid over it, and its content ends by y 836 at 1440×900. Check at 390, 768, 820, 1024, 1280 and 1440: the following section must not peek in at any of them.
- Structure: `.wrap > .hero-text` holding an optional notice line, the `h1`, one lead paragraph, at most two buttons, and the picture. No caption, no second floating card, no third button style.
- The `h1` starts at y 120 (96 on phone), runs three lines at most at every width and is never smaller than the `h2` size. A notice line, if any, sits 16 px above it at 14 px.
- The picture ends inside the hero: beside the words, behind them as a layer, or above/below only when everything still ends 24 px above the fold.
- At 768 and 820 the hero stacks. Its bottom edge lands on a whole element or a deliberate bleed with a fade of at least 96 px, never a card sliced by the fold.
- Hero pictures are the work itself: the product, the place, the app, the client's work. Never a colour field or mood image.
- Phone: text first; a photo above it only if the hero still ends 24 px above the bar. Buttons stack unless both fit one line.
- Never: a loader, a gate before the page, an entrance during which the words are hidden, or products that slide or crossfade in turn.
- Heroes are dealt by site kind and by what material exists (photos, UI, film, object, setting), never by taste, and not repeated within three pages. The place hero is fixed, never dealt.
- Games always show their world (key art, film or a stand-in setting photograph); never the statement or word hero.
- Product and hardware pages may only use heroes that show the product at about 80% of content width (product, photo or film hero).
- A docked strip under the hero (software and product only): at most 96 px, still, one row (logos used with permission, a rating line, or three facts). Hidden on phone unless it fits.

## Hero catalogue

Column numbers refer to the 1440 grid below. Phone notes in brackets.

| Hero | Layout | Kinds | Motion |
|---|---|---|---|
| Split | text span 5; picture span 6 from column 7, top aligned with the `h1`; one opaque detail card lower left [text, then picture about 240 px] | all but place | entrance only |
| Photo | full-bleed photo layer; words on its calm dark side over six columns, `h1` about 80 px on two lines; four facts at the foot [photo cropped to top, words below] | product, service | none |
| Product | `h1` across columns 1–7 on two lines, lead and buttons on 9–12; the product large across the wrap down to the fold | product, hardware | entrance only |
| Editorial | the headline is the picture: about 156 px on three lines, with one or two small photos set into the line [56 px on four lines] | service, product | photos open once on load |
| Collage | words on 5 columns; on 6 columns a lit frame whose lower edge crops the app window, one loop card [window alone] | software, tech | one loop card |
| Word | oversized `h1` (about 144 px, two lines) with one live word underlined last; lead and buttons span 6; facts span 5 from column 8 [54 px, three lines] | tech only | one word |
| Film | a cinema frame on the lines with the poster still; white `h1` on a calm area; a play disc plays it on click [frame then words] | tech, games | plays on click only |
| Statement | one calm two-line sentence (about 56 px) on the page ground with lead, buttons and four facts [34 px] | service, software | none |
| Triptych | a ~52 px `h1` across 3 columns; from column 4, six columns hold 3–5 pieces as a collage, rotating to the next set after 2.8 s; a single big button [collage 342 wide] | product, tech | swap, with pause |
| Centred | a small notice, a ~72 px centred `h1`, the lead and two buttons; below, a wrap-wide lit frame whose app window fades away across its bottom 18% | software | none |

Every hero: one screen, on the edge lines, one `h1` within its character budget, at most one motion, and still under reduced motion and on phone.

A hero fails when: the picture runs to one viewport edge but not the other, the hero is taller than the screen, the visual sits above the text on phone, words sit on a busy picture, there is a second floating card, the `h1` is a slogan, or there is a caption under the picture.

## Place hero

Cafés, restaurants, shops, studios, salons, clinics and workshops.

- One still, full-bleed daylight photograph of this place under the header: the room from the door, the counter, the shopfront with customers, the workshop, the best room. No words on it, no scrim, gradient, fade or box. Never mood shots, scenery, cut-outs or hazy files.
- The words sit on the page ground below the photo. It enters once on load (`motion.md`).
- At 1440: photo 480 px tall with a 40 px gap; `h1` 48/53 across columns 1–6 at about y 592, three lines at most; a 20/30 sub-line from the split line; one button.
- Shops and bookshops may use a letterbox instead: 1200×504 inside the column, 24 px under the header.
- 640–1023: photo at most `56vw` tall, words stacked below, hero ends 24 px above the fold.
- 390: photo at least 390×292 (up to 390×488 when the photo should fill more), 24 px gap, `h1` 32/37 on three lines at most, sub-line 18/28, one 342×48 button.
- The visit block (address, hours, directions) is always screen two, never squeezed into the first screen.

## Grid

One wrap for header, sections and footer: `width: min(100% - 2 × gutter, 1280px)`.

| Frame | Wrap | Column, gap | Column n starts at | n columns span |
|---|---|---|---|---|
| 1440 standard | 1280, from x 80 to 1360 | 84.67, 24 | 80 + 108.67 (n − 1) | 108.67 n − 24 (span 3 is 302, span 6 is 628) |
| 1440 place | 1200, from x 120 to 1320 | 78, 24 | 120 + 102 (n − 1) | 102 n − 24 (span 3 is 282, span 6 is 588) |
| 390 phone | 342, from x 24 to 366 | 165, 12 (two tiles) or the full 342 | — | — |

Round each result to the nearest pixel.

Check the numbers in the browser rather than trusting the table:

```js
// Print the left x of each column of the first .grid on the page.
const g = document.querySelector('.grid');
const cols = getComputedStyle(g).gridTemplateColumns.split(' ').filter(t => !t.startsWith('[')).map(parseFloat);
const gap = parseFloat(getComputedStyle(g).columnGap);
let x = g.getBoundingClientRect().left;
console.log(cols.map(w => { const s = Math.round(x); x += w + gap; return s; }));
```

- Blocks start on the left edge or a column start; blocks that reach the right end on a column end. A block more than half the wrap wide is made full-wrap.
- Every card in a row is the same height, whether the row splits 6+6, 4+4+4 or 3+3+3+3.
- Two text lines only: the left edge and one split line (the start of column 6, 7 or 8 — x 623, 732 or 841; a place page always splits 6/6, at x 732). Choose the split before building. Centred text moves to the left line except in the centred hero.
- Splits: text left, visual right, top-aligned. Never mirrored, never alternating left/right down the page. The `h2` sits above the split on the left line. Filled columns get 48 px inner padding. Phone: text then visual, both 342 wide.
- Pictures either span the viewport as a layer or start and end on column lines. Each row picks a single ratio from 1:1, 3:2, 4:3 and 4:5. None taller than 708 px outside the hero.
- Bleeds are for layers only: an `img` marked `aria-hidden="true"` (or with a proper `alt` if it carries meaning) covering 90% or more of its section. A cut window stays inside its frame. A picture wall runs edge line to edge line with 0–2 px gaps.
- No element straddles two sections, gets clipped by mistake, steps out of line or pokes in from the side. No dead space beside short text.
- 1024–1279: span-4 cards with panels go two-up. 640–1023: splits stack text first and panel cards take the full row. Nothing scrolls sideways; no swipe rows.

## Type sizes

`system.md` holds the scale. Layout-specific points:

- Use a single family, or two (display and text) each kept to its own job; a third face is never allowed, and four font files is the ceiling.
- Display weight: 500 for tech kinds, 400 for place, service and product. Tracking tightened by about 0.5–4.5% at 40 px and above. Text 400 and 500 only. No light weights under 20 px.
- Place type sizes, as size/line height in px:

  | Role | Desktop | Phone |
  |---|---|---|
  | `h1` | 48/53 | 32/37 |
  | `h2` | 32/40 | 24/30 |
  | names | 20/28 | 18/26 |
  | sub-line | 20/30 | 18/28 |
  | body, small, labels | 16/26, 14/20, 13/16 | same |
- Each level at least 1.3× the next from 1024 up (1.2× below).
- Any text at 40 px or above that is not inside a grid item is a heading and must be marked up as one; a free-floating line at `h2` size is an error. The footer wordmark may be larger.
- Font loading: self-host or use the provider's CSS with `font-display: swap` and preload only the hero face. https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/font-display

## Checks

Run in the browser at 1440×900, 1024×768, 820×1180, 768×1024 and 390×844. Every finding fails the page.

| Finding | Means |
|---|---|
| hero-fold | hero content passes y = viewport height − 64, or the next section shows |
| hero-lines | `h1` over three lines or over its character budget |
| screen-height | a section is not exactly 1 or 2 screens |
| sparse | content fills under 55% of its box |
| neighbour | two adjacent sections share the same ground and layout |
| edge | a block starts or ends off the edge lines or column lines |
| overflow | anything scrolls sideways |
| ratio | mixed picture ratios in one row, or a picture taller than 708 px |

A small in-page script can collect the section heights and compare them to the viewport:

```js
const vh = innerHeight;
for (const s of document.querySelectorAll('main > section')) {
  const k = s.getBoundingClientRect().height / vh;
  if (Math.abs(k - Math.round(k)) > 0.01 || k < 0.99 || k > 2.01) console.warn('screen-height', s.id, k.toFixed(2));
}
if (document.documentElement.scrollWidth > innerWidth) console.warn('overflow');
```
