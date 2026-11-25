from . import invoices
from .money import format_money, round_half_even


def aging_rows(ledger):
    """(customer name, invoice count, outstanding cents) per customer."""
    return [
        (c.name, len(invoices.for_customer(ledger, c)), invoices.outstanding_for(ledger, c))
        for c in ledger.customers
    ]


def average_invoice_cents(ledger):
    if not ledger.invoices:
        return 0
    return round_half_even(sum(i.amount_cents for i in ledger.invoices), len(ledger.invoices))


def render_report(ledger):
    lines = ["Customer | Invoices | Outstanding"]
    for c in ledger.customers:
        n = len(invoices.for_customer(ledger, c))
        lines.append(f"{c.name} | {n} | {format_money(invoices.outstanding_for(ledger, c), c.currency)}")
    return "\n".join(lines)
