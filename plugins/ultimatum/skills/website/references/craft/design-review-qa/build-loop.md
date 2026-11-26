# Build loop: checking UI states while it is being built

Read when a section of UI is under construction (a settings list, a table, a form with confirm and error states) and each state needs a quick look before the work is called done. It replaces the full audit; it never commits, stashes or resets, and when unattended it records "needs input" instead of asking.

## The seven items to check on every screenshot

| # | Item |
|---|---|
| 1 | Row padding holds with one line of text and with two |
| 2 | Neighbouring rows have room to breathe |
| 3 | Help text sits clear of the list above it and uses the same muted style as sibling sections |
| 4 | A status note gets a separate line in a warning style instead of being squeezed into a row |
| 5 | Heading, then name, then hint, laid out as the sibling sections do it |
| 6 | Hit areas are comfortable (44 px) |
| 7 | Nothing overflows at 375 px |

For items 3 and 5 the repo's own sibling sections are the standard; judge against one of them.

## 1. Inventory of states

List every state the change can show: each user role or scenario, crossed with busy, success, error and empty, plus overlays such as a confirm dialog. Save as a small JSON file next to the screenshots:

```json
{ "section": "#settings-members",
  "states": [
    { "name": "owner", "url": "http://127.0.0.1:5300/settings?as=owner" },
    { "name": "empty", "url": "http://127.0.0.1:5300/settings?as=empty" },
    { "name": "remove-confirm", "steps": "press the Remove control in row two" } ] }
```

A state reached by URL is lintable; one that needs clicks is screenshot-only and is counted as looked at, not scanned.

## 2. Preflight

- The preview runs on `127.0.0.1` only and answers API calls from fixture files, never from a live backend. Without a way to guarantee that, do not click actions that might reach a real service.
- Each state loads and shows the element that proves it rendered with its data (check the selector, not just the status code).
- If the browser or preview is missing, say so and stop; that is "not run", not a pass.

## 3. Rounds (three at most)

1. Run the scripted checks on every URL state (`design-audit-recipes.md`) and read the numbers, never only an exit code.
2. Screenshot each state at its width (390 and 1280 by default); save under the run folder.
3. Go through the seven items against each screenshot.
4. Exercise every changed action in its busy, success, error and recovery forms, and confirm that closing with the keyboard puts focus back on the control that opened it.
5. Fix in source and fixtures; leave edits uncommitted.

A state that fails to render is a harness problem: fix its cause and rerun that state. Stop after round 3, or sooner when a round is clean.

## 4. Final read-only pass and receipt

After the last edit make one pass that changes nothing, then write a single receipt line with the outcome and round count.

| Outcome | Means | Next |
|---|---|---|
| clean | all URL states seen at all widths, with a shot of each and no open finding | report it |
| open | full coverage, open findings | each gets a fix or a reasoned waiver, or a line in the PR text |
| incomplete | a state not checked at every width, not shot, or evidence is stale | name the gap; list the rest as unverified |
| not rendered | install, browser or preview missing | say what is missing |
| stale | files changed after the receipt was written | run the final pass again |

Only the receipt written after the last edit counts. An incomplete run never satisfies a "done" claim.

## Merge note

The seven items extend `../../website/feel-bar.md` and `checklist-visual.md` for state-heavy UI; the fixture-backed preview idea is ours to write (`later.md` lists the missing helper).
