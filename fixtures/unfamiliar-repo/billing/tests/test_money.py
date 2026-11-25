import unittest
from billing.money import format_money, round_half_even


class MoneyTests(unittest.TestCase):
    def test_usd(self):
        self.assertEqual(format_money(123456, "USD"), "$1,234.56")

    def test_negative(self):
        self.assertEqual(format_money(-5, "USD"), "-$0.05")

    def test_eur(self):
        self.assertEqual(format_money(100, "EUR"), "€1.00")

    def test_jpy(self):
        self.assertEqual(format_money(1500, "JPY"), "¥1,500")

    def test_half_even(self):
        self.assertEqual(round_half_even(5, 2), 2)
        self.assertEqual(round_half_even(7, 2), 4)
        self.assertEqual(round_half_even(8, 3), 3)
