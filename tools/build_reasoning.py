#!/usr/bin/env python3
"""Build Ultimatum's own reasoning table: plugins/ultimatum/data/design-own/ui-reasoning.csv.

One row per product type in data/design-own/product-types.txt, so `ult design system` can
join it to the product table on UI_Category = Product Type. Rows are written by hand, in our
own words, in tools/reasoning_rows/*.json as lists of seven strings:
[UI_Category, Recommended_Pattern, Style_Priority, Color_Mood, Typography_Mood, Key_Effects,
 Anti_Patterns]. Style_Priority names styles joined by " + "; each must be a Style or an
Alias in data/design-own/styles.csv. Anti_Patterns are joined by " + " too (design.py splits
on it). The build fails on a missing or extra category, an unknown style, or a lint-banned
habit recommended outside Anti_Patterns.

    python3 tools/build_reasoning.py                      # check all parts, write the CSV
    python3 tools/build_reasoning.py --check              # exit 1 if the CSV is out of date
    python3 tools/build_reasoning.py --validate FILE ...  # check some parts only, write nothing

Standard library only; no network.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "tools" / "reasoning_rows"
DATA = ROOT / "plugins" / "ultimatum" / "data" / "design-own"
OUT = DATA / "ui-reasoning.csv"

COLS = ("UI_Category", "Recommended_Pattern", "Style_Priority", "Color_Mood", "Typography_Mood",
        "Key_Effects", "Anti_Patterns")
# Phrases from the anti-generic lint that a row must never recommend (they may be named in Anti_Patterns).
BANNED = ("purple-to-blue gradient", "add a glow", "sparkle", "lorem ipsum", "welcome to",
          "seamless", "elevate", "fade in on scroll", "eyebrow label above every")


def known_styles() -> set[str]:
    names = set()
    with (DATA / "styles.csv").open(encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            names.add(r["Style"])
            names.update(a.strip() for a in r["Aliases"].split("|") if a.strip())
    return names


def categories() -> list[str]:
    return [ln.strip() for ln in (DATA / "product-types.txt").read_text(encoding="utf-8").splitlines() if ln.strip()]


def problems(raw, src: str, styles: set[str]) -> tuple[dict | None, list[str]]:
    if not isinstance(raw, list) or len(raw) != len(COLS):
        return None, [f"{src}: each row needs {len(COLS)} items: {', '.join(COLS)}"]
    row = {k: " ".join(str(v).split()) for k, v in zip(COLS, raw)}
    name = f"{src}: {row['UI_Category']}"
    out = [f"{name}: empty {k}" for k in COLS if not row[k]]
    for s in [s.strip() for s in row["Style_Priority"].split(" + ") if s.strip()]:
        if s not in styles:
            out.append(f"{name}: style {s!r} is not in styles.csv")
    if not 2 <= len(row["Style_Priority"].split(" + ")) <= 3:
        out.append(f"{name}: Style_Priority needs 2 or 3 styles joined by ' + '")
    if len([a for a in row["Anti_Patterns"].split(" + ") if a.strip()]) < 2:
        out.append(f"{name}: Anti_Patterns needs at least 2 items joined by ' + '")
    for k in COLS[:-1]:
        low = row[k].lower()
        out.extend(f"{name}: {k} recommends a lint-banned habit: {b!r}" for b in BANNED if b in low)
    return (None if out else row), out


def load(paths: list[Path], full: bool = True) -> tuple[list[dict], list[str]]:
    styles = known_styles()
    rows, errs = [], []
    for p in paths:
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errs.append(f"{p.name}: not valid JSON: {e}")
            continue
        if not isinstance(data, list):
            errs.append(f"{p.name}: must hold a JSON list of rows")
            continue
        for item in data:
            row, e = problems(item, p.name, styles)
            errs.extend(e)
            if row:
                rows.append(row)
    names = [r["UI_Category"] for r in rows]
    errs.extend(f"duplicate category: {n}" for n in sorted({n for n in names if names.count(n) > 1}))
    if full:
        want = categories()
        errs.extend(f"no row for product type: {c}" for c in want if c not in names)
        errs.extend(f"row for unknown product type: {n}" for n in names if n not in want)
    return rows, errs


def build(rows: list[dict]) -> str:
    order = {c: i for i, c in enumerate(categories())}
    buf = io.StringIO()
    w = csv.DictWriter(buf, COLS, lineterminator="\n")
    w.writeheader()
    for r in sorted(rows, key=lambda r: order.get(r["UI_Category"], 10**6)):
        w.writerow(r)
    return buf.getvalue()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--validate", nargs="+", type=Path)
    a = ap.parse_args()
    rows, errs = load(a.validate or sorted(SRC.glob("*.json")), full=not a.validate)
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
        print("ui-reasoning.csv is up to date" if same else "ui-reasoning.csv is out of date: run tools/build_reasoning.py")
        return 0 if same else 1
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(rows)} rows)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
