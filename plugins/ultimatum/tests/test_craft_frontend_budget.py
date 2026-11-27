"""Checks for the frontend-budget craft references (skills/work/references/craft/frontend-budget)."""
from __future__ import annotations

from pathlib import Path
import os
import re
import subprocess
import sys
import unittest

P = Path(__file__).resolve().parents[1]
CRAFT = P / "skills" / "work" / "references" / "craft" / "frontend-budget"
DATA = P / "data" / "craft" / "frontend-budget"
REPO = P.parents[1]
SOURCE = Path(os.environ.get("ULT_FRONTEND_BUDGET_SRC", "/tmp/src/frontend-budget"))

URL = re.compile(r"\bhttps?://[^\s)`>\]|]+")
TICKED = re.compile(r"`([A-Za-z0-9_./-]+\.(?:md|csv|py|js))`(?:[ \t]*§[ \t]*([A-Z0-9][^`|)\n]*))?")


def _md() -> list[Path]:
    return sorted(CRAFT.glob("*.md"))


def _data() -> list[Path]:
    return sorted(f for f in DATA.rglob("*") if f.is_file() and "__pycache__" not in f.parts) if DATA.is_dir() else []


def _headings(path: Path) -> set[str]:
    return {m.group(1).strip() for m in re.finditer(r"^#{2,4}\s+(.+)$", path.read_text(encoding="utf-8"), re.M)}


class CraftFrontendBudget(unittest.TestCase):
    def test_index_lists_every_file_and_each_exists(self):
        index = (CRAFT / "index.md").read_text(encoding="utf-8")
        listed = set(re.findall(r"^- `([a-z0-9-]+\.md)`:", index, re.M))
        self.assertTrue(listed)
        on_disk = {p.name for p in _md()} - {"index.md", "later.md"}
        self.assertEqual(on_disk, listed, "index.md must list every craft file once")
        self.assertTrue((CRAFT / "later.md").is_file())

    def test_files_are_small_and_open_with_when_to_read(self):
        for path in _md():
            lines = path.read_bytes().decode("utf-8").split("\n")
            with self.subTest(file=path.name):
                self.assertLessEqual(path.stat().st_size, 15 * 1024)
                self.assertTrue(lines[0].startswith("# "))
                self.assertTrue(lines[2].startswith("Read "), "line 3 says when to read the file")

    def test_links_are_https(self):
        for path in _md() + [f for f in _data() if f.suffix in {".md", ".py", ".js", ".html"}]:
            for url in URL.findall(path.read_text(encoding="utf-8")):
                with self.subTest(file=path.name, url=url):
                    local = re.match(r"http://(localhost|127\.0\.0\.1)[:/]", url)
                    self.assertTrue(url.startswith("https://") or local, "use https, or a local dev URL")

    def test_relative_references_resolve(self):
        for path in _md():
            text = path.read_text(encoding="utf-8")
            for ref, section in TICKED.findall(text):
                target = (path.parent / ref).resolve()
                if "/" not in ref and not target.exists():
                    continue  # a bare file name in prose
                with self.subTest(file=path.name, ref=ref):
                    self.assertTrue(target.exists(), f"{ref} not found")
                if section and target.suffix == ".md" and target.exists():
                    with self.subTest(file=path.name, ref=ref, section=section):
                        heads = _headings(target)
                        self.assertTrue(any(section.startswith(h) or h.startswith(section.strip()) for h in heads),
                                        f"{ref} has no heading at the start of: {section.strip()}")

    def test_no_credentials(self):
        secret = re.compile(r"(api[_-]?key|secret|token)\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}|[\w.+-]+@[\w-]+\.[a-z]{2,}", re.I)
        for path in _md() + _data():
            with self.subTest(file=path.name):
                self.assertIsNone(secret.search(path.read_text(encoding="utf-8", errors="replace")))

    def test_data_scripts_are_stdlib_only(self):
        allowed = set(sys.stdlib_module_names)
        for path in [f for f in _data() if f.suffix == ".py"]:
            for mod in re.findall(r"^\s*(?:from|import)\s+([A-Za-z_][\w]*)", path.read_text(encoding="utf-8"), re.M):
                with self.subTest(file=path.name, module=mod):
                    self.assertIn(mod, allowed | {"__future__"})

    @unittest.skipUnless(SOURCE.is_dir(), "source checkout not present (set ULT_FRONTEND_BUDGET_SRC)")
    def test_copy_check_passes(self):
        res = subprocess.run([sys.executable, str(REPO / "tools" / "copy_check.py"), str(CRAFT), str(SOURCE)],
                             capture_output=True, text=True, timeout=600)
        self.assertEqual(res.returncode, 0, res.stdout[-2000:])


class Scripts(unittest.TestCase):
    def run_script(self, *args):
        return subprocess.run([sys.executable, "-I", str(DATA / "load_budget.py"), *args],
                              capture_output=True, text=True, timeout=120)

    def test_self_check(self):
        r = self.run_script("--self-check")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_plugin_is_within_budget(self):
        r = self.run_script("size", str(P))
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("0 over", r.stdout)

    def test_plan_over_budget_exits_1(self):
        import json
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "plan.json"
            plan.write_text(json.dumps({"phases": [{"name": "Review", "lead": "a", "support": ["b", "c", "d"]}]}))
            r = self.run_script("plan", str(plan))
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("3 supporting skills, at most 2", r.stdout)

    def test_bad_usage_exits_2(self):
        self.assertEqual(self.run_script().returncode, 2)
        self.assertEqual(self.run_script("size", "/no/such/path").returncode, 2)
        self.assertEqual(self.run_script("plan", "/no/such/plan.json").returncode, 2)


if __name__ == "__main__":
    unittest.main()
