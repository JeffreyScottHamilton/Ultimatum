"""Covers ultlib.designskill through `ult website`."""
import json

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

