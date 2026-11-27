import ast
import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from ultlib import market  # noqa: E402

ULT = os.path.join(ROOT, "scripts", "ult")
GUIDES = os.path.join(ROOT, "skills", "website", "references", "craft", "marketing")

GOOD = """<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Boiler repair in Northgate | Smith Heating</title>
<meta name="description" content="Same-day boiler repair across Northgate. Gas Safe engineers, fixed prices from 85 pounds, and a 90-day guarantee on every repair.">
<link rel="canonical" href="https://smithheating.example/services/boiler-repair">
<meta property="og:title" content="Boiler repair in Northgate">
<meta property="og:description" content="Same-day boiler repair across Northgate.">
<meta property="og:image" content="https://smithheating.example/og.jpg">
<script type="application/ld+json">{"@context":"https://schema.org","@type":"Plumber","name":"Smith Heating","address":"1 High St, Northgate"}</script>
<script type="application/ld+json">{"@context":"https://schema.org","@type":"Service","name":"Boiler repair"}</script>
</head><body><h1>Boiler repair in Northgate</h1>
<img src="van.jpg" alt="Smith Heating van outside a house">
<a href="/book">Book a repair</a>
<form><label for="e">Email</label><input id="e" type="email" autocomplete="email">
<button>Get my quote</button></form>
</body></html>"""

BAD = """<html><head><script type="application/ld+json">{"@type":"Product", bad</script></head>
<body><img src="a.jpg"><form><input name="x"><button>Submit</button></form><a href="/x">click here</a></body></html>"""


def run(*args):
    return subprocess.run([sys.executable, ULT, "market", *args], capture_output=True, text=True)


def levels(findings):
    return [f["level"] if isinstance(f, dict) else f[0] for f in findings]


def ids(findings):
    out = []
    for f in findings:
        out.append(json.dumps(f) if isinstance(f, dict) else " ".join(map(str, f)))
    return " | ".join(out)


class Page(unittest.TestCase):
    def test_good_page_has_no_fail(self):
        findings, meta = market.check_page(GOOD, "good.html", "service")
        self.assertNotIn("fail", levels(findings), ids(findings))
        self.assertEqual(meta["title"], "Boiler repair in Northgate | Smith Heating")

    def test_bad_page_fails_on_basics(self):
        findings, _ = market.check_page(BAD, "bad.html", "home")
        text = ids(findings).lower()
        self.assertIn("fail", levels(findings))
        for word in ("title", "viewport", "h1", "alt", "json"):
            self.assertIn(word, text, word)

    def test_self_serving_stars_warn(self):
        page = GOOD.replace('"address":"1 High St, Northgate"}',
                            '"address":"1 High St","aggregateRating":{"ratingValue":5}}')
        findings, _ = market.check_page(page, "p.html", "service")
        self.assertIn("warn", levels(findings))
        self.assertIn("jsonld-self-review", ids(findings))

    def test_missing_required_schema_prop_fails(self):
        page = GOOD.replace(',"address":"1 High St, Northgate"', "")
        findings, _ = market.check_page(page, "p.html", "service")
        self.assertIn("address", ids(findings))
        self.assertIn("fail", levels(findings))

    def test_cli_exit_codes(self):
        with tempfile.TemporaryDirectory() as d:
            good = os.path.join(d, "good.html")
            bad = os.path.join(d, "bad.html")
            open(good, "w").write(GOOD)
            open(bad, "w").write(BAD)
            self.assertEqual(run("page", good, "--kind", "service").returncode, 0)
            self.assertEqual(run("page", bad).returncode, 1)
            self.assertEqual(run("page", os.path.join(d, "missing.html")).returncode, 2)
            out = run("page", good, bad, "--json")
            json.loads(out.stdout)


class ABTest(unittest.TestCase):
    def test_sample_size_known_value(self):
        n = market.sample_size(0.04, 0.10)
        self.assertTrue(39400 <= n <= 39550, n)

    def test_plan_rounds_to_weeks(self):
        out = market.plan(0.04, 0.10, daily=1500)
        self.assertEqual(out["run_days"] % 7, 0)
        self.assertGreaterEqual(out["run_days"], 14)
        small = market.plan(0.2, 0.5, daily=100000)
        self.assertEqual(small["run_days"], 14)

    def test_more_variants_need_more(self):
        self.assertGreater(market.sample_size(0.04, 0.10, variants=3), market.sample_size(0.04, 0.10))

    def test_read_verdicts(self):
        win = market.read((120, 3000), (160, 3010))
        self.assertEqual(win["verdict"], "B wins")
        self.assertAlmostEqual(win["p_value"], 0.0155, places=3)
        same = market.read((120, 3000), (122, 3000))
        self.assertEqual(same["verdict"], "no clear difference")
        early = market.read((120, 3000), (160, 3010), planned=39000)
        self.assertEqual(early["verdict"], "not finished")
        broken = market.read((120, 3000), (150, 3600))
        self.assertEqual(broken["verdict"], "broken split")

    def test_cli(self):
        self.assertEqual(run("abtest", "plan", "--base", "0.04", "--lift", "0.1").returncode, 0)
        self.assertEqual(run("abtest", "read", "--a", "120/3000", "--b", "150/3600").returncode, 1)
        self.assertEqual(run("abtest", "read", "--a", "nonsense", "--b", "1/2").returncode, 2)


class Events(unittest.TestCase):
    def check(self, rows):
        return market.check_events(rows)

    def test_good_plan(self):
        rows = [{"event": "quote_form_submitted", "properties": ["service_type"], "trigger": "server 200"},
                {"event": "booking_completed", "properties": [], "trigger": "thanks page"}]
        self.assertNotIn("fail", levels(self.check(rows)))

    def test_rules(self):
        rows = [{"event": "SubmitForm", "properties": [], "trigger": "x"},
                {"event": "lead_created", "properties": ["email"], "trigger": "x"},
                {"event": "lead_created", "properties": [], "trigger": "x"},
                {"event": "form_submit", "properties": [], "trigger": ""}]
        found = self.check(rows)
        text = ids(found).lower()
        self.assertGreaterEqual(levels(found).count("fail"), 3, text)
        self.assertIn("warn", levels(found))

    def test_cli_csv(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "plan.csv")
            open(path, "w").write("event,properties,trigger\ncall_link_clicked,page_path,tap on tel link\n")
            self.assertEqual(run("events", path).returncode, 0)
            open(path, "w").write("event,properties,trigger\nCallClick,phone_number,tap\n")
            self.assertEqual(run("events", path).returncode, 1)


class Hygiene(unittest.TestCase):
    def test_stdlib_only(self):
        src = open(market.__file__, encoding="utf-8").read()
        allowed = {"argparse", "csv", "json", "math", "re", "sys", "html", "pathlib", "statistics", "__future__"}
        for node in ast.walk(ast.parse(src)):
            if isinstance(node, ast.Import):
                names = [a.name.split(".")[0] for a in node.names]
            elif isinstance(node, ast.ImportFrom) and node.level == 0:
                names = [node.module.split(".")[0]]
            else:
                continue
            for name in names:
                self.assertIn(name, allowed, name)

    def test_guides_shaped_and_linked(self):
        index = open(os.path.join(GUIDES, "index.md"), encoding="utf-8").read()
        for name in sorted(os.listdir(GUIDES)):
            path = os.path.join(GUIDES, name)
            lines = open(path, encoding="utf-8").read().splitlines()
            self.assertTrue(lines[0].startswith("# "), name)
            self.assertTrue(lines[2].startswith("Read "), name)
            self.assertLess(os.path.getsize(path), 15000, name)
            if name != "index.md":
                self.assertIn("`%s`" % name, index, name)
        skill = open(os.path.join(ROOT, "skills", "website", "SKILL.md"), encoding="utf-8").read()
        self.assertIn("craft/marketing/index.md", skill)

    def test_cross_references_exist(self):
        import re
        for name in os.listdir(GUIDES):
            text = open(os.path.join(GUIDES, name), encoding="utf-8").read()
            for ref in re.findall(r"`([a-z-]+\.md)`", text):
                self.assertTrue(os.path.exists(os.path.join(GUIDES, ref))
                                or os.path.exists(os.path.join(GUIDES, "..", "..", ref)), (name, ref))

    def test_credit_line(self):
        index = open(os.path.join(GUIDES, "index.md"), encoding="utf-8").read()
        self.assertIn("MIT", index)
        self.assertIn("None of its text is copied", index)


if __name__ == "__main__":
    unittest.main()
