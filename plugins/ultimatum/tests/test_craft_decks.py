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


if __name__ == "__main__":
    unittest.main()
