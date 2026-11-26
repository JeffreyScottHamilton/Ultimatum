"""Checks for the design review and QA craft references and their data tables."""
from __future__ import annotations

import csv
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path

P = Path(__file__).resolve().parents[1]
CRAFT = P / "skills" / "website" / "references" / "craft" / "design-review-qa"
DATA = P / "data" / "craft" / "design-review-qa"
REPO = P.parents[1]
SOURCE = Path(os.environ.get("GSTACK_SOURCE", "/tmp/src/design-review-qa"))

URL = re.compile(r"\bhttps?://[^\s)`>\]|]+")
TICKED = re.compile(r"`([A-Za-z0-9_./-]+\.(?:md|csv))`(?:[ \t]*§[ \t]*([A-Z][^`|)\n]*))?")
TABLES = {
    "design-checks.csv": ["id", "category", "check", "file"],
    "slop-tells.csv": ["id", "kind", "tell", "instead", "severity", "file"],
    "qa-issues.csv": ["kind", "name", "meaning", "example", "score_effect"],
}


def _md() -> list[Path]:
    return sorted(CRAFT.glob("*.md"))


def _headings(path: Path) -> set[str]:
    heads = re.findall(r"^#{2,4}\s+(.+)$", path.read_text(encoding="utf-8"), re.M)
    return {re.sub(r"^\d+\.\s*", "", h.strip()) for h in heads}


class CraftDesignReviewQa(unittest.TestCase):
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
                    continue  # a bare name such as `qa-sweep.mjs` in prose
                with self.subTest(file=path.name, ref=ref):
                    self.assertTrue(target.exists(), f"{ref} not found")
                if section and target.suffix == ".md" and target.parent == CRAFT:
                    sec = section.strip()
                    with self.subTest(file=path.name, ref=ref, section=sec):
                        self.assertTrue(any(h.startswith(sec) or sec.startswith(h) for h in _headings(target)),
                                        f"{ref} has no heading matching: {sec}")

    def test_csvs_parse_with_no_empty_cells(self):
        for name, columns in TABLES.items():
            with open(DATA / name, encoding="utf-8", newline="") as fh:
                rows = list(csv.reader(fh))
            self.assertEqual(rows[0], columns, name)
            seen = set()
            for n, row in enumerate(rows[1:], start=2):
                with self.subTest(table=name, line=n):
                    self.assertEqual(len(row), len(columns))
                    self.assertTrue(all(cell.strip() for cell in row), "empty cell")
                    self.assertNotIn(row[0] if name != "qa-issues.csv" else (row[0], row[1]), seen)
                    seen.add(row[0] if name != "qa-issues.csv" else (row[0], row[1]))
                    if "file" in columns:
                        self.assertTrue((CRAFT / row[columns.index("file")]).is_file())
            self.assertGreater(len(seen), 0)

    def test_no_credentials(self):
        secret = re.compile(r"(api[_-]?key|secret|token)\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}|[\w.+-]+@[\w-]+\.[a-z]{2,}", re.I)
        for path in _md() + list(DATA.iterdir()):
            with self.subTest(file=path.name):
                self.assertIsNone(secret.search(path.read_text(encoding="utf-8")))

    @unittest.skipUnless(SOURCE.is_dir(), "source checkout not present (set GSTACK_SOURCE)")
    def test_copy_check_passes(self):
        res = subprocess.run([sys.executable, str(REPO / "tools" / "copy_check.py"), str(CRAFT), str(SOURCE)],
                             capture_output=True, text=True, timeout=600)
        self.assertEqual(res.returncode, 0, res.stdout[-2000:])


if __name__ == "__main__":
    unittest.main()
