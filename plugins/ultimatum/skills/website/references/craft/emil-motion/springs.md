# Springs, velocity and momentum

Read when motion follows a pointer, is released with speed, can be interrupted, or needs to feel alive. For fixed-time transitions read `easing-and-duration.md`. Gesture structure is in `gestures.md`.

## When a spring beats a curve

- Drag with release momentum, sheets, swipes.
- Anything the person can interrupt or reverse halfway: a spring keeps its current velocity when retargeted, while a CSS keyframe restarts from zero.
- Decorative pointer following (a tilt or glow that trails the cursor). Smooth the target with a spring rather than writing the pointer position straight in. Only for decoration: never smooth a functional readout.
- Things meant to feel alive, such as a growing pill-shaped status island.

Use a plain CSS transition or keyframe for opacity, colour and short fades with no release gesture. Do not install a library for a fade.

## Two ways to describe one

- Designer form: a visual `duration` plus a `bounce` between 0 and 1. In Motion: `{ type: "spring", duration: 0.45, bounce: 0.15 }`.
- Physics form: `mass`, `stiffness`, `damping`. More control, harder to reason about.
- Apple's own pair is a damping ratio (1 means no overshoot, below 1 overshoots) and a response time in seconds. Response is not a duration: the spring has no fixed end, its settling emerges.
- Docs: https://motion.dev/docs/spring

| Moment | Damping ratio | Response |
|---|---|---|
| Default settle, nothing thrown | 1.0 | 0.3 to 0.4 s |
| Reposition after a drag | 0.8 to 1.0 | about 0.4 s |
| Sheet or drawer release | about 0.8 | about 0.3 s |
| A flick that carried momentum | about 0.8 | 0.3 to 0.4 s |

Rules of thumb

- Bounce only when the gesture itself carried force. A menu that fades in does not bounce; a card that was flicked may, slightly (bounce 0.1 to 0.3).
- The same sheet closed by a button gets no bounce: no force was applied.
- Smaller things need more bounce to read the same; a large view with the same bounce settles slowly and feels heavy.
- A spring that feels strange is usually under-damped: raise damping first.
- In a web page, a pure-CSS bezier can stand in for an iOS-like sheet (`--curve-sheet` in `easing-and-duration.md`).

## Handing velocity to the animation

When a drag ends, the next animation starts at the speed the finger had, so there is no seam.

- Record the last few pointer positions with timestamps during the drag; velocity is distance over time across them.
- Pass that to the spring as its starting velocity. Some APIs take absolute pixels per second; others want it relative to the remaining distance (velocity divided by target minus current).
- Start from the on-screen value, never from the target: on interruption read the live transform and begin there, or the element jumps.
- When the gesture reverses, a new animation that discards velocity creates a "brick wall". Pick a spring implementation that retargets with its current velocity.
- Run X and Y as separate springs; one spring on a 2D distance falls out of step when the two velocities differ.

## Project where it is going

A flick should aim where the motion would end, not where the finger lifted.

```js
// distance a release at `v` px/s would coast with exponential decay
function coast(v, rate = 0.998) {
  return (v / 1000) * rate / (1 - rate);
}
const landing = nearest(snapPoints, pos + coast(releaseVelocity));
```

- Rate near 0.998 is a normal scroll feel; 0.99 is snappier. Snap to the stop nearest the projected point, then spring there with the release velocity.
- Choose commit or reverse from velocity direction, not from position alone.
- Simple alternative used by toast libraries: dismiss when distance passes a threshold or when speed (distance over elapsed milliseconds) beats roughly 0.11 px/ms.

## Soft edges

Past a boundary the element follows less and less, never stops dead.

```js
function resist(overshoot, size, k = 0.55) {
  return (overshoot * size * k) / (size + k * Math.abs(overshoot));
}
```

In Motion, `dragElastic` near 0.2 gives a similar feel. Hard stops read as frozen; rising resistance reads as responsive with nothing further.

## Reduced motion

Direct tracking stays (the person produces the motion). Drop momentum flings, bounce and decorative follow-through; settle with a short opacity or position change instead. Details: `reduced-motion.md`.
