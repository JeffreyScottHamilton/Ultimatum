"""Read a CSV file and render the report."""
import csv

from .money import fmt_cents
from .totals import invoice_total_cents, line_total_cents


def read_rows(path):
    with open(path, newline="") as fh:
        return [row for row in csv.DictReader(fh) if row.get("sku")]


def render(rows) -> str:
    lines = []
    for r in rows:
        total = line_total_cents(r["unit_price"], r["qty"], r["tax_pct"])
        lines.append(f"{r['sku']},{fmt_cents(total)}")
    lines.append(f"TOTAL,{fmt_cents(invoice_total_cents(rows))}")
    return "\n".join(lines)
