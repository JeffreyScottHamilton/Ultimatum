"""Launch-load and real-world-condition guides for apps: shape, wiring, and the worked example runs."""
from __future__ import annotations

import re
import shutil
import subprocess
import unittest
from pathlib import Path

from _harness import WEB_REFS

APP = WEB_REFS / "app"
DATA = Path(__file__).resolve().parents[1] / "data" / "app"
GUIDES = {"launch-load.md": 20, "field-conditions.md": 11}


def numbered(text: str) -> list[int]:
    return [int(n) for n in re.findall(r"^(\d+)\. \*\*", text, re.M)]


class LaunchGuides(unittest.TestCase):
    def test_shape(self):
        for name, count in GUIDES.items():
            with self.subTest(name=name):
                p = APP / name
                lines = p.read_text(encoding="utf-8").splitlines()
                self.assertLess(p.stat().st_size, 15_000)
                self.assertTrue(lines[0].startswith("# "))
                self.assertTrue(lines[2].startswith("Read "))
                self.assertEqual(numbered(p.read_text(encoding="utf-8")), list(range(1, count + 1)))

    def test_wired_into_the_app_checklist(self):
        text = (APP / "checklist.md").read_text(encoding="utf-8")
        for name in GUIDES:
            self.assertIn(f"`{name}`", text)

    def test_referenced_guides_and_files_exist(self):
        for name in GUIDES:
            text = (APP / name).read_text(encoding="utf-8")
            for ref in set(re.findall(r"`([\w-]+\.md)`", text)):
                self.assertTrue((APP / ref).is_file(), f"{name} -> {ref}")
        for f in ("field-demo.html", "field-check.cjs"):
            self.assertTrue((DATA / f).is_file(), f)

    def test_load_test_and_spend_rules_kept(self):
        text = (APP / "launch-load.md").read_text(encoding="utf-8")
        self.assertIn("on staging", text)
        self.assertIn("owner's yes", text)
        self.assertIn("pauses", text)

    @unittest.skipUnless(shutil.which("node"), "node not installed")
    def test_worked_example_passes(self):
        probe = subprocess.run(["node", "-e", "require('playwright')"], capture_output=True, cwd=DATA)
        if probe.returncode:
            self.skipTest("playwright not available")
        p = subprocess.run(["node", "field-check.cjs"], capture_output=True, text=True, cwd=DATA, timeout=240)
        self.assertEqual(p.returncode, 0, p.stdout[-2000:] + p.stderr[-1000:])
        self.assertEqual(p.stdout.count("\nok") + p.stdout.startswith("ok"), 12, p.stdout)


if __name__ == "__main__":
    unittest.main()
