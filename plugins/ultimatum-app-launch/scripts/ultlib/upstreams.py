"""`ult upstreams [--json]` - upstream sources, pins, licences and decisions.

Lists the bundled data/upstreams.json. Read-only and offline. Updating pins
is a maintainer task done with git outside the toolbelt.
"""
from __future__ import annotations

import json
from pathlib import Path

from .common import dump_json

DATA = Path(__file__).resolve().parents[2] / "data" / "upstreams.json"


def load(path: Path = DATA) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))["upstreams"]


def _short_repo(url: str) -> str:
    return url.split("github.com/", 1)[-1]


def _short_licence(text: str, width: int = 28) -> str:
    return text if len(text) <= width else text[: width - 1] + "~"


def format_text(entries: list[dict]) -> str:
    lines = [f"upstreams: {len(entries)} (decision: adapt | adapter | skip; full fields with --json)"]
    for e in entries:
        modules = ",".join(e["modules"]) or "-"
        lines.append(
            f"{e['id']:<24} {e['decision']:<8} {e['pin']:<8} {_short_repo(e['repo']):<42} "
            f"{_short_licence(e['licence']):<28} {modules}"
        )
    return "\n".join(lines)


def cmd_upstreams(args) -> int:
    entries = load()
    if args.json:
        print(dump_json(entries))
        return 0
    print(format_text(entries))
    return 0


def register(sub):
    p = sub.add_parser("upstreams", help="upstream sources, pins, licences and decisions")
    p.add_argument("--json", action="store_true", help="machine-readable output")
    p.set_defaults(func=cmd_upstreams)
