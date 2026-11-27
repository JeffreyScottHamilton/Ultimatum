"""Ultimatum's own icon table (data/design-own/icons.csv): freshness, metadata, requests and copy check."""
import csv
import json
import shutil
import subprocess
import sys
from pathlib import Path

from _harness import UltCase

PLUGIN = Path(__file__).resolve().parents[1]
REPO = PLUGIN.parents[1]
OWN = PLUGIN / "data" / "design-own"
THEIRS = PLUGIN / "data" / "design"

COLUMNS = ["Category", "Icon Name", "Keywords", "Library", "Style", "Licence", "Import Code", "Best For",
           "Usage", "Accessible Name"]
PACKAGES = {"Lucide": "lucide-react", "Phosphor": "@phosphor-icons/react"}

# Real requests and the icon(s) the first result may be.
REQUESTS = {
    "phone call button": {"phone", "phone-call"},
    "opening hours": {"clock"},
    "map pin address": {"map-pin"},
    "star rating review": {"star"},
    "customer testimonial quote": {"quote", "message-square-quote"},
    "plumber repair wrench": {"wrench"},
    "book appointment": {"calendar-check"},
    "hamburger menu": {"menu"},
    "close dialog": {"x"},
    "delete item": {"trash"},
    "download pdf": {"download", "file-pdf"},
    "instagram link": {"instagram-logo"},
    "whatsapp chat": {"whatsapp-logo"},
    "shopping cart checkout": {"shopping-cart", "shopping-cart-simple"},
    "loading spinner": {"loader-circle"},
    "success message": {"circle-check"},
    "error warning": {"triangle-exclamation-point", "circle-exclamation-point"},
    "dentist teeth": {"tooth"},
    "get directions": {"navigation"},
    "dark mode toggle": {"moon", "sun"},
    "email contact": {"mail"},
    "gym workout": {"dumbbell"},
    "electrician power": {"zap"},
    "filter results": {"funnel"},
    "facebook page": {"facebook-logo"},
    "wheelchair access": {"wheelchair"},
}


class TestOwnIcons(UltCase):
    @classmethod
    def setUpClass(cls):
        with open(OWN / "icons.csv", newline="", encoding="utf-8") as f:
            cls.rows = list(csv.DictReader(f))
        cls.meta = json.loads((OWN / "icons-meta.json").read_text(encoding="utf-8"))

    def test_csv_matches_a_fresh_build(self):
        p = subprocess.run([sys.executable, str(REPO / "tools" / "build_icons.py"), "--check"],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)

    def test_columns_and_no_empty_cells(self):
        self.assertEqual(list(self.rows[0]), COLUMNS)
        for r in self.rows:
            for k, v in r.items():
                self.assertTrue((v or "").strip(), f"{r['Icon Name']}: empty {k}")

    def test_covers_at_least_as_many_icons_as_upstream(self):
        with open(THEIRS / "icons.csv", newline="", encoding="utf-8") as f:
            theirs = sum(1 for _ in csv.DictReader(f))
        self.assertGreaterEqual(len(self.rows), max(theirs, 105))
        keys = [(r["Library"], r["Icon Name"]) for r in self.rows]
        self.assertEqual(len(keys), len(set(keys)))

    def test_every_icon_exists_in_the_project_metadata(self):
        for r in self.rows:
            lib = r["Library"].lower()
            m = self.meta[lib].get(r["Icon Name"])
            self.assertIsNotNone(m, f"{lib}: {r['Icon Name']}")
            self.assertTrue(m["export_found"], f"{lib}: {r['Icon Name']} has no React export")

    def test_import_code_uses_the_exported_name_and_package(self):
        for r in self.rows:
            m = self.meta[r["Library"].lower()][r["Icon Name"]]
            want = f"import {{ {m['pascal']} }} from '{PACKAGES[r['Library']]}'"
            self.assertEqual(r["Import Code"], want)
            self.assertIn(f"<{m['pascal']} ", r["Usage"])
            self.assertRegex(m["pascal"], r"^[A-Z][A-Za-z0-9]*$")

    def test_licences_and_commits_are_recorded(self):
        for lib, licence in (("lucide", "ISC"), ("phosphor", "MIT")):
            src = self.meta["sources"][lib]
            self.assertEqual(src["licence_id"], licence)
            self.assertRegex(src["commit"], r"^[0-9a-f]{40}$")
            self.assertTrue(src["npm_version"])
        self.assertEqual({r["Licence"] for r in self.rows}, {"ISC (Lucide)", "MIT (Phosphor)"})

    def test_metadata_holds_no_artwork(self):
        text = (OWN / "icons-meta.json").read_text(encoding="utf-8")
        for bad in ("<svg", "<path", " d=\""):
            self.assertNotIn(bad, text)

    def test_covers_the_common_ui_jobs(self):
        names = {r["Icon Name"] for r in self.rows}
        for want in ("phone", "map-pin", "calendar", "clock", "star", "quote", "wrench", "menu", "x", "search",
                     "mail", "shopping-cart", "circle-check", "loader-circle", "instagram-logo"):
            self.assertIn(want, names)

    def test_requests_land_on_a_fitting_icon(self):
        self.assertGreaterEqual(len(REQUESTS), 15)
        for q, want in REQUESTS.items():
            r = self.ult("design", "search", *q.split(), "--in", "icon", "-n", "1", "--json")
            self.assertEqual(r.code, 0, r.err)
            got = [x["Icon Name"] for x in json.loads(r.out)]
            self.assertTrue(got and got[0] in want, f"{q!r} -> {got}")

    def test_design_domains_marks_icons_as_ours(self):
        r = self.ult("design", "domains")
        self.assertRegex(r.out, r"icon\s+\d+ rows\s+icons.csv\s+\(ours\)")

    def test_no_shared_word_runs_with_the_upstream_table(self):
        import tempfile
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            shutil.copy(OWN / "icons.csv", a)
            shutil.copy(THEIRS / "icons.csv", b)
            p = subprocess.run([sys.executable, str(REPO / "tools" / "copy_check.py"), a, b],
                               capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout[-2000:])
