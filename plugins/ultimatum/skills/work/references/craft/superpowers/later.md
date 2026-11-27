# Superpowers: parts not rebuilt

Read when you wonder whether some Superpowers feature exists here; most of what is left out runs code or belongs to the source's own harness.

Routing for the rebuilt parts is in `index.md`; the main router is `../../../SKILL.md`.

| Source part | Why it is not here |
|---|---|
| Session-start injection and the "use the skills" bootstrap | excluded by the brief; it runs at session start and Ultimatum routes with `ult route` instead |
| Brainstorm visual companion and its local server | excluded by the brief; it runs a server. Text sketches stay (`shaping-conversation.md` § Show it) |
| The workspace, brief, task-start, task-done and review-package shell scripts | runtime scripts; the same records are kept by hand in `.ultimatum/` (`plan-execution.md` § The ledger) |
| `find-polluter.sh` | not run, per the rules; `find_polluter.py` is our own stdlib version |
| The TypeScript condition-wait example | replaced by our Python `wait_until.py` |
| Skill-writing and skill-testing skill, and the skill self-diagnosis skill | outside this brief's list; skill work lives in `../../skill-author.md` and `../../skill-evaluation.md` |
| Per-platform tool maps and harness-specific dispatch notes | tied to other agent harnesses; our helper rules are in `../../orchestration.md` |
| The implementer, task-reviewer and re-review prompt files | merged: review briefs are in `review-rounds.md`, and the worker brief template is in our orchestration file (`../../orchestration.md` § 3) |
| Field results quoted in the source (test counts, pass-rate gains) | measured by the source on its own projects; not re-run here, so no numbers are repeated |
