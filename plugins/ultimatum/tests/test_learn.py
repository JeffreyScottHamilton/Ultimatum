"""Tests for `ult learn`: lesson store, relevance, observation hook and proposals."""
import json
import os
import sys
import time
import unittest
from unittest import mock

from _harness import UltCase, SCRIPTS

sys.path.insert(0, SCRIPTS)
from ultlib import learn  # noqa: E402

FAKE_SECRETS = [
    "AKIAABCDEFGHIJKLMNOP",
    "ghp_" + "a" * 36,
    "sk-ant-api03-" + "Z" * 30,
]
FORBIDDEN_IN_PROPOSALS = FAKE_SECRETS + [
    "alice", "acme", "billing", "example.com", "github.com", "/home/", "PRIVATE-PROMPT",
    "fix the", "failing test", "pytest", "npm", "ANTHROPIC", "token", "invoices",
]


def tool_pair(i, name, inp, content, is_error=False):
    usage = {"input_tokens": 5, "output_tokens": 7, "cache_read_input_tokens": 100, "cache_creation_input_tokens": 0}
    tid = f"t{i}"
    return [
        {"type": "assistant", "message": {"id": f"m{i}", "role": "assistant", "usage": usage,
                                          "content": [{"type": "tool_use", "id": tid, "name": name, "input": inp}]}},
        {"type": "user", "message": {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": tid, "content": content, "is_error": is_error}]}},
    ]


def write_transcript(path, prompt, failing_cmds=(), reads=(), big=0):
    entries = [{"type": "user", "message": {"role": "user", "content": prompt}}]
    i = 0
    for cmd in failing_cmds:
        i += 1
        entries += tool_pair(i, "Bash", {"command": cmd}, "boom", is_error=True)
    for f in reads:
        i += 1
        entries += tool_pair(i, "Read", {"file_path": f}, "ok")
    for _ in range(big):
        i += 1
        entries += tool_pair(i, "Bash", {"command": "ls"}, "x" * 25000)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(e) for e in entries) + "\n")
    return path


class LearnCase(UltCase):
    def setUp(self):
        super().setUp()
        self.home = self.tmp / "home"
        env = {"ULTIMATUM_HOME": str(self.home)}
        patcher = mock.patch.dict(os.environ, env)
        patcher.start()
        self.addCleanup(patcher.stop)
        for k in ("ULTIMATUM_OBSERVE", "ULTIMATUM_STATE_DIR"):
            os.environ.pop(k, None)

    def obs_path(self):
        return self.root / ".ultimatum" / "observations.jsonl"

    def proposal_files(self):
        d = self.root / ".ultimatum" / "proposals"
        return sorted(d.glob("*")) if d.is_dir() else []


class TestCleaning(unittest.TestCase):
    def test_clean_strips_control_and_caps_length(self):
        raw = "hello\x1b[31m\nworld‮ " + "a" * 300
        out = learn.clean_lesson(raw)
        self.assertLessEqual(len(out), learn.LESSON_MAX_CHARS)
        self.assertTrue(out.endswith("..."))
        self.assertFalse([c for c in out if c.isspace() and c != " " or (ord(c) < 32)])
        self.assertNotIn("‮", out)

    def test_clean_redacts_secrets(self):
        out = learn.clean_lesson("use " + FAKE_SECRETS[1] + " in CI")
        self.assertNotIn(FAKE_SECRETS[1], out)
        self.assertIn("[REDACTED", out)

    def test_prune_caps_store_and_expires_single_use(self):
        now = time.time()
        recs = [{"id": f"L{i}", "text": f"t{i}", "module": None, "count": 1, "created": now, "updated": now - i}
                for i in range(205)]
        recs.append({"id": "Lkeep", "text": "keep", "module": None, "count": 9, "created": now, "updated": 0})
        recs.append({"id": "Lold", "text": "old", "module": None, "count": 1, "created": 0, "updated": 0})
        kept = learn.prune(recs, now)
        self.assertLessEqual(len(kept), learn.LESSON_CAP)
        ids = {r["id"] for r in kept}
        self.assertIn("Lkeep", ids)
        self.assertNotIn("Lold", ids)


class TestLessonStore(LearnCase):
    def test_add_dedupes_and_counts(self):
        self.assertEqual(self.ult("learn", "add", "run the billing suite first").code, 0)
        r = self.ult("learn", "add", "Run the billing suite first")
        self.assertEqual(r.code, 0, r.all)
        out = self.ult("learn", "list").out
        self.assertEqual(out.count("lesson:"), 1)
        self.assertIn("x2", out)

    def test_global_scope_goes_to_home_not_project(self):
        self.assertEqual(self.ult("learn", "add", "keep ui snapshots small", "--scope", "global").code, 0)
        self.assertTrue((self.home / "lessons.jsonl").is_file())
        self.assertFalse((self.root / ".ultimatum" / "lessons.jsonl").exists())
        self.assertIn("lesson: keep ui snapshots small", self.ult("learn", "list", "--scope", "global").out)

    def test_add_redacts_and_reports_lesson_prefix(self):
        r = self.ult("learn", "add", "deploy with " + FAKE_SECRETS[1])
        self.assertEqual(r.code, 0, r.all)
        self.assertNotIn(FAKE_SECRETS[1], r.out)
        self.assertIn("lesson: ", r.out)

    def test_invalid_module_rejected(self):
        r = self.ult("learn", "add", "something", "--module", "../etc")
        self.assertEqual(r.code, 2)

    def test_empty_lesson_rejected(self):
        self.assertEqual(self.ult("learn", "add", "\x01\n").code, 2)

    def test_prune_cli_runs(self):
        self.ult("learn", "add", "one lesson")
        r = self.ult("learn", "prune")
        self.assertEqual(r.code, 0, r.all)
        self.assertIn("prune:", r.out)


class TestRelevant(LearnCase):
    def test_keyword_overlap_returns_prefixed_short_lines(self):
        self.ult("learn", "add", "run pytest -q tests/billing before editing invoices", "--module", "debugging")
        lines = learn.relevant("fix invoices rounding bug", self.root)
        self.assertEqual(len(lines), 1)
        self.assertTrue(lines[0].startswith("lesson: run pytest"))
        self.assertLessEqual(len(lines[0]), learn.RELEVANT_MAX_CHARS)

    def test_unrelated_task_gets_nothing(self):
        self.ult("learn", "add", "run pytest -q tests/billing before editing invoices")
        self.assertEqual(learn.relevant("restyle the landing hero banner", self.root), [])

    def test_limit_is_capped_at_three(self):
        for i in range(5):
            self.ult("learn", "add", f"invoices lesson number {i} with detail")
        self.assertEqual(len(learn.relevant("invoices", self.root, limit=10)), 3)

    def test_never_raises(self):
        self.assertEqual(learn.relevant(None, self.root), [])
        self.assertEqual(learn.relevant("invoices", object()), [])
        self.assertEqual(learn.relevant("invoices", "/nonexistent/dir/for/ult"), [])
        self.assertEqual(learn.relevant("invoices", self.root, limit="x"), [])

    def test_relevant_reads_knowledge_bullets(self):
        self.write(".ultimatum/knowledge.md", "# Knowledge\n- run make check before release\n")
        lines = learn.relevant("prepare the release notes", self.root)
        self.assertEqual(lines, ["lesson: run make check before release"])


class TestObservation(LearnCase):
    def test_hook_is_silent_on_malformed_input(self):
        r = self.ult("learn", "observe", "--hook", input="{not json")
        self.assertEqual((r.code, r.out, r.err), (0, "", ""))

    def test_hook_is_silent_on_missing_transcript(self):
        payload = json.dumps({"transcript_path": str(self.tmp / "missing.jsonl")})
        r = self.ult("learn", "observe", "--hook", input=payload)
        self.assertEqual((r.code, r.out, r.err), (0, "", ""))
        self.assertFalse(self.obs_path().exists())

    def test_hook_honours_disable_switch(self):
        t = write_transcript(self.tmp / "t.jsonl", "fix it", ["pytest -q"] * 3)
        with mock.patch.dict(os.environ, {"ULTIMATUM_OBSERVE": "0"}):
            r = self.ult("learn", "observe", "--hook", input=json.dumps({"transcript_path": str(t)}))
        self.assertEqual((r.code, r.out, r.err), (0, "", ""))
        self.assertFalse(self.obs_path().exists())

    def test_hook_records_counts_not_text(self):
        t = write_transcript(self.tmp / "t.jsonl", "PRIVATE-PROMPT-MARK fix the failing test",
                             failing_cmds=["pytest -q a"] * 3 + ["npm test --token " + FAKE_SECRETS[1]] * 3,
                             reads=["/home/alice/x.py"] * 3, big=2)
        r = self.ult("learn", "observe", "--hook", input=json.dumps({"transcript_path": str(t)}))
        self.assertEqual((r.code, r.out, r.err), (0, "", ""))
        text = self.obs_path().read_text()
        rec = json.loads(text.splitlines()[-1])
        self.assertEqual(rec["category"], "bug")
        self.assertEqual(rec["signals"]["repeated-failure"], 2)
        self.assertEqual(rec["signals"]["re-read"], 1)
        self.assertEqual(rec["signals"]["big-output"], 2)
        self.assertEqual(rec["failing_kinds"], {"pytest": 3, "npm": 3})
        for bad in ["PRIVATE-PROMPT", "alice", "/home/", FAKE_SECRETS[1]]:
            self.assertNotIn(bad, text)

    def test_tail_reads_only_end_of_large_transcript(self):
        p = self.tmp / "big.jsonl"
        filler = json.dumps({"type": "noise", "pad": "y" * 1000})
        with open(p, "w") as fh:
            fh.write("STARTMARK\n")
            for _ in range(2600):
                fh.write(filler + "\n")
            fh.write("ENDMARK\n")
        self.assertGreater(p.stat().st_size, learn.TAIL_BYTES)
        text = learn._tail_text(p)
        self.assertNotIn("STARTMARK", text)
        self.assertIn("ENDMARK", text)
        self.assertLessEqual(len(text), learn.TAIL_BYTES)

    def test_manual_observe_prints_one_line(self):
        t = write_transcript(self.tmp / "t.jsonl", "explain how the module works")
        r = self.ult("learn", "observe", "--transcript", str(t))
        self.assertEqual(r.code, 0, r.all)
        self.assertIn("[ult learn] observed this chat (discover)", r.out)


class TestProposals(LearnCase):
    def test_no_observations_no_proposal(self):
        r = self.ult("learn", "propose")
        self.assertEqual(r.code, 0)
        self.assertIn("no proposal crossed the threshold", r.out)

    def test_proposals_never_contain_secrets_paths_or_repo_names(self):
        prompt = ("fix the failing test: key AKIAABCDEFGHIJKLMNOP for alice@example.com in "
                  "/home/alice/src/acme-billing; see https://github.com/acme/billing invoices")
        for n in range(3):
            t = write_transcript(
                self.tmp / f"chat{n}" / "s.jsonl", prompt,
                failing_cmds=[f"ANTHROPIC_API_KEY={FAKE_SECRETS[2]} pytest -q /home/alice/src/acme-billing/tests"] * 3
                + [f"npm test --token {FAKE_SECRETS[1]}"] * 3,
                reads=["/home/alice/src/acme-billing/invoices.py"] * 3,
                big=2)
            self.assertEqual(self.ult("learn", "observe", "--transcript", str(t)).code, 0)
        r = self.ult("learn", "propose")
        self.assertEqual(r.code, 0, r.all)
        self.assertIn("wrote", r.out)
        files = self.proposal_files()
        self.assertTrue(any(f.suffix == ".json" for f in files))
        self.assertTrue(any(f.suffix == ".md" for f in files))
        for f in files:
            for bad in FORBIDDEN_IN_PROPOSALS:
                self.assertNotIn(bad, f.read_text(), f"{bad!r} leaked into {f.name}")
        # observations may name a tool (pytest, npm) but never a secret, path or prompt text
        for bad in FAKE_SECRETS + ["alice", "acme", "/home/", "PRIVATE", "invoices"]:
            self.assertNotIn(bad, self.obs_path().read_text(), f"{bad!r} leaked into observations")
        for f in files:
            if f.suffix == ".json":
                self.assertEqual(set(json.loads(f.read_text())),
                                 {"id", "created", "plugin_version", "module", "signal", "category", "counts", "lesson"})

    def test_list_and_clear(self):
        for n in range(3):
            t2 = write_transcript(self.tmp / f"c{n}" / "s.jsonl", "fix the failing test", failing_cmds=["pytest"] * 3 + ["npm"] * 3)
            self.ult("learn", "observe", "--transcript", str(t2))
        self.ult("learn", "propose")
        out = self.ult("learn", "proposals").out
        self.assertIn("repeated-failure", out)
        pid = out.split()[0]
        self.assertEqual(self.ult("learn", "proposals", "--clear", pid).code, 0)
        self.assertEqual(self.ult("learn", "proposals").out.strip(), "[ult learn] no pending proposals")
        self.assertEqual(self.ult("learn", "proposals", "--clear", "../x").code, 2)


if __name__ == "__main__":
    unittest.main()
