#!/usr/bin/env python3
"""Import the UI UX Pro Max design tables into plugins/ultimatum/data/design/.

The tables come from nextlevelbuilder/ui-ux-pro-max-skill (MIT, Copyright (c) 2024
Next Level Builder). They are third-party data, shipped with their licence; see
data/design/NOTICE.md. This script records every change made to them, so the import
can be repeated against a newer upstream commit:

- keep the web-facing tables and 12 stacks; leave out the full Google Fonts and
  Phosphor catalogues (2 MB of lookup data the workflows do not read)
- drop deprecated styles and the bookkeeping columns (row numbers, status, replacements)
- link each product to a landing pattern that exists (upstream names often differ)
- trim cells and rename the two headers that carry check marks

    python3 tools/import_design_data.py PATH/TO/ui-ux-pro-max/data [--commit SHA]
"""
from __future__ import annotations

import argparse
import csv
import difflib
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "plugins" / "ultimatum" / "data" / "design"
TABLES = ("products", "styles", "colors", "typography", "landing", "ui-reasoning", "ux-guidelines",
          "app-interface", "react-performance", "charts", "motion", "icons")
STACKS = ("html-tailwind", "react", "nextjs", "shadcn", "vue", "nuxtjs", "svelte", "astro",
          "threejs", "react-native", "flutter", "swiftui")
DROP = {"No", "Status", "Parent Style ID", "Replacement Domain", "Replacement ID", "Verified At"}
RENAME = {"Light Mode ✓": "Light Mode", "Dark Mode ✓": "Dark Mode"}


def read(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def write(path: Path, rows: list[dict]) -> None:
    cols = [RENAME.get(c, c) for c in rows[0] if c not in DROP]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        out = csv.DictWriter(fh, fieldnames=cols, lineterminator="\n")
        out.writeheader()
        for row in rows:
            out.writerow({RENAME.get(k, k): " ".join((v or "").split()) for k, v in row.items() if k not in DROP})


def link_landing(products: list[dict], landing: list[dict]) -> None:
    """Name the landing pattern a product points at, or leave it blank when none is close."""
    names: dict[str, str] = {}
    for r in landing:
        for alias in [r["Pattern Name"], *(r.get("Aliases") or "").split("|")]:
            if alias.strip():
                names[alias.strip().lower()] = r["Pattern Name"]
    for row in products:
        want = row["Landing Page Pattern"].strip().lower()
        if want.startswith("n/a"):
            row["Landing Pattern Match"] = ""
            continue
        close = difflib.get_close_matches(want, list(names), n=1, cutoff=0.75)
        row["Landing Pattern Match"] = names.get(want) or (names[close[0]] if close else "")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("src", type=Path, help="upstream data/ folder")
    ap.add_argument("--commit", default="", help="upstream commit, recorded in SOURCE.txt")
    args = ap.parse_args(argv)
    tables = {t: read(args.src / f"{t}.csv") for t in TABLES}
    tables["styles"] = [r for r in tables["styles"] if r.get("Status") != "deprecated"]
    link_landing(tables["products"], tables["landing"])
    if OUT.is_dir():
        shutil.rmtree(OUT / "stacks", ignore_errors=True)
    for name, rows in tables.items():
        write(OUT / f"{name}.csv", rows)
    for stack in STACKS:
        write(OUT / "stacks" / f"{stack}.csv", read(args.src / "stacks" / f"{stack}.csv"))
    licence = next((d / "LICENSE" for d in args.src.resolve().parents if (d / "LICENSE").is_file()), None)
    if licence is None:
        raise SystemExit("no upstream LICENSE found above the data folder; the tables cannot ship without it")
    shutil.copy2(licence, OUT / "LICENSE")
    if args.commit:
        (OUT / "SOURCE.txt").write_text(
            f"nextlevelbuilder/ui-ux-pro-max-skill@{args.commit} .claude/skills/ui-ux-pro-max/data\n", encoding="utf-8")
    print(f"wrote {len(tables) + len(STACKS)} tables to {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
