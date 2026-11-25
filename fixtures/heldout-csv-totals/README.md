# billing

Small CSV invoice report. `python3 -m billing data.csv` prints one line per row and a grand total.

Input columns: `sku,unit_price,qty,tax_pct`. Run tests with `python3 -m unittest`.

Amounts are rounded half up to the cent.
