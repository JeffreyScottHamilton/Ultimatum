# noisy-test — answer key

**Task prompt:** "Run the test suite and report which test(s) fail and why."

**Command / result:** `cd fixtures/noisy-test && python3 -m unittest -v > out.txt 2>&1; echo $?` -> exit 1. 151 tests, exactly 1 failure, ~2360 lines of output (stdout log lines + 150+ DeprecationWarning lines on stderr). The failing test is mid-run (about line 1009 of 2363).

**Key failure (must be reported):**
- Test: `test_parse_european_decimal` (`tests.test_parse.ParseTests`)
- Assertion string: `AssertionError: 1234.5 != 1234.56`
- Location: `tests/test_parse.py` line 85, `parse_amount("1.234,56")`.

**Root cause:** `pipeline/parse.py` `parse_amount`, European branch: `s = whole + "." + frac[:1]` truncates the decimal part to one digit. Fix: `s = whole + "." + frac`. Single-decimal European tests (`"1.000,5"`) pass, which hides the bug.

**Grading:** report must name the single failing test and the exact assertion, not be derailed by DeprecationWarnings/log lines (not failures), and not claim multiple failures. Ideal agent filters output (grep/tail) instead of dumping the whole thing. After fix: exit 0, 151 tests OK.
