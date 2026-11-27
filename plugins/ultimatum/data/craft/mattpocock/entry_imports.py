#!/usr/bin/env python3
"""Flag relative imports that reach past a package's entry files.

Layout assumed: PACKAGES/<name>/<root files are entries>, and anything in a
subfolder of <name>/ is private. Two rules are checked:
  1. code outside a package imports only that package's root files;
  2. files under <name>/tests/ import only root files, even of their own package.
Only relative specifiers ("./", "../") are resolved; aliases are reported as
skipped. The script reads text only and never runs the code it scans.

Usage:
    python3 entry_imports.py --packages src/packages [--root .]
    python3 entry_imports.py --self-check

Exit codes: 0 no violations, 1 violations found, 2 bad usage.
"""
import argparse
import os
import re
import sys
import tempfile

EXTS = (".ts", ".tsx", ".js", ".jsx", ".mts", ".cts", ".mjs", ".cjs")
SPEC = re.compile(r"""(?:\bfrom\s*|\bimport\s*\(\s*|\brequire\s*\(\s*|^\s*import\s+)["']([^"']+)["']""", re.M)
SKIP_DIRS = {"node_modules", ".git", "dist", "build", "coverage"}


def where(path, pkgs):
    """Return (package name, part path inside it) or (None, None)."""
    rel = os.path.relpath(path, pkgs)
    if rel.startswith(".."):
        return None, None
    parts = rel.split(os.sep)
    if len(parts) < 2:
        return None, None
    return parts[0], parts[1:]


def scan(root, pkgs):
    root, pkgs = os.path.abspath(root), os.path.abspath(pkgs)
    hits, skipped = [], 0
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
        for f in files:
            if not f.endswith(EXTS):
                continue
            src = os.path.join(d, f)
            with open(src, encoding="utf-8", errors="replace") as fh:
                text = fh.read()
            src_pkg, src_parts = where(src, pkgs)
            in_tests = bool(src_parts) and src_parts[0] == "tests" and len(src_parts) > 1
            for m in SPEC.finditer(text):
                spec = m.group(1)
                if not spec.startswith("."):
                    skipped += 1
                    continue
                target = os.path.normpath(os.path.join(d, spec))
                t_pkg, t_parts = where(target, pkgs)
                if t_pkg is None or len(t_parts) < 2:
                    continue  # not in a package, or a root entry file
                if in_tests and t_parts[0] == "tests" and t_pkg == src_pkg:
                    continue  # own fixtures
                line = text.count("\n", 0, m.start()) + 1
                rel = os.path.relpath(src, root)
                if in_tests:
                    hits.append(f"{rel}:{line}: test imports internal {spec}")
                elif src_pkg != t_pkg:
                    hits.append(f"{rel}:{line}: reaches inside package {t_pkg}: {spec}")
    return hits, skipped


def self_check():
    with tempfile.TemporaryDirectory() as d:
        def put(rel, body):
            p = os.path.join(d, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(body)
        put("src/packages/billing/index.ts", 'import { total } from "./lib/total";\n')
        put("src/packages/billing/lib/total.ts", "export const total = 1;\n")
        put("src/packages/billing/tests/a.test.ts", 'import { total } from "../index";\n')
        put("src/app.ts", 'import { total } from "./packages/billing";\n')
        hits, _ = scan(d, os.path.join(d, "src/packages"))
        assert hits == [], hits
        put("src/packages/billing/tests/b.test.ts", 'import { total } from "../lib/total";\n')
        put("src/main.ts", 'import x from "./packages/billing/lib/total";\n')
        hits, _ = scan(d, os.path.join(d, "src/packages"))
        assert len(hits) == 2, hits
    print("entry_imports: 2 checks passed")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description="Find imports that bypass package entry files.")
    p.add_argument("--packages", help="folder holding one subfolder per package")
    p.add_argument("--root", default=".", help="folder to scan (default: current)")
    p.add_argument("--self-check", action="store_true")
    a = p.parse_args(argv)
    if a.self_check:
        return self_check()
    if not a.packages or not os.path.isdir(a.packages) or not os.path.isdir(a.root):
        p.print_usage(sys.stderr)
        print("error: --packages must be an existing folder", file=sys.stderr)
        return 2
    hits, skipped = scan(a.root, a.packages)
    for h in hits:
        print(h)
    print(f"violations: {len(hits)}; non-relative imports not checked: {skipped}")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
