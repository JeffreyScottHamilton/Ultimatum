#!/usr/bin/env python3
"""Build Ultimatum's own style table: plugins/ultimatum/data/design-own/styles.csv.

Rows are written by hand, in our own words, in tools/style_rows/*.json (one list of
objects per file). This script checks every row and writes the CSV.

    python3 tools/build_styles.py                      # check all parts, write styles.csv
    python3 tools/build_styles.py --check              # exit 1 if the CSV is out of date
    python3 tools/build_styles.py --validate FILE ...  # check some parts only, write nothing

Standard library only.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "tools" / "style_rows"
OUT = ROOT / "plugins" / "ultimatum" / "data" / "design-own" / "styles.csv"

COLS = ("Style", "Aliases", "Type", "Keywords", "Looks Like", "Use When", "Avoid When", "Palette",
        "Type Approach", "Layout", "Motion", "Slop Habits", "Accessibility", "Performance", "Mode",
        "Effort", "Tokens", "CSS Starter", "Checklist")
TYPES = {"General", "Dashboard", "Mobile", "Design System", "Local"}
MODES = {"light-first", "dark-first", "both"}
LEVELS = {"low", "medium", "high"}
HEX = re.compile(r"#[0-9A-Fa-f]{6}\b")
TOKEN = re.compile(r"^--[a-z0-9-]+: [^,]+$")
# Phrases from the anti-generic lint that a style row must never recommend.
BANNED = ("purple-to-blue gradient", "add a glow", "sparkle", "lorem ipsum", "welcome to",
          "seamless", "elevate", "fade in on scroll", "eyebrow label above every")


def problems(row: dict) -> list[str]:
    name = row.get("Style", "?")
    out = []
    missing = [c for c in COLS if not str(row.get(c, "")).strip()]
    extra = [k for k in row if k not in COLS]
    if missing:
        out.append(f"{name}: missing {missing}")
    if extra:
        out.append(f"{name}: unknown keys {extra}")
    if missing:
        return out
    if row["Type"] not in TYPES:
        out.append(f"{name}: Type must be one of {sorted(TYPES)}")
    if row["Mode"] not in MODES:
        out.append(f"{name}: Mode must be one of {sorted(MODES)}")
    if row["Effort"] not in LEVELS:
        out.append(f"{name}: Effort must be low, medium or high")
    if not re.match(r"^(low|medium|high): \S", row["Performance"]):
        out.append(f"{name}: Performance must start 'low: ', 'medium: ' or 'high: '")
    if len(HEX.findall(row["Palette"])) < 3:
        out.append(f"{name}: Palette needs at least 3 hex colours (#RRGGBB)")
    toks = [t.strip() for t in row["Tokens"].split(", ") if t.strip()]
    if not 5 <= len(toks) <= 10 or not all(TOKEN.match(t) for t in toks):
        out.append(f"{name}: Tokens must be 5-10 '--name: value' items separated by ', '")
    if len([s for s in row["Slop Habits"].split(";") if s.strip()]) < 2:
        out.append(f"{name}: Slop Habits needs at least 2 items separated by ';'")
    if len([s for s in row["Checklist"].split(";") if s.strip()]) < 3:
        out.append(f"{name}: Checklist needs at least 3 items separated by ';'")
    css = row["CSS Starter"]
    if css.count("{") != css.count("}") or ":" not in css or ";" not in css:
        out.append(f"{name}: CSS Starter must be valid-looking CSS with braces balanced")
    if len(row["Keywords"].split(",")) < 5:
        out.append(f"{name}: Keywords needs at least 5 comma-separated words")
    low = " ".join(str(row[c]) for c in COLS if c != "Slop Habits").lower()
    for bad in BANNED:
        if bad in low:
            out.append(f"{name}: recommends a lint-banned habit: {bad!r}")
    return out


def load(paths: list[Path]) -> tuple[list[dict], list[str]]:
    rows, errs = [], []
    for p in paths:
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errs.append(f"{p.name}: not valid JSON: {e}")
            continue
        if not isinstance(data, list):
            errs.append(f"{p.name}: must hold a JSON list of row objects")
            continue
        for row in data:
            errs.extend(f"{p.name}: {e}" for e in problems(row))
            rows.append(row)
    names = [r.get("Style") for r in rows]
    errs.extend(f"duplicate style: {n}" for n in sorted({n for n in names if names.count(n) > 1}))
    return rows, errs


def build(rows: list[dict]) -> str:
    buf = io.StringIO()
    w = csv.DictWriter(buf, COLS, lineterminator="\n")
    w.writeheader()
    for r in sorted(rows, key=lambda r: (r["Type"] != "General", r["Type"], r["Style"].lower())):
        w.writerow({c: " ".join(str(r[c]).split()) if c != "CSS Starter" else str(r[c]).strip() for c in COLS})
    return buf.getvalue()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--validate", nargs="+", type=Path)
    a = ap.parse_args()
    rows, errs = load(a.validate or sorted(SRC.glob("*.json")))
    for e in errs:
        print(e)
    if errs:
        print(f"{len(errs)} problem(s)")
        return 1
    if a.validate:
        print(f"ok: {len(rows)} rows")
        return 0
    text = build(rows)
    if a.check:
        same = OUT.is_file() and OUT.read_text(encoding="utf-8") == text
        print("styles.csv is up to date" if same else "styles.csv is out of date: run tools/build_styles.py")
        return 0 if same else 1
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(rows)} styles)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
