#!/usr/bin/env python3
"""Plan a deck's slide list by type, then check a built deck against it.

The tables are deck-types.csv (length, arc and the beats each type needs, in
order, with the layouts that fit each beat) and layouts.csv (what each layout
holds, its word budget, and whether it resets attention). A built deck marks
each slide: <section class="slide" data-beat="proof" data-layout="big-number">.

Standard library only; reads local files and never fetches anything.

Usage:
  deck_plan.py types | layouts
  deck_plan.py plan TYPE [--read] [--json] [--html]
  deck_plan.py check DECK.html --type TYPE [--json]
  deck_plan.py --self-check
Exit: 0 fine, 1 findings, 2 bad arguments or unreadable file.
"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True  # keep the installed data folder clean
sys.path.insert(0, str(HERE))
import deck_check  # noqa: E402  (same folder; -I drops the script folder from the path)

RESET_GAP = 6   # longest run of slides without a reset layout

RULES = {
    "slide-count": ("medium", "outside the usual length for this deck type"),
    "unmarked": ("low", "slide has no data-beat or data-layout, so the plan check cannot place it"),
    "unknown-layout": ("medium", "data-layout is not in layouts.csv"),
    "missing-beat": ("high", "a beat this deck type needs is not on any slide"),
    "beat-order": ("medium", "beats are out of the order the arc needs"),
    "layout-fit": ("low", "layout is not one that usually carries this beat"),
    "over-budget": ("medium", "more body words than this layout holds"),
    "same-layout-run": ("medium", "three slides in a row share a layout; they blur together"),
    "no-reset": ("low", "a long run with no statement, number, image, quote or demo slide"),
    "ask-not-last": ("medium", "the ask is not the last slide before the appendix"),
    "agenda-early": ("low", "slide 2 is an agenda; spend it on the problem"),
}


def _rows(name):
    with open(HERE / name, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def load():
    layouts = {r["layout"]: r for r in _rows("layouts.csv")}
    types = {}
    for r in _rows("deck-types.csv"):
        beats = []
        for part in r["beats"].split(";"):
            beat, _, fits = part.strip().partition(":")
            beats.append((beat.strip(), [f.strip() for f in fits.split("|") if f.strip()]))
        types[r["type"]] = dict(r, min=int(r["min"]), max=int(r["max"]), beats=beats)
    return types, layouts


def plan(kind, types, layouts, read_ahead=False):
    t = types[kind]
    slides = []
    for n, (beat, fits) in enumerate(t["beats"], start=1):
        lay = layouts[fits[0]]
        budget = int(lay["max_words"])
        if read_ahead and fits[0] not in ("title", "statement"):
            budget = min(budget + 20, 90)
        slides.append({"n": n, "beat": beat, "layout": fits[0], "other_layouts": fits[1:],
                       "holds": lay["the_one_thing"], "max_words": budget})
    return {"type": kind, "label": t["label"], "arc": t["arc"], "slides_min": t["min"],
            "slides_max": t["max"], "read_ahead": read_ahead,
            "read_ahead_note": t["read_ahead"] if read_ahead else "", "slides": slides}


def plan_text(p):
    out = [f"{p['label']}: {p['arc']}, {p['slides_min']}–{p['slides_max']} slides "
           f"({len(p['slides'])} beats below; add slides inside a beat, not new beats).", ""]
    out.append("| # | Beat | Layout | Holds | Words | Headline (a sentence) | Note |")
    out.append("|---|---|---|---|---|---|---|")
    for s in p["slides"]:
        alt = f" (or {', '.join(s['other_layouts'])})" if s["other_layouts"] else ""
        out.append(f"| {s['n']} | {s['beat']} | {s['layout']}{alt} | {s['holds']} | ≤{s['max_words']} | | |")
    if p["read_ahead"]:
        out += ["", p["read_ahead_note"]]
    out += ["", "Fill the last two columns, read the headlines alone in order, and agree the list before design."]
    return "\n".join(out)


def plan_html(p):
    out = []
    for s in p["slides"]:
        out.append(f'<section class="slide" data-beat="{s["beat"]}" data-layout="{s["layout"]}">\n'
                   f'  <h2>TODO: the {s["beat"]} slide as one sentence</h2>\n'
                   f'  <!-- holds: {s["holds"]}; at most {s["max_words"]} words -->\n'
                   f'  <aside class="notes">TODO</aside>\n</section>')
    return "\n\n".join(out)


def check(path, text, kind, types, layouts):
    tag = "section" if re.search(r"<section\b", text, re.I) else None
    parser = deck_check.DeckParser(tag)
    parser.feed(text)
    parser.close()
    slides = parser.slides
    t = types[kind]
    found = []

    def add(line, rule, note=""):
        found.append({"file": path, "line": line, "rule": rule, "severity": RULES[rule][0],
                      "message": RULES[rule][1], "detail": note})

    n = len(slides)
    if not t["min"] <= n <= t["max"]:
        add(1, "slide-count", f"{n} slides; {t['label']}: {t['min']}–{t['max']}")
    if slides and not any(s.beat or s.layout for s in slides):
        add(1, "unmarked", f"no slide has data-beat or data-layout; mark them as `deck_plan.py plan {kind} --html` does")
        return n, found
    main = [s for s in slides if s.layout != "appendix" and s.beat != "appendix"]
    for i, s in enumerate(slides, start=1):
        if not s.beat or not s.layout:
            add(s.line, "unmarked", f"slide {i}")
        if s.layout and s.layout not in layouts:
            add(s.line, "unknown-layout", f"slide {i}: {s.layout!r}")
        elif s.layout:
            budget = int(layouts[s.layout]["max_words"])
            if s.body_words > budget:
                add(s.line, "over-budget", f"slide {i}: {s.body_words} words in a {s.layout} (≤{budget})")
    fits = dict(t["beats"])
    first = {}
    for i, s in enumerate(main, start=1):
        if s.beat in fits:
            first.setdefault(s.beat, (i, s))
            if s.layout in layouts and s.layout not in fits[s.beat]:
                add(s.line, "layout-fit", f"{s.beat} on a {s.layout}; usually {', '.join(fits[s.beat])}")
    last_pos = 0
    for beat, _ in t["beats"]:
        if beat not in first:
            add(1, "missing-beat", beat)
            continue
        pos, s = first[beat]
        if pos < last_pos:
            add(s.line, "beat-order", f"{beat} comes before a beat the arc puts first")
        last_pos = max(last_pos, pos)
    run = 1
    for a, b in zip(main, main[1:]):
        run = run + 1 if a.layout and a.layout == b.layout else 1
        if run == 3:
            add(b.line, "same-layout-run", f"{b.layout} x3")
    gap = 0
    for s in main:
        resets = s.layout in layouts and layouts[s.layout]["reset"] == "yes"
        gap = 0 if resets or s.layout == "title" else gap + 1
        if gap == RESET_GAP + 1:
            add(s.line, "no-reset", f"{RESET_GAP + 1} slides without one")
    asks = [i for i, s in enumerate(main) if s.layout == "ask" or s.beat in ("ask", "next-step")]
    if asks and asks[-1] != len(main) - 1:
        add(main[asks[-1]].line, "ask-not-last", f"slide {asks[-1] + 1} of {len(main)}")
    if len(main) >= 2 and main[1].layout == "agenda" and t["max"] <= 20:
        add(main[1].line, "agenda-early")
    found.sort(key=lambda f: (f["line"], f["rule"]))
    return n, found


def self_check(types, layouts):
    problems = []
    for kind, t in types.items():
        if not 1 <= t["min"] <= t["max"]:
            problems.append(f"{kind}: bad length")
        if len(t["beats"]) > t["max"]:
            problems.append(f"{kind}: more beats than slides")
        for beat, fits in t["beats"]:
            for f in fits:
                if f not in layouts:
                    problems.append(f"{kind}/{beat}: unknown layout {f}")
        if t["beats"][0][1] != ["title"]:
            problems.append(f"{kind}: first beat is not a title")
    for name, lay in layouts.items():
        if lay["reset"] not in ("yes", "no") or not lay["max_words"].isdigit():
            problems.append(f"layout {name}: bad row")
    # a planned deck built straight from the plan must pass its own check
    for kind in types:
        html = plan_html(plan(kind, types, layouts)).replace("TODO", "Done")
        _, found = check("plan", html, kind, types, layouts)
        bad = [f["rule"] for f in found if f["rule"] not in ("slide-count",)]
        if bad:
            problems.append(f"{kind}: own plan fails {bad}")
    return problems


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    try:
        types, layouts = load()
    except (OSError, KeyError, ValueError) as e:
        print(f"cannot read the tables: {e}", file=sys.stderr)
        return 2
    as_json = "--json" in argv
    argv = [a for a in argv if a != "--json"]
    if argv == ["--self-check"]:
        problems = self_check(types, layouts)
        for p in problems:
            print(p)
        print("self-check " + ("ok" if not problems else f"failed: {len(problems)}"))
        return 1 if problems else 0
    if argv == ["types"]:
        for k, t in types.items():
            print(f"{k}: {t['label']}, {t['min']}–{t['max']} slides, {t['arc']}")
        return 0
    if argv == ["layouts"]:
        for k, lay in layouts.items():
            print(f"{k}: {lay['use_for']}; holds {lay['the_one_thing']}; ≤{lay['max_words']} words")
        return 0
    if argv and argv[0] == "plan" and len(argv) >= 2:
        kind, flags = argv[1], set(argv[2:])
        if kind not in types or flags - {"--read", "--html"}:
            print(f"usage: deck_plan.py plan TYPE [--read] [--json] [--html]; types: {', '.join(types)}",
                  file=sys.stderr)
            return 2
        p = plan(kind, types, layouts, "--read" in flags)
        print(json.dumps(p, indent=2, ensure_ascii=False) if as_json
              else plan_html(p) if "--html" in flags else plan_text(p))
        return 0
    if argv and argv[0] == "check" and len(argv) == 4 and argv[2] == "--type":
        deck, kind = argv[1], argv[3]
        if kind not in types:
            print(f"unknown deck type {kind!r}; one of: {', '.join(types)}", file=sys.stderr)
            return 2
        try:
            text = Path(deck).read_text(encoding="utf-8")
        except OSError as e:
            print(f"cannot read {deck}: {e}", file=sys.stderr)
            return 2
        n, found = check(deck, text, kind, types, layouts)
        if as_json:
            print(json.dumps({"slides": n, "type": kind, "findings": found}, indent=2))
        else:
            for f in found:
                extra = f" ({f['detail']})" if f["detail"] else ""
                print(f"{f['file']}:{f['line']} {f['rule']} [{f['severity']}]: {f['message']}{extra}")
            print(f"{n} slide(s), " + (f"{len(found)} finding(s)" if found else "no findings"))
        return 1 if found else 0
    print(__doc__.split("Usage:")[1].split("Exit:")[0].rstrip(), file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
