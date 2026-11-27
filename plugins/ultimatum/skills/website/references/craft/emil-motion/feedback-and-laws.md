# Feedback moves and the three UX laws

Read when a control works but feels unsure (did my click land? where did that panel come from?), or when a review asks why a target, a menu or a wait feels wrong. Five motion moves, one focus move, three laws with numbers, each with a check. Durations and curves come from `easing-and-duration.md`; every move here has a still version under `prefers-reduced-motion: reduce` (`accessibility` rules in `gate.md`).

## Motion moves

| Move | Use it for | Numbers | Never |
|---|---|---|---|
| Pulse to confirm | A save, copy, add-to-cart or toggle that changes nothing else on screen | one scale 1 → 1.06 → 1 or a ring that grows and fades, 250–400 ms, once | looping, or on errors (an error shakes or turns red and says why) |
| Grow from the same element | A card that opens to detail, a button that becomes its menu or form | 250–400 ms ease-out; the moving box keeps its corners and colour until it lands | fading the card out and a new panel in from nowhere |
| Swap icons with a blur | Play/pause, copy/copied, menu/close: one icon becomes another in place | 150–200 ms; outgoing scale 1 → 0.6, opacity 1 → 0, blur 0 → 4px; incoming the reverse | a hard cut, or both icons visible at full size at once |
| Rubber-band past the edge | Drag or scroll that hits the end of a list, sheet or carousel | travel past the edge shrinks as you pull (about a third of the finger's distance, falling); spring back on release | a hard wall, or letting the content leave the screen |
| Reveal with a mask | A heading, image or panel entering on scroll or first load | 400–700 ms on `clip-path: inset()` or a gradient `mask-image`, once per element | revealing body text line by line, or replaying on every scroll pass |

```css
/* Pulse once when .is-saved is added; JS removes the class on animationend. */
@keyframes confirm-pulse { 50% { transform: scale(1.06); } }
.is-saved { animation: confirm-pulse 320ms var(--curve-out, cubic-bezier(.2,.8,.2,1)); }

/* Icon swap: two stacked icons, the parent's state decides which shows. */
.swap { display: grid; }
.swap > svg { grid-area: 1 / 1; transition: opacity 180ms, transform 180ms, filter 180ms; }
.swap > .off { opacity: 0; transform: scale(.6); filter: blur(4px); }
.swap[aria-pressed="true"] > .on  { opacity: 0; transform: scale(.6); filter: blur(4px); }
.swap[aria-pressed="true"] > .off { opacity: 1; transform: none; filter: none; }

/* Mask reveal, left to right: the box is in place from the start, only its visible part grows. */
.reveal { clip-path: inset(0 100% 0 0); }
.reveal.is-in { clip-path: inset(0); transition: clip-path .6s cubic-bezier(.2,.8,.2,1); }

@media (prefers-reduced-motion: reduce) {
  .is-saved { animation: none; outline: 2px solid var(--accent); outline-offset: 2px; }
  .swap > svg, .reveal { transition: none; filter: none; }
}
```

```js
// Rubber band: resistance rises with distance past the edge (d in px, size = track length).
const band = (d, size) => (1 - 1 / (d * 0.55 / size + 1)) * size;
```

Grow-from-the-same-element in plain CSS is the View Transitions API: give the card and the detail the same `view-transition-name`, then call `document.startViewTransition(update)`. Where it is missing, measure the card, set the panel to that box, and animate `transform` to the final box (first, last, invert, play: `performance.md`).

Check: the pulse fires once and only on success; the icon button keeps its `aria-label` or `aria-pressed` in step with the picture; the mask reveal shows the whole element with motion off.

## Stage the focus

One thing moves or brightens at a time, and everything else waits or dims. On a step that opens a dialog, a tour step or a result, quiet the rest (opacity 0.4–0.6, or a scrim), move focus to the new thing, and bring the rest back when it closes. Stagger a group at 30–60 ms per item and stop after about six items; longer lists come in together.

Check: at any moment a reviewer can name the one element the screen wants them to look at, and keyboard focus is on it.

## The laws

| Law | What it says | Rule of thumb | Check |
|---|---|---|---|
| Fitts's law | Time to hit a target grows with distance and shrinks with size | The main action is large and near where the hand already is; touch targets at least 44 × 44 px (24 × 24 CSS px is the WCAG 2.2 floor); edges and corners of a desktop screen are easy to hit; a destructive action sits away from the common one | measure each target's box in DevTools at 320 px wide; count the full hit area, padding included |
| Hick's law | Time to choose grows with the number and sameness of options | One primary action per view; menus of more than about seven grouped or searched; defaults pre-chosen; advanced settings behind a disclosure | count the equal-weight choices on each screen; more than one primary button is a finding |
| Doherty threshold | People stay in flow when the system answers in under about 400 ms | Show a response within 100 ms (pressed state, optimistic update, skeleton); real work over 400 ms gets progress; over 10 s gets a percent or steps and a way to leave | time the click to first visible change in DevTools Performance; INP under 200 ms is the web target (`../taste/performance.md`) |

The laws explain a finding; they don't replace measuring. Write the finding as the number (a 28 px target, nine equal buttons, 900 ms of nothing) and name the law after it.
