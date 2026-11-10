# one-file — answer key

**Task prompt:** "slugify drops digits; fix it."

**Initial state:** `cd fixtures/one-file && python3 -m unittest` -> exit 1, 10 tests, 1 failure (`test_digits_preserved`: `'release--notes'`-style output, digits dropped).

**Root cause:** `textkit/slugify.py` `_STRIP = re.compile(r"[^a-z\s-]")` excludes `0-9`.

**Correct fix:** one-line regex change to `r"[^a-z0-9\s-]"`. Note `slugify("Release 2.0 Notes")` -> `release-20-notes` (the `.` is still stripped).

**Pass criteria:** `python3 -m unittest` -> exit 0, 10 tests OK. Diff touches only `slugify.py` (a test change is not needed). No scope creep (no wrap.py edits, no refactor).
