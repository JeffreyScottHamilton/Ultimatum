"""`ult kitlint` — check React interaction components for the motion and access mistakes
that make animated UI feel cheap or lock people out.

    python3 kitlint.py PATH... [--json] [--strict]

PATH is a .tsx, .jsx, .ts or .js file, or a folder searched for them. Rules come from
website/references/craft/interaction-kit/details.md. A comment `kitlint-ok: RULE reason`
on the line or the line above silences that rule there. Failures exit 1; warnings are
listed but only fail with --strict. Exit 2 on bad arguments.
Standard library only, no network. It reads source text: a quick screen, not a
replacement for a typecheck, a browser render or an axe run.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SUFFIXES = {".tsx", ".jsx", ".ts", ".js"}
SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".next"}

MOTION_IMPORT = re.compile(r"""from\s+["'](?:motion(?:/react)?|framer-motion)["']""")
REDUCE = re.compile(r"useReducedMotion|prefers-reduced-motion|motion-reduce:|MotionConfig[^>]*reducedMotion")
CSS_MOVES = re.compile(r"\banimate-(?!none\b)[a-z]|\[animation:|@keyframes")
TRANSITION_ALL = re.compile(r"\btransition-all\b|transition:\s*['\"]?all\b|transition:\s*`all\b|transitionProperty:\s*['\"]all")
WILL_CHANGE_ALL = re.compile(r"will-change:\s*all|willChange:\s*['\"]all|will-change-\[all\]")
HEX = re.compile(r"""(?<![&\w/#-])#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})\b(?![\w-])""")
FUNC_COLOUR = re.compile(r"\b(?:rgba?|hsla?|oklch|oklab|lab|lch)\(\s*[\d.]")
TAP = re.compile(r"whileTap=\{\{[^}]*?\bscale:\s*(0?\.\d+|0|1(?:\.0+)?)")
ACTIVE_SCALE = re.compile(r"active:scale-(?:\[(0?\.\d+)\]|(\d+))\b")
OUTLINE_OFF = re.compile(r"(?<![\w:-])(?:focus:)?outline-none\b|outline:\s*['\"]?none")
FOCUS_BACK = re.compile(r"focus(?:-visible|-within)?:(?!outline-none)[\w\[]|focusRing|\bopacity-0\b|\bsr-only\b")
LABEL_ATTR = re.compile(r"\baria-label(?:ledby)?=|\btitle=")
# Children of a composite widget get their keys from the parent (a combobox input, a menu).
PARENT_KEYS = {"option", "menuitem", "menuitemradio", "menuitemcheckbox", "treeitem", "gridcell", "row", "tab"}
OK_MARK = re.compile(r"kitlint-ok:\s*([\w,-]+)")


def _strip_comments(text: str) -> str:
    """Blank out // and /* */ comments, keeping line numbers. Leaves strings alone."""
    out, i, n = [], 0, len(text)
    quote = None
    while i < n:
        c = text[i]
        if quote:
            out.append(c)
            if c == "\\" and i + 1 < n:
                out.append(text[i + 1]); i += 2; continue
            if c == quote:
                quote = None
            i += 1; continue
        if c in "\"'`":
            quote = c; out.append(c); i += 1; continue
        if text.startswith("//", i) and (i == 0 or text[i - 1] != ":"):
            j = text.find("\n", i)
            j = n if j < 0 else j
            i = j; continue
        if text.startswith("/*", i):
            j = text.find("*/", i + 2)
            j = n if j < 0 else j + 2
            out.append("".join("\n" if ch == "\n" else " " for ch in text[i:j]))
            i = j; continue
        out.append(c); i += 1
    return "".join(out)


def _tag_end(text: str, start: int) -> int:
    """Index just past the '>' closing the JSX opening tag at start, skipping {...} and strings."""
    depth, quote, i, n = 0, None, start + 1, len(text)
    while i < n:
        c = text[i]
        if quote:
            if c == "\\":
                i += 2; continue
            if c == quote:
                quote = None
        elif c in "\"'`":
            quote = c
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        elif c == ">" and depth == 0:
            return i + 1
        i += 1
    return n


def _tags(text: str, name: str):
    for m in re.finditer(rf"<{name}\b", text):
        end = _tag_end(text, m.start())
        yield m.start(), end, text[m.start():end]


def _line(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def lint_text(text: str) -> list[dict]:
    src = _strip_comments(text)
    found: list[dict] = []
    lines = text.splitlines()
    quiet: dict[int, set] = {}
    for i, ln in enumerate(lines, 1):
        for m in OK_MARK.finditer(ln):
            for r in m.group(1).split(","):
                quiet.setdefault(i, set()).add(r)
                quiet.setdefault(i + 1, set()).add(r)

    def add(rule, level, pos, msg):
        line = _line(src, pos)
        if rule in quiet.get(line, ()):
            return
        found.append({"rule": rule, "level": level, "line": line, "message": msg})

    moves = MOTION_IMPORT.search(src) or CSS_MOVES.search(src)
    if moves and not REDUCE.search(src):
        add("reduced-motion", "fail", moves.start(),
            "moves things but never checks reduced motion (useReducedMotion or motion-reduce:)")
    for m in TRANSITION_ALL.finditer(src):
        add("transition-all", "fail", m.start(), "transition-all animates layout too; name the properties")
    for m in WILL_CHANGE_ALL.finditer(src):
        add("will-change-all", "fail", m.start(), "will-change: all costs memory on every property")
    for m in HEX.finditer(src):
        if "mask" in src[src.rfind("\n", 0, m.start()) + 1:m.start()].lower():
            continue  # a mask reads alpha only; the colour is never seen
        add("raw-colour", "fail", m.start(), f"raw colour {m.group(0)}; use a theme token")
    for m in FUNC_COLOUR.finditer(src):
        add("raw-colour", "fail", m.start(), "colour function with literal numbers; use a theme token")
    for m in TAP.finditer(src):
        v = float(m.group(1))
        if v < 0.95:
            add("press-scale", "fail", m.start(), f"press scale {v} is a squash; keep it 0.95 to 0.98")
    for m in ACTIVE_SCALE.finditer(src):
        v = float(m.group(1)) if m.group(1) else int(m.group(2)) / 100
        if v < 0.95:
            add("press-scale", "fail", m.start(), f"active scale {v} is a squash; keep it 0.95 to 0.98")
    for name in ("div", "span", "li", "img", "motion\\.div", "motion\\.span", "motion\\.li"):
        for start, _end, tag in _tags(src, name):
            if not re.search(r"\bonClick=", tag) or re.search(r"aria-hidden=[\"{]+true", tag):
                continue  # aria-hidden: a pointer shortcut (a backdrop) beside a keyboard path such as Escape
            role = re.search(r"\brole=[\"']([\w-]+)", tag)
            if role and (role.group(1) in PARENT_KEYS or re.search(r"\bonKey(?:Down|Up)=", tag)):
                continue
            add("click-target", "fail", start,
                "onClick on a non-button with no role and key handler; use <button> or add both")
    for name in ("button", "motion\\.button"):
        for start, end, tag in _tags(src, name):
            if LABEL_ATTR.search(tag) or tag.endswith("/>"):
                continue
            close = re.compile(rf"</{name}\s*>").search(src, end)
            inner = src[end:close.start()] if close else ""
            visible = re.sub(r"<svg\b.*?</svg>", "", inner, flags=re.S)
            visible = re.sub(r"<[^>]*>", "", visible)
            if not visible.strip():
                add("icon-label", "fail", start, "icon-only button with no aria-label")
    for name in ("button", "a", "input", "select", "textarea", "div", "motion\\.button"):
        for start, _end, tag in _tags(src, name):
            if name in ("input", "select", "textarea") and "focus-within:" in src:
                continue  # a field inside a wrapper that draws the ring with focus-within
            if OUTLINE_OFF.search(tag) and not FOCUS_BACK.search(tag):
                add("focus-hidden", "fail", start, "outline removed with no visible focus style in its place")
    for start, _end, tag in _tags(src, "AnimatePresence"):
        if "initial={false}" not in tag:
            add("presence-initial", "warn", start,
                "AnimatePresence without initial={false} replays the enter animation on first paint")
    return found


def collect(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for p in paths:
        path = Path(p)
        if path.is_dir():
            for f in sorted(path.rglob("*")):
                if f.suffix in SUFFIXES and f.is_file() and not SKIP_DIRS.intersection(f.parts):
                    files.append(f)
        elif path.is_file():
            files.append(path)
        else:
            raise FileNotFoundError(p)
    return files


def run(paths: list[str], as_json: bool = False, strict: bool = False, out=sys.stdout) -> int:
    try:
        files = collect(paths)
    except FileNotFoundError as e:
        print(f"kitlint: no such path: {e}", file=sys.stderr)
        return 2
    report = []
    for f in files:
        for item in lint_text(f.read_text(encoding="utf-8", errors="replace")):
            report.append({"file": str(f), **item})
    fails = sum(1 for r in report if r["level"] == "fail")
    warns = len(report) - fails
    by_rule: dict[str, int] = {}
    for r in report:
        by_rule[r["rule"]] = by_rule.get(r["rule"], 0) + 1
    if as_json:
        json.dump({"files": len(files), "fail": fails, "warn": warns, "by_rule": by_rule, "findings": report}, out, indent=1)
        out.write("\n")
    else:
        for r in report:
            print(f"{r['file']}:{r['line']}: {r['level']} {r['rule']}: {r['message']}", file=out)
        rules = ", ".join(f"{k} {v}" for k, v in sorted(by_rule.items())) or "none"
        print(f"kitlint: {len(files)} files, {fails} fail, {warns} warn ({rules})", file=out)
    return 1 if fails or (strict and warns) else 0


def cmd_kitlint(args) -> int:
    return run(args.paths, args.json, args.strict)


def register(sub):
    p = sub.add_parser("kitlint", help="Check React interaction components: reduced motion, tokens, labels, press scale")
    p.add_argument("paths", nargs="+")
    p.add_argument("--json", action="store_true")
    p.add_argument("--strict", action="store_true", help="warnings fail too")
    p.set_defaults(func=cmd_kitlint)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(prog="kitlint")
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()
    sys.exit(run(a.paths, a.json, a.strict))
