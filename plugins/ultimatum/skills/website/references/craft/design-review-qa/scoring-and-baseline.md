# Scoring, baseline file, regression and report layout

Read when you must turn findings into grades, save a baseline to compare against later, or write the audit report.

## Two headline scores

- **Design score** (A to F): weighted average of the ten categories.
- **AI-slop score** (A to F): graded alone, with a one-line verdict. It also counts 5 per cent of the design score.

Category grade meanings: A intentional and polished; B solid with small inconsistencies; C works but generic, no point of view; D visible problems, careless; F actively hurts the visitor.

## Grade arithmetic

A category begins at A. A high-impact finding lowers it by a full letter; a medium-impact one by half a letter. Polish findings are noted and do not change the grade. The floor is F. Convert letters to numbers (A 4, B 3, C 2, D 1, F 0, with halves between) for the weighted average, then convert back.

| Category | Weight |
|---|---|
| Typography | 15% |
| Visual hierarchy | 15% |
| Spacing and layout | 15% |
| Responsive | 10% |
| Colour and contrast | 10% |
| Content quality | 10% |
| Interaction states | 10% |
| Generic look (slop) | 5% |
| Performance feel | 5% |
| Motion | 5% |

Untested categories are left out and the score is marked provisional with its coverage, never filled in.

## Baseline file

Write `design-baseline.json` into the report folder, via a temporary file then a rename so a crash never leaves half a file. Keep a per-run copy beside it. Our fields:

```json
{
  "schemaVersion": 1,
  "date": "YYYY-MM-DD",
  "url": "http://127.0.0.1:PORT/",
  "designGrade": "B",
  "genericLookGrade": "C",
  "grades": { "hierarchy": "A", "typography": "B" },
  "findings": [{ "id": "D-001", "title": "Body text under 16 px", "impact": "high", "category": "typography" }],
  "scan": { "mode": "rendered | source | none", "total": 9, "byRule": { "nested-cards": 4 } }
}
```

`scan.mode` is `none` when no scripted scan ran. Compare scans only when mode and the set of pages match; otherwise print "scan set changed, no delta".

## Regression output

When a previous baseline exists or regression was asked for: take the newest readable earlier baseline; unreadable means "previous baseline unreadable, treat as first audit". Print grade changes per category, findings that appeared, findings that went, and rule-id appearances and disappearances (for example `+ nested-cards (4)  - gradient-text (1)  total 6 to 9`). Live pages jitter, so counts are advisory; the appear and disappear list is the signal.

## Report layout

```
design-audit-{site}.md
screenshots/  first-impression.png  {page}-{mobile|tablet|desktop}.png
              finding-NNN-before.png  finding-NNN-after.png
design-baseline.json
```

Sections in order: headline scores, first impression (the four lines), inferred design system (fonts, colour count, heading scale, spacing values), per-category findings with impact, quick wins, flows with the goodwill lines, consistency, then (after fixes) the fix table: status, files changed, before and after pictures. End with one summary line for a pull request: "Reviewed the design: N issues found, M fixed. Design grade X to Y, generic-look grade X to Y."

Save reports under the project's `.ultimatum/` folder, never inside source folders, and never overwrite an earlier run.

## Overlap

The severities here (high, medium, polish) map onto the critic's blocker, major and minor in `../../website/design-rules.md` § 6: high maps to blocker or major, medium to major or minor by reach, polish to minor or nit. The `taste-critic` agent scores out of 10; the letter grades here are for audits of existing pages.
