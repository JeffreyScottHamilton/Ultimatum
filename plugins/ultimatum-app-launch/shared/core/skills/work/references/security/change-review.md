# Security review of a change

Goal: decide whether a diff, PR, or branch opens a security hole, with evidence. The diff tells you where to look. The vulnerability is usually in what the diff connects to.

Default posture: read-only. Run the project's own tests only if the user agreed or the task already includes running them. Never send requests to a deployed system.

## 1. Resolve the change

- Branch or PR: `git diff <base>...HEAD` (merge-base). Uncommitted: `git diff <base>`. PR by number: `gh pr diff <n>` or the GitHub MCP, if available.
- Record the base ref, the head sha, and whether the tree is dirty. List the files changed (`git diff --stat <base>...HEAD`).
- If the diff is huge, review security-relevant hunks first (below) and say in the report what you skipped.

## 2. Triage hunks by risk, not size

Mark each hunk with the surfaces it touches, from `coverage-model.md`: authn/session, authz/tenant, injection sinks, files/paths, SSRF, parsing, money, data exposure, secrets, crypto, config defaults, CORS/CSP/cookies, CI, deploy/IaC, dependencies, agent/LLM tools.

High until proven otherwise:
- **Removed or loosened checks.** A deleted decorator, a dropped `where owner_id = ...`, a widened role list, a check moved after the action, or an `if` changed from `and` to `or`. For each, run `git log -S '<removed text>' --oneline` and `git blame <base> -- <file>` to learn why the check existed, then find what replaced it.
- "Refactors" that touch auth, validation, or query building.
- New routes, handlers, jobs, or webhook endpoints.
- New defaults or config values (debug, CORS, cookie flags, timeouts, permissions).
- Dependency additions or version changes, and lockfile churn.
- CI workflow edits.

## 3. Read the execution path, not just the hunk

For each risky hunk:
1. **Callers and entry points:** `ult refs <fn>` and `ult map query routes`. Find every way an actor reaches the changed code.
2. **Controls before and after:** middleware, decorators, router guards, base classes, policy calls, query scoping, serializer allowlists, DB constraints, and RLS. Read them, and confirm they apply to this path (route registration order, excluded paths, method lists).
3. **Config and defaults:** settings files, env defaults, feature flags, and framework defaults the change relies on.
4. **Siblings:** handlers that do the same thing for another method or shape (GET vs PUT/PATCH/DELETE, single vs list/bulk/export, v1 vs v2, UI route vs API route, admin vs user). If the change fixes or adds a rule in one, check all of them.
5. **Tests:** does any test exercise the security-relevant behavior, and would it fail if the guard were deleted?

## 4. Coverage of categories

Before concluding, go through the categories in `coverage-model.md` §3. For each category the diff touches, say checked (with `file:line`) or not checked (with the reason). For categories it does not touch, a single line "not touched by this diff" is enough. Use the review preset if you want this tracked: `ult findings ledger init --preset review --scope "<base>...<head>"`.

## 5. Deterministic tools (leads only)

Run `ult scan --diff <base>`. It runs installed scanners in offline-safe mode plus built-in checks, limited to changed files and lines, and lists removed lines that look like guards (`diff-removed-guard`, line numbers in BASE). Add `--semgrep-config <local rules>` only if local rules exist. Registry packs (`p/...`) need network access and the user's consent. Read the printed lines that say which commands ran and which tools were not run.

Every lead needs a code read. Discard a lead only with a reason (`findings.md` §4, false-positive patterns). A dependency advisory is `unknown` unless osv-scanner ran. Say so; don't call the dependencies clean.

## 6. Verify serious candidates

For anything you would call high or critical, or report as confirmed, brief a fresh `ultimatum:security-verifier` with the candidate, the relevant paths, the threat model (who the actors are), and whether running local tests is authorized. Don't pass your own reasoning. Its verdict is input: re-check the cited lines yourself before reporting.

## 7. Write-up

Each finding states:
- **Where:** `file:line` and the endpoint or entry point.
- **Who and what:** the actor (role, tenant, authenticated or not) and the input they control.
- **Boundary:** the rule that should hold and how this change breaks it.
- **Conditions:** role, config, flag, or timing needed. Use "none beyond a normal account" when that is the case.
- **Impact:** what was shown (which data or actions, whose), not what could happen in the worst case.
- **Evidence:** quoted lines, the control you checked and why it does not stop this, and a test or command with its exit code if one ran.
- **Fix:** the smallest change, plus the regression test.

Record findings with `ult findings add < candidate.json` (`findings.md` has the fields), then run `ult findings validate`. Redact secrets everywhere as `[REDACTED:<kind>:<last4>]`. Never quote a secret, even from the diff.

## 8. Output format

```
Security review: <base>..<head> (<n> files; dirty: yes/no)
Verdict: <n> confirmed, <n> need validation, <n> rejected. <one-line posture>
Confirmed:
  [high] F-001 <title> — <file:line> — <actor> can <action> → <impact>
Needs validation:
  F-002 <title> — missing: <exact fact>
Rejected (with reason): F-003 <title> — <control at file:line>
Coverage: read <files/paths>; categories touched: <list, each checked/not checked>; not covered: <what and why>
Tools: <commands that ran + exit codes>; not run: <tool: reason>; advisories: <status>
```

With no confirmed findings, write "No confirmed findings in <scope>; coverage: <what was read>. Not evidence of absence." Never write "no issues" without a scope.
