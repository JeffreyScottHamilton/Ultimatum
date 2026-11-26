# Audit checklist, part 2: states, motion, words, speed

Read while auditing how a page behaves and reads. Part 1 is `checklist-visual.md`; slop is `slop-tells.md`. Impact ratings: high, medium, polish.

## 5. Interaction states

- Hover on everything clickable; `cursor: pointer` on clickable non-links.
- A visible `:focus-visible` ring. `outline: none` is only allowed with a replacement ([focus visible](https://www.w3.org/TR/WCAG22/#focus-visible), and [focus not obscured](https://www.w3.org/TR/WCAG22/#focus-not-obscured-minimum) in 2.2: sticky headers must not hide the focused control).
- Active (pressed) state with a small depth or colour shift.
- Disabled state: reduced opacity and `cursor: not-allowed`, and a reason where it is not obvious.
- Loading shows skeleton shapes that match the real layout, not a generic spinner.
- Empty states have a warm line, a primary action and a picture or hint, not "No items."
- An error names what failed and the next step.
- Success confirms by colour or a short animation and dismisses itself.
- Touch targets at least 44 by 44 px (the WCAG 2.2 minimum is 24 px: [target size minimum](https://www.w3.org/TR/WCAG22/#target-size-minimum); the house uses 44).
- **No-thought test:** at each decision point (button, link, menu, modal choice) the right click should be obvious. A choice that makes someone stop and wonder is a high-impact finding.
- Browser-drawn parts follow the palette: text selection, caret, scrollbar, focus ring, underline offset and tabular figures.

## 7. Motion and animation

- Enter and exit with ease-out; moving between two places uses ease-in-out; plain ease-in is a flag.
- Durations from 50 to 700 ms; slower only for a page transition.
- Every animation communicates something: a state change, attention, a spatial relationship.
- `prefers-reduced-motion: reduce` is honoured in CSS and in any JS or WebGL animation. Check by emulating it, not by reading the CSS ([MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion)).
- Never `transition: all`; list the properties.
- Animate `transform` and `opacity`, not width, height, top or left.
- One authored motion moment per page: no identical entrance repeated down the page and no hover effect on every element. Content must never be held back by an animation.
- Check long frames while scrolling: `../../website/feel-bar.md` § How to check it.

## 8. Content and microcopy

- Button labels name the outcome ("Save API key", "Book a visit"), not "Submit" or "Continue".
- No placeholder or lorem ipsum text; no `href="#"` links.
- Long text truncates on purpose: ellipsis, line clamp or wrapping.
- Active voice ("Install the CLI").
- In-progress labels end with a real ellipsis ("Saving…").
- Destructive actions ask for confirmation or offer undo.
- **Happy talk:** welcome paragraphs and self-praise. Flag them and give the share, in the form "X words on this page, Y of them (Z per cent) happy talk".
- Instructions that run past one sentence signal a failed interface. Flag both the text and the interaction it props up.
- Voice and wording rules continue in `../../copy.md` and `../taste/copy.md`.

## 10. Performance as design

- Largest paint under 2.0 s for apps, under 1.5 s for brochure sites; layout shift under 0.1 ([Web Vitals](https://web.dev/articles/vitals)).
- Skeletons match the final layout.
- Images: lazy-loaded below the fold, width and height set, modern formats (WebP or AVIF).
- Fonts: `font-display: swap`, preconnect to font origins, critical fonts preloaded so there is no visible swap flash.
- Byte, request and WebGL budgets are in `../taste/performance.md`; use those numbers when a build used the taste craft.

## Local-business and app additions

- The phone number is a `tel:` link, the address opens a map, hours say "open now" only when computed, not typed.
- A booking, quote or contact form works with one hand on a phone, uses the right input types (`tel`, `email`) and confirms by name what happens next.
- Sign-up, pricing and checkout: each field has a visible label (never placeholder-only), errors name the field, a loading state follows every submit, and a dead payment button is a critical finding (`qa-taxonomy.md`).
- Accessibility floor beyond the rows above: one `h1`, landmarks, labels, alt text, keyboard-reachable everything, no keyboard trap, dragging has a non-drag alternative ([dragging movements](https://www.w3.org/TR/WCAG22/#dragging-movements)), and a sign-in step never relies on a cognitive test alone ([accessible authentication](https://www.w3.org/TR/WCAG22/#accessible-authentication-minimum)).
