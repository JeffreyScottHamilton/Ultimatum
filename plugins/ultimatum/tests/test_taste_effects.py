"""Static checks on the Taste kit's WebGL effects; tools/taste_fx_check.cjs runs them in a browser."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

FX = Path(__file__).resolve().parents[1] / "data" / "craft" / "taste" / "kit" / "effects"
# Words GLSL ES 3.00 reserves that read like ordinary names (performance.md § WebGL).
RESERVED = ("input", "output", "filter", "sample", "active", "common", "partition")


class Effects(unittest.TestCase):
    def setUp(self):
        self.js = (FX / "effects.js").read_text(encoding="utf-8")

    def number(self, name: str) -> float:
        return float(re.search(rf"const {name} = ([\d.e]+);", self.js).group(1))

    def test_budget_constants(self):
        self.assertGreaterEqual(self.number("RUN"), 4)           # ambient runs last 4 s or more
        self.assertLessEqual(self.number("MAX_LIVE"), 4)         # live WebGL contexts
        self.assertLessEqual(self.number("MAX_PIXELS"), 1.5e6)   # canvas pixels across the page
        self.assertIn("Math.min(window.devicePixelRatio || 1, 1.5)", self.js)
        self.assertIn("1000 / 30", self.js)
        self.assertRegex(self.js, r"'grain-gradient': \{ scale: 0\.5,")  # noise at half resolution

    def test_shaders_avoid_reserved_words(self):
        shaders = "\n".join(re.findall(r"`([^`]*)`", self.js))
        self.assertIn("#version 300 es", shaders)
        for word in RESERVED:
            self.assertNotRegex(shaders, rf"\b{word}\b", word)

    def test_poster_rules_and_page_ids(self):
        self.assertIn("(prefers-reduced-motion: reduce), (max-width: 699px)", self.js)
        names = set(re.findall(r"^  '([a-z-]+)': \{", self.js, re.M))
        self.assertEqual(len(names), 3)
        css = (FX / "effects.css").read_text(encoding="utf-8")
        page = set(re.findall(r'data-fx="([a-z-]+)"', (FX / "index.html").read_text(encoding="utf-8")))
        self.assertEqual(page, names)
        for name in names:
            self.assertIn(f'.fx[data-fx="{name}"]', css, f"{name} has no poster")


if __name__ == "__main__":
    unittest.main()
