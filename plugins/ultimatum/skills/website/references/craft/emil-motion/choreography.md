# Choreography: several things moving together

Read when two or more elements move for the same event: a list that cascades, a hero entrance, views swapping inside one container, a multi-step flow, an item leaving while neighbours close the gap. One element's curve and time are in `easing-and-duration.md`.

Good choreography is mostly cutting moving parts and running the rest in parallel. Order only where order means something. A sequence that works reads as one gesture; one that fails reads as a queue.

## Five rules

1. One entrance per container. A panel that slides in already carries its content; a child cascade on top makes people wait twice.
2. No stagger on frequent or keyboard-opened surfaces (menus, palettes, tab content, rows). Things appear together or not at all.
3. No uniform stagger. Equal delay, distance, time and curve for every item moves like a metronome. Vary by importance.
4. Nothing blocks input. Anything visible can be pressed; a late-arriving item never keeps a button from a hand already on its way.
5. Every sequence survives interruption (below).

## Step 1: cast the elements

| Role | Treatment |
|---|---|
| Lead: the one thing to notice (new view, the item acted on) | moves first, travels furthest, stays longest |
| Support: what follows (subtitle, actions, rest of the list) | shorter, smaller motion after it |
| Decoration: badges, accents, dividers | fade only, or nothing |
| Static: everything else, including containers whose contents move | does not animate |

Two leads means a hierarchy problem that motion cannot fix. Most groups shrink here: a side panel with eight menu rows becomes one move, the panel.

## Step 2: relate each pair

- Same visual object or same moment: move together (a drawer and its content; a chip leaving while siblings close the gap).
- Order carries no meaning: together anyway. Order without meaning is delay.
- Order means something and showing both at once looks broken: sequence, with the second starting just before the first ends.
- Order means something and overlap is fine: overlap, which is a stagger.
- Cannot control a child's path (shared-layout animations): carry. Move the parent and the children come along; images drop into a bin because the bin moves.

### Together

- A leaving element stops taking space at once, so neighbours slide into the gap while it fades. Take it out of flow at removal (`position: absolute` at its current offset inside a `position: relative` parent, then animate it out). In Motion this is `AnimatePresence` with `mode="popLayout"`.
- Swapping views in one container is a crossfade: the old view leaves while the new one arrives, never in series.
- Sub-animations of one component share a time and curve family.

### Overlap: the stagger

- Product UI: 30 to 80 ms between items, total under about 300 ms. In a long list, cascade only the first few rows; the others appear together.
- Marketing and first-run: 100 to 150 ms steps on 500 to 600 ms entrances can read as a wave, since it is seen once per visit.
- Order follows importance, not DOM order. Put a title and its first paragraph on one beat.
- Vary treatment as well as delay: the lead item travels furthest, supporting items travel less, ornaments only fade where they stand. Gaps that get smaller down the list feel organic.
- Direction follows reading order, or radiates from the point of interaction.

### Sequence: when overlap fails

- Two dense views in a container changing both width and height: old leaves, then new enters. To keep a crossfade, render the active view twice; one copy only enters, the absolutely positioned second one only plays an exit keyframe from full opacity, scaled toward where the container is going.
- One element visibly passing through another: delay the front face until items have almost landed.
- Cause then effect: a checkbox box draws, then its tick. Second delay equals first duration, both with `animation-fill-mode: both`. Start the second slightly early.

## Step 3: tie secondary motion to a moment

Each supporting motion hooks to a moment of the lead (start, impact, settle), not to a delay that looks about right.

- Sync to the cause: on a hover-then-click control, the background pulse belongs to the click.
- Accents (sparkle lines around an icon) land in the last fifth of the lead's timeline, most important first, others about 40 ms behind.
- A repeat action skips the build-up: once hover has set the stage, click plays at once.

## Step 4: scale to the change

- Duration by distance. A container resizing between views needs a full fade for a large jump and a very short one for a small jump; clamp it, for example `clamp(.15s, delta / 500 * 1s, .27s)`.
- Bounce by size: smaller elements bounce more.
- With a few known states, hand-tune values per transition. Use a formula only when states are too many to tune.

## Step 5: direction and exits

- Forward content enters from the right and moves left; back reverses. Next and Back sliding the same way contradicts the action.
- A leaving element captures its props at the moment it was removed, so hand the up-to-date direction to the presence wrapper as well as the child (`custom` in Motion); otherwise the exit travels the stale way.
- Exits are simultaneous, shorter and simpler. Never reverse-stagger on close.
- An exit matches its entry: slid in from the right, leaves to the right.
- Small containers or similar views: swap the full slide for a crossfade with an 8 px shift and light blur.

## Interruption checks

- Re-trigger mid-way (hover out halfway, press Next twice, switch menus while one opens). Each run stops in-flight animations first; never stack them.
- Start the next thing only once the previous finished: an idle loop restarts when every reset animation has settled (wait on all their promises together).
- Gate "click works after build-up" with a ref flag, not state, to avoid re-rendering per phase.
- Fast switching can leave two children mounted at once; key each child with something stable and unique.

## Attention loops

An idle hint (a tapping hand, a wiggling icon) starts after about 2.5 s, repeats rarely (about every 6 s), stops during interaction and resumes only after the reset finishes. Under reduced motion, no loop.

## CSS stagger with an index variable

```css
.cascade > * { animation: rise .55s var(--curve-out) both; animation-delay: calc(var(--step, 90ms) * var(--n, 0)); }
@keyframes rise { from { opacity: 0; transform: translateY(12px); } }
@media (prefers-reduced-motion: reduce) {
  .cascade > * { animation: none; }
}
```

- Set `style="--n:2"` per item; items on the same beat share a number.
- `both` hides delayed items before they start and keeps the end state. Leaving out `to` animates to the element's own styles.
- Cap the index for long lists (`--n: min(var(--k), 5)` in markup or script) so item 20 does not wait twenty steps.
- An inherited variable changed on a parent recalculates every descendant; fine for a one-shot entrance, wrong for per-frame values.

## Motion library stagger

Variants with a parent `delayChildren: stagger(0.06, { ease: "easeOut" })` give shrinking delays for free; older versions use `staggerChildren`. `stagger(…, { from: "center" })` radiates out. Give each role its own variant (distance, time); the stagger only sets when each starts. Reach for the imperative `useAnimate` only when many elements answer several events and you need to wait for them; hold the running animations in a list and stop them before launching new ones. Docs: https://motion.dev/docs/stagger

## Output when you plan one

A timeline table (element, role, start, duration, motion, relation), a list of two to five things deliberately left still and why, and one line naming what cannot be judged from code (does the stagger read as a wave, does the crossfade read as one object) with the exact moment to scrub on a recording.

## Reduced motion

Collapse, not just shorten: drop delays and movement, keep opacity, show the group together. If the sequence is the explanation, jump between its frames.
