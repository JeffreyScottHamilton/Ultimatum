import csv
import os
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "craft", "design-review-qa")
LINT = os.path.join(DATA, "page_lint.py")
GUIDE = os.path.join(ROOT, "skills", "website", "references", "craft", "design-review-qa", "page-lint.md")


def run(*args):
    return subprocess.run([sys.executable, LINT, *args], capture_output=True, text=True)


def rules():
    return [ln.split(":", 1)[0] for ln in run("--rules").stdout.splitlines() if ln]


class PageLint(unittest.TestCase):
    def test_sloppy_pages_flag_every_rule(self):
        ex = os.path.join(DATA, "examples")
        p = run(*[os.path.join(ex, n) for n in sorted(os.listdir(ex)) if n.startswith("sloppy") and not n.endswith(".css")])
        self.assertEqual(p.returncode, 1)
        for r in rules():
            self.assertIn(" %s [" % r, p.stdout, r)

    def test_clean_page_passes(self):
        p = run(os.path.join(DATA, "examples", "clean.html"))
        self.assertEqual(p.returncode, 0, p.stdout)
        self.assertIn("no findings", p.stdout)

    def test_remote_stylesheet_never_read(self):
        with tempfile.TemporaryDirectory() as d:
            page = os.path.join(d, "a.html")
            with open(page, "w") as fh:
                fh.write('<link rel="stylesheet" href="https://example.invalid/x.css"><h1>Bike repairs in Leeds</h1>')
            p = run(page)
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)

    def test_token_block_black_is_allowed(self):
        with tempfile.TemporaryDirectory() as d:
            css = os.path.join(d, "a.css")
            with open(css, "w") as fh:
                fh.write(":root { --ink: #000; }\n.x { color: var(--ink); }\n")
            self.assertEqual(run(css, "--only", "pure-black-white").returncode, 0)

    def test_unknown_rule(self):
        self.assertEqual(run(DATA, "--only", "nope").returncode, 2)

    def test_json(self):
        import json
        p = run(os.path.join(DATA, "examples", "sloppy.html"), "--json", "--only", "placeholder")
        rows = json.loads(p.stdout)
        self.assertTrue(rows and all(r["rule"] == "placeholder" for r in rows))

    def test_component_file_reads_tailwind(self):
        p = run(os.path.join(DATA, "examples", "sloppy-component.tsx"))
        for r in ("purple-gradient", "gradient-text", "hero-vh", "focus-removed", "two-icon-libraries", "double-sticky"):
            self.assertIn(" %s [" % r, p.stdout, r)

    def _page(self, d, body):
        page = os.path.join(d, "a.html")
        with open(page, "w") as fh:
            fh.write(body)
        return page

    def test_waiver_with_reason(self):
        with tempfile.TemporaryDirectory() as d:
            page = self._page(d, "<!-- page-lint: allow placeholder: demo fixture for a talk -->\n<p>Lorem ipsum</p>")
            self.assertEqual(run(page).returncode, 0, run(page).stdout)

    def test_waiver_without_reason_waives_nothing(self):
        with tempfile.TemporaryDirectory() as d:
            page = self._page(d, "<!-- page-lint: allow placeholder -->\n<p>Lorem ipsum</p>")
            out = run(page).stdout
            self.assertIn(" placeholder [", out)
            self.assertIn(" waiver-no-reason [", out)

    def test_genre_exempts(self):
        css = os.path.join(DATA, "examples", "sloppy.css")
        self.assertIn(" frosted-glass [", run(css).stdout)
        self.assertNotIn(" frosted-glass [", run(css, "--genre", "atmospheric").stdout)

    def test_github_format(self):
        p = run(os.path.join(DATA, "examples", "sloppy.html"), "--format", "github", "--only", "placeholder")
        self.assertTrue(p.stdout.startswith("::error file="), p.stdout)

    def test_contrast(self):
        with tempfile.TemporaryDirectory() as d:
            bad = self._page(d, "<style>.n { color: #9a9a9a; background: #ffffff; }</style><p class=n>Open daily</p>")
            self.assertIn(" low-contrast [", run(bad, "--only", "low-contrast").stdout)
            ok = os.path.join(d, "b.html")
            with open(ok, "w") as fh:
                fh.write("<style>.n { color: #1a1a1a; background: #ffffff; }</style><p class=n>Open daily</p>")
            self.assertEqual(run(ok, "--only", "low-contrast").returncode, 0)


class PageLintGuide(unittest.TestCase):
    def test_guide_lists_every_rule(self):
        text = open(GUIDE, encoding="utf-8").read()
        for r in rules():
            self.assertIn("`%s`" % r, text, r)

    def test_tell_ids_exist(self):
        with open(os.path.join(DATA, "slop-tells.csv"), encoding="utf-8") as fh:
            ids = {row["id"] for row in csv.DictReader(fh)}
        text = open(GUIDE, encoding="utf-8").read()
        table = text.split("## What it checks", 1)[1].split("## What it cannot see", 1)[0]
        named = set(re.findall(r"`([a-z][a-z-]+)`", table)) - set(rules())
        self.assertTrue(named)
        self.assertEqual(named - ids, set())

    def test_linked_from_review_index(self):
        idx = open(os.path.join(os.path.dirname(GUIDE), "index.md"), encoding="utf-8").read()
        self.assertIn("`page-lint.md`", idx)


if __name__ == "__main__":
    unittest.main()
