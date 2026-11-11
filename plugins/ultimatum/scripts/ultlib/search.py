"""`ult search` / `ult symbols` / `ult refs` — scoped, ranked code search.

Local stand-in for symbol-aware tools (Serena/LSP) and repo graphs: regex
definition patterns per language, word-boundary references, and results
grouped per file with a hard cap so a broad query cannot flood context.
Hits are leads: open the file at the reported line before relying on one.
Uses ripgrep when installed, otherwise a pure-Python walk that honours
`git ls-files` (so .gitignore'd and vendored files are skipped).
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
from collections import defaultdict
from pathlib import Path

from .common import project_root, redact

SKIP_DIRS = {".git", "node_modules", ".ultimatum", "dist", "build", ".next", "out", "target",
             "__pycache__", ".venv", "venv", ".tox", ".mypy_cache", ".pytest_cache", "vendor", "coverage"}
CODE_EXT = {".py", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".go", ".rs", ".java", ".kt", ".rb",
            ".php", ".cs", ".swift", ".c", ".h", ".cc", ".cpp", ".hpp", ".scala", ".sql", ".tf", ".vue", ".svelte"}

# Definition patterns; {n} is replaced by the escaped symbol name.
DEF_PATTERNS = {
    "py": [r"^\s*(async\s+)?def\s+{n}\b", r"^\s*class\s+{n}\b", r"^{n}\s*(:[^=]+)?=\s"],
    "js": [r"\bfunction\*?\s+{n}\b", r"\bclass\s+{n}\b", r"\b(const|let|var)\s+{n}\s*=",
           r"^\s*(export\s+)?(default\s+)?(async\s+)?{n}\s*\(.*\)\s*\{{", r"\b(interface|type|enum)\s+{n}\b",
           r"^\s*(public|private|protected|static|readonly|async|\s)*{n}\s*[(:=]"],
    "go": [r"^func\s+(\([^)]*\)\s*)?{n}\b", r"^type\s+{n}\b", r"^\s*(var|const)\s+{n}\b"],
    "rs": [r"\bfn\s+{n}\b", r"\b(struct|enum|trait|type|mod)\s+{n}\b", r"\b(const|static)\s+{n}\b"],
    "java": [r"\b(class|interface|enum|record)\s+{n}\b", r"^\s*(public|private|protected|static|final|\s)+[\w<>\[\],\s]+\s+{n}\s*\("],
    "rb": [r"^\s*def\s+(self\.)?{n}\b", r"^\s*(class|module)\s+{n}\b"],
    "php": [r"\bfunction\s+{n}\b", r"\b(class|interface|trait)\s+{n}\b"],
    "sql": [r"(?i)\bcreate\s+(or\s+replace\s+)?(table|view|function|procedure|index|policy)\s+(if\s+not\s+exists\s+)?[\w.\"]*{n}\b"],
    "tf": [r"^\s*(resource|data|module|variable|output)\s+\"[^\"]*\"?\s*\"?{n}\""],
}
EXT_LANG = {".py": "py", ".js": "js", ".jsx": "js", ".ts": "js", ".tsx": "js", ".mjs": "js", ".cjs": "js",
            ".vue": "js", ".svelte": "js", ".go": "go", ".rs": "rs", ".java": "java", ".kt": "java",
            ".scala": "java", ".cs": "java", ".rb": "rb", ".php": "php", ".sql": "sql", ".tf": "tf"}


def list_files(root: Path, scope: str | None = None, glob: str | None = None) -> list[Path]:
    base = (root / scope).resolve() if scope else root
    files: list[Path] = []
    try:
        out = subprocess.run(["git", "-C", str(root), "ls-files", "-co", "--exclude-standard", "--", str(base)],
                             capture_output=True, text=True, timeout=30)
        if out.returncode == 0 and out.stdout:
            files = [root / l for l in out.stdout.splitlines() if l]
    except (OSError, subprocess.SubprocessError):
        pass
    if not files:
        for dp, dns, fns in os.walk(base):
            dns[:] = [d for d in dns if d not in SKIP_DIRS and d not in {".idea", ".vscode", ".cache"}]
            files.extend(Path(dp) / f for f in fns)
    files = [f for f in files if not (set(f.relative_to(root).parts) & SKIP_DIRS)]
    if glob:
        import fnmatch
        files = [f for f in files if fnmatch.fnmatch(f.name, glob) or fnmatch.fnmatch(str(f.relative_to(root)), glob)]
    return [f for f in files if f.is_file()]


def grep(root: Path, pattern: str, files: list[Path], ignore_case=False) -> list[tuple[Path, int, str]]:
    flags = re.IGNORECASE if ignore_case else 0
    rx = re.compile(pattern, flags)
    hits = []
    for f in files:
        try:
            if f.stat().st_size > 2_000_000:
                continue
            with open(f, "r", encoding="utf-8", errors="replace") as fh:
                for i, line in enumerate(fh, 1):
                    if rx.search(line):
                        hits.append((f, i, line.rstrip("\n")))
        except OSError:
            continue
    return hits


def rg(root: Path, pattern: str, scope: str | None, glob: str | None, ignore_case=False):
    argv = ["rg", "--no-heading", "--line-number", "--color", "never", "-e", pattern]
    if ignore_case:
        argv.insert(1, "-i")
    if glob:
        argv += ["-g", glob]
    for d in SKIP_DIRS:
        argv += ["-g", f"!{d}/"]
    argv.append(str((root / scope) if scope else root))
    out = subprocess.run(argv, capture_output=True, text=True, timeout=60)
    if out.returncode == 2 and not out.stdout:  # rg error (e.g. regex syntax rg rejects)
        raise SystemExit(f"[ult] search failed: {out.stderr.strip()[:300]}")
    hits = []
    for line in out.stdout.splitlines():
        parts = line.split(":", 2)
        if len(parts) == 3 and parts[1].isdigit():
            hits.append((Path(parts[0]), int(parts[1]), parts[2]))
    return hits


def _scope_ok(root: Path, scope: str | None) -> None:
    if scope:
        base = (root / scope).resolve()
        if base != root and root not in base.parents:
            raise SystemExit(f"[ult] --path {scope!r} is outside the project ({root}); refusing to search there")


def _check_regex(pattern: str, ignore_case: bool) -> None:
    try:
        re.compile(pattern, re.IGNORECASE if ignore_case else 0)
    except re.error as e:
        raise SystemExit(f"[ult] invalid regex {pattern!r}: {e}")


def _search(root, pattern, scope, glob, ignore_case=False):
    _scope_ok(root, scope)
    _check_regex(pattern, ignore_case)
    if shutil.which("rg"):
        return rg(root, pattern, scope, glob, ignore_case)
    return grep(root, pattern, list_files(root, scope, glob), ignore_case)


def print_hits(root: Path, hits, per_file=5, max_files=25, label="match"):
    by = defaultdict(list)
    for f, ln, text in hits:
        by[f].append((ln, text))
    ranked = sorted(by.items(), key=lambda kv: (_is_test(kv[0]), -len(kv[1]), str(kv[0])))
    print(f"[ult] {len(hits)} {label}{'' if len(hits) == 1 else ('es' if label == 'match' else 's')} in {len(by)} file(s)" + (f"; showing {max_files}" if len(by) > max_files else ""))
    for f, rows in ranked[:max_files]:
        rel = os.path.relpath(f, root)
        print(f"{rel}  ({len(rows)})")
        for ln, text in rows[:per_file]:
            print(f"  {ln}: {redact(text.strip())[:200]}")
        if len(rows) > per_file:
            print(f"  … +{len(rows) - per_file} more (narrow with --path/--glob)")
    if len(by) > max_files:
        print(f"[ult] {len(by) - max_files} more file(s) omitted; narrow the query")


def _is_test(p: Path) -> bool:
    s = str(p).lower()
    return any(t in s for t in ("/test", "test_", "_test.", ".test.", ".spec.", "/tests/", "__tests__"))


def cmd_search(args) -> int:
    root = project_root()
    hits = _search(root, args.pattern, args.path, args.glob, args.ignore_case)
    if not hits:
        print("[ult] no matches")
        return 1
    print_hits(root, hits, args.per_file, args.max_files)
    return 0


def cmd_symbols(args) -> int:
    root = project_root()
    _scope_ok(root, args.path)
    name = re.escape(args.name) if not args.regex else args.name
    files = [f for f in list_files(root, args.path, args.glob) if f.suffix in EXT_LANG]
    hits = []
    for f in files:
        pats = [re.compile(p.replace("{n}", name)) for p in DEF_PATTERNS[EXT_LANG[f.suffix]]]
        try:
            with open(f, encoding="utf-8", errors="replace") as fh:
                for i, line in enumerate(fh, 1):
                    if any(p.search(line) for p in pats):
                        hits.append((f, i, line.rstrip("\n")))
        except OSError:
            continue
    if not hits:
        print(f"[ult] no definition of {args.name!r} found (try `ult refs`, or a looser --regex)")
        return 1
    print_hits(root, hits, args.per_file, args.max_files, label="definition")
    return 0


def cmd_refs(args) -> int:
    root = project_root()
    pat = rf"\b{re.escape(args.name)}\b"
    hits = _search(root, pat, args.path, args.glob)
    if not hits:
        print("[ult] no references")
        return 1
    print_hits(root, hits, args.per_file, args.max_files, label="reference")
    return 0


def register(sub):
    for name, fn, help_ in (("search", cmd_search, "regex search, grouped per file, capped"),
                            ("symbols", cmd_symbols, "find where a symbol is defined"),
                            ("refs", cmd_refs, "find word-boundary references to a symbol")):
        p = sub.add_parser(name, help=help_)
        if name == "search":
            p.add_argument("pattern")
            p.add_argument("-i", "--ignore-case", action="store_true")
        else:
            p.add_argument("name")
            if name == "symbols":
                p.add_argument("--regex", action="store_true", help="treat name as a regex")
        p.add_argument("--path", help="limit to a subdirectory")
        p.add_argument("--glob", help="filename glob, e.g. '*.py'")
        p.add_argument("--per-file", type=int, default=5)
        p.add_argument("--max-files", type=int, default=25)
        p.set_defaults(func=fn)
