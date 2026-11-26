# Review and audit: a strict pass over existing motion

Read when reviewing a diff or page for motion quality, auditing a whole codebase for motion, or writing fix plans another agent can run. Building new motion starts at `gate.md`; removing it is in `gate.md` § Removing motion. A shorter checklist for pages is the removal pass in `../../../../work/references/design/motion.md` § 9.

Stance: default to flagging; approval is earned. A transition that technically works yet drags, grows from the wrong corner, plays too often or loses frames still counts against the work.

## Ten standards

1. Justified: it answers "why does this move" (`gate.md` § 2).
2. Frequency-matched: none on keyboard or hundreds-a-day actions; reduced at tens a day.
3. Responsive easing: ease-out or a strong custom curve on enter and exit; ease-in on UI is a block.
4. Under 300 ms for interface motion, with per-element budgets from `easing-and-duration.md`.
5. Physically right: trigger-anchored origin (modals exempt), never from `scale(0)`.
6. Interruptible: transitions or springs for rapid or gesture-driven motion, not keyframes.
7. Cheap properties: `transform` and `opacity` (`performance.md`).
8. Accessible: reduced-motion handled, hover gated (`reduced-motion.md`).
9. Asymmetric where deciding: slow deliberate phase, fast response.
10. Cohesive: the personality matches the product; no jarring crossfade where a small blur would bridge.

## Flag on sight

- `transition: all`.
- `scale(0)` entrances, or a pure fade with no initial transform where a small scale fits.
- `ease-in` on any UI interaction; a built-in keyword curve on deliberate motion.
- Animation on a shortcut, palette toggle or 100-per-day action.
- Interface motion longer than 300 ms without a reason given.
- A centred `transform-origin` on something that hangs off a trigger.
- Keyframes on toasts, toggles or anything triggered rapidly.
- Animated width, height, margin, padding, top, left.
- Library shorthand props on a version before acceleration landed, or layout animation on motion that must run through busy script time.
- A parent custom property driving child transforms.
- Movement with no reduced-motion handling; ungated hover motion.
- Symmetric press and release timing on a hold interaction.
- Everything entering at once where a short stagger belongs.

## Fix order, strongest first

1. Delete it. 2. Reduce it (shorter, smaller, fewer properties). 3. Fix the curve. 4. Fix origin and physicality. 5. Make it interruptible. 6. Move to cheap properties or the Web Animations API. 7. Make timing asymmetric. 8. Polish: blur-masked crossfade, stagger, `@starting-style`, spring for alive things. 9. Add reduced-motion, hover gating, cohesion.

## Report format

One table with a row per issue and the columns Before, After, Why, each tied to `file:line`; no running lists of before and after.

| Before | After | Why |
|---|---|---|
| `transition: all .3s` | `transition: transform .2s var(--curve-out)` | list the properties; `all` also moves things nobody intended |
| `ease-in` on a menu | ease-out strong curve | first frames are the ones watched |

Then group remaining notes by impact, highest first, omitting empty tiers: feel-breaking regressions, missed simplifications, performance, interruptibility and timing, origin and cohesion, accessibility. Close with Block or Approve. Block for any feel-breaking regression, motion on a keyboard or frequent action, `scale(0)` or ease-in on UI, or a layout-property animation with an easy cheap fix. Approve when none of those exist, times and curves are in bounds, interruption is handled and reduced motion is respected. When feel is uncertain recommend slow motion, frame stepping and a look the next day instead of guessing.

## Codebase audit

Eight categories:

1. Purpose and frequency (hunt: animation on shortcuts, palettes with open and close, constant hover motion).
2. Easing and duration (ease-in anywhere, bare `ease` or `linear` on entrances, over 300 ms, a tooltip delay and animation on every tooltip in a toolbar).
3. Physicality and origin (`scale(0)`, pure fades, centre origin on anchored panels, pressables with no press state).
4. Interruptibility (keyframes on dynamic UI, fixed-duration tweens in gesture handlers, distance-only dismissal, hard stops at drag limits).
5. Performance (`all`, layout properties, shorthand props on busy pages, variable-driven transforms, loops CSS could do).
6. Accessibility (no reduced-motion, ungated hover, reduced-motion that kills all feedback).
7. Cohesion and tokens (five almost-equal hand-typed beziers; one bouncy piece in a crisp app; list entrances with no stagger; double-exposed crossfades).
8. Missed opportunities (teleporting state, panels with no origin story, flat rare moments; at most a handful).

Method: recon first (stack, motion libraries, existing curve and duration tokens, personality, a frequency map of animated surfaces), then audit per category (read-only sub-passes for large repos), then re-read every cited line yourself and drop anything by design or exempt (centre origin on a modal is correct; length on a marketing page can be fine), then present one table ordered by impact over effort:

| # | Severity | Category | Location | What is wrong | Fix in short |

Severity: high is feel-breaking, medium is noticeably off, low is polish. List two to four missed opportunities separately. Depth: quick (high-traffic components, about five findings), standard (all interactive UI), deep (whole repo including marketing, plus low items). A short list of confident findings beats a padded one; "the motion is already right" is a valid result. Respect motion decisions documented in a comment or design doc.

## Fix plans another agent can run

One plan per finding, self-contained: the executor has no context and no taste.

- Header: number, short imperative title, status, commit hash, severity, category, scope.
- Problem: every location as `path:line` with the current code verbatim.
- Target: exact values (curve, time, spring, media queries). Never "use a nicer easing".
- Repo conventions: where tokens live, plus one exemplar already correct.
- Steps: one concrete edit each.
- Boundaries: files not to touch, no markup change unless a step says so, no new dependencies, stop and report if the code has drifted from the plan.
- Verification: mechanical commands, plus a feel check (what to watch in slow motion, that rapid toggling never restarts from zero, that reduced motion drops movement and keeps opacity) and done-when criteria.
- A plans index with order, dependencies and status; later, re-check plans against current code and retire fixed ones.

Plans never modify source; a separate step executes them and its diff gets this same review.

## Debugging feel

Slow motion at two to five times; frame by frame; check on a real device for touch; check the next day. Look for two colours overlapping, abrupt easing ends, wrong origin and coordinated properties drifting.
