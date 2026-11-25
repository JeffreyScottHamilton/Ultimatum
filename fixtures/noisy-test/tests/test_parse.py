import unittest

from datetime import date
from pipeline.parse import parse_amount, parse_int, parse_date, parse_bool
from tests.noise import chatter


class ParseTests(unittest.TestCase):
    def setUp(self):
        chatter(self)

    def test_parse_amount_00(self):
        self.assertEqual(parse_amount('$1,234.56'), 1234.56)

    def test_parse_amount_01(self):
        self.assertEqual(parse_amount('1234.56'), 1234.56)

    def test_parse_amount_02(self):
        self.assertEqual(parse_amount('-12'), -12.0)

    def test_parse_amount_03(self):
        self.assertEqual(parse_amount('(5.50)'), -5.5)

    def test_parse_amount_04(self):
        self.assertEqual(parse_amount('€ 10'), 10.0)

    def test_parse_amount_05(self):
        self.assertEqual(parse_amount('0.99'), 0.99)

    def test_parse_amount_06(self):
        self.assertEqual(parse_amount('1,000.00'), 1000.0)

    def test_parse_amount_07(self):
        self.assertEqual(parse_amount('$0'), 0.0)

    def test_parse_amount_plain_00(self):
        self.assertEqual(parse_amount("1.25"), 1.25)

    def test_parse_amount_plain_01(self):
        self.assertEqual(parse_amount("8.25"), 8.25)

    def test_parse_amount_plain_02(self):
        self.assertEqual(parse_amount("15.25"), 15.25)

    def test_parse_amount_plain_03(self):
        self.assertEqual(parse_amount("22.25"), 22.25)

    def test_parse_amount_plain_04(self):
        self.assertEqual(parse_amount("29.25"), 29.25)

    def test_parse_amount_plain_05(self):
        self.assertEqual(parse_amount("36.25"), 36.25)

    def test_parse_amount_plain_06(self):
        self.assertEqual(parse_amount("43.25"), 43.25)

    def test_parse_amount_plain_07(self):
        self.assertEqual(parse_amount("50.25"), 50.25)

    def test_parse_amount_european_single_00(self):
        self.assertEqual(parse_amount("1.000,5"), 1000.5)

    def test_parse_amount_european_single_01(self):
        self.assertEqual(parse_amount("2.000,5"), 2000.5)

    def test_parse_amount_european_single_02(self):
        self.assertEqual(parse_amount("3.000,5"), 3000.5)

    def test_parse_amount_european_single_03(self):
        self.assertEqual(parse_amount("4.000,5"), 4000.5)

    def test_parse_amount_european_single_04(self):
        self.assertEqual(parse_amount("5.000,5"), 5000.5)

    def test_parse_amount_european_single_05(self):
        self.assertEqual(parse_amount("6.000,5"), 6000.5)

    def test_parse_amount_european_single_06(self):
        self.assertEqual(parse_amount("7.000,5"), 7000.5)

    def test_parse_amount_european_single_07(self):
        self.assertEqual(parse_amount("8.000,5"), 8000.5)

    def test_parse_european_decimal(self):
        self.assertEqual(parse_amount("1.234,56"), 1234.56)

    def test_parse_int_00(self):
        self.assertEqual(parse_int("0_000"), 0)

    def test_parse_int_01(self):
        self.assertEqual(parse_int("1_000"), 1000)

    def test_parse_int_02(self):
        self.assertEqual(parse_int("2_000"), 2000)

    def test_parse_int_03(self):
        self.assertEqual(parse_int("3_000"), 3000)

    def test_parse_int_04(self):
        self.assertEqual(parse_int("4_000"), 4000)

    def test_parse_int_05(self):
        self.assertEqual(parse_int("5_000"), 5000)

    def test_parse_int_06(self):
        self.assertEqual(parse_int("6_000"), 6000)

    def test_parse_int_07(self):
        self.assertEqual(parse_int("7_000"), 7000)

    def test_parse_date_iso_00(self):
        self.assertEqual(parse_date("2024-01-10"), date(2024, 1, 10))

    def test_parse_date_iso_01(self):
        self.assertEqual(parse_date("2024-02-11"), date(2024, 2, 11))

    def test_parse_date_iso_02(self):
        self.assertEqual(parse_date("2024-03-12"), date(2024, 3, 12))

    def test_parse_date_iso_03(self):
        self.assertEqual(parse_date("2024-04-13"), date(2024, 4, 13))

    def test_parse_date_iso_04(self):
        self.assertEqual(parse_date("2024-05-14"), date(2024, 5, 14))

    def test_parse_date_iso_05(self):
        self.assertEqual(parse_date("2024-06-15"), date(2024, 6, 15))

    def test_parse_date_dmy_00(self):
        self.assertEqual(parse_date("01/02/2023"), date(2023, 2, 1))

    def test_parse_date_dmy_01(self):
        self.assertEqual(parse_date("02/02/2023"), date(2023, 2, 2))

    def test_parse_date_dmy_02(self):
        self.assertEqual(parse_date("03/02/2023"), date(2023, 2, 3))

    def test_parse_date_dmy_03(self):
        self.assertEqual(parse_date("04/02/2023"), date(2023, 2, 4))

    def test_parse_date_bad(self):
        with self.assertRaises(ValueError):
            parse_date("yesterday")

    def test_parse_bool(self):
        self.assertTrue(parse_bool("Yes"))
        self.assertFalse(parse_bool("no"))
