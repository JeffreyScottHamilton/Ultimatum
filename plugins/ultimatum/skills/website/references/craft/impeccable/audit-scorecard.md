# Technical audit scorecard

Read when you are asked to audit built front-end code (not judge its look) and need a scored, repeatable report across five areas.

This is a code-level pass. It records problems; it does not fix them. The visual and UX review lives in `critique.md`; the page-mode checks and slop tells are in `../design-review-qa/page-modes.md` and `../design-review-qa/slop-tells.md`. Use this file when the question is "is this front end sound?".

## Five areas, each scored 0 to 4

| Area | 0 means | 4 means |
|---|---|---|
| Accessibility | keyboard users or screen-reader users cannot finish the main task | WCAG 2.2 AA met on the paths checked, with no open P1 |
| Performance | the main view janks or shifts on a mid-range phone | Core Web Vitals inside "good" on the checked pages |
| Theming | colours and sizes are hard-coded throughout; dark mode breaks | every colour and size comes from tokens; each theme is designed, not inverted |
| Responsive | content is cut off or scrolls sideways at 320 px | layout restructures cleanly from 320 px to wide screens and at 200% zoom |
| Implementation integrity | the build drifts from its own system and fakes content | the build matches the agreed system and every visible claim is true |

Score 1 to 3 in between: 1 = several blockers, 2 = works but with major gaps, 3 = minor gaps only.

**Total out of 20.** Bands: 18 to 20 ship-ready; 14 to 17 good with fixes; 10 to 13 needs a fix round; 6 to 9 major rework; 0 to 5 not usable. Say which pages and states you scored; a score covers only what you looked at.

## What to look for in each area

**Accessibility** (checks map to WCAG 2.2; see <https://www.w3.org/TR/WCAG22/>):
- text contrast 4.5:1, large text and UI parts 3:1 (SC 1.4.3, 1.4.11); 7:1 only if AAA was asked for;
- every control reachable and usable by keyboard, with a visible focus ring that is not hidden by sticky bars (SC 2.1.1, 2.4.7, 2.4.11);
- focus is trapped inside an open modal dialog and returns to the opener when it closes;
- landmarks and one logical heading outline; native elements before ARIA; ARIA states that match what is on screen;
- alt text that carries the image's information, empty alt on decoration; every field has a programmatic label;
- reduced motion: the reduced path keeps state changes visible. A blanket rule that sets every duration to near zero is a finding, because it also removes feedback.

**Performance:**
- reads and writes of layout interleaved in one frame (layout thrash);
- animations on width, height, top, left or margins where a transform would do;
- large blur, filter or shadow areas repainted every frame; `will-change` left on everything;
- images without width, height or `aspect-ratio` (layout shift), off-screen images not lazy, oversized files;
- script bundle size and needless re-renders in framework code.

**Theming:**
- literal colours where a token exists; tokens from two systems mixed;
- dark mode that only swaps background and text, so secondary text or borders fail contrast;
- a theme switch that leaves stale colours in canvases, charts, iframes or the browser's own UI (`color-scheme`, `theme-color`).

**Responsive:**
- fixed pixel widths on text containers; content that overflows at 320 px; sideways page scroll;
- touch targets: WCAG 2.5.8 sets 24 by 24 CSS px as the AA floor, with spacing and inline-text exceptions; 44 px is the comfortable size to aim for on touch;
- drags or swipes that fight the page scroll; hover-only actions;
- text that cannot grow to 200% without loss (SC 1.4.4) or reflow at 320 px wide (SC 1.4.10).

**Right-to-left, only when the page declares it.** Flag physical properties (`margin-left`, `left`, `border-right`) only where the document or a container sets `dir="rtl"`. Setting `lang` to Arabic or Hebrew is not enough to trigger this check. Centring with `left: 50%` plus a transform is fine in both directions. Arrows and chevrons that mean "next" or "back" should mirror. A worked example is `../../../../../data/craft/impeccable/examples/harden-demo.html`.

**Implementation integrity:**
- components that drift from the system (one-off spacing, colours, radii);
- placeholder or invented content presented as fact (numbers, logos, quotes);
- structure that any product could use unchanged, with nothing tied to this one.

## Severity

Use the shared scale in `../design-review-qa/qa-taxonomy.md` if the report sits beside a QA run. Standalone:
- **P0** blocks the main task or loses data;
- **P1** a WCAG AA failure on a main path, or a major break at a common width;
- **P2** a clear problem that has a workaround;
- **P3** polish. Keep P3s few; a long tail hides the real issues.

## The report

1. **Integrity verdict first**: one or two lines on whether the build is the system it claims to be.
2. **Score table**: five rows, the total and the band.
3. **Findings by severity**, each with: location (`file:line` taken from the file), area, who it hurts and how, the standard (WCAG SC number or metric), and the fix.
4. **Systemic patterns**: the same fault in many places, fixed once at the source (a token, a base style, a shared component).
5. **What works**: the parts to keep, so a fix round does not break them.

Before reporting, re-check each P0 and P1 in the running page or code; drop what you cannot reproduce. Claim only the checks you ran (Ultimatum rule: evidence before claims).

## Native apps

For iOS or Android builds, swap the five areas for: VoiceOver or TalkBack, performance, appearance (Dark Mode, Dynamic Type or font scale), platform conformance, and adaptivity across sizes. Platform conformance is the one to lead with. Rules are in `native-platforms.md`.
