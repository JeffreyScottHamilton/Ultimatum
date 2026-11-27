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
        self.assertIn("Ultimatum's own", r.out)

    def test_guidance_does_not_push_generic_colour_habits(self):
        text = (OWN / "colors.csv").read_text(encoding="utf-8").lower()
        for bad in ("use a gradient", "add a glow", "purple gradient for"):
            self.assertNotIn(bad, text)

    def test_no_shared_word_runs_with_the_upstream_source(self):
        if not VAULT.is_dir():
            self.skipTest("upstream copy not present (git-ignored vault)")
        p = subprocess.run([sys.executable, str(REPO / "tools" / "copy_check.py"), str(OWN), str(VAULT),
                            "--skip", "fonts-meta.json", "--skip", "fonts.csv"],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout[-2000:])


# Real requests and the pairing each must land on.
FONT_REQUESTS = {
    "plumber": "Workshop", "cafe": "Kneaded", "law firm": "Counsel", "saas dashboard": "Product",
    "arabic": "Arabic Pair", "kids game": "Puzzle Box", "wedding photographer": "Keepsake",
    "vet clinic": "Paws", "nail salon": "Nail Bar", "fintech app": "Ledger App", "barber": "Chair",
    "hindi": "Devanagari Pair", "brewery": "Taproom", "museum": "Exhibit", "restaurant": "Supper",
    "gym": "Training Floor", "florist": "Bloom", "hotel": "Front Desk", "charity": "Good Cause",
    "university": "Campus", "news site": "Broadsheet", "documentation": "Docs", "japanese": "Japanese Pair",
}
GENERIC_DISPLAY = {"Inter", "Roboto", "Arial", "Open Sans"}  # craft.md: not as the display face
LICENCES = {"SIL Open Font License 1.1", "Apache 2.0", "Ubuntu Font Licence 1.0"}


class TestOwnTypography(UltCase):
    @classmethod
    def setUpClass(cls):
        with open(OWN / "typography.csv", newline="", encoding="utf-8") as f:
            cls.rows = list(csv.DictReader(f))
        cls.meta = json.loads((OWN / "fonts-meta.json").read_text(encoding="utf-8"))

    def test_covers_at_least_as_many_pairings_as_upstream(self):
        with open(THEIRS / "typography.csv", newline="", encoding="utf-8") as f:
            theirs = sum(1 for _ in csv.DictReader(f))
        self.assertGreaterEqual(len(self.rows), theirs)
        self.assertEqual(len({r["Pairing"] for r in self.rows}), len(self.rows))
        for r in self.rows:
            self.assertTrue(all(v.strip() for v in r.values()), r["Pairing"])

    def test_weights_exist_in_the_foundry_metadata(self):
        for r in self.rows:
            for fam, col in (("Heading Font", "Heading Weights"), ("Body Font", "Body Weights")):
                m = self.meta[r[fam]]
                for w in r[col].split(", "):
                    w = int(w)
                    ok = m["wght"][0] <= w <= m["wght"][1] if m["wght"] else w in m["weights"]
                    self.assertTrue(ok, f"{r['Pairing']}: {r[fam]} {w}")

    def test_licences_are_open_and_urls_load_only_used_weights(self):
        for r in self.rows:
            for lic in r["Licence"].split("; "):
                self.assertIn(lic, LICENCES, r["Pairing"])
            url = r["Google Fonts URL"]
            self.assertTrue(url.startswith("https://fonts.googleapis.com/css2?family="), url)
            self.assertTrue(url.endswith("&display=swap"), url)
            self.assertNotIn("ital,", url)

    def test_follows_the_type_lint(self):
        for r in self.rows:
            self.assertNotIn(r["Heading Font"], GENERIC_DISPLAY, r["Pairing"])
            self.assertNotIn("monospace", r["Kind"].split(" + ")[1], f"{r['Pairing']}: mono body text")
        bodies = __import__("collections").Counter(r["Body Font"] for r in self.rows)
        self.assertLessEqual(max(bodies.values()), 4, bodies.most_common(3))

    def test_csv_matches_a_fresh_build(self):
        p = subprocess.run([sys.executable, str(REPO / "tools" / "build_typography.py"), "--check"],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)

    def test_requests_land_on_the_right_pairing(self):
        for q, want in FONT_REQUESTS.items():
            r = self.ult("design", "search", *q.split(), "--in", "typography", "-n", "1", "--json")
            self.assertEqual(r.code, 0, r.err)
            got = [x["Pairing"] for x in json.loads(r.out)]
            self.assertEqual(got[:1], [want], q)

    def test_system_credits_our_typography(self):
        r = self.ult("design", "system", "coffee shop")
        self.assertRegex(r.out, r"\btypography\b[^:]*: Ultimatum's own")


# Real requests and the style each must land on.
STYLE_REQUESTS = {
    "glassmorphism frosted": "Glassmorphism",
    "plumber call quote": "Local Service Clear",
    "independent cafe shop": "Neighbourhood Warm",
    "potter joiner workshop": "Craft Workshop",
    "dentist clinic calm": "Clinical Calm",
    "jeweller hotel luxury": "Quiet Luxury",
    "photographer documentary": "Photo-led Documentary",
    "council public service": "Public Service Plain",
    "zine band gig": "Print Zine",
    "brutalism raw": "Brutalism",
    "bento grid": "Bento Box Grid",
    "executive kpi dashboard": "Executive Dashboard",
}


class TestOwnStyles(UltCase):
    @classmethod
    def setUpClass(cls):
        with open(OWN / "styles.csv", newline="", encoding="utf-8") as f:
            cls.rows = list(csv.DictReader(f))

    def test_covers_every_upstream_style_by_name(self):
        with open(THEIRS / "styles.csv", newline="", encoding="utf-8") as f:
            theirs = {r["Style Category"] for r in csv.DictReader(f)}
        ours = {r["Style"] for r in self.rows}
        self.assertEqual(len(ours), len(self.rows))
        self.assertEqual(sorted(theirs - ours), [])
        self.assertGreaterEqual(len(ours), len(theirs) + 8)

    def test_every_product_style_resolves(self):
        with open(THEIRS / "products.csv", newline="", encoding="utf-8") as f:
            wanted = {s.strip() for r in csv.DictReader(f)
                      for s in __import__("re").split(r"\s\+\s", r["Primary Style Recommendation"]) if s.strip()}
        names = {r["Style"] for r in self.rows}
        self.assertEqual(sorted(wanted - names), [])

    def test_csv_matches_a_fresh_build(self):
        p = subprocess.run([sys.executable, str(REPO / "tools" / "build_styles.py"), "--check"],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)

    def test_requests_land_on_the_right_style(self):
        for q, want in STYLE_REQUESTS.items():
            r = self.ult("design", "search", *q.split(), "--in", "style", "-n", "1", "--json")
            self.assertEqual(r.code, 0, r.err)
            got = [x["Style"] for x in json.loads(r.out)]
            self.assertEqual(got[:1], [want], q)

    def test_system_shows_our_style_tokens(self):
        r = self.ult("design", "system", "plumber")
        self.assertEqual(r.code, 0, r.err)
        self.assertIn("tokens:", r.out)
        self.assertRegex(r.out, r"\bstyles\b[^:]*: Ultimatum's own")
