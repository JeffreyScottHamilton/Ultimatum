# Anatomy: accessibility, reduced motion and where figures fail

Read when a figure is going on a public page or in an app, and before hand-over.

The upstream project says little on access. These rules are ours, and they bind every figure. The page-wide rules are in `../taste/accessibility.md`; this file is what is specific to figures.

## Text alternative

- The whole figure is one image with a short name (`role=img` and `aria-label`, or a `title`), or a group with a name if parts are individually reachable.
- The idea must also exist as text: the caption and the readout say what the drawing shows, with the real numbers. Someone who cannot see the picture loses nothing.
- Decorative parts are hidden from assistive tech (`aria-hidden`).

## Operable by keyboard (WCAG 2.1.1, 2.4.7, 2.5.8)

- Every control is a real button, link or slider, reachable by Tab, with a visible focus ring that holds 3:1 against its ground.
- No drag-only action. Offer a button or key for every drag (2.5.7).
- Targets are at least 24 by 24 CSS pixels (2.5.8).
- The figure never traps focus.

## Colour and contrast (1.4.1, 1.4.3, 1.4.11)

- Meaning is never carried by colour alone: add a label, a shape change or a pattern.
- Text on the card: 4.5:1. Edge lines and parts that carry meaning: 3:1 against the ground and against neighbours.
- Check the figure on the light and dark theme it ships in.

## Motion (2.2.2, 2.3.1)

- Any motion that starts on its own, runs over 5 seconds and sits beside other content has a visible pause control.
- No part flashes more than three times a second.
- Under `prefers-reduced-motion: reduce`: no idle tour, no auto-play, no tween; controls jump to the result; a complete still is shown. Also apply it if the page offers its own motion switch.
- Parallax, spin and zoom effects tied to scroll are off in reduced motion.

## Announcements

Phase changes go in one polite live region, short sentences, only when the phase changes. Slider value text changes only when the shown value changes.

## Reflow and zoom (1.4.4, 1.4.10)

The figure scales with its container, text in the card stays real text, and at 400 percent zoom nothing is cut off or needs two-direction scrolling (the figure itself may be exempt as a diagram, but its readout and controls are not).

## Where figures fail the business

- A figure that takes seconds to show on a phone loses the visit. Keep the SVG light and lazy-load it (`../taste/performance.md`).
- Invented numbers destroy trust. Use the owner's.
- Jargon labels no customer uses.
- A figure on the page only because it looks impressive: it counts against the effect cap and the anti-generic lint (`../../website/design-rules.md` §2 and §3).

## Fit to the anti-generic lint

A figure is not a mock-up with unreadable detail, not a blob or aurora, not three cards in a row, not a section that fades in the same way as every other. Its colours come from the page's three tokens plus one accent.

Docs: https://www.w3.org/TR/WCAG22/ and https://www.w3.org/WAI/ARIA/apg/patterns/slider/
