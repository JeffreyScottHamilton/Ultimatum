# Motion vocabulary: naming the effect you want

Read when a request says "make it feel smoother", "add that thing where it slides in" or any other vague motion wish, and you need the exact name before you can build or search for it. The full term list is `../../../../../data/craft/emil-motion/vocabulary.csv` (search it by group).

## Turning a vague wish into a name

1. Restate what the viewer sees in plain words: what moves, from where to where, what triggers it.
2. Find the group in the CSV that matches: `entrance-exit`, `timing`, `movement`, `state-change`, `scroll`, `feedback`, `easing`, `spring`, `loop`, `polish`, `performance`, `principle`.
3. Pick the term, then say it back in one line: "a stagger: items enter 40 ms apart, ease-out, once". If the user says no, the second line of the CSV (`not_to_confuse_with`) usually shows the neighbour they meant.
4. Only then go to the file that builds it: `components.md` for recipes, `choreography.md` for stagger and sequence, `springs.md` for physics, `gestures.md` for drag.

## Pairs people mix up

- Stagger is offset start times; orchestration is the whole plan. A stagger is one tool inside it.
- Crossfade swaps two things in place; a morph changes one thing's shape; a shared-element move carries one thing between two places.
- Scroll reveal fires once when something enters the view; scroll-driven motion follows the scroll position continuously.
- Clip-path hides by geometry with a hard edge; a mask hides with a soft edge. Sliders and wipes want clip-path.
- A tween has a duration you chose; a spring has a feel you chose and a duration it finds.
- Press feedback answers the pointer down; a hover effect answers the pointer's presence and must be gated (`reduced-motion.md`).

## When writing a request for someone else

Give three things: the term, the trigger, the budget. "Scroll reveal on each service card, first view only, 200 ms ease-out, off under reduced motion" can be built and reviewed. "Make the cards pop" cannot.

## Principles worth naming in reviews

Purposeful motion, frequency of use, spatial consistency (leave the way you came), perceived performance (short ease-out feels faster than a long one), anticipation and follow-through (small, never on frequent actions). They are one-liners in the CSV group `principle`; the working rules are in `gate.md` and `easing-and-duration.md`.

## Writing for an agent

When you hand a motion task to another agent, quote the term from the CSV and the property tier it must stay in (`performance.md`). Ask for a recording or screenshots as proof, not an adjective.
