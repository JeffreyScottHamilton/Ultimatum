"""`ult loop` — a small review-loop list: Reviewer reports, Manager sorts, maker fixes, Reviewer rechecks.

  ult loop add "TEXT" [--where W] [--at 0:04]   Reviewer reports a finding to the Manager (state: new)
  ult loop triage ID --blocker|--minor [--to builder|animator]   Manager decides what must be fixed
  ult loop fixed ID [--note N]                   Builder or Animator says the fix is in
  ult loop recheck ID --pass|--fail [--note N]   Reviewer rechecks; a fail goes back to the maker
  ult loop status                                exit 1 while a blocker is open or a finding is unsorted
  ult loop clear                                 start a new list for the next job

Use it only when it helps track the work (several findings, or helpers). Lives in .ultimatum/review-loop.json.
"""
from __future__ import annotations

import json
from pathlib import Path

from .common import dump_json, project_root, redact, state_dir, write_private

FILE = "review-loop.json"


def _path(root: Path) -> Path:
    return state_dir(root) / FILE


def load(root: Path) -> list[dict]:
    try:
        data = json.loads(_path(root).read_text(encoding="utf-8"))
        return data.get("items", []) if isinstance(data, dict) else []
    except (OSError, ValueError):
        return []


def save(root: Path, items: list[dict]) -> None:
    write_private(_path(root), dump_json({"items": items}))


def _find(items: list[dict], ident: str) -> dict | None:
    return next((i for i in items if i["id"].lower() == ident.lower()), None)


def blocking(items: list[dict]) -> tuple[list[dict], list[dict]]:
    """(open blockers, unsorted findings): either one holds delivery."""
    return ([i for i in items if i.get("severity") == "blocker" and i["state"] != "passed"],
            [i for i in items if i["state"] == "new"])


def _line(i: dict) -> str:
    sev = i.get("severity") or "unsorted"
    owner = f" -> {i['owner']}" if i.get("owner") else ""
    where = " @ " + ", ".join(x for x in (i.get("where"), i.get("at")) if x) if i.get("where") or i.get("at") else ""
    return f"{i['id']} [{sev}/{i['state']}{owner}]{where}: {i['text']}"


def cmd_loop(args) -> int:
    root = Path(args.root).resolve() if args.root else project_root()
    items = load(root)
    act = args.action
    if act == "clear":
        save(root, [])
        print("review loop cleared")
        return 0
    if act == "add":
        text = redact(" ".join(args.rest).strip())
        if not text:
            print("ult loop add needs the finding in words")
            return 2
        ident = f"F{len(items) + 1}"
        items.append({"id": ident, "text": text, "where": args.where, "at": args.at,
                      "severity": None, "owner": None, "state": "new", "notes": []})
        save(root, items)
        print(f"{ident} reported to the Manager (sort it: ult loop triage {ident} --blocker|--minor)")
        return 0
    if act == "status":
        open_b, unsorted = blocking(items)
        for i in items:
            print(_line(i))
        minor = [i for i in items if i.get("severity") == "minor"]
        if open_b or unsorted:
            print(f"delivery: blocked ({len(open_b)} open blocker(s), {len(unsorted)} unsorted)")
            return 1
        print(f"delivery: clear ({len(minor)} minor to mention in the report)" if items else "delivery: clear (no findings)")
        return 0
    if not args.rest:
        print(f"ult loop {act} needs a finding id")
        return 2
    item = _find(items, args.rest[0])
    if not item:
        print(f"ult loop: no finding {args.rest[0]}")
        return 2
    note = " ".join(args.rest[1:]).strip() or args.note
    if act == "triage":
        if args.blocker == args.minor:
            print("ult loop triage needs exactly one of --blocker or --minor")
            return 2
        item["severity"] = "blocker" if args.blocker else "minor"
        item["owner"] = args.to if args.blocker else None
        item["state"] = "assigned" if args.blocker else "noted"
    elif act == "fixed":
        if item.get("severity") != "blocker":
            print(f"{item['id']} is not an assigned blocker; triage it first")
            return 2
        item["state"] = "fixed"
    elif act == "recheck":
        if args.ok == args.fail:
            print("ult loop recheck needs exactly one of --pass or --fail")
            return 2
        if item["state"] != "fixed":
            print(f"{item['id']} is {item['state']}; recheck after the maker runs: ult loop fixed {item['id']}")
            return 2
        item["state"] = "passed" if args.ok else "assigned"
    if note:
        item.setdefault("notes", []).append(redact(note))
    save(root, items)
    print(_line(item))
    return 0


def register(sub):
    p = sub.add_parser("loop", help="review loop: Reviewer reports, Manager sorts blockers, maker fixes, Reviewer rechecks")
    p.add_argument("action", choices=["add", "triage", "fixed", "recheck", "status", "clear"])
    p.add_argument("rest", nargs="*", help="finding text (add) or finding id (triage, fixed, recheck)")
    p.add_argument("--where", help="file:line, page and steps, or shot")
    p.add_argument("--at", help="timestamp in the video, e.g. 0:04")
    p.add_argument("--blocker", action="store_true", help="must be fixed before delivery")
    p.add_argument("--minor", action="store_true", help="report it; does not hold delivery")
    p.add_argument("--to", choices=["builder", "animator", "manager"], default="builder")
    p.add_argument("--pass", dest="ok", action="store_true", help="recheck passed")
    p.add_argument("--fail", action="store_true", help="recheck failed; back to the maker")
    p.add_argument("--note")
    p.add_argument("--root", help="project directory (default: the current project)")
    p.set_defaults(func=cmd_loop)
