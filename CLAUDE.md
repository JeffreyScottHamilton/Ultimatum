# Working on Ultimatum

- The plugin lives in `plugins/ultimatum/`. `skills/work/SKILL.md` is the router; keep it under 20 KB and put occasional material in `skills/work/references/`.
- Unit tests: `python3 -m unittest discover -s plugins/ultimatum/tests`
- Validation: `claude plugin validate . --strict` and `claude plugin validate plugins/ultimatum --strict`
- The toolbelt (`scripts/ult`, `scripts/ultlib/`) is Python standard library only, with no network access.
- Any change to the plugin bumps `version` in `plugins/ultimatum/.claude-plugin/plugin.json` and adds a `CHANGELOG.md` entry, otherwise installs don't update.
- Original wording and code only; never copy upstream text (`research/REVISIONS.md`).
- Claim only what was run. Live evals (`evals/live/run_live.py`) cost money; ask before running them.

## Learned
