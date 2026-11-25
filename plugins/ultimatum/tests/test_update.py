"""Tests for `ult update`: status, setup --apply (settings.json) and migrate."""
import json
import os
import unittest
from pathlib import Path
from unittest import mock

from _harness import UltCase

PLUGIN_JSON = Path(__file__).resolve().parents[1] / ".claude-plugin" / "plugin.json"
EXPECTED_ENTRY = {"source": {"source": "github", "repo": "JeffreyScottHamilton/Ultimatum"}, "autoUpdate": True}


class UpdateCase(UltCase):
    def setUp(self):
        super().setUp()
        self.home = self.tmp / "home"
        self.home.mkdir()
        patcher = mock.patch.dict(os.environ, {"HOME": str(self.home)})
        patcher.start()
        self.addCleanup(patcher.stop)
        for k in ("ULTIMATUM_OBSERVE", "ULTIMATUM_STATE_DIR", "CLAUDE_CONFIG_DIR"):
            os.environ.pop(k, None)
        self.settings = self.home / ".claude" / "settings.json"

    def write_settings(self, data):
        self.settings.parent.mkdir(parents=True, exist_ok=True)
        text = json.dumps(data, indent=2) + "\n"
        self.settings.write_text(text)
        return text

    def backups(self):
        return sorted(self.settings.parent.glob("settings.json.bak-*"))

    def running_version(self):
        return json.loads(PLUGIN_JSON.read_text())["version"]


class TestSetupApply(UpdateCase):
    def test_creates_settings_when_absent_and_is_idempotent(self):
        r = self.ult("update", "setup", "--apply")
        self.assertEqual(r.code, 0, r.all)
        self.assertIn("auto-update on", r.out)
        data = json.loads(self.settings.read_text())
        self.assertEqual(data["extraKnownMarketplaces"]["ultimatum"], EXPECTED_ENTRY)
        self.assertEqual(self.backups(), [])

        before = self.settings.read_text()
        r = self.ult("update", "setup", "--apply")
        self.assertEqual(r.code, 0, r.all)
        self.assertIn("already on", r.out)
        self.assertEqual(self.settings.read_text(), before)
        self.assertEqual(self.backups(), [])

    def test_preserves_other_keys_and_backs_up_first(self):
        original = self.write_settings({
            "theme": "dark",
            "permissions": {"allow": ["Bash(ls)"]},
            "extraKnownMarketplaces": {"other": {"source": {"source": "github", "repo": "x/y"}}},
        })
        r = self.ult("update", "setup", "--apply")
        self.assertEqual(r.code, 0, r.all)
        data = json.loads(self.settings.read_text())
        self.assertEqual(data["theme"], "dark")
        self.assertEqual(data["permissions"], {"allow": ["Bash(ls)"]})
        self.assertEqual(data["extraKnownMarketplaces"]["other"], {"source": {"source": "github", "repo": "x/y"}})
        self.assertEqual(data["extraKnownMarketplaces"]["ultimatum"], EXPECTED_ENTRY)
        backups = self.backups()
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(), original)

    def test_sets_autoupdate_on_existing_entry_keeping_its_fields(self):
        self.write_settings({"extraKnownMarketplaces": {"ultimatum": {
            "source": {"source": "github", "repo": "fork/Ultimatum"}, "autoUpdate": False, "note": "keep"}}})
        self.assertEqual(self.ult("update", "setup", "--apply").code, 0)
        entry = json.loads(self.settings.read_text())["extraKnownMarketplaces"]["ultimatum"]
        self.assertIs(entry["autoUpdate"], True)
        self.assertEqual(entry["note"], "keep")
        self.assertEqual(entry["source"]["repo"], "fork/Ultimatum")

    def test_invalid_json_is_left_alone(self):
        self.settings.parent.mkdir(parents=True)
        self.settings.write_text("{not json")
        r = self.ult("update", "setup", "--apply")
        self.assertEqual(r.code, 1)
        self.assertIn("not valid JSON", r.out)
        self.assertEqual(self.settings.read_text(), "{not json")
        self.assertEqual(self.backups(), [])

    def test_setup_without_apply_only_prints_steps(self):
        r = self.ult("update", "setup")
        self.assertEqual(r.code, 0, r.all)
        self.assertIn("/reload-plugins", r.out)
        self.assertIn("claude.ai/customize/plugins", r.out)
        self.assertLessEqual(len(r.out.strip().splitlines()), 8)
        self.assertFalse(self.settings.exists())


class TestStatus(UpdateCase):
    def test_reports_running_version_and_unset_autoupdate(self):
        r = self.ult("update", "status")
        self.assertEqual(r.code, 0, r.all)
        self.assertIn(f"running: {self.running_version()}", r.out)
        self.assertIn("auto-update (ultimatum marketplace): not set", r.out)
        self.assertIn("run `ult update setup --apply`", r.out)

    def test_newer_marketplace_copy_suggests_reload(self):
        copy = self.home / ".claude" / "plugins" / "marketplaces" / "ultimatum-mkt" / "plugins" / "ultimatum" / ".claude-plugin"
        copy.mkdir(parents=True)
        (copy / "plugin.json").write_text(json.dumps({"name": "ultimatum", "version": "9.9.9"}))
        self.write_settings({"extraKnownMarketplaces": {"ultimatum": EXPECTED_ENTRY}})
        r = self.ult("update", "status")
        self.assertIn("marketplace copy: 9.9.9", r.out)
        self.assertIn("auto-update (ultimatum marketplace): on", r.out)
        self.assertIn("/reload-plugins", r.out)


class TestMigrate(UpdateCase):
    def test_creates_missing_files_once_then_nothing_to_do(self):
        r = self.ult("update", "migrate")
        self.assertEqual(r.code, 0, r.all)
        self.assertIn("created knowledge.md", r.out)
        self.assertTrue((self.root / ".ultimatum" / "proposals").is_dir())
        r = self.ult("update", "migrate")
        self.assertEqual(r.out.strip(), "migrate: nothing to do")

    def test_never_rewrites_existing_knowledge(self):
        self.write(".ultimatum/knowledge.md", "# Mine\n- keep me\n")
        self.ult("update", "migrate")
        self.assertEqual((self.root / ".ultimatum" / "knowledge.md").read_text(), "# Mine\n- keep me\n")


if __name__ == "__main__":
    unittest.main()
