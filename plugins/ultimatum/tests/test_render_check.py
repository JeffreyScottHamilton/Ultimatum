import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "craft", "design-review-qa")
CHECK = os.path.join(DATA, "render_check.py")
EX = os.path.join(DATA, "examples")
GUIDE = os.path.join(ROOT, "skills", "website", "references", "craft", "design-review-qa", "render-check.md")


def run(*args):
    return subprocess.run([sys.executable, CHECK, *args], capture_output=True, text=True, timeout=300)


def rules():
    return [ln.split()[0] for ln in run("--rules").stdout.splitlines() if ln.strip()]


class RenderCheckOffline(unittest.TestCase):
    """Parts that need no browser."""

    def test_remote_url_refused(self):
        p = run("http://example.com/")
        self.assertEqual(p.returncode, 2, p.stdout + p.stderr)
        self.assertIn("not a local address", p.stdout + p.stderr)

    def test_missing_file_is_bad_argument(self):
        p = run(os.path.join(EX, "no-such-page.html"))
        self.assertEqual(p.returncode, 2)

    def test_guide_lists_every_rule(self):
        with open(GUIDE, encoding="utf-8") as fh:
            text = fh.read()
        for r in rules():
            self.assertIn("`%s`" % r, text, r)
        self.assertLess(len(text.encode()), 15000)


class RenderCheckBrowser(unittest.TestCase):
    """Parts that open pages in Chromium; skipped when no browser is found."""

    @classmethod
    def setUpClass(cls):
        p = run(os.path.join(EX, "render-clean.html"))
        if p.returncode == 3:
            raise unittest.SkipTest("no browser: " + p.stdout.strip())
        cls.clean = p

    def test_clean_page_passes(self):
        self.assertEqual(self.clean.returncode, 0, self.clean.stdout)
        self.assertIn("no findings", self.clean.stdout)

    def test_sloppy_pages_cover_every_rule(self):
        p = run(os.path.join(EX, "render-sloppy.html"), os.path.join(EX, "render-sloppy-2.html"), "--json")
        self.assertEqual(p.returncode, 1, p.stderr)
        seen = {r["rule"] for r in json.loads(p.stdout)}
        self.assertEqual(set(rules()) - seen, set())

    def test_waiver_with_reason_silences_rule(self):
        body = '<p style="font-size:9px;line-height:1.5">Small print that is far too small to read.</p>'
        with tempfile.TemporaryDirectory() as d:
            bare = os.path.join(d, "a.html")
            waived = os.path.join(d, "b.html")
            with open(bare, "w") as fh:
                fh.write(body)
            with open(waived, "w") as fh:
                fh.write("<!-- render-check: allow tiny-text: legal footnote sized by the client -->" + body)
            a = run(bare, "--only", "tiny-text", "--widths", "1440")
            b = run(waived, "--only", "tiny-text", "--widths", "1440")
        self.assertEqual(a.returncode, 1, a.stdout)
        self.assertEqual(b.returncode, 0, b.stdout)

    def test_github_format(self):
        p = run(os.path.join(EX, "render-sloppy.html"), "--only", "tiny-text", "--format", "github")
        self.assertTrue(p.stdout.startswith("::warning file=") or p.stdout.startswith("::error file="), p.stdout)


if __name__ == "__main__":
    unittest.main()
