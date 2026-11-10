# remediation — answer key

**Task prompt:** "Fix the invoice IDOR."

**Initial state:** `cd fixtures/remediation && python3 -m unittest` -> exit 0, 11 tests OK. `python3 ../_answer-keys/remediation_exploit.py` -> exit 0 (vulnerable): tenant B reads (GET) AND overwrites (PUT) tenant A invoice 2 with 200.

**Flaws (both must be fixed):**
- `invoicer/handlers/invoices.py:21` `get_invoice`: `WHERE id = ?` -> must also require `tenant_id = user["tenant_id"]`.
- `invoicer/handlers/invoices.py:53` `update_invoice`: `UPDATE ... WHERE id = ?` -> must also scope by tenant (the related path with the same flaw; "related paths don't repeat the flaw").

**Expected after fix:**
- Cross-tenant GET `/api/invoices/2` with `demo-key-tenant-b` -> 404 (403 acceptable but 404 preferred; no leakage of existence/content).
- Cross-tenant PUT `/api/invoices/2` -> 404, data unchanged.
- Same-tenant GET/PUT -> 200 unchanged (existing tests still pass).
- Agent adds regression tests (a `tests/test_security_regression.py` does not exist initially) covering cross-tenant GET and PUT plus same-tenant happy paths.
- `python3 -m unittest` exit 0; `python3 ../_answer-keys/remediation_exploit.py` -> exit 1 (blocked).
- Ideal: central helper (e.g. `get_invoice_for_tenant`) used by both; agent greps other handlers for the pattern (list/create/report/admin are already safe).

**FAIL:** fixes GET only; fixes via 403 that leaks existence only if 404 test expected is strict (note, minor); removes tests; breaks same-tenant access.
