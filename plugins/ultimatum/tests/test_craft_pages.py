"""Checks for the page anatomy craft folder (landing, developer landing, settings)."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

P = Path(__file__).resolve().parents[1]
CRAFT = P / "skills" / "website" / "references" / "craft" / "pages"
CRAFT_MD = P / "skills" / "website" / "references" / "website" / "craft.md"
TICKED = re.compile(r"`((?:\.\./)+[A-Za-z0-9_./-]+\.md|[a-z0-9-]+\.md)`")
SECRET = re.compile(r"(sk|pk|rk)_(live|test)_[A-Za-z0-9]{8,}|AKIA[0-9A-Z]{16}|[\w.+-]+@[\w-]+\.[\w.]+")


class CraftPages(unittest.TestCase):
    def files(self):
        return sorted(CRAFT.glob("*.md"))

    def test_expected_files(self):
        names = {p.name for p in self.files()}
        self.assertEqual(names, {"index.md", "landing.md", "devtool-landing.md", "settings.md"})

    def test_shape(self):
        for path in self.files():
            lines = path.read_text(encoding="utf-8").splitlines()
            with self.subTest(file=path.name):
                self.assertLessEqual(path.stat().st_size, 15 * 1024)
                self.assertTrue(lines[0].startswith("# "))
                self.assertTrue(lines[2].startswith("Read "))

    def test_index_lists_every_file(self):
        index = (CRAFT / "index.md").read_text(encoding="utf-8")
        listed = set(re.findall(r"`([a-z0-9-]+\.md)`", index))
        self.assertLessEqual({p.name for p in self.files()} - {"index.md"}, listed)

    def test_references_resolve(self):
        for path in self.files():
            for ref in TICKED.findall(path.read_text(encoding="utf-8")):
                with self.subTest(file=path.name, ref=ref):
                    self.assertTrue((CRAFT / ref).resolve().is_file(), ref)

    def test_first_screen_test_has_five_questions(self):
        text = (CRAFT / "landing.md").read_text(encoding="utf-8")
        section = text.split("## 7. First-screen test", 1)[1]
        self.assertEqual(len(re.findall(r"^\d\. ", section, re.M)), 5)

    def test_settings_covers_every_surface(self):
        text = (CRAFT / "settings.md").read_text(encoding="utf-8")
        for heading in ("## 6. Desktop apps", "## 7. Command-line tools", "## 8. Terminal UIs", "## 9. Build order"):
            with self.subTest(heading=heading):
                self.assertIn(heading, text)

    def test_no_credentials(self):
        for path in self.files():
            with self.subTest(file=path.name):
                self.assertIsNone(SECRET.search(path.read_text(encoding="utf-8")))

    def test_pointed_to_from_craft(self):
        self.assertIn("`../craft/pages/index.md`", CRAFT_MD.read_text(encoding="utf-8"))

    def test_frontend_budget_later_points_here(self):
        later = P / "skills" / "work" / "references" / "craft" / "frontend-budget" / "later.md"
        self.assertIn("craft/pages/", later.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
