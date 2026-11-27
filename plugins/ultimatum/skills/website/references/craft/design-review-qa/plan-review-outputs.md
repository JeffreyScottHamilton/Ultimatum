# Plan design review: required outputs and summary

Read when finishing a plan design review: the sections to add to the plan, how to compute the score, and how to record decisions.

## Sections to write into the plan

- **Not in scope:** design decisions that were considered and deferred, one line of reason each.
- **What already exists:** the design file, patterns and components the plan should reuse.
- **TODOs:** approved fixes go into the plan's tasks, not into an optional follow-up. Only unresolved or out-of-scope debt becomes a proposed TODO, asked one at a time. Each proposal has what, why, pros, cons, enough context for someone in three months, and what it depends on. Options: add it, skip it, or build it now in this change.
- **Implementation tasks:** only for agreed work. Unapproved remedies stay as pending findings.
- **Approved mockups** (only if any were made): screen, path, direction, notes.
- **Unresolved decisions:** every open finding, including ones not yet asked. Never silently default to an option.

## Score

Overall score is the lowest of the six rated passes (1 to 6), shown before and after the approved fixes. Pass 7 is not scored. The first-impression rating from step 0 gets its own row. An overall 8 or more means every rated pass is 8 or more. Unresolved findings stop the review being called clean even then.

Count only individually approved decisions under "decisions made"; a proposal or a next-step answer counts zero.

## Summary block

```
DESIGN PLAN REVIEW: SUMMARY
Audit            design-file status and UI scope
Step 0           first rating, chosen focus
Pass 1  info architecture   _/10 -> _/10
Pass 2  states              _/10 -> _/10
Pass 3  journey             _/10 -> _/10
Pass 4  generic risk        _/10 -> _/10
Pass 5  design system       _/10 -> _/10
Pass 6  responsive and a11y _/10 -> _/10
Pass 7  open decisions      _ resolved, _ deferred
Not in scope / already exists / TODOs: written (counts)
Decisions made _, deferred _ (listed)
Overall _/10 -> _/10
```

Write it as its own section of the plan, replacing any earlier summary from a previous review. After saving, read the file back to confirm it saved before saying the review is complete. If everything is 8 or more: "the plan is design-complete; run the live review after the build for a visual check". Otherwise name what is open and why.

## Review record

Where the project keeps a review log, add one line: date, status ("clean" when the overall score is 8 or more and nothing is unresolved, otherwise "issues open"), initial and final score, unresolved count, decisions made and the short commit id. Ultimatum has no shared dashboard for these; keep the line in the plan or the project notes (`later.md`).

## Next steps

Offer the live review (`design-review-modes.md`) once the build exists, and a second opinion on the plan (`second-opinion.md`) when the stakes are high.
