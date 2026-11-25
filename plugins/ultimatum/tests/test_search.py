import unittest

from _harness import UltCase


class SearchBase(UltCase):
    def setUp(self):
        super().setUp()
        self.write("app/main.py", "import os\n\nclass Widget:\n    pass\n\ndef make_widget(n):\n    return Widget()\n\nMAX_SIZE = 10\n\nasync def fetch_data():\n    make_widget(1)\n")
        self.write("web/app.js", "function makeWidget(a) {\n  return a;\n}\nconst fetchData = async () => makeWidget(1);\nclass Widget {}\nexport default makeWidget;\n")
        self.write("srv/server.go", "package main\n\ntype Widget struct{}\n\nfunc MakeWidget() Widget { return Widget{} }\n\nfunc (w *Widget) Run() {}\n\nfunc main() { MakeWidget() }\n")
        self.write("node_modules/dep/index.js", "function makeWidget() {}\nclass Widget {}\n// make_widget makeWidget\n")
        self.write("vendor/v.py", "def make_widget(): pass\n")
        self.write("tests/test_main.py", "from app.main import make_widget\n\ndef test_it():\n    make_widget(2)\n")
        self.write("README.md", "make_widget docs\n")


class TestSearch(SearchBase):
    def test_search_basic_and_skip_dirs(self):
        r = self.ult("search", "make_?[wW]idget")
        self.assertEqual(r.code, 0, r.all)
        self.assertIn("app/main.py", r.out)
        self.assertNotIn("node_modules", r.out)
        self.assertNotIn("vendor/", r.out)

    def test_search_no_match_exit1(self):
        r = self.ult("search", "zzzz_nothing_zzzz")
        self.assertEqual(r.code, 1)

    def test_search_glob_path_ignore_case(self):
        r = self.ult("search", "WIDGET", "-i", "--glob", "*.go")
        self.assertIn("srv/server.go", r.out)
        self.assertNotIn("app/main.py", r.out)
        r = self.ult("search", "Widget", "--path", "web")
        self.assertIn("web/app.js", r.out)
        self.assertNotIn("app/main.py", r.out)

    def test_search_in_git_repo_skips_node_modules(self):
        self.git_init()
        self.git("add", "-A")
        r = self.ult("search", "makeWidget")
        self.assertNotIn("node_modules", r.out)
        self.assertIn("web/app.js", r.out)

    def test_search_untracked_node_modules_in_git_repo(self):
        # even when not gitignored and untracked, node_modules must be skipped
        self.git_init()
        r = self.ult("search", "makeWidget")
        self.assertNotIn("node_modules", r.out)

    def test_tests_ranked_after_source(self):
        r = self.ult("search", "make_widget", "--glob", "*.py")
        names = [l.split()[0] for l in r.out.splitlines() if l and not l.startswith((" ", "["))]
        self.assertLess(names.index("app/main.py"), names.index("tests/test_main.py"))

    def test_max_files_cap(self):
        for i in range(40):
            self.write(f"many/f{i}.py", "needle_token = 1\n")
        r = self.ult("search", "needle_token", "--max-files", "5")
        files = [l for l in r.out.splitlines() if l.startswith("many/")]
        self.assertEqual(len(files), 5, r.out)
        self.assertIn("35 more file(s) omitted", r.out)

    def test_per_file_cap(self):
        self.write("big.py", "".join(f"hit_{i} = 'zork'\n" for i in range(30)))
        r = self.ult("search", "zork", "--per-file", "3")
        self.assertEqual(sum(1 for l in r.out.splitlines() if l.startswith("  ") and ": " in l and "more" not in l), 3, r.out)
        self.assertIn("+27 more", r.out)

    def test_bad_regex_no_traceback(self):
        r = self.ult("search", "(unclosed")
        self.assertNotIn("Traceback", r.err, r.err)

    def test_search_output_redacted(self):
        secret = "gh" + "p_" + "Q1w2E3r4T5" * 4
        self.write("conf.py", f"T = '{secret}'\n")
        r = self.ult("search", "ghp_")
        self.assertNotIn(secret, r.out)

    def test_summary_pluralisation(self):
        r = self.ult("search", "MAX_SIZE")
        self.assertIn("1 match in 1 file(s)", r.out)

    def test_symbols(self):
        r = self.ult("symbols", "make_widget")
        self.assertEqual(r.code, 0, r.all)
        self.assertIn("app/main.py", r.out)
        self.assertIn("6: def make_widget(n):", r.out)
        self.assertNotIn("node_modules", r.out)
        self.assertNotIn("vendor", r.out)
        self.assertNotIn("README", r.out)
        self.assertNotIn("test_main.py", r.out)  # only a call/import there, no def

    def test_symbols_js_go_classes(self):
        r = self.ult("symbols", "makeWidget")
        self.assertIn("web/app.js", r.out)
        r = self.ult("symbols", "Widget")
        self.assertIn("app/main.py", r.out)
        self.assertIn("web/app.js", r.out)
        self.assertIn("srv/server.go", r.out)
        r = self.ult("symbols", "MakeWidget")
        self.assertIn("srv/server.go", r.out)
        r = self.ult("symbols", "Run")
        self.assertIn("srv/server.go", r.out)
        r = self.ult("symbols", "MAX_SIZE")
        self.assertIn("app/main.py", r.out)
        r = self.ult("symbols", "fetch_data")
        self.assertIn("async def fetch_data", r.out)
        r = self.ult("symbols", "fetchData")
        self.assertIn("web/app.js", r.out)

    def test_symbols_name_is_literal(self):
        r = self.ult("symbols", "make.widget")
        self.assertEqual(r.code, 1, r.out)
        r = self.ult("symbols", "make_widget(")
        self.assertNotIn("Traceback", r.err)

    def test_symbols_regex_mode(self):
        r = self.ult("symbols", "make_w.*", "--regex")
        self.assertIn("app/main.py", r.out)

    def test_symbols_missing(self):
        r = self.ult("symbols", "NoSuchThing")
        self.assertEqual(r.code, 1)

    def test_refs(self):
        r = self.ult("refs", "make_widget")
        self.assertEqual(r.code, 0, r.all)
        self.assertIn("app/main.py", r.out)
        self.assertIn("tests/test_main.py", r.out)
        self.assertNotIn("node_modules", r.out)
        self.assertNotIn("vendor", r.out)

    def test_refs_word_boundary(self):
        self.write("wb.py", "make_widget_extra()\nxmake_widget()\nmake_widget()\n")
        r = self.ult("refs", "make_widget", "--path", ".", "--glob", "wb.py")
        self.assertIn("3: make_widget()", r.out)
        self.assertNotIn("make_widget_extra", r.out)
        self.assertNotIn("xmake_widget", r.out)

    def test_refs_special_chars(self):
        r = self.ult("refs", "a.b(")
        self.assertNotIn("Traceback", r.err, r.err)
        self.assertEqual(r.code, 1)

    def test_python_fallback_when_no_rg(self):
        # run with a PATH lacking rg to exercise grep(); git still needed, so symlink it
        import os, shutil, tempfile
        d = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, d, True)
        os.symlink(shutil.which("git"), os.path.join(d, "git"))
        import subprocess, sys
        from _harness import ULT
        e = self.env()
        e["PATH"] = d
        cp = subprocess.run([sys.executable, ULT, "search", "make_?widget", "-i"], cwd=self.root, env=e, capture_output=True, text=True)
        self.assertEqual(cp.returncode, 0, cp.stderr)
        self.assertIn("app/main.py", cp.stdout)
        self.assertNotIn("node_modules", cp.stdout)
        self.assertNotIn("vendor/", cp.stdout)

    def test_dotdir_scope_and_scope_escape(self):
        r = self.ult("search", "Widget", "--path", "../")
        self.assertNotIn("Traceback", r.err, r.err[-300:])


if __name__ == "__main__":
    unittest.main()
