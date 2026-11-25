"""`ult style` — opt-in: copy Ultimatum's shared defaults into a CLAUDE.md for normal chats.

Writes only between two marker lines and leaves every other byte of the file as it was.
Nothing changes without `apply`; `remove` takes the block out again.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[2]
DEFAULTS = PLUGIN / "shared" / "defaults.md"
BEGIN = "<!-- ultimatum:style begin (managed by `ult style`; edit outside these lines) -->"
END = "<!-- ultimatum:style end -->"
_BLOCK_RE = re.compile(r"<!-- ultimatum:style begin[^\n]*-->\n.*?<!-- ultimatum:style end -->\n?", re.S)


def default_target() -> Path:
    return Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude") / "CLAUDE.md"


def block() -> str:
    body = DEFAULTS.read_text(encoding="utf-8").strip()
    body = re.sub(r"^# Shared defaults[^\n]*", "## Ultimatum shared style", body, count=1)
    return f"{BEGIN}\n{body}\n{END}\n"


def status(path: Path) -> str:
    if not path.is_file():
        return f"not set: {path} does not exist (apply creates it)"
    text = path.read_text(encoding="utf-8")
    if not _BLOCK_RE.search(text):
        return f"not set: {path} has no Ultimatum style block"
    return f"on: {path}" + ("" if block().strip() in text else " (older text; apply refreshes it)")


def apply(path: Path) -> str:
    old = path.read_text(encoding="utf-8") if path.is_file() else ""
    if _BLOCK_RE.search(old):
        new = _BLOCK_RE.sub(lambda _m: block(), old, count=1)
    elif not old:
        new = block()
    else:
        new = (old if old.endswith("\n") else old + "\n") + "\n" + block()
    if new == old:
        return f"unchanged: {path}"
    path.parent.mkdir(parents=True, exist_ok=True)
    backup = path.with_name(path.name + ".ultimatum-backup")
    if old and not backup.exists():
        backup.write_text(old, encoding="utf-8")
    path.write_text(new, encoding="utf-8")
    return f"applied: {path} (your other text is unchanged)"


def remove(path: Path) -> str:
    old = path.read_text(encoding="utf-8") if path.is_file() else ""
    m = _BLOCK_RE.search(old)
    if not m:
        return f"nothing to remove: {path}"
    prefix, suffix = old[:m.start()], old[m.end():]
    if prefix.endswith("\n\n"):
        prefix = prefix[:-1]
    path.write_text(prefix + suffix, encoding="utf-8")
    return f"removed: {path}"


def cmd_style(args) -> int:
    path = Path(args.file).expanduser() if args.file else default_target()
    fn = {"status": status, "apply": apply, "remove": remove}[args.action]
    print(f"[ult style] {fn(path)}")
    return 0


def register(sub):
    p = sub.add_parser("style", help="opt-in: add Ultimatum's shared answer style to ~/.claude/CLAUDE.md")
    p.add_argument("action", choices=("status", "apply", "remove"))
    p.add_argument("--file", help="CLAUDE.md to manage (default: ~/.claude/CLAUDE.md)")
    p.set_defaults(func=cmd_style)
