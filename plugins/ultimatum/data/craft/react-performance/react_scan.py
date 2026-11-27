#!/usr/bin/env python3
"""Pattern scan of React/Next.js source for common slow or fragile code.

Standard library only. Line patterns, not a parser: treat each hit as a
question to check, not a verdict. Usage:
    react_scan.py PATH [PATH ...] [--only RULE,RULE] [--json]
Exit 1 when any finding is printed, 0 otherwise.
"""
import argparse
import json
import os
import re
import sys

EXTS = (".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs")
SKIP_DIRS = {"node_modules", ".next", "dist", "build", "out", ".git", "coverage", ".turbo"}

HEAVY_BARRELS = {
    "lodash": "import from 'lodash/<fn>' or use lodash-es with tree shaking",
    "date-fns": "fine with modern bundlers if tree shaking works; check the analyzer",
    "@mui/material": "import from '@mui/material/<Component>' or enable optimizePackageImports",
    "@mui/icons-material": "import each icon from '@mui/icons-material/<Icon>'",
    "react-icons": "import from the sub-pack, e.g. 'react-icons/fa'",
    "lucide-react": "enable optimizePackageImports or import from 'lucide-react/icons/<name>'",
    "antd": "check the analyzer; enable optimizePackageImports",
    "rxjs": "check the analyzer",
}
HEAVY_RARE = ("monaco-editor", "@monaco-editor/react", "react-quill", "quill", "chart.js",
              "react-chartjs-2", "recharts", "mapbox-gl", "leaflet", "react-leaflet",
              "three", "@react-three/fiber", "pdfjs-dist", "@tiptap/react", "draft-js",
              "highlight.js", "prismjs", "xlsx")
SERVER_ONLY = ("@prisma/client", "pg", "mysql2", "mongoose", "drizzle-orm", "fs", "node:fs",
               "child_process", "node:child_process", "bcrypt", "stripe")

RULES = {
    "serial-await": "two or more awaits in a row with no use of the first result; start them together (react.md C1)",
    "await-in-loop": "await inside a for loop runs one at a time; batch or run in parallel with a cap (react.md C1)",
    "barrel-import": "named import from a large barrel package (react.md D1)",
    "heavy-static-import": "heavy, often rarely used library imported statically; consider a dynamic import (react.md D2)",
    "server-import-in-client": "server-only module imported in a 'use client' file (react.md B4)",
    "use-client-page": "'use client' on a page or layout; push the boundary down to the interactive leaf (react.md B2)",
    "index-key": "array index used as key (react.md E8)",
    "effect-sets-state": "useEffect whose body only sets state; derive during render instead (react.md E1)",
    "inline-context-value": "context value built inline as an object; every render makes a new one (react.md E3)",
    "pointer-state": "state set on pointer or scroll movement; use a ref and the DOM (react.md E10)",
    "component-in-component": "component defined inside another component; it remounts each render (react.md F1)",
}

IMPORT_RE = re.compile(r"""^\s*import\s+(?P<what>[^'"]*?)\s*from\s*['"](?P<mod>[^'"]+)['"]""")
AWAIT_DECL_RE = re.compile(r"^\s*(?:const|let|var)\s+(?P<lhs>\{[^}]*\}|\[[^\]]*\]|[\w$]+)\s*=\s*await\s+(?P<rhs>.+)$")
FOR_RE = re.compile(r"^\s*for\s*\(|\.forEach\(\s*async")
KEY_INDEX_RE = re.compile(r"key=\{\s*(?:i|idx|index|`[^`]*\$\{\s*(?:i|idx|index)\s*\}[^`]*`)\s*\}")
MAP_INDEX_RE = re.compile(r"\.map\(\s*\(\s*[\w$]+\s*,\s*(i|idx|index)\s*\)")
EFFECT_ONELINE_RE = re.compile(r"useEffect\(\s*\(\)\s*=>\s*\{?\s*set[A-Z]\w*\([^;]*\)\s*;?\s*\}?\s*,\s*\[")
EFFECT_START_RE = re.compile(r"useEffect\(\s*\(\)\s*=>\s*\{\s*$")
CTX_RE = re.compile(r"\.Provider\s+value=\{\{")
POINTER_RE = re.compile(r"on(?:Pointer|Mouse)Move=\{[^}]*\bset[A-Z]\w*\(|on(?:Scroll|Wheel)=\{[^}]*\bset[A-Z]\w*\(")
COMP_DEF_RE = re.compile(r"^(?P<ind>\s*)(?:export\s+(?:default\s+)?)?function\s+(?P<name>[A-Z]\w*)\s*\(|^(?P<ind2>\s*)(?:export\s+)?const\s+(?P<name2>[A-Z]\w*)\s*=\s*(?:\([^)]*\)|[\w$]+)\s*=>")


def names_in(lhs):
    return set(re.findall(r"[A-Za-z_$][\w$]*", lhs))


def is_client(lines):
    for ln in lines[:5]:
        s = ln.strip()
        if s in ("'use client'", '"use client"', "'use client';", '"use client";'):
            return True
    return False


def scan_text(path, text):
    lines = text.splitlines()
    out = []
    client = is_client(lines)
    base = os.path.basename(path)
    stem = base.rsplit(".", 1)[0]

    def add(i, rule, extra=""):
        out.append({"file": path, "line": i + 1, "rule": rule, "note": extra or RULES[rule]})

    if client and stem in ("page", "layout"):
        add(0, "use-client-page")

    prev_await = None  # (line index, names, indent)
    loop_depth_lines = []  # indents of open for-loops (approximate)
    comp_indent = None
    for i, ln in enumerate(lines):
        s = ln.strip()
        if not s or s.startswith("//") or s.startswith("*"):
            continue
        indent = len(ln) - len(ln.lstrip())

        m = IMPORT_RE.match(ln)
        if m:
            mod, what = m.group("mod"), m.group("what")
            if mod in HEAVY_BARRELS and "{" in what:
                add(i, "barrel-import", f"named import from '{mod}': {HEAVY_BARRELS[mod]} (react.md D1)")
            if mod in HEAVY_RARE and not what.startswith("type "):
                add(i, "heavy-static-import", f"'{mod}' imported statically; load it with a dynamic import if it is not on first screen (react.md D2)")
            if client and (mod in SERVER_ONLY or mod.startswith("server/") or mod.endswith("/server")):
                add(i, "server-import-in-client", f"'{mod}' in a 'use client' file (react.md B4)")
            continue

        # serial awaits
        a = AWAIT_DECL_RE.match(ln)
        if a:
            names = names_in(a.group("lhs"))
            rhs = a.group("rhs")
            if prev_await and prev_await[2] == indent and i - prev_await[0] <= 2:
                used = names_in(rhs) & prev_await[1]
                if not used:
                    add(i, "serial-await")
                names = names | prev_await[1]
            prev_await = (i, names, indent)
        elif s.startswith("await ") and prev_await and prev_await[2] == indent and i - prev_await[0] <= 2:
            if not (names_in(s) & prev_await[1]):
                add(i, "serial-await")
            prev_await = (i, prev_await[1], indent)
        else:
            prev_await = None

        # await in loop
        while loop_depth_lines and indent <= loop_depth_lines[-1] and not s.startswith("for"):
            if s.startswith("}"):
                loop_depth_lines.pop()
                break
            loop_depth_lines.pop()
        if FOR_RE.search(ln):
            if "await" in ln.split(")", 1)[-1] or ".forEach(" in ln:
                add(i, "await-in-loop")
            elif "for await" not in ln:
                loop_depth_lines.append(indent)
        elif loop_depth_lines and re.search(r"\bawait\b", ln):
            add(i, "await-in-loop")
            loop_depth_lines.pop()

        if KEY_INDEX_RE.search(ln) or (MAP_INDEX_RE.search(ln) and re.search(r"key=\{\s*(i|idx|index)\s*\}", ln)):
            add(i, "index-key")

        if EFFECT_ONELINE_RE.search(ln):
            add(i, "effect-sets-state")
        elif EFFECT_START_RE.search(ln):
            body = []
            for j in range(i + 1, min(i + 6, len(lines))):
                t = lines[j].strip()
                if t.startswith("}"):
                    break
                body.append(t)
            if body and all(re.match(r"set[A-Z]\w*\(", b) for b in body):
                add(i, "effect-sets-state")

        if CTX_RE.search(ln):
            add(i, "inline-context-value")
        if POINTER_RE.search(ln):
            add(i, "pointer-state")

        c = COMP_DEF_RE.match(ln)
        if c:
            ind = len(c.group("ind") if c.group("ind") is not None else c.group("ind2") or "")
            if comp_indent is not None and ind > comp_indent:
                add(i, "component-in-component")
            elif comp_indent is None or ind <= comp_indent:
                comp_indent = ind
    return out


def walk(paths):
    for p in paths:
        if os.path.isfile(p):
            yield p
            continue
        for root, dirs, files in os.walk(p):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for f in sorted(files):
                if f.endswith(EXTS) and not f.endswith(".d.ts"):
                    yield os.path.join(root, f)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--only", default="", help="comma-separated rule names")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--rules", action="store_true", help="list rules and exit")
    if argv is None:
        argv = sys.argv[1:]
    if "--rules" in argv:
        for k, v in RULES.items():
            print(f"{k}: {v}")
        return 0
    a = ap.parse_args(argv)
    only = {r for r in a.only.split(",") if r}
    bad = only - set(RULES)
    if bad:
        print("unknown rule(s): " + ", ".join(sorted(bad)), file=sys.stderr)
        return 2
    found = []
    for f in walk(a.paths):
        try:
            with open(f, encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except OSError as e:
            print(f"skip {f}: {e}", file=sys.stderr)
            continue
        found.extend(x for x in scan_text(f, text) if not only or x["rule"] in only)
    if a.json:
        print(json.dumps(found, indent=2))
    else:
        for x in found:
            print(f"{x['file']}:{x['line']} {x['rule']}: {x['note']}")
        print(f"{len(found)} finding(s)" if found else "no findings")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
