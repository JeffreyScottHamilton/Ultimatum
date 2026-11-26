"""Hook variants and their real results, so the next post copies what worked.

  ult posts variant add ID --hook-type T --text "..." [--platform P] [--date D]
  ult posts variant result ID --views N [--saves N] [--shares N] [--clicks N] [--signups N] [--sales N]
  ult posts variant next
      ranks hook types by the numbers entered so far (signups, then clicks, then saves and shares per view)

Numbers come only from the platform's own analytics, typed in by a person or read through a connector.
Nothing is estimated: a variant with no result is listed as waiting.
"""
from __future__ import annotations

import json

from ultlib.common import state_dir

METRICS = ("views", "saves", "shares", "clicks", "signups", "sales")


def _path():
    return state_dir() / "variants.json"


def load() -> dict:
    p = _path()
    if not p.is_file():
        return {"variants": {}}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except ValueError:
        raise SystemExit(f"[ult] {p} is not valid JSON; fix or remove it")


def save(data: dict) -> None:
    _path().write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def cmd_add(args) -> int:
    data = load()
    if args.id in data["variants"]:
        print(f"variant {args.id} already exists")
        return 1
    data["variants"][args.id] = {"hook_type": args.hook_type, "text": args.text, "platform": args.platform or "",
                                 "date": args.date or "", "results": None}
    save(data)
    print(f"added {args.id} ({args.hook_type}); enter results after 48 hours with `ult posts variant result`")
    return 0


def cmd_result(args) -> int:
    data = load()
    v = data["variants"].get(args.id)
    if not v:
        print(f"no variant {args.id}; add it first")
        return 2
    v["results"] = {m: getattr(args, m) for m in METRICS if getattr(args, m) is not None}
    save(data)
    print(f"saved results for {args.id}")
    return 0


def rank(variants: dict) -> list[dict]:
    groups: dict[str, dict] = {}
    for v in variants.values():
        r = v.get("results")
        if not r or not r.get("views"):
            continue
        g = groups.setdefault(v["hook_type"], {"hook_type": v["hook_type"], "posts": 0, **{m: 0 for m in METRICS}})
        g["posts"] += 1
        for m in METRICS:
            g[m] += r.get(m, 0) or 0
    out = []
    for g in groups.values():
        per = lambda n: round(1000 * n / g["views"], 2)  # noqa: E731
        g.update(signups_per_1k=per(g["signups"]), clicks_per_1k=per(g["clicks"]),
                 saves_shares_per_1k=per(g["saves"] + g["shares"]))
        out.append(g)
    return sorted(out, key=lambda g: (g["signups_per_1k"], g["clicks_per_1k"], g["saves_shares_per_1k"]), reverse=True)


def cmd_next(args) -> int:
    variants = load()["variants"]
    waiting = [k for k, v in variants.items() if not (v.get("results") or {}).get("views")]
    ranked = rank(variants)
    if args.json:
        print(json.dumps({"ranked": ranked, "waiting": waiting}, indent=2))
        return 0
    if not ranked:
        print("no results yet: post the variants, then enter the platform's numbers with `variant result`")
    for i, g in enumerate(ranked, 1):
        print(f"{i}. {g['hook_type']}: {g['posts']} posts, {g['views']} views, signups/1k {g['signups_per_1k']}, "
              f"clicks/1k {g['clicks_per_1k']}, saves+shares/1k {g['saves_shares_per_1k']}")
    if ranked and ranked[0]["posts"] < 3:
        print("fewer than 3 posts behind the top hook type: treat it as a lead, not a winner")
    if waiting:
        print("waiting for results: " + ", ".join(waiting))
    if ranked:
        print(f"next: write 2 new hooks of type '{ranked[0]['hook_type']}' and 1 of a type not tried yet")
    return 0


def register(sub):
    v = sub.add_parser("variant", help="hook variants and their real results").add_subparsers(dest="vcmd", required=True)
    c = v.add_parser("add")
    c.add_argument("id")
    c.add_argument("--hook-type", required=True, help="e.g. question, number, before-after, mistake, story")
    c.add_argument("--text", required=True)
    c.add_argument("--platform")
    c.add_argument("--date")
    c.set_defaults(func=cmd_add)
    c = v.add_parser("result")
    c.add_argument("id")
    for m in METRICS:
        c.add_argument(f"--{m}", type=int, required=(m == "views"))
    c.set_defaults(func=cmd_result)
    c = v.add_parser("next")
    c.add_argument("--json", action="store_true")
    c.set_defaults(func=cmd_next)
