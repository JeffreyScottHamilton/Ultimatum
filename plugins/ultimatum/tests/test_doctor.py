import unittest

from _harness import UltCase


class TestDoctor(UltCase):
    def test_doctor_runs_and_changes_nothing(self):
        r = self.ult("doctor")
        self.assertEqual(r.code, 0, r.all)
        self.assertIn("git", r.out)
        self.assertFalse((self.root / "index.db").exists())

    def test_help_and_bad_cmd(self):
        self.assertEqual(self.ult("--help").code, 0)
        self.assertNotEqual(self.ult("bogus").code, 0)


if __name__ == "__main__":
    unittest.main()
