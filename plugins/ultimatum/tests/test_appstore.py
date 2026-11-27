"""`ult appstore check` on small Expo fixture projects, plus the app-store skill files."""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ultlib import appstore, route  # noqa: E402

ULT = ROOT / "scripts" / "ult"
FIX = ROOT / "tests" / "data" / "appstore"
SKILL = ROOT / "skills" / "app-store"


def codes(report, level=None):
    return {f["code"] for f in report["findings"] if level is None or f["level"] == level}


def run_ult(*args):
    return subprocess.run([sys.executable, str(ULT), "appstore", "check", *args],
                          capture_output=True, text=True, timeout=60)


class Fixture:
    """Copy a fixture to a temp folder so a test can change it."""

    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / self.name
        shutil.copytree(FIX / self.name, self.root)
        return self.root

    def __exit__(self, *exc):
        self.tmp.cleanup()

    @staticmethod
    def edit(root, name, fn):
        path = root / name
        data = json.loads(path.read_text())
        fn(data)
        path.write_text(json.dumps(data, indent=2))


class CleanProject(unittest.TestCase):
    def test_clean_project_exits_zero(self):
        res = run_ult("--root", str(FIX / "clean"))
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
        self.assertIn("0 fail, 0 warn", res.stdout)

    def test_json_output_shape(self):
        res = run_ult("--root", str(FIX / "clean"), "--json")
        data = json.loads(res.stdout)
        self.assertEqual(set(data), {"root", "config", "counts", "findings"})
        self.assertEqual(data["config"], "app.json")


class RiskyProject(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = appstore.check(FIX / "risky")

    def test_exit_one_with_findings(self):
        res = run_ult("--root", str(FIX / "risky"))
        self.assertEqual(res.returncode, 1)

    def test_missing_usage_string_for_installed_permission(self):
        self.assertIn("AS030", codes(self.report, "fail"))
        where = [f["where"] for f in self.report["findings"] if f["code"] == "AS030"]
        self.assertTrue(any("NSLocationWhenInUseUsageDescription" in w for w in where))

    def test_vague_usage_string(self):
        self.assertIn("AS031", codes(self.report, "warn"))

    def test_placeholder_bundle_id(self):
        self.assertIn("AS012", codes(self.report))

    def test_bad_privacy_manifest_entry(self):
        self.assertTrue({"AS042", "AS043"} <= codes(self.report, "fail"))

    def test_internal_production_profile(self):
        self.assertIn("AS062", codes(self.report, "fail"))

    def test_secret_in_eas_env(self):
        found = {f["where"]: f["level"] for f in self.report["findings"] if f["code"] == "AS092"}
        self.assertEqual(found.get("eas.json build.production.env.STRIPE_SECRET_KEY"), "fail")
        self.assertEqual(found.get("eas.json build.production.env.EXPO_PUBLIC_API_TOKEN"), "warn")

    def test_icon_size_and_alpha(self):
        self.assertTrue({"AS053", "AS054"} <= codes(self.report))

    def test_policy_risks(self):
        self.assertIn("AS080", codes(self.report))  # third-party sign-in, no Apple sign-in
        self.assertIn("AS081", codes(self.report))  # card payments, no IAP library

    def test_no_privacy_url_and_no_runtime_version(self):
        self.assertTrue({"AS070", "AS066", "AS068", "AS056"} <= codes(self.report))


class Changes(unittest.TestCase):
    def test_missing_bundle_id_fails(self):
        with Fixture("clean") as root:
            Fixture.edit(root, "app.json", lambda d: d["expo"]["ios"].pop("bundleIdentifier"))
            self.assertIn("AS010", codes(appstore.check(root), "fail"))

    def test_bad_marketing_version_fails(self):
        with Fixture("clean") as root:
            Fixture.edit(root, "app.json", lambda d: d["expo"].update(version="1.2.0-beta"))
            self.assertIn("AS021", codes(appstore.check(root), "fail"))

    def test_local_versions_without_build_number_warn(self):
        with Fixture("clean") as root:
            def local(d):
                d["cli"]["appVersionSource"] = "local"
                d["build"]["production"].pop("autoIncrement")
            Fixture.edit(root, "eas.json", local)
            self.assertIn("AS023", codes(appstore.check(root), "warn"))

    def test_plugin_without_permission_text_warns(self):
        with Fixture("clean") as root:
            def bare(d):
                d["expo"]["plugins"] = [p for p in d["expo"]["plugins"] if p[0] != "expo-camera"] + ["expo-camera"]
            Fixture.edit(root, "app.json", bare)
            self.assertIn("AS032", codes(appstore.check(root), "warn"))

    def test_signing_files_inside_project_fail(self):
        with Fixture("clean") as root:
            keys = root / "keys"
            keys.mkdir()
            (keys / "AuthKey_TEST.p8").write_text("test placeholder, not a key\n")
            Fixture.edit(root, "eas.json",
                         lambda d: d["submit"]["production"]["ios"].update(ascApiKeyPath="./keys/AuthKey_TEST.p8"))
            got = codes(appstore.check(root), "fail")
            self.assertTrue({"AS090", "AS093"} <= got, got)

    def test_private_key_text_in_config_fails(self):
        with Fixture("clean") as root:
            marker = "-----BEGIN " + "PRIVATE KEY-----"
            Fixture.edit(root, "app.json", lambda d: d["expo"].update(extra={"k": marker}))
            self.assertIn("AS091", codes(appstore.check(root), "fail"))

    def test_store_listing_limits(self):
        with Fixture("clean") as root:
            def long(d):
                info = d["apple"]["info"]["en-US"]
                info["subtitle"] = "x" * 31
                info["keywords"] = ["word" * 10] * 3
                info.pop("privacyPolicyUrl")
            Fixture.edit(root, "store.config.json", long)
            got = codes(appstore.check(root), "fail")
            self.assertTrue({"AS072", "AS074", "AS075"} <= got, got)

    def test_build_number_not_bumped_since_ref(self):
        if not shutil.which("git"):
            self.skipTest("git not installed")
        with Fixture("clean") as root:
            def local(d):
                d["cli"]["appVersionSource"] = "local"
                d["build"]["production"].pop("autoIncrement")
            Fixture.edit(root, "eas.json", local)
            Fixture.edit(root, "app.json", lambda d: d["expo"]["ios"].update(buildNumber="7"))
            env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@example.com",
                       GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@example.com")
            for cmd in (["init", "-q"], ["add", "-A"], ["commit", "-qm", "release 1.2.0 (7)"]):
                subprocess.run(["git", "-C", str(root), *cmd], check=True, env=env, capture_output=True)
            self.assertIn("AS025", codes(appstore.check(root, since="HEAD"), "fail"))
            Fixture.edit(root, "app.json", lambda d: d["expo"]["ios"].update(buildNumber="8"))
            self.assertNotIn("AS025", codes(appstore.check(root, since="HEAD")))


class BadInput(unittest.TestCase):
    def test_invalid_json_exits_two(self):
        res = run_ult("--root", str(FIX / "bad-json"))
        self.assertEqual(res.returncode, 2)
        self.assertIn("not valid JSON", res.stderr)

    def test_dynamic_config_only_exits_two_with_hint(self):
        res = run_ult("--root", str(FIX / "dynamic-only"))
        self.assertEqual(res.returncode, 2)
        self.assertIn("npx expo config --json", res.stderr)

    def test_resolved_config_flag(self):
        with Fixture("dynamic-only") as root:
            data = json.loads((FIX / "clean" / "app.json").read_text())["expo"]
            data["icon"] = None
            (root / "resolved.json").write_text(json.dumps(data))
            res = run_ult("--root", str(root), "--config", "resolved.json")
            self.assertEqual(res.returncode, 1)
            self.assertIn("AS050", res.stdout)

    def test_missing_folder_exits_two(self):
        self.assertEqual(run_ult("--root", "/no/such/folder/here").returncode, 2)


class Toolbelt(unittest.TestCase):
    def test_stdlib_only_and_no_network(self):
        text = (ROOT / "scripts" / "ultlib" / "appstore.py").read_text()
        imports = set(re.findall(r"^(?:from|import)\s+([a-zA-Z_]+)", text, re.M))
        self.assertLessEqual(imports, {"__future__", "json", "os", "re", "struct", "subprocess", "sys", "pathlib"})
        self.assertNotRegex(text, r"\b(urllib|http\.client|socket|requests)\b")

    def test_no_signing_files_or_keys_committed(self):
        bad = [p for p in ROOT.rglob("*") if p.suffix.lower() in appstore.SIGNING_SUFFIXES]
        self.assertEqual(bad, [])


class Routing(unittest.TestCase):
    def test_app_store_tasks_route_to_the_skill(self):
        for task in ("submit my Expo app to the App Store", "set up TestFlight for the beta",
                     "we got rejected in App Review, reply in Resolution Center",
                     "add a privacy manifest", "configure eas build profiles",
                     "ship the app to the Apple store", "bump the iOS build number"):
            with self.subTest(task=task):
                self.assertEqual(route.decide(task, root=None)["workflow"], "app-store")

    def test_other_tasks_do_not(self):
        for task in ("fix the failing date parser test", "add a store page to the website",
                     "write app store optimization keywords for the blog"):
            with self.subTest(task=task):
                self.assertNotEqual(route.decide(task, root=None)["workflow"], "app-store")

    def test_security_review_keeps_its_route(self):
        task = "security review of the App Store submission secrets"
        self.assertEqual(route.workflow_for(task, "sec-review", None), "default")
        self.assertEqual(route.workflow_for(task, "feature", None), "app-store")


class SkillFiles(unittest.TestCase):
    def test_skill_frontmatter_and_size(self):
        text = (SKILL / "SKILL.md").read_text()
        self.assertTrue(text.startswith("---\nname: app-store\n"))
        self.assertIn("description:", text.split("---")[1])
        self.assertLess(len(text.encode()), 20 * 1024)

    def test_every_reference_is_linked_and_exists(self):
        text = (SKILL / "SKILL.md").read_text()
        linked = set(re.findall(r"references/([a-z0-9-]+\.md)", text))
        on_disk = {p.name for p in (SKILL / "references").glob("*.md")}
        self.assertEqual(linked, on_disk)

    def test_references_open_with_when_to_read(self):
        for path in (SKILL / "references").glob("*.md"):
            lines = path.read_text().splitlines()
            with self.subTest(file=path.name):
                self.assertTrue(lines[0].startswith("# "))
                self.assertTrue(lines[2].startswith("Read "))
                self.assertLess(path.stat().st_size, 15 * 1024)

    def test_links_are_https(self):
        for path in [SKILL / "SKILL.md", *(SKILL / "references").glob("*.md")]:
            for url in re.findall(r"\bhttps?://[^\s)`>\]|]+", path.read_text()):
                with self.subTest(file=path.name, url=url):
                    self.assertTrue(url.startswith("https://"))

    def test_guides_say_to_fetch_guidelines_not_quote_them(self):
        text = (SKILL / "references" / "review-check.md").read_text()
        self.assertIn("https://developer.apple.com/app-store/review/guidelines/", text)
        self.assertRegex(text, r"(?i)fetch")

    def test_every_check_code_is_documented(self):
        src = (ROOT / "scripts" / "ultlib" / "appstore.py").read_text()
        doc = (SKILL / "references" / "checker.md").read_text()
        for code in sorted(set(re.findall(r'"(AS\d{3})"', src))):
            with self.subTest(code=code):
                self.assertIn(code, doc)

    def test_router_points_to_skill(self):
        work = (ROOT / "skills" / "work" / "SKILL.md").read_text()
        self.assertIn("app-store", work)
        self.assertLess(len(work.encode()), 20 * 1024)


if __name__ == "__main__":
    unittest.main()
