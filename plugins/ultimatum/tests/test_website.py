"""Tests for the 2.0 workflows: website routing, the optional Designer, solo small jobs,
selective loading, Release gating and the opt-in chat style."""
from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

from _harness import SCRIPTS, WEB_REFS, UltCase, pick_hooks

sys.path.insert(0, SCRIPTS)
from ultlib import route as R  # noqa: E402
from ultlib.website import plan  # noqa: E402

P = Path(SCRIPTS).parent
SKILLS = P / "skills"
WEB_GUIDE = WEB_REFS / "website" / "guide.md"


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
        self.assertIn("A `workflow: website` line (user did not type `/ultimatum:work`)", body)
        self.assertIn("skills/website/SKILL.md", body)


class WebsitePlan(UltCase):
    def test_designer_runs_when_a_new_look_is_asked(self):
        self.write("src/styles.css", "body{}")
        p = plan("Redesign the landing page with a fresh look", root=self.root)
        self.assertTrue(p["designer"])
        self.assertIn("skills/design/SKILL.md", p["load"])
        self.assertEqual(p["roles"][:3], ["planner (manager)", "designer", "user approves mockup"])

    def test_designer_runs_when_project_has_no_styles(self):
        p = plan("Add a pricing section and a contact form to the landing page", root=self.root)
        self.assertTrue(p["designer"])
        self.assertEqual(p["designer_why"], "no existing styles found")

    def test_new_site_always_gets_design_build_and_review(self):
        self.write("styles.css", "body{}")
        p = plan("Build me a website for my coffee shop", root=self.root)
        self.assertTrue(p["designer"])
        for f in ("skills/design/SKILL.md", "skills/coding/SKILL.md", "skills/review/SKILL.md"):
            self.assertIn(f, p["load"])

    def test_small_fix_reuses_the_design_and_checks_in_a_browser(self):
        self.write("index.html", "<nav></nav>")
        self.write("styles.css", "nav{}")
        p = plan("Fix the mobile menu", root=self.root)
        self.assertEqual((p["size"], p["team"], p["designer"]), ("small", "solo", False))
        self.assertEqual(p["roles"], ["manager", "builder", "browser check"])
        self.assertNotIn("skills/design/SKILL.md", p["load"])

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

    def test_website_guide_does_not_load_work(self):
        body = WEB_GUIDE.read_text(encoding="utf-8")
        self.assertNotIn("work/SKILL.md", body)
        self.assertIn("ult website", body)

    def test_release_stays_gated(self):
        rel = (SKILLS / "release" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("explicit yes", rel)
        self.assertIn("never counts as approval", rel)
        for path in (SKILLS / "work" / "SKILL.md", WEB_GUIDE):
            body = path.read_text(encoding="utf-8")
            with self.subTest(file=path.name):
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


class PlainChatPicker(UltCase):
    """The UserPromptSubmit hook that starts Website or Work from plain chat."""

    def pick(self, prompt, cwd=None, auto=None):
        import os
        env = None
        if auto is not None:
            env = dict(os.environ, ULTIMATUM_AUTO=auto)
        return pick_hooks(prompt, cwd or self.root, env=env)

    def site(self):
        self.write("index.html", "<nav class='menu'></nav>")
        self.write("styles.css", "nav{}")

    def kind(self, prompt):
        from ultlib.pick import pick
        return pick(prompt, root=self.root)

    def test_new_website_request_starts_the_website_skill(self):
        self.assertEqual(self.kind("Build me a website for my coffee shop"), "website")
        self.assertIn("ultimatum:website", self.pick("Build me a website for my coffee shop"))

    def test_interface_fix_in_a_website_project_picks_website(self):
        self.site()
        self.assertEqual(self.kind("Fix the mobile menu"), "website")
        self.assertNotIn("ultimatum:work", self.pick("Fix the mobile menu"))

    def test_interface_fix_outside_a_website_project_starts_work(self):
        self.write("app/main.py", "print(1)")
        self.assertEqual(self.kind("Fix the mobile menu"), "work")
        self.assertIn("ultimatum:work", self.pick("Fix the mobile menu"))

    def test_regular_coding_request_starts_work(self):
        self.site()
        out = self.pick("Fix the CSV export")
        self.assertIn('"additionalContext"', out)
        self.assertIn("ultimatum:work", out)

    def test_plain_questions_and_writing_help_get_only_the_style_line(self):
        self.site()
        for prompt in ("What is a closure in JavaScript?", "Thanks!", "write a haiku about autumn",
                       "How does the export module work?", "Make this email shorter: Hi Sam, quick follow-up"):
            with self.subTest(prompt=prompt):
                out = self.pick(prompt)
                self.assertIn("Ultimatum style", out)
                self.assertNotIn("ultimatum:work", out)

    def test_explicit_command_and_off_switch_are_respected(self):
        self.site()
        self.assertEqual(self.pick("/ultimatum:work Fix the mobile menu"), "")
        self.assertEqual(self.pick("Fix the CSV export", auto="0"), "")

    def test_bad_input_never_blocks(self):
        import os, subprocess
        from _harness import PY, SCRIPTS
        cp = subprocess.run([PY, os.path.join(SCRIPTS, "ult-pick"), "--scope", "core"], input="not json",
                            capture_output=True, text=True)
        self.assertEqual((cp.returncode, cp.stdout), (0, ""))

    def test_hook_is_registered_and_guide_runs_the_whole_job(self):
        import json
        from _harness import CORE
        hooks = json.loads((CORE / "hooks/hooks.json").read_text())["hooks"]["UserPromptSubmit"]
        self.assertIn("ult-pick", json.dumps(hooks))
        body = WEB_GUIDE.read_text()
        for needle in ("ult-browser.mjs", "**Preview.**", "no approval needed", "explicit yes",
                       "**one** clear visual direction", "**Small fix = only the reported bug.**", "seen, not changed"):
            self.assertIn(needle, body)
        head = (SKILLS / "website/SKILL.md").read_text()
        self.assertIn("references/website/guide.md", head)

    def test_plan_tells_small_fixes_to_stay_on_the_bug_and_new_sites_to_pick_one_look(self):
        self.site()
        small = self.ult("website", "Fix the mobile menu", "--root", str(self.root)).out
        self.assertIn("scope: only the reported bug", small)
        self.assertNotIn("designer: yes", small)
        new = self.ult("website", "Build me a website for my coffee shop", "--root", str(self.tmp / "empty")).out
        self.assertIn("gate: brief + design + three HTML directions, then stop", new)
        self.assertIn("reviewer", new)


class VisualApproval(UltCase):
    """New sites and redesigns stop for a mockup approval; small fixes never do."""

    def test_new_site_stops_for_mockup_approval_before_building(self):
        p = plan("Build me a website for my coffee shop", root=self.root)
        self.assertEqual(p["approval"], "waiting")
        roles = p["roles"]
        self.assertLess(roles.index("designer"), roles.index("user approves mockup"))
        self.assertLess(roles.index("user approves mockup"), roles.index("builder"))
        self.assertIn("skills/website/references/website/planner.md", p["load"])
        self.assertEqual(p["load"][:2], ["shared/defaults.md", "skills/website/references/website/planner.md"])

    def test_major_redesign_also_stops(self):
        self.write("styles.css", "body{}")
        self.assertEqual(plan("Redesign the homepage with a fresh look", root=self.root)["approval"], "waiting")

    def test_small_menu_fix_takes_the_short_path(self):
        self.write("index.html", "<nav></nav>")
        self.write("styles.css", "nav{}")
        p = plan("Fix the mobile menu", root=self.root)
        self.assertEqual(p["approval"], "not needed")
        self.assertNotIn("user approves mockup", p["roles"])
        self.assertNotIn("skills/website/references/website/planner.md", p["load"])
        out = self.ult("website", "Fix the mobile menu", "--root", str(self.root)).out
        self.assertNotIn("gate:", out)

    def test_approval_is_recorded_in_the_brief_and_opens_the_build(self):
        self.write(".ultimatum/brief.md", "# Brief\n\n## For whom\nCommuters\n\n## Phases\n1. Hero\n")
        r = self.ult("website", "--root", str(self.root), "--approve", "Warm cream and espresso palette, big call button",
                     "--image", "mockups/home.png")
        self.assertEqual(r.code, 0, r.all)
        brief = (self.root / ".ultimatum/brief.md").read_text()
        for needle in ("## For whom", "## Phases", "## Approved direction", "big call button", "mockups/home.png"):
            self.assertIn(needle, brief)
        p = plan("Build me a website for my coffee shop", root=self.root)
        self.assertEqual(p["approval"], "approved")
        self.assertNotIn("user approves mockup", p["roles"])
        out = self.ult("website", "Build me a website for my coffee shop", "--root", str(self.root)).out
        self.assertIn("gate: approved", out)
        # A second approval replaces the first instead of stacking.
        self.ult("website", "--root", str(self.root), "--approve", "Darker green version")
        brief = (self.root / ".ultimatum/brief.md").read_text()
        self.assertEqual(brief.count("## Approved direction"), 1)
        self.assertIn("Darker green version", brief)
        self.assertNotIn("big call button", brief)
        self.assertIn("## Phases", brief)

    def test_empty_approval_is_refused(self):
        r = self.ult("website", "--root", str(self.root), "--approve", "  ")
        self.assertEqual(r.code, 2)
        self.assertFalse((self.root / ".ultimatum/brief.md").exists())

    def test_guide_and_planner_spell_out_the_gate(self):
        skill = WEB_GUIDE.read_text()
        for needle in ("**Visual path**", "**Short path**", "stop and wait", "no production code until the user approves",
                       "ult website --approve", "ChatGPT", "No mockup and no approval stop", "compare with the approved direction"):
            self.assertIn(needle, skill)
        guide = (WEB_REFS / "website/planner.md").read_text()
        for needle in ("[[PLACEHOLDER:", "grayscale wireframe", "ChatGPT", "end your turn", "Approved direction",
                       "First action", "Mobile", "Phases", "exact words"):
            self.assertIn(needle, guide)


class PickAccuracy(unittest.TestCase):
    """ultlib.pick on the labelled sets: coding tasks start a workflow, plain chat never does."""

    @classmethod
    def setUpClass(cls):
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
        from ultlib.pick import pick
        cls.pick = staticmethod(pick)
        cls.data = Path(__file__).resolve().parent / "data"

    def rows(self, name):
        import json
        return [json.loads(l)["task"] for l in (self.data / name).read_text().splitlines() if l.strip()]

    def test_plain_chat_stays_in_chat(self):
        wrong = [t for t in self.rows("plain_chat.jsonl") if self.pick(t) != "chat"]
        self.assertEqual(wrong, [])

    def test_coding_tasks_start_a_workflow_except_code_questions(self):
        import json
        rows = []
        for f in sorted(self.data.glob("routing_*.jsonl")):
            rows += [json.loads(l) for l in f.read_text().splitlines() if l.strip()]
        asks = [r["task"] for r in rows if r["route"] != "discover" and not r["task"].startswith("/")]
        missed = [t for t in asks if self.pick(t) == "chat"]
        self.assertLessEqual(len(missed), 3, missed)

    def test_the_three_example_prompts(self):
        self.assertEqual(self.pick("Build me a website for my coffee shop"), "website")
        self.assertEqual(self.pick("Fix the CSV export"), "work")
        self.assertEqual(self.pick("What is a closure in JavaScript?"), "chat")

