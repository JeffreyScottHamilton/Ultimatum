import unittest

from pipeline.clean import strip_fields, drop_empty, normalize_keys, squash_spaces
from tests.noise import chatter


class CleanTests(unittest.TestCase):
    def setUp(self):
        chatter(self)

    def test_strip_fields_00(self):
        self.assertEqual(strip_fields({"a": " v0 "}), {"a": "v0"})

    def test_strip_fields_01(self):
        self.assertEqual(strip_fields({"a": " v1 "}), {"a": "v1"})

    def test_strip_fields_02(self):
        self.assertEqual(strip_fields({"a": " v2 "}), {"a": "v2"})

    def test_strip_fields_03(self):
        self.assertEqual(strip_fields({"a": " v3 "}), {"a": "v3"})

    def test_strip_fields_04(self):
        self.assertEqual(strip_fields({"a": " v4 "}), {"a": "v4"})

    def test_strip_fields_05(self):
        self.assertEqual(strip_fields({"a": " v5 "}), {"a": "v5"})

    def test_strip_fields_06(self):
        self.assertEqual(strip_fields({"a": " v6 "}), {"a": "v6"})

    def test_strip_fields_07(self):
        self.assertEqual(strip_fields({"a": " v7 "}), {"a": "v7"})

    def test_strip_fields_08(self):
        self.assertEqual(strip_fields({"a": " v8 "}), {"a": "v8"})

    def test_strip_fields_09(self):
        self.assertEqual(strip_fields({"a": " v9 "}), {"a": "v9"})

    def test_drop_empty_00(self):
        self.assertEqual(drop_empty({"a": "", "b": "x0"}), {"b": "x0"})

    def test_drop_empty_01(self):
        self.assertEqual(drop_empty({"a": "", "b": "x1"}), {"b": "x1"})

    def test_drop_empty_02(self):
        self.assertEqual(drop_empty({"a": "", "b": "x2"}), {"b": "x2"})

    def test_drop_empty_03(self):
        self.assertEqual(drop_empty({"a": "", "b": "x3"}), {"b": "x3"})

    def test_drop_empty_04(self):
        self.assertEqual(drop_empty({"a": "", "b": "x4"}), {"b": "x4"})

    def test_drop_empty_05(self):
        self.assertEqual(drop_empty({"a": "", "b": "x5"}), {"b": "x5"})

    def test_drop_empty_06(self):
        self.assertEqual(drop_empty({"a": "", "b": "x6"}), {"b": "x6"})

    def test_drop_empty_07(self):
        self.assertEqual(drop_empty({"a": "", "b": "x7"}), {"b": "x7"})

    def test_drop_empty_08(self):
        self.assertEqual(drop_empty({"a": "", "b": "x8"}), {"b": "x8"})

    def test_drop_empty_09(self):
        self.assertEqual(drop_empty({"a": "", "b": "x9"}), {"b": "x9"})

    def test_normalize_keys_00(self):
        self.assertEqual(normalize_keys({" Key 0 ": 1}), {"key_0": 1})

    def test_normalize_keys_01(self):
        self.assertEqual(normalize_keys({" Key 1 ": 1}), {"key_1": 1})

    def test_normalize_keys_02(self):
        self.assertEqual(normalize_keys({" Key 2 ": 1}), {"key_2": 1})

    def test_normalize_keys_03(self):
        self.assertEqual(normalize_keys({" Key 3 ": 1}), {"key_3": 1})

    def test_normalize_keys_04(self):
        self.assertEqual(normalize_keys({" Key 4 ": 1}), {"key_4": 1})

    def test_normalize_keys_05(self):
        self.assertEqual(normalize_keys({" Key 5 ": 1}), {"key_5": 1})

    def test_normalize_keys_06(self):
        self.assertEqual(normalize_keys({" Key 6 ": 1}), {"key_6": 1})

    def test_normalize_keys_07(self):
        self.assertEqual(normalize_keys({" Key 7 ": 1}), {"key_7": 1})

    def test_normalize_keys_08(self):
        self.assertEqual(normalize_keys({" Key 8 ": 1}), {"key_8": 1})

    def test_normalize_keys_09(self):
        self.assertEqual(normalize_keys({" Key 9 ": 1}), {"key_9": 1})

    def test_squash_spaces(self):
        self.assertEqual(squash_spaces("a   b  c"), "a b c")
