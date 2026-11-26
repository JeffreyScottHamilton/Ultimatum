# Refine moves: polish, simplify, tone down, turn up

Read when an existing page or screen needs refining rather than redesigning, and you must pick the move and keep its identity intact.

The revision verbs and the rule that a redesign keeps content and wiring are in `../../website/design-rules.md` § 5 and `../hallmark/redesign.md`. This file adds how to classify drift, the order of fixes, and what each of four moves changes.

## First rule

A refine keeps the look the product already has. When the underlying idea is the problem, tell the user and offer a redesign; do not slip one in as polish. A clean automated scan proves only that the scan found nothing; it is not proof of quality.

## Classify each fault before fixing

| Kind | Example | Fix at |
|---|---|---|
| Missing token | the same grey typed in six places | add one token, replace the six |
| One-off | a single card with 13 px padding | the card |
| Concept mismatch | a playful bounce in a banking flow | the brief: ask before changing |
| Local defect | a clipped label at 390 px | the element |

Fix at the narrowest level that removes the cause. Promote a value to a token only when it is reused.

## Order of fixes

1. Broken tasks, lost data, misleading or inaccessible parts.
2. Missing states: hover, focus, active, disabled, loading, error, empty, success.
3. Flow, hierarchy, responsive breaks, drift from the system.
4. Visual detail and motion.
5. Code tidy-up: debug output, dead code, unused styles.

Walk the whole path a user takes; do not perfect one corner while the next screen is broken.

## Polish

- Match the habits of neighbouring screens: how saving works, where actions sit, optimistic or wait-for-server.
- Align optically, not just by box: icons beside text, play triangles, round shapes at an edge.
- Check translated lengths, 200% zoom and the moment fonts swap in.
- Give images dimensions or `aspect-ratio` so nothing shifts as they load.
- Make motion interruptible: a second click mid-transition must not queue or jump.
- Try long, missing, slow, offline and no-permission content (see `harden.md`).
- Use one term per idea across the product.
- Ask before changing any claim.
- Re-walk with mouse, keyboard and touch at a phone, a mid and a wide width; check the console, layout shift and response time.
- End with a clean diff: no stray logs, commented code or one-off values left behind.

## Simplify

Find where the complexity comes from: too many elements, too much variation, too much at once, decoration, flat hierarchy, features nobody uses.
- Name the one main goal of the view. Remove or move what does not serve it.
- One primary action per view; merge actions that do the same thing.
- Disclose detail on demand instead of showing every option.
- Colour: one or two brand colours, neutrals, and status colours that also carry a non-colour cue.
- Type: one family, three or four sizes, two or three weights.
- No cards inside cards; space alone often groups better than a box.
- One alignment, one spacing scale, a linear reading order.
- Smart defaults; edit in place instead of a modal; cut steps.
- Copy says each thing once, in active voice.
- In code, delete dead styles and cut component variants to the few that cover most uses.

Do not remove what someone needs to decide, recover or reach the feature by keyboard. A hidden feature is not a simple one. Record what was removed and where it now lives.

## Tone down

Find the loud parts: saturated colour, extreme contrast everywhere, too many heavy weights, large dramatic motion, busy decoration, everything big.
- Lower saturation and use colour as an accent on mostly neutral ground; tint greys slightly toward the brand hue.
- On a coloured background, darken or tint the text from that colour rather than using grey.
- Step weights down (900 to 600, 700 to 500) and shrink the gaps between sizes.
- Thin or remove borders; remove effects that do no work (extra shadows, glows, large blurs).
- Shorten motion distances and drop decorative animation; never bounce.
- Even out spacing and bring stray elements back to the grid.

Keep hierarchy, some colour, the brand's character and clear controls. Toned down is not grey, flat or anonymous.

## Turn up

The page reads flat. Keep the scope the user named; everything else stays as is.
- Amplify what the system already owns (its motif, its type scale) rather than adding new colours or faces.
- Make one decisive move completely, then let the surroundings support it.
- Give the target its own pace in the scroll: a change of density or scale that reads as a peak.
- Keep every claim and every working control as it was.

Check: outside the target nothing changed; no new primitive appeared; the section is still clearly the same brand.
