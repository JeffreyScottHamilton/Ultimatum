# Anatomy: making a figure move

Read when a figure should respond to scroll, pointer, keyboard or time.

## One loop

Run a single animation loop for the figure. It reads state, steps it, and writes to the DOM through stored references, never by querying the DOM each frame. Stop the loop when the figure is off screen or the tab is hidden.

## Time

- Clamp the step to at most 1/30 of a second so a stalled tab does not jump.
- Follow targets with an exponential ease: `value += (target - value) * (1 - exp(-rate * dt))`. It is frame-rate independent.
- For things that should overshoot (a lever, a lid), use a real spring with stiffness and damping, not a canned curve.
- Envelopes for events: smooth rise and fall, a burst that decays, a settle that rings once. Use them for lamps, flashes and valves so nothing pops.

## Visibility and arming

- An IntersectionObserver starts and stops the loop. Read the newest entry in the batch, not the first.
- "Arm" a figure only once it is on screen: set initial state without animation, then animate after.

## Reduced motion

Check `prefers-reduced-motion: reduce` at load and on change. In that case show the still version: the object at a meaningful state, the readout still correct, controls still working but jumping straight to the result with no tween. Never leave only a blank frame. Rules: `accessibility-and-limits.md`, `../taste/motion.md` §Reduced motion.

## Idle tour

An idle tour (the figure slowly demonstrates itself) is allowed only if it can be paused, stops on first input, does not run in reduced motion, and ends or loops no longer than 5 seconds before offering a pause (WCAG 2.2.2).

## Controls

- A slider is a real `input type=range`, or an element with `role=slider`, `aria-valuemin`, `aria-valuemax`, `aria-valuenow` and `aria-valuetext`. Write `aria-valuetext` only when the displayed value changes, so a screen reader is not flooded.
- Phase changes (filling, full, draining) go into an `aria-live=polite` region, one short sentence per change.
- Every pointer action has a keyboard equivalent.

## Exploded view

Parts separate along their own axis in a staggered order, the top part first; the return reverses the order. Re-sort depth while parts move, since an exploded gap can change which part is in front. The end states must each be a correct drawing, not only the middle frames.

## Weight

Move transforms and opacity, not geometry rebuilds. If more than a few dozen SVG elements update every frame, switch the busy layer to canvas (`webgl.md`).

Docs: https://developer.mozilla.org/en-US/docs/Web/API/IntersectionObserver and https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
