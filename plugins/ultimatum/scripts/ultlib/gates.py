"""Approval gates the Manager keeps for the user: brief, mockup, data-model, publish, post,
deploy, live-payments.

State lives in .ultimatum/approvals.json next to the shared brief (.ultimatum/brief.md).
Each approval stores the user's words, the time, and a fingerprint of the "## Build brief"
section (and of a file, when one is named). If the build brief or that file changes after
the approval, the item reads "changed since approval" and counts as not approved, so a
resumed project never treats a newer draft as the approved one.

A data-model approval must name the schema or migration file (--file), and a post approval the
social plan file, so any later edit to it reopens the gate. Publish, post, deploy and
live-payments approvals are used once: `ult gate done ITEM` closes them after the action.
Local, stdlib only, no network.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import time
from pathlib import Path

from .common import project_root, state_dir, write_private
from .website import brief_path

ITEMS = ("brief", "mockup", "data-model", "publish", "post", "deploy", "live-payments")
NEEDS_FILE = ("data-model", "post")
WHAT = {
    "brief": "build brief (shown to the user before the build starts)",
    "mockup": "website mockup (before production code)",
    "publish": "putting the site live (domain, hosting, listings)",
    "data-model": "app data model: tables, who may read and write each (before migrations run)",
    "post": "posting, scheduling or sending one batch of social posts (the approved plan file)",
    "deploy": "deploying or releasing",
    "live-payments": "switching payments to live keys and real charges",
}
BRIEF_HEAD = "## Build brief"
REQUIRED = ("Audience", "Offer", "Main visitor action")
FILE = "approvals.json"


def section(text: str, head: str) -> str:
    _, sep, rest = text.partition(head)
    return rest.split("\n## ", 1)[0].strip() if sep else ""


def brief_section(root: Path) -> str:
    try:
        return section(brief_path(root).read_text(encoding="utf-8", errors="replace"), BRIEF_HEAD)
    except OSError:
        return ""


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()[:16]


def _file_sha(path: str) -> str | None:
    try:
        return _sha(Path(path).read_bytes())
    except OSError:
        return None


def _path(root: Path) -> Path:
    return brief_path(root).parent / FILE


def load(root: Path) -> dict:
    try:
        data = json.loads(_path(root).read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def save(root: Path, data: dict) -> None:
    state_dir(root)
    write_private(_path(root), json.dumps(data, indent=2) + "\n")


def status(root: Path, item: str) -> tuple[str, str]:
    """("approved" | "waiting" | "changed" | "revise", detail)."""
    rec = (load(root).get("items") or {}).get(item)
    if not rec:
        return "waiting", "not approved yet"
    if rec.get("state") == "revise":
        return "revise", f"changes asked: {rec.get('note', '')}"
    if rec.get("state") == "done":
        return "waiting", "used once already; ask again"
    if rec.get("brief") != _sha(brief_section(root).encode()):
        return "changed", "the build brief changed since approval; show it again"
    if rec.get("file"):
        now = _file_sha(rec["file"])
        if now != rec.get("file_sha"):
            return "changed", f"{rec['file']} changed or is missing since approval; show it again"
    extra = f" (link checked: {rec['link']})" if rec.get("link") else ""
    return "approved", f"{rec.get('note', '')}{extra}"


def _record(root: Path, item: str, rec: dict) -> None:
    data = load(root)
    items = data.setdefault("items", {})
    rec["at"] = time.strftime("%Y-%m-%d %H:%M")
    items[item] = rec
    data.setdefault("history", []).append({"item": item, **rec})
    data["history"] = data["history"][-50:]
    save(root, data)


def approve(root: Path, item: str, note: str, link: str | None = None, file: str | None = None) -> str:
    if item == "brief" and not brief_section(root):
        raise ValueError(f"no '{BRIEF_HEAD}' section in {brief_path(root)}; Business drafts it first")
    if item in NEEDS_FILE and not file:
        raise ValueError(f"{item}: name the file the user approved with --file (schema or migration, or the social plan)")
    if item == "brief":
        empty = [f for f in REQUIRED if re.search(rf"^- {f}:\s*$", brief_section(root), re.M | re.I)]
        if empty:
            raise ValueError("the build brief still has empty fields: " + ", ".join(empty))
    rec = {"state": "approved", "note": note.strip(), "brief": _sha(brief_section(root).encode())}
    if link:
        rec["link"] = link
    if file:
        sha = _file_sha(file)
        if sha is None:
            raise ValueError(f"cannot read {file}")
        rec["file"], rec["file_sha"] = str(Path(file).resolve()), sha
    _record(root, item, rec)
    return status(root, item)[0]


def cmd_gate(args) -> int:
    root = Path(args.root).resolve() if args.root else project_root()
    rest = list(args.rest or [])
    if args.action == "status":
        rows = {i: status(root, i) for i in ITEMS}
        if args.json:
            print(json.dumps({i: {"state": s, "detail": d} for i, (s, d) in rows.items()}, indent=2))
            return 0
        for i, (s, d) in rows.items():
            print(f"{i:<15}{s:<9}{d if s != 'waiting' else WHAT[i]}")
        return 0
    if not rest or rest[0] not in ITEMS:
        print(f"name one of: {', '.join(ITEMS)}", file=sys.stderr)
        return 2
    item, note = rest[0], " ".join(rest[1:]).strip()
    if args.action == "check":
        s, d = status(root, item)
        need_link = args.need_link and s == "approved" and "link checked" not in d
        if need_link:
            s, d = "waiting", "approved, but the live link is not checked yet"
        print(f"{item}: {s}: {d}")
        return 0 if s == "approved" else 1
    if args.action in ("approve", "revise") and not note:
        print("write the user's own words: what they approved or what to change", file=sys.stderr)
        return 2
    if args.action == "approve":
        try:
            s = approve(root, item, note, link=args.link, file=args.file)
        except ValueError as e:
            print(str(e), file=sys.stderr)
            return 2
        print(f"{item}: {s}: recorded in {_path(root)}")
        return 0
    if args.action == "revise":
        _record(root, item, {"state": "revise", "note": note, "brief": ""})
        print(f"{item}: revise: {note}")
        return 0
    if args.action == "done":
        if status(root, item)[0] != "approved":
            print(f"{item}: not approved; nothing to close", file=sys.stderr)
            return 1
        _record(root, item, {"state": "done", "note": note or "used", "brief": ""})
        print(f"{item}: used; the next one needs a new approval")
        return 0
    return 2


def register(sub):
    p = sub.add_parser("gate", help="user approvals: " + ", ".join(ITEMS))
    p.add_argument("action", choices=["status", "check", "approve", "revise", "done"])
    p.add_argument("rest", nargs="*", help="ITEM then the user's words")
    p.add_argument("--link", help="live link that was checked (publish, deploy)")
    p.add_argument("--file", help="file the approval is for (mockup image, schema or migration, social plan)")
    p.add_argument("--need-link", action="store_true", help="check: also require a checked live link")
    p.add_argument("--json", action="store_true")
    p.add_argument("--root", help="project directory (default: the current project)")
    p.set_defaults(func=cmd_gate)
