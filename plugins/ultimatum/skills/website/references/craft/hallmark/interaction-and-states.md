# Interaction and states: eight states, the field, overlays, undo and loading

Read for forms and any stateful control. Contrast and size numbers live in `craft-type-colour.md` and `craft-finish.md`; this file owns the state table, the field recipe and the overlay patterns. Widget-level behaviour (menus, accordions, modals) is in `microinteractions.md`.

## The eight states

| State | When | Treatment |
|---|---|---|
| Default | at rest | base styling |
| Hover | pointer over, inside `@media (hover: hover)` | one signal: a colour step, a 1px lift or a border step |
| Focus | keyboard or programmatic | the ring, immediately |
| Active | during press | a 1px drop or one step darker |
| Disabled | not interactive | three signals together: opacity about 0.55, `cursor: not-allowed`, and the native `disabled` (or `aria-disabled="true"` where the control must stay focusable) |
| Loading | processing | inline progress; label stays readable; width does not jump |
| Error | failed | error colour on the border, a message, `aria-invalid`; never colour alone |
| Success | completed | the result itself from the server's answer; at most an icon from the page's set; no toast; no success where no request was made (gate 70) |

A control missing one is not finished. Our own checklist for the same area is `../taste/accessibility.md`.

## Focus ring and hit targets

- One ring for the page: 2px solid in the focus colour with a 2px offset, inset on inputs (negative offset) so it never meets the next field. 3:1 against the element and the page. Use `:focus-visible` (https://developer.mozilla.org/en-US/docs/Web/CSS/:focus-visible). Never `outline: none` without a replacement.
- 44 x 44 CSS px for anything a finger reaches (WCAG 2.2 target size: https://www.w3.org/TR/WCAG22/#target-size-minimum). Grow a small control without changing its look with a pseudo-element:

```css
.icon-btn { position: relative; }
.icon-btn::before { content: ""; position: absolute; inset: -12px; }
```

## Forms

- A visible label above every field; a placeholder is never the label and shows a format, never an instruction.
- Validate on blur once touched, then on each input.
- An error says what broke, why and what to do in one sentence, linked with `aria-describedby`, with `aria-invalid="true"`.
- Required fields carry `aria-required` and a visible word, never colour alone.
- Disable submit only while a request is in flight, never at rest.
- Local sites: a quote or booking form asks the fewest fields that let the owner reply (name, a phone or email, what is needed), and says when they will hear back only if the owner promised it.

## The field (input, textarea, select, combobox)

The border never changes width. Move state into background, border colour, outline or shadow, and reserve a transparent outline at rest so the ring appears without a shift.

```css
.input { border: 1px solid var(--color-muted); outline: 2px solid transparent; outline-offset: -3px; }
.input:focus-visible { outline-color: var(--color-focus); }
```

| State | Treatment |
|---|---|
| Default | 1px muted border (a field edge needs 3:1, which a plain rule lacks), paper background, muted placeholder |
| Hover | second paper tone, border unchanged |
| Focus | the ring; the border may deepen at the same width |
| Filled | as default |
| Disabled | three signals; placeholder dims a step |
| Error | error border, message in the helper line, an error glyph in the right slot |
| Success | only after a real check returned; clears when the user edits |
| Loading | a small spinner in the right slot; the field stays editable, submit waits |

- Match the height of the button beside it (44 to 52px marketing). Vertical padding is `(height - line-height) / 2`.
- Reserve about 24px at the right edge for a clear button, error glyph or spinner so nothing reflows.
- Label 4 to 8px above; helper about 4px below, quieter, in a line reserving `min-height: 1lh`; the error replaces the helper, never adds a second line.
- Never transition `border-width`, `padding` or `height`; never animate the ring.
- **Other controls:** textarea `resize: vertical` with a 6rem minimum; select native with a custom chevron on its wrapper (fully custom only if it keeps native keyboard and screen-reader behaviour); checkbox and radio native with `accent-color` and CSS state, never toggled by script; a switch is a checkbox with the same contract; range thumb has a 44px target; file input uses a styled label; a combobox's listbox sits below without pushing content, `aria-expanded` mirrors it, arrows cycle, Enter selects, Escape closes.

## Modals and overlays

- Native `<dialog>` opened with `showModal()` gives the focus trap, Escape and `::backdrop` (https://developer.mozilla.org/en-US/docs/Web/HTML/Element/dialog).
- Once you add custom positioning pin it, or it can snap to a corner: `position: fixed; inset: 0; margin: auto; height: fit-content; max-height: min(80dvh, 40rem)`. A non-dialog overlay centres with a fixed container using `display: grid; place-items: center`.
- Make the page behind `inert`; close on Escape, backdrop click and a visible close control; first focus lands on the first interactive element.

## Popovers, menus, tooltips

Use the Popover API for light dismiss, stacking and Escape (https://developer.mozilla.org/en-US/docs/Web/API/Popover_API); CSS anchor positioning where supported, else `position: fixed` with `getBoundingClientRect()`; flip near the viewport edge; never inside an `overflow: hidden` ancestor that would clip it.

## Undo over confirm

Reversible actions run at once and offer Undo for 5 to 10 seconds. Irreversible ones (delete an account, drop a table) keep the confirm and ask the user to type the name of what is being destroyed. For an app with Stripe or Supabase data, deletes of paid records are the irreversible kind.

## Loading and empty

- A skeleton where the content's shape is known (lists, cards, tables); a spinner only inside a button, replacing its label.
- An empty state is one line saying what is empty, one on why it matters, and one action. Never a bare "No results".
- A disabled control in the user's line of attention says why it is disabled.
- Every region that loads data has four states: loading, empty, error, full (`flow-branches.md` § App screens, rules for tools).
