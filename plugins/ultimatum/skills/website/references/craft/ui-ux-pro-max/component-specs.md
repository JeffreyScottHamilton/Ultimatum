# Component specs: one sheet per component

Read when a component needs a written spec before it is built or handed to someone else, or when an existing component library has drifted and needs pinning down. The house component rules are in `../../website/design-rules.md` § 8. Components and § 7. Interface basics; states and their order are in `states-and-variants.md`; tokens in `token-architecture.md`. This file gives the sheet format and filled sheets for seven common components, using the starter token names.

## The sheet

Every spec answers the same questions, in this order, so a reader can find any answer in the same place:

1. **Job.** One sentence: what it is for, and what it is not for.
2. **Anatomy.** The named parts.
3. **Variants.** Each with when to use it.
4. **Sizes.** Height, padding, type size, icon size.
5. **States.** Which of the eight apply, and anything special.
6. **Tokens.** The component tokens and what they point at.
7. **Behaviour.** Keyboard, pointer, timing.
8. **Accessibility.** Role, name, attributes, the pattern it follows.
9. **Do / avoid.** Two or three lines each.

Sizes below are a starting point on a 4 px grid. Touch targets are at least 44 x 44 CSS px, the house rule (`../../website/design-rules.md` § 7. Interface basics); WCAG 2.2 SC 2.5.8 sets the legal floor lower, at 24 x 24 (https://www.w3.org/TR/WCAG22/).

## Button

- **Job:** starts an action. Navigation uses a link styled as needed, not a button.
- **Anatomy:** container, label, optional leading or trailing icon, optional spinner.
- **Variants:** primary (one per view), secondary, outline, ghost, danger, link-styled. Build them from local tokens (`states-and-variants.md` § Variants by local tokens).
- **Sizes:**

| Size | Visible height | Padding x | Text | Icon |
|---|---|---|---|---|
| sm | 36 px (hit area extended to 44) | 12 px | 14 px | 16 px |
| md | 44 px | 16 px | 16 px | 18 px |
| lg | 52 px | 24 px | 18 px | 20 px |
| icon | 44 x 44 px | none | none | 20 px |

- **States:** all eight. Loading keeps the width; disabled keeps the label readable.
- **Tokens:** `--button-bg` → `--primary`, `--button-fg` → `--primary-foreground`, `--button-bg-hover` → `--primary-hover`, `--button-radius` → `calc(var(--radius) - 2px)`, `--button-height` 2.75rem.
- **Behaviour:** Enter and Space activate. Never on mouse-down. Labels are verbs naming the result ("Save changes", "Send invoice").
- **Accessibility:** native `<button type="button">` (or `type="submit"` in a form). An icon-only button has an `aria-label`; the icon is `aria-hidden="true"`.
- **Do:** one primary per view; the label says what happens. **Avoid:** two primaries side by side; "Click here", "Submit"; a disabled button with no explanation.

## Field (text input)

- **Job:** collects one value the user types.
- **Anatomy:** label, optional hint, control, optional prefix or suffix, message line (error or help).
- **Variants:** default; with prefix or suffix (currency, units); with a leading icon (search). No floating labels: the label stays visible above the control.
- **Sizes:** control 44 px tall, 12 px padding x, 16 px text (smaller text makes iOS zoom on focus).
- **States:** default, hover, focus, disabled, read-only, error. Read-only looks like text on a muted ground, not like a disabled field.
- **Tokens:** `--field-bg` → `--card`, `--field-border` → `--input` (3:1 against the page), `--field-border-invalid` → `--destructive`, `--field-height` 2.75rem.
- **Behaviour:** validate on leaving the field or on submit; clear the error the moment the value is fixed. Correct `type`, `inputmode` and `autocomplete` values, so phones show the right keyboard and browsers can fill.
- **Accessibility:** `<label for>` tied to the control; hint and message joined with `aria-describedby`; `aria-invalid="true"` on error; `required` on required fields, with the label saying so in words.
- **Do:** keep labels short and above. **Avoid:** placeholder as the only label; blocking paste; asking again for something already entered (WCAG 2.2 SC 3.3.7 Redundant Entry).

The full field rules (textarea, select, combobox) are in `../hallmark/interaction-and-states.md` § The field (input, textarea, select, combobox).

## Card

- **Job:** groups content about one thing. Not a decoration for every section.
- **Anatomy:** container, optional media, header (title, meta), body, optional footer with actions.
- **Variants:** plain (border), raised (shadow), interactive (the whole card is one link).
- **Sizes:** padding 24 px (16 px on phones); gap between parts 12-16 px.
- **States:** interactive cards get hover and focus; others have none.
- **Tokens:** `--card-bg` → `--card`, `--card-fg` → `--card-foreground`, `--card-border` → `--border`, `--card-radius` → `--radius`, `--card-padding` `calc(var(--spacing) * 6)`.
- **Behaviour:** an interactive card has one link (on the title) whose hit area is stretched over the card with a pseudo-element; secondary actions inside sit above that layer.
- **Accessibility:** a heading for the title at the right level; in a list of cards, use a list (`<ul>`).
- **Do:** vary card sizes by content importance. **Avoid:** identical icon-title-text cards in rows of three, the stock layout `../../website/design-rules.md` § 2. Anti-generic lint warns about; cards inside cards.

## Badge

- **Job:** a short label of status or category. Not a button.
- **Anatomy:** container, text, optional dot or icon.
- **Variants:** neutral, primary, and the four statuses (danger, warning, success, info).
- **Sizes:** 20-24 px tall, 8 px padding x, 12-13 px text, weight 500.
- **States:** none (a removable chip is a different component with a button inside).
- **Tokens:** status badges use the role pair (`--success` with `--success-foreground`), or a light ground with dark text from the same ramp; check the pair.
- **Accessibility:** the text carries the meaning; colour only repeats it. If the badge is a count ("3"), add hidden context ("3 unread").
- **Avoid:** badges as decoration on every card; colour-only status dots.

## Alert (inline message)

- **Job:** tells the user something about the page or their last action, in place.
- **Anatomy:** icon, title, body, optional action, optional dismiss button.
- **Variants:** info, success, warning, danger.
- **Sizes:** padding 16 px; icon 20 px; title 16 px semibold; body 14-16 px.
- **Tokens:** a soft ground (status step 100 or a mix of the status colour with the background) with text in the darkest status step or `--foreground`; border in the status colour.
- **Behaviour:** stays until dismissed or resolved. No auto-dismiss for anything the user must read.
- **Accessibility:** a message that appears after an action goes in a live region: `role="status"` for information, `role="alert"` only for urgent errors. A message present at page load needs no role.
- **Avoid:** using an alert for marketing; stacking several.

## Dialog

- **Job:** a focused task or a decision that blocks the page until done.
- **Anatomy:** backdrop, panel, title, body, actions (main action last on the right, or full-width on phones), close button.
- **Sizes:**

| Size | Max width | Use |
|---|---|---|
| sm | 400 px | a confirmation, one question |
| md | 560 px | a short form |
| lg | 720 px | a longer form or a preview |
| full | the viewport, on phones | anything with a keyboard on a small screen |

- **Tokens:** panel uses `--card`; backdrop is the darkest neutral at about 50-60 % opacity; radius `--radius-xl`; layer `modal`.
- **Behaviour:** focus moves into the dialog on open (to the first field, or the least destructive button) and returns to the trigger on close; Tab cycles inside; Escape closes; the page behind cannot scroll.
- **Accessibility:** native `<dialog>` with `showModal()`, or `role="dialog"` with `aria-modal="true"`; `aria-labelledby` the title. A destructive confirmation is an alert dialog (https://www.w3.org/WAI/ARIA/apg/patterns/alertdialog/). Pattern: https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/.
- **Avoid:** dialogs for content that could be a page; a dialog on page load; confirming something undo would handle better (`../hallmark/interaction-and-states.md` § Undo beats confirm).

## Table

- **Job:** compares many records on the same fields.
- **Anatomy:** caption, header row, body rows, optional footer (totals), optional toolbar (search, filters), pagination.
- **Sizes:** row height 44 px (40 px in a dense mode the user chooses); cell padding 12-16 px x; numbers right-aligned in tabular figures (`font-variant-numeric: tabular-nums`).
- **Row states:** default, hover (pointer only), selected (`aria-selected` with a checkbox), and focus when rows are keyboard-navigable.
- **Tokens:** header text `--muted-foreground` at weight 500; dividers `--border`; selected row a soft primary ground.
- **Behaviour:** sortable headers are buttons inside `<th>` with `aria-sort` on the sorted column. On phones, either let the table scroll sideways inside its own container (with the first column fixed) or switch to stacked cards; never squash columns.
- **Accessibility:** a real `<table>` with `<caption>`, `<th scope="col">` and `scope="row"` where it applies. Row actions have names that include the row ("Edit invoice 1042").
- **Avoid:** zebra stripes plus borders plus hover all at once; truncating the key column.

## Spacing and alignment inside components

- Padding comes from the spacing unit: 8, 12, 16, 24 px.
- Icon and label: 8 px gap; icons align to the text's centre, not its baseline.
- Inside a group of controls (a toolbar, button pair), 8 px; between groups, 16-24 px.
- Text inside a control sits on the same baseline across controls of the same size, so a field and its button line up.
