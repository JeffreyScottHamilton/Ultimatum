"""The website workflow covers apps: guides exist, are wired in, and keep the safety rules."""
from __future__ import annotations

import re
import sys
import unittest

from _harness import SCRIPTS, WEB_REFS

sys.path.insert(0, SCRIPTS)
from ultlib import route as R  # noqa: E402

APP = WEB_REFS / "app"
SKILL = WEB_REFS.parent / "SKILL.md"


class AppGuides(unittest.TestCase):
    def test_guides_exist_and_are_linked(self):
        skill = SKILL.read_text()
        for name in ("route.md", "supabase.md", "auth.md", "stripe.md", "checklist.md"):
            self.assertTrue((APP / name).is_file(), name)
            self.assertIn(f"references/app/{name}", skill, name)

    def test_old_out_of_scope_rule_is_gone(self):
        for p in (SKILL, WEB_REFS / "route.md"):
            self.assertNotRegex(p.read_text(), r"out of scope for now")

    def test_new_gates_are_named_in_the_flow(self):
        skill = SKILL.read_text()
        self.assertIn("ult gate approve data-model", skill)
        self.assertIn("ult gate approve live-payments", skill)

    def test_safety_rules_stay(self):
        supa = (APP / "supabase.md").read_text()
        self.assertIn("enable row level security", supa)
        self.assertIn("second-user test", supa)
        stripe = (APP / "stripe.md").read_text()
        self.assertIn("constructEvent", stripe)
        self.assertIn("Never take an amount or a price id straight from the browser", stripe)
        auth = (APP / "auth.md").read_text()
        self.assertIn("getUser()", auth)
        self.assertIn("never base access on it", auth)

    def test_no_real_looking_keys(self):
        key = re.compile(r"(sk|rk|pk)_(live|test)_[A-Za-z0-9]{8,}|whsec_[A-Za-z0-9]{8,}|sb_secret_[A-Za-z0-9]{8,}")
        for p in APP.glob("*.md"):
            self.assertIsNone(key.search(p.read_text()), p.name)


class AppRouting(unittest.TestCase):
    def test_member_and_portal_sites_go_to_the_website_workflow(self):
        for task in ("Build a members site for my gym with Supabase login and Stripe subscriptions",
                     "Add a client portal to our accounting firm"):
            self.assertTrue(R.website_flag(task, "feature", None), task)

    def test_bugs_in_members_area_stay_code_work(self):
        self.assertFalse(R.website_flag("Fix the members area cache bug in the API", "bug", None))


if __name__ == "__main__":
    unittest.main()
