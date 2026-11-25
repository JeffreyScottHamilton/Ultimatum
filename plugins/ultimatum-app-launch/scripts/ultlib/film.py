"""`ult film` — plan and check a Brand Film job (offline, deterministic).

A brand film is the emotional, story-led kind of video: one person, a want, a turn,
the brand last. It has four user gates in order: story, sourcing (footage, spend and
consent), animatic, then the finished video. `--check` validates the footage manifest
(where every clip came from, its licence, cost, AI flag and release) and the voiceover
pace. `--deliver` runs the same export check as Motion Graphics. Nothing here buys,
downloads, generates or contacts the network.
"""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

from .common import project_root
from .route import cat_paths, plugin_file, sanitize

GATES = ("story", "sourcing", "animatic", "video")
FILM_DIR = "film"
MANIFEST = "footage-manifest.json"
REQUIRED = ("file", "source", "id", "license", "date", "cost", "ai", "people")
SOURCES = ("user", "pexels", "pixabay", "coverr", "mixkit", "stock-paid", "ai", "other")
MEDIA_EXT = (".mp4", ".mov", ".m4v", ".mkv", ".webm", ".wav", ".mp3", ".aif", ".aiff", ".braw", ".r3d", ".mxf")
VO_MIN, VO_MAX = 1.2, 1.8  # spoken words per second that leave room to feel

_MONTAGE_RE = re.compile(r"\b(?:montage|anthem\w*|manifesto|many\s+people|everyone|people\s+who|"
                         r"different\s+people|collage|ode\s+to)\b", re.I)
_LONG_RE = re.compile(r"\b(?:(?:[2-9]|\d{2,})\s*min(?:ute)?s?|series|episodes?)\b", re.I)
_SHIP_RE = re.compile(r"\b(?:publish|post\s+it|upload\s+it|release|go\s+live|run\s+(?:it\s+as\s+)?ads?)\b", re.I)

ROLES = {
    "story": ["director (you, the manager)", "writer"],
    "sourcing": ["scout (stock and archive search)", "shoot coordinator (the user's own footage)",
                 "generator (AI b-roll, only if approved)", "compliance reviewer"],
    "animatic": ["editor (rough cut on temp or approved music)", "sound"],
    "video": ["editor", "colorist", "sound", "film critic", "compliance reviewer"],
}
LOAD = {
    "story": ["skills/brand-film/SKILL.md", "skills/brand-film/story.md"],
    "sourcing": ["skills/brand-film/SKILL.md", "skills/brand-film/references/footage.md",
                 "skills/launch/references/licenses.md"],
    "animatic": ["skills/brand-film/SKILL.md", "skills/brand-film/references/edit.md",
                 "skills/brand-film/references/sound.md"],
    "video": ["skills/brand-film/SKILL.md", "skills/brand-film/references/edit.md",
              "skills/brand-film/references/sound.md"],
}


def film_dir(root: Path) -> Path:
    return root / FILM_DIR


def stage(root: Path) -> tuple[str, dict]:
    """The first gate that is not approved, and every gate's state."""
    from .gates import status
    states = {g: status(root, g)[0] for g in GATES}
    for g in GATES:
        if states[g] != "approved":
            return g, states
    return "done", states


def plan(task: str, root: Path) -> dict:
    text, _ = sanitize(task or "")
    nxt, states = stage(root)
    work = nxt if nxt != "done" else "video"
    return {
        "workflow": "film",
        "subgenre": "montage" if _MONTAGE_RE.search(text) else "character",
        "size": "large" if _LONG_RE.search(text) else "standard",
        "gates": states,
        "stage": nxt,
        "roles": ROLES[work],
        "release": "asked (publish only on the user's explicit yes)" if _SHIP_RE.search(text) else "not asked",
        "load": ["shared/defaults.md"] + LOAD[work],
    }


NEXT = {
    "story": "write the logline and beat sheet (story.md); show them with the sub-genre and wait; "
             "on yes `ult gate approve story \"<their words>\"`",
    "sourcing": "build the footage plan: lane per shot, cost total, consent and releases; show it and wait; "
                "nothing is bought, generated or shot before `ult gate approve sourcing \"<their words>\"`",
    "animatic": "cut the rough timeline from approved sources (stills or temp clips are fine); show it; "
                "on yes `ult gate approve animatic \"<their words>\" --file PATH`",
    "video": "finish: grade, mix, titles, cutdowns; critic and compliance pass; `ult film --check`, then "
             "`ult film --deliver FILE` and show it; on yes `ult gate approve video \"<their words>\" --file PATH`",
    "done": "all four approvals are in; hand the delivered film to Social Media for the publish approval",
}


def format_text(p: dict) -> str:
    gates = "  ".join(f"{g}:{s}" for g, s in p["gates"].items())
    return "\n".join([
        f"workflow: film  sub-genre: {p['subgenre']}  size: {p['size']}",
        f"gates: {gates}",
        "roles now: " + " -> ".join(p["roles"]),
        f"next: {NEXT[p['stage']]}",
        f"release: {p['release']}",
        "rule: media files stay out of git; only film/footage-manifest.json and the text plans are committed",
        "load: " + ", ".join(p["load"]),
    ])


# ---------------------------------------------------------------- checks

def check_manifest(root: Path) -> tuple[list[str], list[str]]:
    """(problems, notes) for film/footage-manifest.json."""
    path = film_dir(root) / MANIFEST
    if not path.is_file():
        return [f"no {FILM_DIR}/{MANIFEST}: every clip, track and still needs a row before the edit"], []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except ValueError as e:
        return [f"{MANIFEST} is not valid JSON: {e}"], []
    clips = data.get("clips") if isinstance(data, dict) else data
    if not isinstance(clips, list) or not clips:
        return [f"{MANIFEST} has no clips (expected a list, or an object with a 'clips' list)"], []
    problems, notes, spend, ai = [], [], 0.0, 0
    for n, c in enumerate(clips, 1):
        if not isinstance(c, dict):
            problems.append(f"row {n}: not an object")
            continue
        name = c.get("file") or f"row {n}"
        missing = [k for k in REQUIRED if k not in c or c[k] in ("", None)]
        if missing:
            problems.append(f"{name}: missing {', '.join(missing)}")
        src = str(c.get("source", "")).lower()
        if src and src not in SOURCES:
            notes.append(f"{name}: source '{src}' is not one of {', '.join(SOURCES)}; say what it is")
        if c.get("people") is True and not c.get("ai") and not c.get("release"):
            problems.append(f"{name}: shows people but has no release (signed consent or the stock licence's model release)")
        if c.get("ai") is True:
            ai += 1
            if c.get("people") is True and c.get("hero"):
                problems.append(f"{name}: AI-made person in a hero moment; use a real person for the human beat")
        try:
            spend += float(c.get("cost") or 0)
        except (TypeError, ValueError):
            problems.append(f"{name}: cost must be a number (0 for free)")
    notes.append(f"{len(clips)} clip(s), spend {spend:.2f}, {ai} AI-made")
    if ai:
        notes.append("AI-made clips: label the post where the platform asks, and keep content credentials (C2PA) on export")
    return problems, notes


def tracked_media(root: Path) -> list[str]:
    try:
        out = subprocess.run(["git", "ls-files", FILM_DIR], cwd=root, capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.SubprocessError):
        return []
    return [f for f in out.stdout.splitlines() if f.lower().endswith(MEDIA_EXT)]


def vo_pace(script: Path, seconds: float) -> tuple[float, str]:
    words = len(re.findall(r"[\w']+", script.read_text(encoding="utf-8", errors="replace")))
    rate = words / seconds if seconds > 0 else 0.0
    if rate > VO_MAX:
        return rate, f"too dense: {rate:.2f} words/s; cut to {int(VO_MAX * seconds)} words or less so the film can breathe"
    if rate and rate < VO_MIN:
        return rate, f"sparse: {rate:.2f} words/s; fine if the pictures carry it, else add a line"
    return rate, f"ok: {rate:.2f} words/s"


def cmd_film(args) -> int:
    root = Path(args.root).resolve() if args.root else project_root()
    if args.deliver:
        from .motion import deliver
        problems, _ = check_manifest(root)
        if problems:
            for p in problems:
                print(f"problem: {p}")
            print("not delivered: fix the footage manifest first (`ult film --check`)")
            return 1
        return deliver(root, Path(args.deliver))
    if args.check:
        problems, notes = check_manifest(root)
        problems += [f"media file tracked by git: {f} (keep footage out of the repo)" for f in tracked_media(root)]
        if args.vo:
            if not args.seconds:
                print("ult film --vo needs --seconds (the length the voiceover plays over)")
                return 2
            notes.append("voiceover " + vo_pace(Path(args.vo), args.seconds)[1])
        for p in problems:
            print(f"problem: {p}")
        for n in notes:
            print(f"note: {n}")
        print("film check: " + ("clear" if not problems else f"{len(problems)} problem(s)"))
        return 1 if problems else 0
    p = plan(" ".join(args.task or []), root)
    if args.json:
        print(json.dumps(p, indent=2))
        return 0
    print(format_text(p))
    if args.cat:
        print(cat_paths([plugin_file(f) for f in p["load"]]))
    return 0


def register(sub):
    p = sub.add_parser("film", help="Brand Film plan: sub-genre, four gates, roles; checks footage manifest and VO pace")
    p.add_argument("task", nargs="*", help="the film task (quote it)")
    p.add_argument("--root", help="project directory (default: the current project)")
    p.add_argument("--json", action="store_true")
    p.add_argument("--cat", action="store_true", help="also print the files to load")
    p.add_argument("--check", action="store_true", help="check film/footage-manifest.json, tracked media, and --vo pace")
    p.add_argument("--vo", metavar="FILE", help="with --check: the voiceover script")
    p.add_argument("--seconds", type=float, help="with --vo: seconds the voiceover plays over")
    p.add_argument("--deliver", metavar="FILE", help="manifest check, then the Motion export check, then record it")
    p.set_defaults(func=cmd_film)
