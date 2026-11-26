# Hallmark principles: the floor, the flow and the one idea per screen

Read first when a build should look designed rather than generated: it holds the hard floor, the order of work and the questions asked once. Rebuilt in our own words from the MIT-licensed Hallmark skill (nutlope/hallmark); the house rules in `../../website/design-rules.md` still win on any conflict.

## The aim

- Beat the defaults every model falls into, deal a direction so two builds in a row differ, and give each screen one idea set big.
- Above the floor the page belongs to the designer. The floor is short; the gates (`gates.md`) are long.
- Beyond the source: the buyer's job on a local site (call, book, quote, visit) and on an app (sign up, price, dashboard, checkout) sets the page's anatomy, see `anatomy.md`.

## The floor (never waived)

1. Every colour and every font family is a token declared once at `:root`; none appears as a literal after the token block.
2. No `transition: all`; never animate `width`, `height`, `top` or `left`.
3. One italic word inside a roman heading is banned.
4. `overflow-x: clip` on `html` and `body`; never `hidden`, never a `100vw` width.
5. Image grid tracks are `minmax(0, 1fr)`; display heads take `overflow-wrap: break-word; min-width: 0`.
6. Every interactive element has `:focus-visible`, shown at once with no fade.
7. Every animation has a `prefers-reduced-motion: reduce` answer; content shows with scripting off.
8. No invented metric, quote, logo wall or case-study count.
9. No eyebrow; no label, caption, table head, tag or nav link in tracked capitals or small caps. These use the body face a step smaller, in sentence case, untracked.
10. No middle-dot meta strings, no arrow glued to link text, no decorative status dot.
11. No purple-to-blue gradient, card in a card, emoji as an icon, or hand-drawn browser or OS window.
12. Headline, one sentence and the main action all sit inside 1280×800 without scrolling.
13. About 80 words a screen; the hero text is a headline, one sentence and its actions.
14. A capped, centred container: at 1920 the gutters grow, the measure and grids do not.
15. A first-line CSS stamp naming the build, then a critique line, then any waivers (`gates.md` § Stamp, waivers and answers).
16. Where a render tool exists, run the lint and fix every hard failure before handing back (`quality-gate` rules in `../taste/quality-gate.md` cover our Playwright route).

Merged: items 2, 3, 6, 7, 8, 9, 10, 11 repeat our anti-generic lint (`../../website/design-rules.md` § 2); we keep one copy there and the numbers here.

## Order of work

0. **Pre-flight:** read the project first (design file, brand spec, fonts, palette, spacing, motion library, framework, a runnable product). Report what is kept and what is added. See `flow-branches.md` § Pre-flight edge cases.
1. **Ask once:** material, audience, use, tone (below). A prompt that answers all four, or a headless run, asks nothing.
2. **Shape:** inventory the material, name the visitor's job, design the page, then name its shape (`page-shapes.md`).
3. **Direction:** the user's named theme, else a custom design when asked, else a dealt theme (`themes.md`).
4. **Load** only the files the build needs: layout, anatomy, imagery, craft, genre, theme, gates.
5. **Picks block** once, as the user's redirect window (below).
6. **Build:** scaffold tokens, hero first and checked, then the sections, then the log.
7. **Sweep:** lint, judged gates, a fresh-context review, the material ask. Budget: one batch of inspection, one batch of fixes, at most one confirming round.

## Ask once

One message, even for a five-word prompt. Four questions, material first because it shapes everything:
1. **Material:** what can the page show? Screenshots or a screen recording (or a URL or folder to run and capture), real photos, real numbers, a named quote, logos that may be used. Without photos, stand-ins from a photo library are placed in slots and credited; a number, quote or logo is never invented.
2. **Audience:** who uses it and what do they care about.
3. **Use:** the one action the page drives.
4. **Tone:** choose an extreme (editorial, brutalist, soft, utilitarian, luxury, playful, technical, austere); "clean and modern" is not a tone. Add the vibe in 4–8 words and an anchor colour if there is one.

Skipped answers are opt-outs: infer them, state the inferences in one line, stamp them. Facts are never inferred: a missing number, quote or logo is absent and a missing picture is a stand-in in a slot. For our local sites also ask the business facts that `../../intake.md` covers before this list, and do not ask twice.

## Shape, signature and the mirror test

- **Material inventory, one line:** real (name, claim, numbers, places, dates, images), pictures (and where each comes from), absent (every proof the page will not have). A page with pictures leads with them; a page about words carries type and facts.
- **Signature:** the one thing a visitor would remember, made from the prompt's strongest real thing at its best: the photograph that is the place, the product doing its one job, a price set huge because it is the offer, a control to try. Show it on the first screen. A number drawn as a row of marks is a device, not a signature.
- **Mirror test:** would a neighbouring prompt in the same category get this exact combination of shape, hero, nav, footer and first section? If yes, change one decision and say which.
- **Genre, silently:** AI tools, music, video, dark pages lean atmospheric; SaaS, API, developer tools lean modern-minimal; playful, kids, community lean playful; the rest, editorial. Once a theme is dealt its genre wins (`genres.md`).
- **Scope:** a prompt naming one element is a component; a screen people work in is an app screen (`flow-branches.md`).

## Picks block (said once)

Rows: shape (and the genre and job), theme, chrome (nav and footer), hero posture, signature, section list, material (real, pictures, absent), sweep outcome. Then one quiet line offering a locked design file. A custom run swaps the theme row for its own rows (`direction.md`). A fabricated pass is itself slop; write only what was run.

## Rules that survive every tool

- If the plan has been restated twice, stop narrating and build.
- Never write a gate count that was not verified.
- If a referenced file will not load, proceed on the floor and name the file.
- Long sessions compact: the stamp and the log are the durable memory; re-read them.
- Where a step names a tool the harness lacks, do the intent with what exists; the tool is optional, the check is not.
