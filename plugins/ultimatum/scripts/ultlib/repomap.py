"""`ult map` — compact repository map, built once, queried by section.

Local path for "repo graph" capabilities: it records *where* things are
(entry points, routes, data stores, auth/permission code, tests, CI, infra,
manifests, docs) with file:line anchors. It is a starting index for scoped
reading, not a substitute for it — every relationship that matters must be
confirmed in source. Stored at .ultimatum/map.json; `ult map summary` prints
at most ~40 lines; `ult map query <section|keyword>` prints one slice.
"""
from __future__ import annotations

import json
import os
import re
import time
from collections import Counter, defaultdict
from pathlib import Path

from .common import dump_json, project_root, state_dir, write_private
from .search import EXT_LANG, list_files

MANIFESTS = {"package.json", "pnpm-lock.yaml", "package-lock.json", "yarn.lock", "requirements.txt", "pyproject.toml",
             "poetry.lock", "uv.lock", "Pipfile", "Pipfile.lock", "go.mod", "go.sum", "Cargo.toml", "Cargo.lock", "Gemfile",
             "Gemfile.lock", "composer.json", "composer.lock", "pom.xml", "build.gradle", "build.gradle.kts", "setup.py", "setup.cfg"}
CI_HINTS = (".github/workflows/", ".gitlab-ci.yml", ".circleci/", "azure-pipelines.yml", "Jenkinsfile", ".buildkite/")
INFRA_HINTS = (".tf", "Dockerfile", "docker-compose", "compose.yaml", "compose.yml", "k8s/", "helm/", "Chart.yaml",
               "serverless.yml", "vercel.json", "netlify.toml", "fly.toml", "wrangler.toml", "Procfile", "app.yaml")
DOC_NAMES = re.compile(r"(?i)^(readme|contributing|architecture|design|adr|changelog|security|claude|agents)(\.|$)")

LINE_RULES: dict[str, list[re.Pattern]] = {
    "routes": [
        re.compile(r"@(app|router|bp|blueprint|api)\.(get|post|put|patch|delete|route|api_route)\("),
        re.compile(r"\b(app|router|server)\.(get|post|put|patch|delete|all|use)\(\s*['\"`]/"),
        re.compile(r"\b(path|re_path|url)\(\s*r?['\"]\^?[\w/<>:{}-]*"),
        re.compile(r"\bHandleFunc\(|\bhttp\.Handle\(|\.(GET|POST|PUT|DELETE|PATCH)\(\s*\""),
        re.compile(r"""(?x)^\s*(if|elif)\b.*\b(path|PATH_INFO|url|pathname)\b.*(==|startswith|match|re\.)"""),
        re.compile(r"""['"](GET|POST|PUT|PATCH|DELETE)['"]\s*,\s*r?['"]/"""),
        re.compile(r"export\s+(async\s+)?function\s+(GET|POST|PUT|PATCH|DELETE)\b"),
    ],
    "data_stores": [
        re.compile(r"\b(sqlite3\.connect|psycopg2?|asyncpg|mysql\.connector|pymongo|redis\.|createClient\(|new PrismaClient|"
                   r"knex\(|sequelize|mongoose\.connect|typeorm|drizzle\(|gorm\.Open|sql\.Open|supabase|createPool)"),
        re.compile(r"(?i)\b(create table|alter table)\b"),
    ],
    "auth": [
        re.compile(r"(?i)\b(authenticate|authoriz\w*|login|logout|session|jwt|oauth|bearer|api[_-]?key|csrf|"
                   r"permission|is_admin|role|tenant|owner_id|account_id|current_user|require_\w+|middleware)\b"),
    ],
    "sinks": [
        re.compile(r"\b(subprocess\.|os\.system|exec\(|eval\(|child_process|execSync|spawn\(|pickle\.loads|yaml\.load\(|"
                   r"innerHTML|dangerouslySetInnerHTML|render_template_string|\.raw\(|cursor\.execute\(|requests\.(get|post)|"
                   r"urllib\.request|fetch\(|axios\.|open\(|send_file|sendFile|redirect\()"),
    ],
    "entry_points": [
        re.compile(r"^if __name__ == ['\"]__main__['\"]"),
        re.compile(r"^func main\(\)"),
        re.compile(r"\b(serve_forever|make_server|app\.listen|\.listen\(\d|uvicorn\.run|app\.run\(|createServer\()"),
        re.compile(r"\bargparse\.ArgumentParser\(|\bclick\.(command|group)\b|\bcommander\b|\byargs\b"),
    ],
}


def build(root: Path) -> dict:
    files = list_files(root)
    langs = Counter()
    m: dict = {"root": str(root), "built": time.strftime("%Y-%m-%dT%H:%M:%S"), "file_count": len(files),
               "languages": {}, "manifests": [], "ci": [], "infra": [], "docs": [], "tests": [],
               "routes": [], "data_stores": [], "auth": [], "sinks": [], "entry_points": [], "scripts": {}}
    caps = {"routes": 200, "data_stores": 100, "auth": 300, "sinks": 300, "entry_points": 60}
    auth_files = Counter()
    for f in files:
        rel = os.path.relpath(f, root)
        name = f.name
        if f.suffix in EXT_LANG or f.suffix in {".html", ".css", ".sh"}:
            langs[f.suffix] += 1
        if name in MANIFESTS:
            m["manifests"].append(rel)
            if name == "package.json":
                try:
                    pj = json.loads(f.read_text("utf-8"))
                    if isinstance(pj.get("scripts"), dict):
                        m["scripts"][rel] = pj["scripts"]
                except (OSError, json.JSONDecodeError):
                    pass
        if any(h in rel for h in CI_HINTS):
            m["ci"].append(rel)
        if any(h in rel or rel.endswith(h) for h in INFRA_HINTS):
            m["infra"].append(rel)
        if DOC_NAMES.match(name) or rel.startswith(("docs/", "doc/", "adr/")) and f.suffix in {".md", ".mdx", ".rst"}:
            m["docs"].append(rel)
        low = rel.lower()
        if any(t in low for t in ("test_", "_test.", ".test.", ".spec.", "/tests/", "tests/", "__tests__/")):
            m["tests"].append(rel)
            continue  # do not index test files as routes/sinks
        if f.suffix not in EXT_LANG:
            continue
        try:
            if f.stat().st_size > 1_000_000:
                continue
            lines = f.read_text("utf-8", "replace").splitlines()
        except OSError:
            continue
        for i, line in enumerate(lines, 1):
            for sect, pats in LINE_RULES.items():
                if len(m[sect]) >= caps[sect]:
                    continue
                if any(p.search(line) for p in pats):
                    if sect == "auth":
                        auth_files[rel] += 1
                        if auth_files[rel] > 6:
                            continue
                    m[sect].append(f"{rel}:{i}: {line.strip()[:160]}")
    m["languages"] = dict(langs.most_common())
    m["auth_hotspots"] = [f"{f} ({n})" for f, n in auth_files.most_common(15)]
    return m


def summary(m: dict) -> str:
    out = [f"[ult map] {m['root']} — {m['file_count']} files, built {m['built']}",
           "languages: " + ", ".join(f"{k}×{v}" for k, v in list(m["languages"].items())[:8])]
    for sect in ("manifests", "entry_points", "routes", "data_stores", "auth_hotspots", "ci", "infra", "docs"):
        items = m.get(sect, [])
        if not items:
            continue
        head = items[:4]
        out.append(f"{sect} ({len(items)}): " + (" | ".join(head) if sect in ("manifests", "ci", "infra", "docs", "auth_hotspots") else ""))
        if sect not in ("manifests", "ci", "infra", "docs", "auth_hotspots"):
            out.extend(f"  {x}" for x in head)
    out.append(f"tests: {len(m['tests'])} files" + (f" e.g. {m['tests'][0]}" if m["tests"] else ""))
    if m["scripts"]:
        for k, v in list(m["scripts"].items())[:2]:
            out.append(f"scripts {k}: " + ", ".join(list(v)[:10]))
    out.append("[ult map] slices: ult map query routes|data_stores|auth|sinks|entry_points|tests|<keyword>")
    return "\n".join(out)


def _load(root: Path) -> dict | None:
    p = state_dir(root) / "map.json"
    return json.loads(p.read_text()) if p.exists() else None


def cmd_map(args) -> int:
    root = project_root()
    if args.action == "build" or (args.action in ("summary", "query") and _load(root) is None):
        m = build(root)
        write_private(state_dir(root) / "map.json", dump_json(m))
        if args.action == "build":
            print(summary(m))
            return 0
    m = _load(root)
    if args.action == "summary":
        print(summary(m))
        return 0
    term = " ".join(args.term or [])
    if term in m and isinstance(m[term], list):
        items = m[term]
        print(f"[ult map] {term}: {len(items)}")
        for x in items[: args.limit]:
            print(f"  {x}")
        if len(items) > args.limit:
            print(f"  … +{len(items) - args.limit} more (--limit)")
        return 0
    rx = re.compile(re.escape(term), re.IGNORECASE)
    n = 0
    for sect, items in m.items():
        if not isinstance(items, list):
            continue
        hits = [x for x in items if rx.search(str(x))]
        if hits:
            print(f"[{sect}]")
            for x in hits[: args.limit]:
                print(f"  {x}")
            n += len(hits)
    if not n:
        print(f"[ult map] nothing mentions {term!r}; try `ult search`")
        return 1
    return 0


def register(sub):
    p = sub.add_parser("map", help="build/query a compact repo map (.ultimatum/map.json)")
    p.add_argument("action", choices=["build", "summary", "query"])
    p.add_argument("term", nargs="*")
    p.add_argument("--limit", type=int, default=30)
    p.set_defaults(func=cmd_map)
