"""Ultimatum's own products.csv and landing.csv (data/design-own): rebuild, joins, coverage, copy check."""
import csv
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from _harness import UltCase

PLUGIN = Path(__file__).resolve().parents[1]
REPO = PLUGIN.parents[1]
OWN = PLUGIN / "data" / "design-own"
THEIRS = PLUGIN / "data" / "design"
VAULT = REPO / ".ultimatum" / "vault" / "ui-ux-pro-max"

sys.path.insert(0, str(REPO / "tools"))
import build_landing  # noqa: E402
import build_products  # noqa: E402


def read(path):
    with Path(path).open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


# Real requests and the product each must land on (substring of the Product Type).
PRODUCT_REQUESTS = {
    "plumber site": "Home Services", "cafe": "Bakery/Cafe", "saas pricing page": "SaaS (General)",
    "dentist booking": "Dental Practice", "hair salon": "Hair Salon", "barber shop": "Hair Salon",
    "roofer": "Roofing", "locksmith": "Locksmith", "mechanic garage": "Auto Repair",
    "law firm": "Legal Services", "accountant": "Accountant", "personal trainer": "Personal Trainer",
    "tattoo studio": "Tattoo", "florist": "Florist", "wedding photographer": "Wedding Photographer",
    "food truck": "Food Truck", "vet clinic": "Veterinary", "charity donate": "Non-profit",
    "church": "Church", "developer tool": "Developer Tool", "online course": "Online Course",
    "hotel": "Hotel", "estate agent": "Real Estate", "cleaning service": "Cleaning",
    "landscaper": "Landscaping", "driving school": "Driving School", "tutor": "Tutoring",
    "museum": "Museum", "podcast": "Podcast", "brewery": "Brewery", "pest control": "Pest Control",
    "moving company": "Moving Company", "electrician": "Home Services", "physio": "Physiotherapy",
    "crypto wallet": "Fintech", "dashboard analytics": "Analytics Dashboard",
    "booking app": "Booking & Appointment", "password manager": "Password Manager",
    "pharmacy": "Pharmacy", "caterer": "Caterer", "nail salon": "Nail Salon", "optician": "Optician",
    "job board": "Job Board", "weather app": "Weather", "puzzle game": "Casual Puzzle Game",
}
# Whole-brief requests: the landing pattern `ult design system` must pair with them.
LANDING_REQUESTS = {
    "plumber website": "Call-First Trade Page", "locksmith lockout": "Emergency Call-Out",
    "dentist booking": "Clinic Trust and Book", "cafe": "Menu and Visit",
    "saas pricing page": "Product Page with Proof", "removals company quote": "Quote Request Form",
    "wedding photographer": "Portfolio Enquiry", "charity donate": "Donation and Impact",
}
APP_PATTERNS = {"Sign-up Page", "Pricing Tiers Page", "Dashboard Overview", "Checkout Flow",
                "Booking Flow in an App", "Quote Request Form", "Emergency Call-Out"}


class TestOwnProducts(UltCase):
    def test_csv_matches_a_fresh_build(self):
        for mod, name in ((build_products, "build_products.py"), (build_landing, "build_landing.py")):
            p = subprocess.run([sys.executable, str(REPO / "tools" / name), "--check"],
                               capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)

    def test_one_row_for_every_product_type_ours_and_theirs(self):
        names = [r["Product Type"] for r in read(OWN / "products.csv")]
        self.assertEqual(len(names), len(set(names)))
        want = {l.strip() for l in (OWN / "product-types.txt").read_text(encoding="utf-8").splitlines() if l.strip()}
        want |= {r["Product Type"] for r in read(THEIRS / "products.csv")}
        self.assertGreaterEqual(len(names), 224)
        self.assertEqual(want - set(names), set())

    def test_every_cell_is_filled_and_columns_are_kept(self):
        rows = read(OWN / "products.csv")
        for col in ("Product Type", "Keywords", "Primary Style Recommendation", "Secondary Styles",
                    "Landing Page Pattern", "Dashboard Style (if applicable)", "Color Palette Focus",
                    "Key Considerations", "Main Action", "Trust Signals", "Booking/Quote"):
            self.assertIn(col, rows[0])
        for r in rows:
            for k, v in r.items():
                self.assertTrue(v.strip(), f"{r['Product Type']}: empty {k}")
        lrows = read(OWN / "landing.csv")
        for col in ("Pattern Name", "Aliases", "Keywords", "Section Order", "Primary CTA Placement",
                    "Color Strategy", "Recommended Effects", "Conversion Optimization"):
            self.assertIn(col, lrows[0])
        for r in lrows:
            for k, v in r.items():
                self.assertTrue(v.strip(), f"{r['Pattern Name']}: empty {k}")

    def test_styles_and_landing_patterns_resolve(self):
        styles = build_products.style_names()
        landing = {r["Pattern Name"] for r in read(OWN / "landing.csv")}
        bad = []
        for r in read(OWN / "products.csv"):
            parts = r["Primary Style Recommendation"].split(" + ") + r["Secondary Styles"].split(", ")
            bad += [f"{r['Product Type']}: {p}" for p in parts if p.strip().lower() not in styles]
            if r["Landing Pattern Match"] not in landing:
                bad.append(f"{r['Product Type']}: landing {r['Landing Pattern Match']}")
        self.assertEqual(bad, [])

    def test_landing_covers_page_and_app_patterns(self):
        rows = read(OWN / "landing.csv")
        names = [r["Pattern Name"] for r in rows]
        self.assertEqual(len(names), len(set(names)))
        self.assertGreaterEqual(len(rows), 41)
        self.assertGreaterEqual(len([r for r in rows if r["Kind"] != "App"]), 34)
        self.assertEqual(APP_PATTERNS - set(names), set())

    def test_requests_land_on_the_right_product(self):
        misses = []
        for q, want in PRODUCT_REQUESTS.items():
            r = self.ult("design", "search", q, "--in", "product", "--json")
            found = json.loads(r.out) if r.code == 0 and r.out.strip() else []
            got = found[0]["Product Type"] if found else ""
            if want.lower() not in got.lower():
                misses.append(f"{q!r} -> {got!r}")
        self.assertGreaterEqual(len(PRODUCT_REQUESTS), 30)
        self.assertEqual(misses, [])

    def test_system_pairs_requests_with_the_right_landing_pattern(self):
        misses = []
        for q, want in LANDING_REQUESTS.items():
            r = self.ult("design", "system", q, "--json")
            got = (json.loads(r.out).get("landing") or {}).get("Pattern Name", "") if r.code == 0 else ""
            if got != want:
                misses.append(f"{q!r} -> {got!r}")
        self.assertEqual(misses, [])

    def test_landing_search_finds_patterns(self):
        for q, want in (("emergency call out", "Emergency Call-Out"), ("pricing tiers", "Pricing Tiers Page"),
                        ("checkout payment", "Checkout Flow"), ("sign up account", "Sign-up Page")):
            r = self.ult("design", "search", q, "--in", "landing", "--json")
            self.assertEqual(r.code, 0, r.all)
            self.assertIn(want, [x["Pattern Name"] for x in json.loads(r.out)][:3], q)

    def test_no_shared_word_runs_with_their_tables(self):
        with tempfile.TemporaryDirectory() as tmp:
            for name in ("products.csv", "landing.csv"):
                ours, theirs = Path(tmp, "ours-" + name[:-4]), Path(tmp, "theirs-" + name[:-4])
                ours.mkdir(), theirs.mkdir()
                shutil.copy(OWN / name, ours / name)
                shutil.copy(THEIRS / name, theirs / name)
                p = subprocess.run([sys.executable, str(REPO / "tools" / "copy_check.py"), str(ours), str(theirs)],
                                   capture_output=True, text=True)
                self.assertEqual(p.returncode, 0, name + "\n" + p.stdout[-2000:])
