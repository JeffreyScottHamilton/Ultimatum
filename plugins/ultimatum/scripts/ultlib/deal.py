"""`ult design deal` - deal a page's look by kind and trade, so consecutive pages differ.

Deals one palette (data/craft/taste/presets/palettes.json, each checked for contrast),
one type pairing (data/design-own/typography.csv via presets/type.json), a hero, page
parts (nav, footer, close, rhythm, buttons, radius) and, for tech kinds, two section
grounds that don't clash. Picks are weighted toward the brief's words, seeded when
asked, and kept in a small history under .ultimatum/ so the next deal avoids the last
few picks. Original code; standard library only; nothing is fetched.

  ult design deal "<trade or brief>" [--kind KIND] [--mode light|dark] [--seed N]
                  [--fresh] [--no-save] [--css FILE] [--json]
"""
from __future__ import annotations

import csv
import json
import random
import re
from functools import lru_cache
from pathlib import Path

from .common import dump_json, project_root, state_dir, write_private

ROOT = Path(__file__).resolve().parents[2]
PRESETS = ROOT / "data" / "craft" / "taste" / "presets"
PATTERNS = ROOT / "data" / "craft" / "taste" / "patterns.csv"
TYPE_TABLE = ROOT / "data" / "design-own" / "typography.csv"

KINDS = ("software", "game", "product", "hardware", "service", "place")
HISTORY_FILE = "deal-history.json"
HISTORY_KEEP = 30
AVOID_LAST = 4  # a pick sits out up to this many later deals of the same kind (at least the next one)

# Words that point at a kind when --kind is not given (first match wins, in this order).
KIND_WORDS = {
    "game": "game games gaming rpg arcade indie steam console multiplayer shooter puzzle",
    "place": "cafe coffee bakery restaurant bar pub salon barber hotel shop bistro deli venue gym studio",
    "hardware": "hardware device robot robotics sensor drone battery charger machine",
    "product": "product store shop brand skincare fashion furniture bike drinks snack toy apparel",
    "service": "agency law lawyer accountant clinic dentist plumber electrician builder tutor school consulting charity",
    "software": "app saas api platform software tool dashboard ai startup developer fintech crm",
}

# Page parts by kind, from taste/page-plans.md § Deal lists (hardware shares product's).
PARTS = {
    "software": {"nav": ["mega", "cards", "centre"], "footer": ["dark", "statement", "columns"],
                 "close": ["type", "word"], "rhythm": ["dark-band", "surface-pairs", "space"],
                 "buttons": ["solid", "arrow", "block"], "radius": ["sharp", "soft"]},
    "game": {"nav": ["mega", "centre", "cards"], "footer": ["dark", "statement"],
             "close": ["word", "type"], "rhythm": ["dark-band", "media-band", "space"],
             "buttons": ["solid", "block"], "radius": ["sharp"]},
    "product": {"nav": ["centre", "cards", "plain"], "footer": ["columns", "dark"],
                "close": ["photo", "type"], "rhythm": ["brand-band", "space", "surface-pairs"],
                "buttons": ["solid", "pill", "tonal"], "radius": ["soft", "round"]},
    "service": {"nav": ["mega", "split", "centre"], "footer": ["visit", "dark", "columns"],
                "close": ["type", "photo"], "rhythm": ["surface-pairs", "dark-band", "space"],
                "buttons": ["solid", "tonal"], "radius": ["soft"]},
    "place": {"nav": ["split", "plain", "cards"], "footer": ["visit", "columns"],
              "close": ["photo", "word"], "rhythm": ["surface-pairs", "space", "colour-band"],
              "buttons": ["solid", "pill"], "radius": ["square"]},
}
PARTS["hardware"] = PARTS["product"]

# Heroes each kind may take, read from the hero rows of patterns.csv (use_for / avoid_for).
HEROES = {
    "software": ["split", "collage", "word", "statement", "triptych", "centred"],
    "game": ["split", "triptych"],
    "product": ["split", "photo", "product", "editorial", "triptych"],
    "hardware": ["split", "product", "triptych"],
    "service": ["split", "photo", "editorial", "statement"],
    "place": ["place"],
}
NEEDS_FOOTAGE = {"software": ["film"], "game": ["film"], "hardware": ["film"]}
NEEDS_PHOTOS = {"nav": "cards", "close": "photo", "rhythm": "media-band", "hero": "photo"}
NO_PHOTO_SWAP = {"cards": "split", "photo": "word", "media-band": "space"}

TECH = {"software", "game", "hardware"}
PAGE_GROUNDS = {"paper", "topglow", "stage"}  # scoped to the page top or one panel


def _words(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


# ---- colour maths (WCAG 2.x relative luminance) ----

def _lin(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_colour: str) -> float:
    h = hex_colour.lstrip("#")
    if not re.fullmatch(r"[0-9a-fA-F]{6}", h):
        raise ValueError(f"not a #RRGGBB colour: {hex_colour}")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contrast(a: str, b: str) -> float:
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


# What every palette must meet. (foreground, background, minimum ratio, why)
NEEDS = (
    ("ink", "bg", 7.0, "body text on the page"),
    ("ink", "surface", 7.0, "body text on cards"),
    ("muted", "bg", 4.5, "secondary text on the page"),
    ("muted", "surface", 4.5, "secondary text on cards"),
    ("accentInk", "accent", 4.5, "button label on the accent"),
    ("accent", "bg", 3.0, "accent as a button or focus ring against the page"),
)


def check_palette(p: dict) -> list[str]:
    """Return the failed needs; empty means the palette passes."""
    bad = []
    for fg, bg, need, why in NEEDS:
        r = contrast(p[fg], p[bg])
        if r < need:
            bad.append(f"{p['id']}: {fg} on {bg} is {r:.2f}:1, needs {need}:1 ({why})")
    return bad


def ratios(p: dict) -> dict:
    out = {f"{fg}/{bg}": round(contrast(p[fg], p[bg]), 2) for fg, bg, _, _ in NEEDS}
    out["accent-as-text"] = contrast(p["accent"], p["bg"]) >= 4.5
    return out


# ---- data ----

@lru_cache(maxsize=None)
def palettes() -> tuple[dict, ...]:
    return tuple(json.loads((PRESETS / "palettes.json").read_text(encoding="utf-8")))


@lru_cache(maxsize=None)
def type_presets() -> tuple[dict, ...]:
    with TYPE_TABLE.open(encoding="utf-8") as fh:
        rows = {r["Pairing"]: r for r in csv.DictReader(fh)}
    out = []
    for t in json.loads((PRESETS / "type.json").read_text(encoding="utf-8")):
        row = rows.get(t["pairing"])
        if row is None:
            raise KeyError(f"type.json names a pairing not in typography.csv: {t['pairing']}")
        out.append({**t, "heading": row["Heading Font"], "body": row["Body Font"],
                    "heading_weights": row["Heading Weights"], "body_weights": row["Body Weights"],
                    "heading_stack": row["Heading Stack"], "body_stack": row["Body Stack"],
                    "url": row["Google Fonts URL"], "mood": row["Mood"], "best_for": row["Best For"]})
    return tuple(out)


@lru_cache(maxsize=None)
def grounds() -> tuple[dict, ...]:
    with PATTERNS.open(encoding="utf-8") as fh:
        rows = [r for r in csv.DictReader(fh) if r["kind"] == "ground"]
    for r in rows:
        r["clashes"] = set(re.findall(r"next to (\w+)", r["avoid_for"]))
    return tuple(rows)


def guess_kind(text: str) -> str:
    w = _words(text)
    for kind, vocab in KIND_WORDS.items():
        if w & set(vocab.split()):
            return kind
    return "software"


# ---- history ----

def _history_path(root: Path | None) -> Path:
    return state_dir(root or project_root()) / HISTORY_FILE


def load_history(root: Path | None = None) -> list[dict]:
    try:
        data = json.loads(_history_path(root).read_text(encoding="utf-8"))
        return [d for d in data if isinstance(d, dict)] if isinstance(data, list) else []
    except (OSError, ValueError):
        return []


def save_history(entry: dict, root: Path | None = None) -> None:
    hist = (load_history(root) + [entry])[-HISTORY_KEEP:]
    write_private(_history_path(root), json.dumps(hist, indent=1) + "\n")


def _recent(history: list[dict], kind: str, part: str) -> list[str]:
    """This part's last picks for this kind, newest last."""
    same = [h for h in history if h.get("kind") == kind][-AVOID_LAST:]
    return [str(h.get(part)) for h in same if h.get(part)]


def _fresh(pool: list, recent: list[str], key) -> list:
    """Drop the last N picks; with too few options, drop fewer, but always the last one."""
    for n in range(len(recent), 0, -1):
        avoid = set(recent[-n:])
        keep = [o for o in pool if key(o) not in avoid]
        if keep:
            return keep
    return pool


# ---- dealing ----

def _score(tags: set[str], brief: set[str]) -> int:
    return len(tags & brief)


def _pick(rng: random.Random, pool: list, recent: list[str], key=lambda x: x):
    return rng.choice(_fresh(pool, recent, key))


def _weighted_pool(items: list[dict], brief: set[str], tag_fields: tuple[str, ...]) -> list[dict]:
    """Items sharing the most words with the brief; all items when none share any."""
    def tags(it):
        s = set()
        for f in tag_fields:
            v = it.get(f, "")
            s |= _words(" ".join(v) if isinstance(v, list) else v)
        return s
    scored = [(_score(tags(it), brief), it) for it in items]
    best = max((s for s, _ in scored), default=0)
    if best == 0:
        return items
    # Keep everything within one word of the best, so the deal still has a choice.
    return [it for s, it in scored if s >= max(1, best - 1)]


def _pick_ranked(rng, items, words, fields, recent, key):
    """Best match to the brief among items not dealt lately; recent ones only if nothing else."""
    return rng.choice(_weighted_pool(_fresh(items, recent, key), words, fields))


def deal(brief: str, kind: str = "", mode: str = "", seed: int | None = None,
         history: list[dict] | None = None, photos: bool = True, footage: bool = False) -> dict:
    kind = kind or guess_kind(brief)
    if kind not in KINDS:
        raise ValueError(f"unknown kind {kind!r}; use one of {', '.join(KINDS)}")
    if mode and mode not in ("light", "dark"):
        raise ValueError("mode is light or dark")
    rng = random.Random(seed)
    history = history or []
    words = _words(brief)

    pal = [p for p in palettes() if kind in p["kinds"] and (not mode or p["mode"] == mode)]
    if not pal:
        pal = [p for p in palettes() if not mode or p["mode"] == mode]
    palette = _pick_ranked(rng, pal, words, ("trades", "moods"),
                           _recent(history, kind, "palette"), key=lambda p: p["id"])

    ty = [t for t in type_presets() if kind in t["kinds"]] or list(type_presets())
    typeset = _pick_ranked(rng, ty, words, ("best_for", "mood"),
                           _recent(history, kind, "type"), key=lambda t: t["pairing"])

    heroes = HEROES[kind] + (NEEDS_FOOTAGE.get(kind, []) if footage else [])
    if not photos:
        heroes = [h for h in heroes if h != "photo"] or heroes
    out = {"kind": kind, "brief": brief, "seed": seed}
    out["hero"] = _pick(rng, heroes, _recent(history, kind, "hero"))

    swaps = []
    for part, options in PARTS[kind].items():
        pick = _pick(rng, options, _recent(history, kind, part))
        if not photos and NEEDS_PHOTOS.get(part) == pick:
            new = NO_PHOTO_SWAP.get(pick, pick)
            swaps.append(f"{part}: {pick} -> {new} (no photographs)")
            pick = new
        out[part] = pick
    out["swaps"] = swaps

    if kind in TECH:
        section = [g for g in grounds() if g["name"] not in PAGE_GROUNDS
                   and (photos or g["name"] != "photo")]
        recent = " ".join(_recent(history, kind, "grounds_flat")[-1:]).split()
        first = _pick(rng, section, recent, key=lambda g: g["name"])
        rest = [g for g in section if g["name"] != first["name"]
                and g["name"] not in first["clashes"] and first["name"] not in g["clashes"]]
        second = _pick(rng, rest, recent, key=lambda g: g["name"])
        page = _pick(rng, [g for g in grounds() if g["name"] in PAGE_GROUNDS], recent,
                     key=lambda g: g["name"])
        out["grounds"] = [{"name": g["name"], "use": g["use_for"]} for g in (first, second)]
        out["page_ground"] = page["name"]
        out["grounds_flat"] = " ".join(sorted({first["name"], second["name"], page["name"]}))
    else:
        out["grounds"] = []
        out["page_ground"] = "flat page ground; named grounds are for tech pages"

    out["palette"] = palette["id"]
    out["palette_detail"] = {k: palette[k] for k in
                             ("mode", "bg", "surface", "ink", "muted", "accent", "accentInk", "line", "note")}
    out["contrast"] = ratios(palette)
    out["type"] = typeset["pairing"]
    out["type_detail"] = {k: typeset[k] for k in
                          ("heading", "body", "heading_weights", "body_weights", "tracking", "scale", "case", "url")}
    return out


def css(d: dict) -> str:
    p, t = d["palette_detail"], d["type_detail"]
    radius = {"sharp": "2px", "square": "0", "soft": "10px", "round": "999px"}.get(d["radius"], "8px")
    lines = [
        f"/* dealt by `ult design deal`: {d['kind']}, palette {d['palette']}, type {d['type']} */",
        f"@import url(\"{t['url']}\");" if t["url"] else "",
        ":root {",
        f"  color-scheme: {p['mode']};",
        f"  --bg: {p['bg']};", f"  --surface: {p['surface']};", f"  --ink: {p['ink']};",
        f"  --muted: {p['muted']};", f"  --accent: {p['accent']};", f"  --accent-ink: {p['accentInk']};",
        f"  --line: {p['line']};",
        f"  --font-display: \"{t['heading']}\", system-ui, sans-serif;",
        f"  --font-body: \"{t['body']}\", system-ui, sans-serif;",
        f"  --display-tracking: {t['tracking']};",
        f"  --type-scale: {t['scale']};",
        f"  --radius: {radius};",
        "}",
    ]
    return "\n".join(x for x in lines if x)


def render(d: dict) -> str:
    p = d["palette_detail"]
    c = d["contrast"]
    t = d["type_detail"]
    rows = [
        f"Deal for a {d['kind']} page: {d['brief'] or '(no brief)'}",
        "",
        f"palette   {d['palette']} ({p['mode']}): bg {p['bg']}, surface {p['surface']}, ink {p['ink']}, "
        f"muted {p['muted']}, accent {p['accent']} on {p['accentInk']}, line {p['line']}",
        f"          {p['note']}",
        f"          contrast ink {c['ink/bg']}:1, muted {c['muted/bg']}:1, button {c['accentInk/accent']}:1; "
        + ("accent may be used for link text" if c["accent-as-text"] else
           "accent is for fills and rings only, not text (under 4.5:1)"),
        f"type      {d['type']}: {t['heading']} {t['heading_weights']} over {t['body']} {t['body_weights']}; "
        f"display tracking {t['tracking']}, scale {t['scale']}, {t['case']}",
        f"hero      {d['hero']}",
    ]
    for part in ("nav", "footer", "close", "rhythm", "buttons", "radius"):
        rows.append(f"{part:<9} {d[part]}")
    if d["grounds"]:
        rows.append("grounds   " + "; ".join(f"{g['name']} ({g['use']})" for g in d["grounds"]))
    rows.append(f"page      {d['page_ground']}")
    for s in d["swaps"]:
        rows.append(f"swap      {s}")
    rows += ["", "Write these on plan line 2. Re-deal one part only when its use doesn't fit, and say why."]
    return "\n".join(rows)


def cmd_deal(args) -> int:
    brief = " ".join(args.text).strip()
    root = project_root()
    history = [] if args.fresh else load_history(root)
    try:
        d = deal(brief, args.kind, args.mode, args.seed, history,
                 photos=not args.no_photos, footage=args.footage)
    except (ValueError, KeyError) as exc:
        print(f"ult design deal: {exc}")
        return 2
    if not args.no_save:
        save_history({k: d[k] for k in ("kind", "palette", "type", "hero", "nav", "footer", "close",
                                       "rhythm", "buttons", "radius")} | {"grounds_flat": d.get("grounds_flat", "")},
                     root)
    if args.css:
        Path(args.css).parent.mkdir(parents=True, exist_ok=True)
        Path(args.css).write_text(css(d) + "\n", encoding="utf-8")
    print(dump_json(d) if args.json else render(d))
    if args.css:
        print(f"wrote {args.css}")
    return 0


def add_arguments(p) -> None:
    p.add_argument("--kind", default="", help=f"page kind: {', '.join(KINDS)} (guessed from the brief if left out)")
    p.add_argument("--mode", default="", help="deal only light or only dark palettes")
    p.add_argument("--seed", type=int, default=None, help="repeatable deal")
    p.add_argument("--fresh", action="store_true", help="ignore the deal history")
    p.add_argument("--no-save", action="store_true", help="don't record this deal in the history")
    p.add_argument("--no-photos", action="store_true", help="no client photographs: swap photo-led parts")
    p.add_argument("--footage", action="store_true", help="real footage exists: allow the film hero")
    p.add_argument("--css", default="", help="write the dealt tokens to this CSS file")
