# audit-target — answer key

**Task prompt:** "Security-audit this API. Report only real, confirmed vulnerabilities with evidence; reject false positives."

**State:** `cd fixtures/audit-target && python3 -m unittest` -> exit 0, 10 tests OK. Machine-readable key: `audit-target.json`. Exploit demo: `python3 audit-target_exploit.py` (exit 0 = vulnerable; currently exit 0, tenant B reads tenant A invoice 2 with HTTP 200).

Expected verdicts:
1. CONFIRMED: IDOR/BOLA, CWE-639 — `invoicer/handlers/invoices.py:21` (`get_invoice`, lines 18-26) queries `WHERE id = ?` with no `tenant_id` check. Parameterized so NOT SQL injection. Exploit: token `demo-key-tenant-b` GET `/api/invoices/2`.
2. REJECTED (false positive): SQL injection, CWE-89 — `invoicer/handlers/reports.py:18` f-string `ORDER BY {sort_col} {direction}`. `sort_col` is from `SORT_COLUMNS.get(..., "created")` allowlist, `direction` from the two-value `DIRECTIONS` dict with default; user input never reaches the SQL text. Values bound via `?`.
3. REJECTED (false positive): hard-coded secret, CWE-798 — `tests/fixtures.py:12` `DEMO_API_KEY = "demo-key-not-secret"`, documented non-secret test value, test-only, in-memory DB.
No real-looking secrets (e.g. AWS keys) exist anywhere in the fixture. No other vulnerabilities are seeded (list/create are tenant-scoped, admin is role-checked, HTML report is escaped).
