# Interaction kit: details

Read when you build or review an animated component, or when `ult kitlint` reports something. It covers what the linter checks, how to fix each finding, and the finishing details a source scan can't see.

## What `ult kitlint` checks

Run `ult kitlint <files or folder>` (add `--json` for machine output, or `--strict` to fail on warnings too). It reads source text, so treat it as a fast screen before the browser check, not a replacement for one.

| Rule | Level | Finds | Fix |
|---|---|---|---|
| `reduced-motion` | fail | A file that imports motion or uses CSS animation but never checks reduced motion | Call `useReducedMotion()` and swap movement for a fade or an instant change, or use `motion-reduce:` utilities. |
| `transition-all` | fail | `transition-all`, or `transition: all` | Name the properties (`transition-colors`, `transition-[transform,opacity]`). Animating everything picks up layout changes and stutters. |
| `will-change-all` | fail | `will-change: all` | Name one or two properties, and only on elements that really animate. |
| `raw-colour` | fail | Hex, `rgb()`, `hsl()` or `oklch()` literals in a component | Use a theme token class (`bg-primary`, `text-muted-foreground`). A hex value on a mask line is allowed, because only its alpha is read. |
| `press-scale` | fail | A `whileTap` or `active:scale` below 0.95 | Press at 0.95 to 0.98. Anything smaller reads as a squash, not a press. |
| `click-target` | fail | `onClick` on a div, span, li, img or motion element with no role and key handler | Use a `<button>`. If it must stay a div, add a role and `onKeyDown`. A backdrop marked `aria-hidden` is fine when Escape also closes. |
| `icon-label` | fail | A button with no visible text and no `aria-label`, `aria-labelledby` or `title` | Add `aria-label` that says what it does ("Close", "Copy link"), and mark the SVG `aria-hidden`. |
| `focus-hidden` | fail | `outline-none` with no focus style beside it | Add a two-pixel ring in the `ring` token on `focus-visible` (the kit's `focusRing` in `cn.ts`). A field inside a wrapper that draws `focus-within:` is fine. |
| `presence-initial` | warn | `AnimatePresence` without `initial={false}` | Add `initial={false}` so things already on screen at load don't play their enter animation. |

To keep a finding on purpose, put `kitlint-ok: RULE reason` in a comment on that line or the line above. Always give the reason. A silenced rule with no reason is a finding in review.

Exit codes: 0 when clean, 1 on any failure (or any warning with `--strict`), and 2 for a path that doesn't exist.

## Details the linter can't see

Check these by eye, or in the browser check.

**First paint is still.** Nothing on screen at load should animate in except the one showpiece. That is why `presence-initial` exists. The same goes for counters below the fold: start them when they come into view, once.

**Icon swaps stay in place.** When an icon changes (copy to tick, sun to moon, play to pause), cross-fade it with a slight scale (about 0.8 to 1) and a short blur in the same box. Don't slide it, and don't let the button change width.

**Numbers don't jump.** Any number that changes (counters, timers, prices, scrub values) uses `tabular-nums`, so the digits keep their width and the layout stays still.

**Labels don't shift the layout.** A button that moves between Save, Saving and Saved keeps one width. Reserve space for the longest label, or stack the labels in one grid cell.

**Hit areas are bigger than the drawing.** A 16px icon gets a 40px target. Extend it with padding or a pseudo-element rather than a bigger icon.

**Images get an edge.** A photo on a light card needs a faint inner outline (`ring-1 ring-inset ring-foreground/10`) so its edge doesn't melt into the card.

**Text renders crisp.** Set `antialiased` once at the root, so light text on dark doesn't look heavy on macOS.

**Springs for touch, eases for state.** Anything that follows a finger or a pointer (drag, tilt, magnet, dock) uses a spring, so it can be interrupted. Colour and opacity changes use a short ease (150 to 200ms). The kit's two springs are in `cn.ts`.

**Decoration stays quiet for assistive tech.** Beams, shimmers, glows and marquee copies are `aria-hidden`. Text that scrambles, reveals or counts has its final value available to screen readers from the start.

**Every gesture has a button.** Swipe has two buttons, drag-to-reorder has move buttons, hold has Space or Enter, and drag-to-close has Escape and a close button.

**Pointer effects are mouse-only.** Tilt, magnet, spotlight and dock magnification check `pointerType === "mouse"`, or a fine pointer. On touch they would fire on every scroll.

## Review order

1. Run `ult kitlint` and fix every failure.
2. Render with reduced motion on. Everything should still work and still make sense.
3. Go through the whole page with the keyboard only. Focus should be visible at every step and return to its trigger after every overlay.
4. Check dark mode and a 390px width.
5. Run axe (the kit's `gallery/check.js` shows how).
