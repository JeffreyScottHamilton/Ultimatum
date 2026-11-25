import stat
import unittest

from _harness import UltCase, PY


class TestHandoff(UltCase):
    def make_repo(self):
        self.git_init()
        self.write("src/a.py", "print(1)\n")
        self.write("src/b.py", "print(2)\n")
        self.git("add", "-A")
        self.git("commit", "-qm", "init")

    def test_write_and_show_with_git_changes_and_evidence(self):
        self.make_repo()
        self.write("src/a.py", "print(10)\n")
        self.git("add", "src/a.py")
        self.write("src/new.py", "x=1\n")
        self.ult("run", "--name", "tests", "--", PY, "-c", "import sys; print('fail'); sys.exit(2)")
        rid = self.last_meta()["id"]
        r = self.ult("handoff", "write", "--goal", "Fix widgets", "--decision", "use X — because Y",
                     "--next", "run integration", "--question", "is Z ok?", "--evidence", "manual check")
        self.assertEqual(r.code, 0, r.all)
        hp = self.root / ".ultimatum" / "handoff.md"
        self.assertEqual(stat.S_IMODE(hp.stat().st_mode), 0o600)
        t = hp.read_text()
        self.assertIn("Fix widgets", t)
        self.assertIn("- use X — because Y", t)
        self.assertIn("`src/a.py` (M)", t)
        self.assertIn("`src/new.py` (??)", t)
        self.assertIn("→ exit 2", t)
        self.assertIn(f"log `{rid}`", t)
        self.assertIn("manual check", t)
        self.assertIn("run integration", t)
        self.assertIn("is Z ok?", t)
        self.assertIn("branch=", t)
        self.assertTrue(list((self.root / ".ultimatum" / "handoffs").glob("*.md")))
        s = self.ult("handoff", "show")
        self.assertEqual(s.code, 0, s.all)
        self.assertIn("Fix widgets", s.out)
        self.assertIn("all references present", s.out, s.out)

    def test_first_unstaged_change_not_mangled(self):
        # BUG: handoff.py:25 _git() does .strip() on `git status --short`, removing the leading space of
        # the first line (" M src/a.py"), so compose() (l[3:]) emits `rc/a.py` instead of `src/a.py`
        # and `show` then reports "referenced file missing: rc/a.py".
        self.make_repo()
        self.write("src/a.py", "print(10)\n")
        self.ult("handoff", "write")
        t = (self.root / ".ultimatum" / "handoff.md").read_text()
        self.assertIn("`src/a.py` (M)", t)
        self.assertNotIn("referenced file missing", self.ult("handoff", "show").out)

    def test_ultimatum_dir_not_listed_as_changed(self):
        self.make_repo()
        self.ult("run", "--", PY, "-c", "print(1)")
        self.ult("handoff", "write")
        t = (self.root / ".ultimatum" / "handoff.md").read_text()
        self.assertNotIn(".ultimatum", t.split("## Evidence")[0])
        self.assertIn("(working tree clean)", t)

    def test_check_missing_file_and_moved_head(self):
        self.make_repo()
        self.write("src/a.py", "print(10)\n")
        self.git("add", "src/a.py")
        self.ult("handoff", "write", "--goal", "g")
        # delete a referenced changed file and move HEAD
        (self.root / "src" / "a.py").unlink()
        self.write("src/c.py", "z=1\n")
        self.git("add", "-A")
        self.git("commit", "-qm", "second")
        s = self.ult("handoff", "show")
        self.assertIn("referenced file missing: src/a.py", s.out)
        self.assertIn("HEAD moved since handoff", s.out)
        self.assertNotIn("all references present", s.out)

    def test_check_missing_log(self):
        self.make_repo()
        self.ult("run", "--", PY, "-c", "print(1)")
        self.ult("handoff", "write")
        for p in self.logs_dir().glob("*.log"):
            p.unlink()
        s = self.ult("handoff", "show")
        self.assertIn("log not found locally", s.out)

    def test_show_without_handoff(self):
        r = self.ult("handoff", "show")
        self.assertEqual(r.code, 1)

    def test_no_git(self):
        r = self.ult("handoff", "write", "--goal", "g")
        self.assertEqual(r.code, 0, r.all)
        t = (self.root / ".ultimatum" / "handoff.md").read_text()
        self.assertIn("branch=(no git)", t)
        s = self.ult("handoff", "show")
        self.assertEqual(s.code, 0, s.all)

    def test_head_moved_not_flagged_when_unchanged(self):
        self.make_repo()
        self.ult("handoff", "write")
        s = self.ult("handoff", "show")
        self.assertNotIn("HEAD moved", s.out)

    def test_secrets_redacted(self):
        secret = "gh" + "p_" + "Q1w2E3r4T5" * 4
        self.ult("handoff", "write", "--goal", f"use {secret}", "--evidence", f"tok {secret}")
        t = (self.root / ".ultimatum" / "handoff.md").read_text()
        self.assertNotIn(secret, t)
        self.assertNotIn(secret, self.ult("handoff", "show").out)

    def test_secret_in_run_cmd_redacted_in_handoff(self):
        secret = "gh" + "p_" + "Z9y8X7w6V5" * 4
        self.ult("run", "--", PY, "-c", "print(1)", secret)
        self.ult("handoff", "write")
        self.assertNotIn(secret, (self.root / ".ultimatum" / "handoff.md").read_text())

    def test_renamed_and_deleted_files(self):
        self.make_repo()
        self.git("mv", "src/b.py", "src/b2.py")
        self.git("rm", "-q", "src/a.py")
        self.ult("handoff", "write")
        t = (self.root / ".ultimatum" / "handoff.md").read_text()
        self.assertIn("src/b2.py", t)
        self.assertIn("src/a.py", t)
        s = self.ult("handoff", "show")
        # BUG candidate: rename line "src/b.py -> src/b2.py" is rendered as one backticked token with spaces
        self.assertNotIn("Traceback", s.err)

    def test_untracked_dir_listing(self):
        self.make_repo()
        self.write("newdir/x.py", "1\n")
        self.write("newdir/y.py", "2\n")
        self.ult("handoff", "write")
        t = (self.root / ".ultimatum" / "handoff.md").read_text()
        self.assertIn("newdir/", t)

    def test_filename_with_spaces_check(self):
        self.make_repo()
        self.write("my file.py", "1\n")
        self.ult("handoff", "write")
        s = self.ult("handoff", "show")
        # BUG candidate: filenames with spaces are quoted by git status ("my file.py") and
        # would be reported as missing or mangled
        self.assertNotIn("referenced file missing", s.out, s.out)

    def test_dir_name_dot_in_extension_false_positive(self):
        # a changed file in the evidence like `ult run` cmd with a dotted token must not be flagged missing
        self.make_repo()
        self.ult("run", "--", PY, "-c", "print(1)")
        self.ult("handoff", "write")
        s = self.ult("handoff", "show")
        self.assertNotIn("referenced file missing", s.out, s.out)

    def test_run_cmd_referencing_script_not_flagged(self):
        self.make_repo()
        self.write("build.sh", "echo hi\n")
        self.ult("run", "--", "bash", "build.sh")
        self.ult("handoff", "write")
        s = self.ult("handoff", "show")
        self.assertNotIn("referenced file missing", s.out, s.out)


if __name__ == "__main__":
    unittest.main()
