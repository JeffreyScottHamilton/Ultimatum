"""Ultimatum's own stack tables (data/design-own/stacks): build, coverage, cells and copy check."""
import csv
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from urllib.parse import urlparse

PLUGIN = Path(__file__).resolve().parents[1]
REPO = PLUGIN.parents[1]
OWN = PLUGIN / "data" / "design-own" / "stacks"
THEIRS = PLUGIN / "data" / "design" / "stacks"
STACKS = ("astro", "flutter", "html-tailwind", "nextjs", "nuxtjs", "react-native", "react", "shadcn",
          "svelte", "swiftui", "threejs", "vue")
COLS = ["Category", "Guideline", "Applies To", "Severity", "Description", "Docs URL", "Do", "Don't",
        "Code Good", "Code Bad"]

sys.path.insert(0, str(REPO / "tools"))
import build_stacks  # noqa: E402


def rows(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


class OwnStacks(unittest.TestCase):
    def test_check_matches(self):
        r = subprocess.run([sys.executable, str(REPO / "tools" / "build_stacks.py"), "--check"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_every_stack_present_with_columns(self):
        for s in STACKS:
            with self.subTest(stack=s):
                self.assertTrue((OWN / f"{s}.csv").is_file())
                self.assertEqual(list(rows(OWN / f"{s}.csv")[0]), COLS)

    def test_row_counts_at_least_theirs(self):
        for s in STACKS:
            with self.subTest(stack=s):
                self.assertGreaterEqual(len(rows(OWN / f"{s}.csv")), len(rows(THEIRS / f"{s}.csv")))

    def test_cells_filled_and_urls_official(self):
        for s in STACKS:
            for i, r in enumerate(rows(OWN / f"{s}.csv"), 1):
                with self.subTest(stack=s, row=i):
                    for c in COLS:
                        self.assertTrue(r[c].strip(), f"{c} empty")
                    self.assertIn(r["Severity"], {"Critical", "High", "Medium", "Low"})
                    u = urlparse(r["Docs URL"])
                    self.assertEqual(u.scheme, "https")
                    self.assertIn(u.hostname, build_stacks.HOSTS[s])

    def test_copy_check_per_stack(self):
        for s in STACKS:
            with self.subTest(stack=s), tempfile.TemporaryDirectory() as tmp:
                ours, theirs = Path(tmp, "ours"), Path(tmp, "theirs")
                ours.mkdir()
                theirs.mkdir()
                shutil.copy(OWN / f"{s}.csv", ours / f"{s}.csv")
                shutil.copy(THEIRS / f"{s}.csv", theirs / f"{s}.csv")
                r = subprocess.run([sys.executable, str(REPO / "tools" / "copy_check.py"), str(ours), str(theirs)],
                                   capture_output=True, text=True)
                self.assertEqual(r.returncode, 0, r.stdout[-800:] + r.stderr)


if __name__ == "__main__":
    unittest.main()
