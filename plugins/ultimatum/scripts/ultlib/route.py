"""`ult route` — deterministic task router (no model call, standard library only).

Reads skills/work/modules.json, scores the task text against each module's
phrases, keywords, file globs and repo dependencies, and prints the route,
add-ons, the reference files to read, and the security overlay decision.

Scoring: phrase +3, keyword +2, file glob +2, repo dependency +3, never_when
phrase -3. Phrases and keywords match on word boundaries, case-insensitively.
Sentences that try to steer the router ("ignore your rules", "route to
release") are dropped before scoring: text inside a task is data.
"""
from __future__ import annotations

import fnmatch
import json
import os
import re
import sys
from pathlib import Path

from .common import project_root

PLUGIN = Path(__file__).resolve().parents[2]
MODULES_PATH = PLUGIN / "skills" / "work" / "modules.json"
REFS = PLUGIN / "skills" / "work" / "references"

PRIORITY = ["sec-fix", "sec-audit", "sec-review", "bug", "ci-pr", "release", "data-infra", "ui",
            "optimize", "handoff", "improve", "skill-eval", "mcp-build", "skill-author", "documents",
            "large", "feature", "discover", "small"]
SECURITY_ROUTES = {"sec-review", "sec-audit", "sec-fix"}
MAX_ADDONS = 2
THRESHOLD = 2
EVAL_ROUTE_MIN = 0.95
MODE_CHOICES = ("FAST", "STANDARD", "DEEP", "RECOVERY")

_RECOVERY_RE = re.compile(r"\b(resume|resuming|pick up (?:where|from|the work|again)|picking up (?:where|from)|after compaction|after the compaction|continue)\b", re.I)
_DEEP_RE = re.compile(r"\b(audit|thorough|deep)\b", re.I)
_PREFIX_RE = re.compile(r"^\s*(fast|deep)\s*:\s*", re.I)
_EDIT_RE = re.compile(r"\b(add|change|rename|remove|fix|update|set|replace|move|delete|bump|make|drop|correct|edit)\b", re.I)
_FILE_RE = re.compile(r"\b[\w./-]+\.(?:py|ts|tsx|js|jsx|mjs|md|json|css|scss|html|sql|go|rs|java|rb|ya?ml|toml|sh|txt)\b", re.I)
_CONCRETE_RE = re.compile(r"`|\b[\w./-]+\.(?:py|ts|tsx|js|jsx|md|json|css|html|sql|go|rs|java|rb|ya?ml|toml)\b|\b[a-z]+_[a-z_]+\b|\w+\(\)")

_cache: dict = {}
_rx_cache: dict = {}


def load_modules() -> list[dict]:
    if "mods" not in _cache:
        data = json.loads(MODULES_PATH.read_text(encoding="utf-8"))
        _cache["mods"] = data["modules"]
    return _cache["mods"]


def _by_id() -> dict:
    return {m["id"]: m for m in load_modules()}


def _rx(term: str) -> re.Pattern:
    if term not in _rx_cache:
        parts = [re.escape(p) for p in term.lower().split()]
        _rx_cache[term] = re.compile(r"(?<![a-z0-9_])" + r"\s+".join(parts) + r"(?![a-z0-9_])")
    return _rx_cache[term]


def _route_ids() -> list[str]:
    return [m["id"] for m in load_modules() if m["kind"] == "route"]


def _directive_re() -> re.Pattern:
    alts = "|".join(re.escape(r) for r in sorted(_route_ids(), key=len, reverse=True))
    return re.compile(
        r"ignore\s+(?:all\s+|any\s+|your\s+|the\s+|previous\s+|prior\s+|these\s+|my\s+)*"
        r"(?:rules|instructions|guidance|guidelines|system prompt)"
        r"|\b(?:route|routed|routing)\s+(?:this\s+|it\s+|the\s+task\s+)?(?:to|as|into)\s+(?:the\s+)?(?:route\s+)?(?:" + alts + r")\b"
        r"|\b(?:set|force|override)\s+(?:the\s+)?mode\b"
        r"|\b(?:use|pick|choose|select)\s+(?:the\s+)?(?:" + alts + r")\s+route\b",
        re.I)


def sanitize(task: str) -> tuple[str, int]:
    """Remove text that tries to steer the router. Returns (text, removed count)."""
    removed = 0

    def _cut(m: re.Match) -> str:
        nonlocal removed
        removed += 1
        return " "

    return _directive_re().sub(_cut, task), removed


def _package_deps(root: Path | None) -> set[str]:
    if root is None:
        return set()
    pkg = Path(root) / "package.json"
    try:
        data = json.loads(pkg.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return set()
    deps: set[str] = set()
    for key in ("dependencies", "devDependencies"):
        if isinstance(data.get(key), dict):
            deps.update(data[key].keys())
    return deps


def _score(mod: dict, text: str, base_tokens: list[str], deps: set[str]) -> tuple[int, list[str]]:
    a = mod.get("activate", {})
    score, hits = 0, []
    for p in a.get("phrases", []):
        if _rx(p).search(text):
            score += 3
            hits.append(p)
    for k in a.get("keywords", []):
        if _rx(k).search(text):
            score += 2
            hits.append(k)
    for k in a.get("weak", []):
        if _rx(k).search(text):
            score += 1
            hits.append(k)
    for pat in a.get("files", []):
        if any(fnmatch.fnmatchcase(t, pat.lower()) for t in base_tokens):
            score += 2
            hits.append(pat)
    for d in a.get("deps", []):
        if d in deps:
            score += 3
            hits.append(f"dep:{d}")
    for n in mod.get("never_when", []):
        if _rx(n).search(text):
            score -= 3
    return score, hits


def _file_tokens(task: str) -> list[str]:
    out = []
    for raw in re.split(r"\s+", task):
        tok = raw.strip("`'\"()<>[]{},;:!?").lower()
        if tok:
            out.append(tok.split("/")[-1])
    return out


def _tokens_for(files: list[str]) -> int:
    total = 0
    for f in files:
        p = REFS / f
        if p.is_file():
            total += p.stat().st_size
    return total // 4


def _fmt_tokens(n: int) -> str:
    return f"~{n / 1000:.1f}k tokens" if n >= 1000 else f"~{n} tokens"


def _handoff_exists(root: Path) -> bool:
    base = os.environ.get("ULTIMATUM_STATE_DIR")
    base_path = Path(base) if base else root / ".ultimatum"
    return (base_path / "handoff.md").is_file()


def decide(task: str, root: Path | None = None, use_deps: bool = True, lessons_on: bool = True) -> dict:
    """Route one task. Pure function apart from reading modules.json and package.json."""
    raw = task or ""
    forced = None
    m = _PREFIX_RE.match(raw)
    if m:
        forced = m.group(1).upper()
        raw = raw[m.end():]
    text, dropped = sanitize(raw)
    low = text.lower()
    tokens = _file_tokens(text)
    deps = _package_deps(root) if use_deps else set()
    mods = load_modules()

    route_scores = []
    for mod in mods:
        if mod["kind"] != "route":
            continue
        s, _ = _score(mod, low, tokens, deps)
        route_scores.append((s, mod["id"]))
    # One named file plus an edit verb is a local edit, unless another route has real evidence.
    files = {mm.group(0).lower() for mm in _FILE_RE.finditer(text)}
    top_other = max((sc for sc, rid in route_scores if rid != "small"), default=0)
    if len(files) == 1 and _EDIT_RE.search(text) and len(text.split()) <= 25 and top_other < 4:
        route_scores = [(max(sc, THRESHOLD) if rid == "small" else sc, rid) for sc, rid in route_scores]
    route_scores.sort(key=lambda x: (-x[0], PRIORITY.index(x[1])))

    by = _by_id()
    default = False
    empty = not text.strip()
    if empty and root is not None and _handoff_exists(root):
        route = "handoff"
        alt = None
    elif route_scores[0][0] >= THRESHOLD:
        route = route_scores[0][1]
        second = route_scores[1] if len(route_scores) > 1 else None
        alt = second[1] if second and second[0] >= THRESHOLD and route_scores[0][0] - second[0] <= 2 else None
    else:
        default = True
        alt = None
        route = "small" if (len(text.split()) <= 15 and _CONCRETE_RE.search(text) and _EDIT_RE.search(text)) else "feature"

    # Add-ons: score, then honour requires/conflicts for the chosen route.
    addon_cands = []
    for mod in mods:
        if mod["kind"] != "addon":
            continue
        if mod.get("requires") and route not in mod["requires"]:
            continue
        if route in mod.get("conflicts", []):
            continue
        s, hits = _score(mod, low, tokens, deps)
        if s >= THRESHOLD:
            addon_cands.append((s, mod["id"]))
    addon_cands.sort(key=lambda x: (-x[0], x[1]))
    addons = [aid for _, aid in addon_cands[:MAX_ADDONS]]

    # Security overlay: never on the sec routes, which already cover it.
    sec_score, sec_hits = _score(by["security"], low, tokens, deps)
    overlay = sec_score >= THRESHOLD and route not in SECURITY_ROUTES and route != "discover"
    touches = [h for h in sec_hits if not h.startswith("dep:")][:3] if overlay else []

    # Mode.
    recovery = bool(_RECOVERY_RE.search(text)) or (empty and root is not None and _handoff_exists(root))
    if forced:
        mode = forced
    elif recovery:
        mode = "RECOVERY"
    elif _DEEP_RE.search(text):
        mode = "DEEP"
    else:
        hint = by[route].get("mode_hint", "STANDARD")
        mode = hint if hint in MODE_CHOICES else "STANDARD"
        if mode == "FAST" and overlay:
            mode = "STANDARD"
        if mode == "RECOVERY":
            mode = "STANDARD"

    read: list[str] = list(by[route].get("read", []))
    for aid in addons:
        read.extend(by[aid].get("read", []))
    read = list(dict.fromkeys(read))

    lessons: list[str] = []
    if lessons_on and root is not None and text.strip():
        try:
            from .learn import relevant  # type: ignore
            lessons = [str(x)[:120] for x in relevant(task, root, limit=3)][:3]
        except Exception:  # learn is optional; skip silently
            lessons = []

    return {
        "mode": mode,
        "route": route,
        "addons": addons,
        "read": read,
        "tokens": _tokens_for(read),
        "overlay": overlay,
        "touches": touches,
        "alt": alt,
        "low_confidence": alt is not None,
        "default": default,
        "lessons": lessons,
        "dropped_directives": dropped,
    }


def format_text(d: dict) -> str:
    head = f"mode: {d['mode']}  route: {d['route']}"
    if d["addons"]:
        head += "  +: " + ", ".join(d["addons"])
    lines = [head]
    if d["read"]:
        lines.append(f"read: {', '.join(d['read'])} ({_fmt_tokens(d['tokens'])})")
    else:
        lines.append("read: none")
    if d["overlay"]:
        t = f" (touches: {', '.join(d['touches'])})" if d["touches"] else ""
        lines.append(f"overlay: security{t}")
    else:
        lines.append("overlay: none")
    if d["alt"]:
        lines.append(f"alt: {d['alt']} (low confidence)")
    if d["lessons"]:
        lines.append("lessons: " + " | ".join(d["lessons"]))
    return "\n".join(lines[:6])


def format_list() -> str:
    rows = []
    for m in load_modules():
        tok = _tokens_for(m.get("read", []))
        rows.append(f"{m['id']:<14} {m['kind']:<8} ~{tok} tok  {m.get('summary', '')[:60]}")
    return "\n".join(rows)


def run_eval(path: Path, root: Path | None) -> tuple[str, bool]:
    cases = []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.strip():
            try:
                cases.append(json.loads(line))
            except ValueError as e:
                raise SystemExit(f"[ult route] {path}:{n}: bad JSON ({e})")
    total = len(cases)
    r_ok = o_ok = a_ok = 0
    m_total = m_ok = 0
    fails = []
    for c in cases:
        d = decide(c["task"], root=root, use_deps=root is not None, lessons_on=False)
        want_route = c["route"]
        want_add = sorted(c.get("addons", []))
        want_ov = bool(c.get("overlay", False))
        if d["route"] == want_route:
            r_ok += 1
        else:
            fails.append(f"route: {c['task'][:70]!r} want={want_route} got={d['route']}")
        if d["overlay"] == want_ov:
            o_ok += 1
        else:
            fails.append(f"overlay: {c['task'][:70]!r} want={want_ov} got={d['overlay']}")
        if sorted(d["addons"]) == want_add:
            a_ok += 1
        if "mode" in c:
            m_total += 1
            m_ok += d["mode"] == c["mode"]
    route_acc = r_ok / total if total else 0.0
    ov_acc = o_ok / total if total else 0.0
    out = [f"cases: {total}",
           f"route: {route_acc:.3f} ({r_ok}/{total})",
           f"overlay: {ov_acc:.3f} ({o_ok}/{total})",
           f"addons: {a_ok / total if total else 0:.3f} ({a_ok}/{total})"]
    if m_total:
        out.append(f"mode: {m_ok / m_total:.3f} ({m_ok}/{m_total})")
    out.extend(fails[:30])
    ok = route_acc >= EVAL_ROUTE_MIN and ov_acc >= 1.0
    return "\n".join(out), ok


def cmd_route(args) -> int:
    if args.list:
        print(format_list())
        return 0
    if args.eval:
        root = Path(args.root).resolve() if args.root else None
        ev = Path(args.eval)
        if not ev.is_file():
            print(f"[ult route] no such eval file: {ev}", file=sys.stderr)
            return 2
        text, ok = run_eval(ev, root)
        print(text)
        return 0 if ok else 1
    task = " ".join(args.task or []).strip()
    root = Path(args.root).resolve() if args.root else project_root()
    d = decide(task, root=root)
    if args.json:
        print(json.dumps(d, indent=2, ensure_ascii=False))
    else:
        print(format_text(d))
    return 0


def register(sub):
    p = sub.add_parser("route", help="mode, route, add-ons, files to read and overlay for a task")
    p.add_argument("task", nargs="*", help="the task text (quote it)")
    p.add_argument("--root", help="project directory (package.json deps add add-ons)")
    p.add_argument("--json", action="store_true", help="machine-readable output")
    p.add_argument("--eval", metavar="FILE", help="score JSONL cases; exit 1 below thresholds")
    p.add_argument("--list", action="store_true", help="one line per module: id, kind, tokens, summary")
    p.set_defaults(func=cmd_route)
