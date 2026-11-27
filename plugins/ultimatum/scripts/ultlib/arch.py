"""`ult arch` — deterministic architecture checks (Architecture Guardian).

Builds a file-level dependency graph (Python via ast, JS/TS via import
specifiers, optionally merged with Graphify's EXTRACTED edges) and reports:
import cycles, oversized files and functions, duplicated blocks, placeholder
code, unreferenced private definitions, file-naming outliers and changed
source files with no test touching them. Everything is local and capped.

`check --changed` limits findings to files in the working-tree diff, so a
review of a small change stays cheap. `baseline` snapshots the findings so a
later `check` can report drift (what is new since the snapshot).
"""
from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
import time
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path

from . import archgraph
from .archgraph import build_graph, cycles
from .common import project_root, state_dir, write_private
from .search import EXT_LANG, _is_test, list_files

MAX_FILE_BYTES = 512 * 1024
DEFAULT_MAX_LINES = 500
DEFAULT_MAX_FUNC_LINES = 80
DUP_WINDOW = 8          # normalized lines per duplicate window
DUP_MIN_CHARS = 240     # ignore windows of trivial code (brackets, short calls)
PRINT_CAP = 12
BLOCKING = ("cycle", "stub")  # kinds that fail --strict
DATA_DIRS = {"fixtures", "__fixtures__", "testdata", "test-data", "vendor", "third_party", "__snapshots__", "migrations"}

_STUB_RE = re.compile(
    r"""raise\s+NotImplementedError|throw\s+new\s+Error\(\s*['"`](?i:not\s+implemented|todo)|\b(?:TODO|FIXME|XXX)\b[:(\s]""")
_COMMENT_RE = re.compile(r"^\s*(#|//|/\*|\*|\*/)")
_IMPORT_LINE_RE = re.compile(r"^\s*(import\s|from\s\S+\s+import\s|export\s.*\sfrom\s|const\s+\w+\s*=\s*require\()")
_IDENT_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
STYLES = {
    "snake": re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)+$"),
    "kebab": re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)+$"),
    "camel": re.compile(r"^[a-z][a-z0-9]*(?:[A-Z][a-z0-9]*)+$"),
    "pascal": re.compile(r"^(?:[A-Z][a-z0-9]+){2,}$"),
}


@dataclass
class Finding:
    kind: str       # cycle | size | func-size | dup | stub | dead | naming | untested
    path: str
    line: int
    detail: str
    lead: bool = False  # heuristic: confirm in source before acting

    def key(self) -> str:
        return f"{self.kind}|{self.path}|{self.detail}"

    def text(self) -> str:
        loc = f"{self.path}:{self.line}" if self.line else self.path
        return f"{self.kind}{'?' if self.lead else ''}: {loc} {self.detail}".rstrip()


@dataclass
class Report:
    files: int = 0
    edges: int = 0
    graph_sources: list = field(default_factory=list)
    typed_ratio: float | None = None
    ts_any: int = 0
    findings: list = field(default_factory=list)

    def counts(self) -> dict:
        return dict(Counter(f.kind for f in self.findings))


# --------------------------------------------------------------------------
# Files and source
# --------------------------------------------------------------------------

def _rel(root: Path, p: Path) -> str:
    return p.relative_to(root).as_posix()


def _read(p: Path) -> str | None:
    try:
        if p.stat().st_size > MAX_FILE_BYTES:
            return None
        return p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def source_files(root: Path, scope: str | None = None, exclude: tuple = ()) -> dict[str, str]:
    """rel path -> text for Python and JS/TS sources under scope. Fixture, vendored and generated dirs are skipped."""
    import fnmatch
    out: dict[str, str] = {}
    for p in list_files(root, scope):
        if EXT_LANG.get(p.suffix) not in ("py", "js") or p.suffix in (".vue", ".svelte"):
            continue
        rel = _rel(root, p)
        if set(Path(rel).parts[:-1]) & DATA_DIRS or p.name.endswith((".min.js", ".d.ts")):
            continue
        if any(fnmatch.fnmatch(rel, g) for g in exclude):
            continue
        text = _read(p)
        if text is not None:
            out[rel] = text
    return out


def changed_files(root: Path) -> set[str] | None:
    """Files changed against HEAD plus untracked ones; None when git is unavailable."""
    names: set[str] = set()
    for cmd in (["git", "-C", str(root), "diff", "--name-only", "HEAD"],
                ["git", "-C", str(root), "ls-files", "--others", "--exclude-standard"]):
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        except (OSError, subprocess.SubprocessError):
            return None
        if r.returncode != 0:
            return None
        names.update(l.strip() for l in r.stdout.splitlines() if l.strip())
    return names


# --------------------------------------------------------------------------
# Individual checks
# --------------------------------------------------------------------------

def _is_abstract(fn: ast.AST) -> bool:
    for d in getattr(fn, "decorator_list", []):
        name = d.attr if isinstance(d, ast.Attribute) else getattr(d, "id", "")
        if name in ("abstractmethod", "overload"):
            return True
    return False


def check_sizes(sources, trees, max_lines, max_func) -> list[Finding]:
    out = []
    for rel, text in sources.items():
        n = text.count("\n") + (0 if text.endswith("\n") else 1)
        if n > max_lines and not _is_test(Path("/" + rel)):
            out.append(Finding("size", rel, 0, f"{n} lines > {max_lines}"))
        tree = trees.get(rel)
        if tree is None:
            continue
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and getattr(node, "end_lineno", None):
                length = node.end_lineno - node.lineno + 1
                if length > max_func:
                    out.append(Finding("func-size", rel, node.lineno, f"{node.name}() {length} lines > {max_func}"))
    return out


def check_stubs(sources, trees) -> list[Finding]:
    abstract_lines: dict[str, set[int]] = defaultdict(set)
    for rel, tree in trees.items():
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and _is_abstract(node):
                abstract_lines[rel].update(range(node.lineno, (node.end_lineno or node.lineno) + 1))
    out = []
    for rel, text in sources.items():
        if _is_test(Path("/" + rel)):
            continue
        for i, line in enumerate(text.splitlines(), 1):
            m = _STUB_RE.search(line)
            if m and i not in abstract_lines.get(rel, ()):
                out.append(Finding("stub", rel, i, line.strip()[:80]))
    return out


def _norm_lines(text: str) -> list[tuple[int, str]]:
    out = []
    for i, line in enumerate(text.splitlines(), 1):
        s = " ".join(line.split())
        if not s or _COMMENT_RE.match(s) or _IMPORT_LINE_RE.match(s) or len(s) < 4:
            continue
        out.append((i, s))
    return out


def check_duplicates(sources) -> list[Finding]:
    seen: dict[str, tuple[str, int, int]] = {}
    pairs: dict[tuple[str, str], list[tuple[int, int, int, int]]] = defaultdict(list)
    for rel in sorted(sources):
        lines = _norm_lines(sources[rel])
        for k in range(len(lines) - DUP_WINDOW + 1):
            win = lines[k:k + DUP_WINDOW]
            body = "\n".join(s for _, s in win)
            if len(body) < DUP_MIN_CHARS:
                continue
            h = hashlib.sha1(body.encode()).hexdigest()
            first = seen.get(h)
            if first is None:
                seen[h] = (rel, win[0][0], win[-1][0])
            elif not (first[0] == rel and first[2] >= win[0][0]):
                pairs[(first[0], rel)].append((first[1], first[2], win[0][0], win[-1][0]))
    out = []
    for (a, b), spans in sorted(pairs.items()):
        merged: list[list[int]] = []
        for s in sorted(spans):
            if merged and s[0] <= merged[-1][1] + 1 and s[2] <= merged[-1][3] + 1:
                merged[-1] = [merged[-1][0], max(merged[-1][1], s[1]), merged[-1][2], max(merged[-1][3], s[3])]
            else:
                merged.append(list(s))
        for a0, a1, b0, b1 in merged:
            out.append(Finding("dup", a, a0, f"lines {a0}-{a1} repeat in {b}:{b0}-{b1}"))
    return out


def check_dead(sources, trees) -> list[Finding]:
    """Private top-level Python definitions never referenced anywhere else (a lead, not proof)."""
    uses: Counter = Counter()
    for text in sources.values():
        uses.update(_IDENT_RE.findall(text))
    out = []
    for rel, tree in trees.items():
        if _is_test(Path("/" + rel)):
            continue
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                name = node.name
                if name.startswith("_") and not name.startswith("__") and uses[name] <= 1:
                    out.append(Finding("dead", rel, node.lineno, f"{name} is never referenced", lead=True))
    return out


def _style(stem: str) -> str | None:
    for name, rx in STYLES.items():
        if rx.match(stem):
            return name
    return None


def check_naming(sources) -> list[Finding]:
    by_dir: dict[str, list[tuple[str, str]]] = defaultdict(list)
    out = []
    for rel in sources:
        p = Path(rel)
        stem = p.name.split(".")[0]
        if p.suffix == ".py" and "-" in stem:
            out.append(Finding("naming", rel, 0, "Python module name contains '-' (not importable)"))
            continue
        st = _style(stem)
        if st:
            by_dir[p.parent.as_posix()].append((rel, st))
    for _d, items in sorted(by_dir.items()):
        tally = Counter(st for _, st in items)
        top, n = tally.most_common(1)[0]
        if n >= 3 and n / len(items) >= 0.75:
            for rel, st in items:
                if st != top:
                    out.append(Finding("naming", rel, 0, f"{st} name in a {top}-case directory"))
    return out


def check_untested(sources, changed: set[str]) -> list[Finding]:
    tests = {rel: text for rel, text in sources.items() if _is_test(Path("/" + rel))}
    out = []
    for rel in sorted(changed):
        if rel not in sources or rel in tests:
            continue
        stem = Path(rel).name.split(".")[0]
        if stem in ("__init__", "index", "main", "__main__", "conftest") or len(stem) < 3:
            continue
        pat = re.compile(rf"\b{re.escape(stem)}\b")
        if not any(pat.search(t) or stem in Path(tr).name for tr, t in tests.items()):
            out.append(Finding("untested", rel, 0, "no test file mentions this module", lead=True))
    return out


def typing_stats(sources, trees) -> tuple[float | None, int]:
    total = typed = 0
    for tree in trees.values():
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                total += 1
                args = [a for a in node.args.args + node.args.kwonlyargs if a.arg not in ("self", "cls")]
                if node.returns is not None and all(a.annotation is not None for a in args):
                    typed += 1
    ts_any = sum(len(re.findall(r":\s*any\b|\bas\s+any\b|<any>", t)) for r, t in sources.items() if r.endswith((".ts", ".tsx")))
    return (round(typed / total, 3) if total else None), ts_any


# --------------------------------------------------------------------------
# Orchestration
# --------------------------------------------------------------------------

def scan(root: Path, scope: str | None = None, graph_path: Path | None = None,
         exclude: tuple = ()) -> tuple[dict[str, str], dict[str, ast.AST], dict[str, set[str]], list[str]]:
    """Sources, Python trees, the merged import graph and its source labels (one parse per file)."""
    sources = source_files(root, scope, exclude)
    trees: dict[str, ast.AST] = {}
    for rel, text in sources.items():
        if rel.endswith(".py"):
            try:
                trees[rel] = ast.parse(text)
            except (SyntaxError, ValueError):
                pass
    graph, used = build_graph(root, sources, trees, graph_path)
    return sources, trees, graph, used


def analyze(root: Path, scope: str | None = None, only: set[str] | None = None,
            max_lines: int = DEFAULT_MAX_LINES, max_func: int = DEFAULT_MAX_FUNC_LINES,
            graph_path: Path | None = None, exclude: tuple = ()) -> Report:
    """Whole-scope graph; findings limited to `only` (changed files) when given."""
    sources, trees, graph, used = scan(root, scope, graph_path, exclude)
    findings: list[Finding] = []
    for comp in cycles(graph):
        if only is None or set(comp) & only:
            findings.append(Finding("cycle", comp[0], 0, " -> ".join(comp + [comp[0]])))
    findings += check_sizes(sources, trees, max_lines, max_func)
    findings += check_stubs(sources, trees)
    findings += check_duplicates(sources)
    findings += check_dead(sources, trees)
    findings += check_naming(sources)
    if only is not None:
        findings = [f for f in findings if f.kind == "cycle" or f.path in only
                    or (f.kind == "dup" and any(f" {c}:" in f.detail for c in only))]
        findings += check_untested(sources, only)
    scoped_trees = {r: t for r, t in trees.items() if only is None or r in only}
    scoped_sources = {r: t for r, t in sources.items() if only is None or r in only}
    typed, ts_any = typing_stats(scoped_sources, scoped_trees)
    return Report(files=len(sources), edges=sum(len(v) for v in graph.values()), graph_sources=used,
                  typed_ratio=typed, ts_any=ts_any, findings=findings)


def _baseline_path(root: Path) -> Path:
    return state_dir(root) / "arch-baseline.json"


def save_baseline(root: Path, report: Report) -> Path:
    path = _baseline_path(root)
    data = {"ts": int(time.time()), "counts": report.counts(), "keys": sorted(f.key() for f in report.findings)}
    write_private(path, json.dumps(data, indent=1, sort_keys=True) + "\n")
    return path


def drift(root: Path, report: Report) -> list[Finding] | None:
    path = _baseline_path(root)
    try:
        keys = set(json.loads(path.read_text(encoding="utf-8")).get("keys", []))
    except (OSError, ValueError, AttributeError):
        return None
    return [f for f in report.findings if f.key() not in keys]


def record(root: Path, report: Report) -> None:
    """Counts only, into the self-improvement observations (no paths or code)."""
    try:
        from .learn import record_arch
    except ImportError:
        return
    record_arch(report.counts(), root)


def summary_line(report: Report) -> str:
    c = report.counts()
    order = ("cycle", "stub", "dup", "size", "func-size", "naming", "dead", "untested")
    parts = [f"{k} {c[k]}" for k in order if c.get(k)]
    typed = f"typed {report.typed_ratio:.0%}" if report.typed_ratio is not None else "typed n/a"
    any_part = f", ts any {report.ts_any}" if report.ts_any else ""
    return (f"arch: {report.files} files, {report.edges} edges ({'+'.join(report.graph_sources)}) | "
            f"{', '.join(parts) if parts else 'no findings'} | {typed}{any_part}")


def _print(report: Report, findings: list[Finding], limit: int) -> None:
    print(summary_line(report))
    order = {"cycle": 0, "stub": 1, "dup": 2, "size": 3, "func-size": 4, "naming": 5, "untested": 6, "dead": 7}
    rows = sorted(findings, key=lambda f: (order.get(f.kind, 9), f.path, f.line))
    for f in rows[:limit]:
        print("  " + f.text())
    if len(rows) > limit:
        print(f"  … {len(rows) - limit} more (--json or --limit N)")
    if any(f.lead for f in rows[:limit]):
        print("  '?' = lead: confirm in source before acting")


DEPS_CAP = 30


def _target_rel(root: Path, target: str) -> str:
    """A CLI path (relative to the cwd or absolute) as a repo-relative posix path."""
    p = Path(target)
    if not p.is_absolute():
        p = Path.cwd() / p
    try:
        return p.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return Path(target).as_posix()


def cmd_deps(args, root: Path) -> int:
    """Neighbours of one file in the merged graph: what it imports, or with --reverse what imports it."""
    if not args.target:
        print("[ult arch] deps needs a file: ult arch deps <path> [--reverse]")
        return 2
    if args.depth < 1:
        print("[ult arch] --depth must be 1 or more")
        return 2
    _, _, graph, used = scan(root, None, Path(args.graph) if args.graph else None,
                             tuple(args.exclude or ()))
    rel = _target_rel(root, args.target)
    if rel not in graph:
        print(f"[ult arch] unknown path: {args.target} (not a Python or JS/TS source in this repo)")
        return 2
    hits = archgraph.neighbours(graph, rel, reverse=args.reverse, depth=args.depth)
    limit = DEPS_CAP if args.limit is None else args.limit
    arrow = "<-" if args.reverse else "->"
    labels = "+".join(used)
    if args.json:
        print(json.dumps({"path": rel, "reverse": args.reverse, "graph": used, "total": len(hits),
                          "deps": [{"path": p, "depth": d} for p, d in hits[:limit]]}, indent=1))
        return 0
    print(f"deps: {rel} {arrow} {len(hits)} ({labels})")
    for p, d in hits[:limit]:
        print(f"  {p}" + (f" (depth {d})" if args.depth > 1 else ""))
    if len(hits) > limit:
        print(f"  … {len(hits) - limit} more (--limit N)")
    return 0


def cmd_arch(args) -> int:
    root = project_root()
    if args.action == "deps":
        return cmd_deps(args, root)
    only = None
    if args.changed:
        only = changed_files(root)
        if only is None:
            print("[ult arch] git unavailable; --changed needs a git checkout")
            return 2
        if not only:
            print("arch: no changed files")
            return 0
    graph_path = Path(args.graph) if args.graph else None
    report = analyze(root, args.path, only, args.max_lines, args.max_func, graph_path, tuple(args.exclude or ()))
    if args.action == "baseline":
        p = save_baseline(root, report)
        print(f"{summary_line(report)}\n  baseline saved: {_rel(root, p) if p.is_relative_to(root) else p}")
        return 0
    shown = report.findings
    if args.drift:
        new = drift(root, report)
        if new is None:
            print("[ult arch] no baseline; run `ult arch baseline` first")
            return 2
        shown = new
    if args.record:
        record(root, report)
    if args.json:
        print(json.dumps({"files": report.files, "edges": report.edges, "graph": report.graph_sources,
                          "typed_ratio": report.typed_ratio, "ts_any": report.ts_any,
                          "counts": dict(Counter(f.kind for f in shown)),
                          "findings": [asdict(f) for f in shown]}, indent=1))
    else:
        _print(report, shown, PRINT_CAP if args.limit is None else args.limit)
    if args.strict and any(f.kind in BLOCKING for f in shown):
        return 1
    return 0


def register(sub):
    p = sub.add_parser("arch", help="architecture checks: cycles, duplication, size, stubs, naming, drift")
    p.add_argument("action", nargs="?", choices=["check", "baseline", "deps"], default="check")
    p.add_argument("target", nargs="?", help="deps: the file to start from")
    p.add_argument("--reverse", action="store_true", help="deps: list importers (blast radius) instead of imports")
    p.add_argument("--depth", type=int, default=1, help="deps: hops to follow (default 1)")
    p.add_argument("--path", help="limit to this directory")
    p.add_argument("--changed", action="store_true", help="only findings that touch files changed vs HEAD")
    p.add_argument("--drift", action="store_true", help="only findings that are new since `ult arch baseline`")
    p.add_argument("--exclude", action="append", metavar="GLOB", help="skip matching paths (repeatable)")
    p.add_argument("--graph", help="Graphify graph.json (default: graphify-out/graph.json when present)")
    p.add_argument("--max-lines", type=int, default=DEFAULT_MAX_LINES)
    p.add_argument("--max-func", type=int, default=DEFAULT_MAX_FUNC_LINES)
    p.add_argument("--limit", type=int, default=None, help="max lines printed (check: 12, deps: 30)")
    p.add_argument("--strict", action="store_true", help="exit 1 on cycles or placeholder code")
    p.add_argument("--record", action="store_true", help="add finding counts to local self-improvement observations")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_arch)
