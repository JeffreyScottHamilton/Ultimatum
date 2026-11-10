"""`ult note` / `ult find` / `ult get` — local searchable evidence store.

SQLite FTS5 in .ultimatum/index.db. Indexes run logs (in 40-line chunks that
keep their line numbers) and notes (decisions, findings, facts). Retrieval
returns references plus short snippets; `ult get` returns the exact text.
The store never replaces the source: a hit points back to a log line range or
a file path that must be read before it is relied on.
"""
from __future__ import annotations

import re
import sqlite3
import time
from pathlib import Path

from .common import raw_lines, redact, safe_id, state_dir

CHUNK = 40


def _db() -> sqlite3.Connection:
    path = state_dir() / "index.db"
    if path.is_symlink():
        raise SystemExit(f"[ult] refusing to open {path}: it is a symlink")
    con = sqlite3.connect(path)
    con.execute(
        "CREATE VIRTUAL TABLE IF NOT EXISTS docs USING fts5("
        "ref UNINDEXED, kind, title, body, created UNINDEXED, tokenize='porter unicode61')"
    )
    try:
        path.chmod(0o600)
    except OSError:
        pass
    return con


def index_log(rid: str, lines: list[str], meta: dict) -> None:
    con = _db()
    with con:
        con.execute("DELETE FROM docs WHERE ref LIKE ?", (f"log:{rid}:%",))
        for start in range(0, max(1, len(lines)), CHUNK):
            body = "\n".join(lines[start:start + CHUNK])
            end = min(len(lines), start + CHUNK)
            con.execute(
                "INSERT INTO docs VALUES (?,?,?,?,?)",
                (f"log:{rid}:{start + 1}-{end}", "log", meta.get("cmd", ""), body, meta.get("started", "")),
            )
    con.close()


def add_note(kind: str, title: str, body: str) -> str:
    con = _db()
    ref = f"note:{int(time.time() * 1000)}"
    with con:
        con.execute("INSERT INTO docs VALUES (?,?,?,?,?)",
                    (ref, kind, title, redact(body), time.strftime("%Y-%m-%dT%H:%M:%S")))
    con.close()
    return ref


def _fts_query(q: str) -> str:
    # Treat user input as literal terms (quote each), so punctuation in error
    # strings like `TypeError:` or `a.b.c` does not become FTS syntax.
    terms = [t.replace('"', '""') for t in q.split() if t.strip()]
    return " ".join(f'"{t}"' for t in terms) or '""'


def find(q: str, kind: str | None = None, limit: int = 10) -> list[tuple]:
    con = _db()
    sql = ("SELECT ref, kind, title, snippet(docs, 3, '[', ']', ' … ', 12) FROM docs "
           "WHERE docs MATCH ?")
    params: list = [_fts_query(q)]
    if kind:
        sql += " AND kind = ?"
        params.append(kind)
    sql += " ORDER BY rank LIMIT ?"
    params.append(limit)
    try:
        rows = con.execute(sql, params).fetchall()
    finally:
        con.close()
    return rows


def get(ref: str) -> str | None:
    if ref.startswith("log:"):
        m = re.match(r"^log:([^:]+):(\d+)-(\d+)$", ref)
        if not m:
            return None
        try:
            rid = safe_id(m.group(1))
        except ValueError:
            return None
        a, b = int(m.group(2)), int(m.group(3))
        p = state_dir(sub="logs") / f"{rid}.log"
        if not p.is_file():
            return None
        lines = raw_lines(p.read_bytes().decode("utf-8", "replace"))
        return "\n".join(f"{i}\t{lines[i - 1]}" for i in range(a, min(b, len(lines)) + 1))
    con = _db()
    row = con.execute("SELECT kind, title, body, created FROM docs WHERE ref = ?", (ref,)).fetchone()
    con.close()
    if not row:
        return None
    return f"[{row[0]}] {row[1]} ({row[3]})\n{row[2]}"


def cmd_note(args) -> int:
    body = args.body
    if body == "-":
        import sys
        body = sys.stdin.read()
    print(add_note(args.kind, args.title, body))
    return 0


def cmd_find(args) -> int:
    rows = find(" ".join(args.query), args.kind, args.limit)
    if not rows:
        print("[ult find] no matches")
        return 1
    for ref, kind, title, snip in rows:
        print(f"{ref}  ({kind}) {redact(title)[:60]}\n    {redact(snip).replace(chr(10), ' ⏎ ')}")
    print("[ult find] exact text: ult get <ref>")
    return 0


def cmd_get(args) -> int:
    out = get(args.ref)
    if out is None:
        print(f"not found: {args.ref}")
        return 1
    print(redact(out))
    return 0


def register(sub):
    p = sub.add_parser("note", help="save a decision/fact/finding note to the local index")
    p.add_argument("--kind", default="note", choices=["note", "decision", "fact", "finding", "todo"])
    p.add_argument("--title", required=True)
    p.add_argument("--body", required=True, help="text, or - for stdin")
    p.set_defaults(func=cmd_note)
    p = sub.add_parser("find", help="full-text search logs and notes; returns refs + snippets")
    p.add_argument("query", nargs="+")
    p.add_argument("--kind")
    p.add_argument("--limit", type=int, default=10)
    p.set_defaults(func=cmd_find)
    p = sub.add_parser("get", help="exact text for a ref from `ult find`")
    p.add_argument("ref")
    p.set_defaults(func=cmd_get)
