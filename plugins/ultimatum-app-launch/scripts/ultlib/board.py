"""`ult board` and `ult notes` — a card board and linked notes for big projects.

A long project outlives the chat that started it. The board holds one Markdown card
per piece of work (Backlog, Doing, Blocked, Done); the notes hold decisions and facts
as Markdown pages that link to each other and to cards with [[name]], so the folder
also opens as an Obsidian vault. After lost context, `ult board show` says where to
pick up and `ult notes links NAME` follows the trail.

  ult board add "TITLE" [--check C] [--files F] [--link NOTE]   new card in Backlog
  ult board move ID backlog|doing|blocked|done [--note N]
  ult board show                                 columns, then the cards to resume
  ult board card ID                              one card in full
  ult notes add NAME "TEXT"                      append to notes/NAME.md (created if new)
  ult notes show NAME | list | links NAME        a note, all notes, links in and out

Lives in .ultimatum/board/ and .ultimatum/notes/ (git-ignored). Small jobs skip it.
"""
from __future__ import annotations

import re
from pathlib import Path

from .common import project_root, redact, state_dir, write_private

STATES = ("backlog", "doing", "blocked", "done")
LINK = re.compile(r"\[\[([^\]|#]+)")
_FIELD = re.compile(r"^(status|check|files|links): ?(.*)$", re.M)


def _root(args) -> Path:
    return Path(args.root).resolve() if args.root else project_root()


def _slug(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s[:40] or "note"


# ---- board ---------------------------------------------------------------

def _board(root: Path) -> Path:
    return state_dir(root) / "board"


def cards(root: Path) -> list[dict]:
    out = []
    for p in sorted(_board(root).glob("C*.md"), key=lambda p: int(re.match(r"C(\d+)", p.name).group(1))
                    if re.match(r"C(\d+)", p.name) else 0):
        text = p.read_text(encoding="utf-8")
        fields = dict(_FIELD.findall(text))
        title = text.splitlines()[0].lstrip("# ").strip() if text else p.stem
        out.append({"id": p.name.split("-", 1)[0], "path": p, "title": title,
                    "status": fields.get("status", "backlog"), "text": text})
    return out


def _find(root: Path, ident: str) -> dict | None:
    return next((c for c in cards(root) if c["id"].lower() == ident.lower()), None)


def _write_card(path: Path, text: str) -> None:
    write_private(path, text if text.endswith("\n") else text + "\n")


def cmd_board(args) -> int:
    root = _root(args)
    act = args.action
    if act == "add":
        title = redact(" ".join(args.rest).strip())
        if not title:
            print("ult board add needs the card title in words")
            return 2
        n = max([int(c["id"][1:]) for c in cards(root)] or [0]) + 1
        links = " ".join(f"[[{redact(x)}]]" for x in (args.link or []))
        body = [f"# C{n} {title}", "status: backlog", f"check: {redact(args.check or '')}",
                f"files: {redact(args.files or '')}", f"links: {links}", "", "## Log"]
        path = _board(root) / f"C{n}-{_slug(title)}.md"
        _write_card(path, "\n".join(body))
        print(f"C{n} added to backlog ({path.relative_to(root) if path.is_relative_to(root) else path})")
        return 0
    if act == "show":
        all_cards = cards(root)
        if not all_cards:
            print("board: empty (big project? add the first card: ult board add \"<goal>\" --check \"<how to know it works>\")")
            return 0
        for state in STATES:
            group = [c for c in all_cards if c["status"] == state]
            print(f"{state} ({len(group)})" + "".join(f"\n  {c['id']} {c['title'].split(' ', 1)[-1]}" for c in group))
        resume = [c for c in all_cards if c["status"] in ("doing", "blocked")] or \
                 [c for c in all_cards if c["status"] == "backlog"][:1]
        print("resume: " + (", ".join(f"{c['id']} ({c['status']})" for c in resume) if resume else "all done"))
        return 0
    if not args.rest:
        print(f"ult board {act} needs a card id")
        return 2
    card = _find(root, args.rest[0])
    if not card:
        print(f"ult board: no card {args.rest[0]}")
        return 2
    if act == "card":
        print(card["text"].rstrip())
        return 0
    # move
    if len(args.rest) < 2 or args.rest[1] not in STATES:
        print(f"ult board move {card['id']} needs one of: {', '.join(STATES)}")
        return 2
    new = args.rest[1]
    text = re.sub(r"^status: .*$", f"status: {new}", card["text"], count=1, flags=re.M)
    note = redact(" ".join(args.rest[2:]).strip() or (args.note or ""))
    text = text.rstrip("\n") + f"\n- {card['status']} -> {new}" + (f": {note}" if note else "")
    _write_card(card["path"], text)
    print(f"{card['id']} -> {new}")
    return 0


# ---- notes ---------------------------------------------------------------

def _notes(root: Path) -> Path:
    return state_dir(root) / "notes"


def _note_path(root: Path, name: str) -> Path:
    return _notes(root) / f"{_slug(name)}.md"


def links_out(text: str) -> list[str]:
    seen = []
    for m in LINK.findall(text):
        s = m.strip()
        if s and s not in seen:
            seen.append(s)
    return seen


def cmd_notes(args) -> int:
    root = _root(args)
    act = args.action
    if act == "list":
        names = sorted(p.stem for p in _notes(root).glob("*.md"))
        print("\n".join(names) if names else "notes: none yet (ult notes add <name> \"<decision or fact>\")")
        return 0
    if not args.rest:
        print(f"ult notes {act} needs a note name")
        return 2
    name = args.rest[0]
    path = _note_path(root, name)
    if act == "add":
        text = redact(" ".join(args.rest[1:]).strip())
        if not text:
            print("ult notes add needs the text to save")
            return 2
        old = path.read_text(encoding="utf-8") if path.is_file() else f"# {name}\n"
        write_private(path, old.rstrip("\n") + f"\n- {text}\n")
        print(f"saved to notes/{path.name}")
        return 0
    if act == "show":
        if not path.is_file():
            print(f"ult notes: no note {name}")
            return 2
        print(path.read_text(encoding="utf-8").rstrip())
        return 0
    # links: outgoing from this note, incoming from other notes and cards
    out = links_out(path.read_text(encoding="utf-8")) if path.is_file() else []
    key = _slug(name)
    incoming = []
    for p in sorted(_notes(root).glob("*.md")) + [c["path"] for c in cards(root)]:
        if p != path and key in {_slug(x) for x in links_out(p.read_text(encoding="utf-8"))}:
            incoming.append(p.stem if p.parent == _notes(root) else p.name.split("-", 1)[0])
    print("out: " + (", ".join(out) or "none"))
    print("in: " + (", ".join(incoming) or "none"))
    return 0 if path.is_file() or incoming else 2


def register(sub):
    p = sub.add_parser("board", help="card board for big projects: backlog, doing, blocked, done; read first after lost context")
    p.add_argument("action", choices=["add", "move", "show", "card"])
    p.add_argument("rest", nargs="*", help="title (add), or card id then state (move) or id (card)")
    p.add_argument("--check", help="how to know the card is done")
    p.add_argument("--files", help="files or pages the card touches")
    p.add_argument("--link", action="append", help="note name to link with [[name]] (repeatable)")
    p.add_argument("--note", help="why it moved")
    p.add_argument("--root", help="project directory (default: the current project)")
    p.set_defaults(func=cmd_board)
    n = sub.add_parser("notes", help="linked Markdown notes ([[name]]) for decisions and facts; opens as an Obsidian vault")
    n.add_argument("action", choices=["add", "show", "list", "links"])
    n.add_argument("rest", nargs="*", help="note name, then text (add)")
    n.add_argument("--root", help="project directory (default: the current project)")
    n.set_defaults(func=cmd_notes)
