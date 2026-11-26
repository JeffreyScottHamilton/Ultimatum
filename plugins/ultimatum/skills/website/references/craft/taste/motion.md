# Motion: tokens, hover, entrance, loops

Read when adding any movement to a page: hover and press states, the hero entrance, loops, scroll work, and their reduced-motion versions.

## Where motion is allowed

Every page moves in exactly three places, and nothing else moves:

1. **The hero entrance,** once per visit.
2. **One dealt moment** per section that holds one (`moments-and-scenes.md`).
3. **The hover and press layer.**

- Tech pages (software, gaming, technical hardware) may add card loops, one timed hero or data-visual loop, one count, and the one effect (`grounds-and-effects.md`). Other kinds get none of these.
- A product render stays still unless the page is explicitly live; one live context at most, with a pause button; still on phones and under reduced motion.
- Each motion gets a one-line purpose in the plan. Without one, it goes.
- Every word can be read with nothing moving, with scripts off and under reduced motion. Motion only adds to a whole page.
- A page missing its hover layer, hero entrance or dealt moment is unfinished; the gate counts it as a fault.

## Tokens

```css
:root {
  --m-in: 150ms; --m-out: 120ms; --m-press: 90ms; --m-panel: 200ms; --m-slide: 240ms;
  --m-cycle: 3.2s; --m-image: 600ms; --m-image-out: 400ms;
  /* tech loops only */ --m-count: 1000ms; --m-roll: 700ms; --m-level: .6s;
  --ease: cubic-bezier(.2, .8, .2, 1);                            /* UI steps */
  /* entrances and settles */ --ease-settle: cubic-bezier(.22, 1, .36, 1);
  --ease-travel: cubic-bezier(.65, 0, .35, 1);                    /* things moving across */
}
```

- Loops and drifts are linear. No curve overshoots or bounces.
- Animate only `transform`, `scale` and `opacity`; hovers may also change colour. Never animate width, height, top, left, margin or padding.
- A dealt moment may also animate `clip-path`, `filter` (a photo developing), text colour, and on tech `background-position`. Name each in the plan.
- Distances, and no others: card lift 2 px; photo zoom 1.02–1.03; arrow 3 px; menu drop 6 px; button step 1 px (2 on an extra-large button); press 1 px down at scale .985.
- Easing reference: https://developer.mozilla.org/en-US/docs/Web/CSS/easing-function

## Hover and press

Hover states apply only to fine pointers; keyboard focus shows the same state; every control also works by tap and keyboard; nothing resizes or pushes a neighbour.

| Element | Hover or focus | Press | Times |
|---|---|---|---|
| Button | fill steps 14% toward ink (an outline button picks up a light tint and a darker edge); lifts 1 px | sinks to 1 px below rest | 150 in, 120 out, 90 press |
| Text-style secondary | keeps its underline, doesn't lift | scale .985 | same |
| Arrow in a button | moves 3 px right and settles | | 150 / 120 |
| Running-text link | rests on a faint 1 px line; an ink line draws left to right, leaves to the right | | 150 / 120 |
| Nav word | darkens; a 1 px line draws 4 px under it; no gliding pill | | 150 / 120 |
| Linked card | lifts 2 px, border one step darker, optional soft shadow (blur 24, 10% ink, hover only) | | 180 / 120 |
| Card without a link | nothing (mark it so the layer skips it) | | |
| Linked photo | grows to 102–103% within its own frame; never dims or takes an overlay; a product name underlines with it | | 600 / 400 |
| Field | action-coloured border plus a 3 px soft ring | | 140 |
| Focus ring | 2 px in the action colour, 2 px off the control, drawn at once, never animated | | 0 |

- Nav panel: opens after 150 ms of hover intent, fades in with a 6 px drop as one surface, closes in 120 ms; open panels swap instantly. The chevron turns 180° on tech and flips instantly elsewhere.
- Current page: a 2 px bar under the nav word with `aria-current="page"`, no motion.
- Tabs (software only, click only): one indicator slides by `transform` in 240 ms; panels swap in 200 ms at most and share a fixed height. Other kinds have no tabs.
- Switch and checkbox on tech: the knob slides 16 px and stretches 4 px while pressed; the tick fades in while growing from 70%. Elsewhere they jump.
- Copy button on tech: the glyph becomes a check for 1.5–2 s, then returns.
- FAQ answers are all open; no accordion.
- Banned on hover: rotate, skew, glow, shine sweeps, gliding chips, magnetic buttons. Page CSS never overrides a button's transform or transition.

```css
@media (hover: hover) and (pointer: fine) {
  .btn { transition: transform var(--m-out) var(--ease), background-color var(--m-out) var(--ease); }
  .btn:hover { transform: translateY(-1px); background-color: color-mix(in oklab, var(--accent), var(--ink) 14%);
               transition-duration: var(--m-in); }
  a.card { transition: transform var(--m-out) var(--ease), border-color var(--m-out); }
  a.card:hover { transform: translateY(-2px); border-color: color-mix(in oklab, transparent, var(--ink) 18%); }
  .zoom { overflow: hidden; }
  .zoom img { transition: transform var(--m-image-out) var(--ease-settle); }
  .zoom:hover img { transition-duration: var(--m-image); transform: scale(1.03); }
}
.btn:active { transform: translateY(1px) scale(.985); transition-duration: var(--m-press); }
:focus-visible { outline-offset: 2px; outline: 2px solid var(--accent); }
.link { background: linear-gradient(currentColor 0 0) 0 100% / 0 1px no-repeat,
                    linear-gradient(color-mix(in oklab, currentColor 25%, transparent) 0 0) 0 100% / 100% 1px no-repeat;
        transition: background-size var(--m-out) var(--ease); }
.link:is(:hover, :focus-visible) { transition-duration: var(--m-in); background-size: 100% 1px, 100% 1px; }
```

`hover` and `pointer` queries: https://developer.mozilla.org/en-US/docs/Web/CSS/@media/hover

## Hero entrance

About 1.1 s in total, ease-out, once per visit, never on scroll.

- `h1` lines rise out of word masks, 700 ms each, lines 80 ms apart, at most 240 ms from the first line to the last. A heading that is rebuilt by script rises whole.
- Then the lead, buttons and facts fade up 12 px, 520 ms each, 60 ms apart, starting when the last line is half up.
- A notice line above the `h1` enters with the first line.
- The hero picture never fades: a photo eases down to its size from 105% in 1.1 s, and a window, collage or object grows from 98% in 900 ms, always as a single block.
- Hide words only while a class set in the head is present, and remove it after 700 ms whatever happens, so text never stays hidden. Scripts off, reduced motion and print show the hero as written. Screenshots taken headless see it at rest.
- Never a loader, gate, delay before reading, or second entrance.

```html
<script>
  // In <head>: hide hero words only until the entrance runs, with a hard 700 ms fallback.
  if (!matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const root = document.documentElement;
    root.classList.add('m-enter');
    setTimeout(() => root.classList.add('m-enter-done'), 700);
  }
</script>
<style>
  .m-enter:not(.m-enter-done) [data-enter] .line > span { transform: translateY(105%); }
  [data-enter] .line { display: block; overflow: hidden; }
  [data-enter] .line > span { display: inline-block; transition: transform 700ms var(--ease-settle); }
  [data-enter] .line:nth-child(2) > span { transition-delay: 80ms; }
  [data-enter] .line:nth-child(3) > span { transition-delay: 160ms; }
</style>
```

## Loops

Tech pages only; cards are in `cards-and-ui.md` § Loops.

- One cycle 2.5–4 s (3.2 s default), starting on its finished picture after a 600 ms rest. For its final 10–15% the cycle rests on that finished picture; a reset dims and rewrites, never blanks.
- Pointer or focus entering restarts a loop from the top (not within its first 800 ms). A paused loop stays paused. Cards never zoom, tilt or pan.
- One subject per cycle; one change every 1–2 s, each change 300 ms or less. A label never shows two words at once.
- Signs of life only inside a loop: a spinner for 1 s (12–16 px, then a check); a live dot whose ring grows and fades every 2.4 s, only beside something that is truly live (a pulsing dot on still content is in the house lint); a caret blinking with a hard step at 1 s; level bars at .6 s. No typing dots or block cursor after headlines.
- Card stories run in fixed-height boxes: typed prompts go at 12–20 characters per second, then rest; replies arrive at roughly one bubble per second; new notifications push in from the top as the oldest one fades; checklist items tick roughly once per second; calendar entries appear in turn; a pointer travels roughly 200 px per second, presses (scale ≥ .96, 28 px ring) and holds. A speaker or avatar changes at most every 3 s. Charts stay still.
- Budget: one timed loop per page (hero or data-visual), plus at most one effect; a live hero effect forbids any other timed loop. Card loops, diagram pulses and moments sit outside this count.
- One count per page: about 1 s on load, 1.2 s at most, the final figure already in the HTML. Never a year, price or phone number. Live counters change only the last one to three digits.
- Tech pages may run a single motion on load in the data-visual frame, 600–1200 ms long and at rest within 1.5 s; swapping its content on click takes 400–600 ms.
- If something keeps moving for more than 5 s after it comes into view, it gets a 32 px round pause button 12 px from the bottom right, never over copy (WCAG 2.2.2: https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html).
- Timed loops begin with the page load; scrolling never starts or stops them, though an IntersectionObserver may delay mounting one. Canvases may stop drawing while off screen, and everything may pause in a background tab.

## Scroll

- Outside the dealt moment's section (and a tech scene), nothing animates on scroll: no reveals, parallax, scroll-snap, scroll-tinted grounds, progress lines, scroll-spy or count-on-view.
- Moments pin only with `position: sticky` and scrub to the scrollbar, reversing upward, with a finished state at both ends. Enter moments run once, 1.6–1.8 s.
- Drivers allowed: CSS scroll-driven animations (`animation-timeline`), a single passive scroll listener that sets one custom property per frame, or on tech a scroll library scoped to the section without its own pinning.
- Never a smooth-scroll library or scroll-jacking on any page; no animation library on non-tech pages.
- Scrolling never changes how the header or the phone bar looks. The phone bar appears once the hero button scrolls away (`system.md` § Phone action bar), 240 ms, instant under reduced motion.
- Scroll-driven animations: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_scroll-driven_animations

## Reduced motion

Honour `prefers-reduced-motion: reduce` (WCAG 2.3.3 Animation from Interactions):

- Kept: colour changes, menu fades, a darker tone on press. Tab indicators and switch knobs snap into place; underlines show up in place rather than sliding.
- The hero stands as written. Loops, effects, moments and scenes show their finished frames. Marquees stand still as a row, and counters print their end value. With nothing moving, the pause buttons are hidden.

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation: none !important; scroll-behavior: auto !important;
    transition-property: color, background-color, border-color, opacity !important; }
  [data-enter] .line > span { transform: none !important; }
  .pause { display: none; }
}
```

- Phones (no hover, touch): card loops and effects show a poster or finished frame; heavy canvases become stills; no hover states or simulated pointer. The hero still enters; light moments still run.
- WCAG 2.3.3: https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html

## What never moves

- Cards that reveal, tilt, flip, glow or follow the pointer; magnetic buttons; a replaced cursor.
- Carousels, auto-advancing sliders, timed tabs, rotating notices, logo marquees.
- Twinkles, sparkles, flicker, random blinks, cycling hues, letters that scramble. A change must show real data, a step or a state.
- Two loops in a single panel; a card loop longer than 4 s; a loop that runs only once (a card story's replay is the exception).
- Hovers slower than their token; easing that overshoots; any lag before a button responds; an animated focus ring; a second underline or indicator style; animated width, height or margin.
- Flashing more than three times a second, anywhere (WCAG 2.3.1).

Check every interaction by eye on a demo page at 1440 and 390, with and without reduced motion.
