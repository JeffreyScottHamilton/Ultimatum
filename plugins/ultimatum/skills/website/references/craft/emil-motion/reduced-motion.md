# Reduced motion and input gating

Read when shipping any motion, and when a page must honour `prefers-reduced-motion`, hover capability, transparency or contrast preferences. These ship with the animation, not after it.

## What the setting asks for

The aim is less and softer, never nothing. Keep opacity and colour changes that explain a state change, progress indicators, focus rings. Remove movement, scale, parallax, spinning, elastic overshoot and large travel. Slides and springs become short cross-fades; screen transitions become fades.

```css
@media (prefers-reduced-motion: reduce) {
  .sheet { transform: none; transition: opacity 200ms ease; }
  .reveal { animation: none; opacity: 1; }
}
```

In script, read it once and branch values: `matchMedia('(prefers-reduced-motion: reduce)').matches`. With a library, use its reduced-motion hook to pick `0` instead of `-100%` for a start offset.

- Do not blindly zero every duration: check the screen still shows what changed.
- Loops, marquees and sequences: show the end frame, or step between frames instead of animating between them.
- Gesture tracking stays (the person produces it). Momentum, bounce and decoration reduce.
- Verify by emulating the preference in browser devtools or Playwright (`reduced_motion="reduce"`), then interrupt an animation halfway.

## Related WCAG 2.2 checks

- 2.3.3 Animation from Interactions (AAA, but the reduced-motion rule is the house standard): motion triggered by interaction can be disabled. https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html
- 2.2.2 Pause, Stop, Hide (A): anything that moves on its own for more than five seconds needs a pause control. https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html
- 2.3.1 Three Flashes or Below Threshold (A): no flashing more than three times a second.
- 2.5.7 Dragging Movements (AA): offer a single-pointer alternative to every drag.
- 2.5.8 Target Size Minimum (AA): at least 24 by 24 CSS px.
- Avoid abrupt full-screen brightness jumps (ease dark and light theme changes), full-viewport moving backgrounds, and slow looping oscillation around one cycle every five seconds. Make big moving objects semi-transparent while they travel.

## Hover gating

Touch fakes a hover on tap and leaves it stuck. Wrap hover motion:

```css
@media (hover: hover) and (pointer: fine) { .card:hover { transform: translateY(-2px); } }
```

Give touch people press feedback through `:active`. Details in `mobile-web.md`.

## Other preference queries

- `prefers-reduced-transparency: reduce`: make translucent surfaces solid; raise background opacity, drop `backdrop-filter`.
- `prefers-contrast: more`: near-solid backgrounds and a defined border.
- Support is uneven; always give the default styles a safe look without them. MDN: https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-transparency

```css
@media (prefers-reduced-transparency: reduce) { .bar { background: #fff; backdrop-filter: none; } }
```

## Feedback with sound or touch

Fire visual, sound and any vibration on the same frame, tied to the causal event (the toggle flips, the item snaps home). Use them only for meaningful moments, never as the only feedback, and never per frame. Vibration on the web is limited; treat it as a bonus.

## Checklist before hand-over

- Reduced-motion variant exists and was seen.
- Hover motion gated.
- Nothing blocks input while it plays.
- Pause control on anything running over five seconds.
- A non-drag path exists.
