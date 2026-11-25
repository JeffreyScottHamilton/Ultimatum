#!/usr/bin/env python3
"""Deterministic token-waste analysis of live-eval stream-json transcripts.

Usage: analyze.py <transcript-dir> [--arms a b ...] [--json]

Reads <case>__<arm>.jsonl files. Local only; standard library only.
Token estimates are bytes/4.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

SLEEP_RE = re.compile(r"(^|[;&|\s])sleep\s+\d")
CAT_RE = re.compile(r"^\s*cat\s+(?:-\S+\s+)*(\S+)\s*$")
TEST_RE = re.compile(r"\b(pytest|unittest|jest|vitest|rspec|phpunit)\b|\b(npm|pnpm|yarn)\s+(run\s+)?test\b"
                     r"|\bgo\s+test\b|\bcargo\s+test\b|\bmvn\s+test\b|\bgradle\s+test\b|\bmake\s+test\b")
ULT_RUN_RE = re.compile(r"\bult(?:\s|\S*/ult\s)+run\b|/ult\s+run\b")
ULT_ROUTE_RE = re.compile(r"\bult\b.*\broute\b")
REF_MARK = "skills/work/references"
WASTE_MIN_BYTES = 2000


def _size(content) -> int:
    if isinstance(content, str):
        return len(content.encode("utf-8", "replace"))
    try:
        return len(json.dumps(content).encode("utf-8"))
    except (TypeError, ValueError):
        return 0


def _short(s: str, n: int = 60) -> str:
    s = " ".join(str(s).split())
    return s if len(s) <= n else s[: n - 1] + "~"


def analyze_run(path: Path) -> dict:
    m = {"first_ctx": 0, "cache_creation": 0, "turns": 0, "tools": Counter(), "result_bytes": 0,
         "largest": (0, ""), "ref_reads": 0, "rereads": 0, "polls": 0, "bg_agents": 0,
         "tests_raw": 0, "tests_ult": 0, "routes": 0, "waste": []}
    uses: dict[str, tuple[str, dict]] = {}
    paths: Counter = Counter()
    seen_msgs: set = set()
    first = True
    result_usage = None
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            d = json.loads(line)
        except ValueError:
            continue
        if not isinstance(d, dict):
            continue
        t = d.get("type")
        msg = d.get("message") if isinstance(d.get("message"), dict) else {}
        if t == "result":
            result_usage = d.get("usage") if isinstance(d.get("usage"), dict) else None
            if isinstance(d.get("num_turns"), int):
                m["turns"] = d["num_turns"]
        elif t == "assistant":
            u = msg.get("usage") if isinstance(msg.get("usage"), dict) else {}
            mid = msg.get("id")
            if mid not in seen_msgs:
                seen_msgs.add(mid)
                m["cache_creation"] += int(u.get("cache_creation_input_tokens") or 0)
                if first and u:
                    m["first_ctx"] = sum(int(u.get(k) or 0) for k in
                                         ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"))
                    first = False
            for c in msg.get("content") or []:
                if not (isinstance(c, dict) and c.get("type") == "tool_use"):
                    continue
                name = str(c.get("name"))
                inp = c.get("input") if isinstance(c.get("input"), dict) else {}
                uses[str(c.get("id"))] = (name, inp)
                m["tools"][name] += 1
                cmd = inp.get("command") if isinstance(inp.get("command"), str) else ""
                fp = inp.get("file_path") if isinstance(inp.get("file_path"), str) else ""
                if name == "Read" and fp:
                    paths[fp] += 1
                    if REF_MARK in fp:
                        m["ref_reads"] += 1
                elif name.lower() == "bash":
                    cm = CAT_RE.match(cmd)
                    if cm:
                        paths[cm.group(1)] += 1
                        if REF_MARK in cm.group(1):
                            m["ref_reads"] += 1
                    elif REF_MARK in cmd and re.search(r"\b(cat|sed|head|tail)\b", cmd):
                        m["ref_reads"] += 1
                    if SLEEP_RE.search(cmd):
                        m["polls"] += 1
                    if ULT_ROUTE_RE.search(cmd):
                        m["routes"] += 1
                elif name == "Monitor":
                    m["polls"] += 1
                if name == "Agent" and inp.get("run_in_background"):
                    m["bg_agents"] += 1
        elif t == "user" and isinstance(msg.get("content"), list):
            for c in msg["content"]:
                if not (isinstance(c, dict) and c.get("type") == "tool_result"):
                    continue
                name, inp = uses.get(str(c.get("tool_use_id")), ("?", {}))
                size = _size(c.get("content"))
                m["result_bytes"] += size
                cmd = inp.get("command") if isinstance(inp.get("command"), str) else ""
                label = f"{name}: {_short(cmd or inp.get('file_path') or inp.get('pattern') or inp.get('description') or '')}"
                if size > m["largest"][0]:
                    m["largest"] = (size, label)
                if name.lower() == "bash" and TEST_RE.search(cmd):
                    if ULT_RUN_RE.search(cmd):
                        m["tests_ult"] += 1
                    else:
                        m["tests_raw"] += 1
                        if size > 8192:
                            m["waste"].append(("raw-test", size, label))
                if size >= WASTE_MIN_BYTES:
                    m["waste"].append(("big-result", size, label))
    m["rereads"] = sum(1 for n in paths.values() if n >= 2)
    for p, n in paths.items():
        if n >= 2:
            m["waste"].append(("reread", 0, f"{_short(p, 70)} x{n}"))
    if not m["turns"]:
        m["turns"] = len(seen_msgs)
    m["tool_calls"] = sum(m["tools"].values())
    if result_usage and not m["cache_creation"]:
        m["cache_creation"] = int(result_usage.get("cache_creation_input_tokens") or 0)
    return m


def analyze_dir(d: Path, arms=None) -> dict:
    out: dict = defaultdict(dict)
    for f in sorted(d.glob("*__*.jsonl")):
        case, arm = f.stem.rsplit("__", 1)
        if arms and arm not in arms:
            continue
        out[arm][case] = analyze_run(f)
    return dict(out)


def arm_totals(runs: dict) -> dict:
    t = {"runs": len(runs), "first_ctx": 0, "cache_creation": 0, "turns": 0, "tool_calls": 0, "result_bytes": 0,
         "largest": (0, ""), "ref_reads": 0, "rereads": 0, "polls": 0, "bg_agents": 0,
         "tests_raw": 0, "tests_ult": 0, "routes": 0}
    for r in runs.values():
        for k in ("cache_creation", "turns", "tool_calls", "result_bytes", "ref_reads", "rereads", "polls",
                  "bg_agents", "tests_raw", "tests_ult", "routes"):
            t[k] += r[k]
        t["first_ctx"] += r["first_ctx"]
        if r["largest"][0] > t["largest"][0]:
            t["largest"] = r["largest"]
    if t["runs"]:
        t["first_ctx"] //= t["runs"]
    return t


def waste_list(runs: dict, top: int = 5) -> list:
    items = []
    for case, r in runs.items():
        for kind, size, label in r["waste"]:
            items.append((size // 4, kind, case, label))
    return sorted(items, key=lambda x: -x[0])[:top]


COLS = [("runs", "runs"), ("first_ctx", "first-ctx avg"), ("cache_creation", "cache-create"), ("turns", "turns"),
        ("tool_calls", "tool calls"), ("result_bytes", "result KB"), ("ref_reads", "ref reads"),
        ("rereads", "rereads"), ("polls", "polls"), ("bg_agents", "bg agents"), ("tests_raw", "tests raw"),
        ("tests_ult", "tests ult run"), ("routes", "routes")]


def render(res: dict) -> str:
    lines = ["| arm | " + " | ".join(h for _, h in COLS) + " | largest result |",
             "|" + "---|" * (len(COLS) + 2)]
    for arm in sorted(res):
        t = arm_totals(res[arm])
        cells = [str(t[k] // 1024 if k == "result_bytes" else t[k]) for k, _ in COLS]
        lines.append(f"| {arm} | " + " | ".join(cells) + f" | {t['largest'][0]} B {t['largest'][1]} |")
    for arm in sorted(res):
        lines += ["", f"Waste ({arm}), est. tokens = bytes/4:"]
        w = waste_list(res[arm])
        lines += [f"- {tok} tok  {kind}  {case}  {label}" for tok, kind, case, label in w] or ["- none"]
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("dir")
    ap.add_argument("--arms", nargs="*")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    d = Path(a.dir)
    if not d.is_dir():
        print(f"not a directory: {d}", file=sys.stderr)
        return 2
    res = analyze_dir(d, a.arms)
    if a.json:
        print(json.dumps({arm: {"totals": arm_totals(runs), "runs": runs, "waste": waste_list(runs)}
                          for arm, runs in res.items()}, indent=1, default=lambda o: dict(o) if isinstance(o, Counter) else str(o)))
    else:
        print(render(res))
    return 0


if __name__ == "__main__":
    sys.exit(main())
