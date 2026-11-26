"""`ult design` - offline search over the bundled design tables, and a starting design system.

The tables in data/design/ are third-party data (UI UX Pro Max, MIT; see NOTICE.md there).
This module is original: a small BM25 ranker over chosen columns, and `system`, which joins
the product, reasoning, palette, style, landing and font tables into one brief section.
Standard library only; nothing is fetched.

  ult design search "<query>" [--in DOMAIN] [-n N] [--json]
  ult design system "<what you are making>" [--stack NAME] [--out FILE] [--json]
  ult design domains
"""
from __future__ import annotations

import csv
import math
import re
from collections import Counter
from functools import lru_cache
from pathlib import Path

from .common import dump_json

DATA = Path(__file__).resolve().parents[2] / "data" / "design"

# domain -> (file, columns searched, columns shown)
DOMAINS: dict[str, tuple[str, tuple[str, ...], tuple[str, ...]]] = {
    "product": ("products.csv", ("Product Type", "Keywords", "Key Considerations"),
                ("Product Type", "Primary Style Recommendation", "Secondary Styles", "Landing Page Pattern",
                 "Color Palette Focus", "Key Considerations")),
    "style": ("styles.csv", ("Style Category", "Aliases", "Keywords", "Best For", "Type"),
              ("Style Category", "Keywords", "Primary Colors", "Effects & Animation", "Best For", "Do Not Use For",
               "Accessibility", "Performance", "CSS/Technical Keywords", "Design System Variables")),
    "color": ("colors.csv", ("Product Type", "Notes"),
              ("Product Type", "Primary", "Secondary", "Accent", "Background", "Foreground", "Muted", "Border",
               "Destructive", "Notes")),
    "typography": ("typography.csv", ("Font Pairing Name", "Category", "Mood/Style Keywords", "Best For",
                                      "Heading Font", "Body Font"),
                   ("Font Pairing Name", "Heading Font", "Body Font", "Mood/Style Keywords", "Best For",
                    "Google Fonts URL", "Notes")),
    "landing": ("landing.csv", ("Pattern Name", "Aliases", "Keywords", "Conversion Optimization"),
                ("Pattern Name", "Section Order", "Primary CTA Placement", "Color Strategy", "Recommended Effects",
                 "Conversion Optimization")),
    "reasoning": ("ui-reasoning.csv", ("UI_Category", "Style_Priority", "Color_Mood", "Typography_Mood"),
                  ("UI_Category", "Recommended_Pattern", "Style_Priority", "Color_Mood", "Typography_Mood",
                   "Key_Effects", "Anti_Patterns")),
    "ux": ("ux-guidelines.csv", ("Category", "Issue", "Description", "Platform"),
           ("Category", "Issue", "Severity", "Do", "Don't", "Code Example Good")),
    "app": ("app-interface.csv", ("Category", "Issue", "Keywords", "Description"),
            ("Category", "Issue", "Severity", "Do", "Don't", "Code Example Good")),
    "react": ("react-performance.csv", ("Category", "Issue", "Keywords", "Description"),
              ("Category", "Issue", "Severity", "Do", "Don't", "Code Example Good")),
    "chart": ("charts.csv", ("Data Type", "Keywords", "Best Chart Type", "When to Use"),
              ("Data Type", "Best Chart Type", "Secondary Options", "When to Use", "When NOT to Use",
               "Accessibility Notes", "Library Recommendation")),
    "motion": ("motion.csv", ("Category", "Intensity Tier", "Keywords", "Trigger"),
               ("Category", "Intensity Tier", "Trigger", "Duration", "Easing", "Do", "Don't", "Performance Notes")),
    "icon": ("icons.csv", ("Category", "Icon Name", "Keywords", "Best For", "Library"),
             ("Icon Name", "Library", "Import Code", "Usage", "Best For")),
}
STACK_SEARCH = ("Category", "Guideline", "Description", "Applies To")
STACK_SHOW = ("Category", "Guideline", "Severity", "Do", "Don't", "Docs URL")
STOP = frozenset("a an and the for of to with in on or is are my our we i it this that me make build "
                 "want need new site website page app".split())
# Ultimatum's own additions: everyday words for a business mapped to the words the product
# table uses, so "coffee shop" finds Bakery/Cafe. Applied to `system` briefs only.
SYNONYMS = {
    "coffee": "cafe", "espresso": "cafe", "barista": "cafe", "cafes": "cafe", "bakeries": "bakery",
    "gym": "fitness", "crossfit": "fitness", "yoga": "fitness wellness", "pilates": "fitness wellness",
    "clothing": "fashion e-commerce", "apparel": "fashion e-commerce", "boutique": "fashion",
    "nonprofit": "non profit charity", "ngo": "non profit charity", "shelter": "charity",
    "dentist": "dental clinic", "doctor": "medical clinic", "therapist": "mental health",
    "lawyer": "legal", "attorney": "legal", "realtor": "real estate", "plumber": "home services",
    "electrician": "home services", "contractor": "home services", "salon": "beauty", "barber": "beauty",
    "startup": "saas", "chatbot": "ai", "jewelry": "luxury e-commerce", "jeweler": "luxury e-commerce",
}
SEVERE = {"critical": 0, "high": 1}
NICHE = frozenset({"maps", "ai interaction", "spatial ui", "security"})


def tokens(text: str) -> list[str]:
    out = []
    for w in re.findall(r"[a-z0-9]+", (text or "").lower()):
        if len(w) > 3 and w.endswith("s") and not w.endswith("ss"):
            w = w[:-1]
        if w not in STOP:
            out.append(w)
    return out


@lru_cache(maxsize=None)
def table(file: str) -> tuple[dict, ...]:
    with (DATA / file).open(encoding="utf-8", newline="") as fh:
        return tuple(csv.DictReader(fh))


def stacks() -> list[str]:
    return sorted(p.stem for p in (DATA / "stacks").glob("*.csv"))


def rank(rows, cols, query: str, n: int = 3) -> list[tuple[float, dict]]:
    """BM25 (k1 1.5, b 0.75) over the joined text of `cols`; rows with no hit are left out."""
    want = set(tokens(query))
    if not want:
        return []
    docs = [Counter(tokens(" ".join(r.get(c, "") for c in cols))) for r in rows]
    avg = sum(sum(d.values()) for d in docs) / max(len(docs), 1) or 1.0
    df = Counter(t for d in docs for t in want if t in d)
    scored = []
    for row, doc in zip(rows, docs):
        length = sum(doc.values())
        s = 0.0
        for t in want & doc.keys():
            idf = math.log(1 + (len(docs) - df[t] + 0.5) / (df[t] + 0.5))
            tf = doc[t]
            s += idf * tf * 2.5 / (tf + 1.5 * (0.25 + 0.75 * length / avg))
        if s > 0:
            scored.append((round(s, 3), row))
    scored.sort(key=lambda x: -x[0])
    return scored[:n]


def search(query: str, domain: str, n: int = 3) -> list[dict]:
    if domain.startswith("stack:"):
        name = domain.split(":", 1)[1]
        if name not in stacks():
            raise ValueError(f"unknown stack {name!r}; have: {', '.join(stacks())}")
        rows, cols, show = table(f"stacks/{name}.csv"), STACK_SEARCH, STACK_SHOW
    else:
        file, cols, show = DOMAINS[domain]
        rows = table(file)
    return [dict({c: r.get(c, "") for c in show}, score=s) for s, r in rank(rows, cols, query, n)]


def _by(file: str, col: str, value: str) -> dict | None:
    v = value.strip().lower()
    return next((r for r in table(file) if r.get(col, "").strip().lower() == v), None) if v else None


def _style(name: str) -> dict | None:
    hit = _by("styles.csv", "Style Category", name)
    if hit:
        return hit
    ranked = rank(table("styles.csv"), ("Style Category", "Aliases"), name, 1)
    return ranked[0][1] if ranked else None


def _niche(row: dict, want: set[str]) -> bool:
    """A check for one kind of page (maps, spatial UI, ...) unless the brief names that kind."""
    cat = row.get("Category", "").split("/")[0].strip().lower()
    return cat in NICHE and not (set(tokens(cat)) & want)


def _severe(file: str, cols, query: str, n: int) -> list[dict]:
    want = set(tokens(query))
    rows = [r for r in table(file) if r.get("Severity", "").lower() in SEVERE and not _niche(r, want)
            and r.get("Platform", "All") in ("All", "Web", "")]
    hits: list[dict] = []
    for _, r in rank(rows, cols, query, len(rows)):
        if len(hits) < n and sum(h.get("Category") == r.get("Category") for h in hits) < 3:
            hits.append(r)  # at most 3 from one topic
    seen = {r.get("Category") for r in hits}
    # Fill with the most severe, one per category first so the list is not all one topic.
    for r in sorted(rows, key=lambda r: (r.get("Category") in seen, SEVERE[r["Severity"].lower()])):
        if len(hits) >= n:
            break
        if r not in hits:
            hits.append(r)
            seen.add(r.get("Category"))
    return hits


def system(brief: str, stack: str = "") -> dict:
    """A starting design system for `brief`: one product match and what the tables pair with it."""
    # A brief that names the business ("gym") should land on that product: a word shared with
    # the product's name adds its rarity (idf over all names) to the keyword score.
    rows = table("products.csv")
    names = [set(tokens(r["Product Type"])) for r in rows]
    df = Counter(t for n in names for t in n)
    query = " ".join([brief, *(SYNONYMS[t] for t in tokens(brief) if t in SYNONYMS)])
    want = set(tokens(query))
    found = []
    for s, r in rank(rows, DOMAINS["product"][1], query, 10):
        bonus = 2 * sum(math.log(len(rows) / df[t]) for t in want & set(tokens(r["Product Type"])))
        found.append((s + bonus, r))
    found.sort(key=lambda sr: -sr[0])
    if not found:
        return {"brief": brief, "product": None}
    product = found[0][1]
    kind = product["Product Type"]
    why = _by("ui-reasoning.csv", "UI_Category", kind) or {}
    styles = [s for s in (_style(p) for p in re.split(r"\s\+\s", product["Primary Style Recommendation"])) if s]
    fonts = [r for _, r in rank(table("typography.csv"), DOMAINS["typography"][1],
                                " ".join([brief, why.get("Typography_Mood", ""), product.get("Keywords", "")]), 2)]
    out = {
        "brief": brief,
        "product": kind,
        "also_close": found[1][1]["Product Type"] if len(found) > 1 else "",
        "styles": [s["Style Category"] for s in styles],
        "secondary_styles": product.get("Secondary Styles", ""),
        "style_notes": [{k: s.get(k, "") for k in ("Style Category", "Effects & Animation", "Accessibility",
                                                    "Design System Variables")} for s in styles],
        "palette": {k: v for k, v in (_by("colors.csv", "Product Type", kind) or {}).items() if k != "Product Type"},
        "fonts": [{k: f[k] for k in ("Font Pairing Name", "Heading Font", "Body Font", "Google Fonts URL")} for f in fonts],
        "landing": _by("landing.csv", "Pattern Name", product.get("Landing Pattern Match", "")) or {},
        "effects": why.get("Key_Effects", ""),
        "avoid": [a.strip() for a in why.get("Anti_Patterns", "").split("+") if a.strip()],
        "considerations": product.get("Key Considerations", ""),
        "checks": [{k: r[k] for k in ("Category", "Issue", "Severity", "Do")}
                   for r in _severe("ux-guidelines.csv", DOMAINS["ux"][1], brief, 6)],
    }
    if stack:
        if stack not in stacks():
            raise ValueError(f"unknown stack {stack!r}; have: {', '.join(stacks())}")
        out["stack"] = stack
        out["stack_checks"] = [{k: r.get(k, "") for k in ("Guideline", "Severity", "Do")}
                               for r in _severe(f"stacks/{stack}.csv", STACK_SEARCH, brief, 5)]
    return out


def render(ds: dict) -> str:
    if not ds.get("product"):
        return f"no product match for: {ds['brief']}. Try naming the kind of business, e.g. \"coffee shop\"."
    pal = ds["palette"]
    lines = [
        "## Design system (starting point)",
        f"Source: Ultimatum design tables (UI UX Pro Max data, MIT). Closest product: **{ds['product']}**"
        + (f" (next: {ds['also_close']})" if ds["also_close"] else "") + ". Adjust to the brief; the tables are a start, not the answer.",
        "",
        f"- **Style:** {' + '.join(ds['styles']) or '-'}" + (f"; also fits {ds['secondary_styles']}" if ds["secondary_styles"] else ""),
    ]
    if pal:
        main = ("Primary", "Secondary", "Accent", "Background", "Foreground", "Muted", "Border")
        lines.append("- **Palette:** " + ", ".join(f"{k.lower()} {pal[k]}" for k in main if pal.get(k))
                     + (f". {pal['Notes']}" if pal.get("Notes") else ""))
    for i, f in enumerate(ds["fonts"]):
        label = "Fonts" if i == 0 else "Alt fonts"
        lines.append(f"- **{label}:** {f['Heading Font']} / {f['Body Font']} ({f['Font Pairing Name']})")
    if ds["landing"]:
        lp = ds["landing"]
        lines.append(f"- **Page pattern:** {lp['Pattern Name']}: {lp.get('Section Order', '')}. CTA: {lp.get('Primary CTA Placement', '')}")
    if ds["effects"]:
        lines.append(f"- **Motion:** {ds['effects']}")
    if ds["considerations"]:
        lines.append(f"- **Keep in mind:** {ds['considerations']}")
    if ds["avoid"]:
        lines.append("- **Avoid:** " + "; ".join(ds["avoid"]))
    for s in ds["style_notes"]:
        if s.get("Design System Variables"):
            lines.append(f"- **{s['Style Category']} tokens:** {s['Design System Variables']}")
    lines += ["", "Checks before delivery:"]
    lines += [f"- [{c['Severity']}] {c['Category']}, {c['Issue']}: {c['Do']}" for c in ds["checks"]]
    if ds.get("stack_checks"):
        lines += ["", f"{ds['stack']} checks:"]
        lines += [f"- [{c['Severity']}] {c['Guideline']}: {c['Do']}" for c in ds["stack_checks"]]
    return "\n".join(lines)


def _print_rows(rows: list[dict]) -> None:
    for i, r in enumerate(rows, 1):
        items = [(k, v) for k, v in r.items() if k != "score" and v]
        print(f"{i}. {items[0][1]}" if items else f"{i}.")
        for k, v in items[1:]:
            print(f"   {k}: {v}")


def cmd_design(args) -> int:
    if args.action == "domains":
        for name, (file, _, _) in DOMAINS.items():
            print(f"{name:<10} {len(table(file)):>4} rows  {file}")
        print(f"stack:NAME       {', '.join(stacks())}")
        return 0
    text = " ".join(args.text).strip()
    if not text:
        print(f'usage: ult design {args.action} "<text>"')
        return 2
    try:
        if args.action == "search":
            rows = search(text, args.domain, args.n)
            if args.json:
                print(dump_json(rows))
            elif rows:
                _print_rows(rows)
            else:
                print(f"no match in {args.domain} for: {text}")
            return 0
        ds = system(text, args.stack)
    except (ValueError, KeyError) as exc:
        print(f"ult design: {exc}")
        return 2
    body = dump_json(ds) if args.json else render(ds)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(body + "\n", encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        print(body)
    return 0


def register(sub):
    p = sub.add_parser("design", help="offline design tables: search, or a starting design system")
    p.add_argument("action", choices=("search", "system", "domains"))
    p.add_argument("text", nargs="*", help="query, or what you are making")
    p.add_argument("--in", dest="domain", default="style",
                   help=f"search domain: {', '.join(DOMAINS)}, or stack:NAME (default style)")
    p.add_argument("-n", type=int, default=3, help="results (default 3)")
    p.add_argument("--stack", default="", help="add that stack's high-severity checks to `system`")
    p.add_argument("--out", default="", help="write `system` output to this file")
    p.add_argument("--json", action="store_true", help="machine-readable output")
    p.set_defaults(func=cmd_design)
