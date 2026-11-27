"""`ult audit start|finish`: mechanical audit steps, state-dir only."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from _harness import UltCase


class AuditCase(UltCase):
    def setUp(self):
        super().setUp()
        self.state = Path(tempfile.mkdtemp(prefix="ult-state-")).resolve()
        self.addCleanup(__import__("shutil").rmtree, self.state, True)
        self.write("app.py", "print('hi')\n")

    def env(self):
        e = super().env()
        e["ULTIMATUM_STATE_DIR"] = str(self.state)
        e["PATH"] = "/usr/bin:/bin"  # no optional scanners
        return e

    def snapshot(self):
        return sorted(str(p.relative_to(self.root)) for p in self.root.rglob("*"))

    def test_start_creates_ledger_and_skeleton_and_names_missing_scanners(self):
        before = self.snapshot()
        r = self.ult("audit", "start", "--scope", "demo repo")
        self.assertEqual(r.code, 0, r.all)
        self.assertLessEqual(len(r.out.strip().splitlines()), 8)
        sec = self.state / "security"
        self.assertTrue((sec / "ledger.json").is_file())
        data = json.loads((sec / "findings.json").read_text())
        self.assertEqual(data["findings"], [])
        self.assertEqual(data["scope"], "demo repo")
        for s in ("semgrep", "gitleaks", "osv-scanner", "dependency advisories: not checked",
                  "git history secrets: NOT checked"):
            self.assertIn(s, data["tools"])
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(self.ult("audit", "start").code, 0)  # idempotent
        self.assertIn("kept", self.ult("audit", "start").out)

    def test_finish_fails_on_invalid_finding_then_passes(self):
        self.ult("audit", "start")
        fp = self.state / "security" / "findings.json"
        data = json.loads(fp.read_text())
        data["findings"] = [{"id": "F-001", "title": "x", "status": "confirmed", "file": "app.py", "boundary": "b"}]
        fp.write_text(json.dumps(data))
        r = self.ult("audit", "finish")
        self.assertEqual(r.code, 1, r.all)
        self.assertIn("confirmed finding needs 'entry_point'", r.out)
        fp.write_text(json.dumps({**data, "findings": []}))
        good = {"title": "Missing check", "file": "app.py", "line": 1, "boundary": "http",
                "missing_evidence": "need to see the caller"}
        self.assertEqual(self.ult("findings", "add", input=json.dumps(good)).code, 0)
        r = self.ult("audit", "finish")
        self.assertEqual(r.code, 0, r.all)
        self.assertLessEqual(len(r.out.strip().splitlines()), 6)
        report = (self.state / "security" / "report.md").read_text()
        self.assertIn("dependency advisories: not checked", report)
        self.assertIn("NOT run", report)
        self.assertFalse((self.root / ".ultimatum").exists())

    def test_finish_without_start_fails(self):
        self.assertEqual(self.ult("audit", "finish").code, 1)


if __name__ == "__main__":
    unittest.main()
