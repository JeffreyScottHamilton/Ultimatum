"""`ult cut` — Creator Cut: jump cuts, punch-ins and a 9:16 crop from a talking-head recording.

  ult cut silences VIDEO [--noise -35] [--min 0.35] [--pad 0.1] [--out PLAN]
      ffmpeg silencedetect -> a cut plan (the spoken parts to keep), written as editable JSON
  ult cut check PLAN [--platform P] [--max SECONDS]
      the plan's takes against the source, total length, a quick hook, takes that run long
  ult cut render PLAN --out FILE [--vertical] [--punch 1.12] [--print]
      one ffmpeg pass: trim each take, punch in on every other one, crop to 9:16, join
  ult cut deliver FILE
      the review loop and the export check shared with Motion Graphics, then `## Delivered video`

The plan is plain JSON: delete a take to drop it, move one to the top for a cold open, add a "note".
Silence finding is a suggestion; listen to every join. Local ffmpeg only, nothing is uploaded.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

W, H = 1080, 1920
FADE = 0.012  # seconds of audio fade at each join, so cuts don't click
_START = re.compile(r"silence_start:\s*(-?[\d.]+)")
_END = re.compile(r"silence_end:\s*(-?[\d.]+)")


def parse_silences(log: str, duration: float) -> list[tuple[float, float]]:
    """(start, end) pairs from ffmpeg silencedetect output; an open silence runs to the end."""
    out, start = [], None
    for line in log.splitlines():
        m = _START.search(line)
        if m:
            start = max(0.0, float(m.group(1)))
            continue
        m = _END.search(line)
        if m and start is not None:
            out.append((start, float(m.group(1))))
            start = None
    if start is not None:
        out.append((start, duration))
    return out


def keep_segments(silences: list[tuple[float, float]], duration: float, pad: float = 0.1,
                  min_keep: float = 0.25) -> list[tuple[float, float]]:
    """The spoken parts between silences, each widened by `pad`, merged where they touch."""
    keeps, t = [], 0.0
    for s, e in sorted(silences):
        if s > t:
            keeps.append((t, s))
        t = max(t, e)
    if t < duration:
        keeps.append((t, duration))
    merged: list[list[float]] = []
    for a, b in keeps:
        a, b = max(0.0, a - pad), min(duration, b + pad)
        if merged and a <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    return [(round(a, 3), round(b, 3)) for a, b in merged if b - a >= min_keep]


def probe(path: Path) -> dict:
    """Duration, size and whether there is audio, from the local ffprobe."""
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,width,height",
                        "-of", "json", str(path)], capture_output=True, text=True, check=False)
    if r.returncode != 0:
        raise ValueError(f"ffprobe could not read {path}: {r.stderr.strip()[:200]}")
    data = json.loads(r.stdout or "{}")
    streams = data.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), {})
    return {"duration": round(float(data.get("format", {}).get("duration", 0) or 0), 3),
            "width": video.get("width"), "height": video.get("height"),
            "audio": any(s.get("codec_type") == "audio" for s in streams)}


def total(plan: dict) -> float:
    return round(sum(s["out"] - s["in"] for s in plan.get("segments", [])), 3)


def check_plan(plan: dict, max_s: float | None = None) -> list[tuple[str, str]]:
    """(kind, message) problems: "blocker" stops the render, "fix" is worth a look."""
    found: list[tuple[str, str]] = []
    segs = plan.get("segments") or []
    dur = float(plan.get("duration") or 0)
    if not segs:
        return [("blocker", "no takes in the plan")]
    for i, s in enumerate(segs, 1):
        a, b = s.get("in"), s.get("out")
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)) or b <= a or a < 0:
            found.append(("blocker", f"take {i}: in/out must be numbers with out after in"))
        elif dur and b > dur + 0.05:
            found.append(("blocker", f"take {i}: ends at {b:.2f}s, after the source ends ({dur:.2f}s)"))
        elif b - a > 8:
            found.append(("fix", f"take {i}: {b - a:.1f}s with no cut; add a punch-in, b-roll or a trim"))
        elif b - a < 0.3:
            found.append(("fix", f"take {i}: only {b - a:.2f}s; check it is not a breath or a stray word"))
    if any(k == "blocker" for k, _ in found):
        return found
    order = sorted((s["in"], s["out"], i) for i, s in enumerate(segs, 1))
    for (_, b1, i1), (a2, _, i2) in zip(order, order[1:]):
        if a2 < b1 - 0.05:
            found.append(("fix", f"takes {i1} and {i2} share footage; the same words may play twice"))
    first = segs[0]["out"] - segs[0]["in"]
    if first > 3:
        found.append(("fix", f"the first take runs {first:.1f}s; land the hook in the first 2 s (cold open)"))
    t = total(plan)
    if max_s and t > max_s:
        found.append(("blocker", f"the cut runs {t:.1f}s, over the {max_s:.0f}s limit"))
    return found


def _crop_916() -> str:
    return "crop='min(iw,ih*9/16)':'min(ih,iw*16/9)'"


def filter_graph(plan: dict, vertical: bool = True, punch: float = 1.0) -> str:
    """ffmpeg filter_complex: trim each take, punch in on every other one, scale, join."""
    w, h = (W, H) if vertical else (plan.get("width") or 1920, plan.get("height") or 1080)
    audio = plan.get("audio", True)
    parts, labels = [], []
    for i, s in enumerate(plan["segments"]):
        a, b = s["in"], s["out"]
        v = [f"trim=start={a}:end={b}", "setpts=PTS-STARTPTS"]
        if vertical:
            v.append(_crop_916())
        if punch > 1 and i % 2 == 1:
            v.append(f"crop=iw/{punch}:ih/{punch}")
        v += [f"scale={w}:{h}", "setsar=1"]
        parts.append(f"[0:v]{','.join(v)}[v{i}]")
        labels.append(f"[v{i}]")
        if audio:
            ln = round(b - a, 3)
            parts.append(f"[0:a]atrim=start={a}:end={b},asetpts=PTS-STARTPTS,"
                         f"afade=t=in:d={FADE},afade=t=out:st={max(0.0, round(ln - FADE, 3))}:d={FADE}[a{i}]")
            labels.append(f"[a{i}]")
    n = len(plan["segments"])
    parts.append(f"{''.join(labels)}concat=n={n}:v=1:a={1 if audio else 0}[v]" + ("[a]" if audio else ""))
    return ";".join(parts)


def render_cmd(plan: dict, out: Path, vertical: bool, punch: float) -> list[str]:
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(plan["source"]),
           "-filter_complex", filter_graph(plan, vertical, punch), "-map", "[v]"]
    if plan.get("audio", True):
        cmd += ["-map", "[a]", "-c:a", "aac", "-b:a", "192k"]
    return cmd + ["-c:v", "libx264", "-crf", "20", "-preset", "medium", "-pix_fmt", "yuv420p",
                  "-movflags", "+faststart", str(out)]


def _load(path: str) -> dict:
    plan = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(plan, dict) or "source" not in plan:
        raise ValueError("a cut plan needs a \"source\" and \"segments\"")
    src = Path(plan["source"])
    beside = Path(path).parent / src
    if not src.is_absolute() and not src.exists() and beside.exists():
        plan["source"] = str(beside)  # a path written relative to the plan's own folder
    return plan


def _need_ffmpeg() -> bool:
    if shutil.which("ffmpeg") and shutil.which("ffprobe"):
        return True
    print("ffmpeg and ffprobe are not on PATH; install them, or cut in the user's editor (editors/guide.md)")
    return False


def cmd_silences(args) -> int:
    if not _need_ffmpeg():
        return 2
    src = Path(args.video)
    try:
        info = probe(src)
    except ValueError as e:
        print(e)
        return 2
    if not info["audio"]:
        print(f"{src} has no audio track; silence finding needs speech")
        return 2
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(src), "-af",
                        f"silencedetect=noise={args.noise}dB:d={args.min}", "-f", "null", "-"],
                       capture_output=True, text=True, check=False)
    sil = parse_silences(r.stderr, info["duration"])
    keeps = keep_segments(sil, info["duration"], pad=args.pad)
    plan = {"source": str(src), **info,
            "settings": {"noise_db": args.noise, "min_silence": args.min, "pad": args.pad},
            "segments": [{"in": a, "out": b, "note": ""} for a, b in keeps]}
    out = Path(args.out or f"cut/{src.stem}.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    kept = total(plan)
    print(f"wrote {out}: {len(keeps)} takes, {kept:.1f}s kept of {info['duration']:.1f}s "
          f"({info['duration'] - kept:.1f}s of pauses removed)")
    print("next: drop weak takes and move the hook first in the plan, `ult cut check`, show the user, then render")
    return 0


def cmd_check(args) -> int:
    try:
        plan = _load(args.plan)
    except (OSError, ValueError) as e:
        print(f"plan not readable: {e}")
        return 2
    max_s = args.max
    if max_s is None and args.platform:
        from ultlib.postspecs import PLATFORMS
        max_s = PLATFORMS[args.platform]["video_max"]
    found = check_plan(plan, max_s)
    blockers = sum(1 for k, _ in found if k == "blocker")
    print(f"cut check: {len(plan.get('segments') or [])} takes, {total(plan):.1f}s, "
          f"{blockers} blockers, {len(found) - blockers} fixes")
    for k, m in found:
        print(f"  {k}: {m}")
    return 1 if blockers else 0


def cmd_render(args) -> int:
    try:
        plan = _load(args.plan)
    except (OSError, ValueError) as e:
        print(f"plan not readable: {e}")
        return 2
    blockers = [m for k, m in check_plan(plan) if k == "blocker"]
    if blockers:
        print("not rendered: " + "; ".join(blockers))
        return 1
    if args.punch < 1 or args.punch > 1.5:
        print("--punch is a zoom factor between 1.0 (none) and 1.5")
        return 2
    cmd = render_cmd(plan, Path(args.out), args.vertical, args.punch)
    if args.print:
        print(" ".join(cmd))
        return 0
    if not _need_ffmpeg():
        return 2
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if r.returncode != 0:
        print(f"ffmpeg failed ({r.returncode}): {r.stderr.strip()[-400:]}")
        return 1
    print(f"wrote {args.out}: {len(plan['segments'])} takes, {total(plan):.1f}s"
          f"{', 9:16' if args.vertical else ''}{f', punch-in {args.punch}x' if args.punch > 1 else ''}")
    print(f"next: `ult posts captions {args.out} ...`, `ult media {args.out}`, then watch every join")
    return 0


def cmd_deliver(args) -> int:
    from .common import project_root
    from .motion import deliver
    return deliver(project_root(), Path(args.file))


def register(sub):
    p = sub.add_parser("cut", help="Creator Cut: silence-based jump cuts, punch-ins and a 9:16 render")
    s = p.add_subparsers(dest="cut_cmd", required=True)
    c = s.add_parser("silences", help="find the pauses and write a cut plan of the spoken takes")
    c.add_argument("video")
    c.add_argument("--noise", type=float, default=-35.0, help="silence threshold in dB (default -35)")
    c.add_argument("--min", type=float, default=0.35, help="shortest pause to cut, in seconds")
    c.add_argument("--pad", type=float, default=0.1, help="seconds kept either side of speech")
    c.add_argument("--out")
    c.set_defaults(func=cmd_silences)
    c = s.add_parser("check", help="check a cut plan: takes, length, hook, long takes")
    c.add_argument("plan")
    from ultlib.postspecs import PLATFORMS
    c.add_argument("--platform", choices=sorted(PLATFORMS))
    c.add_argument("--max", type=float)
    c.set_defaults(func=cmd_check)
    c = s.add_parser("render", help="render a cut plan with ffmpeg")
    c.add_argument("plan")
    c.add_argument("--out", required=True)
    c.add_argument("--vertical", action="store_true", help="center-crop to 9:16 at 1080x1920")
    c.add_argument("--punch", type=float, default=1.0, help="zoom on every other take, e.g. 1.12")
    c.add_argument("--print", action="store_true", help="print the ffmpeg command instead of running it")
    c.set_defaults(func=cmd_render)
    c = s.add_parser("deliver", help="check the finished export and record it for Social Media")
    c.add_argument("file")
    c.set_defaults(func=cmd_deliver)
