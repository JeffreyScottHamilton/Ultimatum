# Gestures: drag, swipe, sheet, hold

Read when building anything dragged, swiped, flung, held or dismissed by gesture, or when a gesture lags the finger, jumps on release or cannot be caught mid-flight. Spring detail is in `springs.md`.

## Build or reuse

A proper bottom sheet needs momentum, an overlay that follows progress, dismissal that reads velocity, a focus trap and Escape to close. Weeks of edge cases. Default to a maintained drawer library (https://vaul.emilkowal.ski/) and hand-build only bespoke interactions (swipe cards, custom sliders). Choices: `libraries-and-toasts.md`.

## Two phases

- Pointer down (track): the element sits exactly under the pointer. No easing, no spring, no duration. A spring here makes the element trail the finger like dragging through syrup.
- Pointer up (release): physics finishes it. A spring seeded with release velocity, never a keyframe.

### Track rules

- Respect where the thing was grabbed: keep the offset from the grab point instead of snapping the centre to the finger.
- Use pointer events with `setPointerCapture` so tracking survives leaving the element's bounds. Docs: https://developer.mozilla.org/en-US/docs/Web/API/Element/setPointerCapture
- Ignore a second touch once a drag has begun, or the element jumps to the new finger.
- Write `transform` on the dragged element directly. Do not move children by changing a CSS variable on a parent: variables inherit, so each change restyles every descendant (a drawer with 20+ rows became laggy this way).
- No component state per move event; use direct style writes or motion values.
- Past an edge, rubber-band (rising resistance) instead of a wall.
- Detect plausible gestures in parallel from the first moves, then drop the losers once intent shows; a small movement threshold (about 10 px) decides direction before committing. Avoid recognisers that only report a final "swiped left".
- Do not make people wait for a double-tap window unless double-tap really exists.

### Release rules

- Dismiss on distance or on speed. Distance alone makes flicks feel ignored.
- Snap back quickly if the threshold is not met; a slow snap-back looks like the interface disagreeing in slow motion.
- Bounce only after a drag (force applied); none when closed by button.
- Commit or reverse by velocity direction when velocity is high.

```js
// release: dismiss by distance or by speed
const ms = performance.now() - startedAt;
const speed = Math.abs(dx) / ms;           // px per ms
if (Math.abs(dx) > width * 0.4 || speed > 0.11) dismiss(); else snapBack();
```

## Catchable mid-flight

A person must be able to grab a closing sheet and drag it back. Springs allow it; transitions retarget too. A keyframe run starts over from zero and cannot be caught. Never use a keyframe on anything a gesture can touch.

## Linked values

Derive the overlay opacity or background scale from drag progress rather than animating them separately: one source of truth stays exact even when the person reverses. Example with motion values: `overlay = useTransform(y, [0, height], [1, 0])`.

## Library drag props

In Motion: `drag="y"`, `dragConstraints`, `dragElastic` near 0.2, and an `onDragEnd` that reads offset and velocity. Momentum is on by default: right for a thrown card, wrong for a simple reposition. Docs: https://motion.dev/docs/react-gestures

## Same path out as in

An element dismisses the way it came. A toast that arrived from the bottom is swiped down; the gesture is felt rather than learned. Panels that slide in from the right leave to the right.

## Hold gestures

Linear during the hold (it is a clock), fast ease-out on early release. Add the press scale. Offer a non-hold path.

## Touch checklist

- Real phone on the dev server by LAN address; trackpad emulation lies, and a 60 Hz monitor hides roughness a 120 Hz phone shows.
- Targets at least 44 by 44 px for comfort. WCAG 2.2 requires 24 px at AA (2.5.8) and sets 44 px as AAA (2.5.5), so 44 is the recommendation, 24 is the floor. Enlarge a small visual with an invisible `::before`, not by growing layout.
- `touch-action` names what the browser may still do: `pan-x` on a vertical drag handle, `pan-y` on a horizontal carousel, `none` only where the element truly owns every axis. Docs: https://developer.mozilla.org/en-US/docs/Web/CSS/touch-action
- Gate hover effects behind `(hover: hover) and (pointer: fine)`.
- Every drag has a non-drag way to do it: buttons or keys (WCAG 2.5.7).
- Native scroll with `scroll-snap-type` beats a hand-built carousel spring when it fits.

## Sheet curve and small drawers

A steep edge-sheet curve (`--curve-sheet`) at 500 ms feels near-instant and lands soft. A floating drawer not touching the edge needs about 200 ms. The whole component keeps one time family. Mark interactive children (buttons inside the sheet) as non-draggable so pressing them does not start a drag.

## Reduced motion

Tracking stays. Momentum flings, bounce and decoration reduce. On release, settle with a short opacity or position change.

## Still wrong?

Stutter is a performance fault: check the track rules, then `performance.md`. When you cannot put the feeling into words, record the gesture and step through it one frame at a time.
