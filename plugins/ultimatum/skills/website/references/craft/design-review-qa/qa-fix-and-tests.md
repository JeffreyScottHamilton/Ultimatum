# QA fix loop and regression tests

Read when a QA run should also fix what it finds, or when adding a test for a fixed bug. The design-side loop is `fix-loop.md`; this one is for functional and browser bugs.

## Phases after the report

1. **Triage.** Sort by severity. Choose the tier: Quick (critical and high), Standard (adds medium), Exhaustive (adds low). Mark findings you cannot fix from code (third-party, needs an owner decision) as deferred.
2. **Fix, one at a time.** Find the cause in source, make the smallest change, and keep each fix as its own reviewable change. Commit only if the user asked for commits.
3. **Repeat the failure.** Re-run the exact steps from the same start state; capture after-evidence.
4. **Regression test** where one is warranted (below).
5. **Re-run the affected probes**, then a final pass over the scope, and recompute the score.
6. **Update the report** with before and after, what was fixed, deferred and left.
7. **Record leftovers** as TODO entries or issues, only if the project keeps them and the user wants that.

## Self-regulation

- Cap at 50 fixes in one run. Stop and report when reached.
- After every five fixes, re-run the sweep; if the score fell or a new failure appeared, stop and revert the last change.
- Stop and ask when a fix touches more than three files, changes a public contract, or needs data you do not own.
- If two attempts at one bug fail, defer it with notes. Do not keep guessing.
- Never weaken or delete an existing test to get green.

## Regression tests

Write one for a fixed bug when the fix changed behaviour code can check. Skip it for copy, spacing and other visual-only changes.

- Smallest level that catches it: unit for logic, integration for state and requests, end-to-end only when smaller tests miss the journey.
- Name it after the behaviour, with the finding id in a comment, not "test bug 12".
- Show it fails without the fix (revert the fix or run the test before applying it) and passes with it. Say whether you did that.
- Assert the correct behaviour, never the buggy output.
- Mock only unrelated services. Keep fixtures local and small.
- Match the project's test style and runner; do not add a new framework for one test.

## Setting up a test runner

Only when the project has none and tests are needed. Detect the stack from its files, then use the common default.

| Marker file | Stack | Default runner |
|---|---|---|
| `package.json` | Node | the project's script, else Vitest ([docs](https://vitest.dev/)) |
| `pyproject.toml` or `requirements.txt` | Python | pytest ([docs](https://docs.pytest.org/)) |
| `Gemfile` | Ruby | the existing suite (RSpec or Minitest) |
| `go.mod` | Go | the standard `go test` command |
| `Cargo.toml` | Rust | `cargo test` |
| `composer.json` | PHP | PHPUnit |
| none | static site | a Playwright script from `qa-playwright-recipes.md` |

Ask before adding a dependency. If the user declines, record the missing runner as a TODO and carry on without tests.

## Final report additions

Fixes made (id, change, test), fixes deferred (why), the score before and after, and the list of files touched. Only claim a test passed if you ran it and saw the exit code.

## Checking a fixed browser bug

Re-run the original steps and one nearby happy path. Take the after screenshot under a fresh name (`F-003-after.png`; add a suffix if it exists) and compare it, the console output and the failed-request list with the before evidence. For an interaction bug, use the same script with the same waits as the reproduction, in one run from the affected URL (a new browser context starts empty). A functional fix is checked by re-running its probe, not by this routine.
