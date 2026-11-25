# Held-out live A/B, 2026-11-24

Six new held-out cases (h1–h6). Graders check outcomes only. Arms: vanilla and v2 (after the second optimization pass). Sonnet, 3 trials per case and arm, 36 runs, $2.36 against an $8 cap. Command: `run_live.py --cases h1..h6 --arms vanilla,v2 --trials 3 --budget 0.6 --max-total-usd 8`.

Caveats:
- All three vanilla failures are the h3 check `feature_tested` (no test was added for the new method). The prompt did not ask for a test. Without that check, both arms pass 18/18 and v2 costs about 11% more per run ($0.069 vs $0.062).
- These tasks are smaller than the first benchmark, so their dollar figures are not comparable with the $0.151 and $0.120 targets.

## Per case

| Case | Arm | Runs | Outcome pass | Process pass | Failed checks (all runs) | Mean cost $ | Mean turns | Subagents | Mean out tok | Mean cache-read tok |
|---|---|---|---|---|---|---|---|---|---|---|
| h1-symptom | vanilla | 3 | 3/3 | 3/3 | — | 0.066 | 8.7 | 0.0 | 1499 | 138691 |
| h1-symptom | v2 | 3 | 3/3 | 3/3 | — | 0.063 | 4.7 | 0.0 | 1103 | 169867 |
| h2-noisy-fail | vanilla | 3 | 3/3 | 3/3 | — | 0.065 | 6.0 | 0.0 | 970 | 212027 |
| h2-noisy-fail | v2 | 3 | 3/3 | 3/3 | — | 0.072 | 6.0 | 0.0 | 846 | 224831 |
| h3-reuse-helper | vanilla | 3 | 0/3 | 3/3 | feature_tested | 0.052 | 5.3 | 0.0 | 847 | 138077 |
| h3-reuse-helper | v2 | 3 | 3/3 | 3/3 | — | 0.057 | 4.0 | 0.0 | 909 | 144747 |
| h4-serve-file | vanilla | 3 | 3/3 | 3/3 | — | 0.077 | 4.3 | 0.0 | 2371 | 151407 |
| h4-serve-file | v2 | 3 | 3/3 | 3/3 | — | 0.090 | 4.0 | 0.0 | 2452 | 147646 |
| h5-review | vanilla | 3 | 3/3 | 3/3 | — | 0.055 | 3.0 | 0.0 | 1416 | 100965 |
| h5-review | v2 | 3 | 3/3 | 3/3 | — | 0.072 | 4.0 | 0.0 | 1945 | 119138 |
| h6-dedupe | vanilla | 3 | 3/3 | 3/3 | — | 0.059 | 6.3 | 0.0 | 1349 | 138635 |
| h6-dedupe | v2 | 3 | 3/3 | 3/3 | — | 0.061 | 4.0 | 0.0 | 1174 | 145474 |

## Per arm

Passing = graders pass and no new blocking architecture finding (cycle, placeholder).

| Arm | Runs | Passing | Pass rate | Outcome-only pass | Invalid | New arch findings | Total tokens | Mean tokens | Total cost $ | Cost/run $ | Cost/passing task $ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| vanilla | 18 | 15 | 83% | 15/18 (83%) | 0 | 0 (18/18 measured) | 2,815,269 | 156,404 | 1.12 | 0.062 | 0.075 |
| v2 | 18 | 18 | 100% | 18/18 (100%) | 0 | 0 (18/18 measured) | 3,056,093 | 169,783 | 1.24 | 0.069 | 0.069 |

## Per-case cost ratios (mean cost per run; >1 means more expensive)

| Case | vanilla $ | v041 $ | v2 $ | v041/vanilla | v2/vanilla | v2/v041 |
|---|---|---|---|---|---|---|
| h1-symptom | 0.066 | — | 0.063 | n/a | 0.96x | n/a |
| h2-noisy-fail | 0.065 | — | 0.072 | n/a | 1.11x | n/a |
| h3-reuse-helper | 0.052 | — | 0.057 | n/a | 1.10x | n/a |
| h4-serve-file | 0.077 | — | 0.090 | n/a | 1.17x | n/a |
| h5-review | 0.055 | — | 0.072 | n/a | 1.31x | n/a |
| h6-dedupe | 0.059 | — | 0.061 | n/a | 1.03x | n/a |

Total spend across these runs: $2.36; skipped by the budget cap: 0
