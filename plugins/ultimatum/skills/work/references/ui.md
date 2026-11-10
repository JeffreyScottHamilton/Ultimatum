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

Skip for edits inside an established screen. For new pages or a new visual area, write five lines in the plan and keep them for the final report:

1. Surface mode.
2. Palette roles (ground, ink, accent, state colors) with a reason tied to who uses it and under what light, not to the industry.
3. Type pairing and scale steps (display, h1-h3, body, label, meta, data).
4. Radius and elevation rule (declare once: border OR shadow).
5. One signature move and where it lives; one motion moment.

If a previous card exists in the repo, state how this one differs. Do not default to the same palette, pairing and composition every time.

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
2. Fix them. Re-run. **At most 3 rounds.**
3. Anything still open after round 3 is either fixed by a smaller change you state, or **waived**.

Waiver format, one line each in the report:

`WAIVE <check-id> @ <viewport/selector> -- <reason> -- <who accepts: user/brief>`

Example: `WAIVE tap-target-medium @ 375x812 a.footer-link -- legal links inline in prose -- brief`.

A waiver needs a reason a reviewer could disagree with. "Pre-existing" is a reason only if you also state it was not touched. Never waive a console error, a failed expect, or a P0. The report's UI section lists: direction card (if made), the final `ULT-BROWSER:` line with report path, waivers, and what was not verified (for example "axe not available; fallback coverage only").
