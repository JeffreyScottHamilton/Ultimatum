# unfamiliar-repo — answer key

**Task prompt:** "Add a `summary` CLI subcommand that prints each customer's outstanding total formatted as money."

**Initial state:** `cd fixtures/unfamiliar-repo && python3 -m unittest` -> exit 0, 9 tests OK.

**Correct solution:**
- `billing/cli.py`: add `summary` subparser; for each customer print name and `format_money(invoices.outstanding_for(ledger, c), c.currency)` using `billing.money.format_money` and `billing.invoices.outstanding_for(ledger, customer)`.
- Expected output for the seed ledger (one line per customer, exact layout flexible):
  - Acme Corp: `$1,999.50`
  - Globex GmbH: `€49.99`
  - Initech: `$0.00`
- Add a test (e.g. in `billing/tests/test_cli.py`) for the subcommand.

**FAIL conditions (any):**
- Reimplements currency formatting (f-strings with `/100`, `"%d.%02d"`, etc.) instead of calling `format_money`.
- Imports or copies from `legacy/old_money.py` (deprecated decoy with buggy `fmt`: floors, no separators).
- Recomputes outstanding totals by hand instead of `invoices.outstanding_for`.
- Ignores customer currency (prints EUR customer in `$`).

**Pass:** `python3 -m unittest` exit 0; `python3 -m billing.cli summary` exits 0 with the amounts above.
