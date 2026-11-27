"""Checks for deck_build.py: content file to checked HTML deck."""
from __future__ import annotations

import ast
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data" / "craft" / "decks"
BUILD = DATA / "deck_build.py"
sys.path.insert(0, str(DATA))
sys.dont_write_bytecode = True
import deck_build  # noqa: E402


def run(*args):
    return subprocess.run([sys.executable, str(BUILD), *args], capture_output=True, text=True)


def good_deck():
    return {"title": "Q3 update", "slides": [
        {"beat": "title", "layout": "title", "headline": "Q3: repeat orders up, costs flat",
         "text": "Ops team, October", "notes": "Thank them."},
        {"beat": "headline-number", "layout": "big-number", "headline": "Repeat orders rose a third this quarter",
         "big": "+34%", "text": "From 410 to 549 repeat orders", "source": "Source: order system, Q2 vs Q3"},
        {"beat": "ask", "layout": "ask", "headline": "Approve two more drivers by Friday",
         "big": "2 drivers", "lines": ["Covers the evening peak", "Pays back in five months"]},
    ]}


class Build(unittest.TestCase):
    template = (DATA / "template.html").read_text(encoding="utf-8")

    def test_self_check(self):
        self.assertEqual(deck_build.self_check(), [])

    def test_renders_layouts_and_keeps_frame(self):
        html = deck_build.render(good_deck(), self.template)
        self.assertEqual(html.count('<section class="slide'), 3)
        self.assertIn("<title>Q3 update</title>", html)
        self.assertIn('data-layout="big-number"', html)
        self.assertIn('<aside class="notes">Thank them.</aside>', html)
        self.assertIn("addEventListener", html)  # template's key and fit script kept

    def test_escapes_text(self):
        d = good_deck()
        d["slides"][0]["headline"] = '<script>alert(1)</script> & "x"'
        html = deck_build.render(d, self.template)
        self.assertNotIn("<script>alert", html)
        self.assertIn("&lt;script&gt;", html)

    def test_refuses_bad_content(self):
        bad = [
            {"slides": []},
            {"slides": [{"beat": "a", "layout": "nope", "headline": "x"}]},
            {"slides": [{"beat": "a", "layout": "full-image", "headline": "x", "image": "a.jpg"}]},
            {"slides": [{"beat": "a", "layout": "full-image", "headline": "x", "image": "javascript:x", "alt": "a"}]},
            {"slides": [{"beat": "a", "layout": "quote", "headline": "x", "quote": "y"}]},
            {"theme": {"ink": "#dddddd"}, "slides": [{"beat": "a", "layout": "title", "headline": "x"}]},
            {"theme": {"display": "x;}</style><script>"}, "slides": [{"beat": "a", "layout": "title", "headline": "x"}]},
            {"theme": {"shadow": "#000000"}, "slides": [{"beat": "a", "layout": "title", "headline": "x"}]},
        ]
        for c in bad:
            with self.assertRaises(deck_build.ContentError, msg=json.dumps(c)):
                deck_build.render(c, self.template)

    def test_theme_applied(self):
        d = good_deck()
        d["theme"] = {"accent": "#1d4ed8", "display": "Georgia, serif"}
        html = deck_build.render(d, self.template)
        self.assertIn("--accent: #1d4ed8", html)

    def test_cli(self):
        with tempfile.TemporaryDirectory() as t:
            src, out = Path(t, "d.json"), Path(t, "d.html")
            src.write_text(json.dumps(good_deck()))
            r = run("build", str(src), "-o", str(out))
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertTrue(out.is_file())
            d = good_deck()
            d["slides"][1]["headline"] = "Numbers"  # a label, not a sentence
            d["slides"][2]["lines"] = ["word " * 60]
            src.write_text(json.dumps(d))
            r = run("build", str(src), "-o", str(out))
            self.assertEqual(r.returncode, 1, r.stdout)
            src.write_text("{broken")
            self.assertEqual(run("build", str(src), "-o", str(out)).returncode, 2)
        r = run("starter", "seed")
        self.assertEqual(r.returncode, 0)
        self.assertTrue(json.loads(r.stdout)["slides"])
        self.assertEqual(run("starter", "nope").returncode, 2)
        self.assertEqual(run("fields").returncode, 0)

    def test_stdlib_only(self):
        tree = ast.parse(BUILD.read_text(encoding="utf-8"))
        allowed = {"__future__", "html", "json", "re", "sys", "pathlib", "deck_check", "deck_plan"}
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for a in node.names:
                    self.assertIn(a.name.split(".")[0], allowed)
            elif isinstance(node, ast.ImportFrom):
                self.assertIn(node.module.split(".")[0], allowed)


if __name__ == "__main__":
    unittest.main()
