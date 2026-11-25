import unittest

from inventory.pricing import bulk_price


class PricingTests(unittest.TestCase):
    def test_tiers(self):
        for qty in range(1, 400):
            with self.subTest(qty=qty):
                full = 250 * qty
                expect = full if qty < 20 else full * 95 // 100 if qty < 100 else full * 90 // 100
                self.assertEqual(bulk_price(250, qty), expect)


if __name__ == "__main__":
    unittest.main()
