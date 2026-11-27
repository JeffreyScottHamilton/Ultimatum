#!/usr/bin/env python3
"""Build Ultimatum's own landing-pattern table: plugins/ultimatum/data/design-own/landing.csv.

Rows are written by hand, in our own words, in tools/landing_rows/*.json (one list of
objects per file). This script checks every row and writes the CSV.

    python3 tools/build_landing.py            # check all parts, write landing.csv
    python3 tools/build_landing.py --check    # exit 1 if the CSV is out of date

Standard library only.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "tools" / "landing_rows"
OUT = ROOT / "plugins" / "ultimatum" / "data" / "design-own" / "landing.csv"

COLS = ("Pattern Name", "Aliases", "Keywords", "Kind", "Section Order", "Use When", "Primary CTA Placement",
        "Mobile", "Color Strategy", "Accessibility", "Recommended Effects", "Avoid When",
        "Conversion Optimization", "Slop Habits")
KINDS = ("Local", "App", "Marketing")
# Phrases from the anti-generic lint that a row must never recommend (Slop Habits may name them).
BANNED = ("purple-to-blue", "add a glow", "sparkle", "lorem ipsum", "welcome to", "seamless", "elevate",
          "fade in on scroll", "eyebrow label above every")


def problems(row: dict) -> list[str]:
    name = row.get("Pattern Name", "?")
    out = []
    missing = [c for c in COLS if not str(row.get(c, "")).strip()]
    extra = [k for k in row if k not in COLS]
    if missing:
        out.append(f"{name}: missing {missing}")
    if extra:
        out.append(f"{name}: unknown keys {extra}")
    if missing:
        return out
    if row["Kind"] not in KINDS:
        out.append(f"{name}: Kind must be one of {KINDS}")
    if len(row["Keywords"].split(",")) < 5:
        out.append(f"{name}: Keywords needs at least 5 comma-separated words")
    if row["Section Order"].count(" > ") < 3:
        out.append(f"{name}: Section Order needs at least 4 sections joined by ' > '")
    if len([s for s in row["Slop Habits"].split(";") if s.strip()]) < 1:
        out.append(f"{name}: Slop Habits is empty")
    low = " ".join(str(row[c]) for c in COLS if c != "Slop Habits").lower()
    out += [f"{name}: recommends a lint-banned habit: {b!r}" for b in BANNED if b in low]
    return out


def load(paths: list[Path]) -> tuple[list[dict], list[str]]:
    rows, errs = [], []
    for p in paths:
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errs.append(f"{p.name}: not valid JSON: {e}")
            continue
        for row in data:
            errs.extend(f"{p.name}: {e}" for e in problems(row))
            rows.append(row)
    names = [r.get("Pattern Name") for r in rows]
    errs.extend(f"duplicate pattern: {n}" for n in sorted({n for n in names if names.count(n) > 1}))
    if len(rows) < 34 + 7:
        errs.append(f"need at least 41 patterns (34 page patterns plus app ones), have {len(rows)}")
    kinds = {r.get("Kind") for r in rows}
    errs.extend(f"no {k} patterns" for k in KINDS if k not in kinds)
    return rows, errs


def build(rows: list[dict]) -> str:
    buf = io.StringIO()
    w = csv.DictWriter(buf, COLS, lineterminator="\n")
    w.writeheader()
    order = {k: i for i, k in enumerate(KINDS)}
    for r in sorted(rows, key=lambda r: (order[r["Kind"]], r["Pattern Name"].lower())):
        w.writerow({c: " ".join(str(r[c]).split()) for c in COLS})
    return buf.getvalue()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    rows, errs = load(sorted(SRC.glob("*.json")))
    for e in errs:
        print(e)
    if errs:
        print(f"{len(errs)} problem(s)")
        return 1
    text = build(rows)
    if a.check:
        same = OUT.is_file() and OUT.read_text(encoding="utf-8") == text
        print("landing.csv is up to date" if same else "landing.csv is out of date: run tools/build_landing.py")
        return 0 if same else 1
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(rows)} patterns)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
