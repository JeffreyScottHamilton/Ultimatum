"""`ult budget` — what this chat costs per turn, and where the cost went.

Reads the transcript of the current chat (local, read-only) and prints at most
six lines: turns, the tokens the latest turn re-read, the cache-read share, and
the three most expensive turns with the tool names they used. Tool names only:
no prompt text, paths or tool output.

`--record` appends one totals line to state_dir()/usage.jsonl so later runs can
compare chats. Parsing is shared with usage.py and context.py.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import time
from pathlib import Path

from . import usage
from .common import state_dir
from .context import HIGH, current_transcript

KEYS = ("input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens")
TOOL_RE = re.compile(r"^[A-Za-z0-9_.:-]{1,40}$")


def _int(v) -> int:
    try:
        return max(0, int(v))
    except (TypeError, ValueError):
        return 0


def parse_turns(path: Path) -> list[dict]:
    """One entry per assistant message with usage, in order. Streamed duplicates count once."""
    msgs: dict[str, dict] = {}
    tools: dict[str, set] = {}
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if '"assistant"' not in line:
                continue
            try:
                d = json.loads(line)
            except ValueError:
                continue
            msg = d.get("message") if isinstance(d, dict) else None
            if not isinstance(msg, dict) or not isinstance(msg.get("usage"), dict):
                continue
            mid = str(msg.get("id") or d.get("uuid") or len(msgs))
            u = msgs.setdefault(mid, {k: 0 for k in KEYS})
            for k in KEYS:
                u[k] = max(u[k], _int(msg["usage"].get(k)))
            names = tools.setdefault(mid, set())
            for c in msg.get("content") or []:
                if isinstance(c, dict) and c.get("type") == "tool_use" and TOOL_RE.match(str(c.get("name", ""))):
                    names.add(str(c["name"]))
    turns = []
    for mid, u in msgs.items():
        if not usage.total_tokens(u):
            continue
        turns.append({
            "index": len(turns) + 1,
            "usage": u,
            "input_side": u["input_tokens"] + u["cache_read_input_tokens"] + u["cache_creation_input_tokens"],
            "tools": sorted(tools.get(mid, set()))[:4],
        })
    return turns


def _k(n: int) -> str:
    return f"{n / 1000:.1f}k" if n >= 1000 else str(n)


def summarize(turns: list[dict]) -> dict:
    latest = turns[-1]["input_side"] if turns else 0
    side = sum(t["input_side"] for t in turns) or 1
    cache = sum(t["usage"]["cache_read_input_tokens"] for t in turns)
    output = sum(t["usage"]["output_tokens"] for t in turns)
    top = sorted(turns, key=lambda t: -usage.billable_weight(t["usage"]))[:3]
    return {"turns": len(turns), "latest": latest, "cache_share": cache * 100 // side,
            "output": output, "top": top}


def _session(path: Path) -> str:
    return hashlib.sha1(str(path.resolve()).encode("utf-8")).hexdigest()[:12]


def record(path: Path, s: dict) -> Path:
    d = state_dir()
    f = d / "usage.jsonl"
    if f.is_symlink():
        raise SystemExit(f"[ult] refusing to use {f}: it is a symlink")
    line = json.dumps({"ts": int(time.time()), "session": _session(path), "turns": s["turns"],
                       "latest_tokens": s["latest"], "cache_read_share": s["cache_share"],
                       "output_tokens": s["output"],
                       "top_tokens": [usage.total_tokens(t["usage"]) for t in s["top"]]},
                      sort_keys=True) + "\n"
    fd = os.open(f, os.O_WRONLY | os.O_CREAT | os.O_APPEND | getattr(os, "O_NOFOLLOW", 0), 0o600)
    with os.fdopen(fd, "a", encoding="utf-8") as fh:
        fh.write(line)
    return f


def cmd_budget(args) -> int:
    if args.transcript:
        path = Path(args.transcript).resolve()
    else:
        path = current_transcript()
    if not path or not path.is_file():
        print("[ult budget] no transcript found for this chat; nothing to measure")
        return 1
    s = summarize(parse_turns(path))
    if not s["turns"]:
        print("[ult budget] transcript has no usage records yet")
        return 1
    verdict = f" HIGH: run `ult handoff write` soon." if s["latest"] >= HIGH else ""
    plural = "" if s["turns"] == 1 else "s"
    print(f"[ult budget] {s['turns']} turn{plural}; latest turn re-reads ~{s['latest']:,} tokens.{verdict}")
    print(f"cache read: {s['cache_share']}% of input-side tokens; output: {s['output']:,} tokens")
    tops = [f"#{t['index']} {_k(usage.total_tokens(t['usage']))} ({', '.join(t['tools']) or 'text'})" for t in s["top"]]
    print("top costs: " + "; ".join(tops))
    if args.record:
        f = record(path, s)
        print(f"recorded totals line in {f.parent.name}/usage.jsonl")
    return 0


def register(sub):
    p = sub.add_parser("budget", help="tokens per turn, cache share and top costs for this chat")
    p.add_argument("--record", action="store_true", help="append a totals line to .ultimatum/usage.jsonl")
    p.add_argument("--transcript", help="transcript .jsonl (default: this chat)")
    p.set_defaults(func=cmd_budget)
