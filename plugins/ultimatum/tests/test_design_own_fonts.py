"""Ultimatum's own Google Fonts catalogue (data/design-own/fonts.csv): shape, facts and requests."""
import csv
import json
import subprocess
import sys
from pathlib import Path

from _harness import UltCase

PLUGIN = Path(__file__).resolve().parents[1]
REPO = PLUGIN.parents[1]
FONTS = PLUGIN / "data" / "design-own" / "fonts.csv"

# Real requests and families the top three may include.
REQUESTS = {
    "code monospace": {"Fira Code", "JetBrains Mono", "PT Mono", "M PLUS 1 Code", "Source Code Pro",
                       "IBM Plex Mono", "Roboto Mono"},
    "arabic": {"Noto Naskh Arabic UI", "Noto Sans Arabic UI", "IBM Plex Sans Arabic", "Cairo", "Tajawal",
               "Noto Sans Arabic", "Noto Kufi Arabic"},
    "Fraunces": {"Fraunces"},
    "Inter": {"Inter", "Inter Tight"},
}


class FontCatalogue(UltCase):
    @classmethod
    def setUpClass(cls):
        with FONTS.open(encoding="utf-8", newline="") as fh:
            cls.rows = list(csv.DictReader(fh))
        cls.by = {r["Family"]: r for r in cls.rows}

    def test_builder_check_passes(self):
        p = subprocess.run([sys.executable, str(REPO / "tools" / "build_fonts.py"), "--check"],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout[-1500:])

    def test_covers_the_whole_library(self):
        self.assertGreaterEqual(len(self.rows), 1900)

    def test_known_facts(self):
        inter = self.by["Inter"]
        self.assertEqual(inter["Licence"], "OFL-1.1")
        self.assertEqual(inter["Weights"], "100-900 variable")
        self.assertIn("Latin", inter["Scripts"])
        self.assertTrue(inter["CSS URL"].startswith("https://fonts.googleapis.com/css2?family=Inter:wght@100..900"))
        self.assertEqual(self.by["Molle"]["Italic"], "only")
        self.assertIn("ital,wght@1,", self.by["Molle"]["CSS URL"])
        self.assertEqual(self.by["Noto Sans JP"]["Primary Script"], "Jpan")
        self.assertIn("monospace", self.by["JetBrains Mono"]["Kind"])

    def test_requests_find_sensible_families(self):
        for query, want in REQUESTS.items():
            r = self.ult("design", "search", query, "--in", "font", "-n", "3", "--json")
            got = {row["Family"] for row in json.loads(r.out)}
            self.assertTrue(got & want, f"{query!r} gave {sorted(got)}")

    def test_formal_scripts_answer_wedding_requests(self):
        r = self.ult("design", "search", "wedding invitation", "--in", "font", "-n", "3", "--json")
        for row in json.loads(r.out):
            self.assertIn("handwriting", row["Kind"])

    def test_listed_as_ours(self):
        r = self.ult("design", "domains")
        self.assertRegex(r.out, r"font\s+\d{4} rows\s+fonts.csv\s+\(ours\)")
