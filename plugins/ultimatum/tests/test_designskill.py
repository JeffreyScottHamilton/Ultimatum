"""Covers ultlib.designskill through `ult website` and `ult motion`."""
import json
import os

from _harness import UltCase


class TestDesignSkill(UltCase):
    def skills(self, *names, base="skills"):
        for n in names:
            self.write(f"{base}/{n}/SKILL.md", "---\nname: x\n---\n")
        return str(self.root / base)

    def env(self):
        e = super().env()
        e["ULTIMATUM_SKILL_DIRS"] = getattr(self, "dirs", "")
        return e

    def test_new_site_points_to_an_installed_frontend_design_skill(self):
        self.dirs = self.skills("frontend-design", "pdf")
        r = self.ult("website", "Build a new website for my bakery", "--root", str(self.root))
        self.assertEqual(r.code, 0, r.all)
        self.assertIn("design-skill: frontend-design (", r.out)
        self.assertIn("approval still apply", r.out)
        self.assertNotIn("pdf", r.out.split("design-skill:")[1].split("\n")[0])

    def test_none_installed_says_so_and_small_fixes_skip_the_line(self):
        r = self.ult("website", "Build a new website for my bakery", "--root", str(self.root), "--json")
        self.assertIn("none installed", json.loads(r.out)["design_skill"])
        self.dirs = self.skills("frontend-design")
        r = self.ult("website", "Fix the broken footer link", "--root", str(self.root))
        self.assertNotIn("design-skill", r.out)

    def test_motion_finds_motion_skills_and_skips_ultimatums_own(self):
        own = self.skills("motion-graphics", base="cache/ultimatum/ultimatum-video/0.0.1/skills")
        other = self.skills("remotion-best-practices", base="other")
        self.dirs = os.pathsep.join([own, other])
        r = self.ult("motion", "Make a 15 second logo reveal video", "--root", str(self.root))
        self.assertEqual(r.code, 0, r.all)
        self.assertIn("design-skill: remotion-best-practices (", r.out)
        self.assertNotIn("motion-graphics (", r.out)
        self.assertIn("storyboard and the animation", r.out)
