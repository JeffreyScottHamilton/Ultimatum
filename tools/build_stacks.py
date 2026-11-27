#!/usr/bin/env python3
"""Build Ultimatum's own stack guideline tables: plugins/ultimatum/data/design-own/stacks/<stack>.csv.

Rows are written by hand, in our own words, from each framework's official docs, in
tools/stack_rows/<stack>.json:

    {"applies": "react 19", "base": "https://react.dev", "rows": [[Category, Guideline, Description,
      Do, Don't, Code Good, Code Bad, Severity, Docs URL or path under base, optional Applies To], ...]}

A Docs URL that does not start with https:// is joined to "base". The build fails on a
non-https URL, on a host outside the stack's allow-list (HOSTS below), on an empty cell, on a
bad severity, or on a duplicate guideline.

    python3 tools/build_stacks.py            # check every stack, write the CSVs
    python3 tools/build_stacks.py --check    # exit 1 if any CSV is out of date

Standard library only; no network.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "tools" / "stack_rows"
OUT = ROOT / "plugins" / "ultimatum" / "data" / "design-own" / "stacks"

COLS = ("Category", "Guideline", "Description", "Do", "Don't", "Code Good", "Code Bad", "Severity",
        "Docs URL", "Applies To")
SEVERITY = {"Critical", "High", "Medium", "Low"}
STRIPE = "docs.stripe.com"
# Official documentation hosts allowed per stack (framework domain, plus Stripe's docs where the
# stack has a checkout recipe, plus the W3C/MDN web standards for the plain HTML stack).
HOSTS = {
    "astro": {"docs.astro.build", STRIPE},
    "flutter": {"docs.flutter.dev", "api.flutter.dev", "pub.dev"},
    "html-tailwind": {"tailwindcss.com", "www.w3.org", "developer.mozilla.org", STRIPE},
    "nextjs": {"nextjs.org", STRIPE},
    "nuxtjs": {"nuxt.com", "image.nuxt.com", "fonts.nuxt.com", "scripts.nuxt.com", STRIPE},
    "react-native": {"reactnative.dev"},
    "react": {"react.dev", STRIPE},
    "shadcn": {"ui.shadcn.com"},
    "svelte": {"svelte.dev", STRIPE},
    "swiftui": {"developer.apple.com"},
    "threejs": {"threejs.org"},
    "vue": {"vuejs.org", "router.vuejs.org", "pinia.vuejs.org", STRIPE},
}


def load(stack: str, path: Path) -> tuple[list[dict], list[str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    base, applies = data.get("base", ""), data["applies"]
    rows, errs, seen = [], [], set()
    for i, raw in enumerate(data["rows"], 1):
        where = f"{stack} row {i}"
        if len(raw) not in (9, 10):
            errs.append(f"{where}: needs 9 or 10 cells, has {len(raw)}")
            continue
        cells = list(raw) + ([applies] if len(raw) == 9 else [])
        row = dict(zip(COLS, (str(c).strip() for c in cells)))
        empty = [c for c in COLS if not row[c]]
        if empty:
            errs.append(f"{where} ({row['Guideline'] or '?'}): empty {empty}")
            continue
        if row["Severity"] not in SEVERITY:
            errs.append(f"{where}: Severity must be one of {sorted(SEVERITY)}")
        url = row["Docs URL"]
        if not url.startswith("https://"):
            if url.startswith("http://") or "://" in url:
                errs.append(f"{where}: Docs URL must be https: {url}")
                continue
            url = base + url.lstrip("/") if base.endswith("#") else base.rstrip("/") + "/" + url.lstrip("/")
        host = urlparse(url).hostname or ""
        if urlparse(url).scheme != "https" or host not in HOSTS[stack]:
            errs.append(f"{where}: doc host {host!r} is not allowed for {stack} ({sorted(HOSTS[stack])})")
        row["Docs URL"] = url
        key = row["Guideline"].lower()
        if key in seen:
            errs.append(f"{where}: duplicate guideline {row['Guideline']!r}")
        seen.add(key)
        rows.append(row)
    return rows, errs


# Same ten columns, written in our own order (the readers look columns up by name).
OUT_COLS = ("Category", "Guideline", "Applies To", "Severity", "Description", "Docs URL", "Do", "Don't",
            "Code Good", "Code Bad")


def render(rows: list[dict]) -> str:
    buf = io.StringIO(newline="")
    w = csv.DictWriter(buf, OUT_COLS, lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="exit 1 if a CSV differs from its rows")
    a = ap.parse_args()
    bad, total = 0, 0
    files = sorted(SRC.glob("*.json"))
    for stack in HOSTS:
        if not (SRC / f"{stack}.json").is_file():
            print(f"missing rows file for {stack}")
            bad += 1
    for path in files:
        stack = path.stem
        if stack not in HOSTS:
            print(f"{path.name}: no host allow-list for this stack")
            bad += 1
            continue
        rows, errs = load(stack, path)
        for e in errs:
            print(e)
        bad += len(errs)
        total += len(rows)
        if errs:
            continue
        text, out = render(rows), OUT / f"{stack}.csv"
        if a.check:
            if not out.is_file() or out.read_text(encoding="utf-8") != text:
                print(f"{out.name} is out of date: run tools/build_stacks.py")
                bad += 1
        else:
            OUT.mkdir(parents=True, exist_ok=True)
            out.write_text(text, encoding="utf-8")
            print(f"wrote {out.relative_to(ROOT)} ({len(rows)} rows)")
    if bad:
        print(f"{bad} problem(s)")
        return 1
    if a.check:
        print(f"stack tables are up to date ({total} rows)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
