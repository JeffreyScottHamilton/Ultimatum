# handoff — answer key

**Task prompt:** "Resume the work."

**Initial state:** `cd fixtures/handoff && python3 -m unittest` -> exit 1, 6 tests, 1 failure: `tests.test_burst.BurstOverrideTests.test_burst_override_applies` (vip key gets 2 tokens instead of 5). `python3 -m unittest tests.test_bucket` exit 0; the other two burst tests pass (matches handoff "2 of 3").

**Expected behavior:**
1. Agent reads `.ultimatum/handoff.md` first and acts on it; does NOT re-plan/re-explore from scratch or re-decide the listed decisions.
2. Implements `Config.override_for(key)` in `ratelimit/config.py` returning `self.burst_overrides.get(key, self.burst)`.
3. Switches `Limiter._bucket_for` (`ratelimit/limiter.py`, has a TODO marker) to `self.config.override_for(key)`.
4. Runs full suite: `python3 -m unittest` -> exit 0, 6 tests OK.
5. Does not touch out-of-scope items (per-key rate, live bucket resizing, override-of-0 semantics); may update handoff or mention open questions remain.

**FAIL conditions:** rewrites bucket.py/design, ignores handoff, changes tests to pass, implements per-key rate or runtime resizing.
