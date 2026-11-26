# Accessibility to WCAG 2.2 AA

Read before building any page, and again before review: every craft move in this folder has to pass these checks.

Target: WCAG 2.2 level AA. The numbers below are the criteria's own thresholds; the rest is how they bite on a designed site. Spec: https://www.w3.org/TR/WCAG22/ · plain-language notes: https://www.w3.org/WAI/WCAG22/Understanding/

## Colour and contrast

- Body text: contrast 4.5:1 against what is behind it (1.4.3). Large text (24 px regular, or about 18.7 px bold) needs 3:1.
- Icons, input borders, focus rings and chart lines that carry meaning: 3:1 against their neighbours (1.4.11 Non-text Contrast).
- Text on a photo or video: measure against the lightest patch the text can land on, at every width. Add a solid or scrim layer behind it when it fails; never rely on a shadow alone.
- Colour is never the only signal (1.4.1). An error field gets an icon or text too; a chart series gets a label or pattern.
- Muted grey captions are the usual failure. Check `--muted` on `--bg` and on every card colour before using it for anything people must read.

## Size, zoom and reflow

- Content reflows to a 320 CSS px wide window with no sideways scroll, except for real two-dimensional content such as maps, wide tables and code (1.4.10). We also check at 375 px.
- Text can grow to 200% without loss (1.4.4). Use `rem` for type, never fix heights on text boxes, and never set `maximum-scale=1` or `user-scalable=no`.
- Users may widen line, letter, word and paragraph spacing (1.4.12). Let boxes grow; don't clip text with `overflow: hidden` on a fixed height.

## Pointer and touch

- Targets at least 24 x 24 CSS px, or spaced so a 24 px circle on each does not overlap a neighbour (2.5.8 Target Size Minimum, new in 2.2). Ultimatum's own floor stays at 44 x 44 px for main actions and mobile navigation (`design-rules.md` section 7).
- Anything done by dragging also works with single taps or clicks (2.5.7 Dragging Movements, new in 2.2): sliders get buttons or a number field, sortable lists get move-up and move-down, before/after comparison handles accept arrow keys.
- The visible label is inside the accessible name (2.5.3): a button that reads "Book a table" is not named "submit-cta".
- No action fires on pointer-down alone (2.5.2); use click.

## Keyboard and focus

- Everything works with a keyboard alone, with no trap (2.1.1, 2.1.2). Custom widgets follow the ARIA Authoring Practices patterns: https://www.w3.org/WAI/ARIA/apg/patterns/
- Focus is always visible (2.4.7). Use `:focus-visible` with an outline of at least 2 px in a colour that meets 3:1.
- A focused element is never fully hidden by a sticky header, cookie bar or chat bubble (2.4.11 Focus Not Obscured, new in 2.2). Give anchors and focus targets `scroll-margin-top` equal to the sticky header's height, and keep banners out of the way of the tab order.
- Focus order follows the reading order (2.4.3). Visual reordering with `order`, grid placement or absolute positioning must not scramble it.
- A skip link to the main content on any page with repeated navigation (2.4.1).
- Menus, dialogs and drawers: focus moves in when opened, returns to the trigger when closed, and Escape closes them. Prefer the native `<dialog>` element with `showModal()`.

## Content that moves, flashes or appears

- Any automatic movement lasting over 5 seconds (carousels, marquees, looping video, animated backgrounds) has a visible pause control (2.2.2 Pause, Stop, Hide). Reduced-motion alone does not satisfy this.
- Nothing flashes more than three times a second (2.3.1).
- Motion triggered by scrolling or hovering can be switched off (2.3.3, AAA, but we treat it as required): honour `prefers-reduced-motion` (see `motion.md`).
- Tooltips and popovers that appear on hover or focus can be dismissed with Escape, stay while the pointer moves onto them, and stay until dismissed (1.4.13).

## Structure and names

- One `<h1>`; headings in order without skipped levels used for styling (1.3.1). Big display type is still a heading element underneath.
- Landmarks: `<header>`, `<nav>`, `<main>`, `<footer>`. Set `lang` on `<html>` (3.1.1).
- Meaningful images get alt text that says what the image shows for this page; decorative ones get `alt=""` (1.1.1). Canvas and WebGL art is decorative unless it carries information; then give a text equivalent next to it.
- Split-letter headline effects: keep the whole word readable to screen readers. Put `aria-label` on the heading or keep a visually hidden copy, and hide the split spans with `aria-hidden="true"`.
- Link text says where it goes (2.4.4). Icon-only buttons get an accessible name.
- Status messages (added to cart, form sent) are announced without moving focus: `role="status"` or `aria-live="polite"` (4.1.3).

## Forms, sign-in and checkout

- Every field has a visible `<label>` (3.3.2); placeholders are hints, not labels.
- Use `autocomplete` tokens (`name`, `email`, `tel`, `street-address`, `cc-number`, `one-time-code`) so browsers can fill them (1.3.5).
- Errors name the field and say how to fix it, in text (3.3.1, 3.3.3). Move focus to an error summary on submit.
- Don't ask again for something the user already gave in the same flow (3.3.7 Redundant Entry, new in 2.2): "billing same as delivery" is a checkbox, not a retype.
- Sign-in never depends on a memory or puzzle test (3.3.8 Accessible Authentication, new in 2.2). Allow paste and password managers in password and code fields; offer passkeys, email links or social sign-in; if there is a CAPTCHA, give a non-puzzle alternative.
- Legal, money and data actions can be reviewed, corrected or undone before they are final (3.3.4).
- Help (phone, chat, contact link) sits in the same place on every page that has it (3.2.6 Consistent Help, new in 2.2). For a local business this is the phone link in the header.

## Quick test pass

1. Tab through the page from the address bar to the footer: every stop visible, nothing hidden under sticky bars, order makes sense.
2. Zoom to 200% and resize to 320 px wide: nothing clipped, no sideways scroll.
3. Emulate reduced motion: the page calms down (see `motion.md` for what that means).
4. Run axe or Lighthouse in the browser for contrast, names and labels; it finds about a third of problems, so the manual steps still count. axe rules: https://dequeuniversity.com/rules/axe/
5. Screen reader spot check on the hero, menu, main form and any custom widget.
