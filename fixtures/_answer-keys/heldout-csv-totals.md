# heldout-csv-totals (h1)
Prompt: "The totals in our CSV report are off by one cent for some rows. Can you find out why and fix it?"
Root cause: `billing/totals.py` computes in binary floats; rows like 1.15 x1 at 10% give 126.4999... instead of 127. Fix: Decimal with ROUND_HALF_UP.
Hidden check: `heldout-csv-totals_check.py` (2000 generated rows vs exact Decimal math; ties round half up as the README states (all the float mismatches are exact half-cent ties)).
