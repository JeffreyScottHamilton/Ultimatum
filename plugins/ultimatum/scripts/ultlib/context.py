"""`ult context` — how much conversation each turn re-reads in this chat.

Every turn re-sends the whole chat, so a long chat multiplies the cost of
every later step. Reads only the last usage record of the newest transcript
for this project (local, read-only) and prints one line with a verdict.
"""
from __future__ import annotations

import json
import os
import re
from datetime import datetime
from pathlib import Path

from .common import project_root

HIGH = 150_000


def latest_context(cwd: Path) -> tuple[int, int] | None:
    base = Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude") / "projects"
    slug = re.sub(r"[^A-Za-z0-9]", "-", str(cwd))
    d = base / slug
    files = sorted(d.glob("*.jsonl"), key=lambda p: p.stat().st_mtime) if d.is_dir() else []
    if not files:
        return None
    tokens, turns, _ = transcript_stats(files[-1])
    return tokens, turns


def _epoch(ts) -> float | None:
    if not isinstance(ts, str):
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return None


def transcript_stats(path: Path) -> tuple[int, int, float | None]:
    """(tokens the last turn re-read, assistant turns, epoch of the last assistant turn)."""
    last, turns, when = 0, 0, None
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if '"assistant"' not in line:
                continue
            try:
                e = json.loads(line)
                u = e.get("message", {}).get("usage") or {}
            except (json.JSONDecodeError, AttributeError):
                continue
            c = u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0) + u.get("cache_creation_input_tokens", 0)
            if c:
                last, turns = c, turns + 1
                when = _epoch(e.get("timestamp")) or when
    return last, turns, when


def cmd_context(args) -> int:
    r = None
    for cand in (Path.cwd().resolve(), project_root()):
        r = latest_context(cand)
        if r:
            break
    if not r:
        print("[ult context] no transcript found for this project; size unknown")
        return 1
    tokens, turns = r
    if tokens >= HIGH:
        print(f"[ult context] HIGH: each turn re-reads ~{tokens:,} tokens ({turns} turns so far). "
              f"Write a handoff and continue in a fresh chat.")
        return 3
    print(f"[ult context] ok: ~{tokens:,} tokens per turn ({turns} turns so far)")
    return 0


def register(sub):
    p = sub.add_parser("context", help="how many tokens each turn of this chat re-reads (exit 3 if high)")
    p.set_defaults(func=cmd_context)
