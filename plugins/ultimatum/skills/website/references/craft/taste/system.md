# Page system: tokens, type, colour, buttons, head

Read when setting up the stylesheet for a new page, before any section is built.

## One system

- A page has exactly one set of: grid, spacing scale, type scale, radius family, button pair, card recipe, hairline and link style. A second version of any of these is a bug, not a variant.
- Put all of it in one `:root` block plus a few base rules. Sections use the tokens; they never invent a new size.
- When a section seems to need a new value, change the token or drop the idea.

## Reset

Measured layout drifts when the browser's default margins survive. Start every page with a small reset and a viewport that reaches behind phone notches:

```html
<meta name="viewport" content="viewport-fit=cover, initial-scale=1, width=device-width">
<style>
  html { text-size-adjust: 100%; -webkit-text-size-adjust: 100%; }
  :where(*, *::before, *::after) { box-sizing: border-box; }
  :where(body, p, figure, blockquote, h1, h2, h3, h4, dl, dd, ul, ol) { margin: 0; }
  :where(ul, ol)[role="list"] { padding: 0; list-style: none; }
  :where(img, picture, svg, video, canvas) { max-inline-size: 100%; block-size: auto; display: block; }
  :where(button, input, select, textarea) { color: inherit; font: inherit; }
</style>
```

Never add `maximum-scale` or `user-scalable=no` (see `accessibility.md`).

## Spacing

- Spacing uses ten steps only. Below 16 they rise by 4 (4, 8, 12, 16); above, each roughly doubles every two steps (24, 32, 48, 64, 96, 128).
- Gap from a section heading to its content: 48 px desktop, 32 px phone.
- Cards in a row sit 24 px apart (12 px on phones) and share one height.
- Section height is one screen or two (see `layout-and-heroes.md`).

## Tokens

Name the rhythm once and reuse it:

| Token | Desktop | Phone (<640) | Used for |
|---|---|---|---|
| `--nav` | 64 px | 56 px | fixed header height, `scroll-margin-top` |
| `--pad-top` | 120 px | 96 px | section top to its heading |
| `--pad-bottom` | 96 px | 64 px | space after the last row |
| `--gutter` | 80 px (48 px at 640–1023) | 24 px | left and right page edge; never widen the tablet value |
| `--head-gap` | 48 px | 32 px | heading to content |
| `--bar` | 0 | 64 px + safe area | phone action bar reserve |

```css
:root {
  --nav: 64px; --gutter: 80px; --pad-top: 120px; --pad-bottom: 96px;
  --head-gap: 48px; --gap: 24px; --bar: 0px;
}
@media (max-width: 1023px) { :root { --gutter: 48px; } }
@media (max-width: 639px) {
  :root {
    --nav: 56px; --gutter: 24px; --pad-top: 96px; --pad-bottom: 64px;
    --head-gap: 32px; --gap: 12px;
    --bar: calc(env(safe-area-inset-bottom) + 64px);
  }
}
```

## Grid and frame

- 12 columns with a 24 px gap (12 px under 640 px). Left and right content edges are equal at every width.
- Desktop frame at 1440: content from x 80 to x 1360. The grid maths for spans is in `layout-and-heroes.md`.
- Place pages (cafés, shops, studios) use a narrower 1200 px wrap with 120 px edges at 1440.
- Picture walls are the one exception to the gap: tiles may sit 0–2 px apart.

```css
.wrap { width: min(100% - 2 * var(--gutter), 1280px); margin-inline: auto; }
.grid { --cols: 12; display: grid; gap: var(--gap); grid-template-columns: repeat(var(--cols), [col] minmax(0, 1fr)); }
/* minmax(0, 1fr) stops long words from widening a column */
.place .wrap { width: min(100% - 2 * var(--gutter), 1200px); }
```

## Type

- At most two families and four font files (for example regular and medium of each). Pick faces with character; the over-used defaults listed in `design-rules.md` section 2 are out.
- Weights 400 and 500 only. Big type gets its presence from size, not from 700/800.
- Each level is at least 1.3 times the one below it. Each kind of element keeps a single size site-wide, so all card titles, for instance, are identical.
- Running text 16 px or more, line height 1.5–1.8, lines no longer than about 62 characters. Nothing on the page is smaller than 13 px.
- Labels are 13 px at weight 500 in sentence case. No tracked-out capitals; no eyebrow line above every heading.
- Italic is for quotations and titles of works, not for emphasis styling.
- A big figure (price, stat) is never larger than the heading it supports. Never shrink text to make it fit a box; change the words or the box.
- Typographer's details: curly quotes and apostrophes, a non-breaking space between a number and its unit (`12&nbsp;min`), `hyphens: auto` with `lang` set so long words in big headings can break.
- Emphasis comes from contrast between two sentences, not from marker highlights or a coloured word in every heading. Colour one word at most once per page.

Starting scale (desktop / phone):

| Token | Desktop | Phone | Notes |
|---|---|---|---|
| `--t-h1` | 72 | 38 | hero only; each hero type may set its own |
| `--t-h2` | 48 | 30 | section headings |
| `--t-h3` | 28 | 24 | sub-heads and pull quotes |
| `--t-lead` | 20 | 18 | hero lead, card titles |
| `--t-body` | 16 / 26 line | 16 / 26 | running text |
| `--t-small` | 14 | 14 | meta, form labels |
| `--t-label` | 13 | 13 | the floor |
| `--t-stat` | 38 | 28 | figures; never above `--t-h2` |

Place pages use a fluid section heading instead: `font-size: clamp(1.5rem, 1.1rem + 1.2vw, 2rem);`.

A two-voice heading (a strong first sentence, a quieter second) is the one decorative heading move, and the one place a heading may end with a full stop (name it in the plan):

```html
<h2 class="split-head">Tables for six or more.
  <span>Book a week ahead and we hold the back room.</span></h2>
<style>
  .split-head { font-size: var(--t-h2); font-weight: 500; line-height: 1.15; max-width: 22ch; }
  .split-head span { color: var(--muted); }
</style>
```

## Colour

- The interface is 90–95% neutral. One accent drives the primary button, focus ring, links and an optional brand band; elsewhere it covers under 3% of the screen.
- Ink is a warm or cool near-black that matches the palette, never `#000`. Hairlines are ink at 12–15% opacity.
- Contrast, stricter than WCAG AA because running text is long: body ink 7:1 on its ground; muted grey 4.5:1 and only for labels and meta; large muted text 3:1. Text on a brand band 7:1. Accent as text 4.5:1; accent shapes 3:1 against the ground (WCAG 1.4.11).
- In a hero, use at most one quieter text level under the heading.
- Take the first palette you are dealt unless it clashes with the client's own brand colours.
- No violet or purple in the page's own design: reject any accent whose OKLCH hue is between 270 and 330 degrees. Client logos keep their own colours.

```js
// Reject a violet accent: read the computed colour as OKLCH and test the hue.
function isViolet(cssColour) {
  const probe = document.createElement('i');
  probe.style.color = `oklch(from ${cssColour} l c h)`;
  document.body.append(probe);
  const m = getComputedStyle(probe).color.match(/oklch\(([\d.]+)\s+([\d.]+)\s+([\d.]+)/);
  probe.remove();
  if (!m) return false;               // browser without relative colour: check by hand
  const [, , c, h] = m.map(Number);
  return c > 0.03 && h >= 270 && h <= 330;
}
```

Relative colour syntax: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_colors/Relative_colors

## Radius

- One family per page, chosen by kind: sharp (2–4 px) for fintech and developer tools, soft (8–12 px) as the default, round (16–24 px plus full-round buttons) for consumer apps. Place pages are square except form controls.
- A software window or app frame uses one radius from 12 to 20 px; everything inside it is smaller.
- Nested corners: inner radius = outer radius minus the padding between them.

## Buttons

- 44 px tall (48 px on place pages and in the phone bar), 16 px label, 24 px side padding.
- One filled button per view. A second action is an outline or a plain text link. At most two buttons in a row; on phones they go full width and stack.
- One extra-large size, used once (usually the closing call).
- No slanted, gradient, ghost-on-photo or drop-shadow buttons. Hover and press feedback is in `motion.md`.
- The primary may carry one drawn arrow; if it does, every primary on the page does the same. Arrows are not added to every link.
- The button look is dealt per page from a short list (square, soft, pill) and then kept.

## Phone action bar

Under 640 px a fixed bar holds one or two 48 px buttons (for example "Call" and "Book"). It appears once the hero's own button has scrolled away and hides while the same action is on screen, so the action is never shown twice. While hidden it is `inert`. Without JavaScript it simply stays visible.

```html
<nav class="action-bar" id="bar" aria-label="Quick actions">
  <a href="tel:+10000000000" class="btn">Call</a>
  <a href="#book" class="btn btn-primary">Book a table</a>
</nav>
<style>
  .action-bar { display: none; }
  @media (max-width: 639px) {
    body { padding-bottom: var(--bar); }
    .action-bar {
      position: fixed; inset: auto 0 0; z-index: 10;
      display: grid; grid-auto-flow: column; gap: 8px;
      padding: 8px 12px; padding-bottom: calc(env(safe-area-inset-bottom) + 8px);
      border-top: 1px solid var(--line); background: var(--bg);
      transition: transform 200ms cubic-bezier(.2,.8,.2,1);
    }
    .action-bar.is-hidden { transform: translateY(100%); }
  }
  @media (prefers-reduced-motion: reduce) { .action-bar { transition: none; } }
</style>
<script type="module">
  // Module scripts run after parsing, so every twin below the bar exists. Hide the bar while one is visible.
  const bar = document.getElementById('bar');
  const twins = document.querySelectorAll('[data-same-as-bar]');
  const seen = new Set();
  const io = new IntersectionObserver(entries => {
    for (const e of entries) e.isIntersecting ? seen.add(e.target) : seen.delete(e.target);
    const hide = seen.size > 0;
    bar.classList.toggle('is-hidden', hide);
    bar.inert = hide;
  });
  twins.forEach(el => io.observe(el));
</script>
```

Mark the hero button and the booking section with `data-same-as-bar`. Put the bar after the footer in the source so it is last in the tab order. The bar needs no other script.

## Head

Every page gets this block (fill in real values; never ship the placeholders):

```html
<!doctype html>
<html lang="en" data-kind="service">
<head>
  <meta charset="utf-8">
  <title>[What it is] for [who] in [town] | [Brand]</title>
  <meta name="viewport" content="viewport-fit=cover, initial-scale=1, width=device-width">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <meta name="theme-color" content="[the page's --bg as hex]">
  <meta name="description" content="[One sentence naming the offer, the buyer and its hardest fact.]">
  <meta property="og:image" content="https://example.com/share.png">
  <meta property="og:title" content="[Brand]: [what it is] for [who]">
  <meta property="og:description" content="[The description sentence again.]">
  <meta content="summary_large_image" name="twitter:card">
</head>
```

- `theme-color` equals the page ground. The favicon comes from the client's logo or the page's mark.
- The share image is a 1200×630 screenshot of the hero, not a separate design.
- Add `<link rel="canonical">` only when the real domain is known.
- The first focusable element is a skip link, hidden until it receives focus:

```html
<a class="skip" href="#main">Skip to content</a>
<style>
  .skip { position: absolute; left: 12px; top: -60px; padding: 10px 14px; background: var(--bg); }
  .skip:focus-visible { top: 12px; }
</style>
```

More on titles, descriptions and structured data: `../../pages-and-seo.md`.

## Sections

- Every section is one `<section>` with one `.wrap`, and its `<h2>` comes first in the source.
- Its height is one or two screens (`layout-and-heroes.md`). Content is never half a screen of air.
- Everything in it uses the tokens above.
