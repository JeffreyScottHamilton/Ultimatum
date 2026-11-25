# Motion

Goal: motion that explains a change, costs little to run, and can be stopped or reversed. Read with `ui.md` §5 (the rulebook: frequency and first "no" wins). This file covers the mechanics.

## 1. Does it help?

- Helps: shows where something came from or went; confirms that an action happened; draws attention to a change the user must notice; hides a delay without moving the layout.
- Hurts: slows a repeated action; delays input; hides content behind an intro; decorates a static page; competes with reading.
- Test: remove it. If the user loses information, keep it. If not, cut it.

## 2. Cheap and expensive properties

- Animate `transform` and `opacity`. They run on the compositor and skip layout and paint.
- Avoid animating layout (`width`, `height`, `top`, `left`, margin, padding) and large paint areas (blur, big box-shadow spreads). Use them only on small elements, and measure.
- To reveal height, animate a grid row from `0fr` to `1fr`, or transform a measured element. Do not tween `height` in pixels.
- Set `will-change` only for the animation's life, never as a permanent style.
- Measure frame time in the browser's performance panel on a throttled CPU. Do not assume it is smooth.

## 3. Durations and easing

- Enter: 150 to 250 ms. Exit: about three quarters of the enter duration. Users wait for things to leave, so exit is quicker.
- Press feedback: 80 to 150 ms. Large surfaces: 400 ms at most.
- Enter uses ease-out (decelerates into place). Exit uses ease-in or a short ease-out. Two-way moves use ease-in-out sparingly.
- Linear only for progress indicators and continuous loops.
- Name the curves and durations as tokens (`design.md` §3). Do not hard-code them per component.

## 4. Curves or springs

- Use a curve (CSS transition or keyframes) for opacity, colour, short fades and anything with no release gesture.
- Use a spring for motion that follows a pointer or is released with velocity (drag, swipe, sheets). A spring keeps velocity continuous and interrupts cleanly.
- Choose spring settings for a near-critically damped feel. Under-damped bounce only for rare, playful moments. Aim to settle within about 400 ms.
- Use the project's motion library if it has one (`react.md` §E). Do not add a library for a single transition.

## 5. Interruption

- Every animation must be interruptible. A new target starts from the current value and current velocity, not from the start state.
- Never gate input on an animation finishing. A click during an exit still works.
- A quick toggle reverses from the current point.
- Cancel timers, listeners and pending frames when the element unmounts mid-animation.

## 6. Reduced motion

- Honour `prefers-reduced-motion: reduce`. Remove movement and scale; keep the state change through opacity or an instant swap.
- Keep progress indicators and focus rings. They carry information.
- Do not set every duration to zero blindly. Check that the screen still shows what changed.
- Verify with `ult-browser --reduced-motion` (`browser-verification.md` §1).
- Any loop or auto-moving content that runs longer than five seconds needs a pause control (WCAG 2.2.2).

## 7. Gestures and drag

- Track the pointer one-to-one during a drag. Lag here is the most visible defect.
- Use pointer events with pointer capture. Set `touch-action` to match what you handle: `none` for a custom drag surface, `pan-y` for a vertical list with a horizontal swipe.
- Commit on distance or velocity (a flick, or past a set fraction of the width). Otherwise spring back to the start.
- Every drag action needs a non-drag alternative: a button or a keyboard command (WCAG 2.5.7).
- When the content scrolls, use a drag handle rather than the whole surface.

## 8. Groups (choreography)

- Stagger only on first render or a deliberate reveal. Keep the total stagger under about 300 ms: use a small step and cap the count, and let the rest appear together.
- Order: container first, then content. Stay within two levels.
- No stagger on reorder, filter or any repeated action.
- For a shared element that moves between views, give one name on both sides (`react.md` §G).

## 9. Removal pass

Run before shipping any motion. For each animation:

1. Name its job in a few words. No job means remove it.
2. Estimate how often it runs per day. Frequent means remove or shorten.
3. Check it on a throttled CPU. Dropped frames mean simplify it.
4. Check reduced motion, and interrupt it halfway.
5. Remove ambient loops, scroll parallax and decorative entrances unless motion is the product.

Report a before and after list with one line per removed or changed animation.
