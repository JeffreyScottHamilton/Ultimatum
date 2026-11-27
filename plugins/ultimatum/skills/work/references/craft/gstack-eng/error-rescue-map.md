# Error and rescue map

Read when a plan or diff adds network calls, background jobs, model calls, payments or multi-step writes, and you need to show that every failure has a handler and a visible result.

## 1. The table

One row per thing that can fail. Fill it from the code or plan, not from memory.

| Call site | What fails | Error raised | Caught where | Then | User sees | Test |
|---|---|---|---|---|---|---|
| `PaymentClient.charge` | gateway timeout | `TimeoutError` | `Checkout.submit` | retry once, then mark pending | "Payment pending, we'll email you" | `test_charge_timeout` |
| `PaymentClient.charge` | card declined | `CardDeclined` | `Checkout.submit` | stop | the decline reason | `test_declined` |

Rules for filling it:
- No catch-all that swallows. A broad `except` must log the context (ids, inputs that are safe to log) and re-raise or return a typed failure.
- Each handler does one of three things: retry with a limit, fall back to a degraded result, or re-raise. Say which.
- "User sees" is never blank. A silent failure is the worst row.
- A row with no test, no handler and no signal is a critical gap.
- Model calls get three rows of their own: malformed output, empty output, and a refusal. Validate shape before use.

## 2. Shadow paths of each input

Trace each input through its stages and ask what happens at each when the value is missing, empty, invalid, slow, in conflict with another write, or stale:

```text
input -> validate -> transform -> store -> output
```

Write only the cases that the code does not already handle, with the stage where they should be caught.

## 3. Order of async work

When two async steps can finish in either order (a webhook and a redirect, two parallel fetches), write both orders and the expected end state for each. Test both: pause one step with a controllable fake or a latch, release the other, then release the first. Wait on a condition, never a fixed sleep.

## 4. Logs and signals

For each row, name the log line or metric that would show the failure in production. If a bug from three weeks ago could not be rebuilt from those, add what is missing to the plan.
