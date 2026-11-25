import unittest
from datetime import date

from reports.dates import parse_report_date
from reports.summary import in_range
from schedule.dates import parse_due_date
from schedule.planner import days_until


class DateTests(unittest.TestCase):
    def test_due_formats(self):
        for text in ("2024-03-05", "05/03/2024", " 5  Mar 2024 "):
            self.assertEqual(parse_due_date(text), date(2024, 3, 5))

    def test_report_formats(self):
        for text in ("2024-03-05", "05/03/2024", "5 Mar 2024"):
            self.assertEqual(parse_report_date(text), date(2024, 3, 5))

    def test_errors_keep_their_wording(self):
        with self.assertRaisesRegex(ValueError, "due date"):
            parse_due_date("soon")
        with self.assertRaisesRegex(ValueError, "report date"):
            parse_report_date("soon")

    def test_users(self):
        self.assertEqual(days_until("2024-03-10", date(2024, 3, 5)), 5)
        self.assertTrue(in_range("2024-03-05", "01/03/2024", "31 Mar 2024"))


if __name__ == "__main__":
    unittest.main()
