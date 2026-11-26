#!/usr/bin/env python3
"""Build Ultimatum's own UX guideline table: plugins/ultimatum/data/design-own/ux-guidelines.csv.

Rows are written by hand, in our own words, in tools/ux_rows/*.json. Each row is a list:
[Category, Issue, Platform, Severity, WCAG, Description, Do, Don't, Code Example Good,
 Code Example Bad, Docs URL]. Docs URL may be "" when WCAG names a success criterion; the
builder then links that criterion's Understanding page. This script checks each row and
writes the CSV.

    python3 tools/build_ux.py                      # check all parts, write the CSV
    python3 tools/build_ux.py --check              # exit 1 if the CSV is out of date
    python3 tools/build_ux.py --validate FILE ...  # check some parts only, write nothing

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

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "tools" / "ux_rows"
OUT = ROOT / "plugins" / "ultimatum" / "data" / "design-own" / "ux-guidelines.csv"

COLS = ("Category", "Issue", "Platform", "Description", "Do", "Don't", "Code Example Good",
        "Code Example Bad", "Severity", "WCAG", "Docs URL")
ROW = ("Category", "Issue", "Platform", "Severity", "WCAG", "Description", "Do", "Don't",
       "Code Example Good", "Code Example Bad", "Docs URL")
PLATFORMS = {"All", "Web", "Mobile", "VisionOS"}
SEVERITIES = {"Critical", "High", "Medium", "Low"}
UNDERSTANDING = "https://www.w3.org/WAI/WCAG22/Understanding/"

# Every success criterion in WCAG 2.2 (4.1.1 Parsing was removed in 2.2), with the slug of
# its Understanding page. A row may cite only these.
SC = {
    "1.1.1": "non-text-content", "1.2.1": "audio-only-and-video-only-prerecorded",
    "1.2.2": "captions-prerecorded", "1.2.3": "audio-description-or-media-alternative-prerecorded",
    "1.2.4": "captions-live", "1.2.5": "audio-description-prerecorded",
    "1.2.6": "sign-language-prerecorded", "1.2.7": "extended-audio-description-prerecorded",
    "1.2.8": "media-alternative-prerecorded", "1.2.9": "audio-only-live",
    "1.3.1": "info-and-relationships", "1.3.2": "meaningful-sequence",
    "1.3.3": "sensory-characteristics", "1.3.4": "orientation", "1.3.5": "identify-input-purpose",
    "1.3.6": "identify-purpose", "1.4.1": "use-of-color", "1.4.2": "audio-control",
    "1.4.3": "contrast-minimum", "1.4.4": "resize-text", "1.4.5": "images-of-text",
    "1.4.6": "contrast-enhanced", "1.4.7": "low-or-no-background-audio",
    "1.4.8": "visual-presentation", "1.4.9": "images-of-text-no-exception", "1.4.10": "reflow",
    "1.4.11": "non-text-contrast", "1.4.12": "text-spacing", "1.4.13": "content-on-hover-or-focus",
    "2.1.1": "keyboard", "2.1.2": "no-keyboard-trap", "2.1.3": "keyboard-no-exception",
    "2.1.4": "character-key-shortcuts", "2.2.1": "timing-adjustable", "2.2.2": "pause-stop-hide",
    "2.2.3": "no-timing", "2.2.4": "interruptions", "2.2.5": "re-authenticating",
    "2.2.6": "timeouts", "2.3.1": "three-flashes-or-below-threshold", "2.3.2": "three-flashes",
    "2.3.3": "animation-from-interactions", "2.4.1": "bypass-blocks", "2.4.2": "page-titled",
    "2.4.3": "focus-order", "2.4.4": "link-purpose-in-context", "2.4.5": "multiple-ways",
    "2.4.6": "headings-and-labels", "2.4.7": "focus-visible", "2.4.8": "location",
    "2.4.9": "link-purpose-link-only", "2.4.10": "section-headings",
    "2.4.11": "focus-not-obscured-minimum", "2.4.12": "focus-not-obscured-enhanced",
    "2.4.13": "focus-appearance", "2.5.1": "pointer-gestures", "2.5.2": "pointer-cancellation",
    "2.5.3": "label-in-name", "2.5.4": "motion-actuation", "2.5.5": "target-size-enhanced",
    "2.5.6": "concurrent-input-mechanisms", "2.5.7": "dragging-movements",
    "2.5.8": "target-size-minimum", "3.1.1": "language-of-page", "3.1.2": "language-of-parts",
    "3.1.3": "unusual-words", "3.1.4": "abbreviations", "3.1.5": "reading-level",
    "3.1.6": "pronunciation", "3.2.1": "on-focus", "3.2.2": "on-input",
    "3.2.3": "consistent-navigation", "3.2.4": "consistent-identification",
    "3.2.5": "change-on-request", "3.2.6": "consistent-help", "3.3.1": "error-identification",
    "3.3.2": "labels-or-instructions", "3.3.3": "error-suggestion",
    "3.3.4": "error-prevention-legal-financial-data", "3.3.5": "help",
    "3.3.6": "error-prevention-all", "3.3.7": "redundant-entry",
    "3.3.8": "accessible-authentication-minimum", "3.3.9": "accessible-authentication-enhanced",
    "4.1.2": "name-role-value", "4.1.3": "status-messages",
}
# Habits the anti-generic lint bans; a Do or a good example must never recommend one.
BANNED = ("purple-to-blue gradient", "add a glow", "sparkle", "lorem ipsum", "welcome to",
          "seamless", "elevate", "fade in on scroll", "eyebrow label above every")


def problems(raw, src: str) -> tuple[dict | None, list[str]]:
    if not isinstance(raw, list) or len(raw) != len(ROW):
        return None, [f"{src}: each row needs {len(ROW)} items: {', '.join(ROW)}"]
    row = {k: " ".join(str(v).split()) for k, v in zip(ROW, raw)}
    name = f"{src}: {row['Category']} / {row['Issue']}"
    out = []
    for k in ROW:
        if not row[k] and k != "Docs URL":
            out.append(f"{name}: empty {k}")
    if row["Platform"] not in PLATFORMS:
        out.append(f"{name}: Platform must be one of {sorted(PLATFORMS)}")
    if row["Severity"] not in SEVERITIES:
        out.append(f"{name}: Severity must be one of {sorted(SEVERITIES)}")
    scs = [] if row["WCAG"] == "-" else [s.strip() for s in row["WCAG"].split(",")]
    for s in scs:
        if s not in SC:
            out.append(f"{name}: {s!r} is not a WCAG 2.2 success criterion")
    if not row["Docs URL"] and scs and scs[0] in SC:
        row["Docs URL"] = f"{UNDERSTANDING}{SC[scs[0]]}.html"
    if not row["Docs URL"].startswith("https://"):
        out.append(f"{name}: Docs URL must be https (or give a WCAG criterion)")
    if row["Do"] == row["Don't"]:
        out.append(f"{name}: Do and Don't are the same")
    if row["Code Example Good"] == row["Code Example Bad"]:
        out.append(f"{name}: good and bad examples are the same")
    for k in ("Do", "Code Example Good"):
        low = row[k].lower()
        out.extend(f"{name}: {k} recommends a lint-banned habit: {b!r}" for b in BANNED if b in low)
    return (None if out else row), out


def load(paths: list[Path]) -> tuple[list[dict], list[str]]:
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
            row, e = problems(item, p.name)
            errs.extend(e)
            if row:
                rows.append(row)
    keys = [(r["Category"], r["Issue"]) for r in rows]
    errs.extend(f"duplicate row: {k}" for k in sorted({k for k in keys if keys.count(k) > 1}))
    return rows, errs


def build(rows: list[dict]) -> str:
    buf = io.StringIO()
    w = csv.DictWriter(buf, COLS, lineterminator="\n")
    w.writeheader()
    for r in sorted(rows, key=lambda r: (r["Category"].lower(), r["Issue"].lower())):
        w.writerow({c: r[c] for c in COLS})
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
        print("ux-guidelines.csv is up to date" if same else "ux-guidelines.csv is out of date: run tools/build_ux.py")
        return 0 if same else 1
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(rows)} rows)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
