"""`ult posts` — finished social files and the checks before they go out.

  ult posts specs [PLATFORM]                       sizes, lengths and caption limits used by the checks
  ult posts check FILE... --platform P [--caption TEXT | --caption-file F]
                                                   aspect, size, length, file size, caption length
  ult posts plan PLAN.json [--json]                every planned post: date, channel, hook type, caption,
                                                   link tags, alt text, disclosure, AI label, files, rate
  ult posts calendar PLAN.json [--to csv|ics] [--out FILE]   posting plan as a sheet or calendar file
  ult posts variant add|result|next                hook variants and what to try next (postvariants.py)

Standard library only, plus local ffprobe for video. Nothing here posts or schedules anything.
Finding codes are explained in skills/social-media/references/checker.md.
"""
from __future__ import annotations

import csv
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from ultlib.postspecs import ALIASES, PLATFORMS, SPECS_AS_OF, check_caption, check_file


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
    items = _load_items(path)
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
                                      "Needs the post approval before it goes out.") if x)
        lines += ["BEGIN:VEVENT", f"UID:post-{i}-{start:%Y%m%d%H%M}@ultimatum.local", f"DTSTAMP:{stamp}",
                  f"DTSTART:{start:%Y%m%dT%H%M%S}", f"DTEND:{end:%Y%m%dT%H%M%S}",
                  f"SUMMARY:{_ics_text(summary)}", f"DESCRIPTION:{_ics_text(desc)}", "END:VEVENT"]
    return "\r\n".join(lines + ["END:VCALENDAR"]) + "\r\n"


IMAGE_FORMATS = {"carousel", "image", "photo", "still", "slides", "pin", "story"}
LINK_RE = re.compile(r"https?://[^\s)>\]]+", re.I)
DISCLOSURE_RE = re.compile(r"(?<!\w)#(?:ad|sponsored|paidpartnership|partner)\b|\bpaid partnership\b|\bsponsored\b|"
                           r"\bgifted\b|\bad\b:", re.I)


SOURCE_WORDS = {"shorts": ("youtube", "yt"), "reels": ("instagram", "ig"), "instagram-feed": ("ig",),
                "instagram-story": ("ig",), "x": ("twitter",), "facebook": ("fb", "meta")}


def channel_key(name: str) -> str | None:
    n = (name or "").strip().lower()
    n = ALIASES.get(n, n)
    return n if n in PLATFORMS else None


def _link_problems(link: str, channel: str) -> list[tuple[str, str, str]]:
    q = parse_qs(urlparse(link).query)
    if not q.get("utm_source") or not q.get("utm_campaign"):
        return [("P05", "fix", f"{link}: add utm_source and utm_campaign so visits from this post can be counted")]
    src = q["utm_source"][0].lower()
    ok = {channel, channel.split("-")[0], *SOURCE_WORDS.get(channel, ())}
    if channel and src not in ok and not any(len(w) > 2 and w in src for w in ok):
        return [("P05", "fix", f"{link}: utm_source={src} does not name {channel}")]
    return []


def check_plan(posts: list[dict], base: Path) -> list[dict]:
    """One finding per problem: {post, code, kind, text}. Blockers stop the post going out."""
    found: list[dict] = []

    def add(i, code, kind, text):
        found.append({"post": i, "code": code, "kind": kind, "text": text})

    per_slot: dict[tuple, int] = {}
    seen: dict[tuple, int] = {}
    for i, p in enumerate(posts, 1):
        if not isinstance(p, dict):
            add(i, "P01", "blocker", "not an object with date, channel and caption")
            continue
        try:
            datetime.strptime(f"{p.get('date', '')} {p.get('time', '09:00')}", "%Y-%m-%d %H:%M")
        except ValueError:
            add(i, "P01", "blocker", f"date {p.get('date')!r} / time {p.get('time')!r} is not YYYY-MM-DD and HH:MM")
        ch = channel_key(p.get("channel", ""))
        if not ch:
            add(i, "P02", "blocker", f"channel {p.get('channel')!r} is not one of: {', '.join(sorted(PLATFORMS))}")
        caption = p.get("caption") or ""
        fmt = (p.get("format") or "").lower()
        if not p.get("hook_type"):
            add(i, "P04", "fix", "no hook_type; results are compared by hook type")
        if ch:
            spec = PLATFORMS[ch]
            for kind, msg in check_caption(caption, spec):
                code = "P03" if kind == "blocker" else ("P09" if "hashtag" in msg else "P10" if "first line" in msg
                                                         else "P03")
                add(i, code, kind, msg)
            key = (ch, p.get("date"))
            per_slot[key] = per_slot.get(key, 0) + 1
            if per_slot[key] == 2:
                add(i, "P08", "fix", f"second post on {ch} on {p.get('date')}: a higher rate needs the user's yes")
            dup = (ch, caption.strip().lower())
            if caption.strip() and dup in seen:
                add(i, "P14", "fix", f"same caption as post {seen[dup]} on {ch}")
            seen.setdefault(dup, i)
        if not caption.strip() and not (ch and PLATFORMS[ch]["caption_max"] == 0):
            add(i, "P03", "fix", "no caption")
        links = LINK_RE.findall(caption)
        if p.get("link") and p["link"] not in links:
            links.append(p["link"])
        if len(set(links)) > 1:
            add(i, "P06", "fix", f"{len(set(links))} links; one destination per post reads and measures better")
        for link in sorted(set(links)):
            for code, kind, msg in _link_problems(link, ch or ""):
                add(i, code, kind, msg)
        if not links and not p.get("next_step"):
            add(i, "P15", "fix", "no link and no next_step: say the one thing the viewer should do")
        if (fmt in IMAGE_FORMATS or ch == "pinterest") and not p.get("alt"):
            add(i, "P07", "fix", "image post with no alt text")
        if p.get("sponsored") and not DISCLOSURE_RE.search(caption) and not p.get("paid_label"):
            add(i, "P11", "blocker", "sponsored, gifted or affiliate post with no clear disclosure in the caption "
                                     "and no paid_label: true for the platform's paid-partnership label")
        if p.get("ai_generated") and not p.get("ai_label"):
            add(i, "P12", "blocker", "realistic AI-made media with no ai_label: true; turn on the platform's AI label")
        files = p.get("files") or ([p["file"]] if p.get("file") else [])
        for f in files:
            path = Path(f) if Path(f).is_absolute() else base / f
            if not path.is_file():
                add(i, "P13", "fix", f"{f}: file not found")
            elif ch:
                for kind, msg in check_file(path, PLATFORMS[ch]):
                    add(i, "P13", kind, msg)
    return found


def _load_items(path: Path) -> list:
    data = json.loads(path.read_text(encoding="utf-8"))
    items = data.get("posts", data) if isinstance(data, dict) else data
    if not isinstance(items, list):
        raise ValueError("expected a list of posts, or {\"posts\": [...]}")
    return items


def cmd_plan(args) -> int:
    path = Path(args.plan)
    try:
        posts = _load_items(path)
    except (OSError, ValueError) as e:
        print(f"plan not readable: {e}")
        return 2
    found = check_plan(posts, path.resolve().parent)
    blockers = sum(1 for f in found if f["kind"] == "blocker")
    if args.json:
        print(json.dumps({"posts": len(posts), "blockers": blockers, "findings": found}, indent=2))
    else:
        print(f"posts plan: {len(posts)} posts, {blockers} blockers, {len(found) - blockers} fixes")
        for f in found:
            print(f"  post {f['post']} {f['code']} {f['kind']}: {f['text']}")
        print(f"limits as of {SPECS_AS_OF} (check before relying); nothing was scheduled or posted")
    return 1 if blockers else 0


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
    print(f"check it first: `ult posts plan {args.plan}`")
    busy = [d for d, n in per_day.items() if n > 1]
    if busy:
        print(f"more than one post on {', '.join(busy)}: a higher rate needs the user's yes")
    missing = [p["date"] for p in posts if not p.get("hook_type")]
    if missing:
        print(f"{len(missing)} posts have no hook_type; results compare by hook type")
    return 0


def register(sub):
    from ultlib import postvariants  # noqa: PLC0415 - sibling module
    p = sub.add_parser("posts", help="social posts: plan check, platform checks, calendar, hook variants")
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
    c = s.add_parser("plan", help="check every post in a plan before it is shown for approval")
    c.add_argument("plan")
    c.add_argument("--json", action="store_true")
    c.set_defaults(func=cmd_plan)
    c = s.add_parser("calendar", help="posting plan as a CSV sheet or an .ics calendar")
    c.add_argument("plan")
    c.add_argument("--to", choices=("csv", "ics"), default="csv")
    c.add_argument("--out")
    c.set_defaults(func=cmd_calendar)
    postvariants.register(s)
