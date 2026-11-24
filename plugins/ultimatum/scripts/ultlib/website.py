"""`ult website` — plan the Website workflow for one task (offline, deterministic).

Prints the job size, whether helpers are worth it, whether a Designer is needed,
the role order, whether Release was asked for, and the files each role needs.
With --cat it also prints those files, so the Manager reads them in one call.
Nothing here deploys, installs or contacts the network.
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

from .common import project_root
from .route import PLUGIN, cat_paths, decide, sanitize

_KEEP_RE = re.compile(r"\b(keep|match|reuse|same as|stick (?:to|with)|don'?t change|no redesign|without changing)\b[^.]{0,30}\b(look|style|styles|design|branding|brand|theme|colou?rs?|fonts?)\b|\bno redesign\b", re.I)
_NEW_RE = re.compile(r"\b(redesign|re-?style|rebrand|new look|fresh look|new design|new visual|visual direction|from scratch|brand[- ]new|make it look|look (?:better|more|less|modern|premium)|moderni[sz]e|design (?:a|an|the|our|my) )", re.I)
_SHIP_RE = re.compile(r"\b(ship|deploy|publish|release|launch|go live|put it live|make it live)\b", re.I)
_BIG_RE = re.compile(r"\b(multi-?page|full (?:web)?site|entire (?:web)?site|whole (?:web)?site|several pages|many pages)\b", re.I)
_NPAGES_RE = re.compile(r"\b(\d+|four|five|six|seven|eight|nine|ten)[- ]pages?\b", re.I)
_PAGES = ("home", "about", "pricing", "blog", "contact", "docs", "faq", "features", "team", "careers",
          "services", "portfolio", "shop", "checkout", "login", "signup", "dashboard", "testimonials", "gallery")
_WORDNUM = {"four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}

_SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".next", "out", ".ultimatum", "vendor", ".venv",
              "venv", "__pycache__", "coverage", ".cache"}
_STYLE_EXT = (".css", ".scss", ".sass", ".less", ".styl")
_STYLE_NAMES = re.compile(r"^(tailwind\.config\.\w+|theme\.\w+|tokens\.\w+|design-tokens\.\w+|components\.json)$")


def style_signals(root: Path | None, limit: int = 4000) -> list[str]:
    """Existing styling in the project: tokens, Tailwind config, stylesheets, a components/ui folder."""
    if root is None or not root.is_dir():
        return []
    found: list[str] = []
    seen = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in _SKIP_DIRS and not d.startswith(".")]
        rel = Path(dirpath).relative_to(root)
        if len(rel.parts) > 5:
            dirnames[:] = []
            continue
        if rel.parts[-2:] == ("components", "ui"):
            found.append(str(rel))
        for f in filenames:
            seen += 1
            if _STYLE_NAMES.match(f) or f.endswith(_STYLE_EXT):
                found.append(str(rel / f))
            if seen >= limit or len(found) >= 5:
                return found
    return found


def _page_count(text: str) -> int:
    n = 0
    m = _NPAGES_RE.search(text)
    if m:
        v = m.group(1).lower()
        n = int(v) if v.isdigit() else _WORDNUM.get(v, 0)
    named = {p for p in _PAGES if re.search(rf"\b{p}\b", text, re.I)}
    return max(n, len(named))


def plan(task: str, root: Path | None = None) -> dict:
    text, _ = sanitize(task or "")
    d = decide(text, root=root, use_deps=False, lessons_on=False)
    small = d["route"] == "small" or d["mode"] == "FAST"
    big = not small and (bool(_BIG_RE.search(text)) or _page_count(text) >= 4 or d["route"] == "large")
    size = "small" if small else ("large" if big else "standard")

    signals = style_signals(root)
    if _NEW_RE.search(text) and not _KEEP_RE.search(text):
        designer, why = True, "the task asks for a new look"
    elif _KEEP_RE.search(text):
        designer, why = False, "the task keeps the current look"
    elif small:
        designer, why = False, "small edit: keep the current look"
    elif not signals:
        designer, why = True, "no existing styles found"
    else:
        designer, why = False, f"existing styles: {signals[0]}"

    ship = bool(_SHIP_RE.search(text))
    roles = ["manager"] + (["designer"] if designer else []) + (
        ["builder", "closest check"] if small else ["builder", "reviewer", "manager"])
    load = ["shared/defaults.md"]
    if size == "large":
        load.append("skills/work/references/code-map.md")
    if designer:
        load.append("skills/design/SKILL.md")
    load += ["skills/coding/SKILL.md", "skills/coding/guides/website.md"]
    if not small:
        load.append("skills/review/SKILL.md")
    if ship:
        load.append("skills/release/SKILL.md")
    return {
        "workflow": "website",
        "size": size,
        "team": "helpers" if big else "solo",
        "designer": designer,
        "designer_why": why,
        "roles": roles,
        "release": "asked (deploy only on the user's explicit yes)" if ship else "not asked",
        "load": load,
        "overlay": d["overlay"],
    }


def format_text(p: dict) -> str:
    lines = [f"workflow: website  size: {p['size']}  team: {p['team']}",
             f"designer: {'yes' if p['designer'] else 'no'} ({p['designer_why']})",
             "roles: " + " -> ".join(p["roles"]) + ("  (one person: you)" if p["team"] == "solo" else ""),
             f"release: {p['release']}",
             "load: " + ", ".join(p["load"])]
    if p["overlay"]:
        lines.append("overlay: security (skills/work/references/security/secure-implementation.md)")
    return "\n".join(lines)


def cmd_website(args) -> int:
    task = " ".join(args.task or []).strip()
    root = Path(args.root).resolve() if args.root else project_root()
    p = plan(task, root=root)
    if args.json:
        print(json.dumps(p, indent=2))
        return 0
    print(format_text(p))
    if args.cat:
        files = list(p["load"])
        if p["overlay"]:
            files.append("skills/work/references/security/secure-implementation.md")
        print(cat_paths([PLUGIN / f for f in files]))
    return 0


def register(sub):
    p = sub.add_parser("website", help="Website workflow plan: size, team, designer, roles, files to load")
    p.add_argument("task", nargs="*", help="the website task (quote it)")
    p.add_argument("--root", help="project directory (default: the current project)")
    p.add_argument("--json", action="store_true", help="machine-readable output")
    p.add_argument("--cat", action="store_true", help="also print the files to load")
    p.set_defaults(func=cmd_website)
