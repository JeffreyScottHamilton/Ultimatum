"""`ult posts` — finished social files and the checks before they go out.

  ult posts specs [PLATFORM]                       sizes, lengths and caption limits used by the checks
  ult posts check FILE... --platform P [--caption TEXT | --caption-file F]
                                                   aspect, size, length, file size, caption length
  ult posts calendar PLAN.json [--to csv|ics] [--out FILE]   posting plan as a sheet or calendar file
  ult posts slides | captions                      rendered carousels and captioned video (postmedia.py)
  ult posts variant add|result|next                hook variants and what to try next (postvariants.py)

Standard library only, plus local ffprobe for video. Nothing here posts or schedules anything.
"""
from __future__ import annotations

import csv
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from ultlib.postspecs import PLATFORMS, SPECS_AS_OF, check_caption, check_file


def cmd_specs(args) -> int:
    names = [args.platform] if args.platform else list(PLATFORMS)
    for n in names:
        s = PLATFORMS[n]
        top, bottom, left, right = s["safe"]
        print(f"{n}: sizes {', '.join(f'{a}x{b}' for a, b in s['sizes'])}; video up to {s['video_max']} s; "
              f"caption {s['caption_max']} chars; keep text clear of {top}px top, {bottom}px bottom, {right}px right")
    print(f"as of {SPECS_AS_OF}; check before relying on the platform's own help page")
    return 0


def cmd_check(args) -> int:
    spec = PLATFORMS[args.platform]
    found = []
    for f in args.files:
        found += check_file(Path(f), spec)
    caption = Path(args.caption_file).read_text(encoding="utf-8") if args.caption_file else args.caption
    if caption is not None:
        found += check_caption(caption, spec)
    blockers = sum(1 for k, _ in found if k == "blocker")
    if args.json:
        print(json.dumps({"platform": args.platform, "problems": [{"kind": k, "text": m} for k, m in found]}, indent=2))
    else:
        print(f"posts check ({args.platform}): {len(args.files)} files, {blockers} blockers, {len(found) - blockers} fixes")
        for k, m in found:
            print(f"  {k}: {m}")
        print(f"limits as of {SPECS_AS_OF} (check before relying); safe zones: `ult posts specs {args.platform}`")
    return 1 if blockers else 0


def _plan(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    items = data.get("posts", data) if isinstance(data, dict) else data
    out = []
    for i, p in enumerate(items, 1):
        if not isinstance(p, dict) or not p.get("date"):
            raise ValueError(f"post {i} has no date (YYYY-MM-DD)")
        datetime.strptime(f"{p['date']} {p.get('time', '09:00')}", "%Y-%m-%d %H:%M")
        out.append(p)
    return out


def _ics_text(s: str) -> str:
    return s.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def to_ics(posts: list[dict]) -> str:
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Ultimatum//posts//EN", "CALSCALE:GREGORIAN"]
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for i, p in enumerate(posts, 1):
        start = datetime.strptime(f"{p['date']} {p.get('time', '09:00')}", "%Y-%m-%d %H:%M")
        end = start + timedelta(minutes=15)
        summary = f"Post: {p.get('channel', '')} {p.get('format', '')} ({p.get('hook_type', 'hook?')})".strip()
        desc = "\n".join(x for x in (p.get("caption", ""), p.get("link", ""), p.get("file", ""),
                                      "Needs the publish approval before it goes out.") if x)
        lines += ["BEGIN:VEVENT", f"UID:post-{i}-{start:%Y%m%d%H%M}@ultimatum.local", f"DTSTAMP:{stamp}",
                  f"DTSTART:{start:%Y%m%dT%H%M%S}", f"DTEND:{end:%Y%m%dT%H%M%S}",
                  f"SUMMARY:{_ics_text(summary)}", f"DESCRIPTION:{_ics_text(desc)}", "END:VEVENT"]
    return "\r\n".join(lines + ["END:VCALENDAR"]) + "\r\n"


CAL_COLUMNS = ["date", "time", "channel", "format", "hook_type", "caption", "link", "file", "status"]


def cmd_calendar(args) -> int:
    try:
        posts = _plan(Path(args.plan))
    except (OSError, ValueError) as e:
        print(f"plan not readable: {e}")
        return 2
    posts.sort(key=lambda p: (p["date"], p.get("time", "09:00")))
    out = Path(args.out or f"social/calendar.{args.to}")
    out.parent.mkdir(parents=True, exist_ok=True)
    if args.to == "ics":
        out.write_text(to_ics(posts), encoding="utf-8", newline="")
    else:
        with out.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=CAL_COLUMNS, extrasaction="ignore")
            w.writeheader()
            w.writerows({**p, "status": p.get("status", "draft, needs approval")} for p in posts)
    per_day: dict[str, int] = {}
    for p in posts:
        per_day[p["date"]] = per_day.get(p["date"], 0) + 1
    print(f"wrote {out}: {len(posts)} posts over {len(per_day)} days; nothing is scheduled or posted")
    busy = [d for d, n in per_day.items() if n > 1]
    if busy:
        print(f"more than one post on {', '.join(busy)}: a higher rate needs the user's yes")
    missing = [p["date"] for p in posts if not p.get("hook_type")]
    if missing:
        print(f"{len(missing)} posts have no hook_type; results compare by hook type")
    return 0


def register(sub):
    from ultlib import postmedia, postvariants  # noqa: PLC0415 - sibling modules
    p = sub.add_parser("posts", help="social files: platform checks, calendar, rendered slides, captions, hook variants")
    s = p.add_subparsers(dest="posts_cmd", required=True)
    c = s.add_parser("specs", help="sizes, lengths and caption limits per platform")
    c.add_argument("platform", nargs="?", choices=sorted(PLATFORMS))
    c.set_defaults(func=cmd_specs)
    c = s.add_parser("check", help="check images or videos and a caption against a platform")
    c.add_argument("files", nargs="*")
    c.add_argument("--platform", required=True, choices=sorted(PLATFORMS))
    c.add_argument("--caption")
    c.add_argument("--caption-file")
    c.add_argument("--json", action="store_true")
    c.set_defaults(func=cmd_check)
    c = s.add_parser("calendar", help="posting plan as a CSV sheet or an .ics calendar")
    c.add_argument("plan")
    c.add_argument("--to", choices=("csv", "ics"), default="csv")
    c.add_argument("--out")
    c.set_defaults(func=cmd_calendar)
    postmedia.register(s)
    postvariants.register(s)
