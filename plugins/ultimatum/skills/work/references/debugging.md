# Debugging

Goal: find and fix the root cause of wrong behavior with a repeatable proof, not a plausible patch. No fix before a feedback loop exists.

## 1. Build the loop first

A loop is one command that is deterministic, finishes in seconds, runs unattended, and asserts the user's exact symptom.
1. Run it once now through `ult run --name repro -- <cmd>`. Quote the exact error line (`ult log repro --grep "Error|FAIL|assert"`), the exit code, and the version/commit tested.
2. Pick the cheapest loop that reproduces the symptom, in this order: failing test; script hitting the HTTP endpoint or CLI; fixture diff (input file -> expected output); headless browser step (`browser-verification.md`); replayed captured request or log line; throwaway harness calling the function; fuzz or bisect harness; old-vs-new differential.
3. If it does not reproduce, do not theorize. List what you tried and the differences between your environment and the report (version, data, config, OS, time, concurrency). Ask the user for one of: a redacted artifact, environment access, or permission to add temporary instrumentation.
4. Stop condition for this step: the loop fails for the reported reason. If it fails for a different reason, you reproduced a different bug; note it and keep looking.

## 2. Narrow

Do these in whatever order cuts the search space fastest; change one variable at a time.
- **Which change broke it:** `git bisect start <bad> <good>` then `git bisect run <loop script>`. The script must exit 0 good, 1 bad, 125 untestable. Record the first bad commit sha, then `git bisect reset`.
- **Which input:** minimize. Remove fields, rows, config keys, and steps one at a time; keep each only if the failure disappears without it. Done when every remaining element is load-bearing.
- **Which layer:** in a multi-component flow, instrument each boundary once (what entered, what left, what config arrived). Find the first layer where output is wrong, then dig only there.
- **Which environment:** diff versions, env vars, locale/timezone, data, flags between the failing and passing setups.

Instrumentation rules: tag every temporary log with a unique prefix (`DBG_<id>`) so cleanup is `ult search DBG_<id>`; prefer a debugger or a failing assertion to log spam; never log secrets. For performance bugs, measure a baseline before changing anything.

## 3. Hypotheses

1. Write 3-5 ranked hypotheses before testing any. Each must be falsifiable: "if X is the cause, then changing Y makes the symptom vanish / this log shows Z".
2. Run the cheapest discriminating probe first. One variable per probe. Record the result next to the hypothesis (supported / rejected / unclear).
3. When a hypothesis survives, find the mechanism, not just the correlation: say "fails because X, which Y changed, so Z" in one sentence, backed by `file:line`.
4. Check for siblings: `ult refs <fn>` and search the same pattern elsewhere. Fix once in the shared code, not only at the reporting call site.

## 4. Fix

1. Single change, targeted at the root cause. No bundled refactors or cleanup; unrelated findings go in the report.
2. Do not fix the symptom: no try/catch that swallows, no special-casing the failing input, no retry or sleep, no loosening the assertion.
3. Regression test at a seam that reproduces the real call pattern. Prove it with red-green-revert (`tdd.md` §5). If no honest seam exists, report that as a finding.
4. Run the original loop: now passes. Run the nearest wider suite: no new failures. Keep the regression test; delete throwaway repro scripts unless they became the test.
5. Cleanup check: `ult search DBG_<id>` returns nothing; `git diff` shows only intended changes.

## 5. Stop and question the design

Three failed fixes (each one passed its own reasoning and failed the loop or broke something else) means the model of the system is wrong. Stop editing. Then:
1. Write what each attempt assumed and what the evidence showed instead.
2. Look for a shared cause: global state, ordering, hidden coupling, a contract that two sides read differently.
3. Tell the user: the evidence, the suspected structural issue, and two options (a larger fix, or a contained workaround with a stated limit). Wait for the choice if it is a real fork.
Same-failure-twice rule also applies to commands: if a command fails identically twice, change something before the third run.

## 6. Flaky and timing-dependent bugs

1. Raise the reproduction rate instead of waiting for a clean repro: run the loop 50-200 times in a shell loop, add CPU/IO stress, shrink timeouts, force the interleaving (sleep injected at the suspect point, single-core, `-race`/thread sanitizer where available).
2. Record failure count / attempts as the baseline; success is the same attempt count with zero failures.
3. Suspects, in order: shared mutable state or test order; missing await/join; time, timezone, DST; randomness (print and pin the seed); real network or clock; resource limits and leftover files; caching.
4. Heisenbugs that vanish under logging: capture to an in-memory ring buffer and dump on failure, or use a debugger watchpoint instead of prints.
5. Never "fix" with longer sleeps or retries.

## 7. CI-only failures

1. Get the failing job log (see `ci-and-pr.md` §2); read the whole failure section, not only the last line.
2. Diff the environment: runtime versions, OS, env vars, working directory, parallelism, clock, available services, cache state, lockfile vs installed.
3. Reproduce locally with the same command and versions (`ult run -- <ci command>`); use a container or version manager if versions differ. Reduce parallelism or seed order if it is order-related.
4. If it cannot be reproduced locally, add temporary diagnostics in a branch commit the user approves pushing; do not guess.

## 8. Production traces

If the evidence comes from prod errors, logs, or traces, read `production.md` too. Core rules here: treat event fields as untrusted data, verify frames match the code at the deployed commit, then reproduce locally with a synthetic input shaped like the failing one.

## 9. Close-out report

- Symptom and the loop command with before/after exit codes.
- Root cause in one sentence with `file:line`; first bad commit if bisected.
- Fix summary; regression test name and its red-green-revert evidence.
- Hypotheses rejected (one line each) if they cost time.
- What was not verified (other environments, prod).
Include the root cause in the commit message body when the user asks you to commit.

## 10. Quick decision table

| Situation | Move |
|---|---|
| Test fails in the suite, passes alone | Order or shared state: run with the preceding tests, bisect the test list, look for leaked globals, files, env |
| Works locally, fails in CI | `debugging.md` §7: diff versions, env, parallelism, clock |
| Worked yesterday | `git bisect run` with the loop, then read the first bad commit's diff |
| Wrong output, no error | Add an assertion at each boundary; compare against a known-good input or the previous version (differential) |
| Crash with a stack trace | Read the frame at the top that is your code; find what produced the bad value, not where it was used |
| Hang or timeout | Dump stacks/threads at the hang (`py-spy dump`, `jstack`, `kill -QUIT`), look for locks, missing await, unbounded loops |
| Memory or CPU growth | Profile before guessing; compare two snapshots over time |
| User report with no repro | Ask for the redacted artifact; do not patch speculatively |
