"""`ult copylint` — flag generic page copy: banned words, stock lines and over-used devices.

    python3 copylint.py PATH... [--allow WORD]... [--year YYYY] [--json]

PATH is an .html, .htm, .md or .txt file, or a folder searched for them. In HTML only
visible text counts: script, style, comments and elements marked data-copy-ok (words
the client wrote themselves) are skipped. Rules come from the website references:
craft/taste/copy.md § Tells, craft/taste/voice.md § Device budget and
website/design-rules.md § 2.

Banned items fail at once. Capped devices have a per-page budget: over it is a
warning, and twice the budget plus one is a failure. Exit 0 when nothing fails
(warnings are still listed), 1 on any failure, 2 on bad arguments.
Standard library only, no network.
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

SUFFIXES = {".html", ".htm", ".md", ".txt"}
HEADINGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
ACTIONS = {"a", "button"}
SKIP = {"script", "style", "noscript", "template", "svg", "code", "pre"}
VOID = {"img", "br", "hr", "input", "meta", "link", "source", "wbr", "col", "area", "base", "embed", "track"}


def _words(*items: str) -> re.Pattern:
    return re.compile(r"\b(?:" + "|".join(items) + r")\b", re.I)


# Banned outright: (rule, pattern). Matched against every text run.
BANNED = [
    ("residue", re.compile(r"\bcertainly!|\bas an ai\b|\blorem ipsum\b|\[need\]|\{\{|\}\}|\bTODO\b|\bto be added\b", re.I)),
    ("worn word", _words("delve[sd]?", "delving", "tapestry", "elevate[sd]?", "elevating", "seamless(?:ly)?", "robust",
                         "leverag(?:e|es|ed|ing)", "unlock(?:s|ed|ing)?", "empower(?:s|ed|ing)?", "cutting-edge",
                         "game-changer", "testament", "realm", "bespoke", "curated")),
    ("stock line", re.compile(r"in today's fast-paced world|look no further|take (?:it|your \w+) to the next level|"
                              r"we've got you covered", re.I)),
    ("metaphor frame", re.compile(r"\bwhere \w+(?: \w+)? meets\b|\bthe heart of\b|\bjourney\b|\becosystem\b|\bhub\b",
                                  re.I)),
    ("virtue word", _words("passionate", "dependable", "thoughtful", "genuine", "honest", "quiet", "calm", "simply",
                           "truly", "crafted")),
    ("process talk", re.compile(r"\bthis section shows\b|\bbelow you'll find\b|\bwe've added\b", re.I)),
    ("exclamation", re.compile(r"\w!(?:\s|$)")),
    ("middle dots", re.compile(r"\S · \S")),
    ("sparkle or emoji", re.compile("[✦✨\U0001F300-\U0001FAFF]")),
]

# Capped devices: (rule, pattern, budget per page).
CAPPED = [
    ("em dash", re.compile(r"\w ?— ?\w"), 2),
    ("-ing tail", re.compile(r", (?:making|helping|allowing|ensuring|giving|letting|enabling)\b", re.I), 1),
    ("question answered at once", re.compile(r"\?\s+[A-Z]\w*(?: \w+)?\.(?:\s|$)"), 1),
    ("inflated verb", re.compile(r"\bplays? a (?:key|vital|crucial) role\b|\bstands as\b|\bserves as\b", re.I), 1),
    ("contrast frame", re.compile(r"\bnot (?:just )?\w+(?: \w+)?, but\b|\bisn't \w+(?: \w+)?[,;] it's\b", re.I), 2),
    ("negation run", re.compile(r"(?:\bNo \w+(?: \w+)?\.\s*){3,}"), 1),
    ("clipped rhythm", re.compile(r"(?:(?<![\w,])[A-Z]\w*(?: \w+)?\.\s+){2,}[A-Z]\w*(?: \w+)?\.(?=\s|$)"), 1),
    ("since year", re.compile(r"\bsince (?:19|20)\d\d\b", re.I), 1),
    ("real", _words("real"), 2),
]

BUTTON_BANNED = {"click here", "more", "explore", "discover", "read more", "learn more", "here"}
NUMBER = r"(?:\d+|ten|nine|eight|seven|six|five|four|three|two|one)"
NUMBER_PAIR = re.compile(rf"^{NUMBER} \w+, {NUMBER} \w+$", re.I)
COPYRIGHT = re.compile(r"(?:©|\(c\)|copyright)\s*(?:\d{4}\s*[-–]\s*)?((?:19|20)\d\d)\b", re.I)


class _Text(HTMLParser):
    """Collect visible text runs as (line, tag context, text)."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, bool]] = []
        self.runs: list[tuple[int, str, str]] = []
        self.blocks: list[list] = []  # [tag, line, text, depth] for headings and actions
        self.open: list[list] = []

    def _hidden(self) -> bool:
        return any(tag in SKIP or ok for tag, ok in self.stack)

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        ok = any(name == "data-copy-ok" for name, _ in attrs) or any(
            name == "aria-hidden" and value == "true" for name, value in attrs)
        self.stack.append((tag, ok))
        if (tag in HEADINGS or tag in ACTIONS) and not self._hidden():
            block = [tag, self.getpos()[0], "", len(self.stack)]
            self.blocks.append(block)
            self.open.append(block)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break
        self.open = [b for b in self.open if b[3] <= len(self.stack)]

    def handle_data(self, data):
        if not data.strip() or self._hidden():
            return
        context = next((tag for tag, _ in reversed(self.stack) if tag in HEADINGS | ACTIONS), "")
        self.runs.append((self.getpos()[0], context, data))
        for block in self.open:
            block[2] += data


def _read(path: Path) -> tuple[list[tuple[int, str, str]], list[tuple[str, int, str]]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix.lower() in {".html", ".htm"}:
        parser = _Text()
        parser.feed(text)
        parser.close()
        blocks = [(tag, line, " ".join(body.split())) for tag, line, body, _ in parser.blocks]
        return parser.runs, blocks
    runs, blocks = [], []
    for n, line in enumerate(text.splitlines(), 1):
        heading = re.match(r"^(#{1,6})\s+(.*)$", line)
        if heading:
            blocks.append((f"h{len(heading.group(1))}", n, heading.group(2).strip()))
        runs.append((n, "", line))
    return runs, blocks


def _excerpt(text: str, start: int, end: int) -> str:
    lo, hi = max(0, start - 30), min(len(text), end + 30)
    return " ".join(text[lo:hi].split())


def lint(path: Path, allow: set[str] = frozenset(), year: int | None = None) -> list[dict]:
    """Return the findings for one file, each {level, rule, line, text}."""
    year = year or datetime.date.today().year
    runs, blocks = _read(path)
    allowed = {a.lower() for a in allow}
    found: list[dict] = []

    def add(level, rule, line, text):
        found.append({"file": str(path), "level": level, "rule": rule, "line": line, "text": text})

    joined = []
    for line, _context, text in runs:
        for rule, pattern in BANNED:
            for m in pattern.finditer(text):
                if m.group(0).strip(" !").lower() not in allowed:
                    add("fail", rule, line, _excerpt(text, m.start(), m.end()))
        for m in COPYRIGHT.finditer(text):
            if int(m.group(1)) < year:
                add("fail", "old copyright year", line, m.group(0))
        joined.append((line, text))

    for rule, pattern, budget in CAPPED:
        hits = []
        for line, text in joined:
            hits += [(line, _excerpt(text, m.start(), m.end())) for m in pattern.finditer(" ".join(text.split()))
                     if m.group(0).strip().lower() not in allowed]
        if len(hits) > budget:
            level = "fail" if len(hits) >= 2 * budget + 1 else "warn"
            for line, text in hits:
                add(level, f"{rule} ({len(hits)} on the page, budget {budget})", line, text)

    for tag, line, text in blocks:
        if not text:
            continue
        if tag in ACTIONS and text.lower().strip(" .→>") in BUTTON_BANNED:
            add("fail", "vague action label", line, text)
        if tag in HEADINGS:
            if text.endswith(".") and not text.endswith("..."):
                add("fail", "heading ends with a full stop", line, text)
            if tag in {"h1", "h2"} and text.endswith("?"):
                add("fail", "headline posed as a question", line, text)
            if tag == "h1" and text.lower().startswith("welcome to"):
                add("fail", "welcome headline", line, text)
            if NUMBER_PAIR.match(text):
                add("warn", "number-pair heading", line, text)
            letters = re.sub(r"[^A-Za-z ]", "", text)
            if len(letters.split()) >= 2 and letters.isupper():
                add("fail", "heading in capitals", line, text)
    found.sort(key=lambda f: (f["file"], f["line"], f["level"]))
    return found


def files(paths: list[str]) -> list[Path]:
    out: list[Path] = []
    for raw in paths:
        p = Path(raw)
        if p.is_dir():
            out += sorted(f for f in p.rglob("*") if f.is_file() and f.suffix.lower() in SUFFIXES)
        elif p.is_file():
            out.append(p)
        else:
            raise FileNotFoundError(raw)
    return out


def cmd_copylint(args) -> int:
    try:
        targets = files(args.paths)
    except FileNotFoundError as missing:
        print(f"copylint: no such file or folder: {missing}", file=sys.stderr)
        return 2
    found = [f for path in targets for f in lint(path, set(args.allow or ()), args.year)]
    fails = sum(f["level"] == "fail" for f in found)
    if args.json:
        print(json.dumps({"files": len(targets), "fail": fails, "warn": len(found) - fails, "findings": found}, indent=2))
    else:
        for f in found:
            print(f"{f['level'].upper():4} {f['file']}:{f['line']}  {f['rule']}: {f['text']}")
        print(f"copylint: {len(targets)} file(s), {fails} fail, {len(found) - fails} warn")
    return 1 if fails else 0


def _arguments(p: argparse.ArgumentParser) -> None:
    p.add_argument("paths", nargs="+", help="HTML, Markdown or text files, or folders")
    p.add_argument("--allow", action="append", metavar="WORD", help="client's own word to exempt (repeatable)")
    p.add_argument("--year", type=int, help="current year for the copyright check (default: today)")
    p.add_argument("--json", action="store_true", help="machine-readable output")


def register(sub):
    p = sub.add_parser("copylint", help="Flag generic page copy: banned words, stock lines, over-used devices")
    _arguments(p)
    p.set_defaults(func=cmd_copylint)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="copylint", description=__doc__.split("\n\n")[0])
    _arguments(p)
    try:
        args = p.parse_args(argv)
    except SystemExit as exit_:
        return int(exit_.code or 0) and 2
    return cmd_copylint(args)


if __name__ == "__main__":
    sys.exit(main())
