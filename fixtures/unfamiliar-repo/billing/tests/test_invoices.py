import unittest
from billing import invoices, reports
from billing.seed import sample_ledger


class InvoiceTests(unittest.TestCase):
    def setUp(self):
        self.ledger = sample_ledger()
        self.c = {c.id: c for c in self.ledger.customers}

    def test_outstanding(self):
        self.assertEqual(invoices.outstanding_for(self.ledger, self.c["c1"]), 199950)
        self.assertEqual(invoices.outstanding_for(self.ledger, self.c["c2"]), 4999)
        self.assertEqual(invoices.outstanding_for(self.ledger, self.c["c3"]), 0)

    def test_report(self):
        self.assertIn("Acme Corp | 2 | $1,999.50", reports.render_report(self.ledger))

    def test_average(self):
        self.assertEqual(reports.average_invoice_cents(self.ledger), 96010)
