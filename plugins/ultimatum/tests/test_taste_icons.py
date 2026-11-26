"""The Taste kit's icon demo page inlines glyphs.svg; keep the two the same."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ICONS = Path(__file__).resolve().parents[1] / "data" / "craft" / "taste" / "kit" / "icons"
SYMBOL = re.compile(r"<symbol\b.*?</symbol>", re.S)


class Icons(unittest.TestCase):
    def test_demo_page_carries_every_symbol_verbatim(self):
        sprite = SYMBOL.findall((ICONS / "glyphs.svg").read_text(encoding="utf-8"))
        page = (ICONS / "index.html").read_text(encoding="utf-8")
        self.assertEqual(len(sprite), 16)
        self.assertEqual(SYMBOL.findall(page), sprite)

    def test_every_used_glyph_exists(self):
        ids = set(re.findall(r'<symbol id="([\w-]+)"', (ICONS / "glyphs.svg").read_text(encoding="utf-8")))
        used = set(re.findall(r'href="#(i-[\w-]+)"', (ICONS / "index.html").read_text(encoding="utf-8")))
        self.assertTrue(used)
        self.assertLessEqual(used, ids)


if __name__ == "__main__":
    unittest.main()
