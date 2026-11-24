"""`ult motion` — plan the Motion Graphics workflow for one task (offline, deterministic).

Prints the job size, the role order, the storyboard gate, the renderer this
machine can use, and the files each role needs. With --cat it also prints them.
`--approve TEXT` records the storyboard the user approved in the shared brief.
Nothing here renders, installs or contacts the network.
"""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

from .common import project_root
from .route import PLUGIN, cat_paths, decide, sanitize
from .website import approval, record_approval

APPROVED_STORYBOARD = "## Approved storyboard"

# Changing a clip that already exists (no new storyboard needed).
_TWEAK_RE = re.compile(
    r"\b(?:fix|trim|shorten|lengthen|speed\s+up|slow\s+down|swap|replace|re-?export|export\s+again|change\s+the\s+"
    r"(?:colou?r|text|font|music|song|logo|ending|title)|typo|nudge|retime|re-?time|louder|quieter)\b", re.I)
_EXISTING_RE = re.compile(r"\b(?:the|my|our|this|existing|current)\s+(?:[\w-]+\s+){0,2}(?:clip|video|reel|intro|animation|cut|edit|export)\b", re.I)
_LONG_RE = re.compile(r"\b(?:series|several\s+videos|episodes?|(?:[2-9]|\d{2,})\s*(?:min(?:ute)?s?)\b|"
                      r"(?:[6-9]\d|\d{3,})\s*(?:s|sec(?:ond)?s?)\b)", re.I)
_MUSIC_RE = re.compile(r"\b(?:music|song|track|beats?|soundtrack|audio|mp3|wav|bpm|drop|voice-?over|narration)\b", re.I)
_SHIP_RE = re.compile(r"\b(?:publish|post\s+it|upload\s+it|share\s+it\s+(?:on|to)|release|go\s+live)\b", re.I)


def renderer(root: Path | None) -> tuple[str, str]:
    """The renderer this machine can use, best first, and why."""
    if shutil.which("hyperframes") or (root and (root / "node_modules" / "hyperframes").is_dir()):
        return "hyperframes", "installed"
    if shutil.which("node") and shutil.which("ffmpeg"):
        return "html-capture", "HyperFrames not installed; HTML/CSS animation captured with Playwright, joined by ffmpeg"
    if shutil.which("ffmpeg"):
        return "ffmpeg", "HyperFrames and node not found; ffmpeg filters only"
    return "none", "no renderer found: deliver the storyboard and animation code, and say the video was not rendered"


def plan(task: str, root: Path | None = None) -> dict:
    text, _ = sanitize(task or "")
    d = decide(text, root=root, use_deps=False, lessons_on=False)
    small = bool(_TWEAK_RE.search(text) and _EXISTING_RE.search(text))
    big = not small and bool(_LONG_RE.search(text))
    size = "small" if small else ("large" if big else "standard")
    status = "not needed" if small else approval(root, APPROVED_STORYBOARD)
    roles = (["manager", "animator", "motion reviewer"] if small else
             ["planner (manager)", "designer"] + (["user approves storyboard"] if status != "approved" else [])
             + ["animator", "motion reviewer", "manager"])
    ship = bool(_SHIP_RE.search(text))
    load = ["shared/defaults.md"]
    if not small:
        load += ["skills/motion-graphics/storyboard.md", "skills/design/SKILL.md"]
    load += ["skills/coding/SKILL.md", "skills/coding/guides/motion.md", "skills/review/SKILL.md"]
    if ship:
        load.append("skills/release/SKILL.md")
    tool, why = renderer(root)
    return {
        "workflow": "motion",
        "size": size,
        "team": "helpers" if big else "solo",
        "roles": roles,
        "approval": status,
        "music": bool(_MUSIC_RE.search(text)),
        "renderer": tool,
        "renderer_why": why,
        "release": "asked (publish only on the user's explicit yes)" if ship else "not asked",
        "load": load,
        "overlay": d["overlay"],
    }


def format_text(p: dict) -> str:
    lines = [f"workflow: motion  size: {p['size']}  team: {p['team']}",
             "roles: " + " -> ".join(p["roles"]) + ("  (one person: you)" if p["team"] == "solo" else ""),
             f"renderer: {p['renderer']} ({p['renderer_why']})",
             f"release: {p['release']}",
             "load: " + ", ".join(p["load"])]
    if p["music"]:
        lines.append("audio: `ult beats <file>` gives suggested beats (librosa) or possible cues (ffmpeg); "
                     "listen and confirm before timing cuts")
    if p["size"] == "small":
        lines.append("scope: only the change asked for; then `ult media <export>` and watch it once")
    elif p["approval"] == "waiting":
        lines.append("gate: brief + storyboard (key frames, rough times, transitions, audio cues), then stop until "
                     "the user approves it; no production animation before that (storyboard.md)")
    else:
        lines.append("gate: approved; animate from the brief's Approved storyboard, then review the export against it")
    if p["overlay"]:
        lines.append("overlay: security (skills/work/references/security/secure-implementation.md)")
    return "\n".join(lines)


def cmd_motion(args) -> int:
    task = " ".join(args.task or []).strip()
    root = Path(args.root).resolve() if args.root else project_root()
    if args.approve is not None:
        if not args.approve.strip():
            print("ult motion --approve needs the user's approved storyboard in words")
            return 2
        print(f"recorded approval in {record_approval(root, args.approve, args.image, APPROVED_STORYBOARD)}")
        return 0
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
    p = sub.add_parser("motion", help="Motion Graphics plan: size, roles, storyboard gate, renderer, files to load")
    p.add_argument("task", nargs="*", help="the motion task (quote it)")
    p.add_argument("--root", help="project directory (default: the current project)")
    p.add_argument("--json", action="store_true", help="machine-readable output")
    p.add_argument("--cat", action="store_true", help="also print the files to load")
    p.add_argument("--approve", metavar="TEXT", help="record the storyboard the user approved in the brief")
    p.add_argument("--image", metavar="PATH", help="with --approve: the storyboard frames image, if saved")
    p.set_defaults(func=cmd_motion)
