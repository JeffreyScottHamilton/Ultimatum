"""Checks for the coding-discipline craft references (skills/work/references/craft/coding-discipline)."""
from __future__ import annotations

from pathlib import Path
import os
import re
import subprocess
import sys
import unittest

P = Path(__file__).resolve().parents[1]
CRAFT = P / "skills" / "work" / "references" / "craft" / "coding-discipline"
DATA = P / "data" / "craft" / "coding-discipline"
REPO = P.parents[1]

URL = re.compile(r"\bhttps?://[^\s)`>\]|]+")
TICKED = re.compile(r"`([A-Za-z0-9_./-]+\.(?:md|csv|py|js))`(?:[ \t]*§[ \t]*([A-Z0-9][^`|)\n]*))?")


def _md() -> list[Path]:
    return sorted(CRAFT.glob("*.md"))


def _data() -> list[Path]:
    return sorted(f for f in DATA.rglob("*") if f.is_file() and "__pycache__" not in f.parts) if DATA.is_dir() else []


def _headings(path: Path) -> set[str]:
    return {m.group(1).strip() for m in re.finditer(r"^#{2,4}\s+(.+)$", path.read_text(encoding="utf-8"), re.M)}


class CraftCodingDiscipline(unittest.TestCase):
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


DIFF = """diff --git a/app.py b/app.py
--- a/app.py
+++ b/app.py
@@ -3 +3 @@
-x = 'a'
+x = "a"
@@ -10 +10 @@
-    total = a+b
+    total = a + b
@@ -20 +20 @@
-# old note
+# new note
@@ -30,2 +30,2 @@
-import os
-import re
+import re
+import os
@@ -40 +40 @@
-limit = 10
+limit = 20
diff --git a/sql/q.sql b/sql/q.sql
--- a/sql/q.sql
+++ b/sql/q.sql
@@ -1 +1 @@
--- keep
+select 1;
"""


class DiffScope(unittest.TestCase):
    def run_it(self, text: str, *args: str) -> tuple[int, str]:
        res = subprocess.run([sys.executable, "-I", str(DATA / "diff_scope.py"), *args], input=text,
                             capture_output=True, text=True, timeout=60)
        return res.returncode, res.stdout

    def test_flags_each_drive_by_kind_and_not_the_real_edit(self):
        code, out = self.run_it(DIFF)
        self.assertEqual(code, 1)
        for row in ("app.py:3 quote-only", "app.py:10 whitespace-only", "app.py:20 comment-only", "app.py:30 reorder-only"):
            self.assertIn(row, out)
        self.assertNotIn("app.py:40", out)
        self.assertNotIn("sql/q.sql:1 comment-only", out)

    def test_allow_list(self):
        code, out = self.run_it(DIFF, "--allow", "app.py")
        self.assertIn("sql/q.sql:1 outside-scope", out)
        self.assertNotIn("app.py:1 outside-scope", out)

    def test_clean_diff_exits_zero(self):
        code, out = self.run_it("diff --git a/a b/a\n--- a/a\n+++ b/a\n@@ -1 +1 @@\n-n = 1\n+n = 2\n")
        self.assertEqual((code, out.strip()), (0, "no drive-by hunks found"))


if __name__ == "__main__":
    unittest.main()
