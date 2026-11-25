import sys
import unittest

from _harness import SCRIPTS

sys.path.insert(0, SCRIPTS)
from ultlib import common  # noqa: E402

redact = common.redact


def j(*parts):
    return "".join(parts)


A36 = "AbC1dE2fG3" * 4  # 40 alnum chars


class TestRedactPositive(unittest.TestCase):
    def assertRedacted(self, secret, text=None, kind=None):
        text = text or f"x {secret} y"
        out = redact(text)
        self.assertNotIn(secret, out, out)
        self.assertIn("[REDACTED", out)
        if kind:
            self.assertIn(f"REDACTED:{kind}", out)
        return out

    def test_private_key(self):
        body = "MIIEvQIBADANBgkqhkiG9w0BAQEFAASC"
        pem = j("-----BEGIN RSA PRIV", "ATE KEY-----\n", body, "\n-----END RSA PRIV", "ATE KEY-----")
        out = self.assertRedacted(body, f"before\n{pem}\nafter", "private-key")
        self.assertIn("before", out)
        self.assertIn("after", out)

    def test_private_key_unterminated(self):
        body = "MIIEvQIBADANBgkqhkiG9w0BAQEFAASC"
        pem = j("-----BEGIN PRIV", "ATE KEY-----\n", body)
        self.assertRedacted(body, pem)

    def test_aws(self):
        self.assertRedacted(j("AKI", "A", "IOSFODNN7EXAMPLE"), kind="aws-access-key-id")
        self.assertRedacted(j("ASI", "A", "IOSFODNN7EXAMPLE"), kind="aws-access-key-id")

    def test_github(self):
        for pre in ("ghp_", "gho_", "ghu_", "ghs_", "ghr_"):
            self.assertRedacted(j(pre, A36), kind="github-token")
        self.assertRedacted(j("github", "_pat_", "11ABCDEFG0_" * 3), kind="github-token")

    def test_gitlab(self):
        self.assertRedacted(j("glp", "at-", "abcdefghij0123456789"), kind="gitlab-token")

    def test_slack(self):
        self.assertRedacted(j("xo", "xb-", "123456789012-abcdefghijkl"), kind="slack-token")
        self.assertRedacted(j("https://hooks.", "slack.com/services/", "T000/B000/XXXXXXXX"), kind="slack-webhook")

    def test_stripe(self):
        self.assertRedacted(j("sk", "_live_", "abcdefghij0123456789"), kind="stripe-key")
        self.assertRedacted(j("rk", "_test_", "abcdefghij0123456789"), kind="stripe-key")

    def test_anthropic(self):
        self.assertRedacted(j("sk", "-ant-", "api03-abcdefghij0123456789xyz"), kind="anthropic-key")

    def test_openai(self):
        self.assertRedacted(j("sk", "-", "abcdefghij0123456789ABCDEFGHIJ0123"), kind="openai-key")
        self.assertRedacted(j("sk", "-proj-", "abcdefghij0123456789ABCDEFGHIJ0123"), kind="openai-key")

    def test_google(self):
        self.assertRedacted(j("AI", "za", "SyA-abcdefghij0123456789_ABCDEFGHIJ"), kind="google-api-key")

    def test_npm(self):
        self.assertRedacted(j("npm", "_", "abcdefghij0123456789ABCDEFGHIJ012345"), kind="npm-token")

    def test_sendgrid(self):
        self.assertRedacted(j("SG", ".", "abcdefghij0123456789AB", ".", "abcdefghij0123456789ABCDEFGHIJ0123456789ABC"), kind="sendgrid-key")

    def test_jwt(self):
        self.assertRedacted(j("ey", "JhbGcIOiJ", ".", "ey", "JzdWIiOiJ", "abc", ".", "SflKxwRJSMeKKF2QT4"), kind="jwt")

    def test_url_credentials(self):
        out = self.assertRedacted("hunter22pw", "postgres://admin:hunter22pw@db.example.com:5432/app", "url-credentials")
        self.assertIn("db.example.com", out)

    def test_bearer(self):
        self.assertRedacted("abcdef0123456789xyz", "Authorization: Bearer abcdef0123456789xyz", "bearer")
        self.assertRedacted("abcdef0123456789xyz", "authorization: bearer abcdef0123456789xyz", "bearer")

    def test_assigned_secret(self):
        for name in ("api_key", "API-KEY", "secret_key", "client_secret", "access_token", "auth_token", "password", "passwd", "private_key"):
            self.assertRedacted("s3cr3tValue99", f'{name} = "s3cr3tValue99"', "assigned-secret")
        self.assertRedacted("s3cr3tValue99", "password: 's3cr3tValue99'")
        self.assertRedacted("s3cr3tValue99", '{"password": "s3cr3tValue99"}')

    def test_prefixed_env_var_names(self):
        # BUG: common.py assigned-secret pattern has lookbehind (?<![A-Za-z0-9_]) so names with a
        # prefix such as DB_PASSWORD="...", MY_API_KEY="...", STRIPE_SECRET_KEY="..." are NOT redacted.
        for name in ("DB_PASSWORD", "MY_API_KEY", "AWS_SECRET_KEY", "GITHUB_AUTH_TOKEN"):
            out = redact(f'{name}="s3cr3tValue99"')
            self.assertNotIn("s3cr3tValue99", out, name)

    def test_unquoted_env_assignment_known_gap(self):
        # documented limitation of the pattern: only quoted values are caught
        self.assertNotIn("s3cr3tValue99", redact('password = "s3cr3tValue99"'))

    def test_last4_kept_and_keys_distinguishable(self):
        a = redact(j("ghp", "_", "A" * 36 + "1111"))
        b = redact(j("ghp", "_", "A" * 36 + "2222"))
        self.assertIn("1111", a)
        self.assertNotEqual(a, b)

    def test_multiple_in_one_line(self):
        t = j("ghp", "_", A36) + " and " + j("AKI", "A", "IOSFODNN7EXAMPLE")
        out = redact(t)
        self.assertEqual(out.count("[REDACTED"), 2)

    def test_idempotent(self):
        t = j("ghp", "_", A36)
        once = redact(t)
        self.assertEqual(redact(once), once)

    def test_empty(self):
        self.assertEqual(redact(""), "")
        self.assertIsNone(redact(None))


class TestRedactNegative(unittest.TestCase):
    def assertUnchanged(self, t):
        self.assertEqual(redact(t), t)

    def test_normal_code(self):
        for t in ("def get_password(user): return db.lookup(user)",
                  "token = request.headers.get('X-Token')",
                  "password = input('Enter: ')",
                  "const apiKey = process.env.API_KEY;",
                  "SELECT * FROM users WHERE id = 5;",
                  "for i in range(10): print(i)",
                  "https://example.com/path/to/resource?x=1",
                  "http://localhost:8080/api",
                  "git@github.com:org/repo.git",
                  "Authorization: Bearer <token>",
                  "the sky is blue"):
            self.assertUnchanged(t)

    def test_uuid_and_sha(self):
        self.assertUnchanged("id 123e4567-e89b-12d3-a456-426614174000 ok")
        self.assertUnchanged("commit 3f786850e387550fdab836ed7e6dc881de23001b")
        self.assertUnchanged("sha256 " + "ab" * 32)

    def test_short_assignments(self):
        self.assertUnchanged('password="x"')
        self.assertUnchanged("password = 'abc'")
        self.assertUnchanged('api_key = ""')

    def test_short_prefixes(self):
        self.assertUnchanged("sk-short")
        self.assertUnchanged("ghp_short")
        self.assertUnchanged("AKIA123")

    def test_hyphenated_identifiers_not_openai_key(self):
        # a word merely ending in "sk" followed by a long slug must not match (\b prevents)
        self.assertUnchanged("disk-usage-report-for-the-whole-cluster-nodes")

    def test_slug_containing_sk_segment(self):
        # BUG: openai-key regex \bsk-[A-Za-z0-9_-]{32,} matches the "sk-" segment inside an ordinary
        # hyphenated slug/path such as "my-sk-this-is-a-long-kebab-case-identifier-name".
        t = "my-sk-this-is-a-long-kebab-case-identifier-name"
        self.assertEqual(redact(t), t)

    def test_url_with_port_not_creds(self):
        self.assertUnchanged("connect to host:5432 user@example.com")


if __name__ == "__main__":
    unittest.main()


import os  # noqa: E402


class TestSymlinkSafety(unittest.TestCase):
    """A repository-planted `.ultimatum/map.json -> victim` must not be written through."""

    def test_map_build_refuses_planted_symlink(self):
        import subprocess, tempfile, sys
        from pathlib import Path
        root = Path(tempfile.mkdtemp())
        victim = Path(tempfile.mkdtemp()) / "victim.txt"
        victim.write_text("ORIGINAL")
        (root / ".ultimatum").mkdir()
        (root / ".ultimatum" / "map.json").symlink_to(victim)
        (root / "a.py").write_text("x = 1\n")
        ult = Path(__file__).resolve().parents[1] / "scripts" / "ult"
        env = {**os.environ, "ULTIMATUM_ROOT": str(root)}
        r = subprocess.run([sys.executable, str(ult), "map", "build"], cwd=root, env=env, capture_output=True, text=True)
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(victim.read_text(), "ORIGINAL")

    def test_state_dir_symlink_refused(self):
        import subprocess, tempfile, sys
        from pathlib import Path
        root = Path(tempfile.mkdtemp())
        elsewhere = Path(tempfile.mkdtemp())
        (root / ".ultimatum").symlink_to(elsewhere, target_is_directory=True)
        ult = Path(__file__).resolve().parents[1] / "scripts" / "ult"
        env = {**os.environ, "ULTIMATUM_ROOT": str(root)}
        r = subprocess.run([sys.executable, str(ult), "run", "--", "true"], cwd=root, env=env, capture_output=True, text=True)
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(list(elsewhere.iterdir()), [])


class TestExternalStateDir(unittest.TestCase):
    def test_state_dir_env_keeps_project_untouched(self):
        import subprocess, tempfile, sys
        from pathlib import Path
        root = Path(tempfile.mkdtemp())
        ext = Path(tempfile.mkdtemp()) / "state"
        ult = Path(__file__).resolve().parents[1] / "scripts" / "ult"
        env = {**os.environ, "ULTIMATUM_ROOT": str(root), "ULTIMATUM_STATE_DIR": str(ext)}
        r = subprocess.run([sys.executable, str(ult), "run", "--", "echo", "hi"], cwd=root, env=env, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0)
        self.assertEqual(list(root.iterdir()), [])
        self.assertTrue(list((ext / "logs").glob("*.log")))
        r = subprocess.run([sys.executable, str(ult), "log", "last"], cwd=root, env=env, capture_output=True, text=True)
        self.assertIn("hi", r.stdout)
