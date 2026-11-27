#!/usr/bin/env python3
"""Build Ultimatum's own product table: plugins/ultimatum/data/design-own/products.csv.

Rows are written by hand, in our own words, in tools/product_rows/*.json. Each file holds
{"defaults": {...}, "rows": [[name, keywords, considerations, {overrides}], ...]}: a family's
shared answers and one row per business or product type. Short keys: s primary style,
x secondary styles, l landing pattern, d dashboard style, c colour focus, a main action,
t trust signals, b booking or quote.

The build fails unless every name in data/design-own/product-types.txt (and, while it ships,
every Product Type in data/design/products.csv) has a row, every style named exists in
design-own/styles.csv, and every landing pattern named exists in design-own/landing.csv.

    python3 tools/build_products.py          # check all parts, write products.csv
    python3 tools/build_products.py --check  # exit 1 if the CSV is out of date

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
SRC = ROOT / "tools" / "product_rows"
DATA = ROOT / "plugins" / "ultimatum" / "data"
OWN = DATA / "design-own"
OUT = OWN / "products.csv"

# Column order matters to the copy check: our own columns sit between the borrowed names so the
# header never repeats their column run.
COLS = ("Product Type", "Keywords", "Main Action", "Primary Style Recommendation", "Landing Page Pattern",
        "Landing Pattern Match", "Secondary Styles", "Trust Signals", "Dashboard Style (if applicable)",
        "Color Palette Focus", "Booking/Quote", "Key Considerations")
KEYS = {"s": "Primary Style Recommendation", "x": "Secondary Styles", "l": "Landing Page Pattern",
        "d": "Dashboard Style (if applicable)", "c": "Color Palette Focus", "a": "Main Action",
        "t": "Trust Signals", "b": "Booking/Quote"}
BANNED = ("purple-to-blue", "add a glow", "sparkle", "lorem ipsum", "welcome to", "seamless", "elevate",
          "fade in on scroll", "eyebrow label above every")


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def style_names() -> set[str]:
    out = set()
    for r in read_csv(OWN / "styles.csv"):
        out.add(r["Style"].strip().lower())
        out.update(a.strip().lower() for a in r["Aliases"].split("|") if a.strip())
    return out


def expected_names() -> set[str]:
    names = {l.strip() for l in (OWN / "product-types.txt").read_text(encoding="utf-8").splitlines() if l.strip()}
    theirs = DATA / "design" / "products.csv"
    if theirs.is_file():
        names |= {r["Product Type"] for r in read_csv(theirs)}
    return names


def load(paths: list[Path]) -> tuple[list[dict], list[str]]:
    rows, errs = [], []
    for p in paths:
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errs.append(f"{p.name}: not valid JSON: {e}")
            continue
        base = {KEYS[k]: v for k, v in data["defaults"].items()}
        for item in data["rows"]:
            name, kw, why, over = (item + [{}])[:4]
            row = dict(base)
            row.update({KEYS[k]: v for k, v in over.items()})
            row.update({"Product Type": name, "Keywords": kw, "Key Considerations": why})
            row["Landing Pattern Match"] = row["Landing Page Pattern"]
            rows.append(row)
    return rows, errs


def check(rows: list[dict]) -> list[str]:
    errs = []
    styles = style_names()
    landing = {r["Pattern Name"] for r in read_csv(OWN / "landing.csv")}
    names = [r["Product Type"] for r in rows]
    errs += [f"duplicate product: {n}" for n in sorted({n for n in names if names.count(n) > 1})]
    want = expected_names()
    errs += [f"no row for: {n}" for n in sorted(want - set(names))]
    errs += [f"unexpected row: {n}" for n in sorted(set(names) - want)]
    for r in rows:
        n = r["Product Type"]
        blanks = [c for c in COLS if not str(r.get(c, "")).strip()]
        if blanks:
            errs.append(f"{n}: empty {blanks}")
            continue
        named = re.split(r"\s\+\s", r["Primary Style Recommendation"]) + [s.strip() for s in r["Secondary Styles"].split(",")]
        errs += [f"{n}: unknown style {s!r}" for s in named if s.strip().lower() not in styles]
        if r["Landing Pattern Match"] not in landing:
            errs.append(f"{n}: unknown landing pattern {r['Landing Pattern Match']!r}")
        if len(r["Keywords"].split(",")) < 5:
            errs.append(f"{n}: Keywords needs at least 5 comma-separated words")
        low = " ".join(str(r[c]) for c in COLS).lower()
        errs += [f"{n}: recommends a lint-banned habit: {b!r}" for b in BANNED if b in low]
    return errs


def build(rows: list[dict]) -> str:
    buf = io.StringIO()
    w = csv.DictWriter(buf, COLS, lineterminator="\n")
    w.writeheader()
    for r in sorted(rows, key=lambda r: r["Product Type"].lower()):
        w.writerow({c: " ".join(str(r[c]).split()) for c in COLS})
    return buf.getvalue()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    rows, errs = load(sorted(SRC.glob("*.json")))
    errs += check(rows)
    for e in errs:
        print(e)
    if errs:
        print(f"{len(errs)} problem(s)")
        return 1
    text = build(rows)
    if a.check:
        same = OUT.is_file() and OUT.read_text(encoding="utf-8") == text
        print("products.csv is up to date" if same else "products.csv is out of date: run tools/build_products.py")
        return 0 if same else 1
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(rows)} product types)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
