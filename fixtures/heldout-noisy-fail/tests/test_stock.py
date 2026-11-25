import unittest

from inventory.stock import apply_events, reorder_qty


class StockTests(unittest.TestCase):
    def test_apply_many_events(self):
        events = [("in", 3), ("out", 2)] * 400
        self.assertEqual(apply_events(10, events), 410)

    def test_never_negative(self):
        self.assertEqual(apply_events(1, [("out", 5)] * 300), 0)

    def test_reorder_nothing_needed(self):
        self.assertEqual(reorder_qty(50, 40, 6), 0)

    def test_reorder_exact_packs(self):
        for need in range(6, 600, 6):
            with self.subTest(need=need):
                self.assertEqual(reorder_qty(0, need, 6), need)

    def test_reorder_rounds_up_to_whole_pack(self):
        for need in range(1, 200):
            with self.subTest(need=need):
                got = reorder_qty(0, need, 12)
                self.assertEqual(got % 12, 0)
                self.assertGreaterEqual(got, need)


if __name__ == "__main__":
    unittest.main()
