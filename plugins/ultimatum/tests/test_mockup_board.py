"""Tests for the mockup comparison board (design review Step 0.5, built not generated)."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "craft" / "design-review-qa"
TOOL = DATA / "mockup_board.py"
GUIDE = ROOT / "skills" / "website" / "references" / "craft" / "design-review-qa" / "mockup-step.md"
sys.dont_write_bytecode = True  # keep caches out of the data folder its scans read
sys.path.insert(0, str(DATA))

import mockup_board as M  # noqa: E402

CALM = ('<!doctype html><title>Calm</title><meta name="variant-axis" content="quiet, outlines">'
        '<style>body{font:16px serif;padding:40px}</style><h1>Plans</h1><p>Starter 9, Team 29</p>')
DENSE = ('<!doctype html><title>Dense</title><style>td{padding:4px;border:1px solid}</style>'
         '<table><tr><td>Starter</td><td>9</td><td>3 seats</td></tr></table>')


def run(*args):
    return subprocess.run([sys.executable, str(TOOL), *args], capture_output=True, text=True, timeout=120)


class Board(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = Path(self.tmp.name)
        (self.d / "calm.html").write_text(CALM)
        (self.d / "dense.html").write_text(DENSE)

    def tearDown(self):
        self.tmp.cleanup()

    def build(self, *extra):
        return run("build", str(self.d / "calm.html"), str(self.d / "dense.html"), "--brief", "pricing </script>",
                   "--out", str(self.d / "out"), *extra)

    def test_build_writes_board_and_manifest(self):
        p = self.build("--axis", "dense=a table, all at once")
        self.assertEqual(p.returncode, 0, p.stderr)
        board = json.loads((self.d / "out" / "board.json").read_text())
        self.assertEqual([v["id"] for v in board["variants"]], ["calm", "dense"])
        self.assertEqual(board["variants"][0]["axis"], "quiet, outlines")  # from the meta tag
        self.assertEqual(board["warnings"], [])
        html = (self.d / "out" / "board.html").read_text()
        self.assertIn('src="variants/calm.html"', html)
        self.assertIn('name=pick value=\'dense\'', html)
        self.assertNotIn("pricing </script>", html)  # brief is escaped
        self.assertTrue((self.d / "out" / "variants" / "dense.html").is_file())

    def test_warns_on_missing_axis_and_near_copy(self):
        (self.d / "calm2.html").write_text(CALM.replace("<h1>Plans", "<h1>Our plans"))
        p = run("build", str(self.d / "calm.html"), str(self.d / "dense.html"), str(self.d / "calm2.html"),
                "--brief", "x", "--out", str(self.d / "out"))
        self.assertEqual(p.returncode, 0)
        self.assertIn("dense: no axis", p.stdout)
        self.assertIn("calm and calm2 are", p.stdout)
        self.assertIn("name the same axis", p.stdout)

    def test_similarity_separates_directions(self):
        long = CALM.replace("<p>", "<p>" + "Every plan has unlimited orders and a free month. " * 6)
        self.assertGreater(M.similarity(long, long.replace("Team 29", "Team 32")), M.NEAR_COPY)
        self.assertLess(M.similarity(CALM, DENSE), 0.6)

    def test_baseline_is_now(self):
        p = run("build", str(self.d / "dense.html"), "--baseline", str(self.d / "calm.html"),
                "--brief", "ideal hierarchy", "--out", str(self.d / "out"))
        self.assertEqual(p.returncode, 0, p.stderr)
        ids = [v["id"] for v in json.loads((self.d / "out" / "board.json").read_text())["variants"]]
        self.assertEqual(ids, ["now", "dense"])

    def test_bad_input(self):
        self.assertEqual(run("build", str(self.d / "calm.html"), "--brief", "x", "--out", str(self.d / "o")).returncode, 2)
        self.assertEqual(run("build", str(self.d / "nope.html"), str(self.d / "calm.html"), "--brief", "x",
                             "--out", str(self.d / "o")).returncode, 2)
        self.assertEqual(self.build("--axis", "dense").returncode, 2)

    def test_read_pick_none_and_wrong_board(self):
        self.build()
        out = self.d / "out"
        bid = json.loads((out / "board.json").read_text())["id"]
        fb = out / "feedback.json"
        fb.write_text(json.dumps({"board": bid, "pick": "dense", "overall": "go",
                                  "variants": {"dense": {"rating": 4, "comment": "clear"}, "calm": {"rating": 9}}}))
        p = run("read", str(fb))
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("pick: dense", p.stdout)
        self.assertIn("4/5", p.stdout)
        self.assertIn("calm             -/5", p.stdout)  # out-of-range rating is ignored
        fb.write_text(json.dumps({"board": bid, "pick": None, "variants": {}}))
        self.assertEqual(run("read", str(fb)).returncode, 4)
        fb.write_text(json.dumps({"board": bid, "pick": "rm -rf", "variants": {}}))
        self.assertEqual(run("read", str(fb)).returncode, 2)
        fb.write_text(json.dumps({"board": "other", "pick": "dense"}))
        self.assertEqual(run("read", str(fb)).returncode, 2)
        fb.write_text("{not json")
        self.assertEqual(run("read", str(fb)).returncode, 2)

    def test_board_round_trip_in_browser(self):
        try:
            from render_check import launch
        except ImportError:
            self.skipTest("render_check not importable")
        pw, browser, why = launch()
        if not browser:
            self.skipTest("no browser: " + why)
        try:
            self.assertEqual(self.build().returncode, 0)
            out = self.d / "out"
            page = browser.new_page(accept_downloads=True, viewport={"width": 390, "height": 800})
            errors = []
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.goto((out / "board.html").as_uri())
            self.assertLessEqual(page.evaluate("document.documentElement.scrollWidth"), 390)
            page.check("input[name=rate-calm][value='5']")
            page.check("input[name=pick][value=calm]")
            page.fill("#c-calm", "calmer")
            with page.expect_download() as dl:
                page.click("#save")
            dl.value.save_as(str(out / "feedback.json"))
            self.assertEqual(errors, [])
        finally:
            browser.close()
            pw.stop()
        p = run("read", str(out / "feedback.json"))
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("pick: calm", p.stdout)
        self.assertIn("calmer", p.stdout)

    def test_guide_names_the_commands(self):
        text = GUIDE.read_text()
        for word in ("mockup_board.py build", "mockup_board.py read", "--baseline", "--shots", "variant-axis"):
            self.assertIn(word, text)


if __name__ == "__main__":
    unittest.main()
