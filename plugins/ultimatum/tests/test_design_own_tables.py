"""Ultimatum's own app, react, chart and motion tables: build, cells, links, requests and copy check."""
import csv
import json
import re
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

# table -> (domain, minimum rows, column that names a row, real requests -> text the top row's name must contain)
TABLES = {
    "app-interface": ("app", 32, "Issue", {
        "icon button needs a label for screen readers": "Icon-only",
        "tap target size on mobile": "Touch target size",
        "modal dialog escape key": "Modal escape",
        "password show hide toggle": "Password",
        "numeric keyboard for code input": "Keyboard type",
        "safe area notch": "Safe area",
        "dark mode contrast": "Contrast",
        "drag and drop alternative": "Dragging",
        "skeleton loading state": "Loading",
        "empty state": "Empty states",
        "prefers reduced motion": "reduced motion",
    }),
    "react-performance": ("react", 44, "Issue", {
        "avoid waterfall promise all": "Run independent requests",
        "lazy load heavy component": "Load heavy components",
        "third party script analytics": "Third-party scripts",
        "useTransition slow filter": "transitions",
        "hydration mismatch": "hydration",
        "next/image priority hero": "images",
        "cache duplicate queries server component": "Deduplicate",
        "server action authorization": "authorise",
        "useEffect fetch race": "fetching in effects",
        "context rerender": "context",
    }),
    "charts": ("chart", 25, "Data Type", {
        "line chart for trend over time": "Change over a period",
        "sankey flow": "Flow between states",
        "heatmap correlation matrix": "Intensity",
        "candlestick stock": "Price candles",
        "map of regions choropleth": "Geographic",
        "funnel conversion": "Funnel",
        "treemap hierarchy": "Nested",
        "gantt schedule": "Schedule",
        "kpi sparkline": "Single key figure",
        "waterfall variance": "Running total",
    }),
    "motion": ("motion", 20, "Category", {
        "hover button feedback": "Hover",
        "scroll reveal": "Scroll reveal",
        "page transition view transitions": "Page transition",
        "skeleton loading shimmer": "Loading",
        "carousel autoplay": "Carousel",
        "stagger list": "Stagger",
        "parallax": "Parallax",
        "snappy precise personality": "Snappy",
        "cinematic": "Cinematic",
        "marquee ambient loop": "Ambient",
    }),
}


def rows(table):
    with (OWN / f"{table}.csv").open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


class TestOwnTables(UltCase):
    def test_csvs_match_a_fresh_build(self):
        p = subprocess.run([sys.executable, str(REPO / "tools" / "build_tables.py"), "--check"],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)

    def test_enough_rows_and_no_empty_cells(self):
        for table, (_, minimum, key, _) in TABLES.items():
            rs = rows(table)
            self.assertGreaterEqual(len(rs), minimum, table)
            for r in rs:
                for col, v in r.items():
                    self.assertTrue(v.strip(), f"{table}: {r[key]}: empty {col}")

    def test_kept_columns_are_still_there(self):
        keep = {
            "app-interface": ["Category", "Issue", "Keywords", "Description", "Do", "Don't", "Code Example Good", "Severity"],
            "react-performance": ["Category", "Issue", "Keywords", "Description", "Do", "Don't", "Code Example Good", "Severity"],
            "charts": ["Data Type", "Keywords", "Best Chart Type", "Secondary Options", "When to Use",
                       "When NOT to Use", "Accessibility Notes", "Library Recommendation"],
            "motion": ["Category", "Intensity Tier", "Keywords", "Trigger", "Duration", "Easing", "Do", "Don't",
                       "Performance Notes"],
        }
        extra = {"app-interface": ["Code Example Bad", "Platform", "Docs URL"],
                 "react-performance": ["Code Example Bad", "Platform", "Docs URL"],
                 "charts": ["Docs URL"], "motion": ["Reduced Motion"]}
        for table, cols in keep.items():
            have = list(rows(table)[0])
            self.assertEqual([c for c in cols + extra[table] if c not in have], [], table)

    def test_links_are_https_and_react_rows_cite_react_or_next(self):
        for table in ("app-interface", "react-performance", "charts"):
            for r in rows(table):
                self.assertRegex(r["Docs URL"], r"^https://[^\s]+$", f"{table}: {r[TABLES[table][2]]}")
        for r in rows("react-performance"):
            self.assertRegex(r["Docs URL"], r"^https://(react\.dev|nextjs\.org)/", r["Issue"])

    def test_code_examples_differ_and_names_are_unique(self):
        for table in ("app-interface", "react-performance"):
            rs = rows(table)
            self.assertEqual(len({(r["Category"], r["Issue"]) for r in rs}), len(rs), table)
            for r in rs:
                self.assertNotEqual(r["Code Example Good"], r["Code Example Bad"], r["Issue"])

    def test_chart_libraries_name_a_permissive_licence(self):
        for r in rows("charts"):
            for lib in r["Library Recommendation"].split(";"):
                self.assertTrue(lib.strip().startswith("Native HTML")
                                or re.search(r"\((MIT|ISC|BSD-[23]-Clause|Apache-2\.0)\)$", lib.strip()),
                                f"{r['Data Type']}: {lib}")

    def test_every_motion_row_has_a_reduced_motion_fallback_and_personalities_exist(self):
        rs = rows("motion")
        for r in rs:
            self.assertGreater(len(r["Reduced Motion"].split()), 2, r["Category"])
        personalities = [r["Category"] for r in rs if r["Category"].startswith("Personality")]
        self.assertEqual(len(personalities), 3)

    def test_requests_land_on_a_fitting_row(self):
        for table, (domain, _, key, reqs) in TABLES.items():
            self.assertGreaterEqual(len(reqs), 8, table)
            for q, want in reqs.items():
                r = self.ult("design", "search", q, "--in", domain, "-n", "1", "--json")
                self.assertEqual(r.code, 0, r.err)
                got = json.loads(r.out)
                name = (got[0].get(key, "") if got else "")
                self.assertIn(want.lower(), name.lower(), f"{table}: {q!r} -> {name!r}")

    def test_domains_list_marks_them_ours(self):
        out = self.ult("design", "domains").out
        for table, (domain, _, _, _) in TABLES.items():
            self.assertRegex(out, rf"{domain}\s+\d+ rows\s+{re.escape(table)}.csv\s+\(ours\)")

    def test_no_shared_word_runs_with_the_third_party_tables(self):
        for table in TABLES:
            with tempfile.TemporaryDirectory() as ours, tempfile.TemporaryDirectory() as theirs:
                for src, dest in ((OWN, ours), (THEIRS, theirs)):
                    shutil.copy(src / f"{table}.csv", dest)
                p = subprocess.run([sys.executable, str(REPO / "tools" / "copy_check.py"), ours, theirs],
                                   capture_output=True, text=True)
                self.assertEqual(p.returncode, 0, f"{table}: {p.stdout[-1500:]}")
