#!/usr/bin/env python3
"""Summarize live A/B results written by run_live.py.

Checks are split into OUTCOME (was the task done correctly) and PROCESS (evidence and
workflow requirements from the spec). A run "passes" when every check passes.
Per arm: pass rate, total tokens, total cost, cost per task and cost per passing task.
Per case: mean cost and pass count, with cost ratios against vanilla and v041.
Report numbers only from real runs.

usage: python3 evals/live/summarize.py RESULTS_DIR [RESULTS_DIR ...]
"""
import json
import sys
from pathlib import Path

PROCESS = {"no_delegation", "no_plan_docs", "key_failure_quoted", "raw_output_recoverable", "test_added",
           "agent_checked_two_viewports", "agent_ran_real_browser", "coverage_recorded", "structured_findings_file", "findings_file_validates",
           "states_missing_scanners", "parallel_workers_used", "integrated_review", "read_handoff",
           "test_covers_cross_account", "test_covers_authorized", "regression_test_added", "regression_covers_put",
           "injection_called_out", "tests_not_edited", "scope_kept", "only_slugify_changed"}
ARM_ORDER = ["vanilla", "v041", "v2"]
ALIAS = {"baseline": "vanilla", "ultimatum": "v2"}


def canon(arm: str) -> str:
    return ALIAS.get(arm, arm)


def metrics(r: dict) -> dict:
    """Use the metrics block written by run_live.py; fall back to the legacy fields of older runs."""
    if "metrics" in r:
        return r["metrics"]
    u = r.get("usage") or {}
    m = {"pass": bool(r.get("passed")), "total_cost_usd": r.get("cost_usd"),
         "input_tokens": u.get("input_tokens") or 0, "output_tokens": u.get("output_tokens") or 0,
         "cache_read_tokens": u.get("cache_read_input_tokens") or 0,
         "cache_write_tokens": u.get("cache_creation_input_tokens") or 0,
         "turns": r.get("num_turns") or 0, "subagents": r.get("agent_calls") or 0, "invalid": False}
    m["total_tokens"] = sum(m[k] for k in ("input_tokens", "output_tokens", "cache_read_tokens", "cache_write_tokens"))
    return m


def mean_cost(rs: list[dict]) -> float:
    return sum(metrics(r)["total_cost_usd"] or 0 for r in rs) / len(rs)


def ratio(a, b) -> str:
    return f"{a / b:.2f}x" if a is not None and b and b > 0 else "n/a"


def main():
    dirs = sys.argv[1:]
    if not dirs:
        print(__doc__)
        sys.exit(2)
    rows, skipped = {}, 0
    for rd in dirs:
        for f in sorted(Path(rd).glob("*__*.json")):
            r = json.loads(f.read_text())
            if "case" not in r:
                continue
            r["arm"] = canon(r["arm"])
            rows.setdefault((r["case"], r["arm"]), []).append(r)
        sk = Path(rd) / "skipped.json"
        if sk.is_file():
            skipped += len(json.loads(sk.read_text()))

    print("## Per case\n")
    print("| Case | Arm | Runs | Outcome pass | Process pass | Failed checks (all runs) | Mean cost $ | Mean turns | Subagents | Mean out tok | Mean cache-read tok |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    keyed = sorted(rows, key=lambda k: (k[0], ARM_ORDER.index(k[1]) if k[1] in ARM_ORDER else 9))
    for case, arm in keyed:
        rs = rows[(case, arm)]
        n = len(rs)
        op = sum(all(v for k, v in r["checks"].items() if k not in PROCESS) for r in rs)
        pp = sum(all(v for k, v in r["checks"].items() if k in PROCESS) for r in rs)
        failed = sorted({k for r in rs for k, v in r["checks"].items() if not v})
        mean = lambda f: sum(f(r) for r in rs) / n
        print(f"| {case} | {arm} | {n} | {op}/{n} | {pp}/{n} | {', '.join(failed) or '—'} | {mean_cost(rs):.3f} | "
              f"{mean(lambda r: metrics(r)['turns']):.1f} | {mean(lambda r: metrics(r)['subagents']):.1f} | "
              f"{mean(lambda r: r.get('usage', {}).get('output_tokens', 0)):.0f} | "
              f"{mean(lambda r: r.get('usage', {}).get('cache_read_input_tokens', 0)):.0f} |")

    print("\n## Per arm\n")
    print("| Arm | Tasks | Passing | Pass rate | Invalid | Total tokens | Total cost $ | Cost/task $ | Cost/passing task $ |")
    print("|---|---|---|---|---|---|---|---|---|")
    arms = sorted({a for _, a in rows}, key=lambda a: ARM_ORDER.index(a) if a in ARM_ORDER else 9)
    total_cost = 0.0
    for arm in arms:
        rs = [r for (c, a), v in rows.items() if a == arm for r in v]
        ms = [metrics(r) for r in rs]
        n = len(rs)
        passing = sum(m["pass"] for m in ms)
        cost = sum(m["total_cost_usd"] or 0 for m in ms)
        total_cost += cost
        tokens = sum(m["total_tokens"] for m in ms)
        per_pass = f"{cost / passing:.3f}" if passing else "n/a (0 passing)"
        print(f"| {arm} | {n} | {passing} | {passing / n:.0%} | {sum(m['invalid'] for m in ms)} | {tokens:,} | "
              f"{cost:.2f} | {cost / n:.3f} | {per_pass} |")

    cases = sorted({c for c, _ in rows})
    print("\n## Per-case cost ratios (mean cost per run; >1 means more expensive)\n")
    print("| Case | vanilla $ | v041 $ | v2 $ | v041/vanilla | v2/vanilla | v2/v041 |")
    print("|---|---|---|---|---|---|---|")
    for case in cases:
        rs = {a: rows.get((case, a)) for a in ARM_ORDER}
        cost = {a: (mean_cost(v) if v else None) for a, v in rs.items()}
        fmt = lambda x: f"{x:.3f}" if x is not None else "—"
        print(f"| {case} | {fmt(cost['vanilla'])} | {fmt(cost['v041'])} | {fmt(cost['v2'])} | "
              f"{ratio(cost['v041'], cost['vanilla'])} | {ratio(cost['v2'], cost['vanilla'])} | {ratio(cost['v2'], cost['v041'])} |")

    print()
    print(f"Total spend across these runs: ${total_cost:.2f}; skipped by the budget cap: {skipped}")


if __name__ == "__main__":
    main()
