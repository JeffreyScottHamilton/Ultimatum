# Test-driven development

Goal: every new or fixed behavior is pinned by a test you watched fail for the right reason, then pass, with the evidence in this session. Loop context: SKILL.md §3 steps 3-4.

## 1. Cycle (one behavior at a time)

1. **Pick one behavior** from the slice's acceptance list. Name the test after the behavior ("rejects expired token"), not the function.
2. **Choose the seam.** Use an existing public interface (HTTP handler, exported function, CLI, component render) at the highest level that observes the behavior. Check existing tests for the project's style (`ult search "describe\(|def test_" --path tests`). Prefer few seams over many.
3. **RED.** Write the test only. Run it alone: `ult run -- <runner> <single test>`. It must fail, and for the right reason:
   - Quote the failing assertion line from the output (`ult log last --grep "Assert|Error|expected"`).
   - The message must describe the missing behavior (expected 404, got 200). Reject: import error, typo, missing fixture, syntax error, wrong test path. Fix those and rerun until the failure is about behavior.
4. **GREEN.** Write the least code that passes. Run the single test, then the file, then the nearest suite. Quote exit code 0 and the pass count.
5. **REFACTOR.** Only while green. Remove duplication you introduced, rename, extract. Rerun the file after each step. No new behavior in this step.
6. Repeat from 1. Do not write a batch of tests ahead of the code; one slice at a time keeps each failure interpretable.

## 2. Stop conditions

- The test passes immediately in step 3: you are testing existing behavior, a vacuous assertion, or the wrong path. Run the flip check (§6), fix the test, or conclude the behavior already exists and say so.
- Three attempts at GREEN fail with unrelated errors each time: stop, reread the seam and the contract, ask or switch approach (see `debugging.md` §8).
- The code is untestable without mocking internals: that is a design finding. Introduce a seam (inject the clock, client, or repo) rather than patching privates.

## 3. Green means tests ran

- Exit code 0 with **zero tests executed** is ZERO_RUN, which is a failure state, not green. Check the count in the output: "collected 0 items", "No tests found", "0 passing", `Ran 0 tests`, a glob that matched nothing, a filter that excluded everything.
- Report the number that ran. If the runner does not print a count, say "count unknown" rather than claiming a pass.
- A changed source file no test touches is UNMAPPED: add a test or state the file is untested and why.
- Missing tool, service, secret, or network is an environment failure: report the log line and stop. Do not skip, stub, or delete the test to get past it.
- Run order while working: the single test, then its file, typecheck/lint occasionally, then the full suite once before claiming done. Warnings in test output are findings.

## 4. Test through behavior

- Assert on outputs and observable effects (return value, response, rendered text, stored record read back through the public API), not on call counts, private methods, or internal state.
- Mock only at system boundaries: network, clock, randomness, filesystem or DB when slow. Never mock the unit under test or its internal collaborators. Prefer one small injected function per external operation.
- Expected values come from a literal, a worked example, or the spec. Never recompute the expected value with the production formula; that is a tautology.
- One behavior per test; table-driven for many inputs of the same behavior.
- Cover, per behavior: the main case, an empty or minimal input, a boundary, an invalid input, and the permission-denied case when auth applies.

## 5. Regression tests (bug fixes)

A regression test is proven only by red-green-revert:
1. Write the test reproducing the reported symptom through the real call pattern. Run it on unfixed code: RED, quote the assertion.
2. Apply the fix. Run: GREEN.
3. Revert only the fix (`git stash push -- <src file>` or comment out the change). Run: it must be RED again with the same assertion. Restore the fix, run once more: GREEN.
4. If a failure was produced by mutating a fixture or file, `git diff` it to confirm the mutation landed.
5. If no seam reproduces the real call pattern, say so in the report. A too-shallow test that stays green on the bug is false confidence.

Security overlay changes use the same proof for the negative test (see `security/secure-implementation.md`).

## 6. Smells: tests that pass even if the change is reverted

Run the **flip check** on any suspicious green: change one expected value or revert the change; the test must fail. If it still passes, it is vacuous. Typical causes:
- no assertion, or assertion inside a callback/promise that never runs (await missing)
- `expect(x).toBeDefined()`, `assert result`, `len(items) >= 0`
- asserting on a mock you just configured
- asserting source text, export lists, or snapshots updated blindly
- catch-all `try/except` that swallows the failure
- loop over an empty collection; parametrized cases that resolve to nothing
- conditional assertion (`if x: assert ...`) whose branch never runs
- test hits the old code path through a stale build, cache, or compiled output
Also flag near-duplicate tests and production code kept alive only by its test.

## 7. Property-based tests

Use when the input space is large and you can state a rule that holds for all inputs (parsers, serializers, sorting, money math, path handling, state machines). Use the project's existing library (`hypothesis`, `fast-check`, `proptest`, `gopter`) if present; do not add a dependency for one test, use a seeded loop over generated inputs instead.
1. Pick the invariant kind: **round-trip** (`decode(encode(x)) == x`), **oracle** (compare with a slow obvious implementation or a trusted library), **idempotence** (`f(f(x)) == f(x)`), **monotonic/ordering**, **conservation** (totals unchanged), **no-crash** on arbitrary input.
2. Generators must produce the hard values: empty, huge, unicode, negative, boundary, duplicates. A generator that only yields friendly values is vacuous; print a few samples or assert coverage to check.
3. Avoid tautologies: the property must not re-implement the code under test. Keep a few example-based tests for known cases next to it.
4. Pin the seed in CI output; when it finds a failure, minimize it, then freeze the failing input as a plain example test (the regression).
5. Flip check: break the code deliberately; the property must fail.

## 8. Flaky tests

1. Confirm: rerun the single test 20-100 times (`ult run -- <loop>`). Record the failure rate.
2. Classify the cause: shared state or order dependence, time or timezone, randomness, real network, concurrency or missing await, resource leak, leftover files.
3. Fix the cause (inject clock, seed, isolate state, await the condition). Never fix with a longer sleep, a retry wrapper, or `skip`.
4. Prove: the loop now passes at the same count that failed before. If the cause is not found after two hypotheses, quarantine only with the user's approval and file the reason.

## 9. Report

Per test lane: command, exit code, tests ran / failed. Name the RED assertion you saw, whether the revert check was run, and anything untested.
