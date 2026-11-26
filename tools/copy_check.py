#!/usr/bin/env python3
"""Flag word runs that our files share with a third-party source.

Used when a third-party skill is rebuilt in Ultimatum's own words
(docs/plans/skill-rebuild-prompt.md). Both folders are read as text; each file is
lower-cased, URLs are dropped (links to official docs are allowed), and the rest
is split into words (letters and digits; punctuation and spacing are ignored).
Any run of N or more words (default 8) found in both is a hit.

    python3 tools/copy_check.py OURS_DIR SOURCE_DIR [--words 8]

Exit codes: 0 no hits, 1 at least one hit, 2 bad arguments.
Standard library only; no network.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Phrases that may appear on both sides: API names, spec titles and similar
# fixed strings that cannot be reworded. A hit is ignored when every word of the
# shared run lies inside one of these phrases. Keep the list short and say why.
ALLOW = (
    # WCAG 2.2 success criterion titles are fixed names.
    "web content accessibility guidelines wcag 2 2",
)

TEXT_SUFFIXES = {
    ".md", ".txt", ".html", ".htm", ".css", ".js", ".mjs", ".cjs", ".ts", ".tsx",
    ".jsx", ".json", ".csv", ".py", ".sh", ".yml", ".yaml", ".svg", ".toml",
}
MAX_BYTES = 4_000_000
URL = re.compile(r"https?://\S+")
WORD = re.compile(r"[a-z0-9]+(?:'[a-z0-9]+)*")


def words(text: str) -> list[tuple[str, int]]:
    """Words of a text with their 1-based line numbers."""
    out: list[tuple[str, int]] = []
    for lineno, line in enumerate(text.lower().replace("’", "'").splitlines(), 1):
        line = URL.sub(" ", line)
        out.extend((w, lineno) for w in WORD.findall(line))
    return out


def read_texts(root: Path):
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if ".git" in path.parts or path.stat().st_size > MAX_BYTES:
            continue
        try:
            yield path, path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue


def allowed_spans(tokens: list[str], n: int) -> set[int]:
    """Start indexes of shingles that sit fully inside an allowed phrase."""
    ok: set[int] = set()
    for phrase in ALLOW:
        p = phrase.split()
        for i in range(len(tokens) - len(p) + 1):
            if tokens[i:i + len(p)] == p:
                ok.update(range(i, i + len(p) - n + 1))
    return ok


def check(ours: Path, source: Path, n: int) -> list[str]:
    shingles: set[tuple[str, ...]] = set()
    for _, text in read_texts(source):
        toks = [w for w, _ in words(text)]
        shingles.update(tuple(toks[i:i + n]) for i in range(len(toks) - n + 1))

    hits: list[str] = []
    for path, text in read_texts(ours):
        pairs = words(text)
        toks = [w for w, _ in pairs]
        skip = allowed_spans(toks, n)
        i = 0
        while i <= len(toks) - n:
            if i in skip or tuple(toks[i:i + n]) not in shingles:
                i += 1
                continue
            end = i + n
            while end < len(toks) and tuple(toks[end - n + 1:end + 1]) in shingles:
                end += 1
            hits.append(f"{path}:{pairs[i][1]}: {' '.join(toks[i:end])}")
            i = end
    return hits


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("ours", type=Path)
    ap.add_argument("source", type=Path)
    ap.add_argument("--words", type=int, default=8, help="shared run length that counts as a hit")
    args = ap.parse_args(argv)
    if not args.ours.is_dir() or not args.source.is_dir() or args.words < 2:
        print("copy_check: both arguments must be folders and --words at least 2", file=sys.stderr)
        return 2
    hits = check(args.ours, args.source, args.words)
    for h in hits:
        print(h)
    print(f"copy_check: {len(hits)} shared run(s) of {args.words}+ words")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
