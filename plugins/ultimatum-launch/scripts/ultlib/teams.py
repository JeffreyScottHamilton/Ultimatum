"""Launch Manager, Business and Social Media plans (offline, deterministic).

- `ult launch`   the launch board: who works next, which approvals are open, one next step.
- `ult business` advice, a launch build brief, or a scoped hand-off; never changes anything for advice.
- `ult social`   channel, posts, measurement, the video step and the publish gate; `--results` records
                 what the campaign did so Business and Launch can decide what to try next.
All state is the shared brief (.ultimatum/brief.md) plus approvals (gates.py). Stdlib only, no network.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from .common import project_root, state_dir, write_private
from .gates import BRIEF_HEAD, brief_section, status
from .route import cat_paths, plugin_file, sanitize
from .website import brief_path

BRIEF_FIELDS = ("Audience", "Offer", "Main visitor action", "Pages", "Known business details",
                "Open questions", "Checks that show it works")
DELIVERED_HEAD = "## Delivered video"
RESULTS_HEAD = "## Campaign results"

_CHANGE_RE = re.compile(r"^\s*(?:please\s+)?(?:change|update|rewrite|edit|add|remove|fix|replace|move|make|put|set)\b", re.I)
_LAUNCH_WORD_RE = re.compile(r"\b(?:launch|launching|go[- ]to[- ]market|build\s+brief)\b", re.I)
_VIDEO_RE = re.compile(r"\b(?:video|reel|reels|clip|tiktok|shorts|animation|motion)\b", re.I)
_LINK_RE = re.compile(r"\b(?:link|website|site|landing|book(?:ing)?\s+page|sign\s*up|url)\b", re.I)


def _brief_text(root: Path) -> str:
    try:
        return brief_path(root).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def write_section(root: Path, head: str, body: str) -> Path:
    """Replace one '## ' section of the brief, keeping the others."""
    path = state_dir(root) / "brief.md"
    old = path.read_text(encoding="utf-8", errors="replace") if path.exists() else "# Brief\n"
    before, sep, rest = old.partition(head)
    tail = rest.split("\n## ", 1)[1] if sep and "\n## " in rest else ""
    new = before.rstrip() + f"\n\n{head}\n\n{body.strip()}\n" + (f"\n## {tail}" if tail else "")
    write_private(path, new)
    return path


def launch_active(root: Path) -> bool:
    return bool(brief_section(root))


# ---------------------------------------------------------------- launch

def board(root: Path) -> dict:
    g = {i: status(root, i)[0] for i in ("brief", "mockup", "storyboard", "story", "video", "publish")}
    drafted = launch_active(root)
    text = _brief_text(root)
    steps = [
        ("business drafts the build brief", "done" if drafted else "next"),
        ("user approves the brief (Launch Manager shows it)", g["brief"] if drafted else "later"),
        ("website: mockup for the user's approval", g["mockup"]),
        ("website: build, browser review, fixes, checked preview", "after mockup"),
        ("social: drafts from the approved offer while Website builds", "open" if g["brief"] == "approved" else "after brief"),
        ("video, only if it helps: Brand Film (a feeling) or Motion Graphics (a feature or number); "
         "story or storyboard approved first, then the finished video", g["video"]),
        ("user approves publishing (checked live link if the campaign needs one)", g["publish"]),
        ("publish and measure; results back to Business", "done" if RESULTS_HEAD in text else "later"),
    ]
    if not drafted:
        nxt = "run Business (`ult business --start-brief`), fill the build brief, then show it to the user"
    elif g["brief"] != "approved":
        nxt = ("show the build brief to the user and wait; on 'yes' run `ult gate approve brief \"<their words>\"`, "
               "on changes `ult gate revise brief \"<their words>\"` and send it back to Business")
    elif g["mockup"] != "approved":
        nxt = "send the approved brief to Website; bring its mockup back to the user before production code"
    elif g["publish"] != "approved":
        nxt = "Website builds; Social drafts; show the checked preview and the campaign, then ask about publishing"
    else:
        nxt = "publish what was approved, check the live result, then `ult gate done publish` and report results"
    return {"workflow": "launch", "gates": g, "steps": steps, "next": nxt,
            "load": ["shared/defaults.md", "skills/launch/SKILL.md"]}


def cmd_launch(args) -> int:
    root = Path(args.root).resolve() if args.root else project_root()
    b = board(root)
    if args.json:
        print(json.dumps(b, indent=2))
        return 0
    print("workflow: launch  manager: you, in the user's main chat")
    for n, (what, st) in enumerate(b["steps"], 1):
        print(f"{n}. {what}: {st}")
    print("rule: changes to an approved brief and every sign-off go through the Launch Manager")
    print(f"next: {b['next']}")
    print("load: " + ", ".join(b["load"]))
    if args.cat:
        print(cat_paths([plugin_file(f) for f in b["load"]]))
    return 0


# ---------------------------------------------------------------- business

def business_plan(task: str, root: Path) -> dict:
    text, _ = sanitize(task or "")
    if _LAUNCH_WORD_RE.search(text) or launch_active(root):
        mode, out = "launch", "a build brief in the shared brief, returned to the Launch Manager for the user's approval"
    elif _CHANGE_RE.search(text):
        mode, out = "change", "a hand-off to Website (or Work) covering only the change the user asked for"
    else:
        mode, out = "advice", "a recommendation in chat; no files, site or records are changed"
    return {"workflow": "business", "mode": mode, "output": out,
            "roles": ["researcher (Customer Research, Competitor Profiling)",
                      "marketing planner (Product Marketing, Offers)",
                      "analyst (Analytics, Conversion Tracking)"],
            "rules": ["label each point observed (with its source) or guessed",
                      "say what you accessed; with no connector, use public pages and the user's files"],
            "load": ["shared/defaults.md", "skills/business/SKILL.md"] + (
                ["skills/business/brief.md"] if mode == "launch" else [])}


def start_brief(root: Path) -> tuple[Path, bool]:
    if launch_active(root):
        return brief_path(root), False
    body = "\n".join(f"- {f}: " for f in BRIEF_FIELDS) + "\n\nStatus: draft (not approved)"
    return write_section(root, BRIEF_HEAD, body), True


def cmd_business(args) -> int:
    root = Path(args.root).resolve() if args.root else project_root()
    if args.start_brief:
        path, made = start_brief(root)
        print(f"{'started' if made else 'kept the existing'} {BRIEF_HEAD} in {path}; it is a draft until the user approves it")
        return 0
    p = business_plan(" ".join(args.task or []), root)
    if args.json:
        print(json.dumps(p, indent=2))
        return 0
    print(f"workflow: business  mode: {p['mode']}")
    print("roles: " + " -> ".join(p["roles"]))
    print(f"output: {p['output']}")
    for r in p["rules"]:
        print(f"rule: {r}")
    print("load: " + ", ".join(p["load"]))
    if args.cat:
        print(cat_paths([plugin_file(f) for f in p["load"]]))
    return 0


# ---------------------------------------------------------------- social

def social_plan(task: str, root: Path) -> dict:
    text, _ = sanitize(task or "")
    launch = launch_active(root)
    offer = status(root, "brief")[0] if launch else "not needed"
    video = bool(_VIDEO_RE.search(text))
    delivered = DELIVERED_HEAD in _brief_text(root)
    steps = ["content planner: one channel and why (Content Strategy)",
             "copywriter: posts, each with one clear next step (Social Content, Copywriting)",
             "analyst: what to measure and how each link is tracked (Analytics)"]
    if video:
        steps.append("video: " + ("checked export received (brief: Delivered video)" if delivered else
                                  "pick the style first: Brand Film when the message is a feeling and people "
                                  "carry it, Motion Graphics when it is a feature, a number or needs frequent "
                                  "updates; send one brief to that team and wait for its checked export"))
    steps += ["campaign reviewer: claims, links, tracking, AI labels", "user approves publishing"]
    return {"workflow": "social", "offer": offer, "video": video, "delivered": delivered,
            "needs_link": bool(_LINK_RE.search(text)) or launch, "steps": steps,
            "publish": status(root, "publish")[0],
            "load": ["shared/defaults.md", "skills/social-media/SKILL.md", "skills/social-media/campaign.md"]}


def cmd_social(args) -> int:
    root = Path(args.root).resolve() if args.root else project_root()
    if args.results is not None:
        if not args.results.strip():
            print("write what was measured (views, site visits, inquiries, bookings) or 'not available'")
            return 2
        path = write_section(root, RESULTS_HEAD, args.results)
        print(f"recorded results in {path}; Business and Launch read them to decide what to try next")
        return 0
    p = social_plan(" ".join(args.task or []), root)
    if args.json:
        print(json.dumps(p, indent=2))
        return 0
    print(f"workflow: social  offer: {p['offer']}  video: {'yes' if p['video'] else 'no'}")
    for n, s in enumerate(p["steps"], 1):
        print(f"{n}. {s}")
    if p["offer"] not in ("approved", "not needed"):
        print("wait: the launch brief is not approved yet; draft only from what the Launch Manager shares")
    gate = "publish: approved" if p["publish"] == "approved" else "publish: waiting for the user's yes"
    if p["needs_link"]:
        gate += "; check the live link first (`ult gate check publish --need-link`)"
    print(gate + "; no posting, sending, spending or customer-record changes before that")
    print("load: " + ", ".join(p["load"]))
    if args.cat:
        print(cat_paths([plugin_file(f) for f in p["load"]]))
    return 0


def register(sub):
    p = sub.add_parser("launch", help="Launch Manager board: steps, open approvals, the next step")
    p.add_argument("task", nargs="*")
    p.add_argument("--root")
    p.add_argument("--json", action="store_true")
    p.add_argument("--cat", action="store_true")
    p.set_defaults(func=cmd_launch)
    p = sub.add_parser("business", help="Business plan: advice, launch build brief, or scoped hand-off")
    p.add_argument("task", nargs="*")
    p.add_argument("--root")
    p.add_argument("--json", action="store_true")
    p.add_argument("--cat", action="store_true")
    p.add_argument("--start-brief", action="store_true", help="add an empty draft build brief to the shared brief")
    p.set_defaults(func=cmd_business)
    p = sub.add_parser("social", help="Social Media plan: channel, posts, video step, publish gate, results")
    p.add_argument("task", nargs="*")
    p.add_argument("--root")
    p.add_argument("--json", action="store_true")
    p.add_argument("--cat", action="store_true")
    p.add_argument("--results", metavar="TEXT", help="record what the campaign measured, for Business and Launch")
    p.set_defaults(func=cmd_social)
