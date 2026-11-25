#!/usr/bin/env python3
"""Copy the shared team guides, reviewer agents and toolbelt into every head plugin.

Each Ultimatum plugin other than core is a self-contained head: one skill, plus the
team guides it reads, its own reviewer agents and its own copy of core's `ult`.
Claude Code gives each plugin its own folder and documents no way for one plugin to
read another's files, so the shared material is written once and copied here:

- `teams/<team>/`  -> `plugins/<p>/skills/<head>/references/<team>/`
- `teams/agents/*` -> `plugins/<p>/agents/`
- core's toolbelt  -> `plugins/<p>/scripts/`, `shared/` and `data/`

Edit the source, never the copies, then run this. Core's test_plugin_sync fails
until every copy matches again. Standard library only.

    python3 tools/sync_plugins.py          # copy, and remove stale copied files
    python3 tools/sync_plugins.py --check  # exit 1 if any copy differs
"""
from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CORE = REPO / "plugins" / "ultimatum"
TEAMS = REPO / "teams"

LAUNCH_TEAMS = ("business", "website", "social-media", "motion-graphics", "brand-film", "editors", "shared")
# plugin -> (head skill, the team folders it ships). A plugin whose folder does not
# exist yet is skipped, so a new head can be added here before it lands.
MANIFEST = {
    "ultimatum-website-launch": ("launch", LAUNCH_TEAMS),
    "ultimatum-ecommerce-launch": ("launch", LAUNCH_TEAMS),
    "ultimatum-app-launch": ("launch", LAUNCH_TEAMS),
    "ultimatum-event-launch": ("launch", LAUNCH_TEAMS),
    "ultimatum-social-media": ("social-media", ("social-media", "motion-graphics", "brand-film", "editors", "shared")),
}
AGENTS = ("compliance-reviewer", "taste-critic")

# Core toolbelt files, at the same path in every head.
SAME_PATH = [
    "scripts/ult",
    "scripts/ult-pick",
    "scripts/ult-browser.mjs",
    "shared/defaults.md",
    "data/components.json",  # `ult components`
]
# Core files the toolbelt prints with --cat and the guides point at; kept under
# shared/core/ so they are not registered as skills. ultlib/route.py:plugin_file() finds them.
CORE_DOCS = [
    "skills/work/modules.json",
    "skills/work/references/ui.md",
    "skills/work/references/browser-verification.md",
    "skills/work/references/code-map.md",
    "skills/work/references/react.md",
    "skills/work/references/release.md",
    "skills/work/references/design/design.md",
    "skills/work/references/design/motion.md",
    "skills/work/references/design/components.md",
    "skills/work/references/security/secure-implementation.md",
    "skills/work/references/security/change-review.md",
    "skills/work/references/security/coverage-model.md",
    "skills/design/SKILL.md",
    "skills/coding/SKILL.md",
    "skills/coding/guides/website.md",
    "skills/coding/guides/motion.md",
    "skills/review/SKILL.md",
    "skills/release/SKILL.md",
]


def heads() -> list[tuple[Path, str, tuple[str, ...]]]:
    """(plugin dir, head skill, teams) for every head plugin that exists."""
    return [(REPO / "plugins" / name, head, teams) for name, (head, teams) in MANIFEST.items()
            if (REPO / "plugins" / name / ".claude-plugin" / "plugin.json").is_file()]


def _tree(src: Path, dst: Path) -> list[tuple[Path, Path]]:
    return [(p, dst / p.relative_to(src)) for p in sorted(src.rglob("*")) if p.is_file()] if src.is_dir() else []


def pairs() -> list[tuple[Path, Path]]:
    """(source, copy) for every copied file in every head plugin."""
    out = []
    for root, head, teams in heads():
        out += [(CORE / rel, root / rel) for rel in SAME_PATH]
        out += [(p, root / "scripts" / "ultlib" / p.name) for p in sorted((CORE / "scripts" / "ultlib").glob("*.py"))]
        out += [(CORE / rel, root / "shared" / "core" / rel) for rel in CORE_DOCS]
        out += [(TEAMS / "agents" / f"{a}.md", root / "agents" / f"{a}.md") for a in AGENTS]
        for team in teams:
            out += _tree(TEAMS / team, root / "skills" / head / "references" / team)
    return out


def _managed_dirs() -> list[Path]:
    """Folders whose every file is a copy, so anything else in them is stale."""
    dirs = []
    for root, head, teams in heads():
        dirs += [root / "scripts" / "ultlib", root / "agents", root / "shared" / "core"]
        dirs += [root / "skills" / head / "references" / t for t in teams]
    return dirs


def stale() -> list[Path]:
    """Files in a copied folder that no source has any more."""
    wanted = {dst for _, dst in pairs()}
    return [p for d in _managed_dirs() if d.is_dir() for p in sorted(d.rglob("*"))
            if p.is_file() and p not in wanted and "__pycache__" not in p.parts]


def differences() -> list[str]:
    bad = [str(dst.relative_to(REPO)) for src, dst in pairs()
           if not dst.is_file() or not filecmp.cmp(src, dst, shallow=False)]
    return bad + [f"{p.relative_to(REPO)} (no source)" for p in stale()]


def sync() -> int:
    n = 0
    for src, dst in pairs():
        if dst.is_file() and filecmp.cmp(src, dst, shallow=False):
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        n += 1
    for p in stale():
        p.unlink()
        n += 1
    return n


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="only report differences; exit 1 if any")
    args = ap.parse_args(argv)
    if args.check:
        bad = differences()
        for b in bad:
            print(f"differs: {b}")
        print("head plugins match their sources" if not bad else f"{len(bad)} file(s) differ; run tools/sync_plugins.py")
        return 1 if bad else 0
    print(f"updated {sync()} file(s) in {len(heads())} head plugin(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
