"""Component-library lookup and upstream registry: data schema, licence rules,
search behaviour, CLI output, and a no-network check on the two modules."""
import ast
import json
import re
import sys
import unittest
from datetime import date
from pathlib import Path

from _harness import SCRIPTS, UltCase

sys.path.insert(0, SCRIPTS)
from ultlib import components as comp  # noqa: E402
from ultlib import upstreams as ups  # noqa: E402

DATA_DIR = Path(SCRIPTS).parent / "data"
MOD_FILES = [Path(SCRIPTS) / "ultlib" / "components.py", Path(SCRIPTS) / "ultlib" / "upstreams.py"]

REGISTRY_IDS = {
    "shadcn-ui", "base-ui", "radix-ui", "sonner", "vaul", "cmdk", "number-flow", "magic-ui",
    "aceternity-ui", "21st-dev", "react-bits", "react-aria", "motion", "framer-motion", "gsap", "rareui",
}
RESTRICTED_IDS = {"react-bits", "rareui", "gsap"}
UPSTREAM_PINS = {
    "emil": "64eb3de", "impeccable": "b49177d", "ui-ux-pro-max": "a4fc248", "anthropic-skills": "e4bb5d9",
    "superpowers": "22f0b46", "vercel-agent-skills": "5a37a63", "taste": "6c0b5c7", "remotion": "89c8afa",
    "jaimejunr-frontend-skills": "7177def",
}
SPDX_PERMISSIVE = {"MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC"}
COMPONENT_KEYS = {"id", "name", "package", "stacks", "categories", "keywords", "licence", "restricted",
                  "maintained", "last_release", "install", "fit", "alternatives_to", "source", "verified", "note"}
UPSTREAM_KEYS = {"id", "kind", "repo", "pin", "licence", "decision", "modules", "reviewed", "note"}
STACK_NAMES = {"react", "vue", "svelte", "any"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _load(name):
    return json.loads((DATA_DIR / name).read_text(encoding="utf-8"))


def _is_date(text):
    if not isinstance(text, str) or not DATE_RE.match(text):
        return False
    try:
        date.fromisoformat(text)
        return True
    except ValueError:
        return False


class TestComponentData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = _load("components.json")
        cls.entries = cls.doc["components"]
        cls.upstreams = _load("upstreams.json")["upstreams"]
        cls.by_id = {e["id"]: e for e in cls.entries}

    def test_top_level_and_unique_ids(self):
        self.assertEqual(self.doc["version"], 1)
        ids = [e["id"] for e in self.entries]
        self.assertEqual(len(ids), len(set(ids)), "component ids must be unique")
        self.assertTrue(REGISTRY_IDS <= set(ids), "all 16 registry entries must be present")

    def test_every_entry_has_the_schema(self):
        for e in self.entries:
            with self.subTest(id=e["id"]):
                self.assertEqual(set(e), COMPONENT_KEYS)
                self.assertIsInstance(e["name"], str)
                self.assertTrue(e["name"])
                self.assertTrue(e["stacks"] and set(e["stacks"]) <= STACK_NAMES)
                self.assertIsInstance(e["categories"], list)
                self.assertTrue(e["keywords"] and all(isinstance(k, str) for k in e["keywords"]))
                self.assertIsInstance(e["restricted"], bool)
                self.assertIsInstance(e["maintained"], bool)
                self.assertTrue(e["last_release"] is None or _is_date(e["last_release"]))
                self.assertTrue(e["install"].strip())
                self.assertTrue(0 < len(e["fit"]) <= 100)
                self.assertTrue(e["source"] is None or e["source"].startswith("https://"))
                self.assertEqual(e["verified"], "2026-11-24")

    def test_licence_is_spdx_or_marked_restricted(self):
        for e in self.entries:
            with self.subTest(id=e["id"]):
                lic = e["licence"]
                ok = lic in SPDX_PERMISSIVE or lic == "none" or lic.startswith("restricted:")
                self.assertTrue(ok, f"unexpected licence field: {lic!r}")
                self.assertEqual(e["restricted"], lic == "none" or lic.startswith("restricted:"))

    def test_every_restricted_entry_is_flagged(self):
        restricted = {e["id"] for e in self.entries if e["restricted"]}
        self.assertEqual(restricted, RESTRICTED_IDS)
        for rid in RESTRICTED_IDS:
            self.assertTrue(self.by_id[rid]["licence"].startswith("restricted:"))

    def test_alternatives_reference_known_ids_and_are_permissive(self):
        known = {e["id"] for e in self.entries} | {u["id"] for u in self.upstreams}
        for e in self.entries:
            for alt in e["alternatives_to"]:
                self.assertIn(alt, known, f"{e['id']} lists unknown alternative target {alt}")
        for target in ("react-bits", "rareui", "gsap", "vaul"):
            alts = [e for e in self.entries if target in e["alternatives_to"]]
            self.assertTrue(alts, f"no verified alternative for {target}")
            for a in alts:
                with self.subTest(alt=a["id"], target=target):
                    self.assertFalse(a["restricted"])
                    self.assertTrue(a["maintained"])
                    self.assertIn(a["licence"], SPDX_PERMISSIVE)
        self.assertTrue([e for e in self.entries if "remotion" in e["alternatives_to"]],
                        "no verified alternative for remotion")

    def test_vaul_is_flagged_unmaintained_not_restricted(self):
        vaul = self.by_id["vaul"]
        self.assertFalse(vaul["maintained"])
        self.assertFalse(vaul["restricted"])


class TestUpstreamData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.upstreams = _load("upstreams.json")["upstreams"]

    def test_unique_ids_and_schema(self):
        ids = [u["id"] for u in self.upstreams]
        self.assertEqual(len(ids), len(set(ids)))
        for u in self.upstreams:
            with self.subTest(id=u["id"]):
                self.assertEqual(set(u), UPSTREAM_KEYS)
                self.assertIn(u["decision"], {"adapt", "adapter", "skip"})
                self.assertIn(u["kind"], {"skill-source", "component-library"})
                self.assertRegex(u["pin"], r"^[0-9a-f]{7}$")
                self.assertTrue(u["repo"].startswith("https://github.com/"))
                self.assertIsInstance(u["modules"], list)
                self.assertTrue(_is_date(u["reviewed"]))

    def test_nine_researched_sources_with_pins(self):
        sources = {u["id"]: u for u in self.upstreams if u["kind"] == "skill-source"}
        self.assertEqual(set(sources), set(UPSTREAM_PINS))
        for uid, pin in UPSTREAM_PINS.items():
            self.assertEqual(sources[uid]["pin"], pin)

    def test_remotion_is_skipped_without_licence(self):
        remotion = next(u for u in self.upstreams if u["id"] == "remotion")
        self.assertEqual(remotion["decision"], "skip")
        self.assertEqual(remotion["licence"], "none")
        self.assertEqual(remotion["modules"], [])


class TestComponentSearch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.entries = _load("components.json")["components"]

    def test_default_results_never_restricted(self):
        queries = ["animated text background effects", "timeline scroll animation", "gradient button effects",
                   "bottom drawer sheet", "animated number counter", "command palette search"]
        for q in queries:
            with self.subTest(query=q):
                results = comp.search(q, entries=self.entries)
                self.assertTrue(results)
                self.assertFalse([r for r in results if r["restricted"]])

    def test_all_flag_includes_restricted_entries(self):
        results = comp.search("animated text background effects", include_all=True, entries=self.entries)
        flagged = {r["id"]: r["restricted"] for r in results}
        self.assertTrue(flagged.get("react-bits"))
        self.assertTrue(all(isinstance(r["restricted"], bool) for r in results))

    def test_at_most_three_results(self):
        results = comp.search("animated components effects text motion", include_all=True, entries=self.entries)
        self.assertLessEqual(len(results), 3)

    def test_stack_filter(self):
        for stack in ("vue", "svelte"):
            with self.subTest(stack=stack):
                results = comp.search("animation timeline", stack=stack, include_all=True, entries=self.entries)
                for r in results:
                    self.assertTrue(stack in r["stacks"] or "any" in r["stacks"])
        react_only = comp.search("animation gestures", stack="vue", include_all=True, entries=self.entries)
        self.assertNotIn("motion", [r["id"] for r in react_only])

    def test_empty_or_unknown_need(self):
        self.assertEqual(comp.search("   ", entries=self.entries), [])
        self.assertEqual(comp.search("zzqxv blorp", entries=self.entries), [])

    def test_token_normalisation(self):
        self.assertIn("button", comp.tokens("Buttons"))
        self.assertEqual(comp.tokens("animated-backgrounds"), {"animated", "background"})
        self.assertNotIn("the", comp.tokens("the number"))

    def test_best_match_first(self):
        results = comp.search("animated number counter", entries=self.entries)
        self.assertEqual(results[0]["id"], "number-flow")


class TestComponentCLI(UltCase):
    def test_text_output_is_short_and_plain(self):
        r = self.ult("components", "animated number counter")
        self.assertEqual(r.code, 0, r.all)
        self.assertIn("NumberFlow", r.out)
        self.assertLessEqual(len(r.out.splitlines()), 12)
        self.assertNotIn("\x1b", r.out)

    def test_default_hides_restricted_and_all_flags_them(self):
        default = self.ult("components", "animated text background effects")
        self.assertEqual(default.code, 0, default.all)
        self.assertNotIn("RESTRICTED", default.out)
        self.assertNotIn("React Bits", default.out)
        shown = self.ult("components", "animated text background effects", "--all")
        self.assertIn("React Bits", shown.out)
        self.assertIn("RESTRICTED", shown.out)

    def test_json_output(self):
        r = self.ult("components", "bottom drawer sheet", "--json")
        self.assertEqual(r.code, 0, r.all)
        items = json.loads(r.out)
        self.assertIsInstance(items, list)
        self.assertLessEqual(len(items), 3)
        for it in items:
            for key in ("id", "name", "licence", "restricted", "maintained", "install", "fit", "score"):
                self.assertIn(key, it)
            self.assertFalse(it["restricted"])

    def test_json_all_includes_flagged_restricted(self):
        r = self.ult("components", "animated text background effects", "--all", "--json")
        items = json.loads(r.out)
        flagged = [i for i in items if i["restricted"]]
        self.assertTrue(flagged)
        self.assertTrue(all(i["licence"].startswith("restricted:") for i in flagged))

    def test_stack_flag_in_cli(self):
        r = self.ult("components", "animation timeline", "--stack", "vue", "--all", "--json")
        self.assertEqual(r.code, 0, r.all)
        for it in json.loads(r.out):
            self.assertTrue("vue" in it["stacks"] or "any" in it["stacks"])

    def test_missing_need_is_a_usage_error(self):
        r = self.ult("components")
        self.assertEqual(r.code, 2)
        self.assertIn("usage", r.all)

    def test_no_match_message(self):
        r = self.ult("components", "zzqxv blorp")
        self.assertEqual(r.code, 0)
        self.assertIn("no match", r.out)


class TestUpstreamCLI(UltCase):
    def test_listing_shows_every_upstream(self):
        r = self.ult("upstreams")
        self.assertEqual(r.code, 0, r.all)
        for uid, pin in UPSTREAM_PINS.items():
            self.assertIn(uid, r.out)
            self.assertIn(pin, r.out)
        self.assertIn("skip", r.out)

    def test_json_listing(self):
        r = self.ult("upstreams", "--json")
        self.assertEqual(r.code, 0, r.all)
        items = json.loads(r.out)
        sources = {i["id"]: i["pin"] for i in items if i["kind"] == "skill-source"}
        self.assertEqual(sources, UPSTREAM_PINS)
        self.assertTrue(all(set(i) == UPSTREAM_KEYS for i in items))


class TestNoNetwork(unittest.TestCase):
    FORBIDDEN = {"socket", "ssl", "http", "urllib", "urllib3", "requests", "httpx", "aiohttp",
                 "ftplib", "smtplib", "poplib", "imaplib", "telnetlib", "xmlrpc", "websocket"}

    def test_modules_import_no_network_libraries(self):
        for path in MOD_FILES:
            with self.subTest(module=path.name):
                tree = ast.parse(path.read_text(encoding="utf-8"))
                names = set()
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        names |= {a.name.split(".")[0] for a in node.names}
                    elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
                        names.add(node.module.split(".")[0])
                self.assertFalse(names & self.FORBIDDEN, f"network import in {path.name}: {names & self.FORBIDDEN}")
                self.assertIn("from __future__ import annotations", path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
