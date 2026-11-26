"""Checks for the superpowers craft references (skills/work/references/craft/superpowers)."""
from __future__ import annotations

from pathlib import Path
import os
import re
import subprocess
import sys
import unittest

P = Path(__file__).resolve().parents[1]
CRAFT = P / "skills" / "work" / "references" / "craft" / "superpowers"
DATA = P / "data" / "craft" / "superpowers"
REPO = P.parents[1]
SOURCE = Path(os.environ.get("SUPERPOWERS_SOURCE", "/tmp/src/superpowers"))

URL = re.compile(r"\bhttps?://[^\s)`>\]|]+")
TICKED = re.compile(r"`([A-Za-z0-9_./-]+\.(?:md|csv|py|js))`(?:[ \t]*§[ \t]*([A-Z0-9][^`|)\n]*))?")


def _md() -> list[Path]:
    return sorted(CRAFT.glob("*.md"))


def _data() -> list[Path]:
    return sorted(f for f in DATA.rglob("*") if f.is_file() and "__pycache__" not in f.parts) if DATA.is_dir() else []


def _headings(path: Path) -> set[str]:
    return {m.group(1).strip() for m in re.finditer(r"^#{2,4}\s+(.+)$", path.read_text(encoding="utf-8"), re.M)}


class CraftSuperpowers(unittest.TestCase):
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

    @unittest.skipUnless(SOURCE.is_dir(), "source checkout not present (set SUPERPOWERS_SOURCE)")
    def test_copy_check_passes(self):
        res = subprocess.run([sys.executable, str(REPO / "tools" / "copy_check.py"), str(CRAFT), str(SOURCE)],
                             capture_output=True, text=True, timeout=600)
        self.assertEqual(res.returncode, 0, res.stdout[-2000:])


class SuperpowersScripts(unittest.TestCase):
    def run_py(self, *args, cwd=None):
        return subprocess.run([sys.executable, *args], cwd=cwd, capture_output=True, text=True, timeout=60)

    def test_wait_until_self_check(self):
        done = self.run_py(str(DATA / "wait_until.py"))
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn("2 checks passed", done.stdout)

    def test_find_polluter_names_the_culprit_and_refuses_dirty_start(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            (base / "tests").mkdir()
            for name in ("one", "two", "three"):
                (base / "tests" / f"test_{name}.py").write_text("x = 1\n")
            (base / "runner.py").write_text(
                "import pathlib, sys\n"
                "if sys.argv[1].endswith('test_two.py'):\n"
                "    pathlib.Path('left; behind').mkdir()\n"
            )
            tool = str(DATA / "find_polluter.py")
            cmd = [tool, "--artifact", "left; behind", "--glob", "tests/test_*.py", "--", sys.executable, "runner.py", "{}"]
            found = self.run_py(*cmd, cwd=base)
            self.assertEqual(found.returncode, 0, found.stderr)
            self.assertIn("tests/test_two.py", found.stdout)
            dirty = self.run_py(*cmd, cwd=base)
            self.assertEqual(dirty.returncode, 2)
            (base / "left; behind").rmdir()
            none = self.run_py(tool, "--artifact", "absent", "--glob", "tests/test_*.py", "--", sys.executable, "runner.py", cwd=base)
            self.assertEqual(none.returncode, 1)


if __name__ == "__main__":
    unittest.main()
