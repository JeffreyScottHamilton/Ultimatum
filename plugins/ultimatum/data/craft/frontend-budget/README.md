# Frontend budget data

Scripts for `skills/work/references/craft/frontend-budget/`. Standard library only, no network.

| Script | What it does |
|---|---|
| `load_budget.py` | `size` estimates the tokens each skill, agent or reference file costs when it loads and flags files over a limit; `plan` checks a phase plan (one lead, at most two supports, no clashing or stacked presets, optional token cap per phase) and prints one load line per phase. `--self-check` runs its own tests. |
