# Checkable goals: a check that fails now and passes when done

Read when a request has no test yet, when you are about to write "should work" in a report, or when you are looping on a fix without knowing what done looks like.

A goal you can check lets you work without asking "is this right?" after every step. A goal you cannot check ("make it better", "clean this up") turns into guessing. Test-first mechanics are in `../../tdd.md`; this file is about choosing the check.

## 1. Turn the request into a check

| Request | Check that fails now and passes when done |
|---|---|
| Fix the crash on empty carts | a test that calls checkout with an empty cart and expects the error message, not the crash |
| Add validation to the sign-up form | tests for each bad input (empty, too long, wrong format) expecting the field error, and one good input passing |
| Make the report faster | a timing on the real-size fixture: now 9.2 s, target under 2 s, same output |
| Refactor the parser | the existing tests pass before and after; add tests first where the parser has none |
| Upgrade the library | build, type check and full suite pass on the new version; changelog breaking changes listed and handled |

If you cannot write the check, the request is not clear yet: go back to `think-first.md` § 2. The two-readings test.

## 2. Watch it fail first

Run the new check before the fix. A check that already passes proves nothing: it may be testing the wrong thing, or the bug may be somewhere else. Record the failing output in one line.

## 3. Plans as step and check

For work with more than two steps, write each step with the check that ends it:

```text
1. Add the `discount_code` column  -> migration runs up and down on a copy; schema test passes
2. Apply the code at checkout       -> new test: valid code lowers the total; expired code is refused
3. Show it on the receipt          -> receipt snapshot test updated; one manual check in the browser
```

A step is done when its check passes, not when the code is written. Run the wider suite after the last step.

## 4. When to stop looping

- The check passes and the wider suite is green: stop and report.
- The same check has failed three times with three different fixes: stop guessing. Re-read the failure, form one hypothesis, and test it alone (`../../debugging.md`).
- The check turns out to be wrong (it tests the wrong thing): say so, fix the check first, and note the change in the report.

## 5. Report with the evidence

Name each check, the command, and its result: "`pytest tests/test_checkout.py` 14 passed; full suite 512 passed, exit 0." Never "should work" without the run behind it.
