# shadcn/ui accessibility: what comes built in, and what is still ours

Read when building with shadcn/ui and checking keyboard use, screen-reader names, forms and contrast. The component primitives underneath (Radix, or Base UI in newer setups) handle much of the behaviour; the content, names and colours are still the project's job. The house checklist is `../taste/accessibility.md` (WCAG 2.2 AA); this file maps it onto shadcn's components. Patterns cited are the WAI-ARIA Authoring Practices (https://www.w3.org/WAI/ARIA/apg/patterns/).

## What the primitives give us, and what they do not

| Built in (check once, do not rebuild) | Still ours |
|---|---|
| focus moved into Dialog, Alert Dialog, Sheet, Drawer on open, and back to the trigger on close | an accessible title on every dialog (a dialog without one triggers a console warning; a visually hidden title is allowed) |
| Escape closes overlays; Tab stays inside a modal | a visible focus ring that passes 3:1 on every ground |
| arrow keys in menus, tabs, radio groups, selects, accordions | labels for every field and icon-only button |
| roles and states (`aria-expanded`, `aria-selected`, `aria-checked`) on the primitives | the text of errors and descriptions, and joining them to fields |
| type-ahead in menus and selects | colour contrast of the theme |
| | live announcements for results (toasts, saved states) |
| | the order of the page, headings, landmarks and link text |

The quickest way to break the built-in behaviour is to replace a primitive part with a plain element (a `div` as a trigger), or to stop events in a wrapper. Use `asChild` to swap the rendered element while keeping the behaviour.

## Keyboard, component by component

| Component | Keys to test | Pattern |
|---|---|---|
| Button, Toggle | Tab to it; Enter and Space | |
| Dialog, Sheet, Drawer | opens with focus inside; Tab cycles; Escape closes; focus returns | https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/ |
| Alert Dialog | as Dialog; focus starts on the least destructive action | https://www.w3.org/WAI/ARIA/apg/patterns/alertdialog/ |
| Dropdown Menu | Enter, Space or Down opens; arrows move; Escape closes; type-ahead | https://www.w3.org/WAI/ARIA/apg/patterns/menu-button/ |
| Navigation Menu, Menubar | arrows between top items; Down into sub-menus | https://www.w3.org/WAI/ARIA/apg/patterns/menubar/ |
| Tabs | Tab enters the tab list; arrows move between tabs; Tab moves to the panel | https://www.w3.org/WAI/ARIA/apg/patterns/tabs/ |
| Accordion | Enter or Space toggles; each header is a button | https://www.w3.org/WAI/ARIA/apg/patterns/accordion/ |
| Select | Enter or Space opens; arrows; type-ahead; Escape | https://www.w3.org/WAI/ARIA/apg/patterns/listbox/ |
| Combobox (Popover + Command) | typing filters; arrows move; Enter picks; Escape closes | https://www.w3.org/WAI/ARIA/apg/patterns/combobox/ |
| Switch | Space toggles | https://www.w3.org/WAI/ARIA/apg/patterns/switch/ |
| Command | arrows through results; Enter runs | |

Test with the keyboard alone, on the real page, after styling: custom CSS can hide focus or trap it under a sticky header (WCAG 2.2 SC 2.4.11 Focus Not Obscured).

## Names and descriptions

- Every field has a visible label tied to it. Placeholder text is not a label.
- An icon-only button gets an `aria-label` that names the action ("Close", "Delete invoice 1042"); the icon gets `aria-hidden="true"`.
- Every Dialog and Sheet has a title; if the design shows none, render it visually hidden (`className="sr-only"`). Add a description where it helps; if there is none, say so to the primitive as its docs describe, rather than leaving a broken reference.
- Repeated actions in lists ("Edit") need distinct names: add the item, visually hidden if needed.
- Tooltips repeat information; they never hold the only copy of something the user needs.

## Forms

- Required fields say "required" in words in the label; `required` on the input.
- Errors appear below the field in text, join to it with `aria-describedby`, and set `aria-invalid="true"`. shadcn's form field parts do this when used as documented; check the rendered HTML once.
- Group related radios and checkboxes in a `fieldset` with a `legend` (the Radio Group needs a visible group label).
- Use the right `autocomplete` values, so browsers and password managers can fill (also required for SC 3.3.8 Accessible Authentication: do not block paste into password or code fields).
- On a failed submit, move focus to the first invalid field or to an error summary.

## Announcements

- After an action whose result is not otherwise visible (saved, copied, sent), announce it. Sonner toasts are announced through a live region; keep toast text short and do not put the only copy of an error, or an action the user must take, in a toast that disappears.
- For an error that stops the user, use an inline Alert with `role="alert"`, placed by the thing that failed.
- Loading regions get `aria-busy="true"` until filled; announce "Loaded" only if the wait was long.

## Contrast and focus

- Check the theme's pairs in both modes (`shadcn-theming.md` § Checks before shipping a theme): 4.5:1 for text, 3:1 for the ring and field borders (WCAG 2.2 SC 1.4.3, 1.4.11).
- The default focus style uses the `ring` role; confirm it shows on `primary` and `destructive` grounds and on images.
- `muted-foreground` is the role most often too pale. Check it on `muted` and on `card`, not only on `background`.
- Disabled controls may be dimmer, but text must still be readable.

## Motion

- Overlays animate in with `tw-animate-css` classes. Respect `prefers-reduced-motion`: Tailwind's `motion-reduce:` variant can switch an animation off (`motion-reduce:animate-none`), or set short durations globally inside the media query.
- No animation should block input; closing animations must not delay the next focus.

## Test pass

1. Keyboard only, through every interactive component on the page.
2. A screen reader on one main flow (VoiceOver with Safari, or NVDA with Firefox or Chrome): names, roles, states, announcements.
3. An automated scan (axe, or the browser's accessibility panel) on every page template; fix every serious issue, then re-test by hand: a clean scan does not mean an accessible page.
4. Zoom to 200 % and to a 320 px wide viewport: nothing clipped, no sideways scroll (SC 1.4.4, 1.4.10).
5. Both themes, with the colour checks above.

For the release-level review, use `../design-review-qa/index.md`.
