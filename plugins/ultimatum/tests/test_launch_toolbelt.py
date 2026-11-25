"""Every head plugin ships copies of the team guides, agents and core's toolbelt; this fails as soon as a copy drifts."""
import importlib.util
import json
import unittest

from _harness import CORE, REPO

SYNC = REPO / "tools" / "sync_plugins.py"


def _sync_module():
    spec = importlib.util.spec_from_file_location("sync_plugins", SYNC)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _heads():
    return _sync_module().heads()


class PluginCopies(unittest.TestCase):
    def test_every_copy_matches_its_source(self):
        bad = _sync_module().differences()
        self.assertEqual(bad, [], "run: python3 tools/sync_plugins.py")

    def test_at_least_the_three_launch_heads_are_synced(self):
        names = {root.name for root, _, _ in _heads()}
        self.assertTrue({"ultimatum-website-launch", "ultimatum-ecommerce-launch", "ultimatum-app-launch"} <= names)

    def test_each_head_registers_only_its_head_skill(self):
        for root, head, _ in _heads():
            with self.subTest(plugin=root.name):
                skills = sorted(p.parent.name for p in (root / "skills").glob("*/SKILL.md"))
                self.assertEqual(skills, [head])
                self.assertFalse((root / "hooks").exists())

    def test_heads_stand_alone_and_are_listed(self):
        market = json.loads((REPO / ".claude-plugin/marketplace.json").read_text())
        sources = {p["name"]: p["source"] for p in market["plugins"]}
        self.assertEqual(sources.get("ultimatum"), "./plugins/ultimatum")
        self.assertNotIn("ultimatum-launch", sources)
        self.assertFalse((REPO / "plugins" / "ultimatum-launch").exists())
        core = json.loads((CORE / ".claude-plugin/plugin.json").read_text())
        self.assertEqual(core["license"], "MIT")
        for root, _, _ in _heads():
            meta = json.loads((root / ".claude-plugin/plugin.json").read_text())
            with self.subTest(plugin=root.name):
                self.assertNotIn("dependencies", meta)
                self.assertEqual(meta["license"], "MIT")
                self.assertEqual(sources.get(root.name), f"./plugins/{root.name}")


if __name__ == "__main__":
    unittest.main()
