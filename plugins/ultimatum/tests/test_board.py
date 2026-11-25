import unittest

from _harness import UltCase


class TestBoard(UltCase):
    def test_empty_board_says_how_to_start(self):
        r = self.ult("board", "show")
        self.assertEqual(r.code, 0, r.all)
        self.assertIn("board: empty", r.out)

    def test_cards_move_and_show_resume_point(self):
        self.assertEqual(self.ult("board", "add", "Checkout page", "--check", "pay test passes",
                                  "--link", "pricing").code, 0)
        self.ult("board", "add", "Emails")
        r = self.ult("board", "show")
        self.assertIn("resume: C1 (backlog)", r.out)
        self.assertEqual(self.ult("board", "move", "C1", "doing", "started").code, 0)
        r = self.ult("board", "show")
        self.assertIn("resume: C1 (doing)", r.out)
        card = (self.root / ".ultimatum" / "board" / "C1-checkout-page.md").read_text()
        self.assertIn("status: doing", card)
        self.assertIn("check: pay test passes", card)
        self.assertIn("[[pricing]]", card)
        self.assertIn("- backlog -> doing: started", card)
        self.ult("board", "move", "C1", "done")
        self.ult("board", "move", "C2", "done")
        self.assertIn("resume: all done", self.ult("board", "show").out)

    def test_bad_ids_and_states_fail(self):
        self.ult("board", "add", "One")
        self.assertEqual(self.ult("board", "move", "C9", "done").code, 2)
        self.assertEqual(self.ult("board", "move", "C1", "finished").code, 2)
        self.assertEqual(self.ult("board", "add").code, 2)

    def test_secrets_are_redacted_on_cards(self):
        self.ult("board", "add", "Wire key sk-ant-api03-abcdefghijklmnopqrstuvwxyz0123456789")
        text = "".join(p.read_text() for p in (self.root / ".ultimatum" / "board").glob("*.md"))
        self.assertNotIn("abcdefghijklmnopqrstuvwxyz0123456789", text)


class TestNotes(UltCase):
    def test_links_in_and_out_across_notes_and_cards(self):
        self.ult("board", "add", "Checkout", "--link", "pricing")
        self.ult("notes", "add", "pricing", "Stripe, three tiers; see [[brand]]")
        self.ult("notes", "add", "brand", "Blue, calm")
        r = self.ult("notes", "links", "pricing")
        self.assertIn("out: brand", r.out)
        self.assertIn("in: C1", r.out)
        r = self.ult("notes", "links", "brand")
        self.assertIn("in: pricing", r.out)
        self.assertEqual(self.ult("notes", "list").out.split(), ["brand", "pricing"])
        self.assertIn("- Blue, calm", self.ult("notes", "show", "brand").out)

    def test_missing_note_fails(self):
        self.assertEqual(self.ult("notes", "show", "nope").code, 2)
        self.assertEqual(self.ult("notes", "add", "x").code, 2)


if __name__ == "__main__":
    unittest.main()
