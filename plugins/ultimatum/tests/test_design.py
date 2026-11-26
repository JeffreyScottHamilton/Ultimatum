"""Covers ultlib.design (`ult design`) and the bundled design tables it reads."""
import json
from pathlib import Path

from _harness import UltCase

DATA = Path(__file__).resolve().parents[1] / "data" / "design"


class TestDesignData(UltCase):
    def test_tables_ship_with_their_licence_and_source(self):
        self.assertIn("MIT", (DATA / "LICENSE").read_text(encoding="utf-8"))
        self.assertIn("ui-ux-pro-max-skill@", (DATA / "SOURCE.txt").read_text(encoding="utf-8"))
        self.assertTrue((DATA / "NOTICE.md").is_file())

    def test_domains_lists_every_table_with_rows(self):
        r = self.ult("design", "domains")
        self.assertEqual(r.code, 0, r.out)
        for name in ("product", "style", "color", "typography", "landing", "ux", "chart"):
            self.assertRegex(r.out, rf"{name}\s+\d+ rows")
        self.assertIn("nextjs", r.out)


class TestDesignSearch(UltCase):
    def test_search_finds_a_style_by_its_words(self):
        r = self.ult("design", "search", "glassmorphism frosted", "--json")
        self.assertEqual(r.code, 0, r.out)
        rows = json.loads(r.out)
        self.assertTrue(rows)
        self.assertIn("glass", rows[0]["Style"].lower())

    def test_search_in_a_stack(self):
        r = self.ult("design", "search", "image optimization", "--in", "stack:nextjs", "--json")
        self.assertEqual(r.code, 0, r.out)
        self.assertTrue(json.loads(r.out))

    def test_unknown_domain_is_a_clear_error(self):
        r = self.ult("design", "search", "x", "--in", "nope")
        self.assertEqual(r.code, 2)


class TestDesignSystem(UltCase):
    def system(self, brief, *extra):
        r = self.ult("design", "system", brief, "--json", *extra)
        self.assertEqual(r.code, 0, r.out)
        return json.loads(r.out)

    def test_everyday_words_land_on_the_right_business(self):
        for brief, want in [("coffee shop website", "Bakery/Cafe"),
                            ("nonprofit animal shelter", "Non-profit/Charity"),
                            ("plumber in Austin", "Home Services"),
                            ("dentist clinic booking", "Dental Practice"),
                            ("SaaS analytics dashboard", "Analytics Dashboard")]:
            with self.subTest(brief=brief):
                self.assertTrue(self.system(brief)["product"].startswith(want))

    def test_system_pairs_style_palette_fonts_and_checks(self):
        ds = self.system("coffee shop website")
        self.assertTrue(ds["styles"])
        self.assertTrue(ds["palette"])
        self.assertEqual(len(ds["fonts"]), 2)
        self.assertTrue(ds["checks"])

    def test_niche_checks_stay_out_unless_named(self):
        cats = {c["Category"].lower() for c in self.system("coffee shop website")["checks"]}
        self.assertNotIn("maps", cats)

    def test_stack_adds_stack_checks_and_rejects_unknown(self):
        self.assertTrue(self.system("coffee shop", "--stack", "nextjs")["stack_checks"])
        self.assertEqual(self.ult("design", "system", "coffee shop", "--stack", "cobol").code, 2)

    def test_markdown_names_the_source_and_writes_a_file(self):
        r = self.ult("design", "system", "Italian restaurant", "--out", "design/system.md")
        self.assertEqual(r.code, 0, r.out)
        text = (self.root / "design" / "system.md").read_text(encoding="utf-8")
        self.assertIn("UI UX Pro Max data, MIT", text)
        self.assertIn("Checks before delivery", text)

    def test_no_match_gives_a_hint(self):
        r = self.ult("design", "system", "zzqx")
        self.assertEqual(r.code, 0)
        self.assertIn("no product match", r.out)
