#!/usr/bin/env python3
"""Draw an isometric figure from its JSON scene, and audit parts that move.

The scene is the same file `figure_audit.py` reads: parts are boxes (or
upright cylinders with "shape": "cylinder", or turned shapes with
"shape": "lathe" and a "profile" of [radius, height] points) in world
units, pipes are polylines with a radius, or springs and heater coils
given as "coil" instead of points. This script adds two things:

  draw   writes an SVG: visible faces only, four tones from one light,
         depth order settled by separating planes, pipes, and labels with
         leader lines. Any camera azimuth and elevation, any group pose.
  turn   samples every moving group through its range (and, with --orbit,
         the camera round a full circle) and reports collisions, crowding,
         draw-order cycles, pipes torn off a moving port, and fixed parts
         placed in a group.

Groups live in the scene under "groups":
  {"name": "lid", "kind": "hinge", "parts": ["lid"], "axis": [1, 0, 0],
   "pivot": [0, 4, 3], "range": [0, 70]}
kind is turn or hinge (degrees about axis through pivot) or slide (world
units along axis). A pipe that rides with a group names it in "group"; a
flexible hose sets "flex": true and is only checked for stretch.

Standard library only; reads one local file, writes one, fetches nothing.

Usage:
  figure_draw.py draw SCENE.json --out FIG.svg [--az 45] [--el 30]
                 [--pose GROUP=VALUE ...] [--size 640x480] [--title TEXT]
  figure_draw.py turn SCENE.json [--steps 24] [--orbit] [--json]
  figure_draw.py --self-check
Exit: 0 clean, 1 faults found, 2 bad arguments or a bad scene.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

TOL = 1e-6
TURN_CHECKS = {
    "collision": "a moving part passes through a part it is not joined to",
    "crowding": "a moving part comes closer than min_gap to a part it is not joined to",
    "order-cycle": "no draw order works at some pose or camera; split a part",
    "tether": "a pipe end leaves its port when the group moves, or a hose stretches",
    "fixed-in-group": "a part marked fixed is listed in a moving group",
}


# ---------------------------------------------------------------- vectors

def sub(a, b):
    return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]


def add(a, b):
    return [a[0] + b[0], a[1] + b[1], a[2] + b[2]]


def mul(a, k):
    return [a[0] * k, a[1] * k, a[2] * k]


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]


def unit(a):
    n = math.sqrt(dot(a, a))
    return [a[0] / n, a[1] / n, a[2] / n] if n > TOL else None


def rotate(p, pivot, axis, deg):
    """Rodrigues rotation of p about the line through pivot along axis."""
    k = unit(axis)
    v = sub(p, pivot)
    t = math.radians(deg)
    c, s = math.cos(t), math.sin(t)
    r = add(add(mul(v, c), mul(cross(k, v), s)), mul(k, dot(k, v) * (1 - c)))
    return add(r, pivot)


# ---------------------------------------------------------------- solids

class Solid:
    """A convex polyhedron: vertices and faces (index lists, outward order)."""

    def __init__(self, name, verts, faces, color, kind="part", part=None, hidden=(), marks=()):
        self.name, self.verts, self.faces, self.color, self.kind = name, verts, faces, color, kind
        self.part = part or name  # the scene part this piece belongs to (a lathe has several)
        self.hidden = frozenset(hidden)  # faces never painted: joins inside one turned part
        self.marks = list(marks)  # (kind, start, end, start + outward normal): knurl and ticks

    def moved(self, fn):
        marks = [(k, fn(a), fn(b), fn(t)) for k, a, b, t in self.marks]
        return Solid(self.name, [fn(v) for v in self.verts], self.faces, self.color, self.kind,
                     self.part, self.hidden, marks)

    def normal(self, f):
        a, b, c = (self.verts[i] for i in self.faces[f][:3])
        return unit(cross(sub(b, a), sub(c, a))) or [0.0, 0.0, 1.0]

    def centre(self):
        n = len(self.verts)
        return [sum(v[i] for v in self.verts) / n for i in range(3)]

    def edges(self):
        out = []
        for f in self.faces:
            for i in range(len(f)):
                d = unit(sub(self.verts[f[(i + 1) % len(f)]], self.verts[f[i]]))
                if d and not any(abs(abs(dot(d, e)) - 1) < 1e-9 for e in out):
                    out.append(d)
        return out


def box_solid(name, at, size, color):
    x, y, z = at
    w, d, h = size
    v = [[x + w * i, y + d * j, z + h * k] for k in (0, 1) for j in (0, 1) for i in (0, 1)]
    # 0..3 bottom (z), 4..7 top; index = i + 2j + 4k
    faces = [[0, 2, 3, 1], [4, 5, 7, 6], [0, 1, 5, 4], [2, 6, 7, 3], [0, 4, 6, 2], [1, 3, 7, 5]]
    return Solid(name, v, faces, color)


def cylinder_solid(name, at, size, color, sides=20):
    x, y, z = at
    w, d, h = size
    cx, cy, rx, ry = x + w / 2, y + d / 2, w / 2, d / 2
    ring = [(cx + rx * math.cos(2 * math.pi * i / sides), cy + ry * math.sin(2 * math.pi * i / sides))
            for i in range(sides)]
    v = [[px, py, z] for px, py in ring] + [[px, py, z + h] for px, py in ring]
    faces = [list(range(sides - 1, -1, -1)), list(range(sides, 2 * sides))]
    faces += [[i, (i + 1) % sides, sides + (i + 1) % sides, sides + i] for i in range(sides)]
    return Solid(name, v, faces, color)


def lathe_solids(name, at, size, color, profile, sides=20):
    """A turned part: the profile revolved round the upright centre line of its box.

    Each pair of profile points with a rise becomes one frustum, which is convex, so
    depth order and the separating-axis checks stay exact. A pair at the same height
    is a step (a shoulder or a lip): the cap of the frustum below or above shows it.
    """
    x, y, z = at
    w, d, _ = size
    cx, cy = x + w / 2, y + d / 2
    rings = [(math.cos(2 * math.pi * i / sides), math.sin(2 * math.pi * i / sides)) for i in range(sides)]
    pts = [(float(r), float(h)) for r, h in profile]
    out = []
    spans = [k for k in range(len(pts) - 1) if pts[k + 1][1] > pts[k][1] + TOL]
    for n, k in enumerate(spans):
        (r0, z0), (r1, z1) = pts[k], pts[k + 1]
        v = [[cx + r0 * c, cy + r0 * s_, z + z0] for c, s_ in rings] + \
            [[cx + r1 * c, cy + r1 * s_, z + z1] for c, s_ in rings]
        faces = [list(range(sides - 1, -1, -1)), list(range(sides, 2 * sides))]
        faces += [[i, (i + 1) % sides, sides + (i + 1) % sides, sides + i] for i in range(sides)]
        hidden = set()
        if n > 0 and spans[n - 1] == k - 1:
            hidden.add(0)  # the piece below meets this one at the same ring
        if n + 1 < len(spans) and spans[n + 1] == k + 1:
            hidden.add(1)
        out.append(Solid(name if n == 0 else f"{name}#{n}", v, faces, color, part=name, hidden=hidden))
    return out


def coil_points(coil):
    """Points along a helix round an upright axis: {"at": [x, y, z] (centre of the
    bottom), "radius": R, "pitch": rise per turn, "turns": N, "start": degrees,
    "steps": points per turn (default 16)}."""
    cx, cy, cz = (float(v) for v in coil["at"])
    rad, pitch, turns = float(coil["radius"]), float(coil["pitch"]), float(coil["turns"])
    steps = int(coil.get("steps", 16))
    a0 = math.radians(float(coil.get("start", 0)))
    n = max(2, round(turns * steps))
    out = []
    for i in range(n + 1):
        t = turns * i / n
        a = a0 + 2 * math.pi * t
        out.append([cx + rad * math.cos(a), cy + rad * math.sin(a), cz + pitch * t])
    return out


def expand_pipes(scene):
    """The scene's pipes with every coil turned into its points (the scene is not changed)."""
    out = []
    for pipe in scene.get("pipes", []):
        if "coil" in pipe and "points" not in pipe:
            pipe = dict(pipe, points=coil_points(pipe["coil"]))
        out.append(pipe)
    return out


def check_lathe(p):
    prof = p.get("profile")
    w, d, h = (float(v) for v in p["size"])
    if not isinstance(prof, list) or len(prof) < 2 or any(not isinstance(q, list) or len(q) != 2 for q in prof):
        return "a lathe needs a profile of two or more [radius, height] points"
    try:
        pts = [(float(r), float(z)) for r, z in prof]
    except (TypeError, ValueError):
        return "profile values must be numbers"
    if any(r <= 0 for r, _ in pts):
        return "profile radii must be above zero (use a small radius for a point)"
    if any(b[1] < a[1] for a, b in zip(pts, pts[1:])):
        return "profile heights must not go down"
    if pts[0][1] < -TOL or pts[-1][1] > h + TOL:
        return f"profile heights must lie within 0 and the part's height {h:g}"
    if max(r for r, _ in pts) > min(w, d) / 2 + TOL:
        return f"profile radius {max(r for r, _ in pts):g} is wider than the part's box allows ({min(w, d) / 2:g})"
    if pts[-1][1] - pts[0][1] <= TOL:
        return "the profile must rise"
    return None


def check_coil(pipe):
    c = pipe["coil"]
    if not isinstance(c, dict) or len(c.get("at", [])) != 3:
        return "a coil needs at [x, y, z]"
    try:
        rad, pitch, turns = float(c["radius"]), float(c["pitch"]), float(c["turns"])
        steps = int(c.get("steps", 16))
    except (KeyError, TypeError, ValueError):
        return "a coil needs number radius, pitch and turns"
    wire = float(pipe.get("radius", 0.2))
    if rad <= wire or turns <= 0 or not 6 <= steps <= 64:
        return "a coil needs radius above the wire's, turns above zero and steps 6 to 64"
    if pitch <= 2 * wire:
        return f"pitch {pitch:g} lets the turns touch; it must be more than the wire's thickness {2 * wire:g}"
    return None


def cylinder_marks(at, size, knurl=0, ticks=0):
    """Knurl ridges up the side and tick marks round the top rim of an upright cylinder."""
    x, y, z = at
    w, d, h = size
    cx, cy, rx, ry = x + w / 2, y + d / 2, w / 2, d / 2
    out = []
    for i in range(int(knurl)):
        a = 2 * math.pi * (i + 0.5) / knurl
        c, s_ = math.cos(a), math.sin(a)
        foot = [cx + rx * c, cy + ry * s_, z + 0.15 * h]
        out.append(("knurl", foot, [foot[0], foot[1], z + 0.85 * h], add(foot, [c, s_, 0])))
    for i in range(int(ticks)):
        a = 2 * math.pi * i / ticks
        c, s_ = math.cos(a), math.sin(a)
        inner = [cx + 0.72 * rx * c, cy + 0.72 * ry * s_, z + h]
        out.append(("tick", inner, [cx + 0.92 * rx * c, cy + 0.92 * ry * s_, z + h], add(inner, [0, 0, 1])))
    return out


def segment_solid(name, p, q, r, color):
    """A square prism round a pipe segment, used to order the pipe, not to paint it."""
    d = unit(sub(q, p)) or [1.0, 0.0, 0.0]
    a = unit(cross(d, [0, 0, 1])) or unit(cross(d, [0, 1, 0]))
    b = cross(d, a)
    corners = [add(mul(a, sa * r), mul(b, sb * r)) for sa, sb in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    v = [add(p, c) for c in corners] + [add(q, c) for c in corners]
    faces = [[3, 2, 1, 0], [4, 5, 6, 7]] + [[i, (i + 1) % 4, 4 + (i + 1) % 4, 4 + i] for i in range(4)]
    return Solid(name, v, faces, color, kind="pipe")


# ---------------------------------------------------------------- scene

def validate(scene):
    if not isinstance(scene, dict) or not isinstance(scene.get("parts"), list) or not scene["parts"]:
        return "scene needs a list of parts"
    names = set()
    for p in scene["parts"]:
        if not isinstance(p, dict) or "name" not in p or len(p.get("at", [])) != 3 or len(p.get("size", [])) != 3:
            return "each part needs a name, at [x, y, z] and size [w, d, h]"
        if p["name"] in names:
            return f"duplicate part name {p['name']}"
        if p.get("shape", "box") not in ("box", "cylinder", "lathe"):
            return f"part {p['name']}: shape must be box, cylinder or lathe"
        if p.get("shape") == "lathe":
            err = check_lathe(p)
            if err:
                return f"part {p['name']}: {err}"
        for mark, lo in (("knurl", 6), ("ticks", 4)):
            if mark in p:
                if p.get("shape") != "cylinder":
                    return f"part {p['name']}: {mark} needs a cylinder"
                if not isinstance(p[mark], int) or isinstance(p[mark], bool) or not lo <= p[mark] <= 120:
                    return f"part {p['name']}: {mark} must be a whole number from {lo} to 120"
        names.add(p["name"])
    for pipe in scene.get("pipes", []):
        if isinstance(pipe, dict) and "coil" in pipe and "points" not in pipe:
            err = check_coil(pipe)
            if err:
                return f"pipe {pipe.get('name')}: {err}"
            continue
        if "name" not in pipe or len(pipe.get("points", [])) < 2 or any(len(pt) != 3 for pt in pipe["points"]):
            return "each pipe needs a name and two or more [x, y, z] points, or a coil"
    for g in scene.get("groups", []):
        if g.get("kind") not in ("turn", "hinge", "slide"):
            return f"group {g.get('name')}: kind must be turn, hinge or slide"
        if not g.get("parts") or any(n not in names for n in g["parts"]):
            return f"group {g.get('name')}: parts must name existing parts"
        if len(g.get("axis", [])) != 3 or not unit(g["axis"]):
            return f"group {g.get('name')}: axis must be a non-zero [x, y, z]"
        rng = g.get("range", [])
        if len(rng) != 2 or rng[0] > rng[1]:
            return f"group {g.get('name')}: range must be [low, high]"
        if g["kind"] != "slide" and len(g.get("pivot", [])) != 3:
            return f"group {g.get('name')}: a turn or hinge needs a pivot"
    return None


def mover(group, value):
    if group["kind"] == "slide":
        step = mul(unit(group["axis"]), value)
        return lambda v: add(v, step)
    return lambda v: rotate(v, group["pivot"], group["axis"], value)


def posed(scene, pose):
    """Solids and pipe polylines with each group at the value in pose (default: low end)."""
    moves = {}
    for g in scene.get("groups", []):
        fn = mover(g, pose.get(g["name"], g["range"][0]))
        for n in g["parts"]:
            moves[n] = fn
        moves["group:" + g["name"]] = fn
    solids = []
    for p in scene["parts"]:
        color = p.get("color", "#8c9bab")
        if p.get("shape") == "lathe":
            pieces = lathe_solids(p["name"], p["at"], p["size"], color, p["profile"])
        elif p.get("shape") == "cylinder":
            pieces = [cylinder_solid(p["name"], p["at"], p["size"], color)]
            pieces[0].marks = cylinder_marks(p["at"], p["size"], p.get("knurl", 0), p.get("ticks", 0))
        else:
            pieces = [box_solid(p["name"], p["at"], p["size"], color)]
        fn = moves.get(p["name"])
        solids += [s.moved(fn) for s in pieces] if fn else pieces
    pipes = []
    for pipe in expand_pipes(scene):
        fn = moves.get("group:" + pipe.get("group", ""))
        pts = [fn(pt) for pt in pipe["points"]] if fn else [list(pt) for pt in pipe["points"]]
        pipes.append((pipe, pts))
    ports = {}
    for p in scene["parts"]:
        for port, at in p.get("ports", {}).items():
            ports[f"{p['name']}.{port}"] = moves[p["name"]](at) if p["name"] in moves else at
    return solids, pipes, ports


# ---------------------------------------------------------------- camera

class Camera:
    def __init__(self, az=45.0, el=30.0):
        a, e = math.radians(az), math.radians(el)
        h = [math.sin(a), math.cos(a), 0.0]
        self.right = [math.cos(a), -math.sin(a), 0.0]
        self.down = [h[0] * math.sin(e), h[1] * math.sin(e), -math.cos(e)]
        self.toward = [h[0] * math.cos(e), h[1] * math.cos(e), math.sin(e)]  # toward the viewer

    def screen(self, p):
        return dot(p, self.right), dot(p, self.down)


def interval(solid, axis):
    vals = [dot(v, axis) for v in solid.verts]
    return min(vals), max(vals)


def separation(a, b):
    """Largest gap between a and b along any separating axis, and that axis.

    Face normals of both and cross products of their edge directions cover
    every separating plane of two convex solids. Negative means they overlap
    by at least that much on every axis (they intersect)."""
    axes = [a.normal(i) for i in range(len(a.faces))] + [b.normal(i) for i in range(len(b.faces))]
    for ea in a.edges():
        for eb in b.edges():
            c = unit(cross(ea, eb))
            if c:
                axes.append(c)
    best, best_axis = -math.inf, None
    for ax in axes:
        a0, a1 = interval(a, ax)
        b0, b1 = interval(b, ax)
        gap = max(b0 - a1, a0 - b1)
        if gap > best:
            best, best_axis = gap, (ax if b0 - a1 >= a0 - b1 else mul(ax, -1))
    return best, best_axis  # axis points from a toward b


def hull(points):
    pts = sorted(set((round(x, 9), round(y, 9)) for x, y in points))
    if len(pts) < 3:
        return pts

    def turn(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and turn(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and turn(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def screen_overlap(ha, hb):
    """True when two convex screen hulls share area (touching edges do not count)."""
    for h in (ha, hb):
        for i in range(len(h)):
            p, q = h[i], h[(i + 1) % len(h)]
            nx, ny = q[1] - p[1], p[0] - q[0]
            if abs(nx) + abs(ny) < TOL:
                continue
            pa = [nx * x + ny * y for x, y in ha]
            pb = [nx * x + ny * y for x, y in hb]
            if max(pa) <= min(pb) + 1e-7 * (abs(nx) + abs(ny)) or max(pb) <= min(pa) + 1e-7 * (abs(nx) + abs(ny)):
                return False
    return len(ha) >= 3 and len(hb) >= 3


def draw_order(solids, cam):
    """Far to near. Returns (order, cycles) where cycles lists pairs left to the fallback."""
    hulls = [hull([cam.screen(v) for v in s.verts]) for s in solids]
    depth = [dot(s.centre(), cam.toward) for s in solids]
    after = {i: set() for i in range(len(solids))}  # j in after[i]: draw i before j
    for i in range(len(solids)):
        for j in range(i + 1, len(solids)):
            if not screen_overlap(hulls[i], hulls[j]):
                continue
            gap, axis = separation(solids[i], solids[j])
            if gap < -1e-6 or axis is None:
                continue  # they intersect; nothing exact to say, fall back to depth
            facing = dot(axis, cam.toward)
            if facing > 1e-9:
                after[i].add(j)  # j lies beyond i toward the viewer
            elif facing < -1e-9:
                after[j].add(i)
    indeg = {i: 0 for i in after}
    for i in after:
        for j in after[i]:
            indeg[j] += 1
    order, cycles = [], []
    left = set(after)
    while left:
        ready = [i for i in left if indeg[i] == 0]
        if not ready:
            pick = min(left, key=lambda k: depth[k])
            cycles.append(solids[pick].name)
        else:
            pick = min(ready, key=lambda k: depth[k])
        left.discard(pick)
        order.append(pick)
        for j in after[pick]:
            indeg[j] -= 1
    return order, cycles


# ---------------------------------------------------------------- painting

def shade(hexcolor, k):
    h = hexcolor.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    rgb = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
    out = [round(c + (255 - c) * k) if k > 0 else round(c * (1 + k)) for c in rgb]
    return "#" + "".join(f"{max(0, min(255, c)):02x}" for c in out)


LIGHT = unit([-0.35, 0.45, 0.82])  # one light for every part: high, from the left


def tones(color):
    return {"lit": shade(color, 0.35), "mid": color, "dark": shade(color, -0.35), "edge": shade(color, -0.6)}


def face_tone(n):
    lam = dot(n, LIGHT)
    return "lit" if lam > 0.6 else "mid" if lam > 0.15 else "dark"


def draw(scene, pose=None, az=45.0, el=30.0, size=(640, 480), title=None):
    pose = pose or {}
    cam = Camera(az, el)
    solids, pipes, _ = posed(scene, pose)
    order_solids = list(solids)
    pipe_of = {}
    for pipe, pts in pipes:
        r = float(pipe.get("radius", 0.2))
        for k in range(len(pts) - 1):
            seg = segment_solid(f"{pipe['name']}#{k}", pts[k], pts[k + 1], r, pipe.get("color", "#5f6b78"))
            pipe_of[len(order_solids)] = (pipe, pts[k], pts[k + 1], r)
            order_solids.append(seg)
    order, cycles = draw_order(order_solids, cam)

    every = [cam.screen(v) for s in order_solids for v in s.verts]
    xs, ys = [p[0] for p in every], [p[1] for p in every]
    labels = [p for p in scene["parts"] if p.get("label")]
    W, H = size
    room = 0.28 * W if labels else 0.0
    span_x, span_y = max(xs) - min(xs) or 1, max(ys) - min(ys) or 1
    s = min((W - room) * 0.75 / span_x, H * 0.65 / span_y)  # about 60 percent of the card
    ox = (W - room) / 2 - s * (min(xs) + max(xs)) / 2
    oy = H / 2 - s * (min(ys) + max(ys)) / 2

    def to_px(p):
        u, v = cam.screen(p)
        return ox + s * u, oy + s * v

    curved = {p["name"]: p.get("shape") in ("cylinder", "lathe") for p in scene["parts"]}
    title = title or scene.get("title", "Isometric figure")
    names = ", ".join(p["name"] for p in scene["parts"])
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" '
           f'aria-labelledby="fig-title fig-desc">',
           f'<title id="fig-title">{escape(title)}</title>',
           f'<desc id="fig-desc">{escape(scene.get("description", "Parts: " + names + "."))}</desc>']
    for idx in order:
        sol = order_solids[idx]
        if idx in pipe_of:
            pipe, p, q, r = pipe_of[idx]
            (x1, y1), (x2, y2) = to_px(p), to_px(q)
            t = tones(pipe.get("color", "#5f6b78"))
            out.append(f'<g data-pipe="{escape(pipe["name"])}">'
                       f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{t["edge"]}" '
                       f'stroke-width="{2 * r * s + 2:.2f}" stroke-linecap="round"/>'
                       f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{t["mid"]}" '
                       f'stroke-width="{2 * r * s:.2f}" stroke-linecap="round"/></g>')
            continue
        t = tones(sol.color)
        faces = []
        for f in range(len(sol.faces)):
            n = sol.normal(f)
            if f in sol.hidden or dot(n, cam.toward) <= 1e-9:
                continue
            pts = " ".join(f"{x:.2f},{y:.2f}" for x, y in (to_px(sol.verts[i]) for i in sol.faces[f]))
            fill = t[face_tone(n)]
            seam = curved.get(sol.part, False) and len(sol.faces[f]) == 4  # a cylinder's side strip: no seam line
            faces.append(f'<polygon points="{pts}" fill="{fill}" stroke="{fill if seam else t["edge"]}" '
                         f'stroke-width="{0.6 if seam else 1}" stroke-linejoin="round"/>')
        for kind, a, b, tip in sol.marks:
            if dot(sub(tip, a), cam.toward) <= 0.05:
                continue  # on the far side, or edge-on
            (x1, y1), (x2, y2) = to_px(a), to_px(b)
            faces.append(f'<line data-mark="{kind}" x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
                         f'stroke="{t["edge"]}" stroke-width="1" stroke-linecap="round"/>')
        piece = f' data-piece="{escape(sol.name)}"' if sol.name != sol.part else ""
        out.append(f'<g data-part="{escape(sol.part)}"{piece}>' + "".join(faces) + "</g>")

    if labels:
        anchors = []
        for p in labels:
            pieces = [s for s in solids if s.part == p["name"]]
            covered = any(q.get("on") == p["name"] for q in scene["parts"])
            best, best_area = None, -1.0
            for sol in pieces:
                for f in range(len(sol.faces)):
                    n = sol.normal(f)
                    if f in sol.hidden or dot(n, cam.toward) <= 1e-9 or (covered and n[2] > 0.9):
                        continue  # hidden, or a top another part sits on
                    pts = [to_px(sol.verts[i]) for i in sol.faces[f]]
                    area = abs(sum(pts[i][0] * pts[i - 1][1] - pts[i - 1][0] * pts[i][1]
                                   for i in range(len(pts)))) / 2
                    if area > best_area:
                        best_area, best = area, pts
            spot = (sum(x for x, _ in best) / len(best), sum(y for _, y in best) / len(best)) if best else \
                to_px(pieces[0].centre())
            anchors.append((spot[1], spot, p))
        anchors.sort(key=lambda a: a[0])
        col = W - room + 12
        gap = 18
        y_prev = -math.inf
        for _, (ax, ay), p in anchors:
            ly = max(ay, y_prev + gap, 16)
            y_prev = ly
            out.append(f'<g data-label="{escape(p["name"])}"><polyline points="{ax:.2f},{ay:.2f} {col - 6:.2f},{ly:.2f}" '
                       f'fill="none" stroke="#5b6470" stroke-width="1"/><circle cx="{ax:.2f}" cy="{ay:.2f}" r="2.5" '
                       f'fill="#5b6470"/><text x="{col:.2f}" y="{ly + 4:.2f}" font-family="system-ui, sans-serif" '
                       f'font-size="13" fill="#2b3038">{escape(p["label"])}</text></g>')
    out.append("</svg>")
    return "\n".join(out), cycles


# ---------------------------------------------------------------- turn audit

def samples(lo, hi, steps):
    return [lo + (hi - lo) * i / steps for i in range(steps + 1)] if hi > lo else [lo]


def turn_audit(scene, steps=24, orbit=False):
    faults = []
    seen = set()

    def note(check, what, detail):
        if (check, what) not in seen:
            seen.add((check, what))
            faults.append({"check": check, "what": what, "detail": detail})

    parts = {p["name"]: p for p in scene["parts"]}
    joined = {frozenset(j) for j in scene.get("joins", [])}
    gap_min = float(scene.get("min_gap", 0.5))
    groups = scene.get("groups", [])
    for g in groups:
        for n in g["parts"]:
            if parts[n].get("fixed"):
                note("fixed-in-group", n, f"in group {g['name']}")

    rest_solids, rest_pipes, rest_ports = posed(scene, {})
    for g in groups:
        moving = set(g["parts"])
        for value in samples(g["range"][0], g["range"][1], steps):
            solids, pipes, ports = posed(scene, {g["name"]: value})
            for ms in (s for s in solids if s.part in moving):
                for os_ in solids:
                    m, other = ms.part, os_.part
                    if other in moving or frozenset((m, other)) in joined:
                        continue
                    sep, _ = separation(ms, os_)
                    pair = " / ".join(sorted((m, other)))
                    if sep < -1e-6:
                        note("collision", pair, f"{g['name']} at {value:g}")
                    elif 1e-6 < sep < gap_min:
                        note("crowding", pair, f"gap {sep:.3g} under {gap_min:g} with {g['name']} at {value:g}")
            for pipe, pts in pipes:
                r = float(pipe.get("radius", 0.2))
                ends = ((pipe.get("from"), pts[0]), (pipe.get("to"), pts[-1]))
                if pipe.get("flex"):
                    a, b = pipe.get("from"), pipe.get("to")
                    if a in ports and b in ports:
                        length = sum(math.dist(pts[k], pts[k + 1]) for k in range(len(pts) - 1))
                        if math.dist(ports[a], ports[b]) > length + TOL:
                            note("tether", pipe["name"], f"stretched with {g['name']} at {value:g}")
                    continue
                for port, end in ends:
                    if port in ports and math.dist(ports[port], end) > max(r, TOL):
                        note("tether", pipe["name"], f"leaves {port} with {g['name']} at {value:g}")
            if not orbit:
                _, cycles = draw_order(solids, Camera())
                if cycles:
                    note("order-cycle", ", ".join(cycles), f"{g['name']} at {value:g}")

    if orbit:
        cam_cfg = scene.get("camera", {})
        els = cam_cfg.get("el", [30, 30])
        poses = [{}] + [{g["name"]: g["range"][1]} for g in groups]
        for pose in poses:
            solids, _, _ = posed(scene, pose)
            for el in sorted(set(els)):
                for i in range(steps):
                    az = 360.0 * i / steps
                    _, cycles = draw_order(solids, Camera(az, el))
                    if cycles:
                        where = ", ".join(f"{k} at {v:g}" for k, v in pose.items()) or "rest"
                        note("order-cycle", ", ".join(cycles), f"camera az {az:g} el {el:g}, {where}")
    return faults


# ---------------------------------------------------------------- self-check

def demo_scene():
    return {
        "title": "Test box with a hinged lid and a dial",
        "min_gap": 0.3,
        "parts": [
            {"name": "body", "at": [0, 0, 0], "size": [6, 4, 3], "fixed": True, "label": "Body",
             "ports": {"side": [6, 2, 1.5]}},
            {"name": "lid", "at": [0, 0, 3], "size": [6, 4, 0.4], "on": "body", "label": "Lid", "color": "#b08d57"},
            {"name": "dial", "at": [7, 1.5, 0], "size": [1.6, 1.6, 0.8], "shape": "cylinder", "label": "Dial",
             "ports": {"in": [7, 2.3, 0.4]}},
            {"name": "post", "at": [2.5, -1.6, 0], "size": [1, 1, 5.5], "fixed": True},
        ],
        "joins": [["body", "lid"]],
        "pipes": [{"name": "lead", "from": "body.side", "to": "dial.in", "radius": 0.12,
                   "points": [[6, 2, 1.5], [6.5, 2, 1.5], [6.5, 2.3, 0.4], [7, 2.3, 0.4]]}],
        "groups": [
            {"name": "lid-hinge", "kind": "hinge", "parts": ["lid"], "axis": [1, 0, 0],
             "pivot": [0, 0, 3], "range": [0, 100]},
            {"name": "dial-turn", "kind": "turn", "parts": ["dial"], "axis": [0, 0, 1],
             "pivot": [7.8, 2.3, 0], "range": [0, 360]},
        ],
    }


def turned_scene():
    """A kettle: a turned body with a shoulder, a heater coil, and a lid arm that swings."""
    return {
        "title": "Kettle with a turned body and a heater coil",
        "min_gap": 0.2,
        "parts": [
            {"name": "base", "at": [-1, -1, 0], "size": [8, 8, 0.5], "fixed": True},
            {"name": "body", "at": [0, 0, 0.5], "size": [6, 6, 6], "shape": "lathe", "label": "Body",
             "profile": [[2.4, 0], [3, 1], [3, 4], [2.2, 5], [1.2, 5], [1.2, 6]], "color": "#a7b4c2"},
            {"name": "arm", "at": [3.5, 2.6, 6.2], "size": [4, 0.8, 0.4], "label": "Arm", "color": "#b08d57"},
            {"name": "knob", "at": [-0.5, 5.6, 0.5], "size": [1.2, 1.2, 0.8], "shape": "cylinder",
             "knurl": 24, "ticks": 12, "color": "#5f6b78"},
        ],
        "joins": [["base", "body"]],
        "pipes": [{"name": "heater", "radius": 0.12, "passes": ["body"], "color": "#c0623f",
                   "coil": {"at": [3, 3, 1.5], "radius": 3.4, "pitch": 0.6, "turns": 3}}],
        "groups": [{"name": "arm-swing", "kind": "hinge", "parts": ["arm"], "axis": [0, 1, 0],
                    "pivot": [7.5, 3, 6.2], "range": [0, 60]},
                   {"name": "knob-turn", "kind": "turn", "parts": ["knob"], "axis": [0, 0, 1],
                    "pivot": [0.1, 6.2, 0.5], "range": [0, 270]}],
    }


def turned_check():
    problems = []
    sc = turned_scene()
    if validate(sc):
        return ["turned scene invalid: " + validate(sc)]
    solids, pipes, _ = posed(sc, {})
    body = [s for s in solids if s.part == "body"]
    if len(body) != 4:
        problems.append(f"the body profile has four rises and should make four pieces, got {len(body)}")
    pts = pipes[0][1]
    if len(pts) != 49 or abs(pts[-1][2] - (1.5 + 0.6 * 3)) > TOL or abs(math.dist(pts[0][:2], [3, 3]) - 3.4) > TOL:
        problems.append("the coil should have 3 x 16 steps, rise pitch x turns and keep its radius")
    svg, cycles = draw(sc)
    root = ET.fromstring(svg)
    ns = "{http://www.w3.org/2000/svg}"
    parts = [g.get("data-part") for g in root.iter(ns + "g") if g.get("data-part")]
    if parts.count("body") != 4 or len([g for g in root.iter(ns + "g") if g.get("data-pipe") == "heater"]) != 48:
        problems.append("the drawing should hold four body pieces and 48 heater segments")
    if len([g for g in root.iter(ns + "g") if g.get("data-label")]) != 2:
        problems.append("expected two labels on the kettle")
    knob = next(g for g in root.iter(ns + "g") if g.get("data-part") == "knob")
    knurl = [ln for ln in knob if ln.get("data-mark") == "knurl"]
    ticks = [ln for ln in knob if ln.get("data-mark") == "tick"]
    if not 8 <= len(knurl) <= 14 or len(ticks) != 12:
        problems.append(f"the knob should show about half its 24 ridges and all 12 ticks, got {len(knurl)} and {len(ticks)}")
    turned = ET.fromstring(draw(sc, {"knob-turn": 15})[0])
    knob2 = next(g for g in turned.iter(ns + "g") if g.get("data-part") == "knob")
    first = [(ln.get("x1"), ln.get("y1")) for ln in ticks]
    if first == [(ln.get("x1"), ln.get("y1")) for ln in knob2 if ln.get("data-mark") == "tick"]:
        problems.append("ticks should turn with the knob")
    if cycles:
        problems.append(f"unexpected order cycle on the kettle {cycles}")
    faults = {(f["check"], f["what"]) for f in turn_audit(sc, steps=12)}
    if ("collision", "arm / body") not in faults:
        problems.append("the arm cutting into the turned body was not found")
    sc["groups"][0]["range"] = [0, 10]
    sc["parts"][2]["at"] = [3.5, 2.6, 7]
    if any(c in ("collision", "crowding") for c, _ in {(f["check"], f["what"]) for f in turn_audit(sc, steps=12)}):
        problems.append("a short swing clear of the body should be clean")
    bad = [
        ({"profile": [[2, 0], [4, 3]]}, "wider than"),
        ({"profile": [[2, 2], [2, 1]]}, "must not go down"),
        ({"profile": [[0, 0], [2, 3]]}, "above zero"),
        ({"profile": [[2, 1]]}, "two or more"),
    ]
    for change, words in bad:
        b = turned_scene()
        b["parts"][1].update(change)
        if words not in (validate(b) or ""):
            problems.append(f"a bad profile {change} should be refused with '{words}'")
    flat = turned_scene()
    flat["parts"][2]["knurl"] = 12
    if "needs a cylinder" not in (validate(flat) or ""):
        problems.append("knurl on a box should be refused")
    tight = turned_scene()
    tight["pipes"][0]["coil"]["pitch"] = 0.2
    if "turns touch" not in (validate(tight) or ""):
        problems.append("a coil whose turns touch should be refused")
    return problems


def self_check():
    problems = turned_check()
    sc = demo_scene()
    if validate(sc):
        problems.append("demo scene invalid: " + validate(sc))
    svg, cycles = draw(sc)
    try:
        root = ET.fromstring(svg)
    except ET.ParseError as e:
        problems.append(f"svg does not parse: {e}")
        root = None
    if root is not None:
        ns = "{http://www.w3.org/2000/svg}"
        groups = {g.get("data-part"): g for g in root.iter(ns + "g") if g.get("data-part")}
        if len(groups.get("body", [])) != 3:
            problems.append("a box at the default camera should show three faces")
        if not root.find(ns + "title").text:
            problems.append("svg has no title")
        if len([g for g in root.iter(ns + "g") if g.get("data-label")]) != 3:
            problems.append("expected three labels")
        order = [g.get("data-part") for g in root.iter(ns + "g") if g.get("data-part")]
        if order.index("body") > order.index("lid"):
            problems.append("lid on top of the body must draw after it")
    if cycles:
        problems.append(f"unexpected order cycle {cycles}")
    # back faces at the opposite camera
    svg_b, _ = draw(sc, az=225)
    rb = ET.fromstring(svg_b)
    for g in rb.iter("{http://www.w3.org/2000/svg}g"):
        if g.get("data-part") == "body" and len(g) != 3:
            problems.append("the far side should also show three faces")
    faults = turn_audit(sc, steps=20)
    checks = {(f["check"], f["what"]) for f in faults}
    if ("collision", "lid / post") not in checks:
        problems.append("the lid swinging into the post was not found")
    if not any(c == "tether" and w == "lead" for c, w in checks):
        problems.append("the lead torn off the turning dial was not found")
    sc2 = demo_scene()
    sc2["groups"][0]["range"] = [0, 40]
    sc2["pipes"][0]["flex"] = True
    sc2["pipes"][0]["points"] = [[6, 2, 1.5], [6.6, 2, 3], [7.6, 2.6, 2], [7, 2.3, 0.4]]
    sc2["parts"][3]["at"] = [2.5, -3.5, 0]
    left = [f for f in turn_audit(sc2, steps=20) if f["check"] in ("collision", "tether")]
    if left:
        problems.append(f"fixed scene still has faults: {left}")
    stuck = demo_scene()
    stuck["parts"][1]["fixed"] = True
    if not any(f["check"] == "fixed-in-group" for f in turn_audit(stuck, steps=4)):
        problems.append("a fixed part in a group was not reported")
    for p in problems:
        print("FAIL " + p)
    print(f"self-check: {len(problems)} problem(s)")
    return 1 if problems else 0


# ---------------------------------------------------------------- command line

def load(path):
    try:
        with open(path, encoding="utf-8") as fh:
            scene = json.load(fh)
    except (OSError, ValueError) as e:
        print(f"cannot read {path}: {e}", file=sys.stderr)
        return None
    err = validate(scene)
    if err:
        print(f"bad scene: {err}", file=sys.stderr)
        return None
    return scene


def main(argv=None):
    ap = argparse.ArgumentParser(description="Draw an isometric scene and audit its moving groups.")
    ap.add_argument("--self-check", action="store_true")
    sub_p = ap.add_subparsers(dest="cmd")
    d = sub_p.add_parser("draw")
    d.add_argument("scene")
    d.add_argument("--out", required=True)
    d.add_argument("--az", type=float, default=45.0)
    d.add_argument("--el", type=float, default=30.0)
    d.add_argument("--pose", action="append", default=[])
    d.add_argument("--size", default="640x480")
    d.add_argument("--title")
    t = sub_p.add_parser("turn")
    t.add_argument("scene")
    t.add_argument("--steps", type=int, default=24)
    t.add_argument("--orbit", action="store_true")
    t.add_argument("--json", action="store_true")
    sub_p.add_parser("checks")
    try:
        a = ap.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code else 0
    if a.self_check:
        return self_check()
    if a.cmd == "checks":
        for k, msg in TURN_CHECKS.items():
            print(f"{k}: {msg}")
        return 0
    if a.cmd not in ("draw", "turn"):
        ap.print_usage(sys.stderr)
        return 2
    scene = load(a.scene)
    if scene is None:
        return 2
    if a.cmd == "draw":
        if not 5 <= a.el <= 85:
            print("--el must be between 5 and 85 degrees", file=sys.stderr)
            return 2
        groups = {g["name"] for g in scene.get("groups", [])}
        pose = {}
        for item in a.pose:
            name, _, val = item.partition("=")
            try:
                pose[name] = float(val)
            except ValueError:
                print(f"bad --pose {item}; use GROUP=NUMBER", file=sys.stderr)
                return 2
            if name not in groups:
                print(f"unknown group {name}", file=sys.stderr)
                return 2
        try:
            w, h = (int(v) for v in a.size.lower().split("x"))
        except ValueError:
            print("bad --size; use WIDTHxHEIGHT", file=sys.stderr)
            return 2
        svg, cycles = draw(scene, pose, a.az, a.el, (w, h), a.title)
        try:
            with open(a.out, "w", encoding="utf-8") as fh:
                fh.write(svg + "\n")
        except OSError as e:
            print(f"cannot write {a.out}: {e}", file=sys.stderr)
            return 2
        print(f"wrote {a.out}")
        if cycles:
            print("order-cycle: no exact order for " + ", ".join(cycles) + "; split one of them")
            return 1
        return 0
    if a.steps < 2:
        print("--steps must be 2 or more", file=sys.stderr)
        return 2
    faults = turn_audit(scene, a.steps, a.orbit)
    counts = {k: sum(f["check"] == k for f in faults) for k in TURN_CHECKS}
    if a.json:
        print(json.dumps({"counts": counts, "faults": faults}, indent=2))
    else:
        for k, n in counts.items():
            print(f"{k:15} {n}")
        for f in faults:
            print(f"  {f['check']}: {f['what']} ({f['detail']})")
    return 1 if faults else 0


if __name__ == "__main__":
    sys.exit(main())
