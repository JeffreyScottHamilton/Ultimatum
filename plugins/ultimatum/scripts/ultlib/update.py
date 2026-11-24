"""`ult update` — versions, auto-update setup and local state migration.

  ult update status            running version, marketplace copy, auto-update, next step
  ult update setup [--apply]   one-time steps; --apply turns on auto-update for the
                               ultimatum marketplace in ~/.claude/settings.json
  ult update migrate           idempotent upgrade of .ultimatum/ state (no-op if nothing to do)

Claude Code's own marketplace updater does the actual installs. This module only
reads versions and, with --apply, edits one key in settings.json: other keys are
preserved, the file is backed up first, and a second run changes nothing.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import time
from pathlib import Path

from .common import project_root, state_dir, write_private

PLUGIN_ROOT = Path(__file__).resolve().parents[2]
MARKET = "ultimatum"
REPO = "JeffreyScottHamilton/Ultimatum"
KNOWLEDGE_SKELETON = (
    "# Project knowledge\n\n"
    "Commands, conventions and gotchas for this repository (40 lines or fewer). "
    "Bullets starting with `- ` are shown to the model by `ult route` when relevant.\n"
)


def claude_home() -> Path:
    return Path.home() / ".claude"


def settings_path() -> Path:
    return claude_home() / "settings.json"


def running_version() -> str:
    try:
        return str(json.loads((PLUGIN_ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))["version"])
    except (OSError, ValueError, KeyError, TypeError):
        return "unknown"


def _vt(v: str) -> tuple:
    nums = [int(x) for x in re.findall(r"\d+", v)[:3]]
    return tuple(nums + [0] * (3 - len(nums)))


def marketplace_copies() -> list[tuple[str, str]]:
    """(path, version) for ultimatum copies under ~/.claude/plugins/marketplaces."""
    base = claude_home() / "plugins" / "marketplaces"
    cands = list(base.glob("*/plugins/ultimatum/.claude-plugin/plugin.json"))
    cands += list(base.glob("*/.claude-plugin/plugin.json"))
    out = []
    for f in cands:
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if isinstance(d, dict) and d.get("name") == "ultimatum" and isinstance(d.get("version"), str):
            out.append((str(f.parent.parent), d["version"]))
    return sorted(out, key=lambda x: _vt(x[1]), reverse=True)


def _load_settings():
    """(dict or None, error). None dict means the file is absent."""
    p = settings_path()
    if not p.exists():
        return {}, None
    if p.is_symlink():
        return None, "settings.json is a symlink; not changed"
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None, "settings.json is not valid JSON; not changed"
    if not isinstance(d, dict):
        return None, "settings.json is not a JSON object; not changed"
    return d, None


def auto_update_state() -> str:
    d, err = _load_settings()
    if err:
        return "unknown"
    markets = d.get("extraKnownMarketplaces")
    entry = markets.get(MARKET) if isinstance(markets, dict) else None
    if not isinstance(entry, dict) or "autoUpdate" not in entry:
        return "not set"
    return "on" if entry["autoUpdate"] is True else "off"


def cmd_status(args) -> int:
    run = running_version()
    copies = marketplace_copies()
    auto = auto_update_state()
    print(f"[ult update] running: {run}")
    if copies:
        print(f"[ult update] marketplace copy: {copies[0][1]} (found under ~/.claude/plugins)")
    else:
        print("[ult update] marketplace copy: not found under ~/.claude/plugins")
    print(f"[ult update] auto-update ({MARKET} marketplace): {auto}")
    if copies and _vt(copies[0][1]) > _vt(run):
        nxt = "run /reload-plugins to load the newer copy"
    elif auto != "on":
        nxt = "run `ult update setup --apply` (or switch on auto-update in /plugin)"
    else:
        nxt = "none; up to date"
    print(f"next: {nxt}")
    return 0


SETUP_TEXT = [
    "[ult update] one-time setup",
    "1. Local CLI: run `ult update setup --apply` (sets auto-update for the ultimatum marketplace; backs up settings.json),",
    "   or /plugin > Marketplaces > ultimatum > enable auto-update.",
    "2. Cloud: install or update Ultimatum at claude.ai/customize/plugins (cloud ignores repo settings).",
    "3. Running sessions: run /reload-plugins after an update.",
]


def apply_setup() -> int:
    d, err = _load_settings()
    if err:
        print(f"[ult update] {err}")
        return 1
    markets = d.get("extraKnownMarketplaces", {})
    if not isinstance(markets, dict):
        print("[ult update] extraKnownMarketplaces is not an object; not changed")
        return 1
    entry = markets.get(MARKET)
    if entry is None:
        entry = {"source": {"source": "github", "repo": REPO}, "autoUpdate": True}
    elif isinstance(entry, dict):
        if entry.get("autoUpdate") is True:
            print("[ult update] auto-update already on for the ultimatum marketplace; no change")
            return 0
        entry["autoUpdate"] = True
    else:
        print("[ult update] extraKnownMarketplaces.ultimatum is not an object; not changed")
        return 1
    path = settings_path()
    backup = None
    if path.exists():
        backup = path.with_name(f"settings.json.bak-{time.strftime('%Y%m%d-%H%M%S')}")
        n = 1
        while backup.exists():
            backup = path.with_name(f"settings.json.bak-{time.strftime('%Y%m%d-%H%M%S')}-{n}")
            n += 1
        shutil.copy2(path, backup)
    markets[MARKET] = entry
    d["extraKnownMarketplaces"] = markets
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".ult-tmp")
    tmp.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if path.exists():
        shutil.copymode(path, tmp)
    os.replace(tmp, path)
    note = f"; backup {backup.name}" if backup else ""
    print(f"[ult update] auto-update on for the ultimatum marketplace in settings.json{note}")
    return 0


def cmd_setup(args) -> int:
    if args.apply:
        return apply_setup()
    print("\n".join(SETUP_TEXT))
    return 0


def migrate(root=None) -> list[str]:
    """Create the 2.0 files that 0.4.x projects lack. Never rewrites existing content."""
    changes = []
    d = state_dir(root)
    k = d / "knowledge.md"
    if not k.exists() and not k.is_symlink():
        write_private(k, KNOWLEDGE_SKELETON)
        changes.append("created knowledge.md")
    props = d / "proposals"
    if not props.exists():
        props.mkdir(mode=0o700)
        changes.append("created proposals/")
    return changes


def cmd_migrate(args) -> int:
    changes = migrate(project_root())
    if not changes:
        print("migrate: nothing to do")
    else:
        print("migrate: " + "; ".join(changes))
    return 0


def register(sub):
    p = sub.add_parser("update", help="versions, auto-update setup, local state migration")
    us = p.add_subparsers(dest="action", required=True)
    s = us.add_parser("status", help="running vs marketplace version and auto-update state")
    s.set_defaults(func=cmd_status)
    st = us.add_parser("setup", help="one-time update steps; --apply turns on auto-update")
    st.add_argument("--apply", action="store_true", help="set autoUpdate in ~/.claude/settings.json (backed up)")
    st.set_defaults(func=cmd_setup)
    m = us.add_parser("migrate", help="upgrade .ultimatum/ state from 0.x (idempotent)")
    m.set_defaults(func=cmd_migrate)
