# Adapting to devices, inputs, print and email

Read when a design made for one context must work in another: phone to desktop, mouse to touch, screen to print, or web page to email.

Breakpoints, units, safe areas and table handling are in `../hallmark/responsive.md`; phone-specific feel fixes are in `../emil-motion/mobile-web.md`. This file adds input detection, the per-context strategy and the checks for custom controls. For native apps see `native-platforms.md`.

## Ask three things first

1. What was it built for, and what did that assume (a big screen, a mouse, a fast link)?
2. What is the new context: device, input, screen, connection, how long people stay, what they expect there?
3. What will not fit, what will not work (hover on touch, small targets) and what feels foreign there?

## Detect input, not screen size

A small window can have a mouse and a laptop can have a touchscreen. Use interaction media features:

```css
@media (hover: hover) and (pointer: fine) { .row-actions { opacity: 0; } .row:hover .row-actions { opacity: 1; } }
@media (pointer: coarse) { .row-actions { opacity: 1; } .control { min-block-size: 44px; } }
```

`any-pointer` and `any-hover` ask whether any attached input can do it. Never put a needed action behind hover alone. Reference: <https://developer.mozilla.org/en-US/docs/Web/CSS/@media/pointer>.

## Per context

**Phone (from desktop).** One column; actions within thumb reach near the bottom; disclose secondary content in tabs or accordions; bottom sheets instead of small dropdowns; body text at least 16 px (smaller inputs make iOS Safari zoom on focus).

**Tablet.** Two panes (list and detail), side panels, layouts that change with orientation; support touch and a pointer at the same time.

**Desktop (from phone).** Use the width with several panes and persistent navigation, but cap line length and content width. Add keyboard shortcuts, right-click menus, multi-select with Shift, and drag where it helps. Show more up front.

**Print.**
```css
@media print {
  nav, .site-footer, button, video { display: none; }
  a[href^="http"]::after { content: " (" attr(href) ")"; }
  h2, h3 { break-after: avoid; } figure, tr { break-inside: avoid; }
  @page { margin: 2cm; }
}
```
Expand collapsed sections, use dark text on white, and give charts a print-safe version.

**Email.** About 600 px wide, one column, inline styles and table-based layout for older clients; big obvious buttons; no hover; link out to the site for anything complex. Many clients strip `<style>` blocks or ignore modern CSS, so test in the clients you target.

## Techniques

- Grid and flex to reflow; container queries when one component lives in several widths (<https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries>).
- `clamp()` for fluid sizes between a floor and a ceiling.
- Breakpoints where the content breaks, not at device names.
- `display: none` still downloads hidden images; load per context with `srcset`, `sizes` and `<picture>` instead.
- Safe areas: `viewport-fit=cover` in the viewport meta plus `env(safe-area-inset-*)` padding.
- Keep the same information architecture across sizes; only the arrangement changes.

## Custom controls on touch

A slider or drag strip can look right in an emulator and still fail on a phone. For each one:
- tap it, then drag it with the target input, and confirm it responds;
- swipe along the page's scroll axis across it: the page must scroll, not the control;
- run the interrupted cases in `harden.md` § Interrupted gestures.

Name the evidence source in the report (emulation, synthetic touch and its engine, or hardware). Emulators miss real touch, CPU limits, font rendering and the on-screen keyboard. Test on at least one real iPhone and one low-cost Android phone when the work is phone-first.

## Do not

- Hide core features on small screens; if it matters, make it work there.
- Assume a desktop is fast; older machines and assistive tech are common.
- Forget landscape on phones and tablets.
- Ignore touch on desktop.
