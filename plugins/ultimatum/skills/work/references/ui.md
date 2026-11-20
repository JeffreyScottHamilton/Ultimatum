# UI route

Goal: an interface that fits the product's existing language, works with real content and a keyboard, and is proven in a browser. Order: **context, surface, direction card (new work only), build to the craft floor, verify, critique gate.** Verification details are in `browser-verification.md`; React specifics in `react.md`.

## 1. Find the incumbent language first

Before writing UI, spend a few searches (`ult search`, `ult symbols`) on:

- design context docs (PRODUCT.md, DESIGN.md, a style guide, Storybook), token files (`tokens.css`, theme config, tailwind config, CSS variables);
- existing components that already do the job (button, dialog, toast, form field, table). Reuse or extend them; never fork a look-alike;
- 2-3 existing screens: spacing rhythm, type scale, radius, how errors and empty states are phrased.

Rules:
1. **Existing identity is evidence.** A refinement keeps it. Only an explicit redesign request treats the old look as something to replace (replace wholesale; do not half-polish it).
2. **Tokens before literals.** Use the project's variables. A raw hex or pixel value that has a token is a defect. If a needed token is missing, add it where tokens live, not inline.
3. **Three or more uses** of the same pattern justify extracting a component; two do not.
4. **The brief wins.** A font, palette, era or material the user pinned is used even if it resembles a "generic" tell below.
5. **shadcn projects** (`components.json` exists): read it, list the ui directory, and compose from installed components with semantic tokens. Adding components via `npx shadcn ...` downloads code, so ask the user first; without approval, write the component by hand in the same style.
6. Real content before polish: actual labels, data shapes and states. No lorem ipsum, invented customers, metrics, prices or testimonials. Mark any assumed value in the report.

## 2. Classify the surface

Say one line: **Persuade** (landing, pricing, marketing), **Operate** (app, dashboard, editor, admin), **Read** (docs, articles), **Experience** (portfolio, gallery, showcase). Classify the requested surface, not the product category: a developer tool's landing page is Persuade; a fashion brand's docs are Read.

- Persuade / Experience: commit to a point of view and one memorable moment.
- Operate / Read: standard controls, familiar navigation, stable density. Personality comes through type, palette, density and one signature detail, and never hides task, state or a known affordance.
- Marketing-page habits (big hero, one idea per screen, scroll choreography) apply to Persuade only. Do not bring them into Operate.

## 3. Direction card (new surfaces only)

Skip for edits inside an established screen. For new pages or a new visual area:

**First, sketch three directions, one line each, each from a different source in section 3a** (for example: one from a domain artifact, one from a material or era, one from a structural constraint). Run the **swap test** on each: replace the product name with a competitor's; if the direction still fits unchanged, it is generic, so drop it or sharpen it. Pick the strongest survivor and say in one line why it beat the others. Your first idea is usually the average of every similar page, so it is a candidate, never the default.

Then write the card, six lines, in the plan, and keep it for the final report:

1. Surface mode.
2. **Concept:** one phrase the whole surface obeys (for example "a well-kept field notebook", "an airport departure board", "a printed train timetable"). Every later choice should be explainable by it.
3. Palette roles (ground, ink, accent, state colors) with a reason tied to the concept, who uses it and under what light, not to the industry.
4. Type pairing and scale steps (display, h1-h3, body, label, meta, data), with a reason from the concept.
5. Radius and elevation rule (declare once: border OR shadow).
6. One signature move and where it lives; one motion moment.

**Do not repeat yourself across projects.** Append each card, with the date and surface, to `.ultimatum/ui-directions.md` (Ultimatum's own state, ignored by git). Before writing a new card, read that file if it exists, and change at least the concept, the display typeface and the accent hue from the last two cards, unless the brief or the project's existing identity pins them.

### 3a. Sources of distinctiveness

Uniqueness comes from specifics, not from effects. Draw on these, in roughly this order:

- **The domain's own artifacts.** What do people in this field already look at: maps, receipts, scorecards, lab labels, sheet music, shipping manifests, film slates? Borrow its structure, rules, type habits or color coding, never a clip-art picture of it.
- **The real content as the graphic.** The product's own screenshots, data, timetable, menu, code or photos, shown large and precisely, beat any decorative illustration. A real chart of real numbers is a better hero than an abstract blob.
- **Typography as the voice.** For Persuade and Experience, choose a display face with a real character (a grotesk with quirks, a condensed or wide cut, a sharp serif, a humanist sans) instead of whatever the framework ships with. Pair it with a quiet, highly legible text face. Use contrast in size boldly: a very large display step against modest body text is cheaper and more memorable than any effect. In Operate and Read, keep the text face practical, and let the voice live in headings, numerals and labels.
- **A specific color source.** Take the palette from a named reference (a material, a place, a printed object, a time of day), build its scale in OKLCH so lightness steps are even, and add one accent that is used sparingly. Two or three committed colors read as more intentional than a full rainbow of tints.
- **Composition with tension.** An asymmetric grid, a column that breaks the margin, content that bleeds off the edge, a strong change of scale between neighbors, generous empty space used on purpose. Keep the grid; break it once, deliberately.
- **A structural constraint.** For example: only rules and type, no boxes; one color plus black; everything aligned to a visible baseline; all motion horizontal. A constraint forces original solutions and keeps the surface consistent.
- **Detail at the edges.** Tailored focus rings, selection color, custom scrollbars where appropriate, the empty state's illustration or copy, the 404 page, the favicon, loading skeletons shaped like the real content. Users notice these, and generators almost never do them.
- **Copy with a point of view.** Specific, concrete sentences in the product's own voice, with real numbers and names. Copy is the cheapest way to be different.

Never trade usability for novelty: labels stay readable, controls stay recognizable, contrast and focus rules in section 4 still hold.

## 4. Craft floor (check on the rendered result)

- **Layout:** related items tight, groups separated, more space above a heading than below. One primary action per view. Reading width 45-75 characters for body copy. `min-width: 0` on flex/grid children that hold text. Use `100dvh`, not `100vh`, for full-height mobile layouts.
- **Type:** a role-based scale with visible steps; tight leading only on display sizes; tracking on display no tighter than about -0.04em; tabular numerals for changing numbers; `text-wrap: balance` on headings.
- **Color:** body and placeholder text at least 4.5:1, large text 3:1, UI boundaries and focus indicators 3:1. Tint secondary text from the surface hue, not neutral gray. Meaning never by color alone. Check light and dark if the project has both.
- **Spacing:** read computed values, not class names. Use the project's spacing scale.
- **States, every interactive piece:** default, hover, focus-visible, active, disabled, loading, error, empty, success. Lists need an empty state with a next action. Forms need inline errors that name the problem and the fix.
- **Long and odd content:** 80+ unbroken characters, 0/1/1000 items, missing image, RTL/CJK, 200% zoom, 320 px width. Truncate with intent (ellipsis plus accessible full text), never clip silently.
- **Focus and keyboard:** every control reachable by Tab in reading order, visible focus ring, Escape closes overlays, focus moves into a dialog and returns to the trigger on close. Prefer native elements (`button`, `a`, `dialog`, `details`) over ARIA reconstructions.
- **Touch:** targets 44x44 CSS px where possible; 24x24 is the hard floor. Inputs 16 px+ font to avoid iOS zoom. `@media (hover: hover)` around hover-only styling.
- **Browser surfaces:** `color-scheme`, `accent-color`, `::selection`, caret color, `theme-color`, a real favicon. Cheap, and their absence reads as unfinished.
- **Copy:** buttons say verb + object. Errors say what happened and what to do. One idea, said once.
- **Modals:** use only when interruption or a focus trap is needed. Otherwise inline or popover.
- **Reduced motion:** honor `prefers-reduced-motion` (see section 5).

## 5. Motion rulebook

Decide in this order and stop at the first "no":

1. **Frequency.** Used hundreds of times a day (keyboard-triggered results, palette toggle): no animation. Tens of times (hover, list navigation): nearly none. Occasional (dialog, drawer, toast): standard. Rare or first-run: may delight.
2. **Purpose.** One of: spatial continuity, state change, explanation, feedback, softening an abrupt change. "Looks nice" is not a purpose for something seen often.
3. **Easing.** Enter/exit: ease-out. Moving between on-screen positions: ease-in-out. Hover/color: ease. Progress or loops: linear. Never ease-in on UI. Prefer a strong custom curve to the built-ins, for example `cubic-bezier(0.23, 1, 0.32, 1)` for out.
4. **Duration.** Press feedback 100-160 ms; tooltip/small popover 125-200 ms; dropdown 150-250 ms; dialog/drawer 200-400 ms. UI motion under 300 ms unless explanatory.
5. **Physicality.** Never `scale(0)`; enter from 0.95-0.97 plus opacity 0. Popovers scale from their trigger (`transform-origin`); dialogs stay centered. Pressable elements dip to about 0.97 on `:active`.
6. **Interruptibility.** CSS transitions retarget mid-flight; keyframes restart. Use transitions for anything that can be toggled quickly; `@starting-style` for entry. Springs only for gestures and pointer-tracking, low bounce.
7. **Performance.** Animate `transform` and `opacity`. List properties explicitly: never `transition: all`. In React, write per-frame values to a ref's style, not to state. `will-change` only after a measured problem, removed at rest.
8. **One authored moment** per surface. No identical fade-up on every section, no scroll-triggered stock reveals, no parallax on text, no scroll-jacking.
9. **Reduced motion** keeps the state change and hierarchy via crossfade or instant swap. Do not blanket-set every duration to zero; do not remove focus or progress indication.
10. **View transitions** (cross-document or `document.startViewTransition`): use for navigation continuity, name only elements that persist, and give a no-op fallback where unsupported (see `react.md`).

When reviewing motion, output a table: Before | After | Why, one row per issue, with exact values.

## 6. Anti-generic tells (defaults to avoid; the brief can earn any back)

- Pages built from identical icon + heading + text cards; cards nested in cards.
- The hero of one big number, a small label and three supporting stats.
- A small uppercase kicker above every heading; numbered sections with no sequence meaning.
- Gradient-filled text, decorative blur/glass, colored glow halos, offset hard shadows outside a deliberate neo-brutalist world.
- A colored stripe down the left edge of cards or alerts; thin border plus huge soft shadow.
- Emoji or text glyphs standing in for icons; mixed icon stroke weights.
- A violet/indigo gradient accent by default; cream background plus serif as the default "warm" look.
- Monospace as costume instead of for code and data.
- Dark theme chosen because the product is "technical", not because of the user's setting.
- Filler copy words in place of facts: seamless, robust, powerful, effortless, unlock, elevate, leverage, supercharge, cutting-edge. Stock lines like "ready to transform your workflow". "Not just X, it's Y" repeated. Replace with the specific fact, or delete.
- Spacing and radius that are all one value; identical shadow on every surface.

## 7. Audit rubric (review-only tasks: findings, no edits unless asked)

Score each dimension 0-4 (0 broken, 2 partial, 4 solid), citing evidence (`file:line`, computed value, or `ult-browser` finding id):

| Dimension | Looks at |
|---|---|
| Accessibility | names, contrast, focus, keyboard, landmarks, headings, reduced motion |
| Performance | layout shift, render-blocking, image sizes, animation cost, bundle |
| Theming | tokens vs literals, dark mode, state colors |
| Responsive | 320-1440, overflow, touch targets, safe areas |
| Integrity | design-system drift, one-off components, decorative filler, copy-paste repeats |

Severity: **P0** blocks the task or is inaccessible; **P1** major or WCAG AA failure; **P2** minor; **P3** polish (keep few). End with what is good, and the 3 highest-value fixes. Run the mechanical evidence pass (browser) separately from the design-judgement pass when a subagent is available; if both happen in one context, say "single-context review".

## 8. Sensitive pages

A page that gates data or actions (login, billing, admin, delete, role changes, uploads) is not done when the UI hides the control. Verify the server enforces it: call the endpoint without the session, with another user's id, with a lower role. Hidden buttons, disabled inputs and client redirects are not controls. Read `security/secure-implementation.md` and add a negative test. Inspect cookies/session handling per `browser-verification.md` section 9.

## 9. Critique gate (bounded)

After building and verifying, run the gate on the changed surface:

1. Run `ult-browser` (and manual checks from `browser-verification.md`); list failures by id.
2. For new surfaces, look at full-page screenshots at desktop and 375 px width and run the **distinctiveness check**, counting each failure like a check failure:
   - **Swap test:** with the product name replaced by a competitor's, would the page still fit? If yes, it is generic.
   - **Memory test:** name the one thing someone would remember tomorrow. It should be the signature move from the card. If you can't name one, or it is a section 6 tell, it fails.
   - **Squint test:** with the screenshot blurred, are the primary action and the hierarchy still obvious?
   - **Card check:** does the result follow the concept, or did it drift back to defaults while building?
3. Fix them. Re-run. **At most 3 rounds** (the checks from steps 1 and 2 share this limit).
3. Anything still open after round 3 is either fixed by a smaller change you state, or **waived**.

Waiver format, one line each in the report:

`WAIVE <check-id> @ <viewport/selector> -- <reason> -- <who accepts: user/brief>`

Example: `WAIVE tap-target-medium @ 375x812 a.footer-link -- legal links inline in prose -- brief`.

A waiver needs a reason a reviewer could disagree with. "Pre-existing" is a reason only if you also state it was not touched. Never waive a console error, a failed expect, or a P0. The report's UI section lists: direction card (if made), the final `ULT-BROWSER:` line with report path, waivers, and what was not verified (for example "axe not available; fallback coverage only").
