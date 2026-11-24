# Ultimatum 2.0 offline evaluation (2026-11-24)

These numbers come only from local commands run in this session. No live model calls were made, so cost, tokens per task and pass rate against vanilla and 0.4.1 are **not measured yet** (see "Live A/B" below).

## Static context cost (always loaded or re-read each turn)

| Item | 0.4.1 | 2.0 |
|---|---|---|
| `work` SKILL.md body (re-read every turn once invoked) | 7,081 B (~1,770 tokens) | 4,029 B (~1,007 tokens) |
| `work` SKILL.md file | 7.6 KB | 4.5 KB |
| Listed skill descriptions (startup) | 432 B | 454 B |
| Agent descriptions (startup) | 1,133 B | 1,138 B |
| Management skills (startup) | n/a | 0 B (`disable-model-invocation`) |
| Stop hook output | n/a | 0 B (observe prints nothing) |

The body is 43% smaller. References load only when `ult route` lists them. For example, `fix the login redirect bug` lists `debugging.md` (~1.9k tokens) plus the security overlay.

`tests/test_sizes.py` enforces these budgets: body at most 4 KB, management skills at most 1.5 KB, and agent descriptions at most 400 chars.

## Router accuracy (`ult route --eval`)

| Set | Cases | Route | Overlay | Add-ons | Independence |
|---|---|---|---|---|---|
| dev | 192 | 0.984 | 1.000 | 0.995 | Tuned against |
| holdout | 80 | 0.963 | 0.963 | 0.863 | Contaminated (categories tuned) |
| holdout2 | 60 | 0.967 | 0.967 | 0.950 | Contaminated (failure categories tuned) |
| **holdout3** | **60** | **0.767** | **0.933** | **0.933** | **Fresh: written by an independent agent, not tuned against** |

holdout3 is the honest generalization estimate. It is below the 95% target. Its misses include:
- bug reports phrased as symptoms going to feature;
- "full security sweep" going to sec-review instead of sec-audit;
- "pentest report … fix it" going to sec-audit;
- "create a subagent … migrations" going to data-infra;
- skill-eval phrasing such as "score the plugin's holdout set".

Mitigation in the design: SKILL.md tells the model that routing is advice. The model overrides it when the task says otherwise, and picks from the `alt:` line when the top two routes are close. A wrong route costs at most one extra reference read. It never blocks work.

Convention: overlay is false for discover and sec-* routes, because they already include the security work. holdout3 follows this. The first holdout labels sec-fix overlay as true, which accounts for 3 of its overlay misses.

## Architecture Guardian (`ult arch`)

Measured on this repository:
- `ult arch check` (full repo, final tree) covers 45 Python files and 60 local import edges: no cycles, duplicate blocks or placeholders. It reports 5 oversized files (`scan.py` 782 lines, `evals/live/run_live.py` 685, `learn.py` 661, `findings.py` 573, `usage.py` 539) and 3 oversized functions (`route.py` `decide()`, `scan.py` `cmd_scan()`, `usage.py` `analyze_file()`). Typed share: 25%. Wall time 0.55 s. These files predate this change and were not refactored.
- The first draft of `arch.py` was 599 lines, over its own limit. It was split into `arch.py` (checks and CLI) and `archgraph.py` (graph and cycles) before commit.
- `ult arch check --changed` on the final diff: size 2, func-size 1, untested 1 (a lead for `run_live.py`), no cycles or placeholders.
- The eval quality gate was checked offline on a copied fixture with no model calls: a clean workspace has 0 new findings, and adding a `raise NotImplementedError` module gives 1 blocking finding, which makes `pass` false.

Router with the `architecture` add-on: the 17 cases whose expected route is `large` were relabelled to include it, which is the `with_routes` rule rather than keyword tuning. Add-ons: dev 0.995, holdout 0.863, holdout2 0.950, holdout3 0.933. One new add-on false positive is left untuned in holdout ("improve my existing code review skill"). Route and overlay scores are unchanged.

## Tests and validation

- `python3 -m unittest discover -s plugins/ultimatum/tests`: 335 tests, OK.
- `claude plugin validate . --strict`: passed.
- `claude plugin validate plugins/ultimatum --strict`: passed.

## Live A/B (run 2026-11-24; see `LIVE-AB-2026-11-24.md`)

One run per case: vanilla $0.151, 0.4.1 $0.193 and 2.0 $0.164 per passing task. Pass rates were 6/10, 6/10 and 7/10. Total spend was $3.21. With this sample size, these are not significant differences.

```bash
python3 evals/live/run_live.py --arms vanilla,v041,v2 --max-total-usd 15
```

It measures total tokens, cost, and cost per passing task for each arm.
