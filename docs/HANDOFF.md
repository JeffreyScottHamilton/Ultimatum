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
- No telemetry, MCP servers, or proxies in the default install. Hooks (`hooks/hooks.json`): the read-only post-compaction handoff hook (0.3.0) and the opt-in chat-size guard (0.2.7, off unless `ULTIMATUM_GUARD=1`).
- The main session orchestrates and never edits project files; workers make every edit (SKILL.md rule 7). It never asks the user to open a new chat.
- Exact evidence is never compressed: exit codes, error strings, `file:line`, and security evidence stay verbatim.
- Report only what was run. Mark anything untested as untested.

## Unfinished work, in priority order
1. **Re-run the live A/B for 0.3.0.** Always-delegate (rule 7) and the compaction hook are unmeasured. Run the nine cases with 3 runs per arm, counting subagent tokens, and update `docs/TEST-REPORT.md`. The 16 routing dry-runs still expect no agent, because they do not implement anything.
2. **Three-way quality test (highest value).** Every comparison so far is Ultimatum against plain Claude Code, never against the original upstream skills. Extend `evals/live/run_live.py` with a third arm that installs the relevant upstream packs (for example Superpowers, Trail of Bits, Impeccable) into the isolated config dir. Run cases 1–9 with 3 runs each, and record correctness first, then cost. Budget is roughly $5–8 per round.
3. **Measure the efficiency coach on real use.** After a week of normal use, run `ult usage report --since 7d` and use `ult improve` on one finding. Then check whether the 200k auto-compact window (`CLAUDE_CODE_AUTO_COMPACT_WINDOW=200000`) reduced tokens per session. Record the results in `docs/TEST-REPORT.md`.
4. **Remaining gaps** are listed in `docs/COVERAGE-MAP.md` (47 gaps; 117 rows marked partial).
5. **Untested areas** are in `docs/TEST-REPORT.md` section 5: large real repositories, other models, multi-hunter audits, live MCP integrations, and OSV advisory lookups.

## Version history since the first handoff
- 0.1.1: CI added (Python 3.9/3.11/3.13 without ripgrep, plus plugin validation). Fixed two search crashes on the no-ripgrep path.
- 0.2.0: efficiency coach (`ult usage report`, `ult improve`, `improve` route, `self-improvement.md`). Tested live: auto-invoked, $0.09 per review, no prompt text in reports.
- 0.2.1: fixed `ult note` reference collisions within one millisecond. This was the earlier unreproduced test failure.
- 0.2.2: handoff refreshed at milestones so work survives compaction. README documents the 200k context cap.
- 0.2.3–0.2.6: git-history secret scan, rule "keep the conversation small", zero-overhead routing, `ult context`.
- 0.3.0: orchestrator-only main session, post-compaction hook, no fresh-chat advice, Learn step. See `CHANGELOG.md`.
- Making Claude use Ultimatum without being asked needs one line in `~/.claude/CLAUDE.md`. Tested 0/3 without it and 3/3 with it. See the plugin README.

## How to verify a change
- Toolbelt or script change: add or update a test in `plugins/ultimatum/tests/`, then run the unit suite.
- Guidance change (SKILL.md, a reference, an agent): run the affected live case, e.g. `python3 evals/live/run_live.py --cases 6-audit --arms ultimatum --budget 6`. Live runs call real Claude sessions and cost money (about $0.05 to $0.50 each). A run cut off by a usage limit is marked INVALID and must be re-run.
- Fixture answer keys are in `fixtures/_answer-keys/`. Never show them to an agent under test.
