"""Invoice queries over a Ledger."""


def for_customer(ledger, customer):
    return [i for i in ledger.invoices if i.customer_id == customer.id]


def outstanding_for(ledger, customer):
    """Total outstanding cents across all of a customer's invoices."""
    return sum(i.outstanding_cents for i in for_customer(ledger, customer))
