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


def newest_transcript(cwd: Path) -> Path | None:
    """The most recently written transcript of the chat running in `cwd`."""
    base = Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude") / "projects"
    d = base / re.sub(r"[^A-Za-z0-9]", "-", str(cwd))
    files = sorted(d.glob("*.jsonl"), key=lambda p: p.stat().st_mtime) if d.is_dir() else []
    return files[-1] if files else None


def current_transcript() -> Path | None:
    for cand in (Path.cwd().resolve(), project_root()):
        f = newest_transcript(cand)
        if f:
            return f
    return None


def latest_context(cwd: Path) -> tuple[int, int] | None:
    f = newest_transcript(cwd)
    if not f:
        return None
    tokens, turns, _ = transcript_stats(f)
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


def set_cap(tokens: int, env=os.environ) -> Path:
    """Write autoCompactWindow to the user's Claude Code settings; other keys are kept."""
    path = Path(env.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude") / "settings.json"
    data = {}
    if path.is_file():
        data = json.loads(path.read_text(encoding="utf-8") or "{}")
        if not isinstance(data, dict):
            raise ValueError("settings.json is not a JSON object")
    data["autoCompactWindow"] = tokens
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".json.ult-tmp")
    tmp.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)
    return path


def cmd_context(args) -> int:
    if args.cap is not None:
        if args.cap < 50_000:
            print("[ult context] --cap must be at least 50000 tokens")
            return 2
        try:
            path = set_cap(args.cap)
        except (OSError, ValueError) as e:
            print(f"[ult context] could not set the cap: {e}")
            return 1
        print(f"[ult context] autoCompactWindow={args.cap} in {path}; applies from the next chat")
        return 0
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
              f"Run `ult handoff write` now; auto-compaction will shrink the chat. Keep working here.")
        return 3
    print(f"[ult context] ok: ~{tokens:,} tokens per turn ({turns} turns so far)")
    return 0


def register(sub):
    p = sub.add_parser("context", help="how many tokens each turn of this chat re-reads (exit 3 if high)")
    p.add_argument("--cap", type=int, help="hold new chats to this many tokens (writes autoCompactWindow "
                   "in your Claude Code settings), e.g. 200000")
    p.set_defaults(func=cmd_context)
