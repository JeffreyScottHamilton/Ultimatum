# Bounded optimization loop

Goal: improve one measurable number (latency, size, cost, tokens, flakiness) through small, reversible experiments, with an independent correctness guard and an honest result. Not for open-ended refactors. General loop: SKILL.md §3.

## 1. Setup (all before iteration 1)

1. **Pin the goal verbatim.** Write one line: `Goal: <metric> <direction> <target or "as far as possible within N iterations">`. Reuse this exact string in every iteration report and on resume; do not reword it. Example: `Goal: p95 of bench/parse.sh decreases >= 15% vs baseline`.
2. **Success predicate.** A comparison that returns yes/no (`new_median < 0.85 * baseline_median`), and the noise margin below which differences are ignored.
3. **Metric command.** One command that prints one number. Run it through `ult run --name metric -- <cmd>` once as a dry run; it must produce a number, not an error. Define units and what lower/higher means.
4. **Guard command.** An independent correctness check that must always pass: the test suite, a golden-output diff, a differential oracle against the old implementation, a type check. Prove it can reject: apply a known-bad change (or flip one expected value), see the guard fail, restore. A guard chosen only because it is easy to keep green is replaced.
5. **Scope.** List the files the loop may edit. Everything else is off limits.
6. **Cap.** Default 10 iterations (or what the user sets); a hard ceiling is checked first each cycle. Unlimited only if the user says so.
7. **Safety.** Git repo; commit or stash unrelated work so the tree is clean; work on a branch. Screen the metric/guard commands for destructive patterns before running. Never push, publish, or deploy from inside the loop.
8. **Baseline.** Run the metric N times (default 5; 10+ if noisy) on the unmodified code in the same conditions; record each value, median, and spread (min/max or stdev). Record machine and load conditions. Run the guard once: it must be green. If the baseline spread is larger than the target gain, fix measurement first (more runs, isolate noise, bigger input) or stop.
9. **Ledger.** Create `.ultimatum/opt/<name>.tsv`; first row is the baseline (iteration 0).

TSV columns: `iter  time  commit  metric_median  delta_vs_best  guard  status  description`, tab-separated. Status vocabulary: `keep`, `discard`, `guard-fail`, `crash`, `metric-error`, `no-op`, `blocked`.

## 2. Iteration (repeat)

1. Read the last ledger rows and `git log --oneline -n 10` so you do not repeat a discarded idea. Pick the single most promising hypothesis (profile first when you have no hypothesis; guessing is the lowest-yield path).
2. Make **one atomic change**: one idea, one reason. Commit it with a message naming the hypothesis.
3. Run the guard first (cheap). Fail: revert, record `guard-fail`, next.
4. Run the metric N times. Compare the median to the **best so far** using the pinned predicate and the noise margin.
   - Better beyond noise and guard green: `keep`; it becomes the new best.
   - Otherwise: `discard`; `git revert`/`git reset --hard <best>` back to the best commit.
   - Build/runtime error: `crash` and revert; metric not a number: `metric-error` and revert; change had no effect: `no-op`.
5. **A failing guard reverts even if the metric improved.** No exceptions, no "fix the test".
6. Append the TSV row. Tag the best commit (`git tag ult-opt-<name>-best` locally) so no branch can lose it.
7. Check stop conditions (§3) before the next iteration.

## 3. Stop conditions

Stop and report on the first that holds:
- Success predicate met and confirmed (§4).
- Iteration cap reached.
- **Plateau:** no `keep` in the last 5 counted iterations. Iterations whose measurement failed are not counted as zero progress; repeated measurement failures mean `blocked`.
- Guard cannot be made meaningful, or the metric is unmeasurable.
- Three consecutive crashes or guard failures: question the approach (see `debugging.md` §5) or ask.
- The user interrupts.
At plateau, try one reset before giving up: restart a fresh pass from the ledger and best commit (not from chat memory), choose structurally different ideas (algorithm or data structure, not micro-tweaks), cap at 3 more iterations.

## 4. Acceptance is separate from search

The search metric ranks candidates; it must not also certify the result.
1. On the final best commit, rerun the metric on a **held-out** input (different data or sizes than the loop used) and an adversarial one (empty, huge, skewed).
2. Time in fresh, independent processes, not one warm process; include end-to-end and tail (p95/p99) cost where relevant, and cold start if it matters.
3. Run the full test suite and the type/lint checks (`ult run`), not only the guard. Quote count of tests run.
4. Check for overfitting: special-casing the benchmark input, caching keyed to the test, removing work the benchmark does not exercise.
5. Confirm promising gains as isolated, reviewable changes: if several kept commits combine, show that each helps alone or note the interaction.
6. Keep a rollback point (the baseline commit sha).

## 5. Metric hygiene

- Same machine, same inputs, same flags between baseline and candidate; warm up if the system caches; discard the first run only if you did so for the baseline too.
- Deterministic where possible (fixed seed, fixed data). For costs and token counts, use counted values from the tool, not estimates.
- Do not widen noise margins after seeing results.
- A metric that can be gamed (lines of code, test count, coverage alone) needs a guard that blocks the gaming.

## 6. Report

Lead with the result and the verbatim goal. Then:
- Baseline: median and spread over N runs; final: median and spread over N runs; delta and whether it exceeds noise.
- Table of kept iterations (commit, change, delta); count of discarded / guard-fail / crash.
- Held-out and adversarial measurements; full-suite result.
- What was not measured (other hardware, production load).
- Ledger path `.ultimatum/opt/<name>.tsv`, branch, and best-commit sha. Nothing pushed.
Do not state a gain without the baseline numbers and the variance beside it.

## 7. Choosing hypotheses

- Profile or trace before iteration 1 and list the top three costs; spend iterations in that order.
- Prefer changes that remove work (skip, batch, cache with correct invalidation, better algorithm) over changes that merely shift it.
- Keep each change small enough to attribute the delta to one cause; if two ideas are coupled, try them as separate iterations first.
- Record rejected ideas in the TSV description so a restart does not retry them.
- If a gain looks too good, suspect the measurement: rerun the baseline and the best commit back to back.

## 8. Example ledger

```
iter	time	commit	metric_median	delta_vs_best	guard	status	description
0	10:02	a1b2c3d	412.0	0	pass	keep	baseline (5 runs, spread 408-419)
1	10:09	b2c3d4e	371.0	-41.0	pass	keep	reuse parsed regex across calls
2	10:16	c3d4e5f	369.5	-1.5	pass	discard	within noise margin (5.0)
3	10:23	d4e5f6a	330.0	-41.0	fail	guard-fail	skip validation; output differs on empty input
```
