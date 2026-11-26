# Moments and big scenes

Read when a page plan reaches its memorable part: choosing the one or two moments, or a tech page's single big scroll scene.

## Moments

A moment is the one place on a page a visitor remembers, and it lives in its own section. Apart from moments, only the hero entrance and the hover layer move (`motion.md`).

- **Count:** a short page gets one. A long page (eight or more sections) may get a second, placed in another section. A third is never right, whatever the kind.
- **Plan line:** each moment's id, its section and what it carries. A moment with nothing to carry is swapped for another.
- **Words and pictures are real:** the HTML holds the finished text in place, and no moment hides a headline on load. Photos are the client's own (or library frames that pass `photos.md`), each used once. No captions; credits go in the footer line.
- **Tokens:** moments read the page's `--bg`, `--ink`, `--muted`, `--accent`, `--line` and display face. Text sits in the normal wrap, so lines, discs and wipes never cut a heading, button or picture.

### Pools by site kind

| Kind | Built from | May use |
|---|---|---|
| Place (café, shop, guesthouse) | type and photographs | word-highlight; picture-develops, film look; photo-chapters |
| Product | type and photographs | word-highlight; picture-develops, film look; photo-chapters; pinned-chapters |
| Service (trade, clinic, agency, firm) | type and photographs | as for product |
| Software, gaming, tech | anything | the eleven moments other than photo-chapters and picture-develops |

Calm kinds get photo- and type-led moments because they move only in their own section, cost no WebGL and stay calm.

**Never on place, product or service:** liquid-hover, liquid-type, cursor-spotlight, iris-opens, line-carries-colour, letters-assemble, picture-develops in its print (halftone) look, giant-type-pass, marquee-row, counter-rolls.

- A place with fewer than eight usable photographs skips photo-chapters. It gets one moment: either picture-develops over its best section photo, or word-highlight inside a statement section one screen tall (`place-pages.md` § Short page).
- A long calm page pairs a statement (word-highlight) with a section moment, or picture-develops with one chapters moment.
- A page uses photo-chapters or pinned-chapters, not both: one tells a story in full-width photos, the other walks steps beside one frame (a booking or order flow).
- On tech, a moment is one of the page's beats, counted against the effect and any big scene (`grounds-and-effects.md` § Budget).

### Catalogue

| Id | Trigger | Fits | Use | Reduced motion and phone |
|---|---|---|---|---|
| word-highlight | scroll | statement | one sentence whose words fill from muted to ink as it crosses the screen | whole statement in ink; runs on phone |
| picture-develops | enter, 1.6–1.8 s | section | one large photo with a clear subject rises from a grey print, darks first, then colour (film look) | photo shown still; runs on phone |
| photo-chapters | scroll | section | 3–5 chapters (title, two lines, one photo) under the `h2`; each full-width photo is uncovered from its foot; text panel at the lower left; each chapter gets roughly 0.66 of a screen | photos side by side (stacked on phone); runs on phone from 600 px tall |
| pinned-chapters | scroll | section | a feature section of 2–4 steps beside two live screens | static rows, each step with its picture under it |
| counter-rolls | text, once | statement | real proof figures roll in; never inside a card | final figures |
| giant-type-pass | scroll | statement | a statement in huge letters over a mid-to-dark photo (tech only) | the photo inside the letters at a smaller size |
| letters-assemble | scroll | statement | a 2–5 word line set very large, letters flying into place | the line as written |
| marquee-row | scroll | row | a moving row of real words such as cities served, trades or formats (logos never), with a pause button | a wrapped still row |
| line-carries-colour | transition | new ground | an inset panel uncovered by a line climbing from its foot | blocks shown whole |
| iris-opens | transition | new ground | an inset panel opened by a disc with a hairline accent ring | blocks shown whole |
| cursor-spotlight | hover | hero frame | a soft light follows the pointer over the hero | the light rests |
| liquid-type | hover | statement, ≤ 6 words | the headline ripples under the pointer through one SVG filter, no WebGL | headline as written |
| liquid-hover | hover | one photo | a photo with clear edges and detail ripples under the pointer; one WebGL context | plain photo, no canvas |

Retired and never dealt: the magnetic button, word-rotate, window-parallax, lines-rise, closing-lift and headline-arrives.

### Hero moments (tech only)

Zero or one, and only on a hero layout that suits it: liquid-hover on a split hero with a photo; cursor-spotlight on a product, collage, film or centred hero; liquid-type on a statement hero of six words or fewer. Off on touch screens; still under reduced motion. A hero moment still counts toward the page's two.

### Dealing

- Different sections for different moments; never two in one slot.
- Never two of one family: every hover or liquid moment is the page's one pointer effect.
- Moments that need a photo are dealt only when the client has one.
- Statement-fit moments (letters, liquid type, word-highlight, counter) go only in a statement section.
- Keep a short history of moments used; don't repeat the last one, and keep the last three out after a full cycle.
- Never in a card, plan, result tile or bento cell. Mark such a moment still rather than run it.

### Hosting and height

- The host is a section carrying `data-moment="<id>"`, with options in a JSON `data-moment-opts`. A statement moment owns a whole section whose first element is the `h2`; a transition is the whole new-ground section; a marquee or counter row joins the section above as its last row.
- Moments sit in one- or two-screen sections. photo-chapters is (hold + 1) screens while live: so 3 chapters take 3 screens and 4–5 chapters take 4. Don't give it a fixed height.
- Add a class from the head when scripts run, and a "safe" class after 2.5 s that shows every finished state, so a failed module never leaves a section blank.

### Timing

- Scroll moments scrub within their own section, do one thing and show a finished state at both ends. Transitions are complete before the section's upper edge climbs to 20% below the viewport top.
- Settle ease `cubic-bezier(.22, 1, .36, 1)`; reveals 600–1000 ms; a photo develops in 1.6–1.8 s; a scrubbed wipe spends about half its chapter's share moving and holds for the rest.
- Nothing blinks, bounces or overshoots. One count per page, by counter-rolls or the tech count, never both.

### Phone and reduced motion

Every moment has a still state. Treat a screen as a phone when it is under 640 px wide, or a touch screen under 500 px tall in landscape. Phones keep three moments running: word-highlight, photo-chapters and the film look of picture-develops. Hover moments do nothing on touch. Decide the still state on mount; crossing 640 px applies on the next load, except the two chapters moments, which re-check on resize.

### Cost

liquid-hover is the single WebGL moment: tech pages only, a single context, mounted when near the viewport, falling back to the plain photo when its shader breaks. liquid-type runs through a single SVG filter that is live just while a ripple lasts. The rest use custom properties, `transform`, `clip-path` and one passive scroll listener. Screenshots from headless Chrome render WebGL in software, so the liquid moments read weaker there than on a real laptop.

Photo tone: giant-type-pass and liquid-hover need mid-to-dark photos with edges. A pale dusk sky inside letters turns lavender; avoid it (no violet or lavender anywhere).

### Example: word-highlight without a library

CSS scroll-driven animation where supported, one passive listener elsewhere, and the full statement in ink under reduced motion:

```html
<section class="statement" data-moment="word-highlight">
  <h2 class="statement__text">We fit every wheel on the same bench the day it comes in.</h2>
</section>
<style>
  .statement__text .w { transition: color 200ms linear; color: color-mix(in oklab, var(--bg), var(--ink) 30%); }
  .statement__text .w.on { color: var(--ink); }
  @media (prefers-reduced-motion: reduce) { .statement__text .w { color: var(--ink); } }
</style>
<script>
  // Wrap words in spans, then light each one as the section crosses the middle of the screen.
  const el = document.querySelector('.statement__text');
  el.innerHTML = el.textContent.trim().split(/\s+/).map(w => `<span class="w">${w}</span>`).join(' ');
  const words = [...el.querySelectorAll('.w')];
  const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let queued = false;
  function paint() {
    queued = false;
    const r = el.getBoundingClientRect();
    const p = Math.min(1, Math.max(0, (innerHeight * 0.8 - r.top) / (r.height + innerHeight * 0.3)));
    const n = Math.round(p * words.length);
    words.forEach((w, i) => w.classList.toggle('on', i < n));
  }
  if (still) words.forEach(w => w.classList.add('on'));
  else { addEventListener('scroll', () => { if (!queued) { queued = true; requestAnimationFrame(paint); } }, { passive: true }); paint(); }
</script>
```

The heading's text stays in the HTML; screen readers read one sentence because spaces stay between the spans. Scroll-driven animations: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_scroll-driven_animations

## Big scenes

A big scene is a full-screen stretch of a tech page that plays as you scroll. Software, tech (technical products, hardware, networks) and gaming only. Places, services and plain products never get one.

- **One scene per page at most,** and only when the brief supplies everything it needs. Never a stand-in picture to make one fit. A game without art sets its name large over stand-in photos of its setting instead, with no effect.
- **It counts as the single effect on its page,** so no WebGL part or shader ground sits anywhere beside it.
- **Choosing:** deal at random among scenes whose fit, kind and needs match; skip the last three used. The plan line names both the scene and the section that hosts it.
- **Calm around it:** one or two scroll moments may sit elsewhere on the page, but not inside the scene's own section, not in its neighbour, and not any moment the scene marks as a clash.

### Catalogue

| Scene | Sits | For | Screens at rest | GL contexts | Under 768 px | The brief must supply |
|---|---|---|---|---|---|---|
| descend-through-weather | under the hero | gaming, tech | 2 | none | finished | a high and a low photograph of the same world |
| shaped-window-over-fixed-world | under the hero | gaming, tech | 2 | none | finished | a single wide photograph of the world |
| fixed-hero-object | under the hero | gaming, tech | 2 | one | finished | a render or cut-out of the object; up to four chapters |
| powers-of-ten-pullback | in the product section | software, tech, product | 1 | none | finished | the real interface at its true size |
| product-assembles-into-its-action | in the product section | software, tech, product | 1 | none | finished | the screen rebuilt in HTML as 4–6 steps |
| parts-lock-into-the-whole | in the product section | software, tech, product | 1 | none | finished | the screen split along its own panels |
| fly-into-the-shape | between sections, or the product one | gaming, software, tech | 1 | none | finished | the logo as a single path plus a dark photograph |
| letter-physics | a statement | gaming, software, tech | 1 | none | lighter run | a claim, then its answer |
| object-through-giant-type | a statement | gaming, software, tech | 1 | one | finished | an object and a quote of 3–5 lines |
| full-stop-dot | a statement | gaming, software, tech | 1 | none | lighter run | a single claim, 4–6 words long; its closing full stop is a named lint waiver in the plan |
| letter-bar-floods-the-ground | between sections, or a statement | gaming, software, tech | 1 | none | finished | two statements, then an inverse-ground section |

- **The hero holds one screen.** A scene becomes the hero only with rest height 1, and powers-of-ten-pullback never does (its first screen has no headline or action). The three rest-height-2 scenes go just below the hero as a two-screen section with its own `h2`.
- **Object scenes** render an object from the client's own trade (`objects.md`). Never a cup on a café page.
- **Height:** the live section is (hold + 1) screens, 1800 px at 1440 × 900 with the default hold of 1. The rest height is a minimum, set as `--screens`; never a fixed height.
- **Under 768 px** a scene shows only its end state; the two type scenes marked "lighter run" play a reduced version instead.
- **Reduced motion, no script or a failed module:** the finished composition. Object scenes show their still picture and create no WebGL context.
- **WebGL:** one context per scene from the page's budget of four (`performance.md` § WebGL), made when the live scene comes close to the viewport and freed once it scrolls away; a still picture when WebGL fails.
- **Text over photos** sits on a flat band of ground or the photo's calm dark area: 4.5:1 for body, 3:1 for display text. No scrim or gradient.
- **Cost:** move layers of fixed size with `transform`, `clip-path` and `opacity`; an SVG clip redrawn every frame, or any width or height change, is out.
- **Reading:** scene words are real text in reading order, and the end state alone carries every word and idea the moving version does. Nothing that moves crosses words being read; each pause shows whole statements. No captions, chips or labels that ride the scroll.
- **Scroll:** native only. The stage sticks with `position: sticky` for the hold; nothing captures the wheel.
- The scene is a direct child of `main`. Its demo pictures, words and objects are placeholders: swap in the client's and credit photos in the footer, marked "adapted" when cropped.

```html
<section class="scene" data-scene="full-stop-dot" style="--screens:1">
  <div class="scene__stage">
    <h2>Builds that finish before the coffee does.</h2>
  </div>
</section>
<style>
  .scene { min-height: calc(var(--screens) * 100svh); }
  .scene.is-live { height: calc((var(--hold, 1) + 1) * 100svh); }
  .scene__stage { position: sticky; top: 0; min-height: 100svh; display: grid; place-items: center; }
</style>
```
