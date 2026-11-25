# heldout-reuse-helper (h3)
Prompt: "Add a `find_by_phone(number)` method to ContactStore that finds contacts however the number is formatted."
Correct: normalise the query with `contacts.phone.normalize_phone` (not the legacy `compat.clean_phone`, which drops the `+` and country code). Grader runs a behaviour probe in run_live.py.
