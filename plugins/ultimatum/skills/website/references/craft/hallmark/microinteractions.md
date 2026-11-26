# Microinteractions: recipes for stateful widgets

Read when the page has buttons, forms, menus, dialogs, tabs, toasts or live numbers. Durations and easings are set in `craft-motion.md`; state tables are in `interaction-and-states.md`. This file holds one recipe per widget. Reduced motion is in every recipe: spatial movement becomes a 150ms opacity fade, state changes still happen (WCAG 2.2.2 and 2.3.3, https://www.w3.org/TR/WCAG22/#animation-from-interactions).

## Principles

- Motion needs a job: clarify, guide or confirm. If instant loses nothing, cut it.
- Success the user can already see gets no toast. Toasts are for failures and for effects off screen.
- Update the interface first, send the request behind it, roll back with a retry on failure.
- Every hover affordance has a focus twin. Nothing is hover-only.
- Three motion ideas per page at most (one reveal, one hover signal, one functional loop). A still theme runs none beyond state changes.

## Character of the system

| Character | Speed against base | Feel |
|---|---|---|
| still | no motion | print; nothing moves except a typed caret that stops after a few beats |
| severe | 0.7 to 0.75x | snaps; no spring |
| brisk | 0.85 to 0.9x | instrument panel |
| calm | 1.0 to 1.3x | gentle ease-out, generous |

Declare one per site. Most pages carry too much motion; the static answer is often right.

## Recipes

Tokens: micro 120ms, short 220ms, long 420ms. Enters ease out, exits ease in at about 65% of the enter time, toggles ease in-out.

- **Button.** Hover changes colour only; press drops 1px; the ring never animates.
- **Field focus.** Ring appears at once; label stays above the field (a floating label is a placeholder in disguise).
- **Validation.** On blur once touched, then per input; never on the first keystroke. The error takes the helper's reserved line.
- **Toast.** One corner, newest pushes the stack, 4 to 6 seconds, pause on hover and focus, an error toast stays and offers one retry.
- **Modal.** `<dialog>` with `showModal()`; backdrop fades, panel scales 0.96 to 1; first focus on the first control, not the close button.
- **Menu.** Popover API; flip within 16px of an edge; stagger items 30ms only when there are eight or fewer.
- **Tooltip.** Delay 800 to 1000ms on hover, none on focus; stays while the pointer is on it; Escape closes (WCAG 1.4.13, https://www.w3.org/TR/WCAG22/#content-on-hover-or-focus).
- **Tabs.** Move the indicator with `transform`, never `width`; a panel that changes height animates `grid-template-rows: 0fr` to `1fr`.
- **Number tick.** Real figures only. Count over 400 to 800ms, format with `Intl.NumberFormat`, announce the final value once through `aria-live="polite"`. Reduced motion shows the final value.
- **Copy button.** Label turns to "Copied" for about 2.5 seconds, no toast:

```js
btn.addEventListener("click", async () => {
  await navigator.clipboard.writeText(btn.dataset.value);
  btn.dataset.state = "copied";
  setTimeout(() => delete btn.dataset.state, 2500);
});
```

- **Drag to reorder.** Handle visible on hover and focus; ghost at half opacity; a 1px line marks the target; arrow keys reorder a focused row and `aria-live` says so. WCAG 2.2 dragging movements (2.5.7) needs that keyboard path.
- **Optimistic update.** Row changes at once; failure rolls back and raises an error with a retry:

```js
const was = item.done;
item.done = !was; render();
try { await save(item); }
catch { item.done = was; render(); showError("Could not save.", retry); }
```

- **Search as you type.** Debounce 250ms; matches in `<mark>`; announce the result count once, after the debounce.
- **Command palette.** Opens on Cmd+K or `/`; input keeps focus; highlight slides by `transform`; rows never move; Enter picks, Escape closes.
- **Page-load reveal.** One staggered entrance of 0.4 to 0.8 seconds, IntersectionObserver, once.

Local and app notes: a call button changes label to "Calling..." only on a `tel:` handoff, never fakes progress; a checkout submit shows inline progress and keeps its width; a dashboard number that refreshes should not tick every poll.
