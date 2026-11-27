"""`ult approvals` — say what a merge-approval policy would decide for the current change.

    python3 approvals.py [--policy FILE] [--base REF] [--important N] [--json] [--root DIR]
    python3 approvals.py --check [--policy FILE]
    python3 approvals.py --starter

It only reports. It never approves, comments, merges or calls a network service: the
decision stays with people and the repository's branch rules. Guide:
skills/work/references/ship.md § Approval policy.

The policy is JSON (default `.claude/ultimatum-approvals.json`):

    {"version": 1, "rules": [
      {"purpose": "Docs can go on a clean review", "paths": ["**/*.md", "!SECURITY.md"],
       "verdict": "approve"},
      {"purpose": "Auth needs two people", "paths": ["src/auth/**"], "verdict": "people",
       "people": 2, "override": [{"if": "diff_lines < 5", "verdict": "people", "people": 1}]}]}

Verdicts, strictest first: block, people (N human reviews), comment, approve. `approve`
holds only when the review found no Important issues (pass --important N). A rule may
carry `if`, a condition over the facts below joined by AND / OR. `override` entries are
tried in order and the first whose `if` holds replaces the verdict.

Facts: files_changed, files_added, files_removed, diff_lines, rule_files, rule_lines,
risk and rule_risk (low < medium < high, from the file paths), author (true when any
commit author in the range matches the value, glob allowed), base (glob).

Exit 0 after a report, 1 when the policy is invalid, 2 on bad arguments or no git.
Standard library only, no network.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

DEFAULT_POLICY = ".claude/ultimatum-approvals.json"
VERDICTS = ["approve", "comment", "people", "block"]  # weakest to strictest
RISKS = ["low", "medium", "high"]
NUM_FACTS = {"files_changed", "files_added", "files_removed", "diff_lines", "rule_files", "rule_lines"}
STR_FACTS = {"risk", "rule_risk", "author", "base"}
RULE_KEYS = {"purpose", "paths", "verdict", "people", "if", "override"}

HIGH = re.compile(r"(^|/)(auth|oauth|sessions?|login|passwords?|secrets?|crypto|payments?|billing|"
                  r"permissions?|iam|acl|migrations?|terraform|infra|deploy)(/|[._-]|$)"
                  r"|(^|/)\.github/workflows/|(^|/)\.env|(^|/)Dockerfile$|\.pem$|\.key$"
                  r"|(^|/)(cors|csp|security)[._-]", re.I)
MEDIUM = re.compile(r"(^|/)(package\.json|requirements[^/]*\.txt|pyproject\.toml|go\.mod|Cargo\.toml|"
                    r"Gemfile|composer\.json|[^/]*\.lock|package-lock\.json|pnpm-lock\.yaml)$"
                    r"|(^|/)(api|db|schema|config|settings|server)(/|[._-])|\.sql$", re.I)
LOW_ONLY = re.compile(r"\.(md|mdx|txt|rst|png|jpe?g|svg|gif|webp)$|(^|/)docs?/", re.I)

STARTER = {
    "version": 1,
    "rules": [
        {"purpose": "Docs and images can go on a clean review",
         "paths": ["**/*.md", "**/*.mdx", "docs/**", "**/*.{png,jpg,svg}"], "verdict": "approve"},
        {"purpose": "Ordinary code needs one person",
         "paths": ["**", "!**/*.md", "!docs/**"], "verdict": "people", "people": 1,
         "override": [{"if": "rule_risk = low AND rule_lines <= 40", "verdict": "approve"}]},
        {"purpose": "Risky areas need two people",
         "paths": ["**"], "if": "rule_risk = high", "verdict": "people", "people": 2},
        {"purpose": "Very large changes are split first",
         "paths": ["**"], "if": "diff_lines > 2000", "verdict": "block"},
    ],
}


def glob_re(pattern: str) -> re.Pattern:
    """Translate a path glob: ** crosses folders, * and ? do not, {a,b} picks one."""
    out, i, n = [], 0, len(pattern)
    while i < n:
        c = pattern[i]
        if pattern.startswith("**/", i):
            out.append("(?:.*/)?"); i += 3; continue
        if pattern.startswith("**", i):
            out.append(".*"); i += 2; continue
        if c == "*":
            out.append("[^/]*")
        elif c == "?":
            out.append("[^/]")
        elif c == "{":
            j = pattern.find("}", i)
            if j < 0:
                out.append(re.escape(c))
            else:
                out.append("(?:" + "|".join(re.escape(p) for p in pattern[i + 1:j].split(",")) + ")")
                i = j
        elif c == "[":
            j = pattern.find("]", i)
            if j < 0:
                out.append(re.escape(c))
            else:
                out.append(pattern[i:j + 1]); i = j
        else:
            out.append(re.escape(c))
        i += 1
    return re.compile("^" + "".join(out) + "$")


def covers(paths: list[str], name: str) -> bool:
    keep = [p for p in paths if not p.startswith("!")]
    drop = [p[1:] for p in paths if p.startswith("!")]
    return any(glob_re(p).match(name) for p in keep) and not any(glob_re(p).match(name) for p in drop)


def file_risk(name: str) -> str:
    if HIGH.search(name):
        return "high"
    if MEDIUM.search(name):
        return "medium"
    return "low"


def max_risk(values) -> str:
    best = 0
    for v in values:
        best = max(best, RISKS.index(v))
    return RISKS[best]


CLAUSE = re.compile(r"^\s*([a-z_]+)\s*(<=|>=|!=|=|<|>)\s*(.+?)\s*$")


def _clauses(cond: str):
    for ors in re.split(r"\s+OR\s+", cond):
        yield [c for c in re.split(r"\s+AND\s+", ors)]


def check_condition(cond) -> list[str]:
    if isinstance(cond, bool):
        return []
    if not isinstance(cond, str) or not cond.strip():
        return ["`if` must be true, false or a condition string"]
    errs = []
    for group in _clauses(cond):
        for c in group:
            m = CLAUSE.match(c)
            if not m:
                errs.append(f"cannot read condition part {c!r}")
                continue
            fact, op, val = m.groups()
            if fact in NUM_FACTS:
                if not re.fullmatch(r"\d+", val):
                    errs.append(f"{fact} needs a whole number, got {val!r}")
            elif fact in ("risk", "rule_risk"):
                if val not in RISKS:
                    errs.append(f"{fact} is one of {', '.join(RISKS)}, got {val!r}")
            elif fact in ("author", "base"):
                if op not in ("=", "!="):
                    errs.append(f"{fact} takes = or != only")
            else:
                errs.append(f"unknown fact {fact!r}")
    return errs


def evaluate(cond, facts: dict) -> bool:
    if isinstance(cond, bool):
        return cond
    for group in _clauses(cond):
        if all(_one(c, facts) for c in group):
            return True
    return False


def _one(clause: str, facts: dict) -> bool:
    fact, op, val = CLAUSE.match(clause).groups()
    val = val.strip("\"'")
    if fact in ("author", "base"):
        pat = glob_re(val)
        have = facts["authors"] if fact == "author" else [facts["base"]]
        hit = any(pat.match(h) for h in have)
        return hit if op == "=" else not hit
    if fact in ("risk", "rule_risk"):
        a, b = RISKS.index(facts[fact]), RISKS.index(val)
    else:
        a, b = facts[fact], int(val)
    return {"=": a == b, "!=": a != b, "<": a < b, "<=": a <= b, ">": a > b, ">=": a >= b}[op]


def _check_verdict(where: str, item: dict) -> list[str]:
    v = item.get("verdict")
    if v not in VERDICTS:
        return [f"{where}: verdict must be one of {', '.join(VERDICTS)}"]
    if v == "people":
        p = item.get("people")
        if not isinstance(p, int) or isinstance(p, bool) or not 1 <= p <= 10:
            return [f"{where}: people needs a whole number from 1 to 10"]
    elif "people" in item:
        return [f"{where}: people only goes with verdict people"]
    return []


def validate(policy) -> list[str]:
    if not isinstance(policy, dict):
        return ["the policy must be a JSON object"]
    errs = []
    if policy.get("version") != 1:
        errs.append("version must be 1")
    extra = set(policy) - {"version", "rules"}
    if extra:
        errs.append(f"unknown top-level keys: {', '.join(sorted(extra))} (this checker only observes; there is no mode)")
    rules = policy.get("rules")
    if not isinstance(rules, list) or not rules:
        return errs + ["rules must be a non-empty list"]
    for i, r in enumerate(rules, 1):
        where = f"rule {i}"
        if not isinstance(r, dict):
            errs.append(f"{where}: must be an object"); continue
        bad = set(r) - RULE_KEYS
        if bad:
            errs.append(f"{where}: unknown keys {', '.join(sorted(bad))}")
        if not isinstance(r.get("purpose"), str) or not r["purpose"].strip():
            errs.append(f"{where}: purpose is required")
        paths = r.get("paths")
        if not isinstance(paths, list) or not all(isinstance(p, str) and p for p in paths):
            errs.append(f"{where}: paths must be a list of globs")
        elif not any(not p.startswith("!") for p in paths):
            errs.append(f"{where}: paths needs at least one pattern that is not an exclusion")
        errs += _check_verdict(where, r)
        if "if" in r:
            errs += [f"{where}: {e}" for e in check_condition(r["if"])]
        for j, o in enumerate(r.get("override", []) or [], 1):
            ow = f"{where} override {j}"
            if not isinstance(o, dict) or "if" not in o:
                errs.append(f"{ow}: needs if and verdict"); continue
            if set(o) - {"if", "verdict", "people"}:
                errs.append(f"{ow}: unknown keys")
            errs += [f"{ow}: {e}" for e in check_condition(o["if"])]
            errs += _check_verdict(ow, o)
    return errs


def _git(root: Path, *args) -> str:
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, check=True).stdout


def default_base(root: Path) -> str:
    for ref in ("origin/HEAD", "origin/main", "main", "origin/master", "master"):
        try:
            _git(root, "rev-parse", "--verify", "--quiet", ref)
            return ref
        except subprocess.CalledProcessError:
            continue
    raise RuntimeError("no base branch found; pass --base")


def collect_changes(root: Path, base: str) -> dict:
    """Files changed since the merge base, including uncommitted and untracked work."""
    mb = _git(root, "merge-base", base, "HEAD").strip()
    files: dict[str, dict] = {}
    for line in _git(root, "diff", "--numstat", "--no-renames", mb).splitlines():
        a, d, name = line.split("\t", 2)
        lines = 0 if a == "-" else int(a) + int(d)
        files[name] = {"lines": lines, "status": "modified"}
    for line in _git(root, "diff", "--name-status", "--no-renames", mb).splitlines():
        st, name = line.split("\t", 1)
        if name in files:
            files[name]["status"] = {"A": "added", "D": "removed"}.get(st[0], "modified")
    for name in _git(root, "ls-files", "--others", "--exclude-standard").splitlines():
        try:
            n = len((root / name).read_text(encoding="utf-8", errors="replace").splitlines())
        except OSError:
            n = 0
        files[name] = {"lines": n, "status": "added"}
    authors = sorted(set(_git(root, "log", "--format=%an%n%ae", f"{mb}..HEAD").split()))
    if not authors:
        authors = [_git(root, "config", "user.email").strip() or "unknown"]
    return {"files": files, "authors": authors, "base": base.removeprefix("origin/")}


def decide(policy: dict, change: dict, important: int | None = None) -> dict:
    files = change["files"]
    facts = {
        "files_changed": len(files),
        "files_added": sum(1 for f in files.values() if f["status"] == "added"),
        "files_removed": sum(1 for f in files.values() if f["status"] == "removed"),
        "diff_lines": sum(f["lines"] for f in files.values()),
        "risk": max_risk(file_risk(n) for n in files) if files else "low",
        "authors": change["authors"], "base": change["base"],
    }
    results, per_file = [], {n: [] for n in files}
    for i, r in enumerate(policy["rules"], 1):
        mine = [n for n in files if covers(r["paths"], n)]
        if not mine:
            continue
        rf = dict(facts, rule_files=len(mine), rule_lines=sum(files[n]["lines"] for n in mine),
                  rule_risk=max_risk(file_risk(n) for n in mine))
        applies = evaluate(r.get("if", True), rf)
        verdict, people, why = r["verdict"], r.get("people", 0), "rule"
        if applies:
            for j, o in enumerate(r.get("override", []) or [], 1):
                if evaluate(o["if"], rf):
                    verdict, people, why = o["verdict"], o.get("people", 0), f"override {j} ({o['if']})"
                    break
        res = {"rule": i, "purpose": r["purpose"], "files": mine, "applies": applies,
               "verdict": verdict if applies else None, "people": people if applies else 0,
               "why": why if applies else f"if not met ({r.get('if')})"}
        results.append(res)
        for n in mine:
            per_file[n].append(res)
    uncovered = sorted(n for n, rs in per_file.items() if not rs)
    no_rule = sorted(n for n, rs in per_file.items() if rs and not any(x["applies"] for x in rs))
    live = [x for x in results if x["applies"]]
    if not files:
        overall, needs = "nothing", ["no changes against the base"]
    else:
        rank = max((VERDICTS.index(x["verdict"]) for x in live), default=-1)
        overall = VERDICTS[rank] if rank >= 0 else "people"
        needs = []
        if uncovered or no_rule:
            overall = max(overall, "people", key=VERDICTS.index)
            needs.append(f"{len(uncovered) + len(no_rule)} file(s) no applying rule decides: a person must look")
        if overall == "block":
            needs.insert(0, "blocked: " + "; ".join(x["purpose"] for x in live if x["verdict"] == "block"))
        elif overall == "people":
            n = max([x["people"] for x in live if x["verdict"] == "people"] or [1])
            needs.insert(0, f"{n} human review(s)")
        elif overall == "comment":
            needs.insert(0, "a person reads the review comments; the agent may not approve")
        else:
            if important is None:
                needs.insert(0, "approvable only if the review reports 0 Important issues (pass --important N)")
            elif important > 0:
                overall = "people"
                needs.insert(0, f"review found {important} Important issue(s): fix them or get 1 human review")
            else:
                needs.insert(0, "the policy allows approval; a person still clicks approve and merge")
    public = {k: v for k, v in facts.items() if k != "authors"}
    return {"observe_only": True, "overall": overall, "needs": needs, "facts": public,
            "rules": results, "uncovered": uncovered, "no_rule_applies": no_rule}


def render(report: dict, out) -> None:
    f = report["facts"]
    print(f"approvals (observe only; nothing was approved): would decide {report['overall'].upper()}", file=out)
    for n in report["needs"]:
        print(f"  needs: {n}", file=out)
    print(f"  change: {f['files_changed']} files, {f['diff_lines']} lines, risk {f['risk']}, base {f['base']}", file=out)
    for r in report["rules"]:
        state = f"{r['verdict']}" + (f" x{r['people']}" if r["verdict"] == "people" else "") if r["applies"] else "skipped"
        print(f"  rule {r['rule']} [{state}] {r['purpose']}: {len(r['files'])} file(s); {r['why']}", file=out)
    for label, key in (("no rule covers", "uncovered"), ("no rule applies to", "no_rule_applies")):
        for n in report[key]:
            print(f"  {label}: {n}", file=out)


def load_policy(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except FileNotFoundError:
        return None, f"no policy at {path}; `ult approvals --starter` prints one to start from"
    except json.JSONDecodeError as e:
        return None, f"{path}: not valid JSON ({e})"


def run(args, out=sys.stdout) -> int:
    if args.starter:
        json.dump(STARTER, out, indent=2); out.write("\n")
        return 0
    root = Path(args.root or ".").resolve()
    path = Path(args.policy) if args.policy else root / DEFAULT_POLICY
    policy, err = load_policy(path)
    if err:
        print(f"approvals: {err}", file=sys.stderr)
        return 1
    errs = validate(policy)
    if errs:
        for e in errs:
            print(f"approvals: {path}: {e}", file=sys.stderr)
        return 1
    if args.check:
        print(f"approvals: {path}: {len(policy['rules'])} rule(s), valid", file=out)
        return 0
    try:
        base = args.base or default_base(root)
        change = collect_changes(root, base)
    except (subprocess.CalledProcessError, RuntimeError, FileNotFoundError) as e:
        print(f"approvals: cannot read the change from git: {getattr(e, 'stderr', '') or e}".strip(), file=sys.stderr)
        return 2
    report = decide(policy, change, args.important)
    if args.json:
        json.dump(report, out, indent=1); out.write("\n")
    else:
        render(report, out)
    return 0


def _args(p):
    p.add_argument("--policy", help=f"policy file (default {DEFAULT_POLICY})")
    p.add_argument("--base", help="branch to compare with (default origin/HEAD or main)")
    p.add_argument("--important", type=int, help="Important findings from the review of this change")
    p.add_argument("--check", action="store_true", help="validate the policy only")
    p.add_argument("--starter", action="store_true", help="print a starter policy")
    p.add_argument("--json", action="store_true")
    p.add_argument("--root", help="project directory (default: current)")


def register(sub):
    p = sub.add_parser("approvals", help="Observe only: what an approval policy would decide for this change")
    _args(p)
    p.set_defaults(func=run)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(prog="approvals")
    _args(ap)
    sys.exit(run(ap.parse_args()))
