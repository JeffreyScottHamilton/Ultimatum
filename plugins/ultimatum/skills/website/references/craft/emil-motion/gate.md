# Gate: should this move at all?

Read before writing any animation, and again when a page or app "feels slow". Four questions come first; code comes after. Zero lines of motion is a valid result.

Scope: these rules suit product UI (dashboards, menus, dialogs, sign-in, checkout) first. On a marketing or local-business page the house tokens in `../taste/motion.md` and the rules in `../../website/design-rules.md` win; use this file for the question it asks, not for its numbers. The same gate as a short list is in `../../../../work/references/design/motion.md` § 1 and § 9 (merged: nothing here repeats it, this file goes deeper).

## 1. Frequency

| How often a person sees it | Decision |
|---|---|
| Hundreds of times a day (shortcut-opened palette, focus jumps, row hover while scanning) | No motion |
| Tens of times a day (hover, list navigation, tab switch) | Near-invisible: a colour or opacity change under 150 ms, or nothing |
| Now and then (dialog, drawer, toast, settings panel) | Normal motion within the budgets in `easing-and-duration.md` |
| Once, or rarely (onboarding, first success, empty state, booking confirmed) | The only tier with room for delight |

- Anything started from the keyboard is out of the gate, not a judgement call. Repetition turns motion into lag.
- Perceived speed is part of the same decision: a faster spinner, a 180 ms select instead of 400 ms, and a second tooltip that opens instantly all make the product feel quicker with identical load time.

## 2. Purpose, in one word

Name it before building. If you cannot, stop.

- **Feedback**: the interface heard the press.
- **Spatial consistency**: explains where an element arrived from or is heading.
- **State indication**: a change becomes legible (a button that morphs through sending, sent).
- **Bridging a jump**: content that would otherwise teleport, appear or vanish.
- **Explanation**: a demo of how a feature works (marketing and onboarding only).
- **Delight**: only in the rare tier.

"It looks good" on something seen often is not a purpose.

## 3. Function: does motion help or hurt here?

Numbers, charts, tables and prices that a person reads or acts on should not move for style. A chart that redraws from zero on every refresh, a figure that counts up on page load, rows that fade in after each fetch: decoration. Counting from old to new after the user changed something is information. A pointer-following tilt is fine on a landing hero and wrong on a bank balance.

## 4. Budget

If the idea only works as a slow, showy move, it fails. Check against the duration table in `easing-and-duration.md`.

## Finding where motion is missing

Hunt for these seams, then run each candidate through the four questions. Report at most five to seven for a whole app, fewer for one screen, and list two to five candidates you rejected with the question that killed them.

- Pressable things with no `:active` state.
- A destructive action confirmed by a plain click (a hold-to-confirm fill can prevent slips: `components.md` § Hold to confirm).
- Content that swaps, appears or vanishes in one frame: conditional renders, expanding sections, list items added or removed on a screen visited only now and then.
- A panel, menu or popover with no visual link to what opened it.
- A toast or sheet that leaves by a different edge than it came in.
- A grid or list that pops in at once on a page seen occasionally (a short stagger: `choreography.md`).
- A draggable thing that snaps with no physics (`gestures.md`).
- Rare moments rendered flat: first run, empty state, success, booking confirmed.

Sweep terms that find them in code: `{isOpen &&`, `display: none` toggles, `onClick` on elements with no `:active`, `<details>`, drag handlers, `.map(` over entering lists, empty-state and success components.

Output as a table: place, today, purpose, frequency tier, suggested motion with exact values from this folder, then the rejected list, then one paragraph on how much motion this interface actually needs.

## Removing motion

Reverse the burden of proof: an animation stays only if it passes. Walk each one down this order and record the branch that decided it.

1. Started by keyboard: delete.
2. Seen hundreds of times a day (in-app route changes, tab switches, row hovers): delete.
3. On data people read or act on: delete, unless it signals an actual change in value.
4. No nameable purpose: keep only if it is a rare first-time moment; otherwise delete.
5. Named purpose but seen tens of times a day: reduce.
6. Over budget, or a slide or scale where a fade says the same: reduce.
7. Otherwise keep.

Marketing pages get more room (one hero entrance, an explanatory demo). Fade-on-scroll for every section still fails: it holds content back from people who scroll quickly and repeats on every visit.

### Reducing

| Today | Becomes |
|---|---|
| Hover with scale, lift or growing shadow | colour or opacity only, 150 ms or less, plain `ease` |
| Slide or scale entrance on a busy surface | opacity only, 150 ms, ease-out |
| UI motion over 300 ms | 200 to 250 ms, same curve |
| Stagger over 80 ms per item or 300 ms total | 30 ms per item at most, or fade the group as one |
| Infinite pulse, shimmer or glow on something that stays on screen | play once, or keep the still end state |

If the reduced version no longer carries its purpose, delete it.

### Hazards when deleting

- **Hidden start state.** Any keyframe filling forwards from `opacity: 0`, an `initial={{ opacity: 0 }}` prop, or a reveal class waiting on an observer. When you remove the animation, remove its start state too, or the element stays invisible.
- **Code waiting on the animation.** `animationend` or `transitionend` listeners, exit-complete callbacks, timers sized to a duration. Remove the wait, or the UI pauses for motion that is gone. A held-open exit means unmount timing changes: move whatever ran after the exit to the moment of closing.
- **A layout animation masking a shift.** Remove it and the jump shows. Keep it, and log the shift as its own finding.
- **Focus moved in an animation callback.** Move it immediately.
- **Tests waiting on classes or durations.**
- Afterwards delete orphans: unused `@keyframes`, animation utilities, empty presence wrappers, unused variants, motion imports. If a motion library is now unused, propose dropping it; do not uninstall it unasked.
- Also cut: a spinner for work that ends in under about 300 ms (the flash reads as a glitch) and skeleton shimmer for the same.

Report removed and reduced items in a table (place, was, verdict, deciding branch) and list two to five animations kept with the purpose that saved each, plus ones kept but badly built, for the review pass in `review-and-audit.md`.
