# Interaction and states: eight states, the field, overlays, undo and loading

Read for forms and any control that holds state. Contrast and size figures are in `craft-type-colour.md` and `craft-finish.md`; this file holds the eight-state table, how to build a field, and overlay patterns. Behaviour of whole widgets (menus, accordions, modals) is in `microinteractions.md`.

## The eight states

| State | Trigger | How it looks |
|---|---|---|
| Default | resting | the base styling |
| Hover | pointer on it, only inside `@media (hover: hover)` | a single signal, either a colour step, a border step or a 1px lift |
| Focus | keyboard or script | the ring, with no delay |
| Active | while pressed | drops 1px or darkens one step |
| Disabled | cannot be used | three signals at once: opacity around 0.55, a `not-allowed` cursor and the native `disabled` attribute (use `aria-disabled="true"` when the control must stay focusable) |
| Loading | working | progress shown inline; the label stays legible and the width holds |
| Error | failed | error colour on the border plus a message and `aria-invalid`; colour is never the only cue |
| Success | done | the server's actual result; an icon from the page's own set at most; no toast; never a success without a request behind it (gate 70) |

A control missing any of these is unfinished. The matching checklist on our side is `../taste/accessibility.md`.

## Focus ring and hit targets

- One ring across the page: 2px solid in the focus colour, offset 2px, and inset on inputs (negative offset) so it never touches the neighbouring field. It needs 3:1 against both element and page. Use `:focus-visible` (https://developer.mozilla.org/en-US/docs/Web/CSS/:focus-visible). Do not write `outline: none` without a replacement.
- Anything a finger can reach needs 44×44 CSS px (WCAG 2.2 target size: https://www.w3.org/TR/WCAG22/#target-size-minimum). Enlarge a small control invisibly with a pseudo-element:

```css
.tap { position: relative; }
.tap::before { position: absolute; inset: -12px; content: ""; }
```

## Forms

- Put a visible label over every field. A placeholder never replaces the label and shows an example format, not an instruction.
- Validate on blur after the field has been touched, and on every keystroke after that.
- Write each error as one sentence covering what broke, why and what to do. Connect it using `aria-describedby`, and mark the field `aria-invalid="true"`.
- Flag required fields with `aria-required` plus a visible word; colour on its own is not enough.
- Keep submit enabled until a request is actually in progress.
- Local sites: a quote or booking form asks for the fewest fields that let the owner reply (name, a phone or email, what is needed), and promises a response time only if the owner promised it.

## The field (input, textarea, select, combobox)

The border keeps one width. Carry state through background, border colour, outline or shadow, and hold a transparent outline at rest so the ring appears without shifting anything.

```css
.field { outline: 2px solid transparent; outline-offset: -3px; border: 1px solid var(--mute); }
.field:focus-visible { outline-color: var(--ring); }
```

| State | Treatment |
|---|---|
| Default | 1px muted border (a field edge needs 3:1, which a plain hairline fails), paper background, muted placeholder |
| Hover | a second paper tone; the border stays |
| Focus | the ring; the border may darken at the same width |
| Filled | same as default |
| Disabled | the three signals, with the placeholder one step dimmer |
| Error | error-coloured border, message in the helper line, error glyph in the right slot |
| Success | shown only once a real check has come back, and removed as soon as the user edits |
| Loading | small spinner in the right slot; the field stays editable and submit waits |

- Match the height of the button next to it (44–52px for marketing). Vertical padding equals `(height - line-height) / 2`.
- Keep about 24px free at the right edge for a clear button, error glyph or spinner so nothing reflows.
- Place the label 4–8px above and the helper about 4px below in a quieter style, in a line holding `min-height: 1lh`. The error replaces the helper and never adds a second line.
- Do not transition `border-width`, `padding` or `height`, and do not animate the ring.
- **Other controls.** Textarea: `resize: vertical`, minimum 6rem. Select: keep it native and put a custom chevron on the wrapper (go fully custom only when native keyboard and screen-reader behaviour survives). Checkbox and radio: native, styled with `accent-color` and CSS state, and script never toggles them. A switch is a checkbox under the same contract. Range thumbs need a 44px target. File inputs get a styled label. A combobox's listbox opens beneath without pushing content; `aria-expanded` tracks it, arrow keys cycle, Enter picks and Escape closes it.

## Dialogs and overlays

- A native `<dialog>` that you open with `showModal()` supplies focus trapping, Escape and `::backdrop` (https://developer.mozilla.org/en-US/docs/Web/HTML/Element/dialog).
- If you add your own positioning, pin the dialog or it may leap to a corner: `margin: auto; inset: 0; position: fixed; max-height: min(80dvh, 40rem); height: fit-content`. For an overlay that is not a dialog, centre a fixed container with `display: grid; place-items: center`.
- Make the page behind `inert`. Allow closing by Escape, a backdrop click or a visible close control, and send the first focus to the first interactive element inside.

## Popovers, menus and tooltips

Use the Popover API to get light dismiss, stacking and Escape (https://developer.mozilla.org/en-US/docs/Web/API/Popover_API). Use CSS anchor positioning where supported; elsewhere fall back to fixed positioning computed from `getBoundingClientRect()`. Flip placement near the viewport edge, and never place one inside an `overflow: hidden` ancestor that would clip it.

## Undo beats confirm

Run reversible actions immediately and offer Undo for 5–10 seconds. Irreversible ones (deleting an account, dropping a table) keep the confirmation and make the user type the name of what will be destroyed. In an app holding Stripe or Supabase data, deleting paid records counts as irreversible.

## Loading and empty

- When the shape of the content is known (lists, cards, tables) show a skeleton; reserve spinners for inside a button, in place of its label.
- An empty state has a line saying what is empty, a line on why that matters, and one action. A bare "No results" falls short.
- A disabled control in the user's line of attention explains why it is disabled.
- Any region loading data has four states: loading, empty, error and full (`flow-branches.md` § App screens, rules for tools).
