"""Tests for the opt-in UserPromptSubmit guard (scripts/ult-guard)."""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

from _harness import SCRIPTS, UltCase

GUARD = str(Path(SCRIPTS) / "ult-guard")
MESSAGE = "Chat too large. Start a new chat and type: /ultimatum:work resume"


def ts(offset=0):
    return time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime(time.time() + offset))


def turn(tokens, offset=0):
    return {"type": "assistant", "timestamp": ts(offset),
            "message": {"id": f"m{tokens}{offset}", "role": "assistant", "content": [],
                        "usage": {"input_tokens": 10, "cache_read_input_tokens": tokens - 10,
                                  "cache_creation_input_tokens": 0, "output_tokens": 5}}}


class GuardCase(UltCase):
    def transcript(self, *entries):
        p = self.tmp / "chat.jsonl"
        p.write_text("\n".join(json.dumps(e) for e in entries) + "\n")
        return p

    def guard(self, transcript, enabled=True, prompt="next step please", **env):
        e = self.env()
        e.pop("ULTIMATUM_GUARD", None)
        if enabled:
            e["ULTIMATUM_GUARD"] = "1"
        e.update(env)
        payload = json.dumps({"session_id": "s", "transcript_path": str(transcript), "cwd": str(self.root),
                              "hook_event_name": "UserPromptSubmit", "prompt": prompt})
        return subprocess.run([sys.executable, GUARD], input=payload, capture_output=True, text=True,
                              env=e, cwd=str(self.root), timeout=60)

    def handoff(self):
        return self.root / ".ultimatum" / "handoff.md"

    def test_off_by_default_even_when_huge(self):
        r = self.guard(self.transcript(turn(900_000)), enabled=False)
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stderr, "")
        self.assertFalse(self.handoff().exists())

    def test_small_recent_chat_passes(self):
        r = self.guard(self.transcript(turn(20_000), turn(40_000)))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertFalse(self.handoff().exists())

    def test_large_chat_blocks_and_writes_handoff(self):
        r = self.guard(self.transcript(turn(20_000), turn(150_001)), prompt="fix the login bug")
        self.assertEqual(r.returncode, 2)
        self.assertIn(MESSAGE, r.stderr)
        self.assertEqual(r.stdout, "")
        text = self.handoff().read_text()
        self.assertIn("ult-guard blocked a prompt", text)
        self.assertIn("fix the login bug", text)

    def test_exactly_at_limit_passes(self):
        self.assertEqual(self.guard(self.transcript(turn(150_000))).returncode, 0)

    def test_idle_chat_blocks(self):
        r = self.guard(self.transcript(turn(5_000, offset=-61 * 60)))
        self.assertEqual(r.returncode, 2)
        self.assertIn(MESSAGE, r.stderr)
        self.assertIn("idle 61 minutes", r.stderr)

    def test_thresholds_are_configurable(self):
        t = self.transcript(turn(60_000, offset=-10 * 60))
        self.assertEqual(self.guard(t, ULTIMATUM_GUARD_TOKENS="50000").returncode, 2)
        self.assertEqual(self.guard(t, ULTIMATUM_GUARD_IDLE_MIN="5").returncode, 2)
        self.assertEqual(self.guard(t).returncode, 0)

    def test_missing_transcript_or_bad_input_never_blocks(self):
        self.assertEqual(self.guard(self.tmp / "nope.jsonl").returncode, 0)
        r = subprocess.run([sys.executable, GUARD], input="not json", capture_output=True, text=True,
                           env={**self.env(), "ULTIMATUM_GUARD": "1"}, timeout=60)
        self.assertEqual(r.returncode, 0)

    def test_block_keeps_existing_goal_and_next_step(self):
        self.assertEqual(self.ult("handoff", "write", "--goal", "Ship the billing page",
                                  "--decision", "use Stripe — already integrated",
                                  "--next", "wire the webhook").code, 0)
        self.assertEqual(self.guard(self.transcript(turn(400_000))).returncode, 2)
        text = self.handoff().read_text()
        self.assertIn("Ship the billing page", text)
        self.assertIn("use Stripe — already integrated", text)
        self.assertIn("wire the webhook", text)

    def test_hooks_json_points_at_guard(self):
        cfg = json.loads((Path(SCRIPTS).parent / "hooks" / "hooks.json").read_text())
        cmd = cfg["hooks"]["UserPromptSubmit"][0]["hooks"][0]["command"]
        self.assertIn("${CLAUDE_PLUGIN_ROOT}/scripts/ult-guard", cmd)


if __name__ == "__main__":
    import unittest
    unittest.main()
