#!/usr/bin/env python3
"""Check an HTML slide deck for the problems that make slides hard to follow.

Each <section> is one slide (or each element with class "slide" if there are
none). Text inside <aside class="notes"> is speaker notes and is not counted.
Standard library only; reads local files and never fetches anything.

Usage: deck_check.py DECK.html [--max-slides N] [--only RULE,...] [--json] [--rules]
Exit: 0 no findings, 1 findings, 2 bad arguments or unreadable file.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser

RULES = {
    "no-headline": ("high", "slide has no h1 or h2; every slide states its point in a headline"),
    "two-headlines": ("medium", "more than one h1 or h2 on a slide; one slide, one message"),
    "topic-headline": ("medium", "headline is a topic label; write the slide's conclusion as a sentence"),
    "long-headline": ("low", "headline over 15 words; shorten it or split the slide"),
    "too-many-words": ("medium", "too much text for a presented slide; move it to the speaker notes"),
    "too-many-bullets": ("medium", "more than five bullets; cut, or use another slide or layout"),
    "nested-bullets": ("medium", "bullets inside bullets; make the sub-points a slide of their own"),
    "big-table": ("medium", "table too big to read from a seat; keep to 6 rows and 5 columns"),
    "img-no-alt": ("medium", "image without alt text"),
    "small-text": ("medium", "font size below 24px at 1920x1080 outside the notes"),
    "no-notes": ("low", "no speaker notes anywhere in the deck"),
    "too-many-slides": ("low", "more slides than the limit for this kind of deck"),
}

WORD_LIMIT = 45      # body words per slide, headline excluded
HEADLINE_LIMIT = 15
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


class Slide:
    def __init__(self, line: int):
        self.line = line
        self.headlines: list[str] = []
        self.body_words = 0
        self.li = 0
        self.nested = False
        self.tables: list[list[int]] = []
        self.img_no_alt: list[int] = []
        self.has_notes = False


class DeckParser(HTMLParser):
    def __init__(self, slide_tag: str | None):
        super().__init__(convert_charrefs=True)
        self.slide_tag = slide_tag      # "section" or None meaning class="slide"
        self.slides: list[Slide] = []
        self.styles: list[tuple[int, str]] = []
        self.stack: list[tuple[str, bool]] = []   # (tag, opens a slide)
        self.cur: Slide | None = None
        self.in_head = 0
        self.head_buf = ""
        self.in_notes = 0
        self.in_style = False
        self.style_line = 0
        self.ul_depth = 0
        self.in_script = False

    def _is_slide(self, tag, attrs):
        if self.slide_tag:
            return tag == self.slide_tag
        return "slide" in (dict(attrs).get("class") or "").split()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        line = self.getpos()[0]
        if tag == "style":
            self.in_style, self.style_line = True, line
        if tag == "script":
            self.in_script = True
        if "style" in a and a["style"]:
            self.styles.append((line, "x{%s}" % a["style"]))
        opens = self.cur is None and self._is_slide(tag, attrs)
        if opens:
            self.cur = Slide(line)
            self.slides.append(self.cur)
        if tag not in VOID:
            self.stack.append((tag, opens))
        s = self.cur
        if s is None:
            return
        if tag == "aside" and "notes" in (a.get("class") or "").split():
            self.in_notes += 1
            s.has_notes = True
        if self.in_notes:
            return
        if tag in ("h1", "h2"):
            self.in_head += 1
            self.head_buf = ""
        elif tag in ("ul", "ol"):
            if self.ul_depth:
                s.nested = True
            self.ul_depth += 1
        elif tag == "li":
            if self.ul_depth == 1:
                s.li += 1
        elif tag == "table":
            s.tables.append([0, 0])
        elif tag == "tr" and s.tables:
            s.tables[-1][0] += 1
        elif tag in ("td", "th") and s.tables:
            t = s.tables[-1]
            if t[0] == 1:
                t[1] += int(a.get("colspan") or 1) if str(a.get("colspan") or "1").isdigit() else 1
        elif tag == "img" and "alt" not in a:
            s.img_no_alt.append(line)

    def handle_endtag(self, tag):
        if tag == "style":
            self.in_style = False
        if tag == "script":
            self.in_script = False
        s = self.cur
        if s is not None and not self.in_notes:
            if tag in ("h1", "h2") and self.in_head:
                self.in_head -= 1
                s.headlines.append(" ".join(self.head_buf.split()))
            elif tag in ("ul", "ol") and self.ul_depth:
                self.ul_depth -= 1
        if s is not None and tag == "aside" and self.in_notes:
            self.in_notes -= 1
        while self.stack:
            t, opens = self.stack.pop()
            if opens:
                self.cur = None
                self.ul_depth = 0
            if t == tag:
                break

    def handle_data(self, data):
        if self.in_style:
            self.styles.append((self.style_line, data))
            return
        if self.in_script or self.cur is None or self.in_notes:
            return
        if self.in_head:
            self.head_buf += data
        else:
            self.cur.body_words += len(re.findall(r"[\w$%€£][\w'’.,%$-]*", data))


def small_text(styles):
    out = []
    for base, css in styles:
        css_nc = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
        for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", css_nc):
            sel = " ".join(m.group(1).split())
            if "notes" in sel or sel.startswith("@") or "print" in sel:
                continue
            for fm in re.finditer(r"font(?:-size)?\s*:\s*([^;]+)", m.group(2)):
                val = fm.group(1)
                size = None
                px = re.search(r"(?<![\w.])(\d+(?:\.\d+)?)px", val)
                rem = re.search(r"(?<![\w.])(\d*\.?\d+)r?em\b", val)
                if px:
                    size = float(px.group(1))
                elif rem:
                    size = float(rem.group(1)) * 16
                if size is not None and size < 24:
                    line = base + css_nc[:m.start()].count("\n")
                    out.append((line, f"{sel}: {val.strip()}"))
    return out


def check(path, text, max_slides):
    tag = "section" if re.search(r"<section\b", text, re.I) else None
    p = DeckParser(tag)
    p.feed(text)
    p.close()
    found = []

    def add(line, rule, note=""):
        found.append({"file": path, "line": line, "rule": rule, "severity": RULES[rule][0],
                      "message": RULES[rule][1], "detail": note})

    for i, s in enumerate(p.slides, start=1):
        if not s.headlines:
            add(s.line, "no-headline", f"slide {i}")
        if len(s.headlines) > 1:
            add(s.line, "two-headlines", f"slide {i}: {len(s.headlines)}")
        for h in s.headlines[:1]:
            n = len(h.split())
            if 1 < i < len(p.slides) and n <= 2:
                add(s.line, "topic-headline", f"slide {i}: {h!r}")
            if n > HEADLINE_LIMIT:
                add(s.line, "long-headline", f"slide {i}: {n} words")
        if s.body_words > WORD_LIMIT:
            add(s.line, "too-many-words", f"slide {i}: {s.body_words} words")
        if s.li > 5:
            add(s.line, "too-many-bullets", f"slide {i}: {s.li}")
        if s.nested:
            add(s.line, "nested-bullets", f"slide {i}")
        for rows, cols in s.tables:
            if rows > 7 or cols > 5:
                add(s.line, "big-table", f"slide {i}: {rows} rows, {cols} columns")
        for line in s.img_no_alt:
            add(line, "img-no-alt", f"slide {i}")
    for line, note in small_text(p.styles):
        add(line, "small-text", note)
    if p.slides and not any(s.has_notes for s in p.slides):
        add(1, "no-notes", f"{len(p.slides)} slides")
    if len(p.slides) > max_slides:
        add(1, "too-many-slides", f"{len(p.slides)} slides, limit {max_slides}")
    return p.slides, found


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check an HTML slide deck.")
    ap.add_argument("deck", nargs="?")
    ap.add_argument("--max-slides", type=int, default=20)
    ap.add_argument("--only", default="")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--rules", action="store_true")
    a = ap.parse_args(argv)
    if a.rules:
        for k, (sev, msg) in RULES.items():
            print(f"{k} [{sev}]: {msg}")
        return 0
    if not a.deck:
        ap.print_usage(sys.stderr)
        return 2
    only = {r.strip() for r in a.only.split(",") if r.strip()}
    bad = only - set(RULES)
    if bad:
        print("unknown rule(s): " + ", ".join(sorted(bad)), file=sys.stderr)
        return 2
    try:
        with open(a.deck, encoding="utf-8") as fh:
            text = fh.read()
    except OSError as e:
        print(f"cannot read {a.deck}: {e}", file=sys.stderr)
        return 2
    slides, found = check(a.deck, text, a.max_slides)
    if only:
        found = [f for f in found if f["rule"] in only]
    found.sort(key=lambda f: (f["line"], f["rule"]))
    if a.json:
        print(json.dumps({"slides": len(slides), "findings": found}, indent=2))
    else:
        for f in found:
            extra = f" ({f['detail']})" if f["detail"] else ""
            print(f"{f['file']}:{f['line']} {f['rule']} [{f['severity']}]: {f['message']}{extra}")
        print(f"{len(slides)} slide(s), " + (f"{len(found)} finding(s)" if found else "no findings"))
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
