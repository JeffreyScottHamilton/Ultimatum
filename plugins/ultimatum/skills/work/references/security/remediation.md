# Remediating a vulnerability

Goal: close the hole at the boundary, prove the fix with a test that failed before it, find the same flaw on sibling paths, and keep the proof. Default: local only. Don't touch deployed systems, and don't rotate credentials yourself. Tell the user what to rotate.

## 1. Restate and locate

In one sentence: "<actor> can <action> via <entry point> because <missing or broken control> at `file:line`." If the report came from someone else, re-read the cited code first (`findings.md` §4, Q11). If the claim does not hold, say so with evidence instead of "fixing" it.

Record the baseline before changing anything: run the existing suite once (`ult run --name base -- <test cmd>`) and note the exit code and any tests already failing.

## 2. Reproduce first

Write the exploit as a test against local code or a local fixture, in the project's test framework:
- Act as the attacker exactly: user B's session with user A's id, no session, wrong role, a negative amount, `../../etc/passwd`, a URL to `127.0.0.1`, a body with an extra `role` field.
- Assert the **secure** outcome (403/404, zero rows, unchanged balance, rejected path), so the test fails now.
- Print a unique marker line just before the key assertion (`print("REPRO_F001_REACHED")`). An import error, a timeout, or a fixture crash then can't pass for a reproduction.
- Run it: `ult run --name repro -- <test cmd>`. Quote the failing assertion line and check that the marker appears (`ult log repro --grep REPRO_`).

If no safe local reproduction exists (it needs a deployed setting), say so. Write the test against the closest local seam, and keep the finding needs-validation for the deployment part.

## 3. Patch with the existing pattern

- Fix at the invariant, in the layer that owns the decision: scope the query by owner or tenant, call the project's existing authz helper or policy, bind parameters, use an argv list, resolve and contain the path, allowlist hosts, use an atomic conditional update, or add an idempotency key.
- Reuse what sibling handlers already do (`ult search`, `ult refs`). Copying the protected sibling's pattern is usually the right fix.
- Keep the change minimal. Don't rename, reformat, or refactor around it. Fail closed. Keep client errors generic.
- Secrets: move the value to configuration with no fallback (fail at startup), remove it from code, and tell the user to rotate it and purge history if it was ever committed.

## 4. Show it is fixed and nothing legitimate broke

1. The exploit test now passes, with the marker printed: quote the result.
2. The allowed path still works. Keep or add a test where the owner or right role succeeds with the correct data. A fix that denies everyone is not a fix.
3. Run the targeted tests, then the nearest wider suite. Compare with the baseline from §1. New failures are yours to explain.
4. Side-blind proof: the same test file, run unchanged on the vulnerable code and on the patched code, must fail first and pass second. Either stash the patch (`git stash push -- <patched files>`), run, then `git stash pop`, or temporarily revert the one guard line. The test must not know which version it is running against: no flags, and no skips keyed to the fix. Record both runs (command, exit code, key line). Then confirm `git diff` shows the patch intact.

## 5. Variant analysis

The same mistake usually exists more than once.
1. Write the exact pattern of the bug first, such as `Document.query.get(doc_id)` without an owner filter. A search that doesn't find the original bug means the pattern is wrong.
2. Widen one element at a time: other models, other methods on the same resource (PUT/PATCH/DELETE next to GET), list, bulk, and export endpoints, download and preview variants, v1/v2 or mobile routes, admin and user versions, background jobs, GraphQL resolvers, and webhook handlers.
3. For each hit: protected (cite the control), vulnerable (fix it the same way with its own negative test, or report it if it's outside the scope you were given), or unclear (needs-validation).
4. Stop when more than half the hits are noise. Record the searches you ran, including ones with no hits, under `variants` in the finding.

## 6. Keep the regression test

The exploit test stays in the suite, named for the rule it protects (`test_user_cannot_download_other_accounts_document`), not "test_fix_F001". Remove the marker print if the project's tests don't print. Update the finding:

```json
"fix_proof": {"status": "verified", "base_result": "<cmd> exit 1: <assert line>",
              "patched_result": "<cmd> exit 0", "allowed_path": "<test name> passed",
              "variant_checked": true, "suite_result": "<cmd> exit 0 (<n> tests)"},
"remediation": "<one line: what changed, file:line>"
```

Then run `ult findings validate`.

## 7. Report

Report the boundary restored, the files changed, and both proof runs (fails before, passes after) with commands and exit codes. Also give the allowed-path test, the variants checked and fixed, the suite result against baseline, and what is left for the user (rotate a secret, a deployment setting, an out-of-scope variant).
