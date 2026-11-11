"""`ult usage` and `ult improve`: the efficiency coach's measuring tools.

`ult usage report` reads Claude Code session transcripts on this machine
(`$CLAUDE_CONFIG_DIR/projects` or `~/.claude/projects`), including subagent
transcripts, and reports where tokens went and which work patterns look
avoidable. Privacy boundary (tested in tests/test_usage.py):
- Read-only on transcripts. Nothing is sent anywhere; no network.
- Reports contain counts, task categories, tool names, file paths and command
  names (all secret-redacted). They never contain prompt text, file contents
  or tool output.

`ult improve` is a small experiment ledger: propose a change, apply it (with
the user's approval), then measure the same metric on later sessions and keep
or roll back. State lives in `$ULTIMATUM_HOME` (default `~/.ultimatum`), not in
any project, because usage spans projects.
"""
from __future__ import annotations

import json
import os
import re
import time
from collections import Counter, defaultdict
from pathlib import Path

from .common import dump_json, redact, safe_id, write_private

# --------------------------------------------------------------------------
# Locations
# --------------------------------------------------------------------------


def transcripts_root() -> Path:
    base = os.environ.get("CLAUDE_CONFIG_DIR") or str(Path.home() / ".claude")
    return Path(base) / "projects"


def coach_home() -> Path:
    d = Path(os.environ.get("ULTIMATUM_HOME") or (Path.home() / ".ultimatum")) / "coach"
    if d.is_symlink():
        raise SystemExit(f"[ult] refusing to use {d}: it is a symlink")
    d.mkdir(mode=0o700, parents=True, exist_ok=True)
    return d


def parse_since(s: str) -> float:
    """'1d', '12h', '7d', '30m' or an ISO date -> epoch seconds."""
    m = re.fullmatch(r"(\d+)([mhdw])", s.strip())
    if m:
        mult = {"m": 60, "h": 3600, "d": 86400, "w": 604800}[m.group(2)]
        return time.time() - int(m.group(1)) * mult
    return time.mktime(time.strptime(s[:10], "%Y-%m-%d"))


def _ts(entry: dict) -> float | None:
    t = entry.get("timestamp")
    if not isinstance(t, str):
        return None
    try:
        return time.mktime(time.strptime(t[:19], "%Y-%m-%dT%H:%M:%S")) - time.timezone
    except ValueError:
        return None


# --------------------------------------------------------------------------
# Task categories: from the first real prompt, keyword based. Only the
# category is kept; the prompt text itself is discarded.
# --------------------------------------------------------------------------
CATEGORIES = [
    ("security", r"\b(audit|vulnerab|security|secur|exploit|idor|xss|injection|cve)\w*"),
    ("ci-pr", r"\b(ci|pipeline|pull request|pr\b|review comments?|github actions)"),
    ("bug", r"\b(bug|fix|broken|fail\w*|error|crash|regress\w*|flaky|doesn'?t work|not working)\b"),
    ("ui", r"\b(ui|css|style|layout|component|page|button|dialog|responsive|frontend|design)\b"),
    ("test", r"\b(test|coverage|spec)s?\b"),
    ("refactor", r"\b(refactor|clean ?up|rename|simplif\w*)\b"),
    ("docs", r"\b(readme|docs?|documentation|changelog)\b"),
    ("discover", r"\b(explain|how does|what does|where is|understand|walk me through|overview)\b"),
    ("feature", r"\b(add|build|implement|create|make|support|new)\b"),
]


def categorize(text: str) -> str:
    low = text.lower()
    for name, pat in CATEGORIES:
        if re.search(pat, low):
            return name
    return "other"


CORRECTION = re.compile(
    r"(?i)\b(that'?s (wrong|not (it|right|what))|still (fail|broken|not)|didn'?t work|doesn'?t work|"
    r"undo|revert|you (broke|missed|forgot)|try again|not what i (asked|meant)|no,? (that|it|this))")

BIG_RESULT = 20_000      # characters in one tool result
REPEAT_READ = 3          # same file read this many times in a session
REPEAT_CMD = 3           # same failing command this many times
SEARCH_CHURN = 15        # Grep/Glob/find/rg calls in a session


def _text_of(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        out = []
        for c in content:
            if isinstance(c, dict) and c.get("type") == "text":
                out.append(c.get("text", ""))
        return "\n".join(out)
    return ""


def _result_size(content) -> int:
    if isinstance(content, str):
        return len(content)
    try:
        return len(json.dumps(content))
    except (TypeError, ValueError):
        return 0


def _norm_cmd(cmd: str) -> str:
    cmd = re.sub(r"\s+", " ", cmd.strip())
    return cmd[:120]


def analyze_file(path: Path, since: float | None) -> dict | None:
    """Metrics for one transcript file. Returns None when nothing is in range."""
    usage_by_msg: dict[str, dict] = {}
    model_by_msg: dict[str, str] = {}
    tools: Counter = Counter()
    tool_inputs: dict[str, tuple[str, dict]] = {}
    reads: Counter = Counter()
    big_results: list[tuple[str, int, str]] = []
    failed_cmds: Counter = Counter()
    errors = 0
    prompts: list[str] = []
    corrections = 0
    compactions = 0
    cwd = None
    first_ts = last_ts = None
    try:
        fh = open(path, encoding="utf-8", errors="replace")
    except OSError:
        return None
    with fh:
        for line in fh:
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            ts = _ts(d)
            if since and ts and ts < since:
                continue
            if ts:
                first_ts = ts if first_ts is None else min(first_ts, ts)
                last_ts = ts if last_ts is None else max(last_ts, ts)
            cwd = cwd or d.get("cwd")
            t = d.get("type")
            if t == "system" and "compact" in str(d.get("subtype", "")):
                compactions += 1
            msg = d.get("message") if isinstance(d.get("message"), dict) else None
            if t == "assistant" and msg:
                mid = msg.get("id") or d.get("uuid") or str(len(usage_by_msg))
                u = msg.get("usage") or {}
                prev = usage_by_msg.get(mid, {})
                usage_by_msg[mid] = {k: max(prev.get(k, 0), u.get(k, 0) or 0) for k in
                                     ("input_tokens", "output_tokens", "cache_read_input_tokens",
                                      "cache_creation_input_tokens")}
                model_by_msg[mid] = msg.get("model", "?")
                for c in msg.get("content") or []:
                    if isinstance(c, dict) and c.get("type") == "tool_use":
                        name = c.get("name", "?")
                        tools[name] += 1
                        inp = c.get("input") if isinstance(c.get("input"), dict) else {}
                        tool_inputs[c.get("id", "")] = (name, inp)
                        if name == "Read" and inp.get("file_path"):
                            reads[inp["file_path"]] += 1
            elif t == "user" and msg:
                content = msg.get("content")
                if isinstance(content, list) and any(isinstance(c, dict) and c.get("type") == "tool_result" for c in content):
                    for c in content:
                        if not (isinstance(c, dict) and c.get("type") == "tool_result"):
                            continue
                        name, inp = tool_inputs.get(c.get("tool_use_id", ""), ("?", {}))
                        size = _result_size(c.get("content"))
                        if c.get("is_error"):
                            errors += 1
                            if name == "Bash" and inp.get("command"):
                                failed_cmds[_norm_cmd(inp["command"])] += 1
                        if size >= BIG_RESULT:
                            what = (inp.get("file_path") or _norm_cmd(inp.get("command", "")) or inp.get("pattern", "")
                                    or inp.get("url", "") or inp.get("description", ""))
                            limited = name == "Read" and ("limit" in inp or "offset" in inp)
                            if not limited:
                                big_results.append((name, size, str(what)[:120]))
                elif not d.get("isMeta") and not d.get("isSidechain"):
                    text = _text_of(content).strip()
                    if text and not text.startswith(("<command-", "<local-command", "<system-reminder", "[Request interrupted")):
                        prompts.append(text)
                        if len(prompts) > 1 and CORRECTION.search(text[:400]):
                            corrections += 1
    if not usage_by_msg and not prompts:
        return None
    tok = Counter()
    for u in usage_by_msg.values():
        tok.update(u)
    searches = tools["Grep"] + tools["Glob"]
    return {
        "file": str(path),
        "project": path.parent.name if path.parent.name != "subagents" else path.parent.parent.parent.name,
        "cwd": cwd,
        "is_subagent": path.parent.name == "subagents",
        "category": categorize(prompts[0]) if prompts else "subagent",
        "prompts": len(prompts),
        "corrections": corrections,
        "assistant_messages": len(usage_by_msg),
        "models": dict(Counter(model_by_msg.values())),
        "tokens": dict(tok),
        "tools": dict(tools),
        "tool_errors": errors,
        "searches": searches,
        "repeated_reads": {p: n for p, n in reads.items() if n >= REPEAT_READ},
        "big_results": big_results,
        "repeated_failures": {c: n for c, n in failed_cmds.items() if n >= REPEAT_CMD},
        "agent_calls": tools["Agent"] + tools["Task"],
        "compactions": compactions,
        "first_ts": first_ts,
        "last_ts": last_ts,
    }


def collect(since: float | None, project: str | None = None) -> list[dict]:
    root = transcripts_root()
    if not root.is_dir():
        return []
    sessions = []
    for f in root.rglob("*.jsonl"):
        try:
            if since and f.stat().st_mtime < since:
                continue
        except OSError:
            continue
        if project and project.lower() not in str(f).lower():
            continue
        r = analyze_file(f, since)
        if r:
            sessions.append(r)
    return sessions


def total_tokens(t: dict) -> int:
    return sum(t.get(k, 0) for k in ("input_tokens", "output_tokens", "cache_read_input_tokens",
                                     "cache_creation_input_tokens"))


def billable_weight(t: dict) -> float:
    """Rough relative cost: cache reads are ~10x cheaper than fresh input;
    output ~5x input. Used only to rank, never reported as dollars."""
    return (t.get("input_tokens", 0) + 1.25 * t.get("cache_creation_input_tokens", 0)
            + 0.1 * t.get("cache_read_input_tokens", 0) + 5 * t.get("output_tokens", 0))


# --------------------------------------------------------------------------
# Waste detectors. Each returns findings with evidence counts and an
# estimate in tokens (characters / 4) of the avoidable context.
# --------------------------------------------------------------------------
FIXES = {
    "big-tool-output": "Route noisy commands through `ult run` and read files by range; add the project's quiet test command to its CLAUDE.md.",
    "repeated-reads": "Note the file's key facts once (CLAUDE.md or `ult note`) or read only the needed range instead of re-reading it.",
    "repeated-failures": "Record the working command (test/build/lint) in the project's CLAUDE.md so it isn't rediscovered by trial and error.",
    "search-churn": "Add a short repo map or 'where things live' section to the project's CLAUDE.md; use `ult map`/`ult symbols` first.",
    "corrections": "Look at what the user had to correct and add the missing convention or requirement to the project's CLAUDE.md.",
    "compactions": "Split long sessions or save a handoff earlier (`ult handoff write`) so context does not overflow.",
    "subagent-share": "Check that delegation was needed; small tasks should run inline (Ultimatum §3 delegation rule).",
}


def findings(sessions: list[dict]) -> list[dict]:
    out = []
    big = [(s, b) for s in sessions for b in s["big_results"]]
    if big:
        chars = sum(b[1] for _, b in big)
        top = Counter(f"{b[0]}: {b[2]}" for _, b in big).most_common(3)
        out.append({"id": "big-tool-output", "sessions": len({s["file"] for s, _ in big}), "count": len(big),
                    "est_tokens": chars // 4, "examples": [f"{k} (x{v})" for k, v in top]})
    rr = [(s, p, n) for s in sessions for p, n in s["repeated_reads"].items()]
    if rr:
        out.append({"id": "repeated-reads", "sessions": len({s["file"] for s, _, _ in rr}), "count": sum(n for *_, n in rr),
                    "est_tokens": sum((n - 1) * 1500 for *_, n in rr),
                    "examples": [f"{p} read {n}x" for _, p, n in sorted(rr, key=lambda x: -x[2])[:3]]})
    rf = [(s, c, n) for s in sessions for c, n in s["repeated_failures"].items()]
    if rf:
        out.append({"id": "repeated-failures", "sessions": len({s["file"] for s, _, _ in rf}), "count": sum(n for *_, n in rf),
                    "est_tokens": sum(n * 2000 for *_, n in rf),
                    "examples": [f"`{c}` failed {n}x" for _, c, n in sorted(rf, key=lambda x: -x[2])[:3]]})
    sc = [s for s in sessions if s["searches"] >= SEARCH_CHURN]
    if sc:
        out.append({"id": "search-churn", "sessions": len(sc), "count": sum(s["searches"] for s in sc),
                    "est_tokens": sum((s["searches"] - SEARCH_CHURN // 2) * 800 for s in sc),
                    "examples": [f"{s['project']}: {s['searches']} searches" for s in sorted(sc, key=lambda s: -s["searches"])[:3]]})
    co = [s for s in sessions if s["corrections"]]
    if co:
        out.append({"id": "corrections", "sessions": len(co), "count": sum(s["corrections"] for s in co),
                    "est_tokens": sum(s["corrections"] * 5000 for s in co),
                    "examples": [f"{s['project']} ({s['category']}): {s['corrections']} correction(s)" for s in co[:3]]})
    cp = [s for s in sessions if s["compactions"]]
    if cp:
        out.append({"id": "compactions", "sessions": len(cp), "count": sum(s["compactions"] for s in cp),
                    "est_tokens": sum(s["compactions"] * 20000 for s in cp),
                    "examples": [f"{s['project']}: {s['compactions']} compaction(s)" for s in cp[:3]]})
    sub = sum(total_tokens(s["tokens"]) for s in sessions if s["is_subagent"])
    allt = sum(total_tokens(s["tokens"]) for s in sessions) or 1
    if sub / allt > 0.4:
        out.append({"id": "subagent-share", "sessions": sum(1 for s in sessions if s["is_subagent"]), "count": 0,
                    "est_tokens": 0, "examples": [f"subagents used {sub * 100 // allt}% of all tokens"]})
    for f in out:
        f["fix"] = FIXES[f["id"]]
        f["examples"] = [redact(e) for e in f["examples"]]
    return sorted(out, key=lambda f: -f["est_tokens"])


def summarize(sessions: list[dict]) -> dict:
    main = [s for s in sessions if not s["is_subagent"]]
    tok = Counter()
    for s in sessions:
        tok.update(s["tokens"])
    by_cat = defaultdict(lambda: {"sessions": 0, "tokens": 0, "corrections": 0})
    for s in main:
        c = by_cat[s["category"]]
        c["sessions"] += 1
        c["tokens"] += total_tokens(s["tokens"])
        c["corrections"] += s["corrections"]
    for s in sessions:
        if s["is_subagent"]:
            by_cat["(subagents)"]["sessions"] += 1
            by_cat["(subagents)"]["tokens"] += total_tokens(s["tokens"])
    tools = Counter()
    for s in sessions:
        tools.update(s["tools"])
    return {"sessions": len(main), "subagent_runs": len(sessions) - len(main), "tokens": dict(tok),
            "total_tokens": total_tokens(tok), "by_category": dict(by_cat), "top_tools": tools.most_common(8),
            "tool_errors": sum(s["tool_errors"] for s in sessions),
            "corrections": sum(s["corrections"] for s in main)}


def render(summary: dict, finds: list[dict], since_label: str) -> str:
    t = summary["tokens"]
    total = summary["total_tokens"] or 1
    lines = [f"# Efficiency review ({since_label}, {time.strftime('%Y-%m-%d')})", "",
             f"**{summary['sessions']} sessions** (+{summary['subagent_runs']} subagent runs), "
             f"{summary['total_tokens']:,} tokens: cache read {t.get('cache_read_input_tokens', 0) * 100 // total}%, "
             f"cache write {t.get('cache_creation_input_tokens', 0) * 100 // total}%, "
             f"fresh input {t.get('input_tokens', 0) * 100 // total}%, output {t.get('output_tokens', 0) * 100 // total}%. "
             f"Tool errors: {summary['tool_errors']}. User corrections: {summary['corrections']}.", "",
             "## Where tokens went", "", "| Category | Sessions | Tokens | Corrections |", "|---|---|---|---|"]
    for cat, v in sorted(summary["by_category"].items(), key=lambda kv: -kv[1]["tokens"]):
        lines.append(f"| {cat} | {v['sessions']} | {v['tokens']:,} | {v['corrections']} |")
    lines += ["", "Top tools: " + ", ".join(f"{n}×{c}" for n, c in summary["top_tools"]), "",
              "## Avoidable work (estimates)", ""]
    if not finds:
        lines.append("No waste pattern crossed its threshold in this window.")
    for i, f in enumerate(finds, 1):
        if f["count"]:
            lines.append(f"{i}. **{f['id']}**: {f['count']} occurrence(s) in {f['sessions']} session(s), "
                         f"~{f['est_tokens']:,} tokens of avoidable context (rough estimate).")
        else:
            lines.append(f"{i}. **{f['id']}** ({f['sessions']} session(s)):")
        for e in f["examples"]:
            lines.append(f"   - {e}")
        lines.append(f"   - Fix: {f['fix']}")
    lines += ["", "Estimates are heuristics for ranking, not measured savings. "
              "Only an applied change measured with `ult improve measure` shows a real effect."]
    return redact("\n".join(lines)) + "\n"


def cmd_usage(args) -> int:
    since = parse_since(args.since) if args.since else None
    sessions = collect(since, args.project)
    if not sessions:
        print(f"[ult usage] no transcripts found under {transcripts_root()} for that window")
        return 1
    summary = summarize(sessions)
    finds = findings(sessions)
    report = render(summary, finds, f"last {args.since}" if args.since else "all time")
    print(report)
    if args.save:
        d = coach_home() / "reports"
        d.mkdir(mode=0o700, exist_ok=True)
        p = d / f"{time.strftime('%Y-%m-%d')}.md"
        write_private(p, report)
        write_private(p.with_suffix(".json"), dump_json({"summary": summary, "findings": finds}))
        print(f"[ult usage] saved {p}")
    return 0


# --------------------------------------------------------------------------
# Experiment ledger
# --------------------------------------------------------------------------
STATES = ("proposed", "applied", "kept", "rolled-back", "rejected")


def _ledger_path() -> Path:
    return coach_home() / "experiments.json"


def _load() -> list[dict]:
    p = _ledger_path()
    return json.loads(p.read_text()) if p.exists() else []


def _save(items: list[dict]) -> None:
    write_private(_ledger_path(), dump_json(items))


def _metric(sessions: list[dict], category: str | None) -> dict:
    sel = [s for s in sessions if not s["is_subagent"] and (not category or s["category"] == category)]
    n = len(sel)
    if not n:
        return {"sessions": 0}
    return {"sessions": n,
            "tokens_per_session": sum(total_tokens(s["tokens"]) for s in sel) // n,
            "weighted_per_session": int(sum(billable_weight(s["tokens"]) for s in sel) / n),
            "corrections_per_session": round(sum(s["corrections"] for s in sel) / n, 2),
            "tool_errors_per_session": round(sum(s["tool_errors"] for s in sel) / n, 2)}


def cmd_improve(args) -> int:
    items = _load()
    if args.action == "propose":
        iid = f"I-{len(items) + 1:03d}"
        items.append({"id": iid, "state": "proposed", "title": redact(args.title), "change": redact(args.change or ""),
                      "target": args.target, "finding": args.finding, "category": args.category,
                      "project": args.project, "created": time.strftime("%Y-%m-%dT%H:%M:%S")})
        _save(items)
        print(f"[ult improve] {iid} proposed: {args.title}")
        return 0
    if args.action == "list":
        if not items:
            print("[ult improve] no experiments yet")
        for it in items:
            print(f"{it['id']}  {it['state']:<11} {it['title']}  -> {it.get('target') or '?'}")
        return 0
    if not args.id:
        raise SystemExit("[ult improve] this action needs an experiment id")
    safe_id(args.id)
    it = next((x for x in items if x["id"] == args.id), None)
    if not it:
        raise SystemExit(f"[ult improve] unknown id {args.id}")
    if args.action == "apply":
        since = parse_since(args.baseline)
        it["baseline"] = _metric(collect(since, it.get("project")), it.get("category"))
        it["state"], it["applied"] = "applied", time.time()
        _save(items)
        print(f"[ult improve] {it['id']} applied. Baseline ({args.baseline}): {json.dumps(it['baseline'])}")
        if it["baseline"].get("sessions", 0) < 3:
            print("[ult improve] warning: fewer than 3 baseline sessions; the comparison will be weak")
        return 0
    if args.action == "measure":
        if "applied" not in it:
            raise SystemExit("[ult improve] not applied yet")
        after = _metric(collect(it["applied"], it.get("project")), it.get("category"))
        before = it.get("baseline", {})
        it["after"] = after
        _save(items)
        print(f"[ult improve] {it['id']} {it['title']}")
        print(f"  before: {json.dumps(before)}")
        print(f"  after:  {json.dumps(after)}")
        if after.get("sessions", 0) < 3 or before.get("sessions", 0) < 3:
            print("  verdict: not enough sessions yet (need >= 3 on each side); keep collecting")
            return 0
        tok_change = (after["weighted_per_session"] - before["weighted_per_session"]) / max(1, before["weighted_per_session"])
        worse_quality = (after["corrections_per_session"] > before["corrections_per_session"] + 0.2
                         or after["tool_errors_per_session"] > before["tool_errors_per_session"] * 1.5 + 0.5)
        if worse_quality:
            print(f"  verdict: ROLL BACK: quality signals got worse (corrections/errors up), token change {tok_change:+.0%}")
        elif tok_change <= -0.10:
            print(f"  verdict: KEEP: weighted tokens per session {tok_change:+.0%} with no quality regression")
        else:
            print(f"  verdict: NO CLEAR EFFECT ({tok_change:+.0%}); roll back unless it helps in another way")
        print("  (sessions differ in difficulty; treat this as a signal, not proof)")
        return 0
    if args.action in ("keep", "rollback", "reject"):
        it["state"] = {"keep": "kept", "rollback": "rolled-back", "reject": "rejected"}[args.action]
        it["decided"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        it["evidence"] = redact(args.evidence or "")
        _save(items)
        print(f"[ult improve] {it['id']} -> {it['state']}")
        return 0
    return 2


def register(sub):
    p = sub.add_parser("usage", help="analyze local Claude Code transcripts: where tokens went, avoidable work")
    p.add_argument("action", choices=["report"])
    p.add_argument("--since", default="1d", help="window: 30m, 12h, 1d, 7d, 2w or YYYY-MM-DD (default 1d)")
    p.add_argument("--project", help="only transcripts whose path contains this text")
    p.add_argument("--save", action="store_true", help="save report to $ULTIMATUM_HOME/coach/reports/")
    p.set_defaults(func=cmd_usage)

    p = sub.add_parser("improve", help="experiment ledger: propose/apply/measure/keep/rollback a workflow change")
    p.add_argument("action", choices=["propose", "list", "apply", "measure", "keep", "rollback", "reject"])
    p.add_argument("id", nargs="?")
    p.add_argument("--title")
    p.add_argument("--change", help="what will be edited, in one or two sentences")
    p.add_argument("--target", help="file the change edits, e.g. ./CLAUDE.md")
    p.add_argument("--finding", help="finding id from `ult usage report`, e.g. repeated-failures")
    p.add_argument("--category", help="restrict measurement to one task category")
    p.add_argument("--project", help="restrict measurement to transcripts whose path contains this")
    p.add_argument("--baseline", default="7d", help="window before applying used as the baseline (default 7d)")
    p.add_argument("--evidence", help="why it was kept/rolled back")
    p.set_defaults(func=cmd_improve)
