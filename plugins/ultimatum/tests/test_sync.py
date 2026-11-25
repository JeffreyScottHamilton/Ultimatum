"""Tests for `ult sync`: export, merge-on-import, dedupe and untrusted input."""
import json
import os
import shutil
import sys
import time
import unittest
from unittest import mock

from _harness import UltCase, SCRIPTS

sys.path.insert(0, SCRIPTS)
from ultlib import learn, sync  # noqa: E402

FAKE_TOKEN = "ghp_" + "b" * 36


class SyncCase(UltCase):
    def setUp(self):
        super().setUp()
        self.home = self.tmp / "home"
        patcher = mock.patch.dict(os.environ, {"ULTIMATUM_HOME": str(self.home)})
        patcher.start()
        self.addCleanup(patcher.stop)
        for k in ("ULTIMATUM_OBSERVE", "ULTIMATUM_STATE_DIR"):
            os.environ.pop(k, None)
        self.dest = self.tmp / "private-copy"

    def switch_home(self, name):
        self.home = self.tmp / name
        os.environ["ULTIMATUM_HOME"] = str(self.home)

    def incoming(self, records):
        d = self.tmp / "incoming"
        d.mkdir(parents=True, exist_ok=True)
        (d / "lessons.jsonl").write_text("".join(json.dumps(r) + "\n" for r in records))
        return d


class TestRoundTrip(SyncCase):
    def test_export_then_import_on_a_fresh_machine(self):
        self.ult("learn", "add", "keep ui snapshots small", "--scope", "global")
        self.ult("learn", "add", "run make check before tagging", "--scope", "global")
        self.write(".ultimatum/knowledge.md", "# Knowledge\n- run make check before tagging\n")
        r = self.ult("sync", "export", "--to", str(self.dest))
        self.assertEqual(r.code, 0, r.all)
        self.assertIn("exported 2 global lesson(s); project knowledge included", r.out)
        self.assertTrue((self.dest / "lessons.jsonl").is_file())
        knowledge = list((self.dest / "projects").glob("*/knowledge.md"))
        self.assertEqual(len(knowledge), 1)

        shutil.rmtree(self.root / ".ultimatum")
        self.switch_home("fresh-home")
        r = self.ult("sync", "import", "--from", str(self.dest))
        self.assertEqual(r.code, 0, r.all)
        self.assertIn("2 new lesson(s)", r.out)
        self.assertIn("2 knowledge line(s) added", r.out)
        self.assertIn("lesson: keep ui snapshots small", self.ult("learn", "list", "--scope", "global").out)
        self.assertIn("- run make check before tagging", (self.root / ".ultimatum" / "knowledge.md").read_text())

    def test_import_is_idempotent(self):
        self.ult("learn", "add", "keep ui snapshots small", "--scope", "global")
        self.ult("sync", "export", "--to", str(self.dest))
        self.switch_home("second-home")
        self.ult("sync", "import", "--from", str(self.dest))
        r = self.ult("sync", "import", "--from", str(self.dest))
        self.assertEqual(r.code, 0, r.all)
        self.assertIn("0 new lesson(s), 0 updated, 0 knowledge line(s) added", r.out)
        self.assertEqual(len(learn.load_lessons(self.home / "lessons.jsonl")), 1)


class TestMerge(SyncCase):
    def test_newer_entry_wins_older_never_overwrites(self):
        now = time.time()
        self.ult("learn", "add", "run the billing suite first", "--scope", "global", "--module", "debugging")
        text = "run the billing suite first"
        lid = learn.lesson_id(text)
        src = self.incoming([
            {"id": lid, "text": text, "module": "ui", "count": 5, "created": 0, "updated": now - 365 * 86400},
            {"id": learn.lesson_id("ship on fridays"), "text": "ship on fridays", "module": "release",
             "count": 2, "created": 0, "updated": now + 60},
        ])
        self.ult("learn", "add", "ship on fridays", "--scope", "global", "--module", "bug-old")
        r = self.ult("sync", "import", "--from", str(src))
        self.assertEqual(r.code, 0, r.all)
        recs = {x["text"]: x for x in learn.load_lessons(self.home / "lessons.jsonl")}
        self.assertEqual(recs[text]["module"], "debugging")
        self.assertEqual(recs[text]["count"], 5)
        self.assertEqual(recs["ship on fridays"]["module"], "release")
        self.assertEqual(recs["ship on fridays"]["count"], 2)

    def test_knowledge_merge_keeps_local_text_and_appends_missing_lines(self):
        self.write(".ultimatum/knowledge.md", "# Mine\n- a line\n")
        src = self.tmp / "incoming"
        (src / "projects" / sync.project_key(self.root)).mkdir(parents=True)
        (src / "projects" / sync.project_key(self.root) / "knowledge.md").write_text("# Theirs\n- a line\n- b line\n")
        r = self.ult("sync", "import", "--from", str(src))
        self.assertEqual(r.code, 0, r.all)
        text = (self.root / ".ultimatum" / "knowledge.md").read_text()
        self.assertTrue(text.startswith("# Mine\n- a line\n"))
        self.assertEqual(text.count("- a line"), 1)
        self.assertEqual(text.count("- b line"), 1)

    def test_incoming_text_is_cleaned_and_redacted(self):
        src = self.incoming([{"id": "Lx", "text": "deploy with " + FAKE_TOKEN + "\x1b[2J\nnow",
                              "module": "bad module!", "count": 1, "created": 0, "updated": time.time()}])
        self.ult("sync", "import", "--from", str(src))
        stored = (self.home / "lessons.jsonl").read_text()
        self.assertNotIn(FAKE_TOKEN, stored)
        self.assertNotIn("\x1b", stored)
        self.assertIn("[REDACTED", stored)
        self.assertNotIn("bad module", stored)

    def test_missing_folder_is_an_error(self):
        r = self.ult("sync", "import", "--from", str(self.tmp / "nope"))
        self.assertEqual(r.code, 2)
        self.assertIn("not a folder", r.out)

    def test_export_only_includes_this_projects_knowledge(self):
        self.write(".ultimatum/knowledge.md", "- mine only\n")
        self.ult("sync", "export", "--to", str(self.dest))
        folders = list((self.dest / "projects").iterdir())
        self.assertEqual([f.name for f in folders], [sync.project_key(self.root)])


if __name__ == "__main__":
    unittest.main()
