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

from .common import project_root, state_dir, write_private
from .route import cat_paths, plugin_file, decide, sanitize
from .website import approval, brief_path, record_approval

APPROVED_STORYBOARD = "## Approved storyboard"

# Changing a clip that already exists (no new storyboard needed).
_TWEAK_RE = re.compile(
    r"\b(?:fix|trim|shorten|lengthen|speed\s+up|slow\s+down|swap|replace|re-?export|export\s+again|change\s+the\s+"
    r"(?:colou?r|text|font|music|song|logo|ending|title)|typo|nudge|retime|re-?time|louder|quieter)\b", re.I)
_EXISTING_RE = re.compile(r"\b(?:the|my|our|this|existing|current)\s+(?:[\w-]+\s+){0,2}(?:clip|video|reel|intro|animation|cut|edit|export)\b", re.I)
_LONG_RE = re.compile(r"\b(?:series|several\s+videos|episodes?|(?:[2-9]|\d{2,})\s*(?:min(?:ute)?s?)\b|"
                      r"(?:[6-9]\d|\d{3,})\s*(?:s|sec(?:ond)?s?)\b)", re.I)
_MUSIC_RE = re.compile(r"\b(?:music|song|track|beats?|soundtrack|audio|mp3|wav|bpm|drop|voice-?over|narration)\b", re.I)
_FRESH_RE = re.compile(r"\b(?:reference|like\s+this|in\s+the\s+style\s+of|fresh\s+(?:look|style)|new\s+style|"
                       r"different\s+style|standalone)\b", re.I)
_LAUNCH_VIDEO_RE = re.compile(r"\blaunch\b", re.I)
STYLE_TOPICS = ("pacing", "cuts", "text", "sound", "ending")
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


def style_path(root: Path) -> Path:
    return brief_path(root).parent / "motion" / "style.md"


def kind(text: str, root: Path) -> str:
    """first-launch (optional /brag), later (reuse the approved style) or standalone (fresh or a reference)."""
    from .gates import brief_section
    if _FRESH_RE.search(text):
        return "standalone"
    if style_path(root).is_file():
        return "later"
    if _LAUNCH_VIDEO_RE.search(text) or brief_section(root):
        return "first-launch"
    return "standalone"


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
    k = kind(text, root or project_root())
    if k == "later" and not small:
        load.append(str(style_path(root or project_root())))
    return {
        "workflow": "motion",
        "kind": k,
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
    if p.get("kind") == "first-launch" and p["size"] != "small":
        lines.append("kind: first launch video; /brag is optional if the user has it: use its ideas inside the "
                     "storyboard step, never to skip approval. After the user approves the finished video, "
                     "`ult motion --save-style`")
    elif p.get("kind") == "later" and p["size"] != "small":
        lines.append("kind: later video; reuse the approved style guide (pacing, cuts, text movement, sound cues, "
                     "ending) with a new storyboard, which still needs approval")
    elif p.get("kind") == "standalone" and p["size"] != "small":
        lines.append("kind: standalone; start from the user's reference if they gave one, else a fresh style")
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
        from .gates import approve
        approve(root, "storyboard", args.approve)
        return 0
    if args.save_style is not None:
        return save_style(root, args.save_style, args.video)
    if args.deliver:
        return deliver(root, Path(args.deliver))
    p = plan(task, root=root)
    if args.json:
        print(json.dumps(p, indent=2))
        return 0
    print(format_text(p))
    if args.cat:
        files = list(p["load"])
        if p["overlay"]:
            files.append("skills/work/references/security/secure-implementation.md")
        print(cat_paths([plugin_file(f) for f in files]))
    return 0


def save_style(root: Path, notes: str, video: str | None) -> int:
    """After the user approves the finished video: keep it on record and write the project style guide."""
    from .gates import _file_sha, status
    if not notes.strip() or not video:
        print("ult motion --save-style needs the style notes and --video PATH of the approved video")
        return 2
    st, detail = status(root, "video")
    if st != "approved":
        print(f"not saved: the finished video is {st} ({detail}); "
              "ask the user, then `ult gate approve video \"<their words>\" --file PATH`")
        return 1
    sha = _file_sha(video)
    if sha is None:
        print(f"ult motion: no such file: {video}")
        return 2
    path = style_path(root)
    state_dir(root, "motion")
    write_private(path, f"# Motion style guide\n\nApproved video: {Path(video).resolve()} (sha {sha})\n\n"
                        f"{notes.strip()}\n\nLater videos reuse this style with a new storyboard.\n")
    missing = [t for t in STYLE_TOPICS if t not in notes.lower()]
    print(f"saved {path}")
    if missing:
        print("warn: the guide does not mention: " + ", ".join(missing))
    return 0


def deliver(root: Path, video: Path) -> int:
    """Manager's final check before handing a video to Social or the user."""
    from . import loop, media
    if not video.is_file():
        print(f"ult motion: no such file: {video}")
        return 2
    blockers, unsorted = loop.blocking(loop.load(root))
    if blockers or unsorted:
        print(f"not delivered: {len(blockers)} open blocker(s), {len(unsorted)} unsorted finding(s) (`ult loop status`)")
        return 1
    if not shutil.which("ffprobe"):
        print("not delivered: ffprobe not found, so the export was not measured; say so and play it once")
        return 2
    m = media.probe(video)
    m["lufs"] = media.loudness(video) if m["audio"] and shutil.which("ffmpeg") else None
    warns = media.warnings(m)
    for w in warns:
        print(f"warn: {w}")
    if warns:
        print("not delivered: fix the export warnings and recheck")
        return 1
    from .gates import _file_sha
    from .teams import DELIVERED_HEAD, write_section
    body = (f"File: {video.resolve()} (sha {_file_sha(str(video))})\n"
            f"Checked: {m['duration']}s {m['width']}x{m['height']} {m['fps']} fps, loudness {m['lufs']} LUFS, "
            "review loop clear")
    print(f"delivered: recorded in {write_section(root, DELIVERED_HEAD, body)}")
    return 0


def register(sub):
    p = sub.add_parser("motion", help="Motion Graphics plan: size, roles, storyboard gate, renderer, files to load")
    p.add_argument("task", nargs="*", help="the motion task (quote it)")
    p.add_argument("--root", help="project directory (default: the current project)")
    p.add_argument("--json", action="store_true", help="machine-readable output")
    p.add_argument("--cat", action="store_true", help="also print the files to load")
    p.add_argument("--approve", metavar="TEXT", help="record the storyboard the user approved in the brief")
    p.add_argument("--image", metavar="PATH", help="with --approve: the storyboard frames image, if saved")
    p.add_argument("--save-style", metavar="NOTES", help="after the user approves the finished video: write the style guide")
    p.add_argument("--video", metavar="PATH", help="with --save-style: the approved video")
    p.add_argument("--deliver", metavar="FILE", help="final check of the export, then record it for Social or the user")
    p.set_defaults(func=cmd_motion)
