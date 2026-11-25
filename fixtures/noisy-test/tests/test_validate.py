import unittest

from pipeline.validate import require, positive_amount, in_range
from tests.noise import chatter


class ValidateTests(unittest.TestCase):
    def setUp(self):
        chatter(self)

    def test_require_ok_00(self):
        self.assertEqual(require({"a": 0, "b": 1}, "a", "b"), {"a": 0, "b": 1})

    def test_require_ok_01(self):
        self.assertEqual(require({"a": 1, "b": 1}, "a", "b"), {"a": 1, "b": 1})

    def test_require_ok_02(self):
        self.assertEqual(require({"a": 2, "b": 1}, "a", "b"), {"a": 2, "b": 1})

    def test_require_ok_03(self):
        self.assertEqual(require({"a": 3, "b": 1}, "a", "b"), {"a": 3, "b": 1})

    def test_require_ok_04(self):
        self.assertEqual(require({"a": 4, "b": 1}, "a", "b"), {"a": 4, "b": 1})

    def test_require_ok_05(self):
        self.assertEqual(require({"a": 5, "b": 1}, "a", "b"), {"a": 5, "b": 1})

    def test_require_ok_06(self):
        self.assertEqual(require({"a": 6, "b": 1}, "a", "b"), {"a": 6, "b": 1})

    def test_require_ok_07(self):
        self.assertEqual(require({"a": 7, "b": 1}, "a", "b"), {"a": 7, "b": 1})

    def test_require_ok_08(self):
        self.assertEqual(require({"a": 8, "b": 1}, "a", "b"), {"a": 8, "b": 1})

    def test_require_ok_09(self):
        self.assertEqual(require({"a": 9, "b": 1}, "a", "b"), {"a": 9, "b": 1})

    def test_require_ok_10(self):
        self.assertEqual(require({"a": 10, "b": 1}, "a", "b"), {"a": 10, "b": 1})

    def test_require_ok_11(self):
        self.assertEqual(require({"a": 11, "b": 1}, "a", "b"), {"a": 11, "b": 1})

    def test_require_missing_00(self):
        with self.assertRaises(ValueError):
            require({"a": 0}, "a", "zz")

    def test_require_missing_01(self):
        with self.assertRaises(ValueError):
            require({"a": 1}, "a", "zz")

    def test_require_missing_02(self):
        with self.assertRaises(ValueError):
            require({"a": 2}, "a", "zz")

    def test_require_missing_03(self):
        with self.assertRaises(ValueError):
            require({"a": 3}, "a", "zz")

    def test_require_missing_04(self):
        with self.assertRaises(ValueError):
            require({"a": 4}, "a", "zz")

    def test_require_missing_05(self):
        with self.assertRaises(ValueError):
            require({"a": 5}, "a", "zz")

    def test_require_missing_06(self):
        with self.assertRaises(ValueError):
            require({"a": 6}, "a", "zz")

    def test_require_missing_07(self):
        with self.assertRaises(ValueError):
            require({"a": 7}, "a", "zz")

    def test_require_missing_08(self):
        with self.assertRaises(ValueError):
            require({"a": 8}, "a", "zz")

    def test_require_missing_09(self):
        with self.assertRaises(ValueError):
            require({"a": 9}, "a", "zz")

    def test_require_missing_10(self):
        with self.assertRaises(ValueError):
            require({"a": 10}, "a", "zz")

    def test_positive_amount_00(self):
        self.assertEqual(positive_amount({"amount": 1})["amount"], 1)

    def test_positive_amount_01(self):
        self.assertEqual(positive_amount({"amount": 2})["amount"], 2)

    def test_positive_amount_02(self):
        self.assertEqual(positive_amount({"amount": 3})["amount"], 3)

    def test_positive_amount_03(self):
        self.assertEqual(positive_amount({"amount": 4})["amount"], 4)

    def test_positive_amount_04(self):
        self.assertEqual(positive_amount({"amount": 5})["amount"], 5)

    def test_positive_amount_05(self):
        self.assertEqual(positive_amount({"amount": 6})["amount"], 6)

    def test_in_range_00(self):
        self.assertTrue(in_range(0, 0, 10))
        self.assertFalse(in_range(20, 0, 10))

    def test_in_range_01(self):
        self.assertTrue(in_range(1, 0, 10))
        self.assertFalse(in_range(21, 0, 10))

    def test_in_range_02(self):
        self.assertTrue(in_range(2, 0, 10))
        self.assertFalse(in_range(22, 0, 10))

    def test_in_range_03(self):
        self.assertTrue(in_range(3, 0, 10))
        self.assertFalse(in_range(23, 0, 10))

    def test_in_range_04(self):
        self.assertTrue(in_range(4, 0, 10))
        self.assertFalse(in_range(24, 0, 10))

    def test_in_range_05(self):
        self.assertTrue(in_range(5, 0, 10))
        self.assertFalse(in_range(25, 0, 10))
