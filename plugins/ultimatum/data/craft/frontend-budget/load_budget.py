#!/usr/bin/env python3
"""Measure what loading a skill costs, and check a phase plan against a load budget.

    load_budget.py size PATH... [--skill-limit N] [--agent-limit N] [--ratio R] [--json]
    load_budget.py plan PLAN.json [--root DIR] [--phase-budget N] [--max-support N] [--json]
    load_budget.py --self-check

Token counts are estimates: characters divided by --ratio (default 4), rounded
up. They are good enough to compare files and spot growth; quote them as
estimates. Standard library only, no network.

Exit codes: 0 within budget, 1 over budget or plan broken, 2 bad usage.
"""
from __future__ import annotations

import math
import sys
import tempfile
from argparse import ArgumentParser, Namespace
from json import dumps, loads
from pathlib import Path

WITHIN, OVER, USAGE = 0, 1, 2
DEFAULT_RATIO = 4.0
LIMIT_DEFAULTS = {"skill": 8000, "agent": 20000, "reference": 6000}
ENTRY_NAMES = ("SKILL.md", "index.md")


def estimate(text: str, ratio: float) -> int:
    return math.ceil(len(text) / ratio) if text else 0


def kind_of(path: Path) -> str:
    if path.name == "SKILL.md":
        return "skill"
    if path.parent.name == "agents":
        return "agent"
    return "reference"


def collect(target: Path) -> list[Path]:
    """A file stands for itself; a folder means its skills and agents."""
    if target.is_file():
        return [target]
    found = sorted(target.glob("skills/*/SKILL.md")) + sorted(target.glob("agents/*.md"))
    if not found:
        found = [target / n for n in ENTRY_NAMES if (target / n).is_file()]
    return found


def size_report(targets: list[Path], limits: dict[str, int], ratio: float) -> list[dict]:
    rows = []
    for target in targets:
        for path in collect(target):
            text = path.read_text(encoding="utf-8", errors="replace")
            kind = kind_of(path)
            tokens = estimate(text, ratio)
            rows.append({"path": str(path), "kind": kind, "bytes": len(text.encode()),
                         "tokens_est": tokens, "limit": limits[kind],
                         "over": tokens > limits[kind]})
    return rows


def resolve(name: str, table: dict[str, str], root: Path | None) -> Path | None:
    """Map a skill name to the file that loads when it fires. Never guess."""
    raw = table.get(name)
    if raw is None and root is None:
        return None
    candidate = (root or Path(".")) / (raw if raw is not None else name)
    if candidate.is_dir():
        for entry in ENTRY_NAMES:
            if (candidate / entry).is_file():
                return candidate / entry
        return None
    return candidate if candidate.is_file() else None


def check_plan(plan: dict, root: Path | None, budget: int | None,
               max_support: int, ratio: float) -> tuple[list[str], list[dict]]:
    problems: list[str] = []
    phases_out: list[dict] = []
    base = list(plan.get("base", []))
    table = dict(plan.get("skills", {}))
    groups = [set(g) for g in plan.get("exclusive", [])]
    presets = set(plan.get("presets", []))
    phases = plan.get("phases")
    if not isinstance(phases, list) or not phases:
        return ["plan has no phases"], []
    for number, phase in enumerate(phases, 1):
        label = phase.get("name") or f"phase {number}"
        lead = phase.get("lead")
        support = list(phase.get("support", []))
        if not isinstance(lead, str) or not lead:
            problems.append(f"{label}: needs exactly one lead (a single name)")
            lead = ""
        if len(support) > max_support:
            problems.append(f"{label}: {len(support)} supporting skills, at most {max_support}")
        if lead and lead in support:
            problems.append(f"{label}: {lead} is both lead and support")
        named = ([lead] if lead else []) + support
        if len(set(named)) != len(named):
            problems.append(f"{label}: a skill is named twice")
        for group in groups:
            clash = sorted(group.intersection(named))
            if len(clash) > 1:
                problems.append(f"{label}: {' and '.join(clash)} never load together")
        stacked = sorted(presets.intersection(named))
        if len(stacked) > 1:
            problems.append(f"{label}: presets do not stack ({', '.join(stacked)})")
        tokens = 0
        resolved = root is not None or bool(table)
        for name in base + named:
            if not resolved:
                break
            path = resolve(name, table, root)
            if path is None:
                problems.append(f"{label}: cannot find {name}; leave it out rather than guess")
                continue
            tokens += estimate(path.read_text(encoding="utf-8", errors="replace"), ratio)
        if resolved and budget is not None and tokens > budget:
            problems.append(f"{label}: about {tokens} tokens, budget {budget}")
        phases_out.append({"phase": label, "base": base, "lead": lead, "support": support,
                           "tokens_est": tokens if resolved else None})
    return problems, phases_out


def load_line(row: dict) -> str:
    parts = []
    if row["base"]:
        parts.append("base " + ", ".join(row["base"]))
    parts.append("lead " + (row["lead"] or "?"))
    if row["support"]:
        parts.append("support " + ", ".join(row["support"]))
    cost = "" if row["tokens_est"] is None else f" (~{row['tokens_est']} tokens)"
    return f"{row['phase']} loads: " + "; ".join(parts) + cost


def emit(payload: object) -> None:
    sys.stdout.write(dumps(payload, indent=2) + "\n")


def run_size(args: Namespace) -> int:
    limits = dict(LIMIT_DEFAULTS, skill=args.skill_limit, agent=args.agent_limit,
                  reference=args.reference_limit)
    targets = [Path(p) for p in args.paths]
    missing = [str(t) for t in targets if not t.exists()]
    if missing:
        print("load_budget: no such path: " + ", ".join(missing), file=sys.stderr)
        return USAGE
    rows = size_report(targets, limits, args.ratio)
    if args.json:
        emit(rows)
    else:
        for r in rows:
            mark = "OVER" if r["over"] else "ok"
            print(f"{mark:4} {r['tokens_est']:6} / {r['limit']:<6} {r['kind']:9} {r['path']}")
        print(f"{len(rows)} file(s), {sum(r['over'] for r in rows)} over, "
              f"~{sum(r['tokens_est'] for r in rows)} tokens in all (estimate)")
    return OVER if any(r["over"] for r in rows) else WITHIN


def run_plan(args: Namespace) -> int:
    try:
        plan = loads(Path(args.plan).read_text(encoding="utf-8"))
    except (ValueError, OSError) as err:
        print(f"load_budget: cannot read plan: {err}", file=sys.stderr)
        return USAGE
    if not isinstance(plan, dict):
        print("load_budget: plan must be a JSON object", file=sys.stderr)
        return USAGE
    root = Path(args.root) if args.root else None
    problems, rows = check_plan(plan, root, args.phase_budget, args.max_support, args.ratio)
    if args.json:
        emit({"phases": rows, "problems": problems})
    else:
        for row in rows:
            print(load_line(row))
        for p in problems:
            print("problem: " + p)
    return OVER if problems else WITHIN


def self_check() -> int:
    failures = []

    def expect(cond: bool, what: str) -> None:
        if not cond:
            failures.append(what)

    expect(estimate("abcd" * 10, 4.0) == 10, "estimate divides by ratio")
    expect(estimate("abcde", 4.0) == 2, "estimate rounds up")
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp)
        (home / "skills" / "small").mkdir(parents=True)
        (home / "skills" / "small" / "SKILL.md").write_text("x" * 400)
        (home / "skills" / "big").mkdir(parents=True)
        (home / "skills" / "big" / "SKILL.md").write_text("y" * 40000)
        (home / "agents").mkdir()
        (home / "agents" / "helper.md").write_text("z" * 80)
        (home / "pack").mkdir()
        (home / "pack" / "index.md").write_text("w" * 800)
        rows = size_report([home], dict(LIMIT_DEFAULTS), DEFAULT_RATIO)
        over = [Path(r["path"]).parent.name for r in rows if r["over"]]
        expect(len(rows) == 3, "plugin folder yields skills and agents")
        expect(over == ["big"], "only the 10000-token skill is over 8000")
        good = {"base": ["skills/small"], "exclusive": [["pack", "skills/big"]],
                "phases": [{"name": "Direction", "lead": "pack", "support": ["agents/helper.md"]}]}
        problems, out = check_plan(good, home, 1000, 2, DEFAULT_RATIO)
        expect(problems == [], f"good plan passes, got {problems}")
        expect(out and out[0]["tokens_est"] == 100 + 200 + 20, "phase cost sums base, lead, support")
        expect(load_line(out[0]).startswith("Direction loads: base skills/small; lead pack"),
               "load line names the base first")
        bad = {"presets": ["p1", "p2"], "exclusive": [["pack", "skills/big"]],
               "phases": [{"name": "Build", "lead": "pack",
                           "support": ["skills/big", "p1", "p2"]},
                          {"name": "Review", "support": ["ghost"]}]}
        problems, _ = check_plan(bad, home, 5000, 2, DEFAULT_RATIO)
        text = "\n".join(problems)
        for needle in ("3 supporting skills", "never load together", "presets do not stack",
                       "about 10200 tokens", "needs exactly one lead", "cannot find ghost"):
            expect(needle in text, f"bad plan reports: {needle}")
        expect(check_plan({"phases": []}, None, None, 2, DEFAULT_RATIO)[0] == ["plan has no phases"],
               "empty plan is refused")
        unresolved = check_plan({"phases": [{"lead": "a"}]}, None, 10, 2, DEFAULT_RATIO)
        expect(unresolved[0] == [] and unresolved[1][0]["tokens_est"] is None,
               "without a root or table, counts are skipped, not guessed")
    for f in failures:
        print("self-check FAIL: " + f)
    print("self-check ok" if not failures else f"self-check: {len(failures)} failure(s)")
    return WITHIN if not failures else OVER


def main(argv: list[str] | None = None) -> int:
    parser = ArgumentParser(prog="load_budget.py", description=__doc__.splitlines()[0])
    parser.add_argument("--self-check", action="store_true")
    sub = parser.add_subparsers(dest="cmd")
    size = sub.add_parser("size", help="estimate tokens per skill, agent or reference file")
    size.add_argument("paths", nargs="+")
    size.add_argument("--skill-limit", type=int, default=LIMIT_DEFAULTS["skill"])
    size.add_argument("--agent-limit", type=int, default=LIMIT_DEFAULTS["agent"])
    size.add_argument("--reference-limit", type=int, default=LIMIT_DEFAULTS["reference"])
    size.add_argument("--ratio", type=float, default=DEFAULT_RATIO)
    size.add_argument("--json", action="store_true")
    plan = sub.add_parser("plan", help="check a phase plan: one lead, few supports, no clashes")
    plan.add_argument("plan")
    plan.add_argument("--root")
    plan.add_argument("--phase-budget", type=int)
    plan.add_argument("--max-support", type=int, default=2)
    plan.add_argument("--ratio", type=float, default=DEFAULT_RATIO)
    plan.add_argument("--json", action="store_true")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return USAGE if exc.code else WITHIN
    if args.self_check:
        return self_check()
    if getattr(args, "ratio", DEFAULT_RATIO) <= 0:
        print("load_budget: --ratio must be positive", file=sys.stderr)
        return USAGE
    if args.cmd == "size":
        return run_size(args)
    if args.cmd == "plan":
        return run_plan(args)
    parser.print_usage(sys.stderr)
    return USAGE


if __name__ == "__main__":
    sys.exit(main())
