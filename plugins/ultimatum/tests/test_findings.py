import json
import re
import unittest
from pathlib import Path

from _harness import UltCase

SCHEMAS = Path(__file__).resolve().parent.parent / "schemas"
GH = "gh" + "p_" + "aB3dE6gH9jK2mN5pQ8sT1vW4yZ7bC0eF3hJ6"  # assembled at runtime; not a real token


def confirmed(**kw):
    f = {"id": "F-001", "title": "Download not scoped to owner", "status": "confirmed", "file": "app/docs.py", "line": 42,
         "endpoint": "GET /docs/<id>/download", "entry_point": "app/docs.py:38", "actor": "any logged-in user",
         "input": "id path parameter", "boundary": "users download only their own account's documents",
         "preconditions": "a normal account", "impact": "reads other accounts' documents",
         "evidence": ["app/docs.py:42 Document.query.get(id) has no owner filter"], "severity": "high",
         "confidence": "high", "found_by": "hunter:authz", "verified_by": "verifier:1"}
    f.update(kw)
    return f


def nv(**kw):
    f = {"id": "F-002", "title": "Proxy header trust", "status": "needs-validation", "file": "app/mw.py", "line": 3,
         "boundary": "identity comes only from the session", "missing_evidence": "whether the proxy strips X-User-Id",
         "suggested_severity": "high"}
    f.update(kw)
    return f


def rej(**kw):
    f = {"id": "F-003", "title": "eval in build script", "status": "rejected", "file": "scripts/build.py", "line": 9,
         "boundary": "no code execution from input", "rejection_reason": "argument is a constant (scripts/build.py:8)",
         "rejected_by_pattern": "FP-01"}
    f.update(kw)
    return f


class FindingsCase(UltCase):
    def put(self, items, name="f.json"):
        p = self.write(name, json.dumps({"scope": "repo at HEAD", "findings": items}))
        return p

    def validate(self, items):
        return self.ult("findings", "validate", str(self.put(items)))


class TestValidate(FindingsCase):
    def test_valid_file(self):
        r = self.validate([confirmed(), nv(), rej()])
        self.assertEqual(r.code, 0, r.all)
        self.assertIn("OK 3 finding(s)", r.out)
        self.assertIn("confirmed=1", r.out)

    def test_bare_array_ok(self):
        p = self.write("a.json", json.dumps([nv()]))
        self.assertEqual(self.ult("findings", "validate", str(p)).code, 0)

    def assertInvalid(self, items, needle):
        r = self.validate(items)
        self.assertEqual(r.code, 1, r.all)
        self.assertIn(needle, r.out)

    def test_status_enum(self):
        self.assertInvalid([nv(status="needs_validation")], "not in")

    def test_confirmed_needs_evidence_and_severity(self):
        self.assertInvalid([confirmed(evidence=[])], "confirmed finding needs 'evidence'")
        self.assertInvalid([confirmed(severity=None)], "confirmed finding needs 'severity'")
        self.assertInvalid([confirmed(severity="unrated")], "not 'unrated'")
        self.assertInvalid([confirmed(severity="severe")], "severity 'severe'")

    def test_needs_validation_rules(self):
        self.assertInvalid([nv(missing_evidence="")], "missing_evidence")
        self.assertInvalid([nv(severity="high")], "must not carry severity")
        self.assertEqual(self.validate([nv(severity="unrated")]).code, 0)

    def test_rejected_needs_reason(self):
        self.assertInvalid([rej(rejection_reason=None)], "rejection_reason")
        self.assertInvalid([rej(rejected_by_pattern="pattern1")], "FP-01")

    def test_unredacted_secret_fails(self):
        r = self.validate([nv(missing_evidence=f"token {GH} seen in logs")])
        self.assertEqual(r.code, 1)
        self.assertIn("unredacted secret", r.out)
        self.assertNotIn(GH, r.all)

    def test_paths_ids_and_independence(self):
        self.assertInvalid([nv(file="/etc/app.py")], "repo-relative")
        self.assertInvalid([nv(file="../x.py")], "'..'")
        self.assertInvalid([nv(line=0)], "line must be")
        self.assertInvalid([nv(), nv()], "duplicate id")
        self.assertInvalid([confirmed(verified_by="hunter:authz")], "verified_by must differ")
        self.assertInvalid([{"status": "rejected"}], "missing required field 'title'")

    def test_warnings_do_not_fail(self):
        r = self.validate([confirmed(verified_by=None, extra_field=1)])
        self.assertEqual(r.code, 0, r.all)
        self.assertIn("unknown field", r.out)
        self.assertIn("no verified_by", r.out)

    def test_missing_file(self):
        self.assertEqual(self.ult("findings", "validate", "nope.json").code, 1)


class TestAdd(FindingsCase):
    def test_add_auto_ids_default_location_and_redaction(self):
        cand = {"title": "x", "file": "a.py", "boundary": "b", "missing_evidence": f"saw {GH}"}
        r = self.ult("findings", "add", input=json.dumps([cand, dict(cand, title="y")]))
        self.assertEqual(r.code, 0, r.all)
        p = self.root / ".ultimatum" / "security" / "findings.json"
        data = json.loads(p.read_text())
        self.assertEqual([f["id"] for f in data["findings"]], ["F-001", "F-002"])
        self.assertEqual(data["findings"][0]["status"], "needs-validation")
        self.assertNotIn(GH, p.read_text())
        self.assertIn("redacted", r.out)
        r = self.ult("findings", "add", input="Hunter result:\n```json\n" + json.dumps([dict(cand, title="z")]) + "\n```\n")
        self.assertEqual(r.code, 0, r.all)
        self.assertEqual(json.loads(p.read_text())["findings"][-1]["id"], "F-003")
        self.assertEqual(self.ult("findings", "validate").code, 0)

    def test_add_refuses_invalid(self):
        r = self.ult("findings", "add", input=json.dumps({"title": "x", "file": "a.py", "boundary": "b"}))
        self.assertEqual(r.code, 1)
        self.assertIn("nothing written", r.out)
        self.assertFalse((self.root / ".ultimatum" / "security" / "findings.json").exists())

    def test_add_jsonl(self):
        lines = "\n".join(json.dumps(nv(id=None, title=t)) for t in ("a", "b"))
        f = self.root / "x.json"
        r = self.ult("findings", "add", "--file", str(f), input=lines)
        self.assertEqual(r.code, 0, r.all)
        self.assertEqual(len(json.loads(f.read_text())["findings"]), 2)


class TestLedger(FindingsCase):
    def test_lifecycle(self):
        r = self.ult("findings", "ledger", "init", "--profile", "quick", "--scope", "repo HEAD")
        self.assertEqual(r.code, 0, r.all)
        lp = self.root / ".ultimatum" / "security" / "ledger.json"
        led = json.loads(lp.read_text())
        ids = [i["id"] for i in led["items"]]
        self.assertIn("authz-object", ids)
        self.assertEqual(self.ult("findings", "ledger", "init").code, 1)  # no silent overwrite
        r = self.ult("findings", "ledger", "check")
        self.assertEqual(r.code, 1)
        self.assertIn("INCOMPLETE", r.out)
        r = self.ult("findings", "ledger", "mark", "authn", "--state", "checked")
        self.assertEqual(r.code, 1)
        self.assertIn("needs --evidence", r.out)
        r = self.ult("findings", "ledger", "mark", "ai-agent", "--state", "not-applicable")
        self.assertEqual(r.code, 1)
        for i in ids:
            if i == "ai-agent":
                r = self.ult("findings", "ledger", "mark", i, "--state", "not-applicable", "--reason", "no agent configs")
            elif i == "dependencies":
                r = self.ult("findings", "ledger", "mark", i, "--state", "blocked", "--reason", "osv-scanner absent")
            else:
                r = self.ult("findings", "ledger", "mark", i, "--state", "checked", "--evidence", f"read {i} paths")
            self.assertEqual(r.code, 0, r.all)
        r = self.ult("findings", "ledger", "mark", "custom-webhooks", "--state", "checked", "--evidence", "app/hooks.py:1-40")
        self.assertEqual(r.code, 0, r.all)
        r = self.ult("findings", "ledger", "check")
        self.assertEqual(r.code, 0, r.all)
        self.assertIn("COMPLETE", r.out)

    def test_check_catches_hand_edits_and_bad_ids(self):
        p = self.write("l.json", json.dumps({"items": [
            {"id": "a", "state": "checked", "evidence": ""},
            {"id": "a", "state": "blocked"},
            {"id": "c", "state": "done"}]}))
        r = self.ult("findings", "ledger", "check", "--file", str(p))
        self.assertEqual(r.code, 1)
        for needle in ("checked but no evidence", "duplicate id", "state 'done'"):
            self.assertIn(needle, r.out)
        r = self.ult("findings", "ledger", "mark", "../evil", "--file", str(p), "--state", "checked", "--evidence", "x")
        self.assertEqual(r.code, 2)


class TestRender(FindingsCase):
    def test_render_grouped_sorted_with_coverage(self):
        low = confirmed(id="F-010", title="Low one", severity="low")
        crit = confirmed(id="F-011", title="Crit one", severity="critical")
        p = self.put([low, nv(), rej(), crit, confirmed()])
        self.ult("findings", "ledger", "init")
        out = self.root / "report.md"
        r = self.ult("findings", "render", str(p), "--ledger", ".ultimatum/security/ledger.json", "--out", str(out))
        self.assertEqual(r.code, 0, r.all)
        md = out.read_text()
        self.assertTrue(md.startswith("> **Partial coverage:**"), md[:200])
        i_c, i_n, i_r, i_cov = (md.index(h) for h in ("## Confirmed findings", "## Needs validation", "## Rejected candidates", "## Coverage"))
        self.assertTrue(i_c < i_n < i_r < i_cov)
        self.assertTrue(md.index("Crit one") < md.index("Download not scoped") < md.index("Low one"))
        self.assertIn("whether the proxy strips X-User-Id", md)
        self.assertIn("FP-01", md)
        self.assertIn("| authz-object |", md)

    def test_render_without_ledger_states_unknown_coverage(self):
        p = self.put([nv()])
        r = self.ult("findings", "render", str(p), "--out", str(self.root / "r.md"))
        self.assertEqual(r.code, 0, r.all)
        md = (self.root / "r.md").read_text()
        self.assertTrue(md.startswith("> **Coverage: unknown**"))
        self.assertIn("No confirmed findings within repo at HEAD", md)
        self.assertIn("not evidence of absence", md)


class TestSchemas(unittest.TestCase):
    def test_schemas_parse_and_match_validator(self):
        import sys
        sys.path.insert(0, str(SCHEMAS.parent / "scripts"))
        from ultlib import findings as F
        fs = json.loads((SCHEMAS / "findings.schema.json").read_text())
        ls = json.loads((SCHEMAS / "coverage-ledger.schema.json").read_text())
        self.assertEqual(fs["$schema"], "https://json-schema.org/draft/2020-12/schema")
        props = fs["$defs"]["finding"]["properties"]
        self.assertEqual(tuple(props["status"]["enum"]), F.STATUSES)
        self.assertEqual(tuple(fs["$defs"]["severity"]["enum"]), F.SEVERITIES)
        self.assertEqual(set(props), F.KNOWN_KEYS)
        self.assertEqual(tuple(ls["properties"]["items"]["items"]["properties"]["state"]["enum"]), F.LEDGER_STATES)
        then = [c["then"] for c in fs["$defs"]["finding"]["allOf"] if c["if"]["properties"]["status"]["const"] == "confirmed"][0]
        self.assertEqual(tuple(then["required"]), F.CONFIRMED_REQUIRED)


if __name__ == "__main__":
    unittest.main()
