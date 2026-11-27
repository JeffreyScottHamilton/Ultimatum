#!/usr/bin/env python3
"""Check an MCP question-and-answer eval file for shape problems before anyone runs it.

File shape (see mcp-eval-set.md):
  <evaluation><qa_pair><question>...</question><answer>...</answer></qa_pair>...</evaluation>

Usage: mcp_eval_check.py FILE.xml [--count 10] [--max-answer 80] [--json]
       mcp_eval_check.py --self-check
Exit: 0 clean (warnings allowed), 1 errors, 2 bad usage or unreadable file.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET

# Verbs that suggest the question needs a write to answer; the set must be read-only.
WRITE_HINTS = re.compile(r"\b(create|delete|remove|update|edit|send|post|merge|close|archive|rename|move)\b", re.I)
RELATIVE_TIME = re.compile(r"\b(today|yesterday|this week|currently|right now|latest|most recent)\b", re.I)


def check(text: str, count: int, max_answer: int) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    # Entity declarations are refused outright: the file is untrusted input.
    if re.search(r"<!DOCTYPE|<!ENTITY", text, re.I):
        return {"errors": ["DOCTYPE or ENTITY declarations are not allowed"], "warnings": [], "pairs": 0}
    try:
        root = ET.fromstring(text)
    except ET.ParseError as exc:
        return {"errors": [f"not well-formed XML: {exc}"], "warnings": [], "pairs": 0}
    if root.tag != "evaluation":
        errors.append(f"root element is <{root.tag}>, expected <evaluation>")
    pairs = root.findall("qa_pair")
    if len(pairs) != count:
        errors.append(f"{len(pairs)} qa_pair elements, expected {count}")
    seen: dict[str, int] = {}
    for n, p in enumerate(pairs, 1):
        q = (p.findtext("question") or "").strip()
        a = (p.findtext("answer") or "").strip()
        if not q:
            errors.append(f"pair {n}: empty question")
        if not a:
            errors.append(f"pair {n}: empty answer")
        if len(a) > max_answer:
            errors.append(f"pair {n}: answer is {len(a)} characters; it should be one short value that compares as a string")
        if q:
            key = re.sub(r"\W+", " ", q.lower()).strip()
            if key in seen:
                errors.append(f"pair {n}: same question as pair {seen[key]}")
            seen.setdefault(key, n)
            if WRITE_HINTS.search(q):
                warnings.append(f"pair {n}: question mentions `{WRITE_HINTS.search(q).group(0)}`; answering must not need a write")
            if RELATIVE_TIME.search(q):
                warnings.append(f"pair {n}: `{RELATIVE_TIME.search(q).group(0)}` makes the answer drift over time")
            if not re.search(r"\b(format|answer with|give the|as a|in the form)\b", q, re.I):
                warnings.append(f"pair {n}: question does not say what form the answer takes")
    return {"errors": errors, "warnings": warnings, "pairs": len(pairs)}


def self_check() -> int:
    good = "<evaluation>" + "".join(
        f"<qa_pair><question>Which label is on issue {i} that also links PR {i + 1}? Answer with the label name.</question>"
        f"<answer>bug-{i}</answer></qa_pair>" for i in range(10)) + "</evaluation>"
    assert check(good, 10, 80) == {"errors": [], "warnings": [], "pairs": 10}, check(good, 10, 80)
    bad = ("<evaluation><qa_pair><question>Delete the latest branch</question><answer></answer></qa_pair>"
           "<qa_pair><question>delete the latest branch!</question><answer>x</answer></qa_pair></evaluation>")
    out = check(bad, 10, 80)
    assert len(out["errors"]) == 3, out          # count, empty answer, duplicate
    assert len(out["warnings"]) == 6, out        # write verb, drift, no format, for both pairs
    assert check('<!DOCTYPE x [<!ENTITY a "b">]><evaluation/>', 10, 80)["errors"][0].startswith("DOCTYPE")
    assert check("<evaluation>", 10, 80)["errors"][0].startswith("not well-formed")
    print("self-check passed: 4 files")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("file", nargs="?")
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--max-answer", type=int, default=80)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args(argv)
    if args.self_check:
        return self_check()
    if not args.file:
        parser.print_usage(sys.stderr)
        return 2
    try:
        with open(args.file, encoding="utf-8") as fh:
            text = fh.read()
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    out = check(text, args.count, args.max_answer)
    if args.json:
        print(json.dumps(out, indent=2))
    else:
        print(f"{out['pairs']} pairs")
        for e in out["errors"]:
            print(f"error: {e}")
        for w in out["warnings"]:
            print(f"warn:  {w}")
    return 1 if out["errors"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
