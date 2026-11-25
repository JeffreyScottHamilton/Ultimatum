# billing

Minimal invoicing service. Stores customers and invoices in memory (seeded
from `billing/seed.py`), computes outstanding balances, and exposes a small CLI.

    python3 -m billing.cli list
    python3 -m billing.cli report

Layout: `models.py` (dataclasses), `money.py` (cents arithmetic and display),
`invoices.py` (queries), `reports.py` (aggregate reports), `cli.py`.

Run tests: `python3 -m unittest`
