# Live A/B evals

`run_live.py` runs each fixture case headless with `claude -p` per arm, grades it with
deterministic checks, and writes one JSON record per run. `summarize.py` turns result
directories into tables.

## Run locally

Live runs call the Anthropic API and cost money. You need an API key and the `claude` CLI:

```
export ANTHROPIC_API_KEY=...          # your key
python3 evals/live/run_live.py --dry-run --arms vanilla,v041,v2   # free: plan and max cost
python3 evals/live/run_live.py --cases 1-one-file --arms vanilla,v2 --budget 1
python3 evals/live/summarize.py evals/live/results/<timestamp>
```

## Spend cap

`--max-total-usd` (default 15) caps cumulative cost across all runs. Each run reserves
`--budget` (default 3, passed as `--max-budget-usd`) before it starts and settles to its
real `total_cost_usd`. A run that does not fit in the remaining budget is skipped and
listed in `skipped.json`. With the defaults only 5 runs fit, so lower `--budget` to
cover a full plan (for example `--budget 0.5` for 30 runs).

## Arms

- `vanilla`: no plugin; alias `baseline`.
- `v041`: plugin from a detached git worktree of commit `e35cea12`, in a temp dir, removed afterwards. Run `git fetch origin main` first so that commit is present.
- `v2`: plugin from `plugins/ultimatum`; alias `ultimatum`.

Plugin arms use the `/ultimatum:work` prefix. All arms run with an isolated config dir.

## Reporting

Report results only from real runs in `evals/live/results/`. Never report numbers from
`--dry-run`, from a regrade, or from memory. Say which arms, cases, model and budget were used.
