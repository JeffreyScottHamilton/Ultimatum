# Triage and fix loop for design findings

Read when the owner asked to fix what the audit found, not only report it. If the brief says report only, stop after triage and hand over the findings.

## Triage

Sort findings by impact: high first (first impression, trust), then medium (polish people feel without naming), then polish. A finding that source cannot fix (a third-party widget, copy only the team can supply, a photo that does not exist) is marked deferred whatever its impact.

## Before editing

- Start from a known state. If the working tree has other changes, tell the manager; our rule is that commits are made only when the user asks, so fixes are left as a reviewable diff by default and each fix is listed with its files. When the user does ask for commits, make one per fix.
- Find the responsible source with search; touch only files tied to the finding. Prefer CSS over structure, since CSS is safer and easier to undo.

## Per fix

1. **Locate** the rule or component, read its context.
2. **Fix minimally.** The smallest change that resolves the finding. No refactor, no extra feature, no unrelated polish. Stay inside the stack already in use, with no migration of framework or styling, and read the dependency file before importing anything. For Tailwind, write for the installed major version (v3 configures in a config file, v4 in CSS with `@import "tailwindcss"` and `@theme`).
3. **Re-test** the affected page the same way it was captured: same script, same widths, a fresh `finding-NNN-after` screenshot beside the before one. Console output may not be worse than the baseline; any new error counts as a regression.
4. **Classify:** verified (re-test passed, nothing new broke), best-effort (applied but could not fully check, say why), reverted (regression found; undo only this fix and mark the finding deferred).

Take a before and after pair for every fix.

## Order inside one impact level

Order by visible gain per unit of risk: typography, colour, then hover, active and focus states, then layout and spacing, motion, components, loading, empty and error states, copy and finally small finishing touches to the type scale.

## Regression tests for design fixes

Most design fixes are CSS-only: skip a test; re-running the audit is the guard. Write a test only when a fix changed JavaScript behaviour (a menu, an animation guard, conditional rendering, an interactive state). Then follow `qa-fix-and-tests.md` § Regression tests.

## Self-regulation

Every 5 fixes, and after any revert, work out a risk figure. Start at 0. Add 15 per revert, 5 per component file (JSX, TSX, template) changed, 20 for touching a file unrelated to the finding, and 1 per extra fix after the tenth; CSS-only files add nothing. Above 20: stop, show what is done, ask whether to go on. Hard cap: 30 fixes in one run.

## Final audit

1. Re-run the audit on every affected page.
2. Recompute both scores and the scan count the same way as the baseline.
3. If either score is worse than the baseline, warn first: something regressed.
4. Delete any saved page dumps unless the owner wants them kept.

## Report and follow-ups

Per fix, add status, files changed, and before and after pictures to the report (`scoring-and-baseline.md`). If the repo has a `TODOS.md`, add deferred findings (impact, category, description) and mark fixed ones with date and branch.

## Design-doc rule

You may write a design doc from the inferred system only when the owner accepted the offer. An existing design doc is never converted or rewritten unasked.
