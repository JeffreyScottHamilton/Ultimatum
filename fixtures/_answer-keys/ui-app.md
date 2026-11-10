# ui-app — answer key

**Task prompt:** "Add a Delete action on each project row with a confirmation dialog; deleting removes the row and shows a toast."

**Initial state:** `cd fixtures/ui-app && python3 -m unittest` -> exit 0, 4 tests OK (static checks only). Serve with `python3 serve.py 8765`.

**Must:**
- Reuse `components/button.js` (`Button.create`, variant `danger`/`secondary`) for the Delete button, `components/dialog.js` (`Dialog.open({... danger:true, onConfirm})`) for confirmation, `components/toast.js` (`Toast.show(msg,{type:"success"})`) after deletion. No new hand-rolled modal or toast.
- Use design tokens from `tokens.css` (`var(--space-*)`, `--color-*`); no hard-coded hex colors/magic px outside tokens.
- Delete removes the project from `window.PROJECTS` (or re-renders) and the row from the DOM; empty state still works.
- Changes confined to `app.js` / `styles.css` (+ `index.html` only if needed). Components should not need modification.

**Verification expected from the agent:**
- Viewports 375px and 1280px (screenshots/inspection). At 375px rows with long names (id 3, and id 4 with an unbroken ~80-char string) must not overflow horizontally; the Delete button stays visible and not clipped. (`.project-main{min-width:0}` + `overflow-wrap:anywhere` already exist; the button must not shrink/push out: e.g. `flex-shrink:0`.)
- Keyboard flow: Tab reaches Delete -> Enter opens dialog -> focus is inside dialog (Cancel is focused by default) -> Escape cancels (row remains, focus returns to the Delete button) -> reopen, Tab to Confirm, Enter -> row removed, toast shown.
- Dialog has `role="dialog"` and `aria-modal="true"` (provided by component). Delete button should have an accessible name including the project (e.g. `ariaLabel: "Delete <name>"`).

**FAIL conditions:** native `confirm()`; custom duplicate modal/toast; hard-coded colors; horizontal scroll at 375px; no keyboard verification; Escape does not cancel.
