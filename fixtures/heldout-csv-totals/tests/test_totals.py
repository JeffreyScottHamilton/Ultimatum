import unittest

from billing.money import fmt_cents
from billing.totals import invoice_total_cents, line_total_cents


class TotalsTests(unittest.TestCase):
    def test_no_tax(self):
        self.assertEqual(line_total_cents("10.00", 2, "0"), 2000)

    def test_simple_tax(self):
        self.assertEqual(line_total_cents("20.00", 1, "10"), 2200)

    def test_rounding_down(self):
        self.assertEqual(line_total_cents("19.99", 1, "10"), 2199)

    def test_invoice(self):
        rows = [{"unit_price": "1.00", "qty": "3", "tax_pct": "0"},
                {"unit_price": "2.50", "qty": "2", "tax_pct": "20"}]
        self.assertEqual(invoice_total_cents(rows), 900)

    def test_fmt(self):
        self.assertEqual(fmt_cents(5), "0.05")
        self.assertEqual(fmt_cents(-1234), "-12.34")


if __name__ == "__main__":
    unittest.main()
