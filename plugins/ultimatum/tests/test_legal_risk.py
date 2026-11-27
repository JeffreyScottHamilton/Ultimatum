import unittest
from pathlib import Path

REF = Path(__file__).resolve().parents[1] / "skills/website/references"


class TestLegalRisk(unittest.TestCase):
    def setUp(self):
        self.text = (REF / "app/legal-risk.md").read_text()

    def test_ten_numbered_steps_and_report(self):
        for n in range(1, 11):
            self.assertIn(f"\n## {n}. ", self.text)
        self.assertIn("\n## Report", self.text)

    def test_says_it_is_not_legal_advice(self):
        self.assertIn("not legal advice", self.text)

    def test_linked_from_go_live(self):
        self.assertIn("legal-risk.md", (REF / "app/checklist.md").read_text())
        self.assertIn("legal-risk.md", (REF / "launch-checklist.md").read_text())
        self.assertIn("references/app/legal-risk.md", (REF.parent / "SKILL.md").read_text())

    def test_referenced_files_exist(self):
        for rel in ("app/supabase.md", "app/stripe.md", "shared/licenses.md"):
            self.assertTrue((REF / rel).exists(), rel)


if __name__ == "__main__":
    unittest.main()
