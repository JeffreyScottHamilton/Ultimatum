import os
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FOLDER = os.path.join(ROOT, "skills", "work", "references", "craft", "react-performance")
SCAN = os.path.join(ROOT, "data", "craft", "react-performance", "react_scan.py")
EX = os.path.join(ROOT, "data", "craft", "react-performance", "examples")


def run(*args):
    return subprocess.run([sys.executable, SCAN, *args], capture_output=True, text=True)


class CraftReactPerformance(unittest.TestCase):
    def test_files_listed_and_shaped(self):
        index = open(os.path.join(FOLDER, "index.md"), encoding="utf-8").read()
        for name in sorted(os.listdir(FOLDER)):
            path = os.path.join(FOLDER, name)
            text = open(path, encoding="utf-8").read()
            lines = text.splitlines()
            self.assertTrue(lines[0].startswith("# "), name)
            self.assertTrue(lines[2].startswith("Read "), name)
            self.assertLess(os.path.getsize(path), 15000, name)
            if name not in ("index.md", "later.md"):
                self.assertIn("`%s`" % name, index, name)

    def test_no_licence_text_claimed(self):
        index = open(os.path.join(FOLDER, "index.md"), encoding="utf-8").read()
        self.assertIn("no LICENSE file", index)
        self.assertIn("none of its text", index)

    def test_react_md_points_here(self):
        react = open(os.path.join(ROOT, "skills", "work", "references", "react.md"), encoding="utf-8").read()
        self.assertIn("craft/react-performance/", react)

    def test_rule_table_matches_scanner(self):
        guide = open(os.path.join(FOLDER, "react-scan.md"), encoding="utf-8").read()
        out = run("--rules").stdout
        rules = [ln.split(":", 1)[0] for ln in out.splitlines() if ln]
        self.assertGreaterEqual(len(rules), 10)
        for r in rules:
            self.assertIn("`%s`" % r, guide, r)


class ReactScan(unittest.TestCase):
    def test_bad_examples_flag_every_rule(self):
        p = run(EX + "/page.tsx", EX + "/loader.ts")
        self.assertEqual(p.returncode, 1, p.stdout)
        rules = run("--rules").stdout
        for line in rules.splitlines():
            rule = line.split(":", 1)[0]
            self.assertIn(" %s:" % rule, p.stdout, rule)

    def test_dependent_await_not_flagged(self):
        p = run(EX + "/loader.ts", "--only", "serial-await")
        hits = [ln for ln in p.stdout.splitlines() if "serial-await" in ln]
        self.assertEqual(len(hits), 1, p.stdout)
        self.assertIn("loader.ts:3 ", hits[0])

    def test_clean_file_passes(self):
        p = run(EX + "/clean.tsx")
        self.assertEqual(p.returncode, 0, p.stdout)
        self.assertIn("no findings", p.stdout)

    def test_unknown_rule(self):
        self.assertEqual(run(EX, "--only", "nope").returncode, 2)

    def test_skips_node_modules(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            nm = os.path.join(d, "node_modules", "x")
            os.makedirs(nm)
            with open(os.path.join(nm, "a.tsx"), "w") as fh:
                fh.write("items.map((it, i) => <li key={i} />)\n")
            self.assertEqual(run(d).returncode, 0)


if __name__ == "__main__":
    unittest.main()
