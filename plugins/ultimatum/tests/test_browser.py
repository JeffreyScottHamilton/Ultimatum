"""ult-browser tests: real Playwright run against the ui-app fixture and a deliberately broken page."""
import json
import os
import shutil
import socket
import subprocess
import tempfile
import time
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parent / "scripts" / "ult-browser.mjs"
FIXTURE = HERE.parent.parent.parent / "fixtures" / "ui-app"

BROKEN = """<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"></head>
<body>
<img src="data:image/gif;base64,R0lGODlhAQABAAAAACw=" width="40" height="40">
<button id="x"></button>
<button id="x" style="width:10px;height:10px">y</button>
<div style="width:2000px;height:20px">wide</div>
</body></html>
"""


def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


def run_browser(*args, cwd=None):
    return subprocess.run(["node", str(SCRIPT), *args], capture_output=True, text=True, cwd=cwd, timeout=120)


def playwright_ready():
    if not shutil.which("node"):
        return False
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / "a.html").write_text("<!doctype html><title>a</title><html lang=en><h1>a</h1>")
        r = run_browser((Path(d) / "a.html").as_uri(), "--viewports", "300x300", "--out", d)
        return r.returncode != 3 and "SKIP" not in r.stdout


@unittest.skipUnless(shutil.which("node"), "node not installed")
class BrowserCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not playwright_ready():
            raise unittest.SkipTest("playwright/chromium not available")

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="ult-br-")).resolve()
        self.addCleanup(shutil.rmtree, self.tmp, True)


class TestFixtureApp(BrowserCase):
    def setUp(self):
        super().setUp()
        self.port = free_port()
        self.srv = subprocess.Popen(["python3", str(FIXTURE / "serve.py"), str(self.port)],
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.addCleanup(lambda: (self.srv.terminate(), self.srv.wait()))
        for _ in range(50):
            try:
                socket.create_connection(("127.0.0.1", self.port), 0.2).close()
                break
            except OSError:
                time.sleep(0.1)

    def steps(self, items):
        p = self.tmp / "steps.json"
        p.write_text(json.dumps(items))
        return str(p)

    def test_existing_ui_passes_steps_at_two_viewports(self):
        steps = self.steps([
            {"expect": {"selector": "h1", "visible": True, "text": "Projects"}},
            {"expect": {"selector": ".project-row", "count": 5}},
            {"screenshot": "list"},
        ])
        out = self.tmp / "out"
        r = run_browser(f"http://127.0.0.1:{self.port}/", "--viewports", "375x812,1280x800",
                        "--steps", steps, "--out", str(out))
        self.assertIn(r.returncode, (0,), r.stdout + r.stderr)
        self.assertRegex(r.stdout.strip().splitlines()[-1], r"^ULT-BROWSER: (PASS|WARN) \(")
        rep = json.loads((out / "report.json").read_text())
        self.assertEqual([v["viewport"] for v in rep["viewports"]], ["375x812", "1280x800"])
        self.assertIn(rep["engine"]["axe"]["used"], ("axe-core", "fallback"))
        for v in rep["viewports"]:
            self.assertTrue(all(s["ok"] for s in v["steps"]), v["steps"])
            self.assertEqual(len(v["steps"]), 3)
            self.assertFalse([f for f in v["findings"] if f["severity"] == "fail"], v["findings"])
            for s in v["screenshots"]:
                self.assertGreater((out / s).stat().st_size, 500)

    def test_failed_expect_reports_step_and_exit_1(self):
        steps = self.steps([
            {"expect": {"selector": "h1", "visible": True}},
            {"expect": {"selector": ".project-row", "count": 99}},
        ])
        out = self.tmp / "out"
        r = run_browser(f"http://127.0.0.1:{self.port}/", "--viewports", "375x812", "--steps", steps, "--out", str(out))
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("step 1", r.stdout)
        self.assertIn("count expected 99 got 5", r.stdout)
        self.assertTrue(r.stdout.strip().splitlines()[-1].startswith("ULT-BROWSER: FAIL"))

    def test_stress_flags_overflow(self):
        out = self.tmp / "out"
        r = run_browser(f"http://127.0.0.1:{self.port}/", "--viewports", "375x812", "--stress", "--out", str(out))
        rep = json.loads((out / "report.json").read_text())
        ids = {f["id"] for f in rep["viewports"][0]["findings"]}
        self.assertIn("stress-overflow", ids, r.stdout)


class TestBrokenPage(BrowserCase):
    def test_detects_defects(self):
        page = self.tmp / "broken.html"
        page.write_text(BROKEN)
        out = self.tmp / "out"
        r = run_browser(page.as_uri(), "--viewports", "375x812", "--out", str(out))
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        rep = json.loads((out / "report.json").read_text())
        ids = {f["id"] for f in rep["viewports"][0]["findings"]}
        for want in ("img-alt", "accessible-name", "h-overflow", "lang", "title", "duplicate-id", "tap-target-small"):
            self.assertIn(want, ids, ids)
        self.assertEqual(rep["summary"]["verdict"], "FAIL")
        self.assertTrue(r.stdout.strip().splitlines()[-1].startswith("ULT-BROWSER: FAIL"))

    def test_external_requests_blocked(self):
        page = self.tmp / "ext.html"
        page.write_text('<!doctype html><html lang="en"><title>t</title><h1>t</h1><img alt="" src="http://203.0.113.9/x.png">')
        out = self.tmp / "out"
        run_browser(page.as_uri(), "--viewports", "375x812", "--out", str(out))
        rep = json.loads((out / "report.json").read_text())
        self.assertTrue(rep["viewports"][0]["blocked"])


class TestMissingPlaywright(unittest.TestCase):
    @unittest.skipUnless(shutil.which("node"), "node not installed")
    def test_skip_exit_3(self):
        # Copy the script somewhere with no node_modules and a PATH without npm so resolution fails.
        d = Path(tempfile.mkdtemp(prefix="ult-nopw-"))
        self.addCleanup(shutil.rmtree, d, True)
        s = d / "ult-browser.mjs"
        s.write_text(SCRIPT.read_text())
        node = shutil.which("node")
        bindir = d / "bin"
        bindir.mkdir()
        (bindir / "node").symlink_to(node)
        env = {"PATH": str(bindir)}
        r = subprocess.run([str(bindir / "node"), str(s), "http://127.0.0.1:1/"], capture_output=True, text=True, env=env, cwd=d)
        self.assertEqual(r.returncode, 3, r.stdout + r.stderr)
        self.assertIn("ULT-BROWSER: SKIP playwright not installed", r.stdout)


if __name__ == "__main__":
    unittest.main()
