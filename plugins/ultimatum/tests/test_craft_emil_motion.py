"""Checks for the Emil motion craft references and their data tables."""
from __future__ import annotations

import csv
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path

P = Path(__file__).resolve().parents[1]
CRAFT = P / "skills" / "website" / "references" / "craft" / "emil-motion"
DATA = P / "data" / "craft" / "emil-motion"
REPO = P.parents[1]
SOURCE = Path(os.environ.get("EMIL_SOURCE", "/tmp/src/emil-motion"))

URL = re.compile(r"\bhttps?://[^\s)`>\]|]+")
TICKED = re.compile(r"`([A-Za-z0-9_./-]+\.(?:md|csv))`(?:[ \t]*§[ \t]*([A-Z][^`|)\n]*))?")
TABLES = {
    "timing.csv": ["element", "enter_ms", "exit_ms", "curve", "note", "file"],
    "symptoms.csv": ["area", "symptom", "likely_cause", "first_fix", "file"],
    "vocabulary.csv": ["term", "group", "meaning", "not_to_confuse_with", "hint"],
    "worst-case.csv": ["kind", "value", "breaks", "fix_hint"],
    "libraries.csv": ["task", "library", "url", "use_when", "skip_when"],
}
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[a-z]{2,}", re.I)
EXAMPLE = re.compile(r"@[\w.-]*example\.(com|org|net)\b|@[\w.-]*\.example\b|@b\.example\b", re.I)


def _md() -> list[Path]:
    return sorted(CRAFT.glob("*.md"))


def _headings(path: Path) -> set[str]:
    return {m.group(1).strip() for m in re.finditer(r"^#{2,4}\s+(.+)$", path.read_text(encoding="utf-8"), re.M)}


class CraftEmilMotion(unittest.TestCase):
    def test_index_lists_every_file_and_each_exists(self):
        index = (CRAFT / "index.md").read_text(encoding="utf-8")
        listed = set(re.findall(r"^- `([a-z0-9-]+\.md)`:", index, re.M))
        self.assertTrue(listed)
        for name in sorted(listed):
            with self.subTest(file=name):
                self.assertTrue((CRAFT / name).is_file())
        on_disk = {p.name for p in _md()} - {"index.md"}
        self.assertEqual(on_disk, listed, "index.md must list every craft file once")

    def test_files_are_small_and_open_with_when_to_read(self):
        for path in _md():
            lines = path.read_text(encoding="utf-8").splitlines()
            with self.subTest(file=path.name):
                self.assertLessEqual(path.stat().st_size, 15 * 1024)
                self.assertTrue(lines[0].startswith("# "))
                self.assertTrue(lines[2].startswith("Read "), "line 3 says when to read the file")

    def test_links_are_https(self):
        for path in _md() + [DATA / "README.md"]:
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
                    continue  # a bare name such as `measure.mjs` in prose
                with self.subTest(file=path.name, ref=ref):
                    self.assertTrue(target.exists(), f"{ref} not found")
                if section and target.suffix == ".md" and target.parent == CRAFT:
                    with self.subTest(file=path.name, ref=ref, section=section):
                        heads = _headings(target)
                        self.assertTrue(any(section.startswith(h) for h in heads),
                                        f"{ref} has no heading at the start of: {section.strip()}")

    def test_csv_tables_parse_with_no_empty_cells(self):
        self.assertEqual({p.name for p in DATA.glob("*.csv")}, set(TABLES))
        for name, columns in TABLES.items():
            with open(DATA / name, encoding="utf-8", newline="") as fh:
                rows = list(csv.reader(fh))
            with self.subTest(table=name):
                self.assertEqual(rows[0], columns)
                self.assertGreater(len(rows), 5)
                seen = set()
                for n, row in enumerate(rows[1:], start=2):
                    self.assertEqual(len(row), len(columns), f"{name} line {n}")
                    self.assertTrue(all(c.strip() for c in row), f"{name} line {n} has an empty cell")
                    key = tuple(row[:2]) if name == "worst-case.csv" else (row[1],) if name in ("symptoms.csv", "libraries.csv") else (row[0],)
                    self.assertNotIn(key, seen, f"{name} repeats {key}")
                    seen.add(key)

    def test_csv_file_columns_point_at_real_files(self):
        for name in ("timing.csv", "symptoms.csv"):
            with open(DATA / name, encoding="utf-8", newline="") as fh:
                for row in csv.DictReader(fh):
                    with self.subTest(table=name, file=row["file"]):
                        self.assertTrue((CRAFT / row["file"]).is_file() or (CRAFT.parent / row["file"]).is_file())

    def test_library_urls_are_https(self):
        with open(DATA / "libraries.csv", encoding="utf-8", newline="") as fh:
            for row in csv.DictReader(fh):
                with self.subTest(url=row["url"]):
                    self.assertTrue(row["url"].startswith("https://"))

    def test_vocabulary_groups(self):
        with open(DATA / "vocabulary.csv", encoding="utf-8", newline="") as fh:
            groups = {r["group"] for r in csv.DictReader(fh)}
        self.assertTrue({"entrance-exit", "timing", "easing", "spring", "polish", "performance", "principle"} <= groups)

    def test_no_credentials(self):
        secret = re.compile(r"(api[_-]?key|secret|token)\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}", re.I)
        for path in _md() + list(DATA.iterdir()):
            text = path.read_text(encoding="utf-8")
            with self.subTest(file=path.name):
                self.assertIsNone(secret.search(text))
                for m in EMAIL.finditer(text):
                    self.assertTrue(EXAMPLE.search(m.group(0)), f"real-looking email: {m.group(0)}")

    @unittest.skipUnless(SOURCE.is_dir(), "source checkout not present (set EMIL_SOURCE)")
    def test_copy_check_passes(self):
        res = subprocess.run([sys.executable, str(REPO / "tools" / "copy_check.py"), str(CRAFT), str(SOURCE)],
                             capture_output=True, text=True, timeout=300)
        self.assertEqual(res.returncode, 0, res.stdout[-2000:])


if __name__ == "__main__":
    unittest.main()
