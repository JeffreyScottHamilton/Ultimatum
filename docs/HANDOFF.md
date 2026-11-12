# Handoff: continuing Ultimatum

Paste the section below into the next assistant. It is self-contained.

---

You are continuing work on **Ultimatum**, a free, open-source Claude Code plugin with one entry command, `/ultimatum:work <task>`. The repository is `JeffreyScottHamilton/Ultimatum`, branch `main`. Work on a new branch off `main` and do not merge, open a pull request, or publish a release unless the owner asks.

## Read these first
1. `README.md`: layout and how to try the plugin.
2. `docs/TEST-REPORT.md`: what was tested live, the results, and what was not tested.
3. `docs/COVERAGE-MAP.md`: 419 upstream capabilities and where each is covered, or why not.
4. `research/ARCHITECTURE-DECISIONS.md`: the 15 design decisions and their reasons.
5. `plugins/ultimatum/skills/work/SKILL.md`: the router. Everything else hangs off it.

## Current state
- The plugin lives in `plugins/ultimatum/`: router skill, 24 on-demand references (`skills/work/references/`), 5 subagents (`agents/`), a Python-stdlib toolbelt (`scripts/ult`, `scripts/ultlib/`), a Playwright browser check (`scripts/ult-browser.mjs`), schemas, and unit tests.
- Unit tests pass: `python3 -m unittest discover -s plugins/ultimatum/tests` (run from inside `plugins/ultimatum/tests` or with `-s`).
- `claude plugin validate . --strict` and `claude plugin validate plugins/ultimatum --strict` pass.
- Live A/B results against plain Claude Code are in `evals/live/results/`. Both arms did every task correctly (21/21). Ultimatum met the evidence and process requirements more often (19/21 against 10/21) and cost about 1.8x more. There is no token-savings evidence. Do not claim any.
- The routing suite passes 16/16 (`docs/ROUTING-TEST.md`).
- After those results, the audit guidance was changed so a read-only audit keeps its state outside the repository (`ULTIMATUM_STATE_DIR`). Six further audit runs then passed every check (`evals/live/results/audit-recheck-*`).

## Rules that must keep holding
- Original wording and code only. Several upstreams are CC BY-SA, ELv2, GPL, or have no license file (`research/REVISIONS.md`). Never copy upstream text or code. Cite standard IDs (ASVS, WSTG, CWE) only.
- The toolbelt stays Python standard library only, with no network access.
- No hooks, telemetry, MCP servers, or proxies in the default install.
- Exact evidence is never compressed: exit codes, error strings, `file:line`, and security evidence stay verbatim.
- Report only what was run. Mark anything untested as untested.

## Unfinished work, in priority order
1. **Gaps listed in `docs/COVERAGE-MAP.md`**, top ones: secret scanning of git history (`ult scan` runs gitleaks on a directory only); an audit coverage-critic step; aggregation and trigger-eval tooling for skill evaluation; PR-description and finish-branch guidance.
2. **Untested areas** from `docs/TEST-REPORT.md` section 5: larger repositories and other languages, other models, audits that fan out to several hunters, the live MCP integrations, a successful OSV-Scanner advisory lookup, and installing from the GitHub marketplace URL.

## How to verify a change
- Toolbelt or script change: add or update a test in `plugins/ultimatum/tests/`, then run the unit suite.
- Guidance change (SKILL.md, a reference, an agent): run the affected live case, e.g. `python3 evals/live/run_live.py --cases 6-audit --arms ultimatum --budget 6`. Live runs call real Claude sessions and cost money (about $0.05 to $0.50 each). A run cut off by a usage limit is marked INVALID and must be re-run.
- Fixture answer keys are in `fixtures/_answer-keys/`. Never show them to an agent under test.
