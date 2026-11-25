#!/usr/bin/env python3
"""Copy core's toolbelt and the core files it reads into every launch plugin.

Claude Code gives each plugin its own folder and documents no way for one plugin to
read another's files, so ultimatum-launch and each kind of launch plugin (website,
e-commerce, app) ship an exact copy of core's `ult`. Run
this after changing anything listed below; core's test_toolbelt_copy fails until the
copy matches again. Standard library only.

    python3 tools/sync_launch_toolbelt.py          # copy (and remove stale ultlib files)
    python3 tools/sync_launch_toolbelt.py --check  # exit 1 if the copy differs
"""
from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CORE = REPO / "plugins" / "ultimatum"
LAUNCH = REPO / "plugins" / "ultimatum-launch"
# The shared launch teams, then one plugin per kind of launch.
TARGETS = [LAUNCH] + [REPO / "plugins" / f"ultimatum-{k}-launch" for k in ("website", "ecommerce", "app")]

# Same path in both plugins.
SAME_PATH = [
    "scripts/ult",
    "scripts/ult-pick",
    "scripts/ult-browser.mjs",
    "shared/defaults.md",
    "data/components.json",  # `ult components`, which coding/SKILL.md uses
]
# Core files the launch commands print with --cat; kept under shared/core/ so they
# are not registered as launch skills. ultlib/route.py:plugin_file() finds them there.
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


def pairs() -> list[tuple[Path, Path]]:
    """(core source, copy) for every copied file in every launch plugin."""
    out = []
    for t in TARGETS:
        out += [(CORE / rel, t / rel) for rel in SAME_PATH]
        out += [(p, t / "scripts" / "ultlib" / p.name)
                for p in sorted((CORE / "scripts" / "ultlib").glob("*.py"))]
        out += [(CORE / rel, t / "shared" / "core" / rel) for rel in CORE_DOCS]
    return out


def stale() -> list[Path]:
    """ultlib files in a copy that core no longer has."""
    keep = {p.name for p in (CORE / "scripts" / "ultlib").glob("*.py")}
    return [p for t in TARGETS for p in sorted((t / "scripts" / "ultlib").glob("*.py")) if p.name not in keep]


def differences() -> list[str]:
    bad = [str(dst.relative_to(REPO)) for src, dst in pairs()
           if not dst.is_file() or not filecmp.cmp(src, dst, shallow=False)]
    return bad + [f"{p.relative_to(REPO)} (not in core)" for p in stale()]


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
        print("launch toolbelt matches core" if not bad else f"{len(bad)} file(s) differ; run tools/sync_launch_toolbelt.py")
        return 1 if bad else 0
    print(f"updated {sync()} file(s) in {len(TARGETS)} launch plugin(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
