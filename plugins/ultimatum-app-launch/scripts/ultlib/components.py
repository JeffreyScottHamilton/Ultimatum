"""`ult components "<need>"` - offline UI component-library lookup with licences.

Reads the bundled data/components.json. No network, no installs. Scoring is
plain token overlap over name, keywords and categories. Restricted or
unlicensed entries are left out unless --all, and then they are flagged.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from .common import dump_json

DATA = Path(__file__).resolve().parents[2] / "data" / "components.json"
STACKS = ("react", "vue", "svelte", "any")
MAX_RESULTS = 3
STOP = frozenset({
    "a", "an", "and", "the", "for", "of", "to", "with", "in", "on", "or", "it", "is", "are",
    "my", "i", "we", "need", "want", "some", "use", "like", "new", "good", "ui", "component",
    "components", "library", "libraries",
})


def load(path: Path = DATA) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))["components"]


def tokens(text: str) -> set[str]:
    out: set[str] = set()
    for word in re.findall(r"[a-z0-9]+", (text or "").lower()):
        if len(word) > 3 and word.endswith("s") and not word.endswith("ss"):
            word = word[:-1]
        if word not in STOP:
            out.add(word)
    return out


def entry_tokens(entry: dict) -> set[str]:
    out = tokens(entry["name"])
    for kw in entry.get("keywords", []):
        out |= tokens(kw)
    for cat in entry.get("categories", []):
        out |= tokens(cat.replace("-", " "))
    return out


def alternatives_of(entry: dict, entries: list[dict]) -> list[str]:
    """Ids of permissive entries that list this entry in alternatives_to."""
    return [e["id"] for e in entries if entry["id"] in e.get("alternatives_to", [])]


def search(need: str, stack: str = "any", include_all: bool = False, entries: list[dict] | None = None) -> list[dict]:
    entries = load() if entries is None else entries
    wanted = tokens(need)
    if not wanted:
        return []
    scored = []
    for entry in entries:
        if stack != "any" and stack not in entry["stacks"] and "any" not in entry["stacks"]:
            continue
        if entry["restricted"] and not include_all:
            continue
        hits = len(wanted & entry_tokens(entry))
        if hits:
            scored.append((hits, entry))
    # Most token hits first; then permissive before restricted, maintained before not, then id.
    scored.sort(key=lambda s: (-s[0], s[1]["restricted"], not s[1]["maintained"], s[1]["id"]))
    out = []
    for hits, entry in scored[:MAX_RESULTS]:
        item = dict(entry, score=hits)
        item["alternatives"] = alternatives_of(entry, entries)
        out.append(item)
    return out


def _licence_label(entry: dict) -> str:
    if entry["restricted"]:
        return "RESTRICTED: " + entry["licence"].removeprefix("restricted:")
    return entry["licence"]


def _maintained_label(entry: dict) -> str:
    if not entry["maintained"]:
        return "NOT maintained" + (f" (last release {entry['last_release']})" if entry.get("last_release") else "")
    return "maintained" + (f" (last release {entry['last_release']})" if entry.get("last_release") else "")


def format_text(results: list[dict]) -> str:
    lines = []
    for i, e in enumerate(results, 1):
        title = e["name"] + (f" ({e['package']})" if e.get("package") else "")
        lines.append(f"{i}. {title} | {_licence_label(e)} | {_maintained_label(e)}")
        lines.append(f"   install: {e['install']}")
        lines.append(f"   fit: {e['fit']}")
        if e["restricted"] and e["alternatives"]:
            lines.append("   alt: " + ", ".join(e["alternatives"][:2]))
    return "\n".join(lines)


def cmd_components(args) -> int:
    need = " ".join(args.need).strip()
    if not need:
        print('usage: ult components "<need>" [--stack react|vue|svelte|any] [--all] [--json]')
        return 2
    results = search(need, args.stack, args.all)
    if args.json:
        print(dump_json(results))
        return 0
    if not results:
        hint = "" if args.all else " Restricted libraries are hidden; add --all to see them."
        print(f"no match for: {need}.{hint}")
        return 0
    print(format_text(results))
    return 0


def register(sub):
    p = sub.add_parser("components", help="offline UI component-library lookup with licences")
    p.add_argument("need", nargs="*", help='what you need, e.g. "animated number counter"')
    p.add_argument("--stack", choices=STACKS, default="any", help="filter by framework")
    p.add_argument("--all", action="store_true", help="include restricted or unlicensed libraries, flagged")
    p.add_argument("--json", action="store_true", help="machine-readable output")
    p.set_defaults(func=cmd_components)
