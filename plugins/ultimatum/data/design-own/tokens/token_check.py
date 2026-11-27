#!/usr/bin/env python3
"""Check that pages, components and assets draw their values from a token stylesheet.

    token_check.py scan --tokens tokens.css src/ [--json] [--strict] [--only raw-color,unknown-var]
    token_check.py embed --tokens tokens.css page.html --out page.html [--used]
    token_check.py colors --tokens tokens.css logo.svg banner.png [--max-distance 2] [--json]
    token_check.py rules
    token_check.py --self-check

scan    reads every custom property in the token stylesheet(s), then reads CSS, HTML, SVG and
        component files and reports values written by hand: colours, colour names, font
        families, sizes off the token scale, and var() names nothing defines.
embed   puts the token stylesheet inside a single-file HTML page, so the page carries its
        tokens with it; running it again replaces the block instead of adding another.
        --used keeps only the properties the page needs (and the ones those point at).
colors  lists the colours an SVG, CSS, HTML or PNG file uses and the nearest token colour
        to each, measured in OKLab; a colour further than --max-distance is off the palette.

Exit codes: 0 clean (scan: warnings allowed unless --strict), 1 findings, 2 bad arguments or
unreadable input. A line containing "token-check: ignore" is skipped, and a file containing
"token-check: ignore-file" is skipped whole. Standard library only; no network.
"""
from __future__ import annotations

import json
import math
import re
import struct
import sys
import tempfile
import zlib
from argparse import ArgumentParser
from pathlib import Path

RULES = [
    ("raw-color", "error", "a colour written by hand where a token should be used"),
    ("unknown-var", "error", "var(--name) where no token file or scanned file defines --name"),
    ("named-color", "warn", "a colour keyword such as white or red in a colour property"),
    ("raw-font", "warn", "a font family named by hand instead of through a token"),
    ("off-scale", "warn", "a size in px, rem or em that is not one of the token sizes"),
    ("off-palette", "error", "colors: an asset colour too far from every token colour"),
]
LEVEL = {name: level for name, level, _ in RULES}

PAGE_EXT = {".html", ".htm", ".svg", ".vue", ".svelte", ".astro"}
CSS_EXT = {".css", ".scss", ".less"}
SCRIPT_EXT = {".jsx", ".tsx", ".js", ".ts"}
SKIP_DIRS = {"node_modules", "dist", "build", "vendor", "__pycache__"}

HEX = re.compile(r"(?<![\w&-])#((?:[\da-f]{2}){3,4}|[\da-f]{3,4})(?![\w-])", re.I)
FUNC = re.compile(r"\b(rgba?|hsla?|hwb|lab|lch|oklab|oklch|color)\(\s*([^()]*)\)", re.I)
VAR_USE = re.compile(r"var\(\s*(--[\w-]+)")
VAR_DEF = re.compile(r"(?<![\w-])(--[\w-]+)\s*:\s*([^;{}]+)")
DECL = re.compile(r"(?<![\w$-])([a-zA-Z][\w-]*)\s*:\s*([^;{}\n]+)")
LENGTH = re.compile(r"(?<![\w.#-])(-?\d*\.?\d+)(px|rem|em)\b")
ATTR = re.compile(r"\b(fill|stroke|stop-color|flood-color|lighting-color|color)\s*=\s*([\"'])(.*?)\2", re.I | re.S)
STYLE_ATTR = re.compile(r"\bstyle\s*=\s*([\"'])(.*?)\1", re.I | re.S)
STYLE_TAG = re.compile(r"<style\b[^>]*>(.*?)</style>", re.I | re.S)

COLOR_PROPS = {"color", "background", "background-color", "border", "border-color", "border-top",
               "border-right", "border-bottom", "border-left", "border-top-color", "border-right-color",
               "border-bottom-color", "border-left-color", "outline", "outline-color", "fill", "stroke",
               "box-shadow", "text-shadow", "text-decoration", "text-decoration-color", "caret-color",
               "accent-color", "stop-color", "flood-color", "lighting-color", "column-rule-color"}
SCALE_PROPS = {"font-size", "line-height", "letter-spacing", "gap", "row-gap", "column-gap",
               "padding", "padding-top", "padding-right", "padding-bottom", "padding-left",
               "padding-inline", "padding-block", "margin", "margin-top", "margin-right", "margin-bottom",
               "margin-left", "margin-inline", "margin-block", "border-radius", "border-top-left-radius",
               "border-top-right-radius", "border-bottom-left-radius", "border-bottom-right-radius"}
NAMED = {"white", "black", "red", "green", "blue", "yellow", "orange", "purple", "pink", "gray", "grey",
         "silver", "navy", "teal", "maroon", "olive", "lime", "aqua", "cyan", "magenta", "fuchsia", "brown",
         "gold", "indigo", "violet", "crimson", "coral", "salmon", "tomato", "beige", "ivory", "khaki",
         "tan", "turquoise", "orchid", "plum", "lavender", "chocolate", "firebrick", "darkgray", "darkgrey",
         "lightgray", "lightgrey", "dimgray", "whitesmoke", "gainsboro", "skyblue", "steelblue",
         "royalblue", "slategray", "seagreen", "forestgreen", "darkblue", "darkred", "darkgreen"}
FONT_KEYWORDS = {"inherit", "initial", "unset", "revert", "revert-layer"}


def camel_to_kebab(name: str) -> str:
    return re.sub(r"[A-Z]", lambda m: "-" + m.group(0).lower(), name)


def blank(text: str, pattern: re.Pattern) -> str:
    """Replace matches with spaces, keeping newlines, so offsets and line numbers hold."""
    return pattern.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), text)


BLOCK_COMMENT = re.compile(r"/\*.*?\*/|<!--.*?-->", re.S)
LINE_COMMENT = re.compile(r"(?:(?<=\s)|^)//[^\n]*", re.M)
STRING_URL = re.compile(r"url\([^)]*\)", re.I)


# ---------- colours ----------

def _num(part: str, scale: float) -> float:
    part = part.strip()
    if part.endswith("%"):
        return float(part[:-1]) / 100 * scale
    return float(part)


def parse_color(text: str) -> tuple[float, float, float, float] | None:
    """sRGB 0..1 and alpha for hex, rgb() and hsl(); None for anything else."""
    text = text.strip()
    m = re.fullmatch(r"#([0-9a-fA-F]{3,8})", text)
    if m:
        h = m.group(1)
        if len(h) in (3, 4):
            h = "".join(c * 2 for c in h)
        if len(h) not in (6, 8):
            return None
        vals = [byte / 255 for byte in bytes.fromhex(h)] + [1.0]
        return tuple(vals[:4])
    m = re.fullmatch(r"(rgba?|hsla?)\(\s*(.*?)\s*\)", text, re.I)
    if not m:
        return None
    body = m.group(2).replace("/", " ").replace(",", " ").split()
    if len(body) not in (3, 4):
        return None
    try:
        alpha = _num(body[3], 1) if len(body) == 4 else 1.0
        if m.group(1).lower().startswith("rgb"):
            r, g, b = (_num(p, 255) / 255 for p in body[:3])
        else:
            hue = float(body[0].rstrip("deg")) % 360
            sat, light = _num(body[1], 1), _num(body[2], 1)
            r, g, b = hsl_to_rgb(hue, min(sat, 1), min(light, 1))
    except ValueError:
        return None
    return (min(max(r, 0), 1), min(max(g, 0), 1), min(max(b, 0), 1), min(max(alpha, 0), 1))


def hsl_to_rgb(h: float, s: float, l: float) -> tuple[float, float, float]:
    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c / 2
    r, g, b = [(c, x, 0), (x, c, 0), (0, c, x), (0, x, c), (x, 0, c), (c, 0, x)][int(h // 60) % 6]
    return r + m, g + m, b + m


def oklab(rgb) -> tuple[float, float, float]:
    offset = 0.055  # sRGB transfer curve: a straight toe below 0.04045, a 2.4 power above

    def linear(v):
        return pow((v + offset) / (1 + offset), 2.4) if v > 0.04045 else v / 12.92
    r, g, b = (linear(v) for v in rgb[:3])
    l_ = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m_ = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s_ = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = (math.copysign(abs(v) ** (1 / 3), v) for v in (l_, m_, s_))
    return (0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
            1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
            0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_)


def distance(a, b) -> float:
    """OKLab distance times 100; about 2 is the smallest difference most people notice."""
    return 100 * math.dist(oklab(a), oklab(b))


def hex_of(rgb) -> str:
    return "#" + "".join(f"{round(c * 255):02x}" for c in rgb[:3])


# ---------- token stylesheets ----------

class Tokens:
    def __init__(self, paths: list[Path]):
        self.defs: dict[str, str] = {}
        self.files = [p.resolve() for p in paths]
        for path in paths:
            text = blank(path.read_text(encoding="utf-8"), BLOCK_COMMENT)
            for name, value in VAR_DEF.findall(text):
                self.defs.setdefault(name, value.strip())
        self.colors: dict[str, tuple] = {}
        self.lengths: set[tuple[float, str]] = set()   # sizes held by a token whose value is one length
        self.step = None                                # Tailwind v4 style --spacing: multiples are on scale
        for name in self.defs:
            value = self.resolve(name)
            col = parse_color(value) if value else None
            if col:
                self.colors[name] = col
            elif value and (m := SINGLE_LENGTH.fullmatch(value.strip())):
                size = to_px(m.group(1), m.group(2))
                self.lengths.add(size)
                if name == "--spacing" and size[1] == "px" and size[0] > 0:
                    self.step = size[0]

    def on_scale(self, size, spacing: bool) -> bool:
        if any(abs(size[0] - v) < 0.01 and size[1] == u for v, u in self.lengths):
            return True
        if spacing and self.step and size[1] == "px":
            ratio = size[0] / self.step
            return abs(ratio - round(ratio)) < 0.01
        return False

    def resolve(self, name: str, seen: frozenset = frozenset()) -> str | None:
        value = self.defs.get(name)
        if value is None or name in seen:
            return None
        m = re.fullmatch(r"var\(\s*(--[\w-]+)\s*(?:,[^)]*)?\)", value)
        return self.resolve(m.group(1), seen | {name}) if m else value

    def suggest(self, col) -> list[str]:
        """Token names whose colour matches; roles (defined through var()) before raw primitives."""
        same = [n for n, c in self.colors.items() if distance(c, col) < 0.5 and abs(c[3] - col[3]) < 0.02]
        return sorted(same, key=lambda n: (not self.defs[n].startswith("var("), n))[:3]

    def nearest(self, col):
        best = min(self.colors.items(), key=lambda kv: distance(kv[1], col), default=None)
        return (best[0], distance(best[1], col)) if best else (None, math.inf)


SINGLE_LENGTH = re.compile(r"(-?\d*\.?\d+)(px|rem|em)")
SPACING_PROPS = {"gap", "row-gap", "column-gap"}


def to_px(num: str, unit: str) -> tuple[float, str]:
    """rem counts as 16px so 1rem and 16px are the same step; em stays relative to its element."""
    value = float(num)
    return (value * 16, "px") if unit == "rem" else (value, unit)


# ---------- scanning ----------

def regions(path: Path, text: str):
    """Yield (offset, css_text, kind) pieces of a file that hold declarations."""
    ext = path.suffix.lower()
    if ext in CSS_EXT:
        yield 0, blank(blank(text, BLOCK_COMMENT), STRING_URL), "css"
        return
    if ext in SCRIPT_EXT:
        clean = blank(blank(blank(text, BLOCK_COMMENT), LINE_COMMENT), STRING_URL)
        yield 0, clean, "script"
        return
    clean = blank(text, BLOCK_COMMENT)
    for m in STYLE_TAG.finditer(clean):
        yield m.start(1), blank(m.group(1), STRING_URL), "css"
    for m in STYLE_ATTR.finditer(clean):
        yield m.start(2), m.group(2), "css"
    for m in ATTR.finditer(clean):
        if not m.group(3).lstrip().startswith(("{", "url(")):
            yield m.start(3), f"{m.group(1).lower()}: {m.group(3)}", "attr"


def files_under(paths: list[Path]):
    for p in paths:
        if p.is_file():
            yield p
        elif p.is_dir():
            for f in sorted(p.rglob("*")):
                rel = f.relative_to(p).parts
                if f.is_file() and f.suffix.lower() in PAGE_EXT | CSS_EXT | SCRIPT_EXT and not any(
                        part in SKIP_DIRS or part.startswith(".") for part in rel[:-1]):
                    yield f


def scan(tokens: Tokens, paths: list[Path], only: set[str] | None = None):
    findings, sources, local_defs, uses = [], [], set(), []
    for f in files_under(paths):
        if f.resolve() in tokens.files:
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        if "token-check: ignore-file" in text:
            continue
        sources.append(str(f))
        lines = text.splitlines()
        ignored = {i + 1 for i, line in enumerate(lines) if "token-check: ignore" in line}

        def add(rule, offset, msg, fix=""):
            line = text.count("\n", 0, offset) + 1
            if line not in ignored and (only is None or rule in only):
                findings.append({"rule": rule, "level": LEVEL[rule], "file": str(f), "line": line,
                                 "message": msg, "fix": fix})

        for base, css, kind in regions(f, text):
            for name, _ in VAR_DEF.findall(css):
                local_defs.add(name)
            for m in VAR_USE.finditer(css):
                uses.append((add, base + m.start(), m.group(1)))
            for m in DECL.finditer(css):
                prop, value = m.group(1), m.group(2)
                if prop.startswith("--") or (kind == "attr" and m.start() != 0):
                    continue
                prop = camel_to_kebab(prop) if kind == "script" else prop.lower()
                at = base + m.start(2)
                check_value(tokens, add, prop, value, at, kind)
    defined = set(tokens.defs) | local_defs
    for add, offset, name in uses:
        if name not in defined:
            add("unknown-var", offset, f"var({name}) is not defined in the token file or the scanned files",
                "define it in the token source or use an existing name")
    findings.sort(key=lambda x: (x["file"], x["line"], x["rule"]))
    return findings, sources


def check_value(tokens, add, prop, value, at, kind):
    value_no_vars = re.sub(r"var\([^()]*(?:\([^()]*\))?[^()]*\)", lambda m: " " * len(m.group(0)), value)
    for m in HEX.finditer(value_no_vars):
        report_color(tokens, add, m.group(0), at + m.start(), prop)
    for m in FUNC.finditer(value_no_vars):
        report_color(tokens, add, m.group(0), at + m.start(), prop)
    if prop in COLOR_PROPS:
        for word in re.findall(r"[a-zA-Z]+", value_no_vars):
            if word.lower() in NAMED:
                idx = value_no_vars.find(word)
                add("named-color", at + idx, f"{prop}: '{word}' is a colour name, not a token",
                    "use a colour role such as var(--foreground)")
                break
    if prop == "font-family" and "var(" not in value:
        bare = value.strip().strip("'\"").strip().lower()
        if bare and bare not in FONT_KEYWORDS:
            add("raw-font", at, f"font-family names '{value.strip()[:40]}' by hand", "use var(--font-...)")
    if prop in SCALE_PROPS and tokens.lengths and kind != "script" and "var(" not in value:
        spacing = prop in SPACING_PROPS or prop.startswith(("padding", "margin"))
        for m in LENGTH.finditer(value):
            if float(m.group(1)) in (0.0, 1.0, -1.0) and m.group(2) == "px":
                continue
            if not tokens.on_scale(to_px(*m.groups()), spacing):
                add("off-scale", at + m.start(), f"{prop}: {m.group(0)} is not on the token scale",
                    "pick the nearest token size")
                break


def report_color(tokens, add, literal, offset, prop):
    col = parse_color(literal)
    names = tokens.suggest(col) if col else []
    fix = "use " + " or ".join(f"var({n})" for n in names) if names else (
        f"nearest token: var({tokens.nearest(col)[0]})" if col and tokens.colors else "add it to the tokens first")
    add("raw-color", offset, f"{prop}: {literal} is written by hand", fix)


# ---------- embedding ----------

TOKEN_BLOCK = re.compile(r"[ \t]*<style data-tokens=\"[^\"]*\">.*?</style>\n?", re.S)


def used_css(css: str, page: str) -> str:
    """Keep only the custom properties the page uses, and the ones they point at."""
    clean = blank(css, BLOCK_COMMENT)
    if re.search(r"\{[^{}]*\{", clean):
        raise ValueError("--used needs a flat token stylesheet (no nested blocks such as @media)")
    defs = {}
    for name, value in VAR_DEF.findall(clean):
        defs.setdefault(name, []).append(value)
    want, todo = set(), list(VAR_USE.findall(blank(page, BLOCK_COMMENT)))
    while todo:
        name = todo.pop()
        if name in want:
            continue
        want.add(name)
        for value in defs.get(name, []):
            todo.extend(VAR_USE.findall(value))
    out = []
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", clean):
        keep = [f"  {n}: {v.strip()};" for n, v in VAR_DEF.findall(m.group(2)) if n in want]
        if keep:
            out.append(m.group(1).strip() + " {\n" + "\n".join(keep) + "\n}")
    return "\n".join(out) + "\n"


def embed(token_paths: list[Path], page: str, only_used: bool) -> str:
    parts = []
    for p in token_paths:
        css = p.read_text(encoding="utf-8")
        parts.append(used_css(css, page) if only_used else css.strip() + "\n")
    label = ",".join(p.name for p in token_paths)
    block = f'<style data-tokens="{label}">\n' + "".join(parts) + "</style>\n"
    page = TOKEN_BLOCK.sub("", page)
    m = re.search(r"<head\b[^>]*>\n?", page, re.I)
    if m:
        return page[:m.end()] + block + page[m.end():]
    m = re.match(r"\s*<!doctype[^>]*>\n?", page, re.I)
    at = m.end() if m else 0
    return page[:at] + block + page[at:]


# ---------- asset colours ----------

def png_pixels(data: bytes):
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")
    pos, idat, palette, trns = 8, [], None, None
    width = height = depth = ctype = None
    while pos < len(data):
        length, kind = struct.unpack(">I4s", data[pos:pos + 8])
        body = data[pos + 8:pos + 8 + length]
        pos += 12 + length
        if kind == b"IHDR":
            width, height, depth, ctype, _, _, interlace = struct.unpack(">IIBBBBB", body)
            if depth != 8 or interlace or ctype not in (0, 2, 3, 4, 6):
                raise ValueError("only 8-bit, non-interlaced PNGs are read; re-export it that way")
            if width * height > 2_000_000:
                raise ValueError("PNG over 2 megapixels; check a smaller export")
        elif kind == b"PLTE":
            palette = [tuple(body[i:i + 3]) for i in range(0, len(body), 3)]
        elif kind == b"tRNS":
            trns = body
        elif kind == b"IDAT":
            idat.append(body)
        elif kind == b"IEND":
            break
    if width is None:
        raise ValueError("PNG has no header")
    channels = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[ctype]
    raw = zlib.decompress(b"".join(idat))
    stride = width * channels
    prev = bytearray(stride)
    rows = []
    for y in range(height):
        f = raw[y * (stride + 1)]
        line = bytearray(raw[y * (stride + 1) + 1:(y + 1) * (stride + 1)])
        for i in range(stride if f else 0):
            a = line[i - channels] if i >= channels else 0
            b = prev[i]
            c = prev[i - channels] if i >= channels else 0
            if f == 1:
                line[i] = (line[i] + a) & 255
            elif f == 2:
                line[i] = (line[i] + b) & 255
            elif f == 3:
                line[i] = (line[i] + (a + b) // 2) & 255
            elif f == 4:
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                line[i] = (line[i] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
        rows.append(bytes(line))
        prev = line
    for line in rows:
        for x in range(width):
            px = line[x * channels:(x + 1) * channels]
            if ctype == 6:
                yield px[0], px[1], px[2], px[3]
            elif ctype == 2:
                yield px[0], px[1], px[2], 255
            elif ctype == 4:
                yield px[0], px[0], px[0], px[1]
            elif ctype == 0:
                yield px[0], px[0], px[0], 255
            else:
                r, g, b = palette[px[0]]
                yield r, g, b, trns[px[0]] if trns and px[0] < len(trns) else 255


def asset_colors(path: Path, min_share: float):
    """[(hex, share)] of the colours an asset uses."""
    if path.suffix.lower() == ".png":
        counts, total = {}, 0
        for r, g, b, a in png_pixels(path.read_bytes()):
            if a < 128:
                continue
            total += 1
            counts[(r, g, b)] = counts.get((r, g, b), 0) + 1
        found = [(f"#{r:02x}{g:02x}{b:02x}", n / total) for (r, g, b), n in counts.items() if total]
        return sorted([c for c in found if c[1] >= min_share], key=lambda c: -c[1])
    if path.suffix.lower() not in PAGE_EXT | CSS_EXT:
        raise ValueError(f"{path.name}: colors reads PNG, SVG, HTML and CSS files")
    text = blank(path.read_text(encoding="utf-8", errors="replace"), BLOCK_COMMENT)
    counts = {}
    for m in list(HEX.finditer(text)) + list(FUNC.finditer(text)):
        col = parse_color(m.group(0))
        if col:
            counts[hex_of(col)] = counts.get(hex_of(col), 0) + 1
    total = sum(counts.values()) or 1
    return sorted(((h, n / total) for h, n in counts.items()), key=lambda c: -c[1])


# ---------- commands ----------

def load_tokens(paths):
    for p in paths:
        if not p.is_file():
            raise FileNotFoundError(f"token file not found: {p}")
    return Tokens(paths)


def cmd_scan(args) -> int:
    tokens = load_tokens(args.tokens)
    only = set(args.only.split(",")) if args.only else None
    if only and only - set(LEVEL):
        print(f"unknown rule(s): {', '.join(sorted(only - set(LEVEL)))}", file=sys.stderr)
        return 2
    targets = [Path(p) for p in args.paths]
    missing = [str(p) for p in targets if not p.exists()]
    if missing:
        print(f"not found: {', '.join(missing)}", file=sys.stderr)
        return 2
    findings, sources = scan(tokens, targets, only)
    counts = {name: sum(f["rule"] == name for f in findings) for name, _, _ in RULES if name != "off-palette"}
    errors = sum(f["level"] == "error" for f in findings)
    if args.json:
        print(json.dumps({"files": len(sources), "tokens": len(tokens.defs), "counts": counts,
                          "scale_checked": bool(tokens.lengths), "findings": findings}, indent=2))
    else:
        for f in findings:
            print(f"{f['file']}:{f['line']}: {f['level']} {f['rule']}: {f['message']}" + (f" ({f['fix']})" if f["fix"] else ""))
        note = "" if tokens.lengths else "; no sizes in the tokens, so off-scale was not checked"
        print(f"{len(sources)} file(s), {len(tokens.defs)} token(s): {errors} error(s), "
              f"{len(findings) - errors} warning(s){note}")
    return 1 if errors or (args.strict and findings) else 0


def cmd_embed(args) -> int:
    load_tokens(args.tokens)
    page = Path(args.page).read_text(encoding="utf-8")
    try:
        out = embed(args.tokens, page, args.used)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 2
    Path(args.out).write_text(out, encoding="utf-8")
    print(f"wrote {args.out} with {', '.join(p.name for p in args.tokens)} embedded")
    return 0


def cmd_colors(args) -> int:
    tokens = load_tokens(args.tokens)
    if not tokens.colors:
        print("the token file defines no colours", file=sys.stderr)
        return 2
    report, off = [], 0
    for name in args.assets:
        path = Path(name)
        try:
            found = asset_colors(path, args.min_share)
        except (OSError, ValueError, zlib.error) as exc:
            print(f"{name}: {exc}", file=sys.stderr)
            return 2
        for hx, share in found:
            col = parse_color(hx)
            token, dist = tokens.nearest(col)
            bad = dist > args.max_distance
            off += bad
            report.append({"file": name, "color": hx, "share": round(share, 4), "nearest": token,
                           "distance": round(dist, 2), "off_palette": bad})
    if args.json:
        print(json.dumps({"colors": report, "off_palette": off}, indent=2))
    else:
        for r in report:
            mark = "off-palette" if r["off_palette"] else "ok"
            print(f"{r['file']}: {r['color']} {r['share']:.1%} -> var({r['nearest']}) at {r['distance']} {mark}")
        print(f"{len(report)} colour(s), {off} off the palette (max distance {args.max_distance})")
    return 1 if off else 0


def png_bytes(width, height, rgba_rows) -> bytes:
    """A tiny RGBA PNG writer, used by the self-check and the tests."""
    raw = b"".join(b"\x00" + bytes(v for px in row for v in px) for row in rgba_rows)

    def chunk(kind, body):
        return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind + body))
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))


def self_check() -> int:
    problems = []
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        tok = d / "tokens.css"
        tok.write_text(":root {\n  --color-moss-600: #2f6b4f;\n  --color-ink-50: #f6f7f6;\n"
                       "  --primary: var(--color-moss-600);\n  --space-4: 16px;\n  --font-body: Inter, sans-serif;\n}\n")
        page = d / "page.html"
        page.write_text("<!doctype html><html><head><style>\n.a { color: #2F6B4F; padding: 16px; }\n"
                        ".b { margin: 13px; font-family: Arial; background: white; }\n"
                        ".c { color: var(--nope); border-color: var(--primary); }\n"
                        ".d { color: #123456; } /* token-check: ignore */\n</style></head>"
                        "<body><p style=\"color: rgb(246 247 246)\">x</p></body></html>\n")
        tokens = Tokens([tok])
        findings, _ = scan(tokens, [d])
        got = sorted((f["rule"], f["line"]) for f in findings)
        want = sorted([("raw-color", 2), ("off-scale", 3), ("raw-font", 3), ("named-color", 3),
                       ("unknown-var", 4), ("raw-color", 6)])
        if got != want:
            problems.append(f"scan found {got}, expected {want}")
        first = next((f for f in findings if f["rule"] == "raw-color"), {})
        if "var(--primary)" not in first.get("fix", ""):
            problems.append("raw colour equal to a role should suggest the role first")
        once = embed([tok], page.read_text(), True)
        twice = embed([tok], once, True)
        if once != twice or once.count("data-tokens") != 1 or "--color-ink-50" in once:
            problems.append("embed --used is not idempotent or kept unused tokens")
        if "--color-moss-600" not in once:
            problems.append("embed --used dropped a token a used role points at")
        png = d / "a.png"
        png.write_bytes(png_bytes(2, 2, [[(47, 107, 79, 255), (47, 107, 79, 255)], [(200, 30, 30, 255), (0, 0, 0, 0)]]))
        cols = dict(asset_colors(png, 0.0))
        if set(cols) != {"#2f6b4f", "#c81e1e"} or abs(cols["#2f6b4f"] - 2 / 3) > 1e-9:
            problems.append(f"PNG colours read as {cols}")
        if tokens.nearest(parse_color("#c81e1e"))[1] < 2:
            problems.append("an off-palette red measured as close")
        if parse_color("hsl(120 100% 25%)") is None or hex_of(parse_color("hsl(120 100% 25%)")) != "#008000":
            problems.append("hsl() parsed wrongly")
    for p in problems:
        print("problem:", p)
    print(f"token_check self-check: {len(problems)} problem(s)")
    return 1 if problems else 0


def main(argv=None) -> int:
    ap = ArgumentParser(description="Check that pages and assets draw their values from tokens.")
    ap.add_argument("--self-check", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    s = sub.add_parser("scan")
    s.add_argument("--tokens", type=Path, action="append", required=True)
    s.add_argument("paths", nargs="+")
    s.add_argument("--json", action="store_true")
    s.add_argument("--strict", action="store_true", help="exit 1 on warnings too")
    s.add_argument("--only", help="comma-separated rule names")
    e = sub.add_parser("embed")
    e.add_argument("--tokens", type=Path, action="append", required=True)
    e.add_argument("page")
    e.add_argument("--out", required=True)
    e.add_argument("--used", action="store_true", help="keep only the properties the page needs")
    c = sub.add_parser("colors")
    c.add_argument("--tokens", type=Path, action="append", required=True)
    c.add_argument("assets", nargs="+")
    c.add_argument("--max-distance", type=float, default=2.0)
    c.add_argument("--min-share", type=float, default=0.005, help="PNG: ignore colours below this share")
    c.add_argument("--json", action="store_true")
    sub.add_parser("rules")
    try:
        args = ap.parse_args(argv)
    except SystemExit as exc:
        return 2 if exc.code else 0
    if args.self_check:
        return self_check()
    if args.cmd == "rules":
        for name, level, what in RULES:
            print(f"{name}: {level}: {what}")
        return 0
    commands = {"scan": cmd_scan, "embed": cmd_embed, "colors": cmd_colors}
    if args.cmd not in commands:
        ap.print_usage(sys.stderr)
        return 2
    try:
        return commands[args.cmd](args)
    except (OSError, UnicodeDecodeError) as exc:
        print(exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
