"""`ult diagram` — draw a node-and-line diagram as inline SVG from a small JSON spec.

    python3 diagram.py SPEC.json [-o OUT.svg]

The spec (craft/taste/icons-and-diagrams.md § Diagrams):

    {"layout": "hub", "size": "card", "title": "Ledgerline sends each paid invoice on",
     "core": "Ledgerline", "nodes": ["Xero", "Stripe", "Slack"], "lines": "straight", "pulse": true}

layout  hub (core with spokes), fan-in (many into the core; add "out" for a bow-tie),
        timeline (steps in turn), free ("nodes" as {"id","label","x","y"}, "edges" as [from, to]).
size    card (560 x 340, up to 8 spokes and 12 nodes) or section (1200 x 560).
lines   straight, curve or elbow (hub and fan-in).
pulse   adds the accent pulse group; kit/diagrams/diagram.css animates it (tech pages only).
id      prefix for the SVG's ids (default "dg"); give each diagram on a page its own.

A malformed spec still draws what it can: each problem goes to stderr and the exit
code is 1. Exit 0 for a clean drawing, 2 when the spec cannot be read at all.
Standard library only, no network.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from xml.sax.saxutils import escape

SIZES = {"card": (560, 340), "section": (1200, 560)}
LIMITS = {"card": (8, 12), "section": (16, 24)}
LAYOUTS = ("hub", "fan-in", "timeline", "free")
FONT, CHAR, PAD, TALL = 13, 7.4, 14, 30   # label type size, average glyph width, side padding, box height
STEP, CYCLE = 0.32, 3.2                   # pulse ripple gap and cycle, seconds


class Drawing:
    def __init__(self, spec: dict, problems: list[str]):
        self.size = spec.get("size", "card")
        if self.size not in SIZES:
            problems.append(f"size {self.size!r} is not card or section; drawn as card")
            self.size = "card"
        self.w, self.h = SIZES[self.size]
        self.lines: list[str] = []    # path data, one per edge
        self.boxes: list[str] = []
        self.problems = problems
        self.id = str(spec.get("id") or "dg")
        if not self.id.replace("-", "").replace("_", "").isalnum():
            problems.append(f"id {self.id!r} should be letters, digits, - or _; used dg")
            self.id = "dg"

    def width(self, label: str) -> float:
        return round(len(label) * CHAR + 2 * PAD, 1)

    def box(self, x: float, y: float, label: str, core: bool = False) -> tuple[float, float]:
        """Draw a labelled box centred on (x, y); return its half width and half height."""
        w = self.width(label)
        tall = TALL + 10 if core else TALL
        fill = 'fill="var(--ink, #1c2126)"' if core else 'fill="var(--surface, #fff)" stroke="var(--line, #d9dde1)"'
        ink = "var(--bg, #fff)" if core else "var(--ink, #1c2126)"
        self.boxes.append(
            f'<g class="dg-node{" dg-core" if core else ""}">'
            f'<rect {fill} height="{tall}" rx="{tall / 4:g}" width="{w:g}" x="{x - w / 2:g}" y="{y - tall / 2:g}"/>'
            f'<text fill="{ink}" font-size="{FONT + (1 if core else 0)}" text-anchor="middle" x="{x:g}" y="{y + 4.5:g}">'
            f"{escape(label)}</text></g>")
        return w / 2, tall / 2

    def edge(self, a: tuple[float, float], b: tuple[float, float], style: str = "straight") -> None:
        (x1, y1), (x2, y2) = a, b
        if style == "curve":
            mx = (x1 + x2) / 2
            self.lines.append(f"M{x1:g} {y1:g}C{mx:g} {y1:g} {mx:g} {y2:g} {x2:g} {y2:g}")
        elif style == "elbow":
            mx, r = (x1 + x2) / 2, min(10.0, abs(y2 - y1) / 2, abs(x2 - x1) / 2)
            if r < 1:
                self.lines.append(f"M{x1:g} {y1:g}L{x2:g} {y2:g}")
                return
            sy, sx = (1 if y2 > y1 else -1), (1 if x2 > x1 else -1)
            self.lines.append(f"M{x1:g} {y1:g}H{mx - sx * r:g}Q{mx:g} {y1:g} {mx:g} {y1 + sy * r:g}"
                              f"V{y2 - sy * r:g}Q{mx:g} {y2:g} {mx + sx * r:g} {y2:g}H{x2:g}")
        else:
            self.lines.append(f"M{x1:g} {y1:g}L{x2:g} {y2:g}")

    def svg(self, title: str, pulse: bool) -> str:
        lines = "".join(f'<path d="{d}" id="{self.id}-e{i}"/>' for i, d in enumerate(self.lines))
        runs = ""
        if pulse and self.lines:
            gap = min(STEP, (CYCLE * 0.6) / max(1, len(self.lines)))
            runs = ('<g class="dg-pulse" fill="none">' + "".join(
                f'<use href="#{self.id}-e{i}" style="--d:{i * gap:.2f}s"/>' for i in range(len(self.lines))) + "</g>")
        return (f'<svg class="dg" role="img" aria-labelledby="{self.id}-title" viewBox="0 0 {self.w} {self.h}" '
                f'xmlns="http://www.w3.org/2000/svg">\n<title id="{self.id}-title">{escape(title)}</title>\n'
                f'<g class="dg-lines" fill="none" stroke="currentColor" stroke-opacity=".3" stroke-width="1">{lines}</g>\n'
                f"{runs}\n" + "\n".join(self.boxes) + "\n</svg>\n")


def _labels(spec: dict, key: str, cap: int, problems: list[str]) -> list[str]:
    raw = spec.get(key, [])
    if not isinstance(raw, list):
        problems.append(f"{key!r} should be a list of labels")
        return []
    labels = [str(x.get("label", "") if isinstance(x, dict) else x).strip() for x in raw]
    if "" in labels:
        problems.append(f"{key!r} has an empty label; skipped")
        labels = [x for x in labels if x]
    if len(labels) > cap:
        problems.append(f"{len(labels)} {key} is more than {cap}: use a list instead; drew the first {cap}")
        labels = labels[:cap]
    return labels


def _hub(d: Drawing, spec: dict) -> None:
    spokes, _ = LIMITS[d.size]
    nodes = _labels(spec, "nodes", spokes, d.problems)
    cx, cy = d.w / 2, d.h / 2
    rx, ry = d.w / 2 - 90, d.h / 2 - 40
    style = spec.get("lines", "straight")
    cw, ch = d.box(cx, cy, spec.get("core") or "Core", core=True)
    for i, label in enumerate(nodes):
        angle = -math.pi / 2 + 2 * math.pi * i / max(1, len(nodes))
        x, y = cx + rx * math.cos(angle), cy + ry * math.sin(angle)
        d.box(x, y, label)
        # leave the core's edge, not its centre: clip the ray to the core box
        dx, dy = x - cx, y - cy
        t = min(cw / abs(dx) if dx else math.inf, ch / abs(dy) if dy else math.inf)
        d.edge((cx + dx * t, cy + dy * t), (x, y), style if style != "elbow" else "elbow")


def _fan(d: Drawing, spec: dict) -> None:
    cap = LIMITS[d.size][0]
    ins = _labels(spec, "nodes", cap, d.problems)
    outs = _labels(spec, "out", cap, d.problems)
    style = spec.get("lines", "curve")
    cx, cy = (d.w / 2, d.h / 2) if outs else (d.w * 0.68, d.h / 2)
    cw, _ = d.box(cx, cy, spec.get("core") or "Core", core=True)

    def column(labels: list[str], x: float, left: bool) -> None:
        gap = (d.h - 40) / max(1, len(labels))
        for i, label in enumerate(labels):
            y = 20 + gap * (i + 0.5)
            half, _ = d.box(x, y, label)
            if left:
                d.edge((x + half, y), (cx - cw, cy), style)
            else:
                d.edge((cx + cw, cy), (x - half, y), style)

    column(ins, d.w * 0.16, True)
    column(outs, d.w * 0.84, False)


def _timeline(d: Drawing, spec: dict) -> None:
    steps = _labels(spec, "nodes", LIMITS[d.size][1], d.problems)
    if not steps:
        return
    across = d.w - 80
    y = d.h / 2
    xs = [40 + across * (i + 0.5) / len(steps) for i in range(len(steps))]
    halves = [d.box(x, y, label)[0] for x, label in zip(xs, steps)]
    for i in range(len(steps) - 1):
        d.edge((xs[i] + halves[i], y), (xs[i + 1] - halves[i + 1], y))
    if sum(h * 2 for h in halves) > across:
        d.problems.append("timeline labels are too long to sit side by side at this size")


def _free(d: Drawing, spec: dict) -> None:
    where: dict[str, tuple[float, float]] = {}
    nodes = spec.get("nodes", [])
    cap = LIMITS[d.size][1]
    if len(nodes) > cap:
        d.problems.append(f"{len(nodes)} nodes is more than {cap}; drew the first {cap}")
    for n in nodes[:cap]:
        try:
            x, y, label = float(n["x"]), float(n["y"]), str(n["label"])
        except (KeyError, TypeError, ValueError):
            d.problems.append(f"node {n!r} needs id, label, x and y; skipped")
            continue
        d.box(x, y, label, core=bool(n.get("core")))
        where[str(n.get("id", label))] = (x, y)
    for e in spec.get("edges", []):
        if not (isinstance(e, list) and len(e) == 2 and all(str(k) in where for k in e)):
            d.problems.append(f"edge {e!r} names a node that is not drawn; skipped")
            continue
        d.edge(where[str(e[0])], where[str(e[1])], spec.get("lines", "straight"))


def draw(spec: dict) -> tuple[str, list[str]]:
    """Return (svg text, problems). Never returns an empty drawing for a readable spec."""
    problems: list[str] = []
    d = Drawing(spec, problems)
    layout = spec.get("layout", "hub")
    if layout not in LAYOUTS:
        problems.append(f"layout {layout!r} is not one of {', '.join(LAYOUTS)}; drawn as hub")
        layout = "hub"
    if spec.get("lines", "straight") not in ("straight", "curve", "elbow"):
        problems.append(f"lines {spec['lines']!r} is not straight, curve or elbow; drawn straight")
        spec = {**spec, "lines": "straight"}
    title = str(spec.get("title") or "").strip()
    if not title:
        problems.append("no title: screen readers need one sentence saying what the diagram shows")
        title = spec.get("core") or "Diagram"
    {"hub": _hub, "fan-in": _fan, "timeline": _timeline, "free": _free}[layout](d, spec)
    if not d.boxes:
        problems.append("nothing to draw; drew the core alone")
        d.box(d.w / 2, d.h / 2, spec.get("core") or title, core=True)
    return d.svg(title, bool(spec.get("pulse"))), problems


def cmd_diagram(args) -> int:
    try:
        spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
        if not isinstance(spec, dict):
            raise ValueError("the spec must be a JSON object")
    except (OSError, ValueError) as err:
        print(f"diagram: cannot read {args.spec}: {err}", file=sys.stderr)
        return 2
    svg, problems = draw(spec)
    if args.out:
        Path(args.out).write_text(svg, encoding="utf-8")
    else:
        sys.stdout.write(svg)
    for p in problems:
        print(f"diagram: {p}", file=sys.stderr)
    return 1 if problems else 0


def _arguments(p: argparse.ArgumentParser) -> None:
    p.add_argument("spec", help="JSON spec file")
    p.add_argument("-o", "--out", help="write the SVG here instead of stdout")


def register(sub):
    p = sub.add_parser("diagram", help="Draw a node-and-line diagram as inline SVG from a JSON spec")
    _arguments(p)
    p.set_defaults(func=cmd_diagram)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="diagram", description=__doc__.split("\n\n")[0])
    _arguments(p)
    try:
        args = p.parse_args(argv)
    except SystemExit as exit_:
        return int(exit_.code or 0) and 2
    return cmd_diagram(args)


if __name__ == "__main__":
    sys.exit(main())
