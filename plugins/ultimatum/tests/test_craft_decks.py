"""Checks for the decks craft folder and its deck checker."""
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

P = Path(__file__).resolve().parents[1]
CRAFT = P / "skills" / "website" / "references" / "craft" / "decks"
DATA = P / "data" / "craft" / "decks"
CHECK = DATA / "deck_check.py"
CRAFT_MD = P / "skills" / "website" / "references" / "website" / "craft.md"
TICKED = re.compile(r"`((?:\.\./)+[A-Za-z0-9_./-]+\.(?:md|py|html)|[a-z0-9-]+\.md)`")


def run(*args):
    return subprocess.run([sys.executable, str(CHECK), *args], capture_output=True, text=True)


class DecksGuide(unittest.TestCase):
    def files(self):
        return sorted(CRAFT.glob("*.md"))

    def test_shape(self):
        for path in self.files():
            lines = path.read_text(encoding="utf-8").splitlines()
            with self.subTest(file=path.name):
                self.assertLessEqual(path.stat().st_size, 15 * 1024)
                self.assertTrue(lines[0].startswith("# "))
                self.assertTrue(lines[2].startswith("Read "))

    def test_index_lists_every_file(self):
        index = (CRAFT / "index.md").read_text(encoding="utf-8")
        listed = set(re.findall(r"`([a-z0-9-]+\.md)`", index))
        self.assertLessEqual({p.name for p in self.files()} - {"index.md"}, listed)

    def test_references_resolve(self):
        for path in self.files():
            for ref in TICKED.findall(path.read_text(encoding="utf-8")):
                with self.subTest(file=path.name, ref=ref):
                    self.assertTrue((CRAFT / ref).resolve().is_file(), ref)

    def test_pointed_to_from_craft(self):
        self.assertIn("`../craft/decks/index.md`", CRAFT_MD.read_text(encoding="utf-8"))

    def test_rule_table_matches_script(self):
        guide = (CRAFT / "build.md").read_text(encoding="utf-8")
        in_guide = set(re.findall(r"^\| `([a-z-]+)` \|", guide, re.M))
        listed = {line.split(" ")[0] for line in run("--rules").stdout.splitlines()}
        self.assertEqual(in_guide, listed)

    def test_no_credentials(self):
        secret = re.compile(r"(api[_-]?key|secret|token)\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}|[\w.+-]+@[\w-]+\.[a-z]{2,}", re.I)
        for path in self.files() + [p for p in DATA.rglob("*") if p.is_file()]:
            with self.subTest(file=path.name):
                self.assertIsNone(secret.search(path.read_text(encoding="utf-8")))


class DeckCheck(unittest.TestCase):
    def test_template_is_clean(self):
        p = run(str(DATA / "template.html"))
        self.assertEqual(p.returncode, 0, p.stdout)
        self.assertIn("no findings", p.stdout)

    def test_messy_deck_flags_every_rule(self):
        p = run(str(DATA / "examples" / "messy-deck.html"), "--max-slides", "5")
        self.assertEqual(p.returncode, 1)
        for rule in (line.split(" ")[0] for line in run("--rules").stdout.splitlines()):
            with self.subTest(rule=rule):
                self.assertIn(" %s [" % rule, p.stdout)

    def test_notes_are_not_counted(self):
        out = json.loads(run(str(DATA / "examples" / "messy-deck.html"), "--json").stdout)
        self.assertEqual(out["slides"], 6)
        words = " ".join(["word"] * 80)
        html = f'<section><h2>A headline that says the point</h2><p>Short.</p><aside class="notes">{words}</aside></section>'
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "deck.html"
            f.write_text(html, encoding="utf-8")
            p = run(str(f), "--only", "too-many-words")
        self.assertEqual(p.returncode, 0, p.stdout)

    def test_only_and_unknown_rule(self):
        deck = str(DATA / "examples" / "messy-deck.html")
        p = run(deck, "--only", "img-no-alt")
        self.assertEqual([l for l in p.stdout.splitlines() if " [" in l and "img-no-alt" not in l], [])
        self.assertEqual(run(deck, "--only", "nope").returncode, 2)

    def test_missing_file(self):
        self.assertEqual(run(str(DATA / "missing.html")).returncode, 2)

    def test_stdlib_only(self):
        src = CHECK.read_text(encoding="utf-8")
        for mod in re.findall(r"^(?:from|import) ([a-z_]+)", src, re.M):
            with self.subTest(module=mod):
                self.assertIn(mod, {"__future__", "argparse", "json", "re", "sys", "html"})
        self.assertNotRegex(src, r"urllib|http\.client|socket|requests")


PLAN = DATA / "deck_plan.py"


def plan(*args):
    return subprocess.run([sys.executable, "-I", str(PLAN), *args], capture_output=True, text=True)


def marked(slides):
    """slides: (beat, layout, body) tuples -> a deck with one headline per slide."""
    out = []
    for i, (beat, layout, body) in enumerate(slides, 1):
        out.append(f'<section class="slide" data-beat="{beat}" data-layout="{layout}">'
                   f'<h2>Slide {i} states its own point plainly</h2><p>{body}</p>'
                   f'<aside class="notes">n</aside></section>')
    return "\n".join(out)


class DeckPlan(unittest.TestCase):
    def check_html(self, html, kind):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "deck.html"
            f.write_text(html, encoding="utf-8")
            p = plan("check", str(f), "--type", kind, "--json")
        return p.returncode, {x["rule"] for x in json.loads(p.stdout)["findings"]}

    def seed(self):
        return [("title", "title", "Example"), ("problem", "statement", "x"), ("solution", "screenshot", "x"),
                ("proof", "big-number", "7%"), ("market", "big-number", "31,000"), ("model", "split", "x"),
                ("competition", "table", "x"), ("go-to-market", "timeline", "x"), ("team", "team", "x"),
                ("ask", "ask", "$2M")]

    def test_self_check(self):
        p = plan("--self-check")
        self.assertEqual(p.returncode, 0, p.stdout)

    def test_example_passes_both_checks(self):
        deck = str(DATA / "examples" / "seed-deck.html")
        self.assertEqual(run(deck, "--type", "seed").returncode, 0)
        p = plan("check", deck, "--type", "seed")
        self.assertEqual(p.returncode, 0, p.stdout)

    def test_clean_seed_passes(self):
        self.assertEqual(self.check_html(marked(self.seed()), "seed"), (0, set()))

    def test_each_structural_rule_fires(self):
        s = self.seed()
        cases = {
            "missing-beat": s[:6] + s[7:],
            "beat-order": [s[0], s[3], s[1], s[2]] + s[4:],
            "ask-not-last": s[:-2] + [s[-1], s[-2]],
            "over-budget": s[:1] + [("problem", "statement", " ".join(["word"] * 20))] + s[2:],
            "same-layout-run": s[:3] + [("proof", "big-number", "1"), ("proof", "big-number", "2")] + s[4:],
            "layout-fit": s[:1] + [("problem", "table", "x")] + s[2:],
            "unknown-layout": s[:1] + [("problem", "hero-banner", "x")] + s[2:],
            "agenda-early": s[:1] + [("agenda", "agenda", "x")] + s[1:],
            "slide-count": s[:1] + s[-1:],
            "no-reset": [s[0]] + [(b, "split", "x") for b in ("problem", "solution", "proof", "market", "model",
                                                             "competition", "go-to-market")] + s[8:],
        }
        for rule, slides in cases.items():
            with self.subTest(rule=rule):
                code, rules = self.check_html(marked(slides), "seed")
                self.assertEqual(code, 1)
                self.assertIn(rule, rules)

    def test_unmarked_deck_is_one_finding(self):
        code, rules = self.check_html("<section><h2>One slide with a point</h2></section>", "demo")
        self.assertEqual(rules, {"unmarked", "slide-count"})

    def test_plan_outputs(self):
        out = json.loads(plan("plan", "seed", "--json").stdout)
        self.assertEqual([s["beat"] for s in out["slides"]][:2], ["title", "problem"])
        self.assertEqual(out["slides"][-1]["layout"], "ask")
        read = json.loads(plan("plan", "seed", "--read", "--json").stdout)
        self.assertGreater(read["slides"][3]["max_words"], out["slides"][3]["max_words"])
        self.assertTrue(read["read_ahead_note"])
        self.assertEqual(plan("plan", "launch", "--html").stdout.count('data-beat="'), 7)
        self.assertEqual(plan("plan", "nope").returncode, 2)
        self.assertEqual(plan("check", "x.html", "--type", "nope").returncode, 2)
        self.assertEqual(plan().returncode, 2)

    def test_type_sets_deck_check_limit(self):
        deck = marked(self.seed())
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "deck.html"
            f.write_text(deck, encoding="utf-8")
            self.assertIn("too-many-slides", run(str(f), "--type", "demo").stdout)
            self.assertEqual(run(str(f), "--type", "seed").returncode, 0)
            self.assertEqual(run(str(f), "--type", "nope").returncode, 2)

    def test_guide_rule_table_matches_script(self):
        guide = (CRAFT / "plan-check.md").read_text(encoding="utf-8")
        in_guide = set(re.findall(r"^\| `([a-z-]+)` \|", guide, re.M))
        src = PLAN.read_text(encoding="utf-8")
        in_script = set(re.findall(r'^    "([a-z-]+)": \("(?:high|medium|low)"', src, re.M))
        self.assertEqual(in_guide, in_script)

    def test_tables_use_known_layouts(self):
        import csv
        with open(DATA / "layouts.csv", encoding="utf-8", newline="") as fh:
            layouts = {r["layout"] for r in csv.DictReader(fh)}
        layouts_md = (CRAFT / "slides.md").read_text(encoding="utf-8").lower()
        for name in layouts - {"agenda", "demo", "appendix"}:
            with self.subTest(layout=name):
                self.assertIn("| " + name.replace("-", " ").replace("before after", "before and after"), layouts_md)


if __name__ == "__main__":
    unittest.main()
