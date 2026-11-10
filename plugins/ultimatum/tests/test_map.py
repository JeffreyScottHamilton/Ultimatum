import json
import unittest

from _harness import UltCase


class TestMap(UltCase):
    def setUp(self):
        super().setUp()
        self.write("app/server.py", (
            "import sqlite3\nfrom flask import Flask\napp = Flask(__name__)\n\n"
            "@app.route('/users/<int:uid>')\ndef user(uid):\n    return ''\n\n"
            "@app.get('/health')\ndef health():\n    return 'ok'\n\n"
            "def get_db():\n    return sqlite3.connect('x.db')\n\n"
            "def require_login(f):\n    return f\n\n"
            "def check_permission(user):\n    return user.is_admin\n\n"
            "if __name__ == '__main__':\n    app.run()\n"))
        self.write("tests/test_server.py", "@app.route('/fake-test-route')\ndef t():\n    sqlite3.connect('t.db')\n")
        self.write("web/api.js", "app.get('/api/items', (req, res) => {});\nrouter.post('/api/items', h);\n")
        self.write("node_modules/x/index.js", "app.get('/nm-route', h);\n")
        self.write("package.json", json.dumps({"scripts": {"test": "jest", "build": "tsc"}}))
        self.write(".github/workflows/ci.yml", "on: push\n")
        self.write("Dockerfile", "FROM python\n")
        self.write("README.md", "# hi\n")

    def test_build_and_files(self):
        r = self.ult("map", "build")
        self.assertEqual(r.code, 0, r.all)
        mp = self.root / ".ultimatum" / "map.json"
        self.assertTrue(mp.exists())
        m = json.loads(mp.read_text())
        self.assertTrue(any("app/server.py:5" in x and "/users/" in x for x in m["routes"]), m["routes"])
        self.assertTrue(any("/health" in x for x in m["routes"]))
        self.assertTrue(any("web/api.js:1" in x for x in m["routes"]))
        self.assertTrue(any("web/api.js:2" in x for x in m["routes"]))
        self.assertFalse(any("test" in x.split(":")[0] for x in m["routes"]), m["routes"])
        self.assertFalse(any("fake-test-route" in x for x in m["routes"]))
        self.assertFalse(any("nm-route" in x or "node_modules" in x for sect in ("routes", "auth", "data_stores") for x in m[sect]))
        self.assertTrue(any("sqlite3.connect" in x and x.startswith("app/server.py:14") for x in m["data_stores"]), m["data_stores"])
        self.assertFalse(any("tests/" in x for x in m["data_stores"]))
        self.assertTrue(any("require_login" in x for x in m["auth"]))
        self.assertTrue(any("__main__" in x for x in m["entry_points"]))
        self.assertIn("tests/test_server.py", m["tests"])
        self.assertIn("package.json", m["manifests"])
        self.assertIn("Dockerfile", m["infra"])
        self.assertIn("README.md", m["docs"])
        self.assertEqual(m["scripts"]["package.json"]["test"], "jest")
        self.assertFalse(any("node_modules" in x for x in m["manifests"] + m["tests"]))

    def test_auth_snake_case_identifiers(self):
        # BUG: repomap.py LINE_RULES["auth"] uses \\b(...permission|role|session|current_user...)\\b so
        # `def check_permission(user):`, `def get_current_user():`, `user_session = ...` are NOT
        # recognised (underscore is a word char, so no boundary before the keyword).
        self.write("authz.py", "def check_permission(user):\n    pass\n\ndef get_current_user():\n    pass\n")
        self.ult("map", "build")
        m = json.loads((self.root / ".ultimatum" / "map.json").read_text())
        joined = "\n".join(m["auth"])
        self.assertIn("authz.py:1", joined)
        self.assertIn("authz.py:4", joined)

    def test_ci_detected_without_git(self):
        # BUG: search.py:50 os.walk fallback drops every dot-directory, so outside a git repo
        # `.github/workflows/ci.yml` is never listed and map["ci"] stays empty.
        self.ult("map", "build")
        m = json.loads((self.root / ".ultimatum" / "map.json").read_text())
        self.assertIn(".github/workflows/ci.yml", m["ci"])

    def test_ci_detected_in_git(self):
        self.git_init()
        self.ult("map", "build")
        m = json.loads((self.root / ".ultimatum" / "map.json").read_text())
        self.assertIn(".github/workflows/ci.yml", m["ci"])

    def test_summary_short(self):
        self.ult("map", "build")
        r = self.ult("map", "summary")
        self.assertEqual(r.code, 0, r.all)
        self.assertLessEqual(len(r.out.splitlines()), 40)
        self.assertIn("routes (", r.out)
        self.assertIn("data_stores", r.out)
        self.assertIn("scripts package.json", r.out)

    def test_summary_autobuilds(self):
        r = self.ult("map", "summary")
        self.assertEqual(r.code, 0, r.all)
        self.assertTrue((self.root / ".ultimatum" / "map.json").exists())

    def test_query_section_and_keyword(self):
        self.ult("map", "build")
        r = self.ult("map", "query", "routes")
        self.assertIn("/health", r.out)
        self.assertNotIn("fake-test-route", r.out)
        r = self.ult("map", "query", "sqlite3")
        self.assertEqual(r.code, 0)
        self.assertIn("[data_stores]", r.out)
        r = self.ult("map", "query", "ZZZNOPE")
        self.assertEqual(r.code, 1)

    def test_query_limit(self):
        self.ult("map", "build")
        r = self.ult("map", "query", "routes", "--limit", "1")
        self.assertIn("more (--limit)", r.out)

    def test_query_term_with_regex_chars(self):
        self.ult("map", "build")
        r = self.ult("map", "query", "a.b(c")
        self.assertNotIn("Traceback", r.err)

    def test_query_empty_term(self):
        # BUG candidate: empty term should not dump everything / crash
        self.ult("map", "build")
        r = self.ult("map", "query")
        self.assertNotIn("Traceback", r.err, r.err)

    def test_route_caps(self):
        self.write("big.py", "".join(f"@app.get('/r{i}')\ndef f{i}(): pass\n" for i in range(400)))
        self.ult("map", "build")
        m = json.loads((self.root / ".ultimatum" / "map.json").read_text())
        self.assertEqual(len(m["routes"]), 200)

    def test_map_json_private(self):
        import stat
        self.ult("map", "build")
        self.assertEqual(stat.S_IMODE((self.root / ".ultimatum" / "map.json").stat().st_mode), 0o600)

    def test_secrets_in_map_lines_redacted(self):
        # map stores source lines; a secret on a matched line should not be persisted/printed
        secret = "gh" + "p_" + "Q1w2E3r4T5" * 4
        self.write("auth_cfg.py", f"AUTH_TOKEN = login('{secret}')\n")
        r = self.ult("map", "build")
        m = (self.root / ".ultimatum" / "map.json").read_text()
        out = self.ult("map", "query", "login").out
        self.assertNotIn(secret, out)  # BUG: repomap.py:98 stores raw source lines; `ult map query` prints them unredacted (and map.json holds them)
        self.assertNotIn(secret, m)

    def test_git_repo_build(self):
        self.git_init()
        self.git("add", "-A")
        r = self.ult("map", "build")
        self.assertEqual(r.code, 0, r.all)
        m = json.loads((self.root / ".ultimatum" / "map.json").read_text())
        self.assertFalse(any("node_modules" in x for x in m["routes"]))
        self.assertFalse(any(x.startswith(".ultimatum") for x in m["docs"] + m["manifests"]))


if __name__ == "__main__":
    unittest.main()
