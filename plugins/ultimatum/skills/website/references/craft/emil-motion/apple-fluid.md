# Fluid interface principles, applied on the web

Read when a drag, sheet, card or switch must feel physical, or when you design translucent bars and sheets. The mechanics are in `springs.md` (velocity, projection, soft edges) and `gestures.md` (track and release). This file holds the principles behind them plus the parts they do not cover: depth, multi-sense feedback, type and process.

## Seven rules of feel

1. Respond at once. Show the pressed state on pointer down, commit on pointer up; delay nothing you can show immediately.
2. Track 1:1 while the finger is down. No easing between finger and object.
3. Stay interruptible. A new touch during motion takes over from where the object is now, with its current velocity.
4. Prefer behaviours to scripted clips. A spring describes how the thing acts; a keyframed clip describes one path.
5. Hand velocity across the seam between drag and release.
6. Aim at where the gesture is going, not where the finger stopped (`springs.md`, projection).
7. Keep space consistent. What leaves by the right comes back from the right; a menu grows from its button.

## Gesture details

- Tap: highlight on down, commit on up, allow cancel by dragging away and back, give the target about 10 px of forgiving padding.
- Drag: ignore the first small movement (about 10 px) until the direction is clear, then follow 1:1.
- Watch every plausible gesture at once from the first move and drop the losers when intent is clear. Events that fire only at the end ("swiped left") discard the tracking you need.
- Double-tap detection delays single taps. Pay for it only where double-tap exists.
- Hint with motion in the direction the gesture will go (a small nudge or peek).

## Smoothness is what is in the frames

Keep the per-frame jump small enough not to strobe; very fast motion reads better with a faint stretch or blur than with a hard streak. Use `transform` and `opacity` (`performance.md`).

## Translucent depth

- Bars, toolbars and sheets can be a blurred, semi-transparent layer with content scrolling beneath it. Use `backdrop-filter`; it is costly on large areas, so keep the surface small and test on a mid-range phone.
- Darker or heavier material marks structure (a sidebar); lighter material draws attention to controls. Never put a light translucent layer on another light translucent layer.
- Bigger surfaces read as thicker: more blur, deeper shadow.
- Dim and push back for a blocking modal task. A parallel, non-blocking panel gets translucency and offset but no scrim.
- Text over blur needs contrast: heavier weight, near-solid colour, small tracking increase. Put colour on a solid layer.
- Prefer a faded edge where content meets floating chrome over a one-pixel divider.
- To make glass arrive, animate blur radius and scale together, not opacity alone.
- Under `prefers-reduced-transparency: reduce` make the surface solid; under `prefers-contrast: more` add a defined border. Both are in `reduced-motion.md`.

```css
.toolbar {
  background: rgb(255 255 255 / .62);
  backdrop-filter: saturate(170%) blur(16px);
  border-top: 1px solid rgb(255 255 255 / .35);
}
@media (prefers-reduced-transparency: reduce) {
  .toolbar { background: #fff; backdrop-filter: none; }
}
```

Never stack the glass look on every card of a local-business page: the anti-generic list in `../../website/design-rules.md` (section 2) already bans glow and glass as defaults. Use it for a floating bar or sheet that truly overlaps content.

## Several senses at once

- Cause: the feedback fires on the real event (the toggle flips, the item snaps home).
- Harmony: sight, sound and haptic arrive in the same frame. A transition that lags the sound breaks the illusion.
- Utility: reserve sound and vibration for commit, success, error and snap. Anything more trains people to ignore it. Sound never autoplays and always has an off switch; vibration needs a user gesture and is absent on many devices.

## Type that changes with size

Tracking tightens as size grows and loosens slightly at small sizes; line height is tight on headings and looser on body; hierarchy comes from weight, size and leading together; spacing in `rem`/`em` so larger user text does not break the layout; start from the system font unless the brand needs one (`../taste/system.md` decides on brand pages).

## Principles for the product around the motion

Purpose (decide what not to build), agency (undo over confirm, confirm only irreversible actions), responsibility (ask for permission at the moment of need), familiarity (same look, same behaviour, same place), flexibility (many abilities and devices), simplicity (fewer steps, not hidden things), craft (nothing random) and delight as the result. Four feedback kinds: status, completion, warning, error; validate inline. Every screen answers where am I, where can I go, what is here, how do I leave.

## Process

Build the interactive version early; a working demo sets a bar no static mock can. Design visuals and motion together. Review in slow motion and frame by frame with fresh eyes (`review-and-audit.md`).
