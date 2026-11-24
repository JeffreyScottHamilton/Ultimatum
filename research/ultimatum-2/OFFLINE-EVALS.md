# Ultimatum 2.0 offline evaluation (2026-11-24)

These numbers come only from local commands run in this session. No live model calls were made, so cost, tokens per task and pass rate against vanilla and 0.4.1 are **not measured yet** (see "Live A/B" below).

## Static context cost (always loaded or re-read each turn)

| Item | 0.4.1 | 2.0 |
|---|---|---|
| `work` SKILL.md body (re-read every turn once invoked) | 7,081 B (~1,770 tokens) | 3,996 B (~999 tokens) |
| `work` SKILL.md file | 7.6 KB | 4.5 KB |
| Listed skill descriptions (startup) | 432 B | 454 B |
| Agent descriptions (startup) | 1,133 B | 1,138 B |
| Management skills (startup) | n/a | 0 B (`disable-model-invocation`) |
| Stop hook output | n/a | 0 B (observe prints nothing) |

The body is 44% smaller. References load only when `ult route` lists them. For example, `fix the login redirect bug` lists `debugging.md` (~1.9k tokens) plus the security overlay.

`tests/test_sizes.py` enforces these budgets: body at most 4 KB, management skills at most 1.5 KB, and agent descriptions at most 400 chars.

## Router accuracy (`ult route --eval`)

| Set | Cases | Route | Overlay | Add-ons | Independence |
|---|---|---|---|---|---|
| dev | 192 | 0.984 | 1.000 | 0.995 | Tuned against |
| holdout | 80 | 0.963 | 0.963 | 0.875 | Contaminated (categories tuned) |
| holdout2 | 60 | 0.967 | 0.967 | 0.950 | Contaminated (failure categories tuned) |
| **holdout3** | **60** | **0.767** | **0.933** | **0.950** | **Fresh: written by an independent agent, not tuned against** |

holdout3 is the honest generalization estimate. It is below the 95% target. Its misses include:
- bug reports phrased as symptoms going to feature;
- "full security sweep" going to sec-review instead of sec-audit;
- "pentest report … fix it" going to sec-audit;
- "create a subagent … migrations" going to data-infra;
- skill-eval phrasing such as "score the plugin's holdout set".

Mitigation in the design: SKILL.md tells the model that routing is advice. The model overrides it when the task says otherwise, and picks from the `alt:` line when the top two routes are close. A wrong route costs at most one extra reference read. It never blocks work.

Convention: overlay is false for discover and sec-* routes, because they already include the security work. holdout3 follows this. The first holdout labels sec-fix overlay as true, which accounts for 3 of its overlay misses.

## Tests and validation

- `python3 -m unittest discover -s plugins/ultimatum/tests`: 311 tests, OK.
- `claude plugin validate . --strict`: passed.
- `claude plugin validate plugins/ultimatum --strict`: passed.

## Live A/B (not run; needs approval, budget cap $15)

```bash
python3 evals/live/run_live.py --arms vanilla,v041,v2 --max-total-usd 15
```

It measures total tokens, cost, and cost per passing task for each arm. Until it runs, no claim is made that 2.0 is cheaper than vanilla or 0.4.1 per task.
