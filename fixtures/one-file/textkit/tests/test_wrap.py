import unittest
from textkit import wrap


class WrapTests(unittest.TestCase):
    def test_wraps(self):
        self.assertEqual(wrap("aaa bbb ccc", 7), ["aaa bbb", "ccc"])

    def test_long_word(self):
        self.assertEqual(wrap("supercalifragilistic a", 5), ["supercalifragilistic", "a"])

    def test_empty(self):
        self.assertEqual(wrap(""), [])

    def test_bad_width(self):
        with self.assertRaises(ValueError):
            wrap("x", 0)
