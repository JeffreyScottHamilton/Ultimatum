"""Checks for the identity icons and banners guides and the icon checker."""
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

P = Path(__file__).resolve().parents[1]
CRAFT = P / "skills" / "website" / "references" / "craft" / "identity"
DATA = P / "data" / "craft" / "identity"
CHECK = DATA / "icon_check.py"
GOOD = DATA / "examples" / "good"
MESSY = DATA / "examples" / "messy"
TICKED = re.compile(r"`((?:\.\./)+[A-Za-z0-9_./-]+\.(?:md|py|json)|[a-z0-9-]+\.md)`")
NEW = ("icons.md", "banners.md")


def run(*args):
    return subprocess.run([sys.executable, str(CHECK), *args], capture_output=True, text=True)


class IconsAndBannersGuides(unittest.TestCase):
    def test_shape(self):
        for name in NEW:
            path = CRAFT / name
            lines = path.read_text(encoding="utf-8").splitlines()
            with self.subTest(file=name):
                self.assertLessEqual(path.stat().st_size, 15 * 1024)
                self.assertTrue(lines[0].startswith("# "))
                self.assertTrue(lines[2].startswith("Read "))

    def test_listed_in_index(self):
        index = (CRAFT / "index.md").read_text(encoding="utf-8")
        for name in NEW:
            self.assertIn(f"`{name}`", index)

    def test_references_resolve(self):
        for name in NEW:
            text = (CRAFT / name).read_text(encoding="utf-8")
            for ref in TICKED.findall(text):
                with self.subTest(file=name, ref=ref):
                    self.assertTrue((CRAFT / ref).resolve().is_file(), ref)

    def test_script_path_in_guide_resolves(self):
        text = (CRAFT / "icons.md").read_text(encoding="utf-8")
        m = re.search(r"python3 (\S+icon_check\.py)", text)
        self.assertIsNotNone(m)
        self.assertEqual((CRAFT / m.group(1)).resolve(), CHECK.resolve())

    def test_rule_table_matches_script(self):
        guide = (CRAFT / "icons.md").read_text(encoding="utf-8")
        in_guide = set(re.findall(r"^\| `([a-z-]+)` \|", guide, re.M))
        listed = {line.split(" ")[0] for line in run("--rules").stdout.splitlines()}
        self.assertEqual(in_guide, listed)

    def test_banners_dated_and_say_check(self):
        text = (CRAFT / "banners.md").read_text(encoding="utf-8")
        self.assertIn("2026", text)
        self.assertIn("help page", text)

    def test_no_credentials(self):
        secret = re.compile(r"(api[_-]?key|secret|token)\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}|[\w.+-]+@[\w-]+\.[a-z]{2,}", re.I)
        files = [CRAFT / n for n in NEW] + [p for p in DATA.rglob("*") if p.is_file()]
        for path in files:
            with self.subTest(file=path.name):
                self.assertIsNone(secret.search(path.read_text(encoding="utf-8")))


class IconCheck(unittest.TestCase):
    def test_good_set_is_clean(self):
        r = run(str(GOOD))
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_messy_set_hits_every_rule(self):
        r = run(str(MESSY), "--json")
        self.assertEqual(r.returncode, 1)
        data = json.loads(r.stdout)
        hit = {f["rule"] for f in data["findings"]}
        listed = {line.split(" ")[0] for line in run("--rules").stdout.splitlines()}
        self.assertEqual(hit, listed)

    def test_relative_path_inside_canvas(self):
        with tempfile.TemporaryDirectory() as d:
            Path(d, "ok.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" '
                                         'fill="none" stroke="currentColor"><path d="M20 4l-16 16h10v-6"/></svg>')
            self.assertEqual(run(d).returncode, 0)

    def test_size_flag(self):
        r = run(str(MESSY / "wrong-size.svg"), "--size", "32", "--only", "wrong-size")
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_entities_refused(self):
        with tempfile.TemporaryDirectory() as d:
            Path(d, "x.svg").write_text('<!DOCTYPE svg [<!ENTITY a "b">]><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">&a;</svg>')
            r = run(d, "--json")
            self.assertEqual(r.returncode, 1)
            self.assertIn("parse", {f["rule"] for f in json.loads(r.stdout)["findings"]})

    def test_bad_arguments(self):
        self.assertEqual(run().returncode, 2)
        self.assertEqual(run(str(GOOD), "--only", "nope").returncode, 2)
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(run(d).returncode, 2)

    def test_stdlib_only(self):
        text = CHECK.read_text(encoding="utf-8")
        mods = set(re.findall(r"^(?:import|from) ([a-z_]+)", text, re.M))
        self.assertLessEqual(mods, {"__future__", "argparse", "json", "re", "sys", "xml", "collections", "pathlib"})
        self.assertNotRegex(text, r"urllib|socket|http\.client|subprocess")


if __name__ == "__main__":
    unittest.main()
