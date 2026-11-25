"""ultimatum-launch ships a copy of core's toolbelt; this fails as soon as the copy drifts."""
import importlib.util
import json
import unittest

from _harness import CORE, LAUNCH, REPO

SYNC = REPO / "tools" / "sync_launch_toolbelt.py"


def _sync_module():
    spec = importlib.util.spec_from_file_location("sync_launch_toolbelt", SYNC)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class ToolbeltCopy(unittest.TestCase):
    def test_launch_copy_matches_core(self):
        bad = _sync_module().differences()
        self.assertEqual(bad, [], "run: python3 tools/sync_launch_toolbelt.py")

    def test_copied_core_docs_are_not_registered_as_launch_skills(self):
        stray = [p for p in (LAUNCH / "skills").glob("*/SKILL.md")
                 if p.parent.name in {"work", "design", "coding", "review", "release"}]
        self.assertEqual(stray, [])

    def test_launch_depends_on_core_and_both_are_listed(self):
        launch = json.loads((LAUNCH / ".claude-plugin/plugin.json").read_text())
        self.assertIn("ultimatum", json.dumps(launch.get("dependencies")))
        market = json.loads((REPO / ".claude-plugin/marketplace.json").read_text())
        sources = {p["name"]: p["source"] for p in market["plugins"]}
        self.assertEqual(sources.get("ultimatum-launch"), "./plugins/ultimatum-launch")
        self.assertIn("ultimatum", sources)
        core = json.loads((CORE / ".claude-plugin/plugin.json").read_text())
        for meta in (launch, core):
            self.assertEqual(meta["license"], "MIT")


if __name__ == "__main__":
    unittest.main()
