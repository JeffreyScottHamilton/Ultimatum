# Design review and QA tables

Lookup rows for `skills/website/references/craft/design-review-qa/`. Every cell is filled. Rows are our own wording.

- `design-checks.csv`: `id`, `category` (the audit's numbered checklist category), `check` (one thing to inspect), `file` (where the rule lives). Built from the two checklist files; the files are the source of truth.
- `slop-tells.csv`: `id`, `kind` (classic, rule, judgement), `tell` (the pattern), `instead` (what to do), `severity` (high or medium), `file`. Rule ids match `slop-tells.md`.
- `qa-issues.csv`: `kind` (severity or category), `name`, `meaning`, `example`, `score_effect` (points deducted for a severity, or the category weight in the health score). The `links` category is scored by count and is filed under functional in the taxonomy.

Scripts:

- `page_lint.py`: static checks on built HTML and CSS (`page-lint.md`).
- `render_check.py`: the same pages measured in headless Chromium (`render-check.md`).
- `mockup_board.py`: `build` lays two or more HTML mockups side by side on a local board with a pick, ratings and comments, and warns on near copies or missing axes; `read` checks the saved `feedback.json` against its board (`mockup-step.md`).
