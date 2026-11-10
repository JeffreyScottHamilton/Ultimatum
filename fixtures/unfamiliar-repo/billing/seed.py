from .models import Customer, Invoice, Ledger


def sample_ledger():
    return Ledger(
        customers=[
            Customer("c1", "Acme Corp"),
            Customer("c2", "Globex GmbH", "EUR"),
            Customer("c3", "Initech"),
        ],
        invoices=[
            Invoice("i1", "c1", 125000, 25000),
            Invoice("i2", "c1", 99950),
            Invoice("i3", "c2", 250000, 250000, "EUR"),
            Invoice("i4", "c2", 4999, 0, "EUR"),
            Invoice("i5", "c3", 100, 100),
        ],
    )
