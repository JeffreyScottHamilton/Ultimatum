# What each "done" claim needs behind it

Read when you are about to tell the user something works, passes, is fixed or is finished, or to accept a helper's report that says so. The rule itself (no claim without a check run this session) is the router's rule 2 and tdd (`../../tdd.md` § 3); this file says which check each kind of claim needs.

## The table

| You want to say | You need, from this session | Not enough |
|---|---|---|
| Tests pass | the full suite command, its exit code 0, and the count (`Ran 42 tests ... OK`) | an earlier run, a subset, "should pass" |
| Lint is clean | the linter's own output with exit code 0 | a passing build; the build does not lint |
| It builds | the build command with exit code 0 | lint passing; a successful install |
| The bug is fixed | the original reproduction now passes | the code changed; a neighbouring test passes |
| A regression test guards it | red-green-revert: fails with the fix reverted, passes with it (`../../tdd.md` § 5) | a test that passed the first time it ran |
| A helper finished its part | its check re-run by you, and its diff read | the helper's report |
| The requirements are met | each requirement ticked against a test or an observed behaviour | "the tests pass" |
| It is secure | the negative test from the security overlay, failing without the guard | "I added validation" |

## Words that mean you have not checked

If a sentence you are about to send contains one of these, run the check first or rewrite the sentence as what it is, a guess:

- "should work", "should pass", "probably fixed";
- "seems to", "looks right", "I believe";
- "Done!" or "All set" before the last command has run;
- "just a small change, no need to test".

## How to say it

Quote the command and the result in the same breath as the claim:

> Fixed: `python3 -m unittest tests.test_row` ran 9 tests, exit 0. The case from the issue (quoted comma in the last column) is `test_quoted_last_column`, which fails with the fix reverted.

When you could not check something, say that instead, and why:

> Not verified on Windows: no Windows runner here. The path join uses `pathlib`, which handles separators, but nothing ran.

## Helpers' reports

A helper that says "all tests pass" may have run a subset, run nothing, or misread output. Before you pass its claim on:

1. Run its check command yourself.
2. Read `git diff` for the files it owned, and check nothing outside them changed.
3. If its report and your run disagree, yours wins; send the difference back (`../../orchestration.md` § 6).
