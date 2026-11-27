"""Checks for the identity craft folder (logo, favicons, app icons, identity kit)."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

P = Path(__file__).resolve().parents[1]
CRAFT = P / "skills" / "website" / "references" / "craft" / "identity"
CRAFT_MD = P / "skills" / "website" / "references" / "website" / "craft.md"
TICKED = re.compile(r"`((?:\.\./)+[A-Za-z0-9_./-]+\.md|[a-z0-9-]+\.md)`")


class CraftIdentity(unittest.TestCase):
    def files(self):
        return sorted(CRAFT.glob("*.md"))

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
        on_disk = {p.name for p in self.files()} - {"index.md"}
        self.assertLessEqual(on_disk, listed)

    def test_references_resolve(self):
        for path in self.files():
            for ref in TICKED.findall(path.read_text(encoding="utf-8")):
                with self.subTest(file=path.name, ref=ref):
                    self.assertTrue((CRAFT / ref).resolve().is_file(), ref)

    def test_links_are_https(self):
        for path in self.files():
            for url in re.findall(r"\bhttps?://(?!www.w3.org/2000/svg)\S+", path.read_text(encoding="utf-8")):
                with self.subTest(file=path.name, url=url):
                    self.assertTrue(url.startswith("https://"))

    def test_pointed_to_from_craft(self):
        self.assertIn("`../craft/identity/index.md`", CRAFT_MD.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
