#!/usr/bin/env python3
"""Pick a base path for a vague UI complaint.

  vague_path.py match "the menu is confusing on my phone" [--json]
  vague_path.py list
  vague_path.py check          every route file exists, at most four questions per area
  vague_path.py --self-check

Reads vague-paths.csv next to this script. Standard library only, no network.
Exit codes: 0 a path was found (or check passed), 4 no area matched (ask which
area), 1 check failed, 2 bad usage.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLUGIN = HERE.parents[2]
TABLE = HERE / "vague-paths.csv"
MAX_QUESTIONS = 4
GENERIC = "ux"


def load(path: Path = TABLE) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["words"] = [w.strip().lower() for w in r["words"].split("|") if w.strip()]
        r["ask"] = [q.strip() for q in r["ask"].split("|") if q.strip()]
        r["routes"] = [tuple(x.strip() for x in part.split("=>", 1)) for part in r["routes"].split(" ; ") if "=>" in part]
    return rows


def score(text: str, row: dict) -> int:
    t = " " + re.sub(r"[^a-z0-9' -]+", " ", text.lower()) + " "
    hits = 0
    for w in row["words"]:
        if re.search(r"(?<![a-z])" + re.escape(w) + r"(?![a-z])", t):
            hits += 2 if " " in w else 1  # a phrase is stronger evidence than one word
    return hits


def match(text: str, rows: list[dict]) -> list[tuple[int, dict]]:
    # On a tie the specific area wins over the catch-all "ux".
    ranked = sorted(((score(text, r), r) for r in rows), key=lambda x: (-x[0], x[1]["area"] == GENERIC))
    return [(s, r) for s, r in ranked if s > 0]


def show(text: str, rows: list[dict], as_json: bool) -> int:
    found = match(text, rows)
    if not found:
        msg = {"area": None, "ask": ["Which area is it about? " + ", ".join(r["area"] for r in rows)]}
        print(json.dumps(msg, indent=2) if as_json else msg["ask"][0])
        return 4
    best = found[0][1]
    also = [r["area"] for s, r in found[1:3] if s >= found[0][0] / 2]
    out = {"area": best["area"], "also": also, "ask": best["ask"],
           "routes": [{"if": c, "read": p} for c, p in best["routes"]],
           "first_check": best["first_check"], "fallback": best["fallback"]}
    if as_json:
        print(json.dumps(out, indent=2))
        return 0
    print(f"area: {out['area']}" + (f" (also: {', '.join(also)})" if also else ""))
    print("ask in one message, skip what the context answers:")
    for q in out["ask"]:
        print(f"  - {q}")
    print("then read, by answer:")
    for c, p in best["routes"]:
        print(f"  {c}: {p}")
    print(f"measure first: {out['first_check']}")
    print(f"if the user says 'you decide': {out['fallback']}")
    return 0


def check(rows: list[dict]) -> list[str]:
    errs, seen = [], set()
    for r in rows:
        a = r["area"]
        if a in seen:
            errs.append(f"{a}: area listed twice")
        seen.add(a)
        if not r["words"]:
            errs.append(f"{a}: no trigger words")
        if not 1 <= len(r["ask"]) <= MAX_QUESTIONS:
            errs.append(f"{a}: {len(r['ask'])} questions, want 1 to {MAX_QUESTIONS}")
        if not r["routes"]:
            errs.append(f"{a}: no routes")
        for cue, path in r["routes"]:
            if not (PLUGIN / path).is_file():
                errs.append(f"{a}: route '{cue}' points to missing {path}")
        for key in ("first_check", "fallback"):
            if not r[key].strip():
                errs.append(f"{a}: empty {key}")
    return errs


def self_check() -> int:
    rows = load()
    cases = {
        "the menu is confusing, people get lost": "navigation",
        "it looks cheap": "looks",
        "our signup form is too long": "flows",
        "it looks AI-made and generic": "identity-existing",
        "the error message wording is off": "copy",
        "the page takes forever to load": "speed",
        "it breaks on small screens": "mobile",
        "the menu is confusing on my phone": "navigation",
    }
    bad = 0
    for text, want in cases.items():
        got = match(text, rows)
        area = got[0][1]["area"] if got else None
        if area != want:
            print(f"FAIL {text!r}: got {area}, want {want}")
            bad += 1
    if match("hello there", rows):
        print("FAIL a sentence with no complaint matched an area")
        bad += 1
    errs = check(rows)
    for e in errs:
        print(f"FAIL {e}")
    bad += len(errs)
    print("self-check ok" if not bad else f"self-check: {bad} failure(s)")
    return 1 if bad else 0


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    if argv == ["--self-check"]:
        return self_check()
    ap = argparse.ArgumentParser(description="Pick a base path for a vague UI complaint.")
    sub = ap.add_subparsers(dest="cmd")
    m = sub.add_parser("match")
    m.add_argument("text", nargs="+")
    m.add_argument("--json", action="store_true")
    sub.add_parser("list")
    sub.add_parser("check")
    try:
        args = ap.parse_args(argv)
    except SystemExit:
        return 2
    if not args.cmd:
        ap.print_usage()
        return 2
    rows = load()
    if args.cmd == "match":
        return show(" ".join(args.text), rows, args.json)
    if args.cmd == "list":
        for r in rows:
            print(f"{r['area']}: {', '.join(r['words'][:5])}")
        return 0
    errs = check(rows)
    for e in errs:
        print(e)
    print(f"{len(rows)} areas, {len(errs)} problem(s)")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
