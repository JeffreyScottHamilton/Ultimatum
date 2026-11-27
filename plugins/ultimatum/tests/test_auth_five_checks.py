"""The five login checks in the app sign-in guide stay present and wired into the checklist."""
import re
import unittest
from pathlib import Path

APP = Path(__file__).resolve().parents[1] / "skills" / "website" / "references" / "app"


class FiveLoginChecks(unittest.TestCase):
    def setUp(self):
        self.auth = (APP / "auth.md").read_text(encoding="utf-8")

    def section(self) -> str:
        m = re.search(r"^## Five checks before an AI-written login ships\n(.*?)^## ", self.auth, re.M | re.S)
        self.assertIsNotNone(m, "five-checks section missing")
        return m.group(1)

    def test_five_numbered_checks_each_with_a_test(self):
        items = re.findall(r"^(\d+)\. \*\*(.+?)\*\*(.*)$", self.section(), re.M)
        self.assertEqual([int(n) for n, _, _ in items], [1, 2, 3, 4, 5])
        for _, title, body in items:
            self.assertIn("Test:", body, title)

    def test_key_points_kept(self):
        s = self.section()
        for needle in ("NEXT_PUBLIC_", "getUser()", "user B's record id", "Row-level security",
                       'scope: "global"', "Cache-Control: no-store", "replay", "same text", "rotate"):
            self.assertIn(needle, s)

    def test_in_checklist(self):
        self.assertIn("five checks in `auth.md`", (APP / "checklist.md").read_text(encoding="utf-8"))

    def test_guide_stays_small(self):
        self.assertLess(len(self.auth.encode()), 15_000)


if __name__ == "__main__":
    unittest.main()
