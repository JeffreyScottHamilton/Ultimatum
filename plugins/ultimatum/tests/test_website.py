"""Tests for the 2.0 workflows: website routing, the optional Designer, solo small jobs,
selective loading, Release gating and the opt-in chat style."""
from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

from _harness import SCRIPTS, UltCase

sys.path.insert(0, SCRIPTS)
from ultlib import route as R  # noqa: E402
from ultlib.website import plan  # noqa: E402

P = Path(SCRIPTS).parent
SKILLS = P / "skills"


def _front(text: str) -> str:
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    return m.group(1) if m else ""


class WebsiteRouting(unittest.TestCase):
    def test_clear_website_requests_are_flagged(self):
        for task in ("Build a landing page for our coffee shop",
                     "Redesign the homepage hero and pricing section",
                     "Make a portfolio site for a photographer"):
            with self.subTest(task=task):
                self.assertEqual(R.decide(task)["workflow"], "website")

    def test_other_work_stays_default(self):
        for task in ("Fix the CORS bug on the website API",          # bug, not website work
                     "Review the website login PR for security issues",
                     "Fix the null check in parse_date in utils.py",
                     "Add a dark mode toggle to the settings modal"):
            with self.subTest(task=task):
                self.assertEqual(R.decide(task)["workflow"], "default")

    def test_flag_is_printed_on_the_first_line(self):
        d = R.decide("Build a landing page for our coffee shop")
        self.assertIn("workflow: website", R.format_text(d).splitlines()[0])

    def test_work_skill_keeps_explicit_command_and_offers_switch(self):
        body = (SKILLS / "work" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("`workflow: website` and the user did not type `/ultimatum:work`", body)
        web = (SKILLS / "website" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("typed `/ultimatum:website`", web)


class WebsitePlan(UltCase):
    def test_designer_runs_when_a_new_look_is_asked(self):
        self.write("src/styles.css", "body{}")
        p = plan("Redesign the landing page with a fresh look", root=self.root)
        self.assertTrue(p["designer"])
        self.assertIn("skills/design/SKILL.md", p["load"])
        self.assertEqual(p["roles"][:2], ["manager", "designer"])

    def test_designer_runs_when_project_has_no_styles(self):
        p = plan("Build a landing page for a bakery with a menu and contact form", root=self.root)
        self.assertTrue(p["designer"])
        self.assertEqual(p["designer_why"], "no existing styles found")

    def test_designer_skipped_when_look_is_set(self):
        self.write("tailwind.config.js", "module.exports={}")
        p = plan("Add a testimonials section to the landing page", root=self.root)
        self.assertFalse(p["designer"])
        self.assertNotIn("skills/design/SKILL.md", p["load"])
        self.assertNotIn("designer", p["roles"])
        p = plan("Add an FAQ section to the landing page and keep the current look", root=self.root)
        self.assertFalse(p["designer"])

    def test_small_jobs_stay_solo_and_load_least(self):
        p = plan("Fix the typo in the homepage hero heading", root=self.root)
        self.assertEqual((p["size"], p["team"]), ("small", "solo"))
        self.assertFalse(p["designer"])
        self.assertEqual(p["load"], ["shared/defaults.md", "skills/coding/SKILL.md",
                                     "skills/coding/guides/website.md"])

    def test_picking_website_alone_never_starts_a_team(self):
        self.write("app.css", "")
        for task in ("Build a landing page for our coffee shop",
                     "deep: build a landing page for our coffee shop"):
            with self.subTest(task=task):
                self.assertEqual(plan(task, root=self.root)["team"], "solo")

    def test_big_sites_allow_helpers_and_load_the_code_map(self):
        self.write("app.css", "")
        p = plan("Build a full site with home, about, pricing, blog and contact pages", root=self.root)
        self.assertEqual((p["size"], p["team"]), ("large", "helpers"))
        self.assertIn("skills/work/references/code-map.md", p["load"])

    def test_release_loads_only_when_asked(self):
        self.write("app.css", "")
        self.assertNotIn("skills/release/SKILL.md", plan("Build a landing page", root=self.root)["load"])
        p = plan("Build a landing page and deploy it", root=self.root)
        self.assertIn("skills/release/SKILL.md", p["load"])
        self.assertIn("explicit yes", p["release"])

    def test_cat_prints_only_the_planned_files_with_root_filled_in(self):
        self.write("app.css", "")
        r = self.ult("website", "--cat", "--root", str(self.root), "Add a pricing section to the landing page")
        self.assertEqual(r.code, 0, r.all)
        heads = re.findall(r"^===== (.+) =====$", r.out, re.M)
        self.assertEqual(heads, ["shared/defaults.md", "skills/coding/SKILL.md",
                                 "skills/coding/guides/website.md", "skills/review/SKILL.md"])
        self.assertNotIn("${CLAUDE_PLUGIN_ROOT}", r.out)

    def test_json_output(self):
        r = self.ult("website", "--json", "--root", str(self.root), "Build a landing page")
        d = json.loads(r.out)
        self.assertEqual(d["workflow"], "website")
        self.assertIn(d["team"], {"solo", "helpers"})


class SharedSkills(unittest.TestCase):
    def test_shared_skills_are_user_invocable_only_and_small(self):
        for name in ("design", "coding", "review", "release", "style"):
            text = (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")
            with self.subTest(skill=name):
                self.assertIn("disable-model-invocation: true", _front(text))
                self.assertLessEqual(len(text.encode()), 1536)

    def test_website_skill_does_not_load_work(self):
        body = (SKILLS / "website" / "SKILL.md").read_text(encoding="utf-8")
        self.assertNotIn("work/SKILL.md", body)
        self.assertIn("ult website", body)

    def test_release_stays_gated(self):
        rel = (SKILLS / "release" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("explicit yes", rel)
        self.assertIn("never counts as approval", rel)
        for name in ("work", "website"):
            body = (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")
            with self.subTest(skill=name):
                self.assertIn("explicit yes", body)
        self.assertEqual(R.decide("Build a landing page for our coffee shop")["route"], "ui")

    def test_shared_defaults_written_once(self):
        phrase = "Pick the simplest approach that fully solves the job"
        hits = [f for f in P.rglob("*.md") if phrase in f.read_text(encoding="utf-8")]
        self.assertEqual([f.relative_to(P).as_posix() for f in hits], ["shared/defaults.md"])


class ChatStyle(UltCase):
    def test_apply_keeps_existing_text_and_remove_restores_it(self):
        f = self.write("CLAUDE.md", "## Mine\nKeep this exactly.\n")
        original = f.read_text()
        self.assertEqual(self.ult("style", "status", "--file", str(f)).code, 0)
        r = self.ult("style", "apply", "--file", str(f))
        self.assertIn("applied", r.out)
        text = f.read_text()
        self.assertTrue(text.startswith(original))
        self.assertIn("Answer first, in plain words", text)
        self.assertIn("unchanged", self.ult("style", "apply", "--file", str(f)).out)
        self.assertEqual(f.read_text(), text)
        self.assertEqual((self.root / "CLAUDE.md.ultimatum-backup").read_text(), original)
        self.ult("style", "remove", "--file", str(f))
        self.assertEqual(f.read_text(), original)

    def test_status_never_writes(self):
        f = self.root / "none" / "CLAUDE.md"
        r = self.ult("style", "status", "--file", str(f))
        self.assertIn("not set", r.out)
        self.assertFalse(f.exists())


if __name__ == "__main__":
    unittest.main()
