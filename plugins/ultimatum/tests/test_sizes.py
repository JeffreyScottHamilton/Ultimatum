"""Static budgets for what Ultimatum puts into every chat (2.0)."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

P = Path(__file__).resolve().parents[1]
SKILLS = P / "skills"
LAUNCH = P.parent / "ultimatum-launch"
LSKILLS = LAUNCH / "skills"
WORKFLOWS = {"work"}  # core's model-invocable workflow; the launch workflows live in ultimatum-launch
LAUNCH_WORKFLOWS = {"launch", "business", "website", "social-media", "motion-graphics"}
LOOKUPS = {"status", "doctor"}  # small read-only checks Claude may run when asked about the install


def _front(text: str) -> str:
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    return m.group(1) if m else ""


class SizeBudgets(unittest.TestCase):
    def test_work_skill_body_is_small(self):
        text = (SKILLS / "work" / "SKILL.md").read_text(encoding="utf-8")
        body = text.split("\n---\n", 1)[1]
        self.assertLessEqual(len(body.encode()), 4096, "L0 body must stay <= 4 KB (~1k tokens)")
        self.assertLessEqual(len(text.encode()), 20 * 1024)

    def test_launch_skill_bodies_are_small(self):
        self.assertEqual({d.name for d in LSKILLS.iterdir() if (d / "SKILL.md").exists()}, LAUNCH_WORKFLOWS)
        for name in sorted(LAUNCH_WORKFLOWS):
            text = (LSKILLS / name / "SKILL.md").read_text(encoding="utf-8")
            with self.subTest(skill=name):
                self.assertLessEqual(len(text.split("\n---\n", 1)[1].encode()), 4096)

    def test_workflow_descriptions_within_listing_cap(self):
        paths = [SKILLS / n / "SKILL.md" for n in sorted(WORKFLOWS | LOOKUPS)]
        paths += [LSKILLS / n / "SKILL.md" for n in sorted(LAUNCH_WORKFLOWS)]
        for path in paths:
            name = path.parent.name
            front = _front(path.read_text(encoding="utf-8"))
            m = re.search(r'^description:\s*"?(.*?)"?$', front, re.M)
            with self.subTest(skill=name):
                self.assertIsNotNone(m)
                self.assertLessEqual(len(m.group(1)), 600)

    def test_management_skills_cost_nothing_at_startup(self):
        for d in sorted(SKILLS.iterdir()):
            if d.name in WORKFLOWS | LOOKUPS or not (d / "SKILL.md").exists():
                continue
            text = (d / "SKILL.md").read_text(encoding="utf-8")
            with self.subTest(skill=d.name):
                self.assertIn("disable-model-invocation: true", _front(text))
                self.assertLessEqual(len(text.encode()), 1536)

    def test_status_and_doctor_are_small_and_never_change_anything(self):
        for name in sorted(LOOKUPS):
            text = (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")
            with self.subTest(skill=name):
                self.assertNotIn("disable-model-invocation", _front(text))
                self.assertLessEqual(len(text.encode()), 1536)
        self.assertIn("disable-model-invocation: true", _front((SKILLS / "setup" / "SKILL.md").read_text()))

    def test_agent_descriptions_are_short(self):
        for f in sorted([*(P / "agents").glob("*.md"), *(LAUNCH / "agents").glob("*.md")]):
            front = _front(f.read_text(encoding="utf-8"))
            m = re.search(r"^description:\s*(.*)$", front, re.M)
            with self.subTest(agent=f.name):
                self.assertIsNotNone(m)
                self.assertLessEqual(len(m.group(1)), 400)

    def test_every_reference_is_bounded(self):
        for f in [*(SKILLS / "work" / "references").rglob("*.md"), *(SKILLS / "coding" / "guides").glob("*.md"),
                  *LSKILLS.rglob("*.md")]:
            if f.name == "SKILL.md":
                continue
            with self.subTest(ref=str(f.relative_to(P.parent))):
                self.assertLessEqual(f.stat().st_size, 16 * 1024)


if __name__ == "__main__":
    unittest.main()
