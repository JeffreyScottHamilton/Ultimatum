# QA for APIs, commands, jobs and webhooks

Read when what you are testing has no screen: an HTTP endpoint, a terminal command, a background worker, a scheduled task or a webhook handler. Use `qa-modes-and-loop.md` for isolation and the probe loop; this file says what to probe.

## Build a contract map first

List every behaviour the change could affect and write one line per contract. Check at least the ones that apply:

1. **Input validation:** missing, wrong type, too long, too large, odd characters, duplicate keys. Expect a clear refusal, not a crash or a silent default.
2. **Success path:** the documented result and the lasting effect (a row, a file, a sent message), not only the status code.
3. **Auth and permission:** no credentials, expired, wrong role, another tenant's id. The refusal must not leak whether the record exists.
4. **State change:** what was changed, and whether a failed call leaves it half-done.
5. **Idempotency and repeat:** the same request twice, the same webhook delivered twice, a retry after a timeout. No double charge, no duplicate row.
6. **Concurrency:** two requests at once against one record; last-write-wins surprises; lost updates.
7. **Errors and exit codes:** a failure returns a non-zero code or a 4xx/5xx with a useful message, never a success with an error body.
8. **Output shape:** fields, types, ordering, pagination edges (empty page, last page, page past the end), timestamps and time zones.
9. **Limits and timing:** rate limits, large payloads, slow dependencies, a timeout that is shorter than the work.
10. **Cleanup and side effects:** files, temp data, queues, emails or charges the run caused; confirm they landed in a fixture, not a real destination.

## Doing the probes

- Run against fixtures the run owns. Resolve the real destination of every URL, path and queue first.
- One command per probe, each with a time limit. Capture the command, exit code, trimmed output and the state afterwards.
- A non-zero exit that is the expected refusal is a pass; label it so, otherwise the report reads as failures.
- When you find a failure, repeat it from the same start state, then shrink the input (halve it until it stops failing) to the smallest case.
- Webhooks: send a signed sample, then the same one again, then one with a bad signature; check the retry and ordering behaviour the docs promise.
- Jobs: run once, run twice, run with the previous run still going, kill it midway and run again.

## Evidence tools

Prefer what the project already has: its test runner, `curl` against a local server, the command itself, a database client on a fixture. Save outputs as files in the report folder with redactions. For anything involving a browser as well, add a browser pass using `qa-playwright-recipes.md`.

## Severity

Use the same four levels as `qa-taxonomy.md`. Data loss, double charge, a leak across accounts and an auth bypass are critical. A wrong status code with correct behaviour is low or medium.

## Our additions

- Stripe or other payment webhooks: a signed event replayed twice must not grant twice; an out-of-order event must not undo a newer state ([Stripe webhooks](https://docs.stripe.com/webhooks)).
- Supabase: check row-level security from a second user's session, not only the owner's, and that a service key never appears in client code ([Supabase RLS](https://supabase.com/docs/guides/database/postgres/row-level-security)).
