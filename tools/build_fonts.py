#!/usr/bin/env python3
"""Build plugins/ultimatum/data/design-own/fonts.csv: every family on Google Fonts.

Facts come from Google Fonts' own repository (https://github.com/google/fonts):
each family's METADATA.pb (name, designer, licence, category, styles, axes,
subsets, date added) and the human-assessed tags in tags/all/families.csv
(mood, style and theme scores). The search keywords, the column layout and
the Quality score (mean of the four /Quality tags) are Ultimatum's own.

Get the metadata once with a sparse checkout (only small text files):

    git clone --depth 1 --filter=blob:none --no-checkout https://github.com/google/fonts gf
    git -C gf sparse-checkout set --no-cone '/ofl/*/METADATA.pb' '/apache/*/METADATA.pb' \
        '/ufl/*/METADATA.pb' '/tags/all/*'
    git -C gf checkout main
    python3 tools/build_fonts.py --from gf          # write fonts.csv
    python3 tools/build_fonts.py --check            # validate fonts.csv (no network)

Standard library only. This script never touches the network itself.
"""
from __future__ import annotations

import argparse
import csv
import io
import re
import sys
from collections import defaultdict
from pathlib import Path

OWN = Path(__file__).resolve().parents[1] / "plugins" / "ultimatum" / "data" / "design-own"
OUT = OWN / "fonts.csv"

COLUMNS = ("Family", "Kind", "Keywords", "Mood", "Style Tags", "Weights", "Italic", "Scripts",
           "Primary Script", "Quality", "Axes", "Licence", "Designer", "Added",
           "Specimen URL", "CSS URL")

KIND = {"SANS_SERIF": "sans serif", "SERIF": "serif", "DISPLAY": "display",
        "HANDWRITING": "handwriting", "MONOSPACE": "monospace", "SLAB_SERIF": "slab serif",
        "SYMBOLS": "symbols"}
LICENCES = {"OFL": "OFL-1.1", "APACHE2": "Apache-2.0", "UFL": "UFL-1.0"}
# Subsets folded into one readable script name; "-ext" variants and "menu" add nothing for choosing.
SCRIPT = {"latin": "Latin", "cyrillic": "Cyrillic", "greek": "Greek", "vietnamese": "Vietnamese",
          "arabic": "Arabic", "hebrew": "Hebrew", "devanagari": "Devanagari", "thai": "Thai",
          "japanese": "Japanese", "korean": "Korean", "chinese-simplified": "Chinese (Simplified)",
          "chinese-traditional": "Chinese (Traditional)", "chinese-hongkong": "Chinese (Hong Kong)",
          "bengali": "Bengali", "tamil": "Tamil", "telugu": "Telugu", "gujarati": "Gujarati",
          "gurmukhi": "Gurmukhi", "kannada": "Kannada", "malayalam": "Malayalam", "khmer": "Khmer",
          "sinhala": "Sinhala", "ethiopic": "Ethiopic", "georgian": "Georgian", "armenian": "Armenian",
          "math": "Math", "symbols": "Symbols", "symbols2": "Symbols", "emoji": "Emoji", "music": "Music"}
# Tag groups kept, and the score (0-100) a family needs for the tag to count.
MOOD_MIN, STYLE_MIN = 60, 50
STYLE_GROUPS = ("Sans", "Serif", "Slab", "Script", "Monospace", "Theme", "Seasonal", "Purpose")
# Our own search words per kind, so plain requests ("code font", "wedding script") find families.
KIND_WORDS = {
    "sans serif": "sans clean ui interface body text",
    "serif": "serif editorial book reading text classic",
    "display": "display headline poster decorative",
    "handwriting": "handwriting script hand-drawn signature",
    "monospace": "monospace code terminal developer tabular",
    "slab serif": "slab serif sturdy headline",
    "symbols": "symbols icons dingbats",
}

# Our own everyday words for some style tags, so a request like "wedding invite" finds formal scripts.
STYLE_WORDS = {
    "script: formal": "wedding invitation elegant",
    "serif: didone": "fashion luxury magazine",
    "sans: rounded": "friendly soft kids app",
    "theme: techno": "tech gaming sci-fi",
    "theme: pixel": "retro game 8-bit",
    "theme: blackletter": "gothic medieval tattoo",
    "theme: stencil": "military industrial",
    "theme: woodtype": "western poster",
    "purpose: learn to write": "school education kids",
    "script: handwritten": "personal note",
    "slab: clarendon": "western poster sturdy",
}


def get(text: str, key: str) -> list[str]:
    return re.findall(rf'^{key}: "([^"]*)"', text, re.M)


def parse(text: str) -> dict:
    """The parts of one METADATA.pb we use."""
    styles = re.findall(r'style: "(normal|italic)"\s+weight: (\d+)', text)
    axes = {t: (float(lo), float(hi)) for t, lo, hi in
            re.findall(r'axes \{\s+tag: "(\w+)"\s+min_value: ([\d.-]+)\s+max_value: ([\d.-]+)', text)}
    return {
        "name": get(text, "name")[0],
        "designer": (get(text, "designer") or [""])[0],
        "license": get(text, "license")[0],
        "category": get(text, "category"),
        "stroke": get(text, "stroke"),
        "classes": get(text, "classifications"),
        # Italic-only families (Molle, Miama) list their weights under italic.
        "weights": sorted({int(w) for s, w in styles if s == "normal"} or {int(w) for _, w in styles}),
        "italic_only": bool(styles) and all(s == "italic" for s, _ in styles),
        "italic": any(s == "italic" for s, _ in styles),
        "axes": axes,
        "subsets": get(text, "subsets"),
        "primary": (get(text, "primary_script") or [""])[0],
        "added": (get(text, "date_added") or [""])[0],
    }


def read_tags(path: Path) -> dict[str, dict[str, int]]:
    """family -> tag -> score at the regular instance (else the highest instance score)."""
    regular: dict[str, dict[str, int]] = defaultdict(dict)
    best: dict[str, dict[str, int]] = defaultdict(dict)
    with path.open(encoding="utf-8", newline="") as fh:
        for row in csv.reader(fh):
            if len(row) < 4 or not row[2].startswith("/"):
                continue
            fam, inst, tag = row[0], row[1], row[2]
            try:
                score = int(float(row[3]))
            except ValueError:
                continue
            if inst in ("", "wght@400"):
                regular[fam][tag] = score
            best[fam][tag] = max(score, best[fam].get(tag, 0))
    return {f: best[f] | regular.get(f, {}) for f in best}


def fmt(x: float) -> str:
    return str(int(x)) if x == int(x) else f"{x:g}"


def scripts(subsets: list[str]) -> list[str]:
    seen = []
    for s in subsets:
        base = s.removesuffix("-ext")
        name = SCRIPT.get(base, base.replace("-", " ").title())
        if s != "menu" and name not in seen:
            seen.append(name)
    return seen


def css_url(m: dict) -> str:
    fam = m["name"].replace(" ", "+")
    w = m["axes"].get("wght")
    if w:
        return f"https://fonts.googleapis.com/css2?family={fam}:wght@{fmt(w[0])}..{fmt(w[1])}&display=swap"
    if m["italic_only"]:
        return (f"https://fonts.googleapis.com/css2?family={fam}:ital,wght@"
                + ";".join(f"1,{x}" for x in m["weights"]) + "&display=swap")
    if m["weights"] and m["weights"] != [400]:
        return (f"https://fonts.googleapis.com/css2?family={fam}:wght@"
                + ";".join(map(str, m["weights"])) + "&display=swap")
    return f"https://fonts.googleapis.com/css2?family={fam}&display=swap"


def row(m: dict, tags: dict[str, int]) -> dict:
    kinds = []
    for k in m["category"] + m["stroke"] + m["classes"]:
        if KIND.get(k) and KIND[k] not in kinds:
            kinds.append(KIND[k])
    moods = [t.split("/")[-1].lower() for t, s in sorted(tags.items(), key=lambda kv: -kv[1])
             if t.startswith("/Expressive/") and s >= MOOD_MIN]
    styles = [t.strip("/").replace("/", ": ").lower() for t, s in sorted(tags.items(), key=lambda kv: -kv[1])
              if t.strip("/").split("/")[0] in STYLE_GROUPS and s >= STYLE_MIN]
    quality = [s for t, s in tags.items() if t.startswith("/Quality/")]
    w = m["axes"].get("wght")
    weights = f"{fmt(w[0])}-{fmt(w[1])} variable" if w else ", ".join(map(str, m["weights"]))
    axes = ", ".join(f"{t} {fmt(lo)}-{fmt(hi)}" for t, (lo, hi) in sorted(m["axes"].items()))
    sc = scripts(m["subsets"])
    words = ([KIND_WORDS.get(k, "") for k in kinds] + moods + [s.split(": ")[-1] for s in styles]
             + [STYLE_WORDS.get(s, "") for s in styles])
    if w or len(m["weights"]) >= 4:
        words.append("variable many weights" if w else "many weights")
    if m["italic"]:
        words.append("italic")
    if len(sc) >= 4:
        words.append("multilingual")
    if m["name"].startswith("Noto"):
        words.append("noto global coverage")
    return {
        "Family": m["name"], "Kind": " / ".join(kinds), "Keywords": " ".join(x for x in words if x),
        "Mood": ", ".join(moods), "Style Tags": ", ".join(styles), "Weights": weights,
        "Italic": "only" if m["italic_only"] else "yes" if m["italic"] else "no", "Axes": axes, "Scripts": ", ".join(sc) or "not listed",
        "Primary Script": m["primary"], "Quality": str(round(sum(quality) / len(quality))) if quality else "",
        "Licence": LICENCES.get(m["license"], m["license"]), "Designer": m["designer"],
        "Added": m["added"], "Specimen URL": "https://fonts.google.com/specimen/" + m["name"].replace(" ", "+"),
        "CSS URL": css_url(m),
    }


def build(src: Path) -> str:
    tags = read_tags(src / "tags" / "all" / "families.csv")
    rows = {}
    for meta in sorted(src.glob("*/*/METADATA.pb")):
        if meta.parts[-3] not in ("ofl", "apache", "ufl"):
            continue
        m = parse(meta.read_text(encoding="utf-8"))
        rows[m["name"]] = row(m, tags.get(m["name"], {}))
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=COLUMNS, lineterminator="\n")
    w.writeheader()
    for name in sorted(rows, key=str.lower):
        w.writerow(rows[name])
    return buf.getvalue()


def check(text: str) -> list[str]:
    problems = []
    rows = list(csv.DictReader(io.StringIO(text)))
    if tuple(rows[0].keys()) != COLUMNS if rows else True:
        return ["missing or wrong header"]
    if len(rows) < 1900:
        problems.append(f"only {len(rows)} families")
    names = [r["Family"] for r in rows]
    if len(set(names)) != len(names):
        problems.append("duplicate families")
    for r in rows:
        if not r["Kind"] or not r["Weights"] or not r["Scripts"]:
            problems.append(f"{r['Family']}: empty kind, weights or scripts")
        if r["Licence"] not in LICENCES.values():
            problems.append(f"{r['Family']}: licence {r['Licence']}")
        if not r["CSS URL"].startswith("https://fonts.googleapis.com/css2?family="):
            problems.append(f"{r['Family']}: css url")
    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--from", dest="src", type=Path, help="a google/fonts checkout (see above)")
    ap.add_argument("--check", action="store_true", help="validate fonts.csv")
    a = ap.parse_args()
    if a.src:
        OUT.write_text(build(a.src), encoding="utf-8")
        print(f"wrote {OUT}")
    problems = check(OUT.read_text(encoding="utf-8"))
    for p in problems[:20]:
        print("problem:", p)
    n = OUT.read_text(encoding="utf-8").count("\n") - 1
    print(f"{n} families, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
