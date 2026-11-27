#!/usr/bin/env python3
"""Check a folder of SVG interface icons for the slips that make a set look uneven.

Reads local .svg files only (a folder, or files listed one by one) and never
fetches anything. Standard library only; the SVG is parsed as XML, and DOCTYPE
or entity declarations are refused rather than expanded.

Usage: icon_check.py PATH [PATH ...] [--size N] [--only RULE,...] [--json] [--rules]
Exit: 0 no findings, 1 findings, 2 bad arguments or no readable SVG files.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

RULES = {
    "no-viewbox": ("high", "no viewBox; the icon cannot scale cleanly"),
    "not-square": ("high", "viewBox is not square; icons sit on a square canvas"),
    "wrong-size": ("medium", "viewBox size differs from the set's canvas"),
    "fixed-colour": ("medium", "hard-coded colour; use currentColor or none so the icon takes the text colour"),
    "mixed-stroke": ("medium", "stroke width differs from the rest of the set"),
    "mixed-caps": ("low", "line cap or join differs from the rest of the set"),
    "has-text": ("medium", "live text inside the icon; outline it or drop it"),
    "has-raster": ("high", "embedded image inside the icon"),
    "has-transform": ("low", "transform left on a shape; flatten it before export"),
    "editor-junk": ("low", "editor metadata, comments or namespaces left in the file"),
    "out-of-bounds": ("medium", "path coordinates fall outside the canvas"),
    "too-complex": ("low", "very long path data for an interface icon; simplify it"),
}

SVG_NS = "http://www.w3.org/2000/svg"
ALLOWED_NS = {SVG_NS, "http://www.w3.org/1999/xlink"}
NEUTRAL = {"none", "currentcolor", "inherit", "transparent", ""}
PATH_LIMIT = 1500  # characters of path data per icon
NUM = re.compile(r"-?(?:\d+\.?\d*|\.\d+)(?:e-?\d+)?", re.I)
STYLE_DECL = re.compile(r"(fill|stroke|stroke-width|stroke-linecap|stroke-linejoin)\s*:\s*([^;]+)")


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def attrs(el) -> dict:
    out = {local(k): v.strip() for k, v in el.attrib.items()}
    for k, v in STYLE_DECL.findall(el.attrib.get("style", "")):
        out[k] = v.strip()
    return out


def abs_points(d: str):
    """Yield absolute (x, y) points from path data, handling relative commands.

    Arcs are reduced to their end point and curve handles are included; that is
    enough to spot a shape drawn off the canvas.
    """
    x = y = sx = sy = 0.0
    sizes = {"m": 2, "l": 2, "t": 2, "h": 1, "v": 1, "c": 6, "s": 4, "q": 4, "a": 7, "z": 0}
    for cmd, body in re.findall(r"([MmLlHhVvCcSsQqTtAaZz])([^MmLlHhVvCcSsQqTtAaZz]*)", d):
        c = cmd.lower()
        rel = cmd.islower()
        nums = [float(n) for n in NUM.findall(body)]
        if c == "z":
            x, y = sx, sy
            continue
        step = sizes[c]
        for i in range(0, len(nums) - step + 1, step):
            g = nums[i:i + step]
            if c == "h":
                x = x + g[0] if rel else g[0]
                yield x, y
            elif c == "v":
                y = y + g[0] if rel else g[0]
                yield x, y
            elif c == "a":
                x, y = (x + g[5], y + g[6]) if rel else (g[5], g[6])
                yield x, y
            else:
                bx, by = x, y
                for j in range(0, step, 2):
                    px, py = (bx + g[j], by + g[j + 1]) if rel else (g[j], g[j + 1])
                    yield px, py
                x, y = px, py
            if c == "m" and i == 0:
                sx, sy = x, y


def read(path: Path):
    text = path.read_text(encoding="utf-8")
    if re.search(r"<!DOCTYPE|<!ENTITY", text, re.I):
        raise ValueError("DOCTYPE or entity declarations are not accepted")
    return text, ET.fromstring(text)


def check_one(path: Path, size: float):
    found, style = [], {}
    try:
        text, root = read(path)
    except (OSError, ValueError, ET.ParseError) as e:
        return None, [{"file": str(path), "rule": "parse", "severity": "high", "message": f"cannot read: {e}", "detail": ""}], style

    def add(rule, detail=""):
        sev, msg = RULES[rule]
        found.append({"file": str(path), "rule": rule, "severity": sev, "message": msg, "detail": detail})

    ra = attrs(root)
    vb = ra.get("viewBox")
    box = None
    if not vb:
        add("no-viewbox")
    else:
        parts = [float(n) for n in NUM.findall(vb)]
        if len(parts) == 4:
            box = parts
            if parts[2] != parts[3]:
                add("not-square", vb)
            elif parts[2] != size:
                add("wrong-size", f"{parts[2]:g} not {size:g}")

    if "<!--" in text or re.search(r"<\?xml-stylesheet|sodipodi|inkscape|sketch:|figma|illustrator", text, re.I):
        add("editor-junk")
    else:
        for el in root.iter():
            ns = el.tag[1:].split("}")[0] if el.tag.startswith("{") else SVG_NS
            if ns not in ALLOWED_NS or local(el.tag) in {"metadata", "sodipodi:namedview"}:
                add("editor-junk", local(el.tag))
                break
            if any(k.startswith("{") and k[1:].split("}")[0] not in ALLOWED_NS for k in el.attrib):
                add("editor-junk", "foreign attribute")
                break

    inherited = {k: ra[k] for k in ("stroke-width", "stroke-linecap", "stroke-linejoin") if k in ra}
    path_len = 0
    colours, transforms = set(), False
    has_text = has_raster = False
    for el in root.iter():
        name = local(el.tag)
        a = attrs(el)
        if name in ("text", "tspan"):
            has_text = True
        if name == "image":
            has_raster = True
        if "transform" in a and el is not root:
            transforms = True
        for k in ("fill", "stroke"):
            v = a.get(k, "").lower()
            if v not in NEUTRAL and not v.startswith("url("):
                colours.add(v)
        for k in ("stroke-width", "stroke-linecap", "stroke-linejoin"):
            if k in a and el is not root:
                inherited.setdefault(k, a[k])
        if name == "path":
            d = a.get("d", "")
            path_len += len(d)
            if box and not any(f["rule"] == "out-of-bounds" for f in found):
                x0, y0, w, h = box
                for px, py in abs_points(d):
                    if px < x0 - 0.01 or py < y0 - 0.01 or px > x0 + w + 0.01 or py > y0 + h + 0.01:
                        add("out-of-bounds", f"point {px:g},{py:g}")
                        break
    if has_text:
        add("has-text")
    if has_raster:
        add("has-raster")
    if colours:
        add("fixed-colour", ", ".join(sorted(colours)))
    if transforms:
        add("has-transform")
    if path_len > PATH_LIMIT:
        add("too-complex", f"{path_len} characters of path data")
    return root, found, inherited


def check(paths, size: float = 24):
    files = []
    for p in paths:
        p = Path(p)
        if p.is_dir():
            files += sorted(p.rglob("*.svg"))
        elif p.suffix.lower() == ".svg" and p.is_file():
            files.append(p)
    found, styles = [], {}
    for f in files:
        _, fnd, style = check_one(f, size)
        found += fnd
        styles[f] = style
    for key, rule in (("stroke-width", "mixed-stroke"), ("stroke-linecap", "mixed-caps"), ("stroke-linejoin", "mixed-caps")):
        values = Counter(s[key] for s in styles.values() if key in s)
        if len(values) > 1:
            common = values.most_common(1)[0][0]
            for f, s in styles.items():
                if key in s and s[key] != common:
                    sev, msg = RULES[rule]
                    found.append({"file": str(f), "rule": rule, "severity": sev, "message": msg,
                                  "detail": f"{key} {s[key]}, most of the set uses {common}"})
    return files, found


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check a set of SVG interface icons.")
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--size", type=float, default=24)
    ap.add_argument("--only", default="")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--rules", action="store_true")
    a = ap.parse_args(argv)
    if a.rules:
        for k, (sev, msg) in RULES.items():
            print(f"{k} [{sev}]: {msg}")
        return 0
    if not a.paths:
        ap.print_usage(sys.stderr)
        return 2
    only = {r.strip() for r in a.only.split(",") if r.strip()}
    bad = only - set(RULES)
    if bad:
        print("unknown rule(s): " + ", ".join(sorted(bad)), file=sys.stderr)
        return 2
    files, found = check(a.paths, a.size)
    if not files:
        print("no SVG files found", file=sys.stderr)
        return 2
    if only:
        found = [f for f in found if f["rule"] in only]
    found.sort(key=lambda f: (f["file"], f["rule"]))
    if a.json:
        print(json.dumps({"icons": len(files), "findings": found}, indent=2))
    else:
        for f in found:
            extra = f" ({f['detail']})" if f["detail"] else ""
            print(f"{f['file']} {f['rule']} [{f['severity']}]: {f['message']}{extra}")
        print(f"{len(files)} icon(s), " + (f"{len(found)} finding(s)" if found else "no findings"))
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
