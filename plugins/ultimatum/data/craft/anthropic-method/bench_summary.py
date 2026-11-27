#!/usr/bin/env python3
"""Summarise graded eval runs per arm and flag assertions that tell the arms apart badly.

Layout read (see eval-workspace.md):  ROOT/<case>/<arm>/run-<n>/grading.json
grading.json: {"expectations": [{"text": str, "passed": bool, "evidence": str}],
               "timing": {"seconds": float, "tokens": int}}   # timing optional

Usage: bench_summary.py ROOT [--json]      bench_summary.py --self-check
Exit: 0 printed, 1 no runs found, 2 bad usage.
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

OK = 0


def _stats(xs: list[float]) -> dict:
    if not xs:
        return {"n": 0, "mean": None, "stdev": None}
    return {"n": len(xs), "mean": round(statistics.fmean(xs), 3),
            "stdev": round(statistics.stdev(xs), 3) if len(xs) > 1 else 0.0}


def collect(root: Path) -> dict:
    arms: dict[str, dict[str, list]] = defaultdict(lambda: {"rate": [], "seconds": [], "tokens": []})
    per_assert: dict[tuple[str, str], dict[str, list[bool]]] = defaultdict(lambda: defaultdict(list))
    bad: list[str] = []
    for g in sorted(root.glob("*/*/run-*/grading.json")):
        case, arm = g.parts[-4], g.parts[-3]
        try:
            data = json.loads(g.read_text(encoding="utf-8"))
            exps = data["expectations"]
            passed = [bool(e["passed"]) for e in exps]
        except (ValueError, KeyError, TypeError) as exc:
            bad.append(f"{g.relative_to(root)}: {exc.__class__.__name__}")
            continue
        if not exps:
            bad.append(f"{g.relative_to(root)}: no expectations")
            continue
        if any(e["passed"] and not str(e.get("evidence", "")).strip() for e in exps):
            bad.append(f"{g.relative_to(root)}: a pass with no evidence")
        arms[arm]["rate"].append(sum(passed) / len(passed))
        timing = data.get("timing") or {}
        for k in ("seconds", "tokens"):
            if isinstance(timing.get(k), (int, float)):
                arms[arm][k].append(float(timing[k]))
        for e in exps:
            per_assert[(case, e["text"])][arm].append(bool(e["passed"]))
    flags = []
    names = sorted(arms)
    for (case, text), by_arm in sorted(per_assert.items()):
        rates = {a: sum(v) / len(v) for a, v in by_arm.items() if v}
        if len(rates) == len(names) and len(names) > 1:
            if all(r == 1.0 for r in rates.values()):
                flags.append({"case": case, "assertion": text, "flag": "passes in every arm: does not discriminate"})
            elif all(r == 0.0 for r in rates.values()):
                flags.append({"case": case, "assertion": text, "flag": "fails in every arm: check the assertion or the task"})
        for a, r in rates.items():
            if 0.0 < r < 1.0 and len(by_arm[a]) >= 3:
                flags.append({"case": case, "assertion": text, "flag": f"flaky in {a} ({r:.0%} of {len(by_arm[a])} runs)"})
    return {"arms": {a: {k: _stats(v) for k, v in arms[a].items()} for a in names},
            "flags": flags, "unreadable": bad}


def render(rep: dict) -> str:
    out = ["arm            pass rate (mean ± sd, n)   seconds    tokens"]
    for arm, s in rep["arms"].items():
        r, t, k = s["rate"], s["seconds"], s["tokens"]
        out.append(f"{arm:<14} {r['mean']:.2f} ± {r['stdev']:.2f} (n={r['n']})"
                   f"{'':>8}{t['mean'] if t['n'] else '-':>8}  {k['mean'] if k['n'] else '-':>8}")
    for f in rep["flags"]:
        out.append(f"flag: {f['case']} / {f['assertion']}: {f['flag']}")
    for b in rep["unreadable"]:
        out.append(f"check: {b}")
    return "\n".join(out)


def _write(root: Path, case: str, arm: str, n: int, results: list[bool], secs: float) -> None:
    d = root / case / arm / f"run-{n}"
    d.mkdir(parents=True)
    exps = [{"text": f"a{i}", "passed": p, "evidence": "line 3 of out.txt" if p else ""} for i, p in enumerate(results)]
    (d / "grading.json").write_text(json.dumps({"expectations": exps, "timing": {"seconds": secs, "tokens": 1000}}))


def self_check() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for n in range(1, 4):
            _write(root, "csv", "with_skill", n, [True, True, n != 2], 30.0 + n)
            _write(root, "csv", "without_skill", n, [True, False, False], 20.0)
        rep = collect(root)
        assert rep["arms"]["with_skill"]["rate"]["n"] == 3
        assert rep["arms"]["without_skill"]["rate"]["mean"] == 0.333, rep
        kinds = sorted(f["flag"].split(":")[0].split(" (")[0] for f in rep["flags"])
        assert kinds == ["flaky in with_skill", "passes in every arm"], kinds
        assert not rep["unreadable"], rep
    print("self-check passed: 6 runs, 2 flags")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("root", nargs="?", type=Path)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args(argv)
    if args.self_check:
        return self_check()
    if not args.root or not args.root.is_dir():
        parser.print_usage(sys.stderr)
        return 2
    rep = collect(args.root)
    if not rep["arms"]:
        print("no runs found under " + str(args.root), file=sys.stderr)
        return 1
    print(json.dumps(rep, indent=2) if args.json else render(rep))
    return OK


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
