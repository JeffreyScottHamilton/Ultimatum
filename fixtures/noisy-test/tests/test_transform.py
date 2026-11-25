import unittest

from pipeline.transform import to_record, total, group_by
from tests.noise import chatter


class TransformTests(unittest.TestCase):
    def setUp(self):
        chatter(self)

    def test_to_record_00(self):
        r = to_record({" Amount ": "1.50", "Qty": "1", "Note": ""})
        self.assertEqual(r, {"amount": 1.5, "qty": 1})

    def test_to_record_01(self):
        r = to_record({" Amount ": "2.50", "Qty": "2", "Note": ""})
        self.assertEqual(r, {"amount": 2.5, "qty": 2})

    def test_to_record_02(self):
        r = to_record({" Amount ": "3.50", "Qty": "3", "Note": ""})
        self.assertEqual(r, {"amount": 3.5, "qty": 3})

    def test_to_record_03(self):
        r = to_record({" Amount ": "4.50", "Qty": "4", "Note": ""})
        self.assertEqual(r, {"amount": 4.5, "qty": 4})

    def test_to_record_04(self):
        r = to_record({" Amount ": "5.50", "Qty": "5", "Note": ""})
        self.assertEqual(r, {"amount": 5.5, "qty": 5})

    def test_to_record_05(self):
        r = to_record({" Amount ": "6.50", "Qty": "6", "Note": ""})
        self.assertEqual(r, {"amount": 6.5, "qty": 6})

    def test_to_record_06(self):
        r = to_record({" Amount ": "7.50", "Qty": "7", "Note": ""})
        self.assertEqual(r, {"amount": 7.5, "qty": 7})

    def test_to_record_07(self):
        r = to_record({" Amount ": "8.50", "Qty": "8", "Note": ""})
        self.assertEqual(r, {"amount": 8.5, "qty": 8})

    def test_to_record_08(self):
        r = to_record({" Amount ": "9.50", "Qty": "9", "Note": ""})
        self.assertEqual(r, {"amount": 9.5, "qty": 9})

    def test_to_record_09(self):
        r = to_record({" Amount ": "10.50", "Qty": "10", "Note": ""})
        self.assertEqual(r, {"amount": 10.5, "qty": 10})

    def test_to_record_10(self):
        r = to_record({" Amount ": "11.50", "Qty": "11", "Note": ""})
        self.assertEqual(r, {"amount": 11.5, "qty": 11})

    def test_to_record_11(self):
        r = to_record({" Amount ": "12.50", "Qty": "12", "Note": ""})
        self.assertEqual(r, {"amount": 12.5, "qty": 12})

    def test_to_record_12(self):
        r = to_record({" Amount ": "13.50", "Qty": "13", "Note": ""})
        self.assertEqual(r, {"amount": 13.5, "qty": 13})

    def test_to_record_13(self):
        r = to_record({" Amount ": "14.50", "Qty": "14", "Note": ""})
        self.assertEqual(r, {"amount": 14.5, "qty": 14})

    def test_to_record_14(self):
        r = to_record({" Amount ": "15.50", "Qty": "15", "Note": ""})
        self.assertEqual(r, {"amount": 15.5, "qty": 15})

    def test_total_00(self):
        recs = [{"amount": 2.5, "qty": 1}, {"amount": 1.0}]
        self.assertEqual(total(recs), 3.5)

    def test_total_01(self):
        recs = [{"amount": 2.5, "qty": 2}, {"amount": 1.0}]
        self.assertEqual(total(recs), 6.0)

    def test_total_02(self):
        recs = [{"amount": 2.5, "qty": 3}, {"amount": 1.0}]
        self.assertEqual(total(recs), 8.5)

    def test_total_03(self):
        recs = [{"amount": 2.5, "qty": 4}, {"amount": 1.0}]
        self.assertEqual(total(recs), 11.0)

    def test_total_04(self):
        recs = [{"amount": 2.5, "qty": 5}, {"amount": 1.0}]
        self.assertEqual(total(recs), 13.5)

    def test_total_05(self):
        recs = [{"amount": 2.5, "qty": 6}, {"amount": 1.0}]
        self.assertEqual(total(recs), 16.0)

    def test_total_06(self):
        recs = [{"amount": 2.5, "qty": 7}, {"amount": 1.0}]
        self.assertEqual(total(recs), 18.5)

    def test_total_07(self):
        recs = [{"amount": 2.5, "qty": 8}, {"amount": 1.0}]
        self.assertEqual(total(recs), 21.0)

    def test_total_08(self):
        recs = [{"amount": 2.5, "qty": 9}, {"amount": 1.0}]
        self.assertEqual(total(recs), 23.5)

    def test_total_09(self):
        recs = [{"amount": 2.5, "qty": 10}, {"amount": 1.0}]
        self.assertEqual(total(recs), 26.0)

    def test_total_10(self):
        recs = [{"amount": 2.5, "qty": 11}, {"amount": 1.0}]
        self.assertEqual(total(recs), 28.5)

    def test_total_11(self):
        recs = [{"amount": 2.5, "qty": 12}, {"amount": 1.0}]
        self.assertEqual(total(recs), 31.0)

    def test_total_12(self):
        recs = [{"amount": 2.5, "qty": 13}, {"amount": 1.0}]
        self.assertEqual(total(recs), 33.5)

    def test_total_13(self):
        recs = [{"amount": 2.5, "qty": 14}, {"amount": 1.0}]
        self.assertEqual(total(recs), 36.0)

    def test_total_14(self):
        recs = [{"amount": 2.5, "qty": 15}, {"amount": 1.0}]
        self.assertEqual(total(recs), 38.5)

    def test_group_by_00(self):
        g = group_by([{"k": "a"}, {"k": "b"}, {"k": "a"}], "k")
        self.assertEqual(len(g["a"]), 2)
        self.assertEqual(len(g["b"]), 1)

    def test_group_by_01(self):
        g = group_by([{"k": "a"}, {"k": "b"}, {"k": "a"}], "k")
        self.assertEqual(len(g["a"]), 2)
        self.assertEqual(len(g["b"]), 1)

    def test_group_by_02(self):
        g = group_by([{"k": "a"}, {"k": "b"}, {"k": "a"}], "k")
        self.assertEqual(len(g["a"]), 2)
        self.assertEqual(len(g["b"]), 1)

    def test_group_by_03(self):
        g = group_by([{"k": "a"}, {"k": "b"}, {"k": "a"}], "k")
        self.assertEqual(len(g["a"]), 2)
        self.assertEqual(len(g["b"]), 1)

    def test_group_by_04(self):
        g = group_by([{"k": "a"}, {"k": "b"}, {"k": "a"}], "k")
        self.assertEqual(len(g["a"]), 2)
        self.assertEqual(len(g["b"]), 1)

    def test_group_by_05(self):
        g = group_by([{"k": "a"}, {"k": "b"}, {"k": "a"}], "k")
        self.assertEqual(len(g["a"]), 2)
        self.assertEqual(len(g["b"]), 1)

    def test_group_by_06(self):
        g = group_by([{"k": "a"}, {"k": "b"}, {"k": "a"}], "k")
        self.assertEqual(len(g["a"]), 2)
        self.assertEqual(len(g["b"]), 1)

    def test_group_by_07(self):
        g = group_by([{"k": "a"}, {"k": "b"}, {"k": "a"}], "k")
        self.assertEqual(len(g["a"]), 2)
        self.assertEqual(len(g["b"]), 1)

    def test_group_by_08(self):
        g = group_by([{"k": "a"}, {"k": "b"}, {"k": "a"}], "k")
        self.assertEqual(len(g["a"]), 2)
        self.assertEqual(len(g["b"]), 1)

    def test_group_by_09(self):
        g = group_by([{"k": "a"}, {"k": "b"}, {"k": "a"}], "k")
        self.assertEqual(len(g["a"]), 2)
        self.assertEqual(len(g["b"]), 1)
