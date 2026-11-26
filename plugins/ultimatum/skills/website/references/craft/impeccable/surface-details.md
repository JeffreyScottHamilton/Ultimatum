# Surface details: type, colour roles, layout and product UI

Read when you are tuning type, colour roles or spacing on a page or app screen, or building product UI that people should trust on first use.

The base type, OKLCH colour and dark-mode rules are in `../hallmark/craft-type-colour.md` and `../hallmark/dark-mode.md`; the eight states and overlays are in `../hallmark/interaction-and-states.md`; browser-surface theming and depth reflexes are in `../design-review-qa/page-modes.md` § Reflexes no automated check catches. This file adds the details those leave out.

## Type

- Ordinary web body text: 1rem (16 px) as the floor; 14 px only for secondary text.
- Prose measure 45 to 75 characters (`max-inline-size: 68ch` is a good start). Data tables may run much wider.
- Line height goes up as lines get longer, and down for large display sizes.
- Light text on a dark ground looks heavier and tighter. Compensate a little on all three: slightly more line height, a touch more letter spacing, one step lighter weight.
- Use paragraph spacing or a first-line indent, not both.
- Tabular figures (`font-variant-numeric: tabular-nums`) for numbers in columns, prices and timers.
- Product UI uses a fixed rem scale with a small ratio (1.125 to 1.2); fluid `clamp()` sizing belongs to marketing display type.
- Load only the faces and weights you use; give the fallback matching metrics (`size-adjust`, `ascent-override`) to stop reflow when the font arrives.

### Line breaks

- `text-wrap: balance` on headings and short centred blocks; `text-wrap: pretty` on body paragraphs to avoid a lone last word. Reference: <https://developer.mozilla.org/en-US/docs/Web/CSS/text-wrap>.
- `pretty` only pulls one word down; it does not fill the last line. When the column is too narrow for wrapping rules to help, rewrite the line or give it more width.
- Manual heading breaks go at phrase boundaries, and need checking at each width the heading appears at. A deliberate uneven break (one word alone for weight) is fine when it is meant.

## Colour roles

Name each role before picking any value: page ground, raised layers, main text, muted text, actions, focus ring, selected state, dividers, the four status colours, and chart series when there are charts.

- The primary action's colour is spent on the primary action, not on decoration.
- Tint neutrals toward the brand hue only when it adds cohesion; plain grey is fine.
- On a coloured surface, derive secondary text from that surface's hue rather than using grey.
- Status colours keep one meaning everywhere and always pair with a label, icon or shape.
- For charts, vary lightness and add labels or patterns so colour is not the only cue (see the dataviz guidance if one is loaded).
- Dark mode gets its own elevation and contrast decisions; never invert the light theme.
- Define primitive values once and point semantic tokens at them, so a theme change edits one layer.

## Layout

Two passes: look first, then measure.

**Look.** The squint test: blur the screen; can you still find the primary element, the secondary ones and the main groups in order? Are related items close and unrelated ones apart? Is spacing a rhythm of tight and generous intervals, or one value everywhere? Does density fit how often the screen is used?

**Apply.**
- Group by proximity before adding boxes, lines or colour.
- Use one documented spacing scale (a 4 px base works for most).
- Use `gap` for spacing between siblings.
- Keep hit areas large even when the visible mark is small (padding or a pseudo-element).
- Use depth only to show state or layering.
- Make optical corrections only after looking at the rendered result.
- Check that keyboard order, screen-reader order and visual order agree.

## Product UI that feels standard

For tools and dashboards (Operate mode), people trust what behaves like the category's best products.
- Standard controls, standard navigation; one family is enough.
- Every control has its full set of states: resting, hovered, focused, pressed, unavailable, busy, failed, plus selected for toggles and lists.
- Skeletons for known shapes rather than spinners; empty states teach the next step.
- Accent colour only for actions, selection and state; a second neutral layer for app chrome.
- Motion explains state only, 150 to 250 ms; no choreography on page load.
- Overlays must escape clipped parents: use `<dialog>` for modal tasks and the `popover` attribute for menus and tips, both of which render in the top layer (<https://developer.mozilla.org/en-US/docs/Web/API/Popover_API>). The harden example shows a popover leaving an `overflow: hidden` card.
- Avoid display faces in labels, reinvented controls, saturated inactive states and modals as the first answer.
- A brand may lend a product UI its type, palette, density and one signature move; more than that turns into costume.
- Show real-looking content, plausible data and at least one interesting state (an alert, an empty list, an overdue item) in every comp.
