# Contributing

Thanks for helping. A few rules keep the plugin working for everyone who installs them.

## Before you open a pull request

1. Run the checks:

   ```bash
   python3 -m unittest discover -s plugins/ultimatum/tests
   ```

   ```bash
   claude plugin validate . --strict
   ```

2. **Bump the version.** Claude Code only updates an installed plugin when the `version` in its `.claude-plugin/plugin.json` changes. Any change inside a plugin needs a version bump and a `CHANGELOG.md` entry. CI enforces both.
3. **Website guides live in `plugins/ultimatum/skills/website/references/`.** Edit them there.

## Code and writing

- The toolbelt (`plugins/ultimatum/scripts/ult` and `scripts/ultlib/`) is Python standard library only and makes no network calls.
- Keep `plugins/ultimatum/skills/work/SKILL.md` under 20 KB; put occasional material in `skills/work/references/`.
- Write original wording and code. Ideas from other projects are welcome when they are credited in `docs/CREDITS.md`; copied text or code is not.
- Claim only what you ran: say which checks you ran and what they printed.

## Live evaluations

`evals/live/run_live.py` starts real Claude sessions and costs money. Use `--dry-run` to see the plan and `--max-total-usd` to cap the spend. Pull requests never need a live run.
