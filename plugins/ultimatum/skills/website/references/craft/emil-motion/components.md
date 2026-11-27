# Component motion recipes (CSS first)

Read when building the motion of a button, popover, tooltip, dialog, drawer, toast, accordion, tab indicator, reveal or hold-to-confirm. Curves are `--curve-out`, `--curve-move`, `--curve-sheet` from `easing-and-duration.md`. Every recipe ships with its reduced-motion and hover-gating (`reduced-motion.md`, `mobile-web.md`). The shared properties rule: animate `transform` and `opacity`; see `performance.md` for the few exceptions.

## Choose the tool, cheapest first

| Need | Use |
|---|---|
| Hover, press, colour, a toggle driven by a class or attribute | CSS transition |
| Entry on mount with no script | CSS `@starting-style` |
| Fixed motion that has to keep going while scripts run | CSS animation |
| Script control with CSS-grade speed, no library | Web Animations API, `element.animate()` |
| Springs, layout animation, exit animation, gesture-driven values | a motion library (https://motion.dev/) |

A toast, drawer, command menu or dropdown is a component, not an animation: use a maintained primitive (`libraries-and-toasts.md`), not a hand-built div with no focus handling.

Transitions beat keyframes for anything fired rapidly. A transition retargets from where it is; a keyframe restarts from zero, so stacking toasts jump. Docs: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_transitions

## Rules that apply to all of them

- Never start from `scale(0)`. Start from 0.9 to 0.97 with opacity 0; things in the world do not appear from nothing.
- Anchor to the trigger: `transform-origin` where the trigger sits (many primitives expose it as a variable). Modals are the exception and stay centred.
- Percent values inside `translate()` measure the element itself: `translateY(100%)` slides a panel exactly its own height, content or not. Prefer them to fixed pixels.
- `scale()` scales children too; on a pressed button the label and icon shrink with it, which is the point.
- Never `transition: all`. List the properties.

## Button press

```css
.btn { transition: transform 150ms var(--curve-out); }
.btn:active { transform: scale(.97); }
```

Scale 0.95 to 0.98. `:active` is a real press on touch, so it needs no hover gate; gate any `:hover` style separately.

## Popover, menu, select

```css
.pop { transform-origin: var(--origin, top left); transition: opacity 180ms var(--curve-out), transform 180ms var(--curve-out); }
.pop[data-state="closed"] { opacity: 0; transform: scale(.95); }
```

The origin is the whole effect: the panel looks like it grew out of what was clicked. Set `--origin` from the trigger's position, or use the variable your primitive provides.

## Tooltip

Same as a popover but quicker (about 125 ms, scale 0.97). The first tooltip waits a beat to avoid accidental opening; once one is open, its neighbours open at once with no animation (`transition-duration: 0ms` on an `[data-instant]` state set while a tooltip is open). A toolbar then feels fast without losing the guard.

## Dialog

```css
.dialog { transform-origin: center; transition: opacity 220ms var(--curve-out), transform 220ms var(--curve-out); }
.dialog:not([open]) { opacity: 0; transform: scale(.96); }
.backdrop { transition: opacity 220ms var(--curve-out); }
```

Fade the backdrop with the same time so they read as one surface. For a native `<dialog>`, animating the display change needs `@starting-style` plus `transition-behavior: allow-discrete` (https://developer.mozilla.org/en-US/docs/Web/CSS/@starting-style).

## Drawer or sheet

`transform: translateY(100%)` when closed, `0` when open, `transition: transform 500ms var(--curve-sheet)` if attached to an edge, about 200 ms if floating. Adding drag makes it a gesture problem: `gestures.md`. A drawer is a bundle of focus trapping, escape to close and drag; use a primitive.

## Toast

```css
.toast { opacity: 1; transform: none; transition: opacity .35s ease, transform .35s ease;
  @starting-style { opacity: 0; transform: translateY(80%); } }
```

- `@starting-style` replaces the old "set mounted after first render" effect. Where it is unsupported, set a `data-mounted` attribute after the first frame and key the same transition off it.
- Leave by the edge it entered; swipe-away then matches the entrance axis.
- Slightly slower, plain `ease`: a calm component should move calmly.

## Accordion

```css
.panel { display: grid; grid-template-rows: 0fr; transition: grid-template-rows 220ms var(--curve-out); }
.panel[data-open] { grid-template-rows: 1fr; }
.panel > div { overflow: hidden; }
```

Animating `height` costs layout each frame; this grid-row form avoids measuring in script and is fine for short content. Keep it short, and fade the content with opacity if the cut looks hard.

## Stagger a group entrance

Only for lists or grids seen now and then. Rules and the index-variable form are in `choreography.md`. Input stays live during it.

## Hold to confirm

Overlay hidden with `clip-path: inset(0 100% 0 0)`, grows to `inset(0)` over about 2 s linear while `:active`, snaps back in 200 ms. Add the press scale. Pair it with a keyboard path (a second confirm step) since a hold is not available to everyone: WCAG 2.5.1 and 2.1.1 still apply.

## Tab indicator with a clean colour change

Interpolating the text colour and background of each tab drifts out of step. Instead render the tab row twice, style the copy as "active", and clip it to the active tab's box: animate `clip-path: inset(0 right 0 left)` on change. Text and fill change together because one element is being revealed. Keep the duplicate `aria-hidden` and non-focusable.

## Scroll reveal

Marketing surfaces only, once per element, never on daily-use product UI. Start `clip-path: inset(0 0 100% 0)`, end `inset(0)` about 600 ms on `--curve-move`, triggered by an `IntersectionObserver` with a negative bottom margin so it starts just inside view. Under reduced motion show it already revealed. Docs: https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API

## Before and after slider

Layer two images; cut the upper one with `clip-path: inset(0 X% 0 0)`, where X follows the drag position. No extra elements; compositing stays cheap. Provide a keyboard slider (`role="slider"`, arrow keys) on the handle.

## Mask a crossfade that will not settle

Two states overlapping reads as two objects. Add `filter: blur(2px)` and `opacity: .7` while the swap runs, so the eye reads one thing changing. Keep blur under 20 px (cost: `performance.md`).

```css
.swap { transition: filter 200ms ease, opacity 200ms ease; }
.swap[data-changing] { filter: blur(2px); opacity: .7; }
```

## Scripted without a library

```js
el.animate({ clipPath: ['inset(0 0 100% 0)', 'inset(0)'] },
  { duration: 600, fill: 'forwards', easing: 'cubic-bezier(.77,0,.175,1)' });
```

Runs on the compositor where the property allows it, can be cancelled or reversed, no bundle cost. https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API

## 3D and depth without script

`transform-style: preserve-3d` on the parent with `rotateX`/`rotateY` and `translateZ` on children gives orbits, flips and tilt in CSS. A lower `perspective` exaggerates depth. Counter-rotate a child so a label stays upright while its carrier spins.

## Transform origin

The anchor for scale and rotate. Default is the centre; set it wherever the thing "lives". Everything above depends on it.
