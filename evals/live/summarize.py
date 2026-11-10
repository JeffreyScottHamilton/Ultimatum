#!/usr/bin/env python3
"""Summarize live A/B results. Splits checks into OUTCOME (did the task get done
correctly) and PROCESS (evidence/workflow requirements from the spec)."""
import json, sys
from pathlib import Path
PROCESS = {"no_delegation", "no_plan_docs", "key_failure_quoted", "raw_output_recoverable", "test_added",
           "agent_checked_two_viewports", "agent_ran_real_browser", "coverage_recorded", "structured_findings_file",
           "states_missing_scanners", "parallel_workers_used", "integrated_review", "read_handoff",
           "test_covers_cross_account", "test_covers_authorized", "regression_test_added", "regression_covers_put",
           "injection_called_out", "tests_not_edited", "scope_kept", "only_slugify_changed"}
rounds = sys.argv[1:]
rows = {}
for rd in rounds:
    for f in sorted(Path(rd).glob("*__*.json")):
        r = json.loads(f.read_text())
        rows.setdefault((r["case"], r["arm"]), []).append(r)
print("| Case | Arm | Runs | Outcome pass | Process pass | Failed checks (all runs) | Mean cost $ | Mean turns | Subagents | Mean out tok | Mean cache-read tok |")
print("|---|---|---|---|---|---|---|---|---|---|---|")
tot = {}
for (case, arm), rs in sorted(rows.items()):
    n = len(rs)
    op = sum(all(v for k, v in r["checks"].items() if k not in PROCESS) for r in rs)
    pp = sum(all(v for k, v in r["checks"].items() if k in PROCESS) for r in rs)
    failed = sorted({k for r in rs for k, v in r["checks"].items() if not v})
    mean = lambda f: sum(f(r) for r in rs) / n
    cost = mean(lambda r: r.get("cost_usd") or 0)
    t = tot.setdefault(arm, [0, 0, 0, 0]); t[0] += sum(r.get("cost_usd") or 0 for r in rs); t[1] += n; t[2] += op; t[3] += pp
    print(f"| {case} | {arm} | {n} | {op}/{n} | {pp}/{n} | {', '.join(failed) or '—'} | {cost:.3f} | {mean(lambda r: r.get('num_turns') or 0):.1f} | "
          f"{mean(lambda r: r.get('agent_calls') or 0):.1f} | {mean(lambda r: (r.get('usage') or {}).get('output_tokens', 0)):.0f} | "
          f"{mean(lambda r: (r.get('usage') or {}).get('cache_read_input_tokens', 0)):.0f} |")
print()
for arm, (c, n, op, pp) in tot.items():
    print(f"- **{arm}**: {n} runs, outcome pass {op}/{n}, process pass {pp}/{n}, total cost ${c:.2f}")
