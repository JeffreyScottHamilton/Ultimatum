# Easing, duration and asymmetric timing

Read when choosing a curve or a time for a transition, or when a motion "feels off" and the cause is probably its curve or its length. Springs are in `springs.md`. Searchable values: `../../../../../data/craft/emil-motion/timing.csv`.

## Pick the easing

Ask in this order and stop at the first yes.

1. Entering or leaving the screen: ease-out (fast start, soft landing). The person watches the first frames hardest, so the first frames should already be moving.
2. Moving or reshaping something already on screen: ease-in-out.
3. A hover colour or background change: plain `ease`.
4. Constant motion that visualises time or progress (progress bar, marquee, hold-to-confirm fill, spinner): `linear`.
5. Anything else: ease-out.

Never ease-in on interface motion. A 200 ms ease-in feels slower than a 200 ms ease-out because nothing happens early.

## Strong curves instead of the built-ins

The keyword curves are weak: they lack the punch that reads as deliberate. Define three named curves once as tokens and reuse them; do not hand-type a new bezier per component.

```css
:root {
  --curve-out:    cubic-bezier(.23, 1, .32, 1);    /* entrances, exits, presses */
  --curve-move:   cubic-bezier(.77, 0, .175, 1);   /* on-screen travel and morphs */
  --curve-sheet:  cubic-bezier(.32, .72, 0, 1);    /* edge-attached sheets and drawers */
}
```

- The sheet curve is very steep at the start, which is why a 500 ms sheet still feels immediate and lands softly like a spring would. It suits a panel attached to a screen edge. A small floating panel that is not attached to an edge should drop to about 200 ms with a gentler out curve such as `cubic-bezier(.165, .84, .44, 1)`.
- Take other curves from a curve picker (https://easings.co/ or https://easing.dev/) and name them as tokens. Reference for the syntax: https://developer.mozilla.org/en-US/docs/Web/CSS/easing-function
- If the project already has curve or duration tokens, extend them. A second parallel scale is a defect. On a website build, the tokens in `../taste/motion.md` § Tokens are the house set; map this folder's rules onto them rather than adding new ones.

## Duration budgets

| Element | Time |
|---|---|
| Press feedback | 100 to 160 ms |
| Tooltip, small popover | 125 to 200 ms |
| Dropdown, select | 150 to 250 ms |
| Modal, drawer | 200 to 500 ms (edge-attached sheet at the long end) |
| Marketing or explanatory sequence | longer is allowed |

- Interface motion stays under 300 ms unless you can say why. A 180 ms dropdown beats a 400 ms one.
- Exit is faster than entrance when the person has already decided to leave. The generic rule from the shared motion file (exit about three quarters of enter) is a ceiling, not a target; going shorter is fine.
- Sub-parts of one component share a time family. A drawer that opens in 500 ms and then resizes in 200 ms reads as two objects; bring them to one duration and one curve family. Inner content may use a lighter curve than the container, though a body on ease-in-out inside a frame on ease-out drifts out of step.

## Asymmetric timing

Slow where the person is deciding, quick where the system answers.

```css
.hold-fill { transition: clip-path .18s var(--curve-out); clip-path: inset(0 100% 0 0); }  /* released: empties quickly */
.hold:active .hold-fill { transition: clip-path 2s linear; clip-path: inset(0 0 0 0); }  /* while held */
```

- A press-and-hold fill is linear because it draws elapsed time; any curve misreports how long is left.
- Release or cancel is always fast.
- Same logic for enter and leave of a panel: the system's response snaps.

## Match the personality

Playful products can be bouncier and slower; a trading or admin screen stays crisp and fast. A calmer toast may use plain `ease` at 400 ms because its whole design is calm. The test is cohesion: curve, time, shape, type and copy tone pull the same way. When unsure whether a move earns its place, deleting it is a legitimate answer.

## Seeing the problem

- Replay at two to five times the duration, or slow the browser animation inspector, and watch: do two colours visibly overlap, does the curve start or stop abruptly, is the origin right, are the animated properties in step?
- Step frame by frame in the browser's animations panel to see drift between coordinated properties.
- Look again the next day. Faults invisible during building show up with fresh eyes.
- Touch gestures need a real phone (`mobile-web.md`).

## Opacity with height

When items enter or leave a list and the container's height also changes, the opacity fade and the height change fight each other. There is no formula: tune the pair by eye, usually fading slightly faster than the height settles, and check it again on another day.
