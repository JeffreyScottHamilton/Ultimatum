"""The helper team: solo by default, one Sonnet coder, no stale 'every edit is delegated' rule."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

P = Path(__file__).resolve().parents[1]


def model(agent):
    text = (P / "agents" / f"{agent}.md").read_text(encoding="utf-8")
    return re.search(r"^model:\s*(\S+)", text, re.M).group(1)


class Subagents(unittest.TestCase):
    def test_worker_is_the_sonnet_coder(self):
        self.assertEqual(model("worker"), "sonnet")
        self.assertEqual(model("scout"), "haiku")

    def test_router_says_solo_and_one_coder(self):
        text = (P / "skills" / "work" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Solo is the default", text)
        self.assertIn("never several coders at once", text)

    def test_no_stale_delegate_everything_rule(self):
        for f in (P / "skills").rglob("*.md"):
            text = f.read_text(encoding="utf-8")
            with self.subTest(f=f.name):
                self.assertNotIn("rule 7", text)
                self.assertNotIn("never edits project files", text)

    def test_orchestration_starts_from_solo(self):
        text = (P / "skills" / "work" / "references" / "orchestration.md").read_text(encoding="utf-8")
        self.assertIn("Start from solo", text)
        self.assertIn("One coder at a time", text)


if __name__ == "__main__":
    unittest.main()
