"""File-level dependency graph for `ult arch`.

Python imports are read with ast, JS/TS imports from relative specifiers, and
Graphify's graph.json adds EXTRACTED import edges when present. Ambiguous
module names are never guessed, so a reported cycle is backed by real edges.
"""
from __future__ import annotations

import ast
import json
import re
from pathlib import Path

JS_EXTS = (".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs")
_JS_SPEC_RE = re.compile(
    r"""(?:\bimport\s+(?:[\w*{}\s,$]+\s+from\s+)?|\bexport\s+[\w*{}\s,$]+\s+from\s+|\brequire\s*\(\s*|\bimport\s*\(\s*)['"]([^'"]+)['"]""")



def _py_module_index(paths) -> dict[str, str]:
    """Dotted module name -> file, rooted at the repo and at any `src/`-style top directory."""
    idx: dict[str, str] = {}
    ambiguous: set[str] = set()
    for rel in paths:
        if not rel.endswith(".py"):
            continue
        parts = rel[:-3].split("/")
        if parts[-1] == "__init__":
            parts = parts[:-1]
        for start in range(len(parts)):
            name = ".".join(parts[start:])
            if name and idx.get(name, rel) != rel:
                ambiguous.add(name)   # two files claim this name: never guess between them
            elif name:
                idx[name] = rel
    return {k: v for k, v in idx.items() if k not in ambiguous}


def _py_edges(rel: str, tree: ast.AST, idx: dict[str, str]) -> set[str]:
    pkg = rel[:-3].split("/")[:-1] if not rel.endswith("__init__.py") else rel.split("/")[:-1]
    out: set[str] = set()

    def add(name: str) -> None:
        while name:
            if name in idx:
                out.add(idx[name])
                return
            name = name.rpartition(".")[0]

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                add(a.name)
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                base = pkg[: len(pkg) - (node.level - 1)] if node.level > 1 else pkg
                prefix = ".".join(base + ([node.module] if node.module else []))
            else:
                prefix = node.module or ""
            for a in node.names:
                full = f"{prefix}.{a.name}" if prefix else a.name
                if full in idx:
                    out.add(idx[full])
                else:
                    add(prefix)
    out.discard(rel)
    return out


def _js_resolve(rel: str, spec: str, known: set[str]) -> str | None:
    if not spec.startswith("."):
        return None
    base = (Path(rel).parent / spec).as_posix()
    parts: list[str] = []
    for seg in base.split("/"):
        if seg == "..":
            if parts:
                parts.pop()
        elif seg not in (".", ""):
            parts.append(seg)
    base = "/".join(parts)
    stem = re.sub(r"\.(js|mjs|cjs|jsx)$", "", base)
    candidates = [base] + [stem + e for e in JS_EXTS] + [f"{base}/index{e}" for e in JS_EXTS]
    return next((c for c in candidates if c in known), None)


def graphify_edges(root: Path, known: set[str], path: Path | None = None) -> list[tuple[str, str]]:
    """File-level edges from a Graphify graph.json. Only EXTRACTED edges count; INFERRED ones are guesses."""
    gp = path or root / "graphify-out" / "graph.json"
    try:
        data = json.loads(gp.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    if not isinstance(data, dict):
        return []
    node_file: dict[str, str] = {}
    for n in data.get("nodes") or []:
        if isinstance(n, dict) and isinstance(n.get("source_file"), str):
            sf = n["source_file"]
            try:
                sf = Path(sf).resolve().relative_to(root.resolve()).as_posix() if Path(sf).is_absolute() else Path(sf).as_posix()
            except ValueError:
                continue
            node_file[str(n.get("id"))] = sf
    out = []
    for e in data.get("links") or data.get("edges") or []:
        if not isinstance(e, dict) or str(e.get("confidence", "EXTRACTED")).upper() != "EXTRACTED":
            continue
        if str(e.get("relation", "")).lower() not in ("imports", "imports_from", "import"):
            continue
        a, b = node_file.get(str(e.get("source"))), node_file.get(str(e.get("target")))
        if a and b and a != b and a in known and b in known:
            out.append((a, b))
    return out


def build_graph(root: Path, sources: dict[str, str], trees: dict[str, ast.AST],
                graph_path: Path | None = None) -> tuple[dict[str, set[str]], list[str]]:
    known = set(sources)
    idx = _py_module_index(known)
    graph: dict[str, set[str]] = {f: set() for f in known}
    for rel, text in sources.items():
        if rel in trees:
            graph[rel] |= _py_edges(rel, trees[rel], idx)
        elif rel.endswith(JS_EXTS):
            for m in _JS_SPEC_RE.finditer(text):
                tgt = _js_resolve(rel, m.group(1), known)
                if tgt and tgt != rel:
                    graph[rel].add(tgt)
    used = ["local"]
    extra = graphify_edges(root, known, graph_path)
    if extra:
        used.append(f"graphify({len(extra)})")
        for a, b in extra:
            graph[a].add(b)
    return graph, used


def cycles(graph: dict[str, set[str]]) -> list[list[str]]:
    """Strongly connected components with more than one file (iterative Tarjan)."""
    index: dict[str, int] = {}
    low: dict[str, int] = {}
    on: set[str] = set()
    stack: list[str] = []
    out: list[list[str]] = []
    counter = 0
    for start in sorted(graph):
        if start in index:
            continue
        work = [(start, iter(sorted(graph[start])))]
        index[start] = low[start] = counter
        counter += 1
        stack.append(start)
        on.add(start)
        while work:
            v, it = work[-1]
            nxt = next(it, None)
            if nxt is not None:
                if nxt not in index:
                    index[nxt] = low[nxt] = counter
                    counter += 1
                    stack.append(nxt)
                    on.add(nxt)
                    work.append((nxt, iter(sorted(graph.get(nxt, ())))))
                elif nxt in on:
                    low[v] = min(low[v], index[nxt])
                continue
            work.pop()
            if work:
                low[work[-1][0]] = min(low[work[-1][0]], low[v])
            if low[v] == index[v]:
                comp = []
                while True:
                    w = stack.pop()
                    on.discard(w)
                    comp.append(w)
                    if w == v:
                        break
                if len(comp) > 1:
                    out.append(sorted(comp))
    return sorted(out)
