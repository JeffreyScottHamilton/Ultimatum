import re
import unittest

from _harness import UltCase, PY


class TestStore(UltCase):
    def test_note_roundtrip(self):
        r = self.ult("note", "--kind", "decision", "--title", "Use WAL mode", "--body", "sqlite journal_mode=WAL because concurrent readers")
        self.assertEqual(r.code, 0, r.all)
        ref = r.out.strip()
        self.assertRegex(ref, r"^note:\d+$")
        f = self.ult("find", "journal_mode")
        self.assertEqual(f.code, 0, f.all)
        self.assertIn(ref, f.out)
        self.assertIn("(decision)", f.out)
        g = self.ult("get", ref)
        self.assertIn("[decision] Use WAL mode", g.out)
        self.assertIn("sqlite journal_mode=WAL because concurrent readers", g.out)

    def test_find_kind_filter_and_no_match(self):
        self.ult("note", "--kind", "fact", "--title", "t1", "--body", "zebra stripes")
        self.ult("note", "--kind", "todo", "--title", "t2", "--body", "zebra later")
        r = self.ult("find", "zebra", "--kind", "todo")
        self.assertIn("(todo)", r.out)
        self.assertNotIn("(fact)", r.out)
        r = self.ult("find", "qqqnotpresent")
        self.assertEqual(r.code, 1)
        self.assertIn("no matches", r.out)

    def test_note_stdin(self):
        r = self.ult("note", "--title", "stdin", "--body", "-", input="multi\nline body marmalade\n")
        ref = r.out.strip()
        self.assertIn("marmalade", self.ult("get", ref).out)

    def test_note_body_redacted(self):
        secret = "gh" + "p_" + "Q1w2E3r4T5" * 4
        r = self.ult("note", "--title", "leak", "--body", f"token {secret}")
        ref = r.out.strip()
        self.assertNotIn(secret, self.ult("get", ref).out)
        self.assertNotIn(secret, self.ult("find", "token").out)

    def test_punctuation_queries_do_not_crash(self):
        self.ult("note", "--title", "err", "--body", "got TypeError: x is not a function in a.b(c)")
        for q in ["TypeError:", "a.b(c)", '"quoted"', "foo*", "NEAR(a b)", "AND", "OR", "-", "x:y", "(", ")", "a'b", "col:val", "^start", "{}", "a OR b"]:
            r = self.ult("find", q)
            self.assertIn(r.code, (0, 1), f"{q!r}: {r.all}")
            self.assertNotIn("Traceback", r.err, f"{q!r}: {r.err}")
        r = self.ult("find", "TypeError:")
        self.assertEqual(r.code, 0, r.all)
        r = self.ult("find", "a.b(c)")
        self.assertEqual(r.code, 0, r.all)

    def test_find_empty_string_query(self):
        r = self.ult("find", "")
        self.assertNotIn("Traceback", r.err, r.err)

    def test_log_chunks_findable_and_get_exact(self):
        code = "for i in range(1, 121): print('line', i, 'needle_%d' % i if i in (5, 95) else '')"
        self.ult("run", "--name", "idx", "--", PY, "-c", code)
        meta = self.last_meta()
        rid = meta["id"]
        r = self.ult("find", "needle_95")
        self.assertEqual(r.code, 0, r.all)
        m = re.search(r"(log:[\w.-]+:\d+-\d+)", r.out)
        self.assertTrue(m, r.out)
        ref = m.group(1)
        self.assertTrue(ref.startswith(f"log:{rid}:"))
        a, b = (int(x) for x in ref.rsplit(":", 1)[1].split("-"))
        self.assertTrue(a <= 95 <= b)
        g = self.ult("get", ref)
        self.assertIn("95\tline 95 needle_95", g.out)

    def test_get_log_range_exact(self):
        self.ult("run", "--name", "g", "--", PY, "-c", "for i in range(1,31): print('L', i)")
        rid = self.last_meta()["id"]
        g = self.ult("get", f"log:{rid}:3-5")
        self.assertEqual(g.out.splitlines(), ["3\tL 3", "4\tL 4", "5\tL 5"])
        # range past EOF is clamped
        g = self.ult("get", f"log:{rid}:29-99")
        self.assertEqual(g.out.splitlines(), ["29\tL 29", "30\tL 30"])

    def test_get_unknown_note(self):
        r = self.ult("get", "note:999")
        self.assertEqual(r.code, 1)

    def test_get_missing_log_no_traceback(self):
        # BUG: store.py:87 `ult get log:nonexistent:1-2` -> uncaught FileNotFoundError traceback
        # (expected: "not found" message and exit 1).
        r = self.ult("get", "log:nonexistent:1-2")
        self.assertNotIn("Traceback", r.err, r.err)

    def test_get_malformed_log_ref_no_traceback(self):
        # BUG: store.py:83-85 `ult get log:bad` / `log:x:a-b` -> uncaught ValueError traceback.
        for ref in ("log:bad", "log:x:a-b", "log:x:5"):
            r = self.ult("get", ref)
            self.assertNotIn("Traceback", r.err, f"{ref}: {r.err[-200:]}")

    def test_get_log_path_traversal(self):
        outside = self.tmp.parent / "ult-outside-secret.log"
        outside.write_text("TOP SECRET OUTSIDE\n")
        self.addCleanup(outside.unlink)
        r = self.ult("get", "log:../../../ult-outside-secret:1-1")
        # BUG: store.py:84-86 `ult get log:../../../x:1-1` reads <anything>.log outside .ultimatum/logs; get joins the ref's rid into a path unsanitised -> arbitrary .log read
        self.assertNotIn("TOP SECRET OUTSIDE", r.out)

    def test_two_notes_same_ms_get_distinct_refs(self):
        import sys
        sys.path.insert(0, __import__("_harness").SCRIPTS)
        import os
        os.environ["ULTIMATUM_ROOT"] = str(self.root)
        self.addCleanup(os.environ.pop, "ULTIMATUM_ROOT", None)
        from ultlib import store
        refs = {store.add_note("note", f"t{i}", f"body{i}") for i in range(30)}
        self.assertEqual(len(refs), 30)  # BUG candidate: ref is int(time.time()*1000)

    def test_rerun_same_id_not_duplicated(self):
        self.ult("run", "--", PY, "-c", "print('uniqueword')")
        r = self.ult("find", "uniqueword")
        self.assertEqual(sum(1 for l in r.out.splitlines() if l.startswith("log:")), 1)

    def test_empty_output_run_indexed_without_crash(self):
        r = self.ult("run", "--", PY, "-c", "pass")
        self.assertEqual(r.code, 0)
        self.assertNotIn("index not updated", r.all)


if __name__ == "__main__":
    unittest.main()
