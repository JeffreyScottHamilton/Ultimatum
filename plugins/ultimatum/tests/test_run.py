import hashlib
import os
import stat
import unittest

from _harness import UltCase, PY


def pyc(code, *extra):
    return ["run", *extra, "--", PY, "-c", code]


class TestRun(UltCase):
    def test_exit_codes(self):
        for c in (0, 1, 3):
            r = self.ult(*pyc(f"import sys; print('hi'); sys.exit({c})"))
            self.assertEqual(r.code, c, r.all)
            self.assertIn(f"exit={c}", r.out)

    def test_missing_command_127(self):
        r = self.ult("run", "--", "definitely-not-a-cmd-xyz")
        self.assertEqual(r.code, 127, r.all)

    def test_timeout_124(self):
        r = self.ult(*pyc("import time; print('x', flush=True); time.sleep(30)", "--timeout", "1"))
        self.assertEqual(r.code, 124, r.all)
        self.assertEqual(self.last_meta()["timed_out"], True)

    @unittest.expectedFailure
    def test_signal_death_exit_code(self):
        # BUG: run.py cmd_run returns proc.returncode (-9 for SIGKILL): prints "exit=-9" and the
        # process exits 247 (-9 & 0xff). Expected shell convention 128+9=137 and a non-negative exit=.
        r = self.ult("run", "--shell", "--", "kill -9 $$")
        self.assertNotIn("exit=-", r.out)
        self.assertEqual(r.code, 137, r.all)

    def test_raw_log_byte_identical(self):
        code = "import sys; sys.stdout.write('a\\n\\tb  \\n'); sys.stdout.flush(); sys.stderr.write('err line\\n'); print('caf\\u00e9 \\u2603')"
        r = self.ult(*pyc(code))
        self.assertEqual(r.code, 0, r.all)
        meta = self.last_meta()
        raw = (self.logs_dir() / f"{meta['id']}.log").read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), meta["sha256"])
        self.assertEqual(len(raw), meta["bytes"])
        got = self.ult("log", meta["id"], "--raw")
        self.assertEqual(got.out.encode("utf-8"), raw)
        self.assertIn(b"err line", raw)

    def test_raw_log_binary_bytes_preserved(self):
        r = self.ult(*pyc("import sys; sys.stdout.buffer.write(b'ok\\n\\xff\\xfe\\x00bin\\n')"))
        meta = self.last_meta()
        raw = (self.logs_dir() / f"{meta['id']}.log").read_bytes()
        self.assertEqual(raw, b"ok\n\xff\xfe\x00bin\n")
        self.assertEqual(hashlib.sha256(raw).hexdigest(), meta["sha256"])

    def test_log_raw_exact_with_odd_line_separators(self):
        # BUG: splitlines() treats \x0c, \x1c,  , \r as line breaks, so `ult log --raw`
        # is not exact for such output (and line numbers diverge from `wc -l`).
        r = self.ult(*pyc("import sys; sys.stdout.write('a\\x0cb\\r\\nc\\n')"))
        meta = self.last_meta()
        raw = (self.logs_dir() / f"{meta['id']}.log").read_bytes()
        got = self.ult("log", meta["id"], "--raw")
        self.assertEqual(got.out.encode(), raw)

    test_log_raw_exact_with_odd_line_separators = unittest.expectedFailure(test_log_raw_exact_with_odd_line_separators)

    def test_buried_failure_verbatim(self):
        code = ("for i in range(2000):\n"
                "    print('noise line', i)\n"
                "    if i == 1234: print('FATAL: database exploded at shard 7 (code=XJ-4411)')\n")
        r = self.ult(*pyc(code))
        self.assertIn("FATAL: database exploded at shard 7 (code=XJ-4411)", r.out)
        self.assertIn("omitted", r.out)
        self.assertLess(len(r.out.splitlines()), 150)
        # tail is shown too
        self.assertIn("noise line 1999", r.out)

    def test_small_output_full(self):
        code = "\n".join(["print('line %d')" % i for i in range(30)])
        r = self.ult(*pyc(code))
        for i in range(30):
            self.assertIn(f"line {i}\n", r.out)
        self.assertNotIn("omitted", r.out)

    def test_lines_and_grep_and_last(self):
        self.ult(*pyc("for i in range(1,101): print('row', i)"))
        r = self.ult("log", "last", "--lines", "10:12")
        self.assertEqual(r.out.splitlines(), ["row 10", "row 11", "row 12"])
        r = self.ult("log", "last", "--lines", "98:")
        self.assertEqual(r.out.splitlines(), ["row 98", "row 99", "row 100"])
        r = self.ult("log", "last", "--grep", r"^row 50$", "--context", "1")
        self.assertIn("row 49", r.out)
        self.assertIn("row 51", r.out)
        self.assertIn("1 match", r.out)
        r = self.ult("log", "last", "-n", "--lines", "5:5")
        self.assertEqual(r.out.strip(), "5\trow 5")
        r = self.ult("log", "last", "--meta")
        self.assertIn('"exit_code": 0', r.out)

    def test_log_by_unique_substring_and_unknown(self):
        self.ult(*pyc("print('a')", "--name", "alpha"))
        r = self.ult("log", "alpha")
        self.assertEqual(r.code, 0, r.all)
        r = self.ult("log", "nonexistent-zzz")
        self.assertNotEqual(r.code, 0)

    def test_logs_listing(self):
        self.ult(*pyc("print('a')", "--name", "one"))
        r = self.ult("logs")
        self.assertIn("one-", r.out)

    def test_secrets_redacted_in_print_not_raw(self):
        secret = "gh" + "p_" + "A1b2C3d4E5" * 4
        r = self.ult(*pyc(f"print('token is {secret}')"))
        self.assertNotIn(secret, r.all)
        self.assertIn("[REDACTED:github-token:", r.out)
        meta = self.last_meta()
        raw = (self.logs_dir() / f"{meta['id']}.log").read_text()
        self.assertIn(secret, raw)
        self.assertNotIn(secret, self.ult("log", meta["id"]).out)
        self.assertIn(secret, self.ult("log", meta["id"], "--raw").out)
        self.assertNotIn(secret, self.ult("log", meta["id"], "--grep", "token").out)

    def test_secret_in_command_line_redacted_in_header(self):
        secret = "gh" + "p_" + "Z9y8X7w6V5" * 4
        r = self.ult("run", "--", PY, "-c", "print(1)", secret)
        self.assertNotIn(secret, r.all)
        self.assertNotIn(secret, self.ult("logs").out)

    def test_file_modes_and_gitignore(self):
        self.ult(*pyc("print('x')"))
        meta = self.last_meta()
        for ext in (".log", ".json"):
            m = stat.S_IMODE((self.logs_dir() / f"{meta['id']}{ext}").stat().st_mode)
            self.assertEqual(m, 0o600, ext)
        gi = self.root / ".ultimatum" / ".gitignore"
        self.assertIn("*", gi.read_text().splitlines())
        self.assertEqual(stat.S_IMODE((self.root / ".ultimatum").stat().st_mode), 0o700)
        db = self.root / ".ultimatum" / "index.db"
        self.assertEqual(stat.S_IMODE(db.stat().st_mode), 0o600)

    def test_gitignore_actually_hides_state(self):
        self.git_init()
        self.ult(*pyc("print('x')"))
        self.assertEqual(self.git("status", "--short").strip(), "")

    def test_no_command_usage(self):
        r = self.ult("run")
        self.assertEqual(r.code, 2)

    def test_dashdash_optional_and_args_with_flags(self):
        r = self.ult("run", PY, "-c", "import sys; print(sys.argv[1:])", "--foo", "-x")
        self.assertEqual(r.code, 0, r.all)
        self.assertIn("['--foo', '-x']", r.out)

    def test_cwd_option(self):
        sub = self.root / "sub"
        sub.mkdir()
        r = self.ult(*pyc("import os; print(os.getcwd())", "--cwd", str(sub)))
        self.assertIn(str(sub), r.out)

    def test_shell_mode(self):
        r = self.ult("run", "--shell", "--", "echo one && echo two >&2; exit 3")
        self.assertEqual(r.code, 3)
        self.assertIn("one", r.out)
        self.assertIn("two", r.out)

    def test_max_lines_respected(self):
        code = "for i in range(500): print('Error: bad thing', i)"
        r = self.ult(*pyc(code, "--max-lines", "20"))
        # header(2) + budget + markers; must be far below 500
        self.assertLess(len(r.out.splitlines()), 60, len(r.out.splitlines()))

    def test_stderr_interleaved_into_log(self):
        r = self.ult("run", "--shell", "--", "echo out; echo err 1>&2")
        raw = (self.logs_dir() / f"{self.last_meta()['id']}.log").read_text()
        self.assertIn("out", raw)
        self.assertIn("err", raw)

    # ---- family selection -------------------------------------------------
    PYTEST_OUT = (
        "============================= test session starts ==============================\n"
        "collected 40 items\n"
        + "".join("tests/test_a.py ........\n" for _ in range(200))
        + "=================================== FAILURES ===================================\n"
        "_____________________________ test_widget_total ________________________________\n"
        "\n"
        "    def test_widget_total():\n"
        ">       assert total([1, 2]) == 4\n"
        "E       assert 3 == 4\n"
        "E        +  where 3 = total([1, 2])\n"
        "\n"
        "tests/test_a.py:12: AssertionError\n"
        "_____________________________ test_other ________________________________\n"
        "\n"
        "E       KeyError: 'zzz'\n"
        "tests/test_a.py:30: KeyError\n"
        "=========================== short test summary info ============================\n"
        "FAILED tests/test_a.py::test_widget_total - assert 3 == 4\n"
        "FAILED tests/test_a.py::test_other - KeyError: 'zzz'\n"
        "========================= 2 failed, 38 passed in 0.12s =========================\n"
    )

    def _emit(self, text):
        p = self.write("canned.txt", text)
        return ["run", "--", PY, "-c", f"import sys; sys.stdout.write(open({str(p)!r}).read()); sys.exit(1)"]

    def test_pytest_like_selection_by_sniff(self):
        r = self.ult(*self._emit(self.PYTEST_OUT))
        self.assertEqual(r.code, 1)
        self.assertIn("family=pytest", r.out)
        self.assertIn("E       assert 3 == 4", r.out)
        self.assertIn("E       KeyError: 'zzz'", r.out)
        self.assertIn("_ test_widget_total _", r.out)
        self.assertIn("2 failed, 38 passed in 0.12s", r.out)
        self.assertIn("FAILED tests/test_a.py::test_widget_total", r.out)
        self.assertIn("omitted", r.out)
        self.assertLess(r.out.count("tests/test_a.py ........"), 5)

    def test_pytest_explicit_family(self):
        r = self.ult(*self._emit(self.PYTEST_OUT)[:1], "--family", "pytest", *self._emit(self.PYTEST_OUT)[1:])
        self.assertIn("family=pytest", r.out)

    JEST_OUT = (
        "".join(f" PASS  src/mod{i}.test.js\n" for i in range(200))
        + " FAIL  src/cart.test.js\n"
        "  ● Cart › computes total\n"
        "\n"
        "    expect(received).toBe(expected)\n"
        "\n"
        "    Expected: 42\n"
        "    Received: 41\n"
        "\n"
        "      at Object.<anonymous> (src/cart.test.js:10:20)\n"
        "\n"
        "Test Suites: 1 failed, 60 passed, 61 total\n"
        "Tests:       1 failed, 120 passed, 121 total\n"
        "Time:        3.2 s\n"
    )

    def test_jest_like_selection(self):
        r = self.ult(*self._emit(self.JEST_OUT))
        self.assertIn("family=jest", r.out)
        self.assertIn("● Cart › computes total", r.out)
        self.assertIn("Expected: 42", r.out)
        self.assertIn("Received: 41", r.out)
        self.assertIn("Test Suites: 1 failed, 60 passed, 61 total", r.out)
        self.assertIn("Tests:       1 failed, 120 passed, 121 total", r.out)
        self.assertLess(r.out.count("PASS"), 20)

    def test_unittest_run_real(self):
        self.write("t_mod.py", "import unittest\nclass T(unittest.TestCase):\n    def test_a(self):\n        self.assertEqual(1, 2)\n    def test_b(self):\n        pass\nif __name__=='__main__': unittest.main()\n")
        r = self.ult("run", "--", PY, "-m", "unittest", "t_mod")
        self.assertEqual(r.code, 1)
        self.assertIn("family=unittest", r.out)
        self.assertIn("FAIL: test_a", r.out)
        self.assertIn("AssertionError: 1 != 2", r.out)
        self.assertIn("FAILED (failures=1)", r.out)


if __name__ == "__main__":
    unittest.main()
