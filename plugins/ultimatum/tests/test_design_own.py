"""Ultimatum's own design tables (data/design-own): contrast, coverage, freshness and copy check."""
import csv
import json
import subprocess
import sys
from pathlib import Path

from _harness import UltCase

PLUGIN = Path(__file__).resolve().parents[1]
REPO = PLUGIN.parents[1]
OWN = PLUGIN / "data" / "design-own"
THEIRS = PLUGIN / "data" / "design"
VAULT = REPO / ".ultimatum" / "vault" / "ui-ux-pro-max"

sys.path.insert(0, str(REPO / "tools"))
from build_palettes import contrast  # noqa: E402

HEX = __import__("re").compile(r"^#[0-9A-F]{6}$")
TEXT_PAIRS = [("On Primary", "Primary"), ("On Secondary", "Secondary"), ("On Accent", "Accent"),
              ("Foreground", "Background"), ("Card Foreground", "Card"), ("Muted Foreground", "Muted"),
              ("Muted Foreground", "Background"), ("On Destructive", "Destructive"),
              ("Primary", "Background"), ("Foreground", "Muted")]

# Real requests and the palette each must land on (coverage test, plan section 3).
REQUESTS = {
    "cafe palette": "Bakery/Cafe", "coffee shop colours": "Bakery/Cafe", "plumber": "Home Services",
    "dentist": "Dental Practice", "hair salon": "Hair Salon", "barber shop": "Hair Salon",
    "roofing company": "Roofing", "locksmith": "Locksmith", "mechanic garage": "Auto Repair",
    "law firm": "Legal Services", "accountant": "Accountant", "yoga studio": "Yoga",
    "personal trainer": "Personal Trainer", "tattoo studio": "Tattoo", "florist": "Florist",
    "wedding photographer": "Wedding Photographer", "food truck": "Food Truck",
    "vet clinic": "Veterinary", "charity": "Non-profit", "church": "Church",
    "saas dashboard": "SaaS", "developer tool": "Developer Tool", "online course": "Course",
    "hotel": "Hotel", "real estate agent": "Real Estate", "cleaning service": "Cleaning",
    "landscaping": "Landscaping", "driving school": "Driving School", "tutoring": "Tutoring",
    "museum": "Museum", "podcast": "Podcast", "brewery": "Brewery", "pest control": "Pest Control",
}


def rows():
    with (OWN / "colors.csv").open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


class TestOwnColors(UltCase):
    def test_every_cell_is_filled_and_colours_are_hex(self):
        rs = rows()
        self.assertGreaterEqual(len(rs), 194)
        for r in rs:
            for k, v in r.items():
                self.assertTrue(v.strip(), f"{r['Product Type']}: empty {k}")
                if k not in ("Product Type", "Family", "Mode", "Notes", "Avoid"):
                    self.assertRegex(v, HEX, f"{r['Product Type']}: {k}")

    def test_every_text_pair_meets_wcag_contrast(self):
        bad = []
        for r in rows():
            for fg, bg in TEXT_PAIRS:
                if contrast(r[fg], r[bg]) < 4.5:
                    bad.append(f"{r['Product Type']}: {fg} on {bg} {contrast(r[fg], r[bg]):.2f}")
            if contrast(r["Ring"], r["Background"]) < 3:
                bad.append(f"{r['Product Type']}: ring {contrast(r['Ring'], r['Background']):.2f}")
        self.assertEqual(bad, [])

    def test_contrast_maths_matches_known_values(self):
        self.assertAlmostEqual(contrast("#000000", "#FFFFFF"), 21.0, places=2)
        self.assertAlmostEqual(contrast("#777777", "#FFFFFF"), 4.48, places=2)

    def test_every_product_type_has_a_palette_and_names_are_unique(self):
        names = [r["Product Type"] for r in rows()]
        self.assertEqual(len(names), len(set(names)))
        with (THEIRS / "products.csv").open(encoding="utf-8", newline="") as fh:
            products = {r["Product Type"] for r in csv.DictReader(fh)}
        self.assertEqual(products - set(names), set())

    def test_brand_colour_is_not_mistaken_for_the_error_red(self):
        import colorsys

        def hue(h):
            return colorsys.rgb_to_hsv(*(b / 255 for b in bytes.fromhex(h[1:])))[0] * 360
        close = [r["Product Type"] for r in rows()
                 if abs((hue(r["Primary"]) - hue(r["Destructive"]) + 180) % 360 - 180) < 12]
        self.assertEqual(close, [])

    def test_palettes_are_not_all_alike(self):
        self.assertGreater(len({r["Primary"] for r in rows()}), 180)

    def test_csv_matches_a_fresh_build(self):
        p = subprocess.run([sys.executable, str(REPO / "tools" / "build_palettes.py"), "--check"],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout)

    def test_requests_land_on_the_right_palette(self):
        misses = []
        for q, want in REQUESTS.items():
            r = self.ult("design", "search", q, "--in", "color", "--json")
            got = json.loads(r.out)[0]["Product Type"] if r.code == 0 and json.loads(r.out) else ""
            if want.lower() not in got.lower():
                misses.append(f"{q!r} -> {got!r}")
        self.assertEqual(misses, [])

    def test_design_tools_use_our_table_and_say_so(self):
        r = self.ult("design", "domains")
        self.assertRegex(r.out, r"color\s+\d+ rows\s+colors.csv\s+\(ours\)")
        r = self.ult("design", "system", "plumber")
        self.assertIn("colors: Ultimatum's own", r.out)

    def test_guidance_does_not_push_generic_colour_habits(self):
        text = (OWN / "colors.csv").read_text(encoding="utf-8").lower()
        for bad in ("use a gradient", "add a glow", "purple gradient for"):
            self.assertNotIn(bad, text)

    def test_no_shared_word_runs_with_the_upstream_source(self):
        if not VAULT.is_dir():
            self.skipTest("upstream copy not present (git-ignored vault)")
        p = subprocess.run([sys.executable, str(REPO / "tools" / "copy_check.py"), str(OWN), str(VAULT)],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout[-2000:])
