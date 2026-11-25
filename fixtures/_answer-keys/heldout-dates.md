# heldout-dates (h6)
Prompt: "schedule/dates.py and reports/dates.py have near-identical date parsing code. Deduplicate it without changing behaviour."
Both public functions keep their names and their distinct error wording. Check: `heldout-dates_check.py` (+ `.expected.json` recorded from the untouched fixture); exactly one strptime call remains in non-test sources.
