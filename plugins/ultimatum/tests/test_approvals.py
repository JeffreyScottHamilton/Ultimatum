import io
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from ultlib import approvals as ap  # noqa: E402

ULT = ROOT / "scripts" / "ult"
SHIP = ROOT / "skills" / "work" / "references" / "ship.md"


def change(files, authors=("dev@example.com",), base="main"):
    return {"files": {n: {"lines": l, "status": s} for n, (l, s) in files.items()},
            "authors": list(authors), "base": base}


def policy(*rules):
    return {"version": 1, "rules": list(rules)}


class Globs(unittest.TestCase):
    def test_double_star_crosses_folders_single_does_not(self):
        self.assertTrue(ap.covers(["src/**"], "src/a/b.py"))
        self.assertTrue(ap.covers(["**/*.md"], "README.md"))
        self.assertTrue(ap.covers(["**/*.md"], "docs/x/y.md"))
        self.assertFalse(ap.covers(["src/*.py"], "src/a/b.py"))

    def test_braces_and_exclusions(self):
        self.assertTrue(ap.covers(["**/*.{png,svg}"], "img/a.svg"))
        self.assertFalse(ap.covers(["**", "!**/*.md"], "a/b.md"))
        self.assertTrue(ap.covers(["**", "!**/*.md"], "a/b.py"))

    def test_risk_from_paths(self):
        self.assertEqual(ap.file_risk("src/auth/login.py"), "high")
        self.assertEqual(ap.file_risk(".github/workflows/ci.yml"), "high")
        self.assertEqual(ap.file_risk("db/migrations/001.sql"), "high")
        self.assertEqual(ap.file_risk("package.json"), "medium")
        self.assertEqual(ap.file_risk("src/api/users.ts"), "medium")
        self.assertEqual(ap.file_risk("README.md"), "low")
        self.assertEqual(ap.file_risk("src/author_card.tsx"), "low")


class Validate(unittest.TestCase):
    def test_starter_is_valid(self):
        self.assertEqual(ap.validate(ap.STARTER), [])

    def test_errors_are_named(self):
        bad = {"version": 2, "mode": "enforce", "rules": [
            {"paths": ["!x"], "verdict": "merge"},
            {"purpose": "p", "paths": ["**"], "verdict": "people"},
            {"purpose": "p", "paths": ["**"], "verdict": "approve", "people": 2},
            {"purpose": "p", "paths": ["**"], "verdict": "block", "if": "lines > 3"},
            {"purpose": "p", "paths": ["**"], "verdict": "block", "if": "risk = huge"},
        ]}
        text = "\n".join(ap.validate(bad))
        for part in ("version must be 1", "no mode", "purpose is required", "not an exclusion",
                     "verdict must be", "people needs", "people only goes", "unknown fact", "risk is one of"):
            self.assertIn(part, text)


class Decide(unittest.TestCase):
    def test_strictest_wins_and_largest_people_count(self):
        p = policy({"purpose": "docs", "paths": ["**/*.md"], "verdict": "approve"},
                   {"purpose": "code", "paths": ["src/**"], "verdict": "people", "people": 1},
                   {"purpose": "auth", "paths": ["src/auth/**"], "verdict": "people", "people": 2})
        r = ap.decide(p, change({"a.md": (3, "modified"), "src/auth/x.py": (10, "modified")}))
        self.assertEqual(r["overall"], "people")
        self.assertIn("2 human review", r["needs"][0])
        self.assertTrue(r["observe_only"])

    def test_block_beats_everything(self):
        p = policy({"purpose": "docs", "paths": ["**"], "verdict": "approve"},
                   {"purpose": "too big", "paths": ["**"], "if": "diff_lines > 100", "verdict": "block"})
        self.assertEqual(ap.decide(p, change({"a.md": (101, "added")}))["overall"], "block")
        self.assertEqual(ap.decide(p, change({"a.md": (100, "added")}), 0)["overall"], "approve")

    def test_uncovered_and_unapplied_files_need_a_person(self):
        p = policy({"purpose": "docs", "paths": ["**/*.md"], "verdict": "approve"},
                   {"purpose": "small code", "paths": ["src/**"], "if": "rule_lines < 5", "verdict": "approve"})
        r = ap.decide(p, change({"a.md": (1, "modified"), "lib/x.py": (1, "modified"), "src/y.py": (50, "modified")}), 0)
        self.assertEqual(r["overall"], "people")
        self.assertEqual(r["uncovered"], ["lib/x.py"])
        self.assertEqual(r["no_rule_applies"], ["src/y.py"])

    def test_approve_depends_on_the_review(self):
        p = policy({"purpose": "all", "paths": ["**"], "verdict": "approve"})
        c = change({"a.py": (2, "modified")})
        self.assertIn("only if the review", ap.decide(p, c)["needs"][0])
        self.assertEqual(ap.decide(p, c, 1)["overall"], "people")
        self.assertEqual(ap.decide(p, c, 0)["overall"], "approve")

    def test_first_true_override_wins(self):
        p = policy({"purpose": "auth", "paths": ["src/**"], "verdict": "people", "people": 2, "override": [
            {"if": "rule_lines < 5", "verdict": "people", "people": 1},
            {"if": "rule_lines < 50", "verdict": "approve"}]})
        self.assertIn("1 human", ap.decide(p, change({"src/a.py": (3, "modified")}))["needs"][0])
        self.assertEqual(ap.decide(p, change({"src/a.py": (30, "modified")}), 0)["overall"], "approve")
        self.assertIn("2 human", ap.decide(p, change({"src/a.py": (90, "modified")}))["needs"][0])

    def test_author_base_risk_and_or(self):
        p = policy({"purpose": "bots", "paths": ["**"], "verdict": "approve",
                    "if": "author = *[bot]* OR base = release/*"},
                   {"purpose": "rest", "paths": ["**"], "verdict": "comment",
                    "if": "risk >= medium AND files_added = 0"})
        bot = change({"package.json": (2, "modified")}, authors=["deps[bot]"])
        self.assertEqual(ap.decide(p, bot, 0)["rules"][0]["applies"], True)
        self.assertEqual(ap.decide(p, bot, 0)["overall"], "comment")
        rel = change({"README.md": (2, "modified")}, base="release/2")
        self.assertEqual(ap.decide(p, rel, 0)["overall"], "approve")

    def test_empty_change(self):
        self.assertEqual(ap.decide(ap.STARTER, change({}))["overall"], "nothing")


def git(cwd, *args):
    subprocess.run(["git", "-C", cwd, *args], check=True, capture_output=True)


class Cli(unittest.TestCase):
    def run_ult(self, *args, cwd=None):
        return subprocess.run([sys.executable, str(ULT), "approvals", *args], cwd=cwd,
                              capture_output=True, text=True)

    def test_real_repo_including_untracked(self):
        with tempfile.TemporaryDirectory() as d:
            git(d, "init", "-q", "-b", "main")
            git(d, "config", "user.email", "t@example.com"); git(d, "config", "user.name", "T")
            Path(d, "README.md").write_text("hi\n")
            git(d, "add", "."); git(d, "commit", "-qm", "init")
            git(d, "checkout", "-qb", "feat")
            os.makedirs(Path(d, "src/auth")); Path(d, "src/auth/login.py").write_text("x = 1\ny = 2\n")
            Path(d, "README.md").write_text("hi\nmore\n")
            pol = Path(d, ".claude"); pol.mkdir()
            (pol / "ultimatum-approvals.json").write_text(json.dumps(ap.STARTER))
            out = self.run_ult("--base", "main", "--json", "--root", d)
            self.assertEqual(out.returncode, 0, out.stderr)
            r = json.loads(out.stdout)
            self.assertIn("src/auth/login.py", [f for x in r["rules"] for f in x["files"]])
            self.assertEqual(r["facts"]["risk"], "high")
            self.assertEqual(r["overall"], "people")
            self.assertIn("2 human", r["needs"][0])
            text = self.run_ult("--base", "main", "--root", d).stdout
            self.assertIn("observe only; nothing was approved", text)

    def test_exit_codes(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(self.run_ult("--root", d).returncode, 1)  # no policy
            bad = Path(d, "p.json"); bad.write_text('{"version": 1, "rules": []}')
            self.assertEqual(self.run_ult("--check", "--policy", str(bad)).returncode, 1)
            good = Path(d, "g.json"); good.write_text(json.dumps(ap.STARTER))
            self.assertEqual(self.run_ult("--check", "--policy", str(good)).returncode, 0)
            self.assertEqual(self.run_ult("--policy", str(good), "--root", d).returncode, 2)  # not a repo
            self.assertEqual(self.run_ult("--bogus").returncode, 2)
            self.assertEqual(json.loads(self.run_ult("--starter").stdout), ap.STARTER)

    def test_stdlib_only_and_never_acts(self):
        src = (ROOT / "scripts" / "ultlib" / "approvals.py").read_text(encoding="utf-8")
        imports = set(re.findall(r"^(?:from|import)\s+([\w.]+)", src, re.M))
        self.assertLessEqual(imports, {"__future__", "argparse", "json", "re", "subprocess", "sys", "pathlib"})
        calls = re.findall(r'_git\(root, "([\w-]+)"', src)
        self.assertLessEqual(set(calls), {"rev-parse", "merge-base", "diff", "ls-files", "log", "config"})
        self.assertNotIn("gh ", src)


class Guides(unittest.TestCase):
    def test_ship_guide(self):
        text = SHIP.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("# "))
        self.assertLess(len(text.encode()), 15000)
        for word in ("Important", "Nit", "Pre-existing", "ult approvals", "Claude Ship", "never", "ci-and-pr.md"):
            self.assertIn(word, text)
        for fact in ("files_changed", "rule_lines", "rule_risk", "author", "base"):
            self.assertIn(f"`{fact}`", text)

    def test_linked_from_release_ci_and_review(self):
        for rel in ("skills/release/SKILL.md", "skills/work/references/ci-and-pr.md", "skills/work/references/release.md"):
            self.assertIn("ship.md", (ROOT / rel).read_text(encoding="utf-8"), rel)
        review = (ROOT / "skills/review/SKILL.md").read_text(encoding="utf-8")
        for tag in ("**Important**", "**Nit**", "**Pre-existing**"):
            self.assertIn(tag, review)
        self.assertIn("Pre-existing", (ROOT / "agents/reviewer.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
