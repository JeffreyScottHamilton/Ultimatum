#!/usr/bin/env python3
"""Compare a compressed prose file with its original and list what went missing.

Usage: check_compressed.py ORIGINAL COMPRESSED
Exit 0 when every protected item survived, 1 when something is missing, 2 on bad usage.
Standard library only; reads the two files and writes nothing.
"""
from __future__ import annotations

import collections
import pathlib
import re
import sys

Counter = collections.Counter
Path = pathlib.Path

FENCE = re.compile(r"^(```|~~~).*?^\1[ \t]*$", re.M | re.S)
INLINE = re.compile(r"`[^`\n]+`")
URL = re.compile(r"https?://[^\s)>\]]+")
HEADING = re.compile(r"^#{1,6}[ \t]+(.+?)[ \t]*$", re.M)
NUMBER = re.compile(r"(?<![\w.])\d+(?:[.,:]\d+)*(?:%|[a-zA-Z]{1,3}\b)?")
NEGATION = re.compile(r"\b(not|never|no|only|except|unless|without|don't|doesn't|isn't|can't|won't|must not)\b", re.I)


def _prose(text: str) -> str:
    """Text outside fenced blocks and inline code."""
    return INLINE.sub(" ", FENCE.sub(" ", text))


def protected(text: str) -> dict[str, Counter]:
    prose = _prose(text)
    return {
        "fenced block": Counter(m.group(0) for m in FENCE.finditer(text)),
        "inline code": Counter(INLINE.findall(FENCE.sub(" ", text))),
        "url": Counter(URL.findall(text)),
        "heading": Counter(HEADING.findall(FENCE.sub(" ", text))),
        "number": Counter(NUMBER.findall(prose)),
        "negation": Counter(w.lower() for w in NEGATION.findall(prose)),
    }


def missing(original: str, compressed: str) -> list[str]:
    before, after = protected(original), protected(compressed)
    out = []
    for kind, wanted in before.items():
        lost = wanted - after[kind]
        for item, n in sorted(lost.items()):
            shown = item if len(item) <= 70 else item[:67] + "..."
            out.append(f"{kind}: {shown!r} (missing {n})")
    return out


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(__doc__.strip().splitlines()[2], file=sys.stderr)
        return 2
    original, compressed = (Path(a).read_text(encoding="utf-8") for a in argv[1:])
    problems = missing(original, compressed)
    for line in problems:
        print("MISSING " + line)
    a, b = len(original.encode()), len(compressed.encode())
    print(f"bytes {a} -> {b} ({b - a:+d}); {'ok' if not problems else str(len(problems)) + ' missing'}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
