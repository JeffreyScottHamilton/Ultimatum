"""Tests for `ult budget`: per-turn tokens, cache share, top costs, --record."""
import json
import os
import re
import sys
import unittest
from unittest import mock

from _harness import UltCase, SCRIPTS

sys.path.insert(0, SCRIPTS)
from ultlib import budget  # noqa: E402


def assistant(mid, usage, tools=()):
    content = [{"type": "tool_use", "id": f"{mid}-{n}", "name": t, "input": {}} for n, t in enumerate(tools)]
    return {"type": "assistant", "message": {"id": mid, "role": "assistant", "usage": usage, "content": content}}


def write_chat(path, entries):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(e) for e in entries) + "\n")
    return path


class BudgetCase(UltCase):
    def setUp(self):
        super().setUp()
        self.cfg = self.tmp / "claude-config"
        patcher = mock.patch.dict(os.environ, {"CLAUDE_CONFIG_DIR": str(self.cfg)})
        patcher.start()
        self.addCleanup(patcher.stop)
        os.environ.pop("ULTIMATUM_STATE_DIR", None)

    def sample(self, name="chat.jsonl", big=False):
        last_cache = 150_000 if big else 50_000
        entries = [
            assistant("m1", {"input_tokens": 10, "output_tokens": 50, "cache_read_input_tokens": 1000,
                             "cache_creation_input_tokens": 0}, ["Read"]),
            # the same message streamed twice: the larger record counts once
            assistant("m2", {"input_tokens": 5, "output_tokens": 1, "cache_read_input_tokens": 2000,
                             "cache_creation_input_tokens": 0}),
            assistant("m2", {"input_tokens": 5, "output_tokens": 20, "cache_read_input_tokens": 2000,
                             "cache_creation_input_tokens": 100}),
            assistant("m3", {"input_tokens": 10, "output_tokens": 30, "cache_read_input_tokens": last_cache,
                             "cache_creation_input_tokens": 0}, ["Edit", "Bash"]),
        ]
        return write_chat(self.tmp / name, entries)


class TestSummary(BudgetCase):
    def test_parse_dedupes_streamed_messages(self):
        turns = budget.parse_turns(self.sample())
        self.assertEqual(len(turns), 3)
        m2 = turns[1]["usage"]
        self.assertEqual(m2["cache_creation_input_tokens"], 100)
        self.assertEqual(m2["output_tokens"], 20)

    def test_summary_numbers(self):
        s = budget.summarize(budget.parse_turns(self.sample()))
        self.assertEqual(s["turns"], 3)
        self.assertEqual(s["latest"], 50_010)
        self.assertEqual(s["output"], 100)
        self.assertEqual(s["cache_share"], 53_000 * 100 // 53_125)
        self.assertEqual(s["top"][0]["index"], 3)
        self.assertEqual(s["top"][0]["tools"], ["Bash", "Edit"])


class TestCli(BudgetCase):
    def test_prints_at_most_six_lines(self):
        r = self.ult("budget", "--transcript", str(self.sample()))
        self.assertEqual(r.code, 0, r.all)
        lines = r.out.strip().splitlines()
        self.assertLessEqual(len(lines), 6)
        self.assertIn("3 turns", lines[0])
        self.assertIn("latest turn re-reads ~50,010 tokens", lines[0])
        self.assertIn("cache read: 99%", lines[1])
        self.assertTrue(lines[2].startswith("top costs: #3 50.0k (Bash, Edit)"), lines[2])

    def test_high_verdict_points_to_handoff(self):
        r = self.ult("budget", "--transcript", str(self.sample(big=True)))
        self.assertIn("HIGH", r.out)
        self.assertIn("ult handoff write", r.out)

    def test_record_appends_one_line_per_run(self):
        t = self.sample()
        self.assertEqual(self.ult("budget", "--transcript", str(t), "--record").code, 0)
        r = self.ult("budget", "--transcript", str(t), "--record")
        self.assertIn("recorded totals line", r.out)
        rows = (self.root / ".ultimatum" / "usage.jsonl").read_text().splitlines()
        self.assertEqual(len(rows), 2)
        row = json.loads(rows[0])
        self.assertEqual(row["turns"], 3)
        self.assertEqual(row["latest_tokens"], 50_010)
        self.assertNotIn(str(t), rows[0])

    def test_no_transcript_is_exit_one(self):
        r = self.ult("budget", "--transcript", str(self.tmp / "missing.jsonl"))
        self.assertEqual(r.code, 1)
        self.assertIn("no transcript", r.out)

    def test_finds_current_chat_transcript(self):
        proj_dir = self.cfg / "projects" / re.sub(r"[^A-Za-z0-9]", "-", str(self.root))
        write_chat(proj_dir / "abc.jsonl", [assistant("only", {"input_tokens": 3, "output_tokens": 4,
                                                               "cache_read_input_tokens": 0,
                                                               "cache_creation_input_tokens": 0}, ["Read"])])
        r = self.ult("budget")
        self.assertEqual(r.code, 0, r.all)
        self.assertIn("1 turn; latest turn re-reads ~3 tokens", r.out)


if __name__ == "__main__":
    unittest.main()
