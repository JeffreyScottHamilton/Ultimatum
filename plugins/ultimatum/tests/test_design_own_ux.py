"""Ultimatum's own UX guideline and reasoning tables (data/design-own): rebuilds, cells, links,
WCAG numbers, coverage requests and the copy check against the third-party tables."""
import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from _harness import UltCase

PLUGIN = Path(__file__).resolve().parents[1]
REPO = PLUGIN.parents[1]
OWN = PLUGIN / "data" / "design-own"
THEIRS = PLUGIN / "data" / "design"

sys.path.insert(0, str(REPO / "tools"))
import build_reasoning  # noqa: E402
import build_ux  # noqa: E402

# Real requests and the Issue each must land on in the first three results (plan section 3).
REQUESTS = {
    "focus ring": "Focus Ring Visible",
    "form error message": "Error Text Names the Problem",
    "tap target size": "Touch Targets Reach 44px",
    "skip link": "Skip Link to Main Content",
    "modal focus trap": "Modal Dialog Focus Handling",
    "color contrast of text": "Text Contrast",
    "alt text for images": "Informative Image Alt Text",
    "keyboard navigation": "Everything Works From the Keyboard",
    "reduced motion preference": "Respect Reduced Motion",
    "placeholder as label": "Visible Labels on Every Field",
    "password paste blocked": "Pasting Must Work",
    "autocomplete attributes on address fields": "Autocomplete Tokens on Personal Data",
    "icon button without label": "Icon-only Controls Need a Name",
    "sticky header covers focused element": "Focus Not Hidden Behind Sticky Bars",
    "carousel pause button": "Pause, Stop, Hide Moving Content",
    "text zoom 200 percent": "Text Resizes to 200 Percent",
    "horizontal scroll on mobile": "No Horizontal Scroll",
    "layout shift images": "Reserve Space to Prevent Jumps",
    "click to call phone number": "Phone Number Is a Tap-to-call Link",
    "map attribution": "Credit the Map Data",
    "drag and drop alternative": "Dragging Needs a Non-drag Alternative",
    "toast notification screen reader": "Announce Status Messages",
    "empty state": "Empty States Say What to Do",
    "delete confirmation": "Confirm Destructive Actions",
    "lazy loading images": "Lazy-load Below the Fold Only",
    "font loading swap": "Font Display Strategy",
    "page language attribute": "Declare the Page Language",
    "video captions": "Captions for Recorded Video",
    "unsaved changes warning": "Warn Before Losing Unsaved Work",
    "heading levels": "Heading Levels Describe Structure",
}


def ux_rows():
    with (OWN / "ux-guidelines.csv").open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def reasoning_rows():
    with (OWN / "ui-reasoning.csv").open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


class TestOwnUx(UltCase):
    def test_rebuild_matches(self):
        for script in ("build_ux.py", "build_reasoning.py"):
            p = subprocess.run([sys.executable, str(REPO / "tools" / script), "--check"],
                               capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)

    def test_enough_rows_and_every_cell_filled(self):
        rs = ux_rows()
        self.assertGreaterEqual(len(rs), 141)
        self.assertEqual(list(rs[0]), list(build_ux.COLS))
        for r in rs:
            for k, v in r.items():
                self.assertTrue(v.strip(), f"{r['Category']} / {r['Issue']}: empty {k}")
            self.assertIn(r["Severity"], build_ux.SEVERITIES)
            self.assertIn(r["Platform"], build_ux.PLATFORMS)
        keys = [(r["Category"], r["Issue"]) for r in rs]
        self.assertEqual(len(keys), len(set(keys)))

    def test_links_are_https_and_wcag_numbers_are_real(self):
        for r in ux_rows():
            self.assertTrue(r["Docs URL"].startswith("https://"), r["Issue"])
            if r["WCAG"] != "-":
                for sc in r["WCAG"].split(","):
                    self.assertIn(sc.strip(), build_ux.SC, f"{r['Issue']}: {sc}")
                    self.assertRegex(sc.strip(), r"^\d\.\d\.\d{1,2}$")
        # SC 4.1.1 (Parsing) was removed from WCAG 2.2, so it must not be cited.
        self.assertNotIn("4.1.1", build_ux.SC)
        self.assertEqual(len(build_ux.SC), 86)

    def test_wcag_rows_cover_the_main_criteria(self):
        cited = {sc.strip() for r in ux_rows() for sc in r["WCAG"].split(",")}
        for sc in ("1.1.1", "1.4.3", "1.4.10", "2.1.1", "2.4.7", "2.4.11", "2.5.7", "2.5.8", "3.2.6",
                   "3.3.7", "3.3.8", "4.1.2", "4.1.3"):
            self.assertIn(sc, cited)

    def test_good_examples_never_recommend_a_lint_banned_habit(self):
        for r in ux_rows():
            for k in ("Do", "Code Example Good"):
                for bad in build_ux.BANNED:
                    self.assertNotIn(bad, r[k].lower(), f"{r['Issue']}: {k}")

    def test_real_requests_land_on_a_fitting_row(self):
        self.assertGreaterEqual(len(REQUESTS), 25)
        for query, issue in REQUESTS.items():
            r = self.ult("design", "search", query, "--in", "ux", "--json")
            self.assertEqual(r.code, 0, r.out)
            got = [row["Issue"] for row in json.loads(r.out)]
            self.assertIn(issue, got, f"{query!r} -> {got}")

    def test_ux_domain_is_ours_and_system_still_returns_checks(self):
        r = self.ult("design", "domains")
        self.assertRegex(r.out, r"ux\s+\d+ rows\s+ux-guidelines.csv\s+\(ours\)")
        r = self.ult("design", "system", "plumber website", "--json")
        self.assertEqual(r.code, 0, r.out)
        self.assertTrue(json.loads(r.out)["checks"])

    def test_no_shared_word_runs_with_the_third_party_table(self):
        with tempfile.TemporaryDirectory() as tmp:
            ours, theirs = Path(tmp, "ours"), Path(tmp, "theirs")
            ours.mkdir()
            theirs.mkdir()
            for name in ("ux-guidelines.csv", "ui-reasoning.csv"):
                # The header row names the columns design.py reads; both tables must share it.
                for src, dest in ((OWN, ours), (THEIRS, theirs)):
                    body = (src / name).read_text(encoding="utf-8").split("\n", 1)[1]
                    (dest / name).write_text(body, encoding="utf-8")
            p = subprocess.run([sys.executable, str(REPO / "tools" / "copy_check.py"), str(ours), str(theirs)],
                               capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stdout[-2000:])


class TestOwnReasoning(UltCase):
    def test_every_product_type_has_exactly_one_row(self):
        want = build_reasoning.categories()
        got = [r["UI_Category"] for r in reasoning_rows()]
        self.assertGreaterEqual(len(got), 194)
        self.assertEqual(sorted(got), sorted(want))

    def test_every_cell_filled_and_styles_exist(self):
        styles = build_reasoning.known_styles()
        for r in reasoning_rows():
            for k, v in r.items():
                self.assertTrue(v.strip(), f"{r['UI_Category']}: empty {k}")
            for s in r["Style_Priority"].split(" + "):
                self.assertIn(s, styles, r["UI_Category"])
            self.assertGreaterEqual(len(r["Anti_Patterns"].split(" + ")), 2, r["UI_Category"])

    def test_joins_to_the_product_table_and_feeds_system(self):
        names = {r["UI_Category"] for r in reasoning_rows()}
        with (THEIRS / "products.csv").open(encoding="utf-8", newline="") as fh:
            for p in csv.DictReader(fh):
                self.assertIn(p["Product Type"], names, p["Product Type"])
        r = self.ult("design", "system", "plumber website", "--json")
        self.assertEqual(r.code, 0, r.out)
        ds = json.loads(r.out)
        self.assertTrue(ds["effects"] and ds["avoid"], ds["product"])

    def test_effects_do_not_recommend_lint_banned_habits(self):
        for r in reasoning_rows():
            for k in ("Recommended_Pattern", "Style_Priority", "Color_Mood", "Typography_Mood", "Key_Effects"):
                for bad in build_reasoning.BANNED:
                    self.assertNotIn(bad, r[k].lower(), f"{r['UI_Category']}: {k}")
