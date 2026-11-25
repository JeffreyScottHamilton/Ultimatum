"""The per-kind launch plugins (website, ecommerce, app): detection, routing, layout and sizes."""
import json
import re
import sys
import unittest

from _harness import LAUNCH, REPO, SCRIPTS, LaunchCase, pick_hooks

sys.path.insert(0, SCRIPTS)
from ultlib.pick import pick  # noqa: E402
from ultlib.teams import KIND_ORDER, kind_plugin, launch_kind  # noqa: E402

KINDS = {k: REPO / "plugins" / f"ultimatum-{k}-launch" for k in KIND_ORDER}


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
        "help me launch my business": "",
    }

    def test_kinds(self):
        for text, kind in self.CASES.items():
            with self.subTest(text=text):
                self.assertEqual(launch_kind(text), kind)

    def test_plugin_names(self):
        self.assertEqual(kind_plugin("app"), "ultimatum-app-launch")


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
    def test_hook_names_the_kind_plugin(self):
        out = pick_hooks("launch my online candle shop", self.root, scopes=("launch",))
        self.assertIn("ultimatum-launch:launch", out)
        self.assertIn("ultimatum-ecommerce-launch:launch", out)

    def test_hook_without_a_kind_names_no_kind_plugin(self):
        out = pick_hooks("help me launch my business", self.root, scopes=("launch",))
        self.assertIn("ultimatum-launch:launch", out)
        self.assertNotRegex(out, r"ultimatum-(website|ecommerce|app)-launch")

    def test_board_prints_the_kind(self):
        r = self.ult("launch", "--root", str(self.root), "--kind", "app")
        self.assertEqual(r.code, 0, r.all)
        self.assertIn("kind: app", r.out)
        self.assertIn("ultimatum-app-launch:launch", r.out)
        r = self.ult("launch", "--root", str(self.root))
        self.assertIn("kind: unknown", r.out)


def _body_and_description(path):
    text = path.read_text(encoding="utf-8")
    front, body = text.split("\n---\n", 1)
    desc = re.search(r'^description:\s*"(.*)"\s*$', front, re.M).group(1)
    return front, body, desc


class KindPluginLayout(unittest.TestCase):
    def test_each_kind_is_a_listed_plugin_that_depends_on_the_base(self):
        market = {p["name"]: p["source"] for p in
                  json.loads((REPO / ".claude-plugin/marketplace.json").read_text())["plugins"]}
        for kind, root in KINDS.items():
            with self.subTest(kind=kind):
                meta = json.loads((root / ".claude-plugin/plugin.json").read_text())
                self.assertEqual(meta["name"], kind_plugin(kind))
                self.assertEqual(set(meta["dependencies"]), {"ultimatum", "ultimatum-launch"})
                self.assertEqual(meta["license"], "MIT")
                self.assertTrue((root / "LICENSE").is_file())
                self.assertTrue((root / "README.md").is_file())
                self.assertEqual(market.get(meta["name"]), f"./plugins/{meta['name']}")

    def test_kind_manager_runs_the_shared_teams_and_stays_small(self):
        for kind, root in KINDS.items():
            with self.subTest(kind=kind):
                skills = sorted(p.parent.name for p in (root / "skills").glob("*/SKILL.md"))
                self.assertEqual(skills, ["launch"])
                front, body, desc = _body_and_description(root / "skills/launch/SKILL.md")
                self.assertIn("name: launch", front)
                self.assertLessEqual(len(body.encode()), 4096)
                self.assertLessEqual(len(desc), 600)
                self.assertIn(f"ult launch --kind {kind}", body)
                for team in ("business", "website", "social-media"):
                    self.assertIn(f"ultimatum-launch:{team}", body)
                self.assertIn("ult gate approve publish", body)
                for ref in (root / "skills/launch/references").glob("*.md"):
                    self.assertLessEqual(ref.stat().st_size, 16384, ref)
                self.assertTrue((root / "skills/launch/references/route.md").is_file())
                self.assertTrue((root / "skills/launch/references/launch-checklist.md").is_file())

    def test_routes_moved_out_of_the_base(self):
        refs = LAUNCH / "skills/launch/references"
        self.assertEqual(sorted(refs.glob("route-*.md")), [])
        self.assertTrue((refs / "routes.md").is_file())
        base = (LAUNCH / "skills/launch/SKILL.md").read_text()
        self.assertIn("ultimatum-<kind>-launch:launch", base)
        self.assertNotIn("Shopify", (refs / "licenses.md").read_text())
        self.assertIn("Shopify Horizon",
                      (KINDS["ecommerce"] / "skills/launch/references/checkout-and-ops.md").read_text())


if __name__ == "__main__":
    unittest.main()
