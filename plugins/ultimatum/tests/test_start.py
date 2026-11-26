"""The SessionStart check (ult-start) and `ult context --cap`."""
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from _harness import PY, REPO, SCRIPTS

START = os.path.join(SCRIPTS, "ult-start")
ULT = os.path.join(SCRIPTS, "ult")


class StartCheck(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.env = {k: v for k, v in os.environ.items()
                    if k not in ("CLAUDE_CODE_AUTO_COMPACT_WINDOW", "ULTIMATUM_START")}
        self.env["CLAUDE_CONFIG_DIR"] = str(self.tmp)

    def start(self, model=None, **env):
        data = json.dumps({"model": model, "cwd": str(self.tmp)})
        cp = subprocess.run([PY, START], input=data, capture_output=True, text=True,
                            env={**self.env, **env}, timeout=30)
        self.assertEqual(cp.returncode, 0, cp.stderr)
        return json.loads(cp.stdout)["systemMessage"] if cp.stdout.strip() else ""

    def settings(self, **data):
        (self.tmp / "settings.json").write_text(json.dumps(data))

    def test_ready_line_has_the_plugin_version(self):
        version = json.loads((REPO / "plugins/ultimatum/.claude-plugin/plugin.json").read_text())["version"]
        msg = self.start("claude-opus-5-5")
        self.assertIn(f"Ultimatum {version} ready", msg)
        self.assertNotIn("plugins:", msg)
        self.assertIn("context: 200K (model default)", msg)

    def test_1m_chat_without_a_cap_is_named_with_the_fix(self):
        msg = self.start("claude-opus-5-5[1m]")
        self.assertIn("not held to 200K", msg)
        self.assertIn("ult context --cap 200000", msg)

    def test_cap_from_env_or_settings_counts(self):
        self.assertIn("held to 200K", self.start("claude-opus-5-5[1m]", CLAUDE_CODE_AUTO_COMPACT_WINDOW="200000"))
        self.settings(autoCompactWindow=200000)
        self.assertIn("held to 200K", self.start("claude-opus-5-5[1m]"))

    def test_off_switch_and_bad_input_never_break_the_session(self):
        self.assertEqual(self.start(ULTIMATUM_START="0"), "")
        cp = subprocess.run([PY, START], input="not json", capture_output=True, text=True, env=self.env, timeout=30)
        self.assertEqual(cp.returncode, 0)
        self.assertIn("ready", cp.stdout)

    def test_hook_is_wired_for_new_chats(self):
        hooks = json.loads((REPO / "plugins/ultimatum/hooks/hooks.json").read_text())["hooks"]["SessionStart"]
        new = [h["command"] for e in hooks if e["matcher"] == "startup|clear" for h in e["hooks"]]
        self.assertTrue(any("ult-start" in c for c in new))

    def test_cap_command_keeps_other_settings(self):
        self.settings(enabledPlugins={"ultimatum@ultimatum": True})
        cp = subprocess.run([PY, ULT, "context", "--cap", "200000"], capture_output=True, text=True,
                            env=self.env, timeout=30)
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)
        data = json.loads((self.tmp / "settings.json").read_text())
        self.assertEqual(data["autoCompactWindow"], 200000)
        self.assertTrue(data["enabledPlugins"]["ultimatum@ultimatum"])
        cp = subprocess.run([PY, ULT, "context", "--cap", "10"], capture_output=True, text=True,
                            env=self.env, timeout=30)
        self.assertEqual(cp.returncode, 2)


if __name__ == "__main__":
    unittest.main()
