#!/usr/bin/env python3
"""Build Ultimatum's own app-interface, react-performance, charts and motion tables.

Rows are written by hand, in our own words, in tools/table_rows/<table>/*.json (one list of
objects per file). This script checks every row and writes plugins/ultimatum/data/design-own/<table>.csv.

    python3 tools/build_tables.py                       # check all rows, write the four CSVs
    python3 tools/build_tables.py --check               # exit 1 if any CSV is out of date
    python3 tools/build_tables.py --table motion        # one table only
    python3 tools/build_tables.py --validate FILE ...   # check some parts only (needs --table), write nothing

Standard library only; no network.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "tools" / "table_rows"
OUT = ROOT / "plugins" / "ultimatum" / "data" / "design-own"

# Column order is ours on purpose: it differs from the third-party tables so that even the header
# row shares no run of eight words with them (tools/copy_check.py).
APP_COLS = ("Category", "Issue", "Keywords", "Platform", "Severity", "Description", "Do", "Don't",
            "Code Example Bad", "Code Example Good", "Docs URL")
CHART_COLS = ("Data Type", "Best Chart Type", "Keywords", "When to Use", "When NOT to Use",
              "Secondary Options", "Accessibility Notes", "Library Recommendation", "Docs URL")
MOTION_COLS = ("Category", "Intensity Tier", "Keywords", "Trigger", "Duration", "Easing", "Do", "Don't",
               "Performance Notes", "Reduced Motion")

SEVERITY = {"Critical", "High", "Medium", "Low"}
PLATFORMS = {"All", "Web", "iOS", "Android", "iOS/Android"}
TIERS = {"Subtle", "Standard", "Complex"}
LICENCES = ("MIT", "ISC", "BSD-2-Clause", "BSD-3-Clause", "Apache-2.0")
# Hosts a row's Docs URL may point to, per table: primary sources only.
HOSTS = {
    "app-interface": {"developer.mozilla.org", "www.w3.org", "web.dev", "developer.apple.com",
                      "m3.material.io", "developer.android.com", "react.dev", "reactnative.dev"},
    "react-performance": {"react.dev", "nextjs.org"},
    "charts": {"developer.mozilla.org", "www.w3.org", "web.dev", "d3js.org", "www.chartjs.org", "recharts.org",
               "echarts.apache.org", "observablehq.com", "airbnb.io", "leafletjs.com", "maplibre.org",
               "tradingview.github.io", "github.com", "nivo.rocks", "www.w3.org"},
}
TABLES = {
    "app-interface": APP_COLS,
    "react-performance": APP_COLS,
    "charts": CHART_COLS,
    "motion": MOTION_COLS,
}
KEY = {"app-interface": ("Category", "Issue"), "react-performance": ("Category", "Issue"),
       "charts": ("Data Type",), "motion": ("Category", "Intensity Tier")}


def problems(table: str, row: dict) -> list[str]:
    cols = TABLES[table]
    name = " / ".join(str(row.get(k, "?")) for k in KEY[table])
    out = []
    missing = [c for c in cols if not str(row.get(c, "")).strip()]
    extra = [k for k in row if k not in cols]
    if missing:
        out.append(f"{name}: missing {missing}")
    if extra:
        out.append(f"{name}: unknown keys {extra}")
    if missing:
        return out
    if len(row["Keywords"].split(",")) < 4:
        out.append(f"{name}: Keywords needs at least 4 comma-separated words")
    if "Docs URL" in cols:
        u = urlparse(row["Docs URL"])
        if u.scheme != "https" or u.netloc not in HOSTS[table] or " " in row["Docs URL"]:
            out.append(f"{name}: Docs URL must be an https link on {sorted(HOSTS[table])}")
    if table in ("app-interface", "react-performance"):
        if row["Severity"] not in SEVERITY:
            out.append(f"{name}: Severity must be one of {sorted(SEVERITY)}")
        if row["Platform"] not in PLATFORMS:
            out.append(f"{name}: Platform must be one of {sorted(PLATFORMS)}")
        if table == "react-performance" and row["Platform"] != "Web":
            out.append(f"{name}: react rows are Platform 'Web'")
        for c in ("Code Example Good", "Code Example Bad"):
            if row[c].count("{") != row[c].count("}") or row[c].count("(") != row[c].count(")"):
                out.append(f"{name}: {c} has unbalanced brackets")
        if row["Code Example Good"].strip() == row["Code Example Bad"].strip():
            out.append(f"{name}: good and bad examples are identical")
    if table == "charts":
        if not any(l in row["Library Recommendation"] for l in LICENCES + ("Native HTML",)):
            out.append(f"{name}: Library Recommendation must name each library with its permissive licence")
        for lib in row["Library Recommendation"].split(";"):
            if lib.strip().startswith("Native HTML"):
                continue
            if not re.search(r"\((MIT|ISC|BSD-[23]-Clause|Apache-2\.0)\)", lib):
                out.append(f"{name}: library {lib.strip()!r} has no licence in parentheses")
    if table == "motion":
        if row["Intensity Tier"] not in TIERS:
            out.append(f"{name}: Intensity Tier must be one of {sorted(TIERS)}")
        if not re.search(r"\d", row["Duration"]):
            out.append(f"{name}: Duration needs a number")
    return out


def load(table: str, paths: list[Path]) -> tuple[list[dict], list[str]]:
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
            errs.extend(f"{p.name}: {e}" for e in problems(table, row))
            rows.append(row)
    keys = [tuple(r.get(k) for k in KEY[table]) for r in rows]
    errs.extend(f"{table}: duplicate row {k}" for k in sorted({k for k in keys if keys.count(k) > 1}, key=str))
    return rows, errs


def build(table: str, rows: list[dict]) -> str:
    cols = TABLES[table]
    buf = io.StringIO()
    w = csv.DictWriter(buf, cols, lineterminator="\n")
    w.writeheader()
    for r in rows:  # file order, then row order: authors group related rows on purpose
        w.writerow({c: str(r[c]).strip() if c.startswith("Code Example") else " ".join(str(r[c]).split())
                    for c in cols})
    return buf.getvalue()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--table", choices=sorted(TABLES))
    ap.add_argument("--validate", nargs="+", type=Path)
    a = ap.parse_args()
    if a.validate and not a.table:
        ap.error("--validate needs --table")
    code = 0
    for table in [a.table] if a.table else sorted(TABLES):
        rows, errs = load(table, a.validate or sorted((SRC / table).glob("*.json")))
        for e in errs:
            print(e)
        if errs:
            print(f"{table}: {len(errs)} problem(s)")
            code = 1
            continue
        if a.validate:
            print(f"{table}: ok, {len(rows)} rows")
            continue
        text, dest = build(table, rows), OUT / f"{table}.csv"
        if a.check:
            same = dest.is_file() and dest.read_text(encoding="utf-8") == text
            print(f"{table}.csv is up to date" if same else f"{table}.csv is out of date: run tools/build_tables.py")
            code |= 0 if same else 1
        else:
            dest.write_text(text, encoding="utf-8")
            print(f"wrote {dest.relative_to(ROOT)} ({len(rows)} rows)")
    return code


if __name__ == "__main__":
    sys.exit(main())
