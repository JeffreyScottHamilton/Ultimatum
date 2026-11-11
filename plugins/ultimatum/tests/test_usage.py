"""Tests for `ult usage` / `ult improve` (the efficiency coach)."""
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

ULT = str(Path(__file__).resolve().parents[1] / "scripts" / "ult")
SECRET_PROMPT_MARKER = "zebra-PRIVATE-prompt-7731"


def ts(offset=0):
    return time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime(time.time() + offset))


def assistant(mid, usage, tools=(), offset=0):
    content = [{"type": "tool_use", "id": tid, "name": name, "input": inp} for tid, name, inp in tools]
    return {"type": "assistant", "timestamp": ts(offset), "cwd": "/work/proj",
            "message": {"id": mid, "model": "claude-test", "role": "assistant", "content": content, "usage": usage}}


def result(tid, content, is_error=False, offset=0):
    return {"type": "user", "timestamp": ts(offset),
            "message": {"role": "user", "content": [{"type": "tool_result", "tool_use_id": tid,
                                                      "content": content, "is_error": is_error}]}}


def prompt(text, offset=0):
    return {"type": "user", "timestamp": ts(offset), "message": {"role": "user", "content": text}}


U = {"input_tokens": 10, "output_tokens": 100, "cache_read_input_tokens": 1000, "cache_creation_input_tokens": 50}


class CoachCase(unittest.TestCase):
    def setUp(self):
        self.cfg = Path(tempfile.mkdtemp())
        self.home = Path(tempfile.mkdtemp())
        self.proj = self.cfg / "projects" / "-work-proj"
        self.proj.mkdir(parents=True)

    def write(self, name, entries, sub=False):
        d = self.proj / "sess1" / "subagents" if sub else self.proj
        d.mkdir(parents=True, exist_ok=True)
        p = d / f"{name}.jsonl"
        p.write_text("\n".join(json.dumps(e) for e in entries) + "\n")
        return p

    def ult(self, *args):
        env = {**os.environ, "CLAUDE_CONFIG_DIR": str(self.cfg), "ULTIMATUM_HOME": str(self.home)}
        return subprocess.run([sys.executable, ULT, *args], capture_output=True, text=True, env=env, timeout=60)

    def session(self, name="s1", prompt_text="fix the failing test " + SECRET_PROMPT_MARKER, offset=0):
        big = "x" * 30000
        return self.write(name, [
            prompt(prompt_text, offset),
            # the same message id streamed twice: usage must count once
            assistant("m1", U, [("t1", "Bash", {"command": "pytest -q"})], offset),
            assistant("m1", U, [], offset),
            result("t1", big, is_error=True, offset=offset),
            assistant("m2", U, [("t2", "Bash", {"command": "pytest -q"})], offset),
            result("t2", "fail", is_error=True, offset=offset),
            assistant("m3", U, [("t3", "Bash", {"command": "pytest -q"})], offset),
            result("t3", "fail", is_error=True, offset=offset),
            assistant("m4", U, [("r1", "Read", {"file_path": "/work/proj/a.py"}),
                                ("r2", "Read", {"file_path": "/work/proj/a.py"}),
                                ("r3", "Read", {"file_path": "/work/proj/a.py"})], offset),
            prompt("no, that's wrong, try again", offset),
        ])


class TestUsageReport(CoachCase):
    def test_report_counts_and_findings(self):
        self.session()
        r = self.ult("usage", "report", "--since", "1d")
        self.assertEqual(r.returncode, 0, r.stderr)
        out = r.stdout
        self.assertIn("**1 sessions**", out)
        # 4 unique messages x 1160 tokens (m1 counted once despite two entries)
        self.assertIn(f"{4 * 1160:,} tokens", out)
        for fid in ("big-tool-output", "repeated-failures", "repeated-reads", "corrections"):
            self.assertIn(fid, out)
        self.assertIn("`pytest -q` failed 3x", out)
        self.assertIn("| bug | 1 |", out)

    def test_prompt_text_never_in_report_or_saved_files(self):
        self.session()
        r = self.ult("usage", "report", "--since", "1d", "--save")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertNotIn(SECRET_PROMPT_MARKER, r.stdout)
        for f in (self.home / "coach" / "reports").iterdir():
            self.assertNotIn(SECRET_PROMPT_MARKER, f.read_text())
            self.assertEqual(f.stat().st_mode & 0o777, 0o600)

    def test_secrets_in_commands_are_redacted(self):
        tok = "ghp_" + "A1b2C3d4" * 4 + "Zz9Y"
        self.write("s1", [prompt("fix it"), *[x for i in range(3) for x in (
            assistant(f"m{i}", U, [(f"t{i}", "Bash", {"command": f"curl -H 'Authorization: token {tok}' x"})]),
            result(f"t{i}", "denied", is_error=True))]])
        r = self.ult("usage", "report", "--since", "1d")
        self.assertNotIn(tok, r.stdout)
        self.assertIn("REDACTED", r.stdout)

    def test_subagent_tokens_attributed(self):
        self.session()
        self.write("agent-1", [assistant("sm1", U)], sub=True)
        r = self.ult("usage", "report", "--since", "1d")
        self.assertIn("(+1 subagent runs)", r.stdout)
        self.assertIn("| (subagents) | 1 |", r.stdout)

    def test_window_excludes_old_entries(self):
        self.session(offset=-10 * 86400)
        r = self.ult("usage", "report", "--since", "1d")
        self.assertEqual(r.returncode, 1)

    def test_no_transcripts(self):
        r = self.ult("usage", "report", "--since", "1d", "--project", "nothing-matches")
        self.assertEqual(r.returncode, 1)
        self.assertIn("no transcripts", r.stdout)


class TestImproveLedger(CoachCase):
    def test_propose_apply_measure_keep(self):
        for i in range(3):
            self.session(f"before{i}", "fix bug")
        r = self.ult("improve", "propose", "--title", "Document test command", "--target", "./CLAUDE.md",
                     "--finding", "repeated-failures", "--category", "bug")
        self.assertIn("I-001 proposed", r.stdout)
        r = self.ult("improve", "apply", "I-001", "--baseline", "1d")
        self.assertIn('"sessions": 3', r.stdout)
        time.sleep(1.1)
        for i in range(3):  # cheaper sessions after the change
            self.write(f"after{i}", [prompt("fix bug", 2), assistant(f"a{i}", {"output_tokens": 10}, offset=2)])
        r = self.ult("improve", "measure", "I-001")
        self.assertIn("KEEP", r.stdout)
        r = self.ult("improve", "keep", "I-001", "--evidence", "tokens down")
        self.assertIn("kept", r.stdout)
        ledger = json.loads((self.home / "coach" / "experiments.json").read_text())
        self.assertEqual(ledger[0]["state"], "kept")

    def test_measure_needs_enough_sessions(self):
        self.session("b0", "fix bug")
        self.ult("improve", "propose", "--title", "x", "--category", "bug")
        self.ult("improve", "apply", "I-001", "--baseline", "1d")
        r = self.ult("improve", "measure", "I-001")
        self.assertIn("not enough sessions", r.stdout)

    def test_bad_id_rejected(self):
        r = self.ult("improve", "measure", "../x")
        self.assertNotEqual(r.returncode, 0)


if __name__ == "__main__":
    unittest.main()
