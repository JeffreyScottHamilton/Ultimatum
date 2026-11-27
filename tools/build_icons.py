#!/usr/bin/env python3
"""Build Ultimatum's own icon table: plugins/ultimatum/data/design-own/icons.csv.

Our rows (what each icon is for, search words, how to label it) are written by hand in
tools/icon_rows/*.json. Facts about the icons (the name exists, its import name, the
project's own tags and categories, the licence) come from the two projects' own metadata,
cached in icons-meta.json so the build and the tests never touch the network:

  Lucide    github.com/lucide-icons/lucide      icons/<name>.json   (ISC)   npm: lucide-react
  Phosphor  github.com/phosphor-icons/core      src/icons.ts        (MIT)   npm: @phosphor-icons/react

    python3 tools/build_icons.py --fetch   # refresh icons-meta.json (network)
    python3 tools/build_icons.py           # write icons.csv from the cache
    python3 tools/build_icons.py --check   # exit 1 if the CSV is out of date

The build fails when a row names an icon that is not in the cached metadata, or whose
React export name was not found in the published npm package at fetch time. No SVG
artwork is cached. Standard library only; the network is used only by --fetch.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import subprocess
import sys
import tarfile
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OWN = ROOT / "plugins" / "ultimatum" / "data" / "design-own"
OUT, META, ROWS = OWN / "icons.csv", OWN / "icons-meta.json", ROOT / "tools" / "icon_rows"

# Column order is ours; design.py reads the columns by name.
COLS = ("Category", "Icon Name", "Keywords", "Library", "Style", "Licence", "Import Code", "Best For",
        "Usage", "Accessible Name")

LIBS = {
    "lucide": {"label": "Lucide", "repo": "lucide-icons/lucide", "package": "lucide-react", "npm": "lucide-react"},
    "phosphor": {"label": "Phosphor", "repo": "phosphor-icons/core", "package": "@phosphor-icons/react",
                 "npm": "@phosphor-icons/react"},
}
RAW = "https://raw.githubusercontent.com/{repo}/{commit}/{path}"
LICENCE_WORDS = {"lucide": "ISC", "phosphor": "MIT"}  # what the project's LICENSE file must start with


# ---- rows ----------------------------------------------------------------------------------------

def load_rows() -> list[dict]:
    out = []
    for path in sorted(ROWS.glob("*.json")):
        for i, r in enumerate(json.loads(path.read_text(encoding="utf-8"))["rows"]):
            if len(r) not in (7, 8):
                raise SystemExit(f"{path.name} row {i}: want 7 or 8 fields, got {len(r)}")
            lib, name, cat, kw, best, usage, label = r[:7]
            if lib not in LIBS:
                raise SystemExit(f"{path.name} row {i}: unknown library {lib!r}")
            out.append({"lib": lib, "name": name, "category": cat, "keywords": kw, "best": best,
                        "usage": usage, "label": label, "weight": r[7] if len(r) == 8 else "regular",
                        "file": path.name})
    return out


def lucide_pascal(name: str) -> str:
    """lucide-react exports each icon as the PascalCase of its kebab-case file name."""
    return "".join(p[:1].upper() + p[1:] for p in name.split("-"))


# ---- fetch ---------------------------------------------------------------------------------------

def get(url: str, binary: bool = False):
    with urllib.request.urlopen(url, timeout=60) as r:
        data = r.read()
    return data if binary else data.decode("utf-8")


def head_commit(repo: str) -> str:
    """Commit of the default branch, read with `git ls-remote` (public, no credentials)."""
    p = subprocess.run(["git", "ls-remote", f"https://github.com/{repo}", "refs/heads/main"],
                       capture_output=True, text=True, timeout=60, check=True)
    return p.stdout.split()[0]


def npm_package(pkg: str) -> tuple[str, tarfile.TarFile]:
    info = json.loads(get(f"https://registry.npmjs.org/{pkg}/latest"))
    tar = get(info["dist"]["tarball"], binary=True)
    return info["version"], tarfile.open(fileobj=io.BytesIO(tar), mode="r:gz")


def phosphor_catalog(text: str) -> dict:
    cat = {}
    for m in re.finditer(r'\n  \{\n    name: "([^"]+)",\n    pascal_name: "([^"]+)",(?:\n    alias: [^\n]*)?\n    categories: \[([^\]]*)\],'
                         r'.*?\n    tags: \[(.*?)\],\n', text, re.S):
        name, pascal, cats, tags = m.groups()
        cat[name] = {"pascal": pascal,
                     "categories": sorted(c.split(".")[-1].lower() for c in re.findall(r"IconCategory\.\w+", cats)),
                     "tags": [t for t in re.findall(r'"([^"]*)"', tags) if not t.startswith("*")]}
    return cat


def fetch(rows: list[dict]) -> dict:
    meta: dict = {"sources": {}, "lucide": {}, "phosphor": {}}
    for lib, info in LIBS.items():
        commit = head_commit(info["repo"])
        licence = get(RAW.format(repo=info["repo"], commit=commit, path="LICENSE")).splitlines()[0].strip()
        if not licence.startswith(LICENCE_WORDS[lib]):
            raise SystemExit(f"{lib}: licence file starts {licence!r}, expected {LICENCE_WORDS[lib]}")
        version, tar = npm_package(info["npm"])
        meta["sources"][lib] = {"repo": f"https://github.com/{info['repo']}", "commit": commit, "licence": licence,
                                "licence_id": LICENCE_WORDS[lib], "npm_package": info["package"], "npm_version": version}
        wanted = sorted({r["name"] for r in rows if r["lib"] == lib})
        if lib == "lucide":
            dts = tar.extractfile("package/dist/lucide-react.d.ts").read().decode("utf-8")
            exports = set(re.findall(r"^declare const (\w+): LucideIcon;", dts, re.M))
            missing = []
            for n in wanted:
                try:
                    j = json.loads(get(RAW.format(repo=info["repo"], commit=commit, path=f"icons/{n}.json")))
                except urllib.error.HTTPError as e:
                    missing.append(f"{n} (HTTP {e.code})")
                    continue
                meta[lib][n] = {"pascal": lucide_pascal(n), "tags": j.get("tags", []), "categories": j.get("categories", []),
                                "export_found": lucide_pascal(n) in exports}
            if missing:
                raise SystemExit(f"lucide: not found at {commit[:10]}: {', '.join(missing)}")
        else:
            cat = phosphor_catalog(get(RAW.format(repo=info["repo"], commit=commit, path="src/icons.ts")))
            files = set(tar.getnames())
            missing = [n for n in wanted if n not in cat]
            if missing:
                raise SystemExit(f"phosphor: not found at {commit[:10]}: {', '.join(missing)}")
            for n in wanted:
                p = cat[n]["pascal"]
                meta[lib][n] = dict(cat[n], export_found=f"package/dist/csr/{p}.es.js" in files)
    return meta


# ---- build ---------------------------------------------------------------------------------------

def row(r: dict, meta: dict) -> dict:
    lib, name = r["lib"], r["name"]
    where = f"{r['file']}: {lib} {name}"
    m = meta[lib].get(name)
    if m is None:
        raise SystemExit(f"{where}: not in icons-meta.json (run --fetch, or the icon does not exist)")
    if not m["export_found"]:
        raise SystemExit(f"{where}: export {m['pascal']} not found in the published npm package")
    src = meta["sources"][lib]
    comp = m["pascal"]
    if lib == "lucide":
        jsx = f'<{comp} size={{20}} aria-hidden="true" />'
        style = "Outline, 2px stroke on a 24px grid"
    else:
        jsx = f'<{comp} size={{20}} weight="{r["weight"]}" aria-hidden="true" />'
        style = f"{r['weight'].capitalize()} weight (also thin, light, bold, fill, duotone)"
    return {
        "Category": r["category"], "Icon Name": name, "Keywords": r["keywords"], "Library": LIBS[lib]["label"],
        "Import Code": f"import {{ {comp} }} from '{src['npm_package']}'",
        "Usage": f"{jsx}; {r['usage']}", "Best For": r["best"], "Style": style,
        "Licence": f"{src['licence_id']} ({LIBS[lib]['label']})", "Accessible Name": r["label"],
    }


def build() -> str:
    meta = json.loads(META.read_text(encoding="utf-8"))
    rows = load_rows()
    keys = [(r["lib"], r["name"]) for r in rows]
    dupes = sorted({k for k in keys if keys.count(k) > 1})
    if dupes:
        raise SystemExit(f"duplicate icons: {dupes}")
    buf = io.StringIO()
    w = csv.DictWriter(buf, COLS, lineterminator="\n")
    w.writeheader()
    for r in rows:
        w.writerow(row(r, meta))
    return buf.getvalue()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--fetch", action="store_true", help="refresh icons-meta.json from the icon projects (network)")
    ap.add_argument("--check", action="store_true", help="exit 1 if the CSV differs from a fresh build")
    a = ap.parse_args()
    if a.fetch:
        META.write_text(json.dumps(fetch(load_rows()), indent=1, sort_keys=True) + "\n", encoding="utf-8")
        print(f"wrote {META.relative_to(ROOT)}")
    text = build()
    if a.check:
        same = OUT.is_file() and OUT.read_text(encoding="utf-8") == text
        print("icons.csv is up to date" if same else "icons.csv is out of date: run tools/build_icons.py")
        return 0 if same else 1
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({text.count(chr(10)) - 1} icons)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
