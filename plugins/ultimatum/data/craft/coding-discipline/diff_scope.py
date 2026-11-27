#!/usr/bin/env python3
"""Flag hunks in a zero-context diff that look like drive-by edits.

    git diff -U0 | python3 diff_scope.py [--allow GLOB ...]

Prints "path:line kind" per suspect hunk and exits 1 if any. Kinds: whitespace-only,
quote-only, comment-only, reorder-only, outside-scope. Reads stdin only; standard library.
"""
from __future__ import annotations

import fnmatch
import re
import sys
from argparse import ArgumentParser

HUNK = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@")
COMMENT = re.compile(r"^\s*(#|//|/\*|\*|--|<!--|;)")


def squash(lines: list[str]) -> str:
    return "".join("".join(ln.split()) for ln in lines)


def kind(old: list[str], new: list[str]) -> str | None:
    if not old and not new:
        return None
    if squash(old) == squash(new):
        return "whitespace-only"
    if squash(old).replace("'", '"') == squash(new).replace("'", '"'):
        return "quote-only"
    changed = [ln for ln in old + new if ln.strip()]
    if changed and all(COMMENT.match(ln) for ln in changed):
        return "comment-only"
    if old and new and len(old) == len(new) and sorted(old) == sorted(new):
        return "reorder-only"
    return None


def scan(text: str, allow: list[str]) -> list[str]:
    out: list[str] = []
    path, line, old, new = None, 0, [], []
    header = False
    flagged_files: set[str] = set()

    def flush() -> None:
        k = kind(old, new) if path else None
        if k:
            out.append(f"{path}:{line} {k}")

    for raw in text.splitlines():
        if raw.startswith("diff --git "):
            flush(); path, old, new = None, [], []
            header = True
        elif header and raw.startswith("--- "):
            continue
        elif header and raw.startswith("+++ "):
            target = raw[4:].strip()
            path = None if target == "/dev/null" else re.sub(r"^b/", "", target)
            if path and allow and not any(fnmatch.fnmatch(path, g) for g in allow) and path not in flagged_files:
                flagged_files.add(path)
                out.append(f"{path}:1 outside-scope")
        elif (m := HUNK.match(raw)):
            flush(); old, new = [], []
            line, header = int(m.group(1)), False
        elif header:
            continue
        elif raw.startswith("-"):
            old.append(raw[1:])
        elif raw.startswith("+"):
            new.append(raw[1:])
    flush()
    return out


def main(argv: list[str] | None = None) -> int:
    ap = ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--allow", action="append", default=[], help="glob of paths the request covers")
    args = ap.parse_args(argv)
    found = scan(sys.stdin.read(), args.allow)
    for row in found:
        print(row)
    print(f"{len(found)} suspect hunk(s)" if found else "no drive-by hunks found")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
