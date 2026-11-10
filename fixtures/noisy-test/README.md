# pipeline

A small CSV-ish data pipeline: parse raw string fields, clean records,
transform them into a normalized shape, and validate the result.

    from pipeline.parse import parse_amount, parse_date
    parse_amount("$1,234.56")   # 1234.56

Modules: `parse.py`, `clean.py`, `transform.py`, `validate.py`, `logutil.py`.

Run tests: `python3 -m unittest` (use `-v` for per-test names). The suite is
chatty: pipeline stages log progress and a few legacy helpers emit
DeprecationWarnings.
