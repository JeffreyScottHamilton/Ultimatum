# Handoff — 2026-11-09

## Goal
Add a per-key burst override to the rate limiter: a key listed in `Config.burst_overrides` gets its own bucket capacity instead of the global `burst`. Keys without an override keep the default.

## Decisions (with why)
- Overrides live in `Config.burst_overrides: dict[str, int]` (not on `Limiter`), because config is the single place callers already pass settings through.
- Lookup goes through a `Config.override_for(key)` method that falls back to `Config.burst`, so `Limiter` never touches the dict directly. This keeps the fallback rule in one place.
- Override changes capacity only, not refill rate. Rate-per-key was explicitly out of scope.
- `TokenBucket` takes `capacity` as a constructor argument (already done) so each key's bucket can differ; do not add global state.
- Buckets are created lazily on first `allow(key)`, so an override added later does not resize an existing bucket. Accepted for now.

## Changed files
- `ratelimit/bucket.py` — `TokenBucket(rate, capacity, clock)`: capacity is now a per-instance argument, refill is capped at it.
- `ratelimit/config.py` — added `burst_overrides` field and a TODO for `override_for`. Method NOT yet written.
- `tests/test_burst.py` — new, 3 tests.

## Evidence (commands run, exit codes, log refs)
- `python3 -m unittest tests.test_bucket` -> exit 0, 3 tests OK
- `python3 -m unittest tests.test_burst` -> exit 1, 3 run, 2 pass, 1 fail:
  `test_burst_override_applies` (vip gets capacity 2 instead of 5, since `Limiter` still reads `config.burst`)
- `test_default_burst_when_no_override` and `test_override_does_not_affect_other_keys` pass.

## Next unfinished step
Implement `override_for(key)` lookup in `config.py` (return `burst_overrides.get(key, burst)`), switch `Limiter._bucket_for` to use it, and make `test_burst_override_applies` pass. Then run the full suite.

## Open questions
- Should an override of 0 mean "block this key entirely"? Currently it would create a bucket that never allows. Undecided; leave as is unless asked.
- Do we need runtime updates to overrides (resize live buckets)? Not for this task.
