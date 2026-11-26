"""Find installed design skills the Website and Motion Graphics teams should load.

Looks only at local folders: the project's `.claude/skills`, `~/.claude/skills` and installed
plugin skills under `~/.claude/plugins/cache`. Nothing is installed or fetched. Ultimatum's own
skills are skipped. `ULTIMATUM_SKILL_DIRS` (os.pathsep list) replaces the search roots, for tests.
"""
from __future__ import annotations

import os
from pathlib import Path

# Skill folder name -> kind. Exact names first; then the substring rules below.
KNOWN = {"frontend-design": "ui", "design-handoff": "ui", "ui-ux-pro-max": "ui", "hallmark": "ui",
         "remotion-best-practices": "motion", "anatomy": "motion", "animejs": "motion", "anime-js": "motion"}
UI_WORDS = ("frontend-design", "ui-design", "web-design", "webdesign", "design-system")
MOTION_WORDS = ("remotion", "motion", "hyperframes", "animation")


def _roots(root: Path | None) -> list[Path]:
    env = os.environ.get("ULTIMATUM_SKILL_DIRS")
    if env is not None:
        return [Path(p) for p in env.split(os.pathsep) if p]
    home = Path.home() / ".claude"
    out = [home / "skills"]
    if root:
        out.insert(0, root / ".claude" / "skills")
    cache = home / "plugins" / "cache"
    if cache.is_dir():
        out += sorted(p for p in cache.glob("*/*/*/skills") if p.is_dir())
        out += sorted(p for p in cache.glob("*/*/skills") if p.is_dir())
    return out


def _kind(name: str) -> str | None:
    n = name.lower()
    if n in KNOWN:
        return KNOWN[n]
    if any(w in n for w in UI_WORDS):
        return "ui"
    if any(w in n for w in MOTION_WORDS):
        return "motion"
    return None


def find(root: Path | None, want: str) -> list[tuple[str, str]]:
    """(skill name, SKILL.md path) for installed skills of kind `want` ("ui" or "motion")."""
    seen: dict[str, str] = {}
    for base in _roots(root):
        if "cache" in base.parts and any(p.startswith("ultimatum") for p in base.parts[-4:-1]):
            continue  # Ultimatum's own skills
        try:
            dirs = sorted(base.iterdir())
        except OSError:
            continue
        for d in dirs:
            skill = d / "SKILL.md"
            if d.name not in seen and _kind(d.name) == want and skill.is_file():
                seen[d.name] = str(skill)
    return sorted(seen.items(), key=lambda kv: (kv[0] not in KNOWN, kv[0]))


def line(root: Path | None, want: str) -> str:
    found = find(root, want)
    if found:
        names = ", ".join(f"{n} ({p})" for n, p in found[:3])
        step = "the three directions and the build" if want == "ui" else "the storyboard and the animation"
        return (f"design-skill: {names}; read it before {step} and follow it for look and craft. "
                "Ultimatum's gates, checks and the user's approval still apply")
    tip = "Anthropic's frontend-design plugin" if want == "ui" else "the renderer's own skill, for example Remotion's"
    return f"design-skill: none installed; use the built-in design guide (the user can add {tip})"
