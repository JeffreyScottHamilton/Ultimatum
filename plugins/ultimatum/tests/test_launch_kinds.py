"""The per-kind launch heads (website, ecommerce, app, event): detection, routing, layout and sizes."""
import json
import re
import sys
import unittest

from _harness import REPO, SCRIPTS, LaunchCase, pick_hooks

sys.path.insert(0, SCRIPTS)
from ultlib.pick import pick  # noqa: E402
from ultlib.teams import KIND_ORDER, kind_plugin, launch_kind  # noqa: E402

# Only kinds whose plugin has landed; the event head arrives from a separate branch.
KINDS = {k: REPO / "plugins" / f"ultimatum-{k}-launch" for k in KIND_ORDER
         if (REPO / "plugins" / f"ultimatum-{k}-launch" / ".claude-plugin" / "plugin.json").is_file()}


class KindDetection(unittest.TestCase):
    CASES = {
        "launch my online candle shop": "ecommerce",
        "launch my business selling candles online": "ecommerce",
        "we sell handmade products": "ecommerce",
        "launch our SaaS invoicing app": "app",
        "we are launching our new mobile app next month": "app",
        "launch my product on product hunt": "app",
        "I want to launch my plumbing business": "website",
        "open my new bakery": "website",
        "help me fill my workshop": "event",
        "promote our opening night": "event",
        "sell tickets for our fundraiser gala": "event",
        "help me launch my business": "",
    }

    def test_kinds(self):
        for text, kind in self.CASES.items():
            with self.subTest(text=text):
                self.assertEqual(launch_kind(text), kind)

    def test_plugin_names(self):
        self.assertEqual(kind_plugin("app"), "ultimatum-app-launch")
        self.assertEqual(kind_plugin("event"), "ultimatum-event-launch")
        self.assertEqual(set(KIND_ORDER), {"website", "ecommerce", "app", "event"})


class KindRouting(unittest.TestCase):
    LAUNCH = ["launch my online candle shop", "launch our SaaS invoicing app",
              "I want to launch my plumbing business", "open my new bakery",
              "we are launching our new mobile app next month", "help me launch my business"]
    NOT_LAUNCH = ["start the app server", "launch the app in debug mode",
                  "launch my app in the simulator", "launch the product page fix"]

    def test_launch_requests_route_to_launch(self):
        for text in self.LAUNCH:
            with self.subTest(text=text):
                self.assertEqual(pick(text), "launch")

    def test_dev_phrases_stay_out(self):
        for text in self.NOT_LAUNCH:
            with self.subTest(text=text):
                self.assertNotEqual(pick(text), "launch")


class KindHookAndBoard(LaunchCase):
    def test_launch_prompts_point_to_a_launch_plugin(self):
        for text in ("launch my online candle shop", "help me launch my business", "help me fill my workshop"):
            with self.subTest(text=text):
                out = pick_hooks(text, self.root)
                self.assertIn("-launch", out)
                self.assertNotIn("ultimatum:work", out)

    def test_board_prints_the_kind_and_its_head(self):
        for kind in KIND_ORDER:
            with self.subTest(kind=kind):
                r = self.ult("launch", "--root", str(self.root), "--kind", kind)
                self.assertEqual(r.code, 0, r.all)
                self.assertIn(f"kind: {kind}", r.out)
                self.assertIn(f"ultimatum-{kind}-launch:launch", r.out)
        r = self.ult("launch", "--root", str(self.root))
        self.assertIn("kind: unknown", r.out)


def _body_and_description(path):
    text = path.read_text(encoding="utf-8")
    front, body = text.split("\n---\n", 1)
    desc = re.search(r'^description:\s*"(.*)"\s*$', front, re.M).group(1)
    return front, body, desc


class KindPluginLayout(unittest.TestCase):
    def test_each_kind_is_a_listed_self_contained_plugin(self):
        market = {p["name"]: p["source"] for p in
                  json.loads((REPO / ".claude-plugin/marketplace.json").read_text())["plugins"]}
        for kind, root in KINDS.items():
            with self.subTest(kind=kind):
                meta = json.loads((root / ".claude-plugin/plugin.json").read_text())
                self.assertEqual(meta["name"], kind_plugin(kind))
                self.assertNotIn("dependencies", meta)
                self.assertEqual(meta["license"], "MIT")
                self.assertTrue((root / "LICENSE").is_file())
                self.assertTrue((root / "README.md").is_file())
                self.assertEqual(market.get(meta["name"]), f"./plugins/{meta['name']}")

    def test_kind_manager_runs_its_own_teams_and_stays_small(self):
        for kind, root in KINDS.items():
            with self.subTest(kind=kind):
                skills = sorted(p.parent.name for p in (root / "skills").glob("*/SKILL.md"))
                self.assertEqual(skills, ["launch"])
                front, body, desc = _body_and_description(root / "skills/launch/SKILL.md")
                self.assertIn("name: launch", front)
                self.assertLessEqual(len(body.encode()), 4096)
                self.assertLessEqual(len(desc), 600)
                self.assertIn(f"ult launch --kind {kind}", body)
                self.assertNotIn("ultimatum-launch:", body)
                for team in ("business", "website", "social-media"):
                    self.assertIn(f"references/{team}/guide.md", body)
                    self.assertTrue((root / f"skills/launch/references/{team}/guide.md").is_file())
                for agent in ("compliance-reviewer", "taste-critic"):
                    self.assertIn(f"{kind_plugin(kind)}:{agent}", body)
                    self.assertTrue((root / f"agents/{agent}.md").is_file())
                self.assertIn("ult gate approve publish", body)
                for ref in (root / "skills/launch/references").rglob("*.md"):
                    self.assertLessEqual(ref.stat().st_size, 16384, ref)
                refs = root / "skills/launch/references"
                for name in ("route.md", "launch-checklist.md"):  # flat, or in the kind's own folder
                    self.assertTrue((refs / name).is_file() or (refs / kind / name).is_file(), name)

    def test_shopify_theme_rows_live_with_ecommerce(self):
        from _harness import TEAMS
        self.assertNotIn("Shopify", (TEAMS / "shared/licenses.md").read_text())
        self.assertIn("Shopify Horizon",
                      (KINDS["ecommerce"] / "skills/launch/references/checkout-and-ops.md").read_text())


if __name__ == "__main__":
    unittest.main()
