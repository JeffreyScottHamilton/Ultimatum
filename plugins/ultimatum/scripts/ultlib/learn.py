"""`ult learn` — local lessons, observations and improvement proposals.

Stores (JSON lines or markdown, written with write_private):
- global lessons:   $ULTIMATUM_HOME/lessons.jsonl (default ~/.ultimatum)
- project lessons:  state_dir()/lessons.jsonl
- project notes:    state_dir()/knowledge.md (read here, edited by hand or by sync)
- observations:     state_dir()/observations.jsonl (counts and categories only)
- proposals:        state_dir()/proposals/<id>.json and .md (allow-listed fields only)

Lesson text is untrusted. It is cleaned (control characters removed), redacted,
capped at 200 characters and shown prefixed with "lesson:" so it reads as data.
Nothing in this module grants permissions or changes configuration.

Privacy boundary (tested in tests/test_learn.py): observations never hold prompt
text, paths, commands beyond a known tool name, or tool output. Proposals are
built only from the fields in PROPOSAL_FIELDS and fixed template sentences.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import time
import unicodedata
from collections import defaultdict
from pathlib import Path

from . import usage
from .common import new_id, project_root, redact, safe_id, state_dir, write_private
from .context import current_transcript

LESSON_CAP = 200          # lessons kept per store
LESSON_MAX_CHARS = 200
EXPIRE_SECONDS = 180 * 86400
RELEVANT_MAX_CHARS = 120
RELEVANT_MAX_LINES = 3
TAIL_BYTES = 2_000_000    # hook reads only the end of a transcript
MAX_OBSERVATIONS = 1000
PROPOSE_MIN_SESSIONS = 3
PROPOSE_MIN_OCCURRENCES = 5
LIST_CAP = 20

MODULE_RE = re.compile(r"^[a-z][a-z0-9-]{0,39}$")
SESSION_RE = re.compile(r"^[0-9a-f]{12}$")
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]{1,30})?$")

ROUTES = {"small", "discover", "feature", "large", "bug", "ci-pr", "ui", "data-infra", "optimize",
          "release", "sec-review", "sec-audit", "sec-fix", "handoff", "improve", "skill-eval",
          "documents", "mcp-build", "skill-author"}
ROUTE_RE = re.compile(r"\broute:\s*([a-z][a-z-]{1,30})")

# Command kinds we will ever record. Anything else is recorded as "other",
# so a path, a token or a repo name in a command never reaches a store.
CMD_KINDS = {"npm", "pnpm", "yarn", "npx", "node", "python", "python3", "pytest", "pip", "pip3",
             "go", "cargo", "make", "mvn", "gradle", "dotnet", "git", "tsc", "eslint", "ruff",
             "mypy", "jest", "vitest", "bundle", "rake", "rspec", "php", "composer", "gcc", "cc",
             "clang", "javac", "swift", "xcodebuild", "ult", "docker", "terraform", "bash", "sh"}

# Observation signals -> the module a lesson about them would belong to.
SIGNAL_MODULE = {
    "repeated-failure": "debugging",
    "re-read": "context",
    "big-output": "context",
    "correction": "engineering",
    "search-churn": "discovery",
    "arch-cycle": "architecture",
    "arch-dup": "architecture",
    "arch-size": "architecture",
    "arch-stub": "architecture",
    "poll-sleep": "context",
    "raw-test-output": "context",
    "reread": "context",
}

# Fixed sentences for architecture signals recorded by `ult arch check --record`.
ARCH_TEMPLATES = {
    "arch-cycle": "Before adding an import between modules, check `ult arch check --changed` so no new dependency cycle appears.",
    "arch-dup": "Before writing a helper, search for an existing one and extend it instead of copying its body.",
    "arch-size": "When a file or function grows past the size limit, split it along one responsibility before adding more.",
    "arch-stub": "Do not leave placeholder code: finish the implementation or remove the stub before reporting done.",
}
# Token-waste signals counted from a session's own transcript (counts only), one fixed sentence each.
WASTE_TEMPLATES = {
    "poll-sleep": "Do not poll with sleep or Monitor; run the command in the foreground or wait for its completion notice.",
    "raw-test-output": "Run noisy test commands through `ult run` so only the summary and failing lines enter the chat.",
    "reread": "Keep what a file said in the notes you already have instead of reading the same file again.",
}
RAW_TEST_BYTES = 8192
TEST_CMD_RE = re.compile(r"\b(pytest|unittest|jest|vitest|rspec|phpunit)\b|\b(npm|pnpm|yarn)\s+(run\s+)?test\b"
                         r"|\bgo\s+test\b|\bcargo\s+test\b|\bmvn\s+test\b|\bgradle\s+test\b|\bmake\s+test\b")
SLEEP_RE = re.compile(r"(^|[;&|\s])sleep\s+\d")
CAT_RE = re.compile(r"^\s*cat\s+(?:-\S+\s+)*(\S+)\s*$")
ARCH_SIGNALS = {"cycle": "arch-cycle", "dup": "arch-dup", "size": "arch-size", "func-size": "arch-size", "stub": "arch-stub"}

# Fixed template sentences, keyed by task category. Proposals use only these.
TEMPLATES = {
    "security": "For security work, name the trust boundary first and tie each finding to one file and one reproducible check.",
    "ci-pr": "When fixing CI, read the first error line of the failing job instead of re-running the whole pipeline.",
    "bug": "Before editing for a failing check, record the one command that reproduces it and re-run only that command after each edit.",
    "ui": "For UI changes, check the rendered page at the target width before reporting the task done.",
    "test": "When adding tests, run the new test alone first, then the nearest suite.",
    "refactor": "For refactors, keep behaviour checks green at each step and do not mix renames with logic changes.",
    "docs": "For docs changes, check that every command quoted in the text still runs.",
    "discover": "For exploration, use the repo map and symbol search before reading whole files.",
    "feature": "For new features, write the smallest failing test first and keep the change to the named files.",
    "other": "Name the check that proves the task is done before editing, and run it after the last change.",
    "unknown": "Name the check that proves the task is done before editing, and run it after the last change.",
}
CATEGORY_SET = {name for name, _ in usage.CATEGORIES} | {"other", "unknown"}
PROPOSAL_FIELDS = {"id", "created", "plugin_version", "module", "signal", "category", "counts", "lesson"}

STOP = {"the", "and", "for", "with", "that", "this", "from", "into", "when", "what", "where", "how",
        "make", "use", "add", "fix", "need", "want", "please", "just", "not", "are", "was", "can",
        "you", "your", "file", "files", "should", "does", "have", "has", "will", "all", "any"}
WORD_RE = re.compile(r"[a-z][a-z0-9_]{2,}")


# --------------------------------------------------------------------------
# Locations and cleaning
# --------------------------------------------------------------------------

def global_home() -> Path:
    return Path(os.environ.get("ULTIMATUM_HOME") or (Path.home() / ".ultimatum"))


def _mkdir_private(d: Path) -> Path:
    if d.is_symlink():
        raise ValueError(f"refusing to use {d}: it is a symlink")
    d.mkdir(mode=0o700, parents=True, exist_ok=True)
    return d


def _project_store(root) -> Path:
    """Read-only twin of state_dir(): never creates directories or files."""
    ext = os.environ.get("ULTIMATUM_STATE_DIR")
    if ext:
        return Path(ext).resolve()
    return Path(root) / ".ultimatum"


def clean_lesson(text) -> str:
    """Strip control and format characters, collapse whitespace, redact, cap."""
    if not isinstance(text, str):
        return ""
    out = "".join(" " if unicodedata.category(ch).startswith("C") else ch for ch in text)
    out = redact(" ".join(out.split()))
    if len(out) > LESSON_MAX_CHARS:
        out = out[: LESSON_MAX_CHARS - 3].rstrip() + "..."
    return out


def lesson_id(text: str) -> str:
    return "L" + hashlib.sha1(text.lower().encode("utf-8")).hexdigest()[:10]


def _module_or_none(value):
    if isinstance(value, str) and MODULE_RE.match(value):
        return value
    return None


def _num(value, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _count(value) -> int:
    try:
        return max(1, min(1_000_000, int(value)))
    except (TypeError, ValueError):
        return 1


# --------------------------------------------------------------------------
# Lesson store
# --------------------------------------------------------------------------

def load_lessons(path: Path) -> list[dict]:
    """Records from a JSON-lines store. Missing, symlinked or bad lines are skipped."""
    if not path.is_file() or path.is_symlink():
        return []
    now = time.time()
    out = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            d = json.loads(line)
        except ValueError:
            continue
        if not isinstance(d, dict):
            continue
        text = clean_lesson(d.get("text"))
        if not text:
            continue
        out.append({"id": lesson_id(text), "text": text, "module": _module_or_none(d.get("module")),
                    "count": _count(d.get("count")), "created": _num(d.get("created"), now),
                    "updated": _num(d.get("updated"), now)})
    return out


def write_lessons(path: Path, records: list[dict]) -> None:
    body = "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in records)
    write_private(path, body)


def prune(records: list[dict], now: float | None = None) -> list[dict]:
    """Drop expired single-use lessons, then the lowest-count oldest ones over the cap."""
    now = now or time.time()
    keep = [r for r in records if not (r["count"] <= 1 and now - r["updated"] > EXPIRE_SECONDS)]
    if len(keep) > LESSON_CAP:
        drop = sorted(keep, key=lambda r: (r["count"], r["updated"]))[: len(keep) - LESSON_CAP]
        dropped = {id(r) for r in drop}
        keep = [r for r in keep if id(r) not in dropped]
    return keep


def store_path(scope: str, root=None) -> Path:
    if scope == "global":
        return _mkdir_private(global_home()) / "lessons.jsonl"
    if scope == "project":
        return state_dir(root) / "lessons.jsonl"
    raise ValueError(f"unknown scope: {scope}")


def add_lesson(text: str, scope: str = "project", module: str | None = None, root=None) -> dict:
    cleaned = clean_lesson(text)
    if not cleaned:
        raise ValueError("empty lesson")
    if module and not _module_or_none(module):
        raise ValueError(f"invalid module id: {module!r}")
    path = store_path(scope, root)
    records = load_lessons(path)
    lid = lesson_id(cleaned)
    now = time.time()
    hit = next((r for r in records if r["id"] == lid), None)
    if hit:
        hit["count"] += 1
        hit["updated"] = now
        hit["module"] = _module_or_none(module) or hit["module"]
    else:
        hit = {"id": lid, "text": cleaned, "module": _module_or_none(module), "count": 1,
               "created": now, "updated": now}
        records.append(hit)
    write_lessons(path, prune(records, now))
    return hit


def relevant(task: str, root, limit: int = 3) -> list[str]:
    """Up to 3 one-line lessons whose words overlap the task. Never raises."""
    try:
        return _relevant(task, root, limit)
    except Exception:
        return []


def _knowledge_lines(store: Path) -> list[str]:
    k = store / "knowledge.md"
    if not k.is_file() or k.is_symlink():
        return []
    lines = k.read_text(encoding="utf-8", errors="replace").splitlines()[:40]
    return [clean_lesson(l[2:]) for l in lines if l.startswith("- ")]


def _words(text: str) -> set[str]:
    return {w for w in WORD_RE.findall(text.lower()) if w not in STOP}


def _relevant(task, root, limit) -> list[str]:
    n = max(0, min(int(limit), RELEVANT_MAX_LINES))
    if not n or not isinstance(task, str):
        return []
    want = _words(task[:2000])
    if not want:
        return []
    root = Path(root) if root is not None else project_root()
    store = _project_store(root)
    cands = [(r["text"], r["count"], r["updated"]) for r in load_lessons(store / "lessons.jsonl")]
    cands += [(r["text"], r["count"], r["updated"]) for r in load_lessons(global_home() / "lessons.jsonl")]
    cands += [(t, 1, 0.0) for t in _knowledge_lines(store) if t]
    scored, seen = [], set()
    for text, count, updated in cands:
        score = len(want & _words(text))
        if score and text not in seen:
            seen.add(text)
            scored.append((score, count, updated, text))
    scored.sort(key=lambda x: (-x[0], -x[1], -x[2]))
    out = []
    for *_, text in scored[:n]:
        line = f"lesson: {text}"
        if len(line) > RELEVANT_MAX_CHARS:
            line = line[: RELEVANT_MAX_CHARS - 3].rstrip() + "..."
        out.append(line)
    return out


# --------------------------------------------------------------------------
# Observations (counts and categories only)
# --------------------------------------------------------------------------

def _tail_text(path: Path, max_bytes: int = TAIL_BYTES) -> str:
    size = path.stat().st_size
    with open(path, "rb") as fh:
        if size > max_bytes:
            fh.seek(size - max_bytes)
            data = fh.read()
            nl = data.find(b"\n")
            data = data[nl + 1:] if nl >= 0 else b""
        else:
            data = fh.read()
    return data.decode("utf-8", errors="replace")


def cmd_kind(cmd) -> str:
    """The tool name of a shell command (first word after env assignments), or 'other'."""
    if not isinstance(cmd, str):
        return "other"
    words = cmd.strip().split()
    while words and "=" in words[0] and not words[0].startswith("-"):
        words.pop(0)
    first = words[0] if words else ""
    return first if first in CMD_KINDS else "other"


def summarize_transcript(text: str) -> dict:
    """Counts from the given transcript text. Prompt text is used only to pick a category."""
    first_prompt = None
    corrections = 0
    tool_inputs: dict[str, tuple[str, dict]] = {}
    reads: defaultdict = defaultdict(int)
    failed: defaultdict = defaultdict(int)
    big = 0
    searches = 0
    routes: defaultdict = defaultdict(int)
    file_reads: defaultdict = defaultdict(int)   # keys are hashed in memory only, never stored
    polls = 0
    raw_tests = 0
    for line in text.splitlines():
        try:
            d = json.loads(line)
        except ValueError:
            continue
        msg = d.get("message") if isinstance(d, dict) and isinstance(d.get("message"), dict) else None
        if not msg:
            continue
        if d.get("type") == "assistant":
            for c in msg.get("content") or []:
                if isinstance(c, dict) and c.get("type") == "tool_use":
                    name = c.get("name") if isinstance(c.get("name"), str) else "?"
                    inp = c.get("input") if isinstance(c.get("input"), dict) else {}
                    tool_inputs[str(c.get("id", ""))] = (name, inp)
                    if name == "Read" and isinstance(inp.get("file_path"), str):
                        reads[inp["file_path"]] += 1
                        file_reads[inp["file_path"]] += 1
                    elif name == "Monitor":
                        polls += 1
                    elif name == "Bash" and isinstance(inp.get("command"), str):
                        m = CAT_RE.match(inp["command"])
                        if m:
                            file_reads[m.group(1)] += 1
                        if SLEEP_RE.search(inp["command"]):
                            polls += 1
                    elif name in ("Grep", "Glob"):
                        searches += 1
        elif d.get("type") == "user" and not d.get("isMeta") and not d.get("isSidechain"):
            content = msg.get("content")
            if isinstance(content, list) and any(isinstance(c, dict) and c.get("type") == "tool_result" for c in content):
                for c in content:
                    if not (isinstance(c, dict) and c.get("type") == "tool_result"):
                        continue
                    name, inp = tool_inputs.get(str(c.get("tool_use_id", "")), ("?", {}))
                    if c.get("is_error") and name == "Bash":
                        failed[cmd_kind(inp.get("command"))] += 1
                    limited = name == "Read" and ("limit" in inp or "offset" in inp)
                    if usage._result_size(c.get("content")) >= usage.BIG_RESULT and not limited:
                        big += 1
                    if (name == "Bash" and TEST_CMD_RE.search(str(inp.get("command", "")))
                            and not re.search(r"\bult['\"]?\s+run\b", str(inp.get("command", "")))
                            and usage._result_size(c.get("content")) > RAW_TEST_BYTES):
                        raw_tests += 1
                    if name == "Bash" and "route" in str(inp.get("command", "")):
                        for r in ROUTE_RE.findall(usage._text_of(c.get("content"))):
                            if r in ROUTES:
                                routes[r] += 1
            else:
                prompt = usage._text_of(content).strip()
                if prompt and not prompt.startswith(("<command-", "<local-command", "<system-reminder",
                                                     "[Request interrupted")):
                    if first_prompt is None:
                        first_prompt = prompt
                    elif usage.CORRECTION.search(prompt[:400]):
                        corrections += 1
    return {
        "category": usage.categorize(first_prompt) if first_prompt else "unknown",
        "signals": {
            "repeated-failure": sum(1 for n in failed.values() if n >= usage.REPEAT_CMD),
            "re-read": sum(1 for n in reads.values() if n >= usage.REPEAT_READ),
            "big-output": big,
            "correction": corrections,
            "search-churn": 1 if searches >= usage.SEARCH_CHURN else 0,
            "poll-sleep": polls,
            "raw-test-output": raw_tests,
            "reread": sum(1 for n in file_reads.values() if n >= 2),
        },
        "failing_kinds": {k: n for k, n in failed.items() if n >= usage.REPEAT_CMD},
        "routes": dict(routes),
    }


def _session(path: Path) -> str:
    return hashlib.sha1(str(path.resolve()).encode("utf-8")).hexdigest()[:12]


def _read_observations(path: Path) -> list[dict]:
    """Validated observation records. Unknown keys and values are dropped."""
    if not path.is_file() or path.is_symlink():
        return []
    out = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            d = json.loads(line)
        except ValueError:
            continue
        if not isinstance(d, dict) or not SESSION_RE.match(str(d.get("session", ""))):
            continue
        cat = d.get("category") if d.get("category") in CATEGORY_SET else "unknown"
        sig = d.get("signals") if isinstance(d.get("signals"), dict) else {}
        out.append({
            "session": d["session"], "category": cat,
            "signals": {k: max(0, min(1_000_000, int(v))) for k, v in sig.items()
                        if k in SIGNAL_MODULE and isinstance(v, (int, float))},
            "ts": _num(d.get("ts"), 0.0),
        })
    return out


def observe(transcript: Path, root=None) -> dict:
    """Append one snapshot for this transcript. Later snapshots of a chat replace earlier ones."""
    summary = summarize_transcript(_tail_text(transcript))
    rec = {"ts": int(time.time()), "session": _session(transcript), "category": summary["category"],
           "signals": summary["signals"], "failing_kinds": summary["failing_kinds"],
           "routes": summary["routes"]}
    path = state_dir(root) / "observations.jsonl"
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()[-(MAX_OBSERVATIONS - 1):] if path.is_file() else []
    lines = [l for l in lines if l.strip()] + [json.dumps(rec, sort_keys=True)]
    write_private(path, "\n".join(lines) + "\n")
    return rec


def record_arch(counts: dict, root=None) -> dict | None:
    """One snapshot per project per day of architecture finding counts. Counts only: no paths or code."""
    signals: dict[str, int] = defaultdict(int)
    for kind, n in counts.items():
        if kind in ARCH_SIGNALS and isinstance(n, int) and n > 0:
            signals[ARCH_SIGNALS[kind]] += n
    if not signals:
        return None
    day = time.strftime("%Y-%m-%d", time.gmtime())
    session = hashlib.sha1(f"arch:{day}".encode("utf-8")).hexdigest()[:12]
    rec = {"ts": int(time.time()), "session": session, "category": "refactor",
           "signals": dict(signals), "failing_kinds": [], "routes": []}
    path = state_dir(root) / "observations.jsonl"
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()[-(MAX_OBSERVATIONS - 1):] if path.is_file() else []
    lines = [l for l in lines if l.strip()] + [json.dumps(rec, sort_keys=True)]
    write_private(path, "\n".join(lines) + "\n")
    return rec


def _observe_disabled() -> bool:
    return os.environ.get("ULTIMATUM_OBSERVE") == "0"


def observe_hook() -> int:
    """Hook mode: JSON on stdin, no output, always exit 0."""
    try:
        if _observe_disabled():
            return 0
        payload = json.loads(sys.stdin.read() or "{}")
        tp = payload.get("transcript_path")
        cwd = payload.get("cwd")
        if not isinstance(tp, str):
            return 0
        path = Path(tp)
        if path.suffix != ".jsonl" or not path.is_file():
            return 0
        root = None
        if isinstance(cwd, str) and Path(cwd).is_dir():
            root = project_root(Path(cwd))
        observe(path, root)
    except (Exception, SystemExit):
        pass
    return 0


# --------------------------------------------------------------------------
# Proposals (allow-listed fields and fixed templates only)
# --------------------------------------------------------------------------

def plugin_version() -> str:
    try:
        v = json.loads((Path(__file__).resolve().parents[2] / ".claude-plugin" / "plugin.json")
                       .read_text(encoding="utf-8")).get("version", "")
    except (OSError, ValueError, AttributeError):
        return "unknown"
    return v if isinstance(v, str) and VERSION_RE.match(v) else "unknown"


def _proposals_dir(root=None) -> Path:
    return state_dir(root, "proposals")


def list_proposals(root=None) -> list[dict]:
    d = _proposals_dir(root)
    out = []
    for f in sorted(d.glob("*.json")):
        if f.is_symlink():
            continue
        try:
            p = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if isinstance(p, dict) and set(p) == PROPOSAL_FIELDS and p.get("id") == f.stem:
            out.append(p)
    return sorted(out, key=lambda p: p["created"])


def _proposal_md(p: dict) -> str:
    return "\n".join([
        f"# Ultimatum proposal {p['id']}", "",
        f"- plugin version: {p['plugin_version']}",
        f"- module: {p['module']}",
        f"- signal: {p['signal']}",
        f"- category: {p['category']}",
        f"- counts: {p['counts']['sessions']} session(s), {p['counts']['occurrences']} occurrence(s)", "",
        f"Proposed lesson (fixed template): {p['lesson']}", "",
        "Nothing was uploaded. Review it, then open an issue or PR yourself if you agree.", "",
    ])


def propose(root=None) -> list[dict]:
    d = state_dir(root)
    latest: dict[str, dict] = {}
    for r in _read_observations(d / "observations.jsonl"):
        latest[r["session"]] = r          # last snapshot per chat wins
    agg: defaultdict = defaultdict(lambda: {"sessions": 0, "occurrences": 0})
    for r in latest.values():
        for sig, n in r["signals"].items():
            if n > 0:
                a = agg[(sig, r["category"])]
                a["sessions"] += 1
                a["occurrences"] += n
    existing = {(p["signal"], p["category"]) for p in list_proposals(root)}
    made = []
    for (sig, cat), a in sorted(agg.items()):
        if a["sessions"] < PROPOSE_MIN_SESSIONS or a["occurrences"] < PROPOSE_MIN_OCCURRENCES:
            continue
        if (sig, cat) in existing:
            continue
        pid = safe_id(new_id("prop"))
        p = {"id": pid, "created": int(time.time()), "plugin_version": plugin_version(),
             "module": SIGNAL_MODULE[sig], "signal": sig, "category": cat,
             "counts": {"sessions": a["sessions"], "occurrences": a["occurrences"]},
             "lesson": ARCH_TEMPLATES.get(sig) or WASTE_TEMPLATES.get(sig) or TEMPLATES.get(cat, TEMPLATES["other"])}
        pdir = _proposals_dir(root)
        write_private(pdir / f"{pid}.json", json.dumps(p, indent=2, sort_keys=True) + "\n")
        write_private(pdir / f"{pid}.md", _proposal_md(p))
        made.append(p)
    return made


def clear_proposal(pid: str, root=None) -> bool:
    safe_id(pid)
    d = _proposals_dir(root)
    gone = False
    for ext in (".json", ".md"):
        f = d / f"{pid}{ext}"
        if f.is_file() and not f.is_symlink():
            f.unlink()
            gone = True
    return gone


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def _print_lessons(rows: list[tuple[str, dict]]) -> None:
    for scope, r in rows[:LIST_CAP]:
        print(f"- lesson: {r['text']} (x{r['count']}, {scope})")
    if len(rows) > LIST_CAP:
        print(f"... {len(rows) - LIST_CAP} more")


def cmd_learn(args) -> int:
    try:
        return _dispatch(args)
    except ValueError as e:
        print(f"[ult learn] {e}")
        return 2


def _dispatch(args) -> int:
    a = args.action
    if a == "observe":
        if args.hook:
            return observe_hook()
        if _observe_disabled():
            print("[ult learn] observation disabled (ULTIMATUM_OBSERVE=0)")
            return 0
        tr = Path(args.transcript).resolve() if args.transcript else current_transcript()
        if not tr or not tr.is_file():
            print("[ult learn] no transcript found for this chat; nothing observed")
            return 1
        rec = observe(tr)
        sig = ", ".join(f"{k} {v}" for k, v in rec["signals"].items() if v) or "none"
        print(f"[ult learn] observed this chat ({rec['category']}): {sig}")
        return 0
    if a == "add":
        rec = add_lesson(args.text, args.scope, args.module)
        print(f"[ult learn] saved ({args.scope}, x{rec['count']}): lesson: {rec['text']}")
        return 0
    if a == "list":
        scopes = ["project", "global"] if args.scope == "all" else [args.scope]
        paths = {"project": _project_store(project_root()) / "lessons.jsonl",
                 "global": global_home() / "lessons.jsonl"}
        rows = [(s, r) for s in scopes for r in load_lessons(paths[s])]
        if not rows:
            print("[ult learn] no lessons yet")
            return 0
        _print_lessons(rows)
        return 0
    if a == "relevant":
        lines = relevant(args.task, project_root())
        print("\n".join(lines) if lines else "[ult learn] no relevant lessons")
        return 0
    if a == "prune":
        out = []
        for s in ("project", "global"):
            path = store_path(s)
            recs = load_lessons(path)
            kept = prune(recs)
            if len(kept) != len(recs):
                write_lessons(path, kept)
            out.append(f"{s} removed {len(recs) - len(kept)}, kept {len(kept)}")
        print("[ult learn] prune: " + "; ".join(out))
        return 0
    if a == "propose":
        made = propose()
        if not made:
            print(f"[ult learn] no proposal crossed the threshold ({PROPOSE_MIN_SESSIONS} chats, "
                  f"{PROPOSE_MIN_OCCURRENCES} occurrences)")
            return 0
        print(f"[ult learn] wrote {len(made)} proposal(s) to .ultimatum/proposals; nothing was uploaded")
        return 0
    if a == "proposals":
        if args.clear:
            if clear_proposal(args.clear):
                print(f"[ult learn] cleared {args.clear}")
                return 0
            print(f"[ult learn] no proposal {args.clear}")
            return 1
        ps = list_proposals()
        if not ps:
            print("[ult learn] no pending proposals")
            return 0
        for p in ps[:LIST_CAP]:
            c = p["counts"]
            print(f"{p['id']}  {p['signal']}  {p['category']}  module={p['module']}  "
                  f"sessions={c['sessions']} occurrences={c['occurrences']}")
        return 0
    return 2


def register(sub):
    p = sub.add_parser("learn", help="local lessons: observe / add / list / relevant / prune / propose")
    ls = p.add_subparsers(dest="action", required=True)
    o = ls.add_parser("observe", help="record counts and categories from this chat (no text kept)")
    o.add_argument("--transcript", help="transcript .jsonl (default: this chat)")
    o.add_argument("--hook", action="store_true", help="hook mode: JSON on stdin, silent, always exit 0")
    a = ls.add_parser("add", help="save a lesson (cleaned, redacted, capped at 200 chars)")
    a.add_argument("text")
    a.add_argument("--scope", choices=["project", "global"], default="project")
    a.add_argument("--module", help="module id this lesson concerns, e.g. debugging")
    li = ls.add_parser("list", help="show saved lessons")
    li.add_argument("--scope", choices=["project", "global", "all"], default="all")
    r = ls.add_parser("relevant", help="the lessons ult route would show for a task")
    r.add_argument("task")
    ls.add_parser("prune", help="drop expired and over-cap lessons")
    ls.add_parser("propose", help="write redacted improvement proposals from observations")
    pr = ls.add_parser("proposals", help="list pending proposals, or --clear ID")
    pr.add_argument("--clear", metavar="ID")
    p.set_defaults(func=cmd_learn)
