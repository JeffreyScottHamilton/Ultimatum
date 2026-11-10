"""`ult handoff` — short, checkable session handoff in .ultimatum/handoff.md.

`write` composes the file from explicit fields plus facts gathered locally
(git branch/HEAD, changed files, recent `ult run` results). `show` prints it
and checks that what it references still exists and whether HEAD moved, so a
fresh session knows which parts to trust before acting on them.
"""
from __future__ import annotations

import json
import re
import subprocess
import time
from pathlib import Path

from .common import project_root, redact, state_dir, write_private


def _git(root: Path, *a: str) -> str:
    try:
        r = subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True, timeout=20)
        return r.stdout.strip() if r.returncode == 0 else ""
    except (OSError, subprocess.SubprocessError):
        return ""


def _recent_runs(n: int = 6) -> list[dict]:
    logs = state_dir(sub="logs")
    out = []
    for p in sorted(logs.glob("*.json"), key=lambda p: p.stat().st_mtime)[-n:]:
        try:
            out.append(json.loads(p.read_text()))
        except json.JSONDecodeError:
            pass
    return out


def compose(root: Path, a) -> str:
    branch = _git(root, "rev-parse", "--abbrev-ref", "HEAD") or "(no git)"
    head = _git(root, "rev-parse", "--short", "HEAD") or "(none)"
    changed = _git(root, "status", "--short").splitlines()
    parts = [f"# Handoff — {time.strftime('%Y-%m-%d %H:%M')}", "",
             f"<!-- ult: branch={branch} head={head} -->", "",
             "## Goal", a.goal or "(unstated)", "",
             "## Decisions (with why)"]
    parts += [f"- {d}" for d in (a.decision or [])] or ["- (none recorded)"]
    parts += ["", "## Changed files"]
    files = [l for l in changed if not l.endswith(".ultimatum/")]
    parts += [f"- `{l[3:]}` ({l[:2].strip() or 'M'})" for l in files] or ["- (working tree clean)"]
    parts += [f"- {x}" for x in (a.file or [])]
    parts += ["", "## Evidence (commands run, exit codes, log refs)"]
    runs = _recent_runs()
    parts += [f"- `{r['cmd']}` → exit {r['exit_code']} (log `{r['id']}`)" for r in runs] or ["- (no `ult run` logs)"]
    parts += [f"- {e}" for e in (a.evidence or [])]
    parts += ["", "## Next unfinished step", a.next or "(unstated)", "", "## Open questions"]
    parts += [f"- {q}" for q in (a.question or [])] or ["- (none)"]
    return redact("\n".join(parts) + "\n")


def check(root: Path, text: str) -> list[str]:
    notes = []
    m = re.search(r"head=(\S+)", text)
    head = _git(root, "rev-parse", "--short", "HEAD")
    if m and head and m.group(1) not in ("(none)", head):
        notes.append(f"HEAD moved since handoff: {m.group(1)} → {head} (re-verify evidence)")
    for f in re.findall(r"`([^`\s]+\.[A-Za-z0-9]{1,5})`", text):
        if "/" in f or "." in f:
            if not (root / f).exists() and not f.startswith(("ult ", "python")):
                notes.append(f"referenced file missing: {f}")
    logs = state_dir(sub="logs")
    for lid in re.findall(r"log `([\w.-]+)`", text):
        if not (logs / f"{lid}.log").exists():
            notes.append(f"log not found locally: {lid}")
    return notes


def cmd_handoff(args) -> int:
    root = project_root()
    path = state_dir(root) / "handoff.md"
    if args.action == "write":
        text = compose(root, args)
        write_private(path, text)
        hist = state_dir(root, "handoffs") / f"{time.strftime('%Y%m%d-%H%M%S')}.md"
        write_private(hist, text)
        print(f"[ult handoff] wrote {path.relative_to(root)} ({len(text.splitlines())} lines)")
        return 0
    if not path.exists():
        print("[ult handoff] no handoff found at .ultimatum/handoff.md")
        return 1
    text = path.read_text()
    print(text)
    notes = check(root, text)
    print("[ult handoff] check: " + ("all references present" if not notes else ""))
    for n in notes:
        print(f"  ! {n}")
    return 0


def register(sub):
    p = sub.add_parser("handoff", help="write or show/check .ultimatum/handoff.md")
    p.add_argument("action", choices=["write", "show"])
    p.add_argument("--goal")
    p.add_argument("--decision", action="append", help="'what — why' (repeatable)")
    p.add_argument("--file", action="append", help="extra changed-file note (repeatable)")
    p.add_argument("--evidence", action="append", help="extra evidence line (repeatable)")
    p.add_argument("--next", help="the single next unfinished step")
    p.add_argument("--question", action="append")
    p.set_defaults(func=cmd_handoff)
