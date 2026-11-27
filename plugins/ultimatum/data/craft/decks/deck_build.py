#!/usr/bin/env python3
"""Build a finished HTML deck from a content file, then check it.

The content file is JSON: the deck type, a title, an optional theme, and one
entry per slide with its beat, layout, headline, the layout's fields and a
speaker note. The deck uses template.html's frame (fit to window, arrow keys,
print to PDF) and is checked by deck_check.py and deck_plan.py before it is
reported done. `starter TYPE` prints a content file to fill in, laid out
from the type's plan.

Standard library only; reads local files and never fetches anything. Image
paths are written as given and never loaded.

Usage:
  deck_build.py starter TYPE [--read]
  deck_build.py build CONTENT.json -o DECK.html
  deck_build.py fields
  deck_build.py --self-check
Exit: 0 built with no findings, 1 built with findings (or self-check failed),
2 bad arguments, bad content or unreadable file.
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE))
import deck_check  # noqa: E402
import deck_plan  # noqa: E402

# Which fields each layout reads. Every slide also takes headline, label and notes.
FIELDS = {
    "title": ["text"],
    "agenda": ["lines"],
    "statement": ["text"],
    "big-number": ["big", "text", "source"],
    "number-row": ["items(big, text)", "source"],
    "split": ["text", "lines", "image", "alt"],
    "full-image": ["image", "alt", "text"],
    "screenshot": ["image", "alt", "text"],
    "demo": ["text", "image", "alt"],
    "chart": ["image", "alt", "text", "source"],
    "three-ideas": ["items(head, text)"],
    "before-after": ["before(head, lines)", "after(head, lines)"],
    "timeline": ["items(head, text, now)"],
    "quote": ["quote", "who"],
    "team": ["items(head, text, image, alt)"],
    "table": ["table(head, rows, pick)", "source"],
    "ask": ["big", "lines"],
    "appendix": ["text", "lines", "table(head, rows, pick)"],
}

EXTRA_CSS = """
  .slide.statement, .slide.full-image { display: flex; flex-direction: column; justify-content: center; }
  .slide.statement h2 { font-size: 96px; max-width: 20ch; }
  .slide.full-image { padding: 0; color: #fff; justify-content: flex-end; }
  .slide.full-image img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
  .slide.full-image .over { position: relative; padding: 80px; background: linear-gradient(transparent, rgba(0,0,0,.72)); }
  .slide.full-image .over p, .slide.full-image .num { color: #fff; }
  .cols { display: grid; grid-template-columns: repeat(var(--n), 1fr); gap: 56px; }
  .cols .big { font-size: 140px; }
  .cols h3 { font: 44px/1.15 var(--display); margin-bottom: 16px; }
  .shot { max-width: 100%; max-height: 720px; border: 1px solid var(--line); border-radius: 12px; }
  .face { width: 220px; height: 220px; object-fit: cover; border-radius: 50%; margin-bottom: 20px; }
  blockquote { font: 60px/1.25 var(--display); max-width: 30ch; }
  blockquote + .label { margin-top: 32px; }
  .line { border-top: 4px solid var(--line); padding-top: 24px; }
  .line.now { border-color: var(--accent); }
  table { border-collapse: collapse; font-size: 30px; }
  th, td { text-align: left; padding: 18px 28px; border-bottom: 1px solid var(--line); }
  th { color: var(--muted); font-weight: 400; }
  .pick { background: color-mix(in srgb, var(--accent) 14%, var(--bg)); font-weight: 700; }
"""

HEX = re.compile(r"^#[0-9a-fA-F]{6}$")
FONT = re.compile(r"^[A-Za-z0-9 ,\"'-]{1,120}$")
THEME_KEYS = {"bg", "ink", "muted", "accent", "line", "display", "body"}


class ContentError(ValueError):
    pass


def esc(s):
    return html.escape(str(s), quote=True)


def _lum(hexcol):
    def ch(v):
        v = int(v, 16) / 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(hexcol[i:i + 2]) for i in (1, 3, 5))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((_lum(a), _lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def theme_css(theme):
    if not theme:
        return ""
    if not isinstance(theme, dict) or set(theme) - THEME_KEYS:
        raise ContentError(f"theme takes only {', '.join(sorted(THEME_KEYS))}")
    for k in ("bg", "ink", "muted", "accent", "line"):
        if k in theme and not HEX.match(str(theme[k])):
            raise ContentError(f"theme.{k} must be a #rrggbb colour")
    for k in ("display", "body"):
        if k in theme and not FONT.match(str(theme[k])):
            raise ContentError(f"theme.{k} must be a plain font list")
    bg = theme.get("bg", "#f6f4ef")
    for k, need in (("ink", 7.0), ("muted", 4.5), ("accent", 3.0)):
        col = theme.get(k, {"ink": "#1d1b18", "muted": "#6b665d", "accent": "#c2410c"}[k])
        if contrast(col, bg) < need:
            raise ContentError(f"theme.{k} {col} on {bg} is {contrast(col, bg):.2f}:1; needs {need}:1")
    pairs = "; ".join(f"--{k}: {theme[k]}" for k in sorted(theme))
    return f"\n  :root {{ {pairs}; }}\n"


def _lines(v, where):
    if v is None:
        return ""
    if not isinstance(v, list) or not all(isinstance(x, str) for x in v):
        raise ContentError(f"{where}: lines must be a list of strings")
    return "  <ul>\n" + "".join(f"    <li>{esc(x)}</li>\n" for x in v) + "  </ul>\n"


def _p(v, cls=""):
    if not v:
        return ""
    c = f' class="{cls}"' if cls else ""
    return f"  <p{c}>{esc(v)}</p>\n"


def _img(s, cls, where):
    if not s.get("image"):
        return ""
    if not s.get("alt"):
        raise ContentError(f"{where}: an image needs alt text (describe it, or \"\" is not allowed here)")
    if re.match(r"^\s*javascript:", str(s["image"]), re.I):
        raise ContentError(f"{where}: image must be a file path or https URL")
    c = f' class="{cls}"' if cls else ""
    return f'  <img{c} src="{esc(s["image"])}" alt="{esc(s["alt"])}">\n'


def _items(s, where, n_max, render):
    items = s.get("items")
    if not isinstance(items, list) or not 2 <= len(items) <= n_max:
        raise ContentError(f"{where}: needs items, a list of 2 to {n_max}")
    cells = "".join(render(it) for it in items)
    return f'  <div class="cols" style="--n:{len(items)}">\n{cells}  </div>\n'


def _table(t, where):
    if not isinstance(t, dict) or not isinstance(t.get("head"), list) or not isinstance(t.get("rows"), list):
        raise ContentError(f"{where}: table needs head (list) and rows (list of lists)")
    pick = t.get("pick")
    def cell(tag, i, v):
        c = ' class="pick"' if pick == i else ""
        return f"<{tag}{c}>{esc(v)}</{tag}>"
    out = "  <table>\n    <tr>" + "".join(cell("th", i, v) for i, v in enumerate(t["head"])) + "</tr>\n"
    for row in t["rows"]:
        out += "    <tr>" + "".join(cell("td", i, v) for i, v in enumerate(row)) + "</tr>\n"
    return out + "  </table>\n"


def body(s, where):
    lay = s["layout"]
    if lay in ("title", "statement"):
        return _p(s.get("text"))
    if lay == "agenda":
        return _lines(s.get("lines"), where)
    if lay in ("big-number", "ask"):
        if not s.get("big"):
            raise ContentError(f"{where}: {lay} needs big (the number or amount)")
        rest = _p(s.get("text")) + _lines(s.get("lines"), where) + _p(s.get("source"), "label")
        if lay == "ask":
            return f'  <div class="split">\n  <p class="big">{esc(s["big"])}</p>\n{rest}  </div>\n'
        return f'  <p class="big">{esc(s["big"])}</p>\n{rest}'
    if lay == "number-row":
        return _items(s, where, 4, lambda it: f'    <div><p class="big">{esc(it.get("big", ""))}</p>'
                      f'<p>{esc(it.get("text", ""))}</p></div>\n') + _p(s.get("source"), "label")
    if lay == "split":
        left = _p(s.get("text")) + _lines(s.get("lines"), where)
        return f'  <div class="split">\n  <div>\n{left}  </div>\n{_img(s, "shot", where) or "  <div></div>"}\n  </div>\n'
    if lay in ("screenshot", "demo", "chart"):
        return _img(s, "shot", where) + _p(s.get("text")) + _p(s.get("source"), "label")
    if lay == "three-ideas":
        return _items(s, where, 4, lambda it: f'    <div><h3>{esc(it.get("head", ""))}</h3>'
                      f'<p>{esc(it.get("text", ""))}</p></div>\n')
    if lay == "timeline":
        return _items(s, where, 6, lambda it: f'    <div class="line{" now" if it.get("now") else ""}">'
                      f'<h3>{esc(it.get("head", ""))}</h3><p>{esc(it.get("text", ""))}</p></div>\n')
    if lay == "team":
        return _items(s, where, 6, lambda it: "    <div>\n" + _img(it, "face", where).replace("  <img", "    <img")
                      + f'    <h3>{esc(it.get("head", ""))}</h3><p>{esc(it.get("text", ""))}</p></div>\n')
    if lay == "before-after":
        halves = []
        for key in ("before", "after"):
            h = s.get(key)
            if not isinstance(h, dict):
                raise ContentError(f"{where}: before-after needs before and after, each with head and lines")
            halves.append(f'    <div><h3>{esc(h.get("head", key.title()))}</h3>\n{_lines(h.get("lines"), where)}    </div>\n')
        return f'  <div class="cols" style="--n:2">\n{"".join(halves)}  </div>\n'
    if lay == "quote":
        if not s.get("quote") or not s.get("who"):
            raise ContentError(f"{where}: quote needs quote and who (name and role)")
        return f'  <blockquote>{esc(s["quote"])}</blockquote>\n  <p class="label">{esc(s["who"])}</p>\n'
    if lay == "table":
        return _table(s.get("table"), where) + _p(s.get("source"), "label")
    if lay == "appendix":
        return _p(s.get("text")) + _lines(s.get("lines"), where) + (_table(s["table"], where) if s.get("table") else "")
    raise ContentError(f"{where}: unknown layout {lay!r}")


def render(content, template):
    if not isinstance(content, dict) or not isinstance(content.get("slides"), list) or not content["slides"]:
        raise ContentError("content needs a non-empty slides list")
    head, sep, rest = template.partition('<main class="deck">')
    _, sep2, tail = rest.partition("</main>")
    if not sep or not sep2:
        raise ContentError("template.html is missing its <main class=\"deck\"> frame")
    head = head.replace("</style>", EXTRA_CSS + theme_css(content.get("theme")) + "</style>", 1)
    head = re.sub(r"<title>.*?</title>", f"<title>{esc(content.get('title', 'Deck'))}</title>", head, count=1)
    if content.get("lang"):
        head = head.replace('<html lang="en">', f'<html lang="{esc(content["lang"])}">', 1)
    parts = []
    for n, s in enumerate(content["slides"], start=1):
        where = f"slide {n}"
        if not isinstance(s, dict) or not s.get("layout") or not s.get("beat") or not s.get("headline"):
            raise ContentError(f"{where}: needs beat, layout and headline")
        if s["layout"] not in FIELDS:
            raise ContentError(f"{where}: unknown layout {s['layout']!r}; see `deck_build.py fields`")
        hl = "h1" if s["layout"] == "title" else "h2"
        cls = "slide " + s["layout"] if s["layout"] in ("title", "statement", "full-image") else "slide"
        label = _p(s.get("label"), "label")
        if s["layout"] == "full-image":
            inner = (_img(s, "", where) + '  <div class="over">\n' + label
                     + f"  <{hl}>{esc(s['headline'])}</{hl}>\n" + _p(s.get("text")) + "  </div>\n")
        else:
            inner = label + f"  <{hl}>{esc(s['headline'])}</{hl}>\n" + body(s, where)
        num = f'  <span class="num">{n}</span>\n' if n > 1 else ""
        notes = f'  <aside class="notes">{esc(s["notes"])}</aside>\n' if s.get("notes") else ""
        parts.append(f'<section class="{cls}" data-beat="{esc(s["beat"])}" data-layout="{esc(s["layout"])}">\n'
                     f"{inner}{num}{notes}</section>\n")
    return head + '<main class="deck">\n\n' + "\n".join(parts) + "\n</main>" + tail


def run_checks(path, text, kind):
    types, layouts = deck_plan.load()
    limits = deck_check.deck_type_limits()
    _, a = deck_check.check(path, text, limits.get(kind, 20))
    found = list(a)
    if kind in types:
        _, b = deck_plan.check(path, text, kind, types, layouts)
        found += b
    found.sort(key=lambda f: (f["line"], f["rule"]))
    return found


SAMPLE = {
    "text": "Plain words a stranger follows",
    "lines": ["First point in a few words", "Second point in a few words", "Third point in a few words"],
    "big": "42%", "source": "Source: sample figure, replace it",
    "quote": "It saved us a day a week.", "who": "A. Customer, operations lead",
    "image": "images/placeholder.jpg", "alt": "Placeholder picture, replace it",
}


def starter(kind, read_ahead=False, sample=False):
    types, layouts = deck_plan.load()
    p = deck_plan.plan(kind, types, layouts, read_ahead)
    slides = []
    for s in p["slides"]:
        lay = s["layout"]
        e = {"beat": s["beat"], "layout": lay,
             "headline": f"The {s['beat'].replace('-', ' ')} slide stated as one full sentence" if sample else "",
             "notes": "What to say here" if sample else ""}
        for f in FIELDS[lay]:
            key = f.split("(")[0]
            if key in ("items",):
                n = 3 if lay != "team" else 2
                e["items"] = [{"head": "Short head", "text": "One line", "big": "12"} for _ in range(n)] if sample \
                    else [{"head": "", "text": ""} for _ in range(3)]
            elif key in ("before", "after"):
                e[key] = {"head": key.title(), "lines": SAMPLE["lines"][:2] if sample else []}
            elif key == "table":
                if lay == "table":
                    e["table"] = {"head": ["", "Us", "Them"], "rows": [["Price", "Low", "High"]] if sample else [],
                                  "pick": 1}
            elif key in ("image", "alt") and lay not in ("full-image", "screenshot", "chart", "team"):
                continue
            elif key != "text" or lay not in ("statement",):
                e[key] = SAMPLE.get(key, "") if sample else ""
        if lay in ("statement",):
            e.pop("text", None)
        slides.append(e)
    return {"type": kind, "title": p["label"], "theme": {}, "slides": slides,
            "_how": "Fill every empty value; delete fields you do not need. `deck_build.py fields` lists what each layout reads."}


def self_check():
    template = (HERE / "template.html").read_text(encoding="utf-8")
    types, _ = deck_plan.load()
    problems = []
    for kind in types:
        content = starter(kind, sample=True)
        try:
            text = render(content, template)
        except ContentError as e:
            problems.append(f"{kind}: {e}")
            continue
        found = [f for f in run_checks(kind, text, kind) if f["rule"] != "slide-count"]
        if found:
            problems.append(f"{kind}: {[f['rule'] for f in found]}")
    for bad, why in ((({"ink": "#cccccc"}), "low ink contrast"), ({"bg": "red"}, "bad colour"),
                     ({"display": "x;}</style>"}, "unsafe font")):
        try:
            theme_css(bad)
            problems.append(f"theme {why} accepted")
        except ContentError:
            pass
    return problems


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv == ["--self-check"]:
        problems = self_check()
        for p in problems:
            print(p)
        print("self-check " + ("ok" if not problems else f"failed: {len(problems)}"))
        return 1 if problems else 0
    if argv == ["fields"]:
        for k, v in FIELDS.items():
            print(f"{k}: headline, label, notes, {', '.join(v)}")
        return 0
    if len(argv) >= 2 and argv[0] == "starter":
        types, _ = deck_plan.load()
        if argv[1] not in types or set(argv[2:]) - {"--read"}:
            print(f"usage: deck_build.py starter TYPE [--read]; types: {', '.join(types)}", file=sys.stderr)
            return 2
        print(json.dumps(starter(argv[1], "--read" in argv), indent=2, ensure_ascii=False))
        return 0
    if len(argv) == 4 and argv[0] == "build" and argv[2] == "-o":
        src, out = argv[1], argv[3]
        try:
            content = json.loads(Path(src).read_text(encoding="utf-8"))
            text = render(content, (HERE / "template.html").read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError, ContentError) as e:
            print(f"cannot build: {e}", file=sys.stderr)
            return 2
        Path(out).write_text(text, encoding="utf-8")
        found = run_checks(out, text, content.get("type", ""))
        for f in found:
            extra = f" ({f['detail']})" if f["detail"] else ""
            print(f"{f['file']}:{f['line']} {f['rule']} [{f['severity']}]: {f['message']}{extra}")
        n = len(content["slides"])
        print(f"wrote {out}: {n} slide(s), " + (f"{len(found)} finding(s); fix the content and build again"
                                                   if found else "no findings"))
        return 1 if found else 0
    print(__doc__.split("Usage:")[1].split("Exit:")[0].rstrip(), file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
