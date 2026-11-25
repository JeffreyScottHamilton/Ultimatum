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
RESEND = "send your message again to continue in this chat"


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

    def start(self, enabled=True, source="startup"):
        e = self.env()
        e.pop("ULTIMATUM_GUARD", None)
        if enabled:
            e["ULTIMATUM_GUARD"] = "1"
        payload = json.dumps({"session_id": "new", "transcript_path": str(self.tmp / "new.jsonl"),
                              "cwd": str(self.root), "hook_event_name": "SessionStart", "source": source})
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
        r = self.guard(self.transcript(turn(20_000), turn(400_001)), prompt="fix the login bug")
        self.assertEqual(r.returncode, 2)
        self.assertIn(MESSAGE, r.stderr)
        self.assertEqual(r.stdout, "")
        text = self.handoff().read_text()
        self.assertIn("ult-guard blocked a prompt", text)
        self.assertIn("fix the login bug", text)

    def test_exactly_at_limit_passes(self):
        self.assertEqual(self.guard(self.transcript(turn(400_000))).returncode, 0)

    def test_idle_large_chat_blocks(self):
        r = self.guard(self.transcript(turn(200_000, offset=-241 * 60)))
        self.assertEqual(r.returncode, 2)
        self.assertIn(MESSAGE, r.stderr)
        self.assertIn(RESEND, r.stderr)
        self.assertIn("idle 241 minutes", r.stderr)

    def test_idle_small_chat_passes(self):
        r = self.guard(self.transcript(turn(5_000, offset=-854 * 60)))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertFalse(self.handoff().exists())

    def test_resending_in_blocked_chat_goes_through_once(self):
        t = self.transcript(turn(200_000, offset=-300 * 60))
        self.assertEqual(self.guard(t).returncode, 2)
        r = self.guard(t)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.start().stdout, "")  # stayed in the chat: no resume in the next new chat
        self.assertEqual(self.guard(t).returncode, 2)  # a later, separate prompt is judged afresh

    def test_thresholds_are_configurable(self):
        t = self.transcript(turn(60_000, offset=-10 * 60))
        self.assertEqual(self.guard(t, ULTIMATUM_GUARD_TOKENS="50000").returncode, 2)
        self.assertEqual(self.guard(t, ULTIMATUM_GUARD_IDLE_MIN="5").returncode, 0)
        self.assertEqual(self.guard(t, ULTIMATUM_GUARD_IDLE_MIN="5",
                                    ULTIMATUM_GUARD_IDLE_TOKENS="50000").returncode, 2)
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
        self.assertEqual(self.guard(self.transcript(turn(500_000))).returncode, 2)
        text = self.handoff().read_text()
        self.assertIn("Ship the billing page", text)
        self.assertIn("use Stripe — already integrated", text)
        self.assertIn("wire the webhook", text)

    def test_new_chat_resumes_after_block_once(self):
        self.assertEqual(self.guard(self.transcript(turn(500_000)), prompt="fix the login bug").returncode, 2)
        r = self.start()
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("stopped by the Ultimatum chat-size guard", r.stdout)
        self.assertIn("fix the login bug", r.stdout)
        self.assertEqual(self.start().stdout, "")  # consumed: the next new chat starts clean

    def test_new_chat_without_block_adds_nothing(self):
        self.ult("handoff", "write", "--goal", "unrelated manual handoff")
        r = self.start()
        self.assertEqual((r.returncode, r.stdout), (0, ""))

    def test_resume_off_when_guard_off(self):
        self.guard(self.transcript(turn(500_000)))
        self.assertEqual(self.start(enabled=False).stdout, "")
        self.assertIn("chat-size guard", self.start().stdout)  # still pending for when it is on

    def test_stale_block_is_not_resumed(self):
        self.guard(self.transcript(turn(500_000)))
        marker = self.root / ".ultimatum" / "guard-pending"
        old = time.time() - 8 * 24 * 3600
        os.utime(marker, (old, old))
        self.assertEqual(self.start().stdout, "")
        self.assertFalse(marker.exists())

    def test_session_start_does_not_create_state_dir(self):
        self.start()
        self.assertFalse((self.root / ".ultimatum").exists())

    def test_hooks_json_points_at_guard(self):
        cfg = json.loads((Path(SCRIPTS).parent / "hooks" / "hooks.json").read_text())
        guard = "${CLAUDE_PLUGIN_ROOT}/scripts/ult-guard"
        self.assertIn(guard, cfg["hooks"]["UserPromptSubmit"][0]["hooks"][0]["command"])
        by_matcher = {e["matcher"]: " ".join(h["command"] for h in e["hooks"]) for e in cfg["hooks"]["SessionStart"]}
        self.assertIn(guard, by_matcher["startup|clear"])
        # the post-compaction hook prints the handoff and never runs the guard
        self.assertIn("handoff show", by_matcher["compact"])
        self.assertNotIn("ult-guard", by_matcher["compact"])


if __name__ == "__main__":
    import unittest
    unittest.main()
