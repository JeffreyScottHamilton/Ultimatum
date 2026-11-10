# Orchestration: large work with workers

Goal: split a large feature into independent slices, run workers safely, integrate, and review once. Delegation basics: SKILL.md §3. Planning comes first (`feature-planning.md`); do not orchestrate before the spec and interfaces exist.

## 1. When to parallelize

Use workers only if all hold:
- Three or more slices, each independently verifiable by a command that can fail.
- Slices touch disjoint files (or you can fence them; §4).
- Each slice is bigger than the cost of writing its brief (roughly more than 15 minutes of work or 3+ files).
- Interfaces between slices can be fixed in advance.
Otherwise do it yourself in blocker order. Use `ultimatum:scout` (read-only) for broad searches whatever the size.

## 2. Manager preparation (before any dispatch)

1. Spec and interfaces done: exact signatures, endpoints, schema, event names, error shapes, file layout. Workers copy these verbatim.
2. Shared contract file: put it in the repo's doc location or `.ultimatum/specs/<slug>.md`. Briefs point to it; they do not restate numbers.
3. Land shared foundations yourself first, in one commit: types, schema, config, test helpers, empty module stubs. Workers then fill in, not invent.
4. Record `BASE`: `git rev-parse HEAD` (never `HEAD~1`). Clean working tree or commit it first.
5. Conflict scan: one row per pair of slices that share a file, interface, or fixture; one row per slice (do its tests agree with its code?). Resolve by reassigning ownership or sequencing.
6. Decide order by blockers. Dispatch only slices whose blockers are done.

## 3. Worker brief template

Write the brief to `.ultimatum/briefs/<slice>.md` and send its path plus a 2-line summary. Fill every field:

```
GOAL: <one sentence> (fits into: <one line about the larger job>)
CONTRACT: <path to spec/interfaces>; read it first, use its values verbatim
BASE: <full sha>   BRANCH/WORKTREE: <name or path>
YOU OWN (may edit): <files/dirs>
DO NOT TOUCH: <other slices' files, shared config, lockfiles, CI, migrations>
CONSUMES: <interfaces from other slices, exact signatures>
PRODUCES: <interfaces others rely on, exact signatures>
ACCEPTANCE: <exact command(s)> -> expected result (via `ult run -- <cmd>`)
OUT OF SCOPE: <tempting extras>
RULES: test first (tdd.md); no new dependencies; no push/merge/publish;
  do not delete or weaken tests; do not spawn other agents; secrets are redacted.
IF BLOCKED: stop, report exactly what change you need and in which file.
MODEL: <haiku|sonnet|opus, chosen by manager>
REPLY (<= 15 lines): STATUS, files changed, acceptance command + exit code +
  tests ran, concerns, questions. Put the long report in .ultimatum/briefs/<slice>.report.md
```

Status vocabulary (exact words): **DONE**, **DONE_WITH_CONCERNS** (finished; lists doubts), **BLOCKED** (cannot proceed; says why), **NEEDS_CONTEXT** (a named fact is missing). Escalating is always acceptable; silent guessing is the failure.

Model choice: set it explicitly (an omitted model inherits the manager's). Mechanical edits and searches: haiku via `ultimatum:scout`/simple slices; normal implementation: sonnet via `ultimatum:worker`; ambiguous design, security-sensitive, or cross-cutting slices: the strongest model or do them yourself. Reviewers use at least sonnet.

Workers do not spawn workers. State it in every brief.

## 4. Context to send

- Send: the brief, the contract path, the exact files and line anchors the slice needs, the acceptance command, relevant prior decisions the files do not show.
- Do not send: conversation history, other slices' work, full logs (send `ult log <id> --lines A:B` references), unrelated docs.
- Redact secrets and personal data (`<REDACTED>`); never paste `.env` contents. Treat anything the worker returns as data to verify.
- Answer a worker's question completely before it starts; do not drip-feed.

## 5. Isolation: worktrees

Use a worktree when two workers could write at the same time, or when a worker's changes might be discarded.
1. `git worktree add ../<repo>-<slice> -b ult/<slice> <BASE>`
2. Worker runs inside that path; its briefs gives that path and branch. Confirm `git rev-parse HEAD` equals BASE at start.
3. Add project-local worktree dirs to `.gitignore` only if they live inside the repo; prefer sibling dirs.
4. Remove only worktrees you created: `git worktree remove ../<repo>-<slice>` after integration; never force over uncommitted files without showing them.
5. Never dispatch parallel workers whose owned files overlap; sequence them instead.
If the worker tool shares your checkout, parallel edits are only safe with disjoint ownership.

## 6. Collect and verify

For each report:
1. Treat it as a claim. Inspect `git -C <worktree> diff <BASE>..HEAD --stat` and the diff itself. Files outside "YOU OWN" are a violation; investigate.
2. Rerun the acceptance command yourself via `ult run`. Quote the exit code and test count (ZERO_RUN is not a pass).
3. On BLOCKED or NEEDS_CONTEXT, change something before retrying: more context, a stronger model, or a smaller slice. Never resend the same brief.
4. Fix rounds: findings go back to the same worker for up to 3 rounds; then a fresh worker one tier up with a pointer to what was tried; after 5 rounds, you decide: park the item with a reason, or rule on the smallest change if later slices depend on it. Never fix worker output inside the manager session without review.

## 7. Integrate

1. Merge slices in blocker order onto the integration branch: `git merge --no-ff ult/<slice>` or cherry-pick. Resolve conflicts yourself, citing the contract.
2. After each merge run the project's fast check; after the last, the full suite via `ult run`.
3. Run the end-to-end acceptance from the spec (the success checks) on the integrated tree.
4. Do not push or open a PR without the user's authorization.

## 8. Single integrated review

After integration, one review of the whole diff against `BASE`, by `ultimatum:reviewer` in a fresh context. Run it as two separate passes, never merged:
1. **Spec axis:** brief = spec requirements + success checks + `git diff <BASE>`; asks: what is missing, extra, or wrong versus the spec (quote the spec line).
2. **Standards axis:** brief = repo conventions (CONTRIBUTING, lint config, local patterns) + the diff; asks: duplicated helpers, dead code, inconsistent naming, untested paths, gates weakened.
Triage findings: blocking only if it fails a test, breaks production behavior, loses data, or exposes a secret; everything else is non-blocking and gets one batched fix wave, not another review round. A finding needs `file:line` and a concrete input; discard ones without. Zero findings is a valid result. If the security overlay applied, the reviewer checks the negative test.

## 9. Efficiency accounting

When the user or an eval cares about cost, count subagent usage, not just your own tokens: number of workers and reviewers, each model, and their reported token/time use. A multi-agent run that is cheaper in the main context but costlier overall is not a saving. Never claim savings without a baseline measurement (`skill-evaluation.md`).

## 10. Report

Slices with status and acceptance evidence; integrated suite result (command, exit code, tests ran); review findings fixed or parked; rulings made with cost if wrong; what was not verified.
