#!/usr/bin/env python3
"""Audit an isometric figure's scene for drawing faults before it ships.

The scene is a JSON file that the figure is drawn from (build the geometry
once, draw it, and audit the same data). Parts are axis-aligned boxes in world
units (turned and round parts are checked by their box); pipes are polylines
with a radius that run between named ports, and a "coil" pipe is first turned
into points by `figure_draw.py` beside this file. The
checks match the audit table in `skills/website/references/craft/anatomy/verify.md`.
Standard library only; reads one local file and never fetches anything.

Usage: figure_audit.py SCENE.json [--only CHECK,...] [--json] [--checks]
Exit: 0 every count is zero, 1 faults found, 2 bad arguments or a bad scene.
"""
from __future__ import annotations

import argparse
import json
import math
import sys

CHECKS = {
    "clearance": "a pipe passes nearer than 1.5 radii to a part it should miss",
    "terminals": "a pipe end is not on the port it names",
    "loose-ends": "a pipe has no port at one end, or names a port that does not exist",
    "folds": "a pipe bends back on itself (a turn of more than 135 degrees)",
    "overlaps": "two parts share volume without being listed as joined",
    "crowding": "two parts are closer than the readable gap but not touching",
    "stand-ins": "a placeholder part is still in the scene",
    "wobble": "a part marked fixed moves between frames",
    "seats": "a part does not rest on the part it says holds it",
    "depth-order": "a nearer part is drawn before a farther one it covers on screen",
}
TOL = 1e-6


def box(p):
    x, y, z = p["at"]
    w, d, h = p["size"]
    return (x, y, z, x + w, y + d, z + h)


def overlap_1d(a0, a1, b0, b1):
    return min(a1, b1) - max(a0, b0)


def box_gap(a, b):
    """Distance between two boxes; 0 when touching, negative depth when they overlap."""
    o = [overlap_1d(a[i], a[i + 3], b[i], b[i + 3]) for i in range(3)]
    if all(v > TOL for v in o):
        return -min(o)
    out = [max(0.0, -v) for v in o]
    return math.sqrt(sum(v * v for v in out))


def seg_box_dist(p, q, b, steps=64):
    best = math.inf
    for i in range(steps + 1):
        t = i / steps
        pt = [p[k] + (q[k] - p[k]) * t for k in range(3)]
        d = [max(b[k] - pt[k], 0.0, pt[k] - b[k + 3]) for k in range(3)]
        best = min(best, math.sqrt(sum(v * v for v in d)))
    return best


def project(pt, az=math.radians(45), el=math.radians(30)):
    x, y, z = pt
    u = (x - y) * math.cos(az)
    d = (x + y) * math.sin(az)
    return u, d * math.sin(el) - z * math.cos(el)


def screen_rect(b):
    pts = [project((x, y, z)) for x in (b[0], b[3]) for y in (b[1], b[4]) for z in (b[2], b[5])]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


def nearer(a, b):
    """Return 1 if box a is nearer the camera than b, -1 if farther, 0 if unknown.

    The camera looks from +x, +y and above, so a box wholly past another on one
    of those axes is in front of it.
    """
    for i in range(3):
        if a[i] >= b[i + 3] - TOL:
            return 1
        if b[i] >= a[i + 3] - TOL:
            return -1
    return 0


def audit(scene):
    faults = []

    def add(check, what, detail=""):
        faults.append({"check": check, "what": what, "detail": detail})

    parts = {p["name"]: p for p in scene.get("parts", [])}
    boxes = {n: box(p) for n, p in parts.items()}
    joined = {frozenset(j) for j in scene.get("joins", [])}
    gap = float(scene.get("min_gap", 0.5))

    for n, p in parts.items():
        if p.get("stand_in"):
            add("stand-ins", n)
        on = p.get("on")
        if on:
            if on not in boxes:
                add("seats", n, f"rests on unknown part {on}")
            else:
                a, b = boxes[n], boxes[on]
                plan = overlap_1d(a[0], a[3], b[0], b[3]) > TOL and overlap_1d(a[1], a[4], b[1], b[4]) > TOL
                if abs(a[2] - b[5]) > TOL or not plan:
                    add("seats", n, f"bottom at {a[2]:g}, top of {on} at {b[5]:g}" if plan else f"not over {on} in plan")

    names = sorted(boxes)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            g = box_gap(boxes[a], boxes[b])
            pair = frozenset((a, b))
            if g < -TOL and pair not in joined:
                add("overlaps", f"{a} / {b}", f"{-g:g} deep")
            elif TOL < g < gap and pair not in joined:
                add("crowding", f"{a} / {b}", f"gap {g:g} under {gap:g}")

    ports = {}
    for n, p in parts.items():
        for port, at in p.get("ports", {}).items():
            ports[f"{n}.{port}"] = at
    for pipe in scene.get("pipes", []):
        name, pts, r = pipe["name"], pipe["points"], float(pipe.get("radius", 0.2))
        ends = (pipe.get("from"), pts[0]), (pipe.get("to"), pts[-1])
        for port, pt in ends:
            if not port or port not in ports:
                add("loose-ends", name, f"port {port or 'missing'}")
            elif math.dist(ports[port], pt) > max(r, TOL):
                add("terminals", name, f"end {pt} is not on {port} {ports[port]}")
        for k in range(1, len(pts) - 1):
            v1 = [pts[k][j] - pts[k - 1][j] for j in range(3)]
            v2 = [pts[k + 1][j] - pts[k][j] for j in range(3)]
            n1, n2 = math.hypot(*v1), math.hypot(*v2)
            if n1 > TOL and n2 > TOL:
                cos = sum(v1[j] * v2[j] for j in range(3)) / (n1 * n2)
                if cos < math.cos(math.radians(135)):
                    add("folds", name, f"at point {k}")
        allowed = {p.split(".")[0] for p in (pipe.get("from"), pipe.get("to")) if p}
        allowed |= set(pipe.get("passes", []))
        for part, b in boxes.items():
            if part in allowed:
                continue
            d = min(seg_box_dist(pts[k], pts[k + 1], b) for k in range(len(pts) - 1))
            if d < 1.5 * r:
                add("clearance", f"{name} / {part}", f"{d:.3g} under {1.5 * r:g}")

    fixed = {n for n, p in parts.items() if p.get("fixed")}
    for f_i, frame in enumerate(scene.get("frames", [])):
        for n, at in frame.items():
            if n in fixed and math.dist(at, parts[n]["at"]) > TOL:
                add("wobble", n, f"frame {f_i}")

    order = scene.get("order")
    if order:
        missing = [n for n in names if n not in order]
        if missing:
            add("depth-order", ", ".join(missing), "not in the draw order")
        pos = {n: i for i, n in enumerate(order)}
        rects = {n: screen_rect(b) for n, b in boxes.items()}
        for i, a in enumerate(names):
            for b in names[i + 1:]:
                if a not in pos or b not in pos or frozenset((a, b)) in joined:
                    continue
                ra, rb = rects[a], rects[b]
                if min(ra[2], rb[2]) - max(ra[0], rb[0]) <= TOL or min(ra[3], rb[3]) - max(ra[1], rb[1]) <= TOL:
                    continue
                front = nearer(boxes[a], boxes[b])
                if front == 1 and pos[a] < pos[b]:
                    add("depth-order", f"{a} / {b}", f"{a} is nearer but drawn first")
                elif front == -1 and pos[b] < pos[a]:
                    add("depth-order", f"{a} / {b}", f"{b} is nearer but drawn first")
    return faults


def with_coils(scene):
    """Turn "coil" pipes into points with the drawer's own helix (figure_draw.py beside this file)."""
    if not isinstance(scene, dict) or not any(isinstance(q, dict) and "coil" in q and "points" not in q
                                              for q in scene.get("pipes", [])):
        return scene, None
    import importlib.util
    import os
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figure_draw.py")
    spec = importlib.util.spec_from_file_location("ult_figure_draw", path)
    fd = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fd)
    for q in scene["pipes"]:
        if isinstance(q, dict) and "coil" in q and "points" not in q:
            err = fd.check_coil(q)
            if err:
                return scene, f"pipe {q.get('name')}: {err}"
    return dict(scene, pipes=fd.expand_pipes(scene)), None


def validate(scene):
    if not isinstance(scene, dict) or not isinstance(scene.get("parts"), list):
        return "scene needs a list of parts"
    seen = set()
    for p in scene["parts"]:
        if not isinstance(p, dict) or "name" not in p or len(p.get("at", [])) != 3 or len(p.get("size", [])) != 3:
            return "each part needs a name, at [x, y, z] and size [w, d, h]"
        if p["name"] in seen:
            return f"duplicate part name {p['name']}"
        seen.add(p["name"])
    for pipe in scene.get("pipes", []):
        if "name" not in pipe or len(pipe.get("points", [])) < 2 or any(len(pt) != 3 for pt in pipe["points"]):
            return "each pipe needs a name and two or more [x, y, z] points"
    return None


def main(argv=None):
    ap = argparse.ArgumentParser(description="Audit an isometric figure scene.")
    ap.add_argument("scene", nargs="?")
    ap.add_argument("--only", default="")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--checks", action="store_true")
    a = ap.parse_args(argv)
    if a.checks:
        for k, msg in CHECKS.items():
            print(f"{k}: {msg}")
        return 0
    if not a.scene:
        ap.print_usage(sys.stderr)
        return 2
    only = {c.strip() for c in a.only.split(",") if c.strip()}
    if only - set(CHECKS):
        print("unknown check(s): " + ", ".join(sorted(only - set(CHECKS))), file=sys.stderr)
        return 2
    try:
        with open(a.scene, encoding="utf-8") as fh:
            scene = json.load(fh)
    except (OSError, ValueError) as e:
        print(f"cannot read {a.scene}: {e}", file=sys.stderr)
        return 2
    scene, err = with_coils(scene)
    err = err or validate(scene)
    if err:
        print(f"bad scene: {err}", file=sys.stderr)
        return 2
    faults = audit(scene)
    if only:
        faults = [f for f in faults if f["check"] in only]
    counts = {k: sum(f["check"] == k for f in faults) for k in CHECKS if not only or k in only}
    if a.json:
        print(json.dumps({"counts": counts, "faults": faults}, indent=2))
    else:
        for k, n in counts.items():
            print(f"{k:12} {n}")
        for f in faults:
            extra = f" ({f['detail']})" if f["detail"] else ""
            print(f"  {f['check']}: {f['what']}{extra}")
    return 1 if faults else 0


if __name__ == "__main__":
    sys.exit(main())
