#!/usr/bin/env python3
"""Lint built HTML and CSS for the machine-checkable design tells.

Standard library only, no network. Reads .html/.htm files and the .css files
they link with a relative path, plus any .css passed directly. Each rule
names the row it checks in slop-tells.csv (this folder) or
../hallmark/gates.csv. A hit is evidence to look at, not a verdict; the
judgement rows in those tables still need a person or a reviewer.

Usage:
    page_lint.py PATH [PATH ...] [--only RULE,RULE] [--json] [--rules]
Exit 1 when anything is found, 0 when clean, 2 on bad arguments.
"""
import argparse
import colorsys
import json
import os
import re
import sys
from html.parser import HTMLParser

RULES = {
    # rule: (severity, tell id, note)
    "purple-gradient": ("medium", "classic-purple-gradient / gate 2a",
                        "gradient through purple, violet or indigo; pick one anchor hue and use solid colour"),
    "gradient-text": ("medium", "gradient-text / gate 2b",
                      "gradient-filled text; use one solid colour and weight for emphasis"),
    "pure-black-white": ("low", "gate 7a",
                         "pure #000 or #fff set directly on an element rather than in :root tokens; shift it slightly toward the brand hue"),
    "system-font-main": ("medium", "classic-system-font",
                         "system font stack is the main face; choose and name a pairing"),
    "default-font": ("low", "overused-font",
                     "a very common default face is the display or body font; check it was chosen on purpose"),
    "uniform-radius": ("medium", "classic-uniform-radius",
                       "one border-radius on almost everything; set radii by element role"),
    "left-border-card": ("medium", "classic-left-border-card / border-accent-on-rounded",
                         "thick coloured left border on a rounded box"),
    "glow": ("medium", "dark-glow / radial-halo",
             "large coloured glow shadow or halo; use plain contrast"),
    "frosted-glass": ("medium", "judge-frosted-glass",
                      "backdrop blur used on several surfaces; keep it to one layer whose depth is explained"),
    "marquee": ("medium", "marquee",
                "scrolling strip (marquee element or endless horizontal animation)"),
    "flat-type-scale": ("medium", "flat-type-hierarchy",
                        "h1 and h2 sizes too close to read as two levels (ratio under 1.2)"),
    "emoji-heading": ("medium", "classic-emoji-design",
                      "emoji in a heading"),
    "generic-copy": ("high", "classic-generic-hero-copy / marketing-buzzword",
                     "stock marketing phrase; say what it is and who it is for"),
    "vague-cta": ("medium", "judge-vague-cta",
                  "every call to action is generic (Get started, Learn more); name what the click gets"),
    "eyebrow-chip": ("low", "hero-eyebrow-chip / kicker-above-heading",
                     "short pill or label right above the h1"),
    "nested-cards": ("medium", "nested-cards",
                     "a card inside a card; flatten with spacing or a rule"),
    "placeholder": ("high", "judge-stock-hero",
                    "placeholder text or image left in the page"),
    "img-no-alt": ("medium", "accessibility",
                   "img without an alt attribute (use alt=\"\" for decoration)"),
}

GENERIC_PHRASES = (
    "welcome to", "unlock the power", "all-in-one", "all in one solution", "seamless",
    "revolutioni", "supercharge", "next-generation", "next generation", "game-changer",
    "game changer", "elevate your", "cutting-edge", "cutting edge", "empower your",
    "take your business to the next level", "world-class", "best-in-class", "leverage the power",
    "harness the power", "transform the way", "in today's fast-paced",
)
VAGUE_CTA = {"get started", "learn more", "start now", "sign up", "try it", "try now",
             "click here", "discover more", "explore", "read more", "start free"}
DEFAULT_FONTS = ("inter", "poppins", "montserrat", "roboto", "open sans", "lato", "arial", "helvetica")
SYSTEM_FIRST = ("system-ui", "-apple-system", "blinkmacsystemfont", "ui-sans-serif", "segoe ui")
PLACEHOLDER = re.compile(r"lorem ipsum|placehold\.co|placeholder\.com|via\.placeholder|dummyimage\.com|picsum\.photos|\[your (?:company|name|product)\]", re.I)
EMOJI = re.compile("[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F000-\U0001F2FF]")
NAMED_PURPLE = re.compile(r"\b(purple|violet|indigo|blueviolet|darkviolet|mediumpurple|rebeccapurple|fuchsia|magenta|orchid)\b", re.I)
HEX = re.compile(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")
RGB = re.compile(r"rgba?\(\s*(\d+)[ ,]+(\d+)[ ,]+(\d+)")
HSL = re.compile(r"hsla?\(\s*(-?\d+(?:\.\d+)?)(?:deg)?[ ,]+(\d+(?:\.\d+)?)%")
OKLCH = re.compile(r"oklch\(\s*[\d.]+%?\s+([\d.]+)\s+([\d.]+)")
DECL = re.compile(r"([\w-]+)\s*:\s*([^;{}]+)")
RULE_BLOCK = re.compile(r"([^{}]+)\{([^{}]*)\}")
CARD_CLASS = re.compile(r"(^|[\s_-])card(s)?($|[\s_-])", re.I)
CHIP_CLASS = re.compile(r"eyebrow|kicker|badge|pill|chip|tag|overline|label", re.I)
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


def hue_sat(color):
    """Return (hue degrees, saturation 0-1) for a colour literal, or None."""
    m = HEX.fullmatch(color.strip())
    if m:
        h = m.group(1)
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    else:
        m = RGB.match(color.strip())
        if m:
            r, g, b = (int(x) / 255 for x in m.groups())
        else:
            m = HSL.match(color.strip())
            if m:
                return float(m.group(1)) % 360, float(m.group(2)) / 100
            m = OKLCH.match(color.strip())
            if m:
                c, h = float(m.group(1)), float(m.group(2))
                # OKLCH hue runs differently from HSL; purple sits near 280-330.
                return ((h - 20) % 360, min(c / 0.2, 1.0))
            return None
    hh, ll, ss = colorsys.rgb_to_hls(r, g, b)
    return hh * 360, ss if 0.05 < ll < 0.95 else 0.0


def colours_in(value):
    out = [m.group(0) for m in HEX.finditer(value)]
    out += [m.group(0) for m in RGB.finditer(value)]
    out += [m.group(0) for m in HSL.finditer(value)]
    out += [m.group(0) for m in OKLCH.finditer(value)]
    return out


def is_purple(value):
    if NAMED_PURPLE.search(value):
        return True
    for c in colours_in(value):
        hs = hue_sat(c)
        if hs and 250 <= hs[0] <= 320 and hs[1] >= 0.25:
            return True
    return False


def px(value):
    m = re.match(r"\s*([\d.]+)(px|rem|em)?", value)
    if not m:
        return None
    n = float(m.group(1))
    return n * 16 if m.group(2) in ("rem", "em") else n


class Finder:
    def __init__(self):
        self.found = []

    def add(self, path, line, rule, extra=""):
        sev, tell, note = RULES[rule]
        self.found.append({"file": path, "line": line, "rule": rule, "severity": sev,
                           "tell": tell, "note": note + (f" ({extra})" if extra else "")})


def lint_css(css, path, f, base_line=1):
    radii, blurs, sizes = [], [], {}
    for m in RULE_BLOCK.finditer(css):
        sel = m.group(1).strip().split("}")[-1].strip()
        body = m.group(2)
        line = base_line + css.count("\n", 0, m.start(2))
        decls = {}
        for d in DECL.finditer(body):
            decls[d.group(1).lower()] = d.group(2).strip()
        in_tokens = sel in (":root", "html", ":host") or sel.startswith(":root") or sel.startswith("@")
        for prop, val in decls.items():
            low = val.lower()
            if "gradient(" in low and is_purple(low):
                f.add(path, line, "purple-gradient", sel)
            if prop in ("background-clip", "-webkit-background-clip") and "text" in low:
                if "gradient(" in (decls.get("background", "") + decls.get("background-image", "")).lower():
                    f.add(path, line, "gradient-text", sel)
            if not in_tokens and not prop.startswith("--") and prop in (
                    "color", "background", "background-color", "border-color", "fill", "stroke"):
                if re.search(r"(^|\s)(#000(000)?|#fff(fff)?|black|white)\b", low):
                    f.add(path, line, "pure-black-white", f"{sel} {{ {prop}: {val} }}")
            if prop == "font-family" and (sel in ("body", "html", ":root") or re.search(r"\bh1\b", sel)):
                first = low.split(",")[0].strip().strip("'\"")
                if first in SYSTEM_FIRST:
                    f.add(path, line, "system-font-main", sel)
                elif first in DEFAULT_FONTS:
                    f.add(path, line, "default-font", f"{sel}: {first}")
            if prop == "border-radius" and not in_tokens:
                radii.append((low, line))
            if prop in ("box-shadow", "text-shadow", "filter"):
                for sm in re.finditer(r"(-?\d+)(?:px)?\s+(-?\d+)(?:px)?\s+(\d+)px(?:\s+(-?\d+)(?:px)?)?\s+((?:rgba?|hsla?|oklch)\([^)]*\)|#[0-9a-f]{3,6})", low):
                    blur = int(sm.group(3))
                    col = sm.group(5)
                    hs = None
                    for c in colours_in(col):
                        hs = hue_sat(c)
                    if blur >= 40 and hs and hs[1] >= 0.3:
                        f.add(path, line, "glow", sel)
                        break
                if "drop-shadow" in low and re.search(r"drop-shadow\([^)]*\b([4-9]\d|\d{3,})px", low):
                    f.add(path, line, "glow", sel)
            if prop in ("backdrop-filter", "-webkit-backdrop-filter") and "blur" in low:
                blurs.append(line)
            if prop.startswith("border-left") and prop != "border-left-color":
                w = px(low)
                if w and w >= 3 and "border-radius" in decls and px(decls["border-radius"]) not in (None, 0.0):
                    f.add(path, line, "left-border-card", sel)
            if prop == "font-size":
                for tag in ("h1", "h2"):
                    if re.fullmatch(rf"{tag}|.*\b{tag}\b(?![-\w])", sel.split(",")[0].strip()):
                        v = px(low) if not low.startswith(("clamp", "calc", "var")) else None
                        if v:
                            sizes[tag] = (v, line)
        anim = decls.get("animation", "") + decls.get("animation-iteration-count", "")
        if "infinite" in anim.lower() and re.search(r"marquee|ticker|scroll|logos?", anim + sel, re.I):
            f.add(path, line, "marquee", sel)
    if len(radii) >= 6:
        counts = {}
        for v, _ in radii:
            counts[v] = counts.get(v, 0) + 1
        top, n = max(counts.items(), key=lambda x: x[1])
        if n / len(radii) >= 0.8:
            f.add(path, radii[0][1], "uniform-radius", f"{n} of {len(radii)} rules use {top}")
    if len(blurs) >= 3:
        f.add(path, blurs[0], "frosted-glass", f"{len(blurs)} surfaces")
    if "h1" in sizes and "h2" in sizes and sizes["h2"][0] > 0 and sizes["h1"][0] / sizes["h2"][0] < 1.2:
        f.add(path, sizes["h1"][1], "flat-type-scale",
              f"h1 {sizes['h1'][0]:g}px, h2 {sizes['h2'][0]:g}px")


class Page(HTMLParser):
    def __init__(self, path, f):
        super().__init__(convert_charrefs=True)
        self.path, self.f = path, f
        self.stack = []          # (tag, is_card, line)
        self.css = []            # (text, line)
        self.links = []
        self.in_style = False
        self.text_tag = None     # heading or action being collected
        self.text = []
        self.ctas = []
        self.last_short = None   # (class, text, line) of the last closed small element
        self.cur_small = None
        self.body_text = []
        self.skip = 0

    def cls(self, attrs):
        return dict(attrs).get("class", "") or ""

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        line = self.getpos()[0]
        if tag == "style":
            self.in_style = True
            self.style_line = line
            return
        if tag in ("script", "noscript", "template"):
            self.skip += 1
        if tag == "link" and "stylesheet" in (a.get("rel") or "").lower() and a.get("href"):
            self.links.append(a["href"])
        if tag == "marquee":
            self.f.add(self.path, line, "marquee", "<marquee>")
        if tag == "img":
            if "alt" not in a:
                self.f.add(self.path, line, "img-no-alt", a.get("src", ""))
            if PLACEHOLDER.search(a.get("src", "") or ""):
                self.f.add(self.path, line, "placeholder", a.get("src", ""))
        if a.get("style"):
            lint_css("x{" + a["style"] + "}", self.path, self.f, line)
        c = self.cls(attrs)
        is_card = bool(CARD_CLASS.search(c))
        if is_card and any(s[1] for s in self.stack):
            self.f.add(self.path, line, "nested-cards", c)
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6", "button") or (tag == "a" and re.search(r"btn|button|cta", c, re.I)):
            self.text_tag, self.text, self.text_line = tag, [], line
            if tag == "h1" and self.last_short and CHIP_CLASS.search(self.last_short[0]):
                self.f.add(self.path, self.last_short[2], "eyebrow-chip", self.last_short[1])
        if tag in ("span", "p", "div", "small") and CHIP_CLASS.search(c):
            self.cur_small = [c, [], line, len(self.stack)]
        elif tag not in VOID:
            self.last_short = None
        if tag not in VOID:
            self.stack.append((tag, is_card, line))

    def handle_endtag(self, tag):
        if tag == "style":
            self.in_style = False
            return
        if tag in ("script", "noscript", "template") and self.skip:
            self.skip -= 1
        if self.text_tag == tag:
            t = " ".join("".join(self.text).split())
            if tag.startswith("h") and EMOJI.search(t):
                self.f.add(self.path, self.text_line, "emoji-heading", t[:60])
            if tag in ("button", "a"):
                self.ctas.append((t.lower().rstrip("!. →>"), self.text_line))
            self.text_tag = None
        while self.stack:
            top = self.stack.pop()
            if top[0] == tag:
                break
        if self.cur_small and len(self.stack) == self.cur_small[3]:
            t = " ".join("".join(self.cur_small[1]).split())
            self.last_short = (self.cur_small[0], t, self.cur_small[2]) if 0 < len(t.split()) <= 5 else None
            self.cur_small = None

    def handle_data(self, data):
        if self.in_style:
            self.css.append((data, self.style_line))
            return
        if self.skip:
            return
        if self.text_tag:
            self.text.append(data)
        if self.cur_small:
            self.cur_small[1].append(data)
        if data.strip():
            self.body_text.append((data, self.getpos()[0]))

    def finish(self):
        for data, line in self.body_text:
            low = " ".join(data.lower().split())
            for p in GENERIC_PHRASES:
                if p in low:
                    self.f.add(self.path, line, "generic-copy", f"\"{p}\"")
                    break
            if PLACEHOLDER.search(data):
                self.f.add(self.path, line, "placeholder", PLACEHOLDER.search(data).group(0))
        if self.ctas and all(t in VAGUE_CTA for t, _ in self.ctas):
            self.f.add(self.path, self.ctas[0][1], "vague-cta",
                       ", ".join(sorted({t for t, _ in self.ctas})))
        for css, line in self.css:
            lint_css(css, self.path, self.f, line)


def lint_file(path, f, seen):
    real = os.path.realpath(path)
    if real in seen:
        return
    seen.add(real)
    try:
        text = open(path, encoding="utf-8", errors="replace").read()
    except OSError as e:
        print(f"skip {path}: {e}", file=sys.stderr)
        return
    if path.lower().endswith(".css"):
        lint_css(text, path, f)
        return
    p = Page(path, f)
    p.feed(text)
    p.close()
    p.finish()
    for href in p.links:
        if re.match(r"^[a-z]+:|^//", href):
            continue  # remote: never fetched
        css_path = os.path.normpath(os.path.join(os.path.dirname(path), href.split("?")[0].lstrip("/")))
        if os.path.isfile(css_path):
            lint_file(css_path, f, seen)


def walk(paths):
    for p in paths:
        if os.path.isfile(p):
            yield p
            continue
        for root, dirs, files in os.walk(p):
            dirs[:] = [d for d in dirs if d not in {"node_modules", ".git", ".next"}]
            for name in sorted(files):
                if name.lower().endswith((".html", ".htm", ".css")):
                    yield os.path.join(root, name)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if "--rules" in argv:
        for k, (sev, tell, note) in RULES.items():
            print(f"{k}: [{sev}] {note} -- {tell}")
        return 0
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--only", default="")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    only = {r for r in a.only.split(",") if r}
    if only - set(RULES):
        print("unknown rule(s): " + ", ".join(sorted(only - set(RULES))), file=sys.stderr)
        return 2
    f, seen = Finder(), set()
    for path in walk(a.paths):
        lint_file(path, f, seen)
    found = [x for x in f.found if not only or x["rule"] in only]
    found.sort(key=lambda x: (x["file"], x["line"]))
    if a.json:
        print(json.dumps(found, indent=2))
    else:
        for x in found:
            print(f"{x['file']}:{x['line']} {x['rule']} [{x['severity']}]: {x['note']}")
        print(f"{len(found)} finding(s)" if found else "no findings")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
