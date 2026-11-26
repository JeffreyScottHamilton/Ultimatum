#!/usr/bin/env python3
"""Build Ultimatum's own font pairings: plugins/ultimatum/data/design-own/typography.csv.

The pairings below are our own choices. Facts about each family (designer, licence,
category, weights, scripts) come from Google Fonts' own metadata (the METADATA.pb file
for the family in https://github.com/google/fonts), cached in fonts-meta.json so the
build and the tests never touch the network.

    python3 tools/build_typography.py --fetch   # refresh fonts-meta.json (network)
    python3 tools/build_typography.py           # write typography.csv from the cache
    python3 tools/build_typography.py --check   # exit 1 if the CSV is out of date

Standard library only.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OWN = ROOT / "plugins" / "ultimatum" / "data" / "design-own"
OUT, META = OWN / "typography.csv", OWN / "fonts-meta.json"
RAW = "https://raw.githubusercontent.com/google/fonts/main/{dir}/{slug}/METADATA.pb"

COLS = ("Pairing", "Mood", "Best For", "Heading Font", "Body Font", "Heading Weights", "Body Weights",
        "Kind", "Licence", "Extra Scripts", "Heading Stack", "Body Stack", "Google Fonts URL", "Notes")

# (pairing, heading, body, heading weights, body weights, mood, best for, notes)
PAIRS: list[tuple[str, str, str, str, str, str, str, str]] = [
    # --- local services and small business --------------------------------------------------
    ("Workshop", "Archivo", "Archivo", "700;800", "400;600", "sturdy, practical, no-nonsense",
     "plumbers, electricians, roofers, builders, garages",
     "One family at two weights reads like signage on a van; the wide letters hold up at small sizes on phones."),
    ("Callout", "Barlow Condensed", "Barlow", "600;700", "400;500", "direct, compact, outdoorsy",
     "landscapers, removals, pest control, trades with long service lists",
     "Condensed headings fit long service names on one line at 375 px; keep the condensed cut out of body text."),
    ("Fresh Start", "Hanken Grotesk", "Hanken Grotesk", "700", "400;500", "clean, tidy, approachable",
     "cleaning services, handymen, home organisers",
     "A neutral grotesk with open shapes; pair it with real photos of finished jobs rather than decoration."),
    ("Main Street", "Libre Franklin", "Source Serif 4", "700;800", "400;600", "established, local, trustworthy",
     "accountants, insurance brokers, estate agents, family firms",
     "A gothic headline over a readable text serif reads like a well-made local paper."),
    ("Chair", "Syne", "Manrope", "600;700", "400;500", "stylish, a little edgy",
     "barbers, hair salons, tattoo studios",
     "Syne's wide display shapes give character in the name and headings only; Manrope keeps prices and times plain."),
    ("Nail Bar", "Gloock", "Figtree", "400", "400;600", "polished, feminine without being frilly",
     "nail salons, brow and lash studios, beauty rooms",
     "Gloock has one weight: use it large and sparingly. Figtree carries the price list and booking form."),
    ("Kneaded", "Young Serif", "Work Sans", "400", "400;500", "warm, homemade, honest",
     "bakeries, cafes, delis, farm shops",
     "A soft, sturdy serif for the name and menu headings; Work Sans for opening hours, allergens and prices."),
    ("Chalkboard", "Bricolage Grotesque", "Bricolage Grotesque", "700;800", "400;500", "lively, independent, a bit loud",
     "coffee bars, food trucks, street food, markets",
     "One variable family: tight and heavy for the headline, relaxed for text. No script fonts needed for personality."),
    ("Supper", "Fraunces", "Libre Franklin", "600;700", "400;500", "rich, convivial, crafted",
     "restaurants, wine bars, bistros",
     "Fraunces has optical sizes and soft shapes; set the menu in Libre Franklin so dishes and prices scan quickly."),
    ("Taproom", "Big Shoulders Display", "Rethink Sans", "700;800", "400;500", "industrial, bold, social",
     "brewery, distillery, bar, pub, music venue",
     "A tall, narrow display face for names and events; avoid it below 24 px."),
    ("Clinic", "Atkinson Hyperlegible", "Atkinson Hyperlegible", "700", "400;700", "clear, calm, inclusive",
     "GP surgeries, pharmacies, opticians, senior care",
     "Designed by the Braille Institute for low-vision readers; distinct letterforms (Il1, 0O) help older visitors."),
    ("Smile", "Plus Jakarta Sans", "Plus Jakarta Sans", "700", "400;500", "friendly, modern, reassuring",
     "dental practices, physiotherapy, chiropractors",
     "Rounded but not childish; one family keeps forms and treatment lists consistent."),
    ("Paws", "Fredoka", "Nunito", "600", "400;600", "cheerful, soft, caring",
     "vets, groomers, pet sitters, daycare",
     "Rounded headings warm the page; keep body in Nunito at 17 px or more for comfortable reading."),
    ("Counsel", "Newsreader", "Public Sans", "500;600", "400;500", "considered, steady, quiet authority",
     "law firms, mediators, financial advisers",
     "Newsreader's optical sizes keep headings elegant at display size; Public Sans is a plain US-government sans."),
    ("Ledger", "IBM Plex Serif", "IBM Plex Sans", "600", "400;500", "precise, technical, dependable",
     "bookkeepers, tax preparers, engineering firms",
     "A superfamily: the serif and sans share skeletons, so they pair without clashing; Plex Mono is there for figures."),
    ("Coach", "Sora", "Inter", "600;700", "400;500", "energetic, confident, modern",
     "consultants, business coaches, speakers",
     "Sora's geometric headings feel current; Inter's tall x-height keeps long service pages readable."),
    ("Studio Hour", "Jost", "Karla", "500;600", "400;500", "light, balanced, mindful",
     "yoga studios, pilates, massage therapy",
     "A geometric sans in medium weight is calmer than bold; avoid thin weights for body text."),
    ("Training Floor", "Saira", "Saira", "700;800", "400;500", "athletic, fast, motivating",
     "gyms, personal trainers, martial arts, sports clubs",
     "Saira has width and weight axes: use the wider, heavier cut for class names and the normal cut for timetables."),
    ("Tutor", "Lexend", "Lexend", "600", "400;500", "clear, encouraging, easy to read",
     "tutoring, driving schools, after-school clubs",
     "Lexend was designed around reading-fluency research. Often picked for dyslexia-friendly sites, though "
     "evidence for any single font is mixed: size, spacing and short lines matter more."),
    ("Bloom", "Petrona", "Albert Sans", "600", "400;500", "natural, gentle, fresh",
     "florists, garden centres, plant shops",
     "Petrona's lively serif suits plant names; Albert Sans keeps delivery details and prices neutral."),
    ("Keepsake", "Cormorant Garamond", "Mulish", "500;600", "400;500", "romantic, refined, timeless",
     "wedding photographers, planners, venues",
     "Cormorant is delicate: only use it at 32 px and up, and never for body text or buttons."),
    ("Shutter", "Instrument Serif", "Instrument Sans", "400", "400;500", "editorial, gallery-like, understated",
     "photographers, galleries, portfolios",
     "A narrow serif with one weight for big titles, its companion sans for captions; let the images lead."),
    ("Little Steps", "Baloo 2", "Nunito Sans", "600;700", "400;600", "playful, safe, welcoming",
     "nurseries, childminders, kids' activities",
     "Baloo's round headings feel friendly to parents; the body stays a plain humanist sans for policies and fees."),
    ("Parish", "Spectral", "Source Sans 3", "500;600", "400;600", "warm, dignified, open",
     "churches, community halls, charities",
     "Spectral is a screen-first serif built for long reading; Source Sans 3 handles service times and events."),
    ("Front Desk", "Red Hat Display", "Red Hat Text", "700", "400;500", "hospitable, clear, modern",
     "hotels, B&Bs, guest houses",
     "Display and text cuts of one design, each tuned for its size; switch to Text below 20 px."),
    # --- shops and commerce ---------------------------------------------------------------
    ("Shopfront", "Outfit", "Outfit", "600;700", "400;500", "modern, friendly, versatile",
     "online shops, boutiques, subscription boxes",
     "A geometric sans that stays readable in product grids and prices; one family keeps the shop tidy."),
    ("Atelier", "Bodoni Moda", "Jost", "500;600", "400;500", "high fashion, dramatic contrast",
     "fashion labels, jewellery, luxury retail",
     "Bodoni's hairlines vanish on small screens: keep it at 40 px and up, with Jost for everything else."),
    ("Maison", "Marcellus", "Tenor Sans", "400", "400", "classical, calm, premium",
     "spas, fragrance, skincare, interiors",
     "Both are single-weight faces, so hierarchy comes from size and space; use for short text only."),
    ("Marketplace", "Rubik", "Rubik", "600;700", "400;500", "approachable, slightly rounded, busy-friendly",
     "marketplaces, classifieds, directories",
     "Rubik's soft corners stay readable in dense listings and badges."),
    ("Catalogue", "Schibsted Grotesk", "Schibsted Grotesk", "700", "400;500", "newsy, sharp, efficient",
     "large catalogues, comparison sites, review sites",
     "Designed for a news publisher; works well in tables, filters and long result lists."),
    ("Property", "Familjen Grotesk", "Inter", "600;700", "400;500", "assured, contemporary, crisp",
     "estate agents, lettings, property developers",
     "Familjen's distinctive headings set the brand; Inter handles prices, room counts and forms."),
    ("Wanderer", "Unbounded", "Commissioner", "600;700", "400;500", "adventurous, wide, upbeat",
     "travel agencies, tours, outdoor activity providers",
     "Unbounded is very wide: two- or three-word headings only. Commissioner keeps itineraries readable."),
    # --- apps, SaaS and tools -----------------------------------------------------------------
    ("Product", "Geist", "Geist", "600;700", "400;500", "neutral, technical, crisp",
     "SaaS products, dashboards, developer platforms",
     "A UI-first grotesk with a matching mono (Geist Mono) for code and IDs."),
    ("Console", "Space Grotesk", "IBM Plex Sans", "600;700", "400;500", "technical, characterful, engineered",
     "developer tools, APIs, infrastructure",
     "Space Grotesk's quirks suit headings only; Plex Sans and Plex Mono cover docs and code."),
    ("Workspace", "Instrument Sans", "Inter", "600;700", "400;500", "efficient, familiar, dense-friendly",
     "productivity apps, CRMs, admin panels",
     "Instrument Sans gives headings a little more voice than the UI text; use tabular figures (font-variant-numeric: tabular-nums) in tables."),
    ("Ledger App", "Manrope", "Manrope", "700", "400;500;600", "trustworthy, modern, numeric",
     "fintech, banking apps, invoicing, expense tools",
     "Clear figures at small sizes; turn on tabular numbers for amounts so columns line up."),
    ("Metrics", "Onest", "Onest", "600;700", "400;500", "calm, open, data-friendly",
     "analytics, reporting, monitoring dashboards",
     "Large x-height and open counters keep axis labels and small numbers legible."),
    ("Launchpad", "Bricolage Grotesque", "Hanken Grotesk", "700;800", "400;500", "bold, startup, energetic",
     "startup landing pages, product launches, waitlists",
     "A characterful headline with a quiet text face; resist adding a third font for 'tech' flavour."),
    ("Builder", "Wix Madefor Display", "Wix Madefor Text", "700", "400;500", "practical, platform-like, clear",
     "no-code tools, site builders, form builders",
     "Display and text cuts of one design; switch to Text below 20 px."),
    ("Assistant", "Albert Sans", "Albert Sans", "600;700", "400;500", "clean, helpful, unobtrusive",
     "AI assistants, chat apps, support tools",
     "Keep the interface plain so the conversation is the focus; no futuristic display faces."),
    ("Secure", "Chakra Petch", "Rethink Sans", "600", "400;500", "technical, guarded, sharp",
     "security products, VPNs, password managers",
     "Chakra Petch's cut corners hint at hardware; keep it to short headings and use Rethink Sans for anything long."),
    ("Status", "Red Hat Mono", "Red Hat Text", "500;600", "400;500", "factual, operational",
     "status pages, changelogs, incident reports",
     "Monospace only for timestamps, versions and service names; prose stays in the sans."),
    ("Docs", "Source Serif 4", "Source Sans 3", "600", "400;600", "scholarly, readable, structured",
     "documentation, knowledge bases, handbooks",
     "Adobe's Source superfamily: serif headings, sans body and Source Code Pro for code all share proportions."),
    ("Notebook", "Literata", "Literata", "600", "400;500", "bookish, focused, long-reading",
     "note apps, writing tools, reading apps, journals",
     "Literata was made for e-reading; one family with optical sizes keeps a long page calm."),
    # --- health, care and wellbeing -----------------------------------------------------------
    ("Care Team", "Figtree", "Figtree", "600;700", "400;500", "warm, clear, human",
     "patient portals, telehealth, care apps",
     "A friendly geometric sans with clear figures for dates, doses and times."),
    ("Breathe", "Alegreya", "Alegreya Sans", "500", "400;500", "literary, calm, organic",
     "therapy, counselling, meditation, journalling",
     "A calligraphic serif with its own humanist sans; soft without being pastel-sweet."),
    ("Lab", "IBM Plex Mono", "Instrument Sans", "500;600", "400;500", "scientific, exact",
     "biotech, research labs, science teams",
     "Mono for headings, data, sample IDs and formulas; long text belongs in Instrument Sans."),
    ("Rest", "Nunito", "Nunito", "700", "400;600", "soft, gentle, reassuring",
     "sleep, habit and mood trackers, wellbeing apps",
     "Rounded terminals feel gentle; keep body at 400 or above, never Light."),
    # --- culture, media and editorial -------------------------------------------------------------
    ("Broadsheet", "Playfair Display", "Source Serif 4", "700;800", "400;600", "serious, journalistic",
     "news sites, magazines, long-form journalism",
     "High-contrast headlines over a sturdy text serif; Playfair is for big headlines only."),
    ("Column", "DM Serif Display", "DM Sans", "400", "400;500", "editorial, warm, contemporary",
     "blogs, newsletters, personal sites",
     "DM Serif Display has one weight; get hierarchy from size. DM Sans is the low-contrast partner."),
    ("Programme", "Fraunces", "Instrument Sans", "600;800", "400;500", "theatrical, expressive",
     "theatres, festivals, cinemas, arts centres",
     "Use Fraunces' soft and wonky axes for posters and titles, not for listings."),
    ("Exhibit", "Gelasio", "Archivo", "500;600", "400;500", "curated, quiet, cultured",
     "museums, archives, heritage sites",
     "Gelasio is metric-compatible with Georgia, so the fallback barely shifts the layout."),
    ("Liner Notes", "Archivo Narrow", "Archivo", "600;700", "400;500", "musical, compact, punchy",
     "musicians, labels, podcasts, venues",
     "Narrow headings fit track and event names; one family keeps it coherent."),
    ("Folio", "Libre Caslon Display", "Libre Caslon Text", "400", "400;700", "literary, traditional, bookish",
     "publishers, authors, bookshops, literary prizes",
     "Display and text cuts of one Caslon revival, each tuned for its size."),
    ("Agency", "Darker Grotesque", "Hanken Grotesk", "700;800", "400;500", "confident, fashion-adjacent, tall",
     "creative agencies, studios, design portfolios",
     "Darker Grotesque is tall and tight at heavy weights; it needs big sizes and short lines."),
    ("Gallery Wall", "Cormorant", "Inter", "500;600", "400", "elegant, sparse, artistic",
     "artists, architects, interior designers",
     "A tall, sharp serif for names and titles over a neutral sans; leave plenty of space."),
    ("Blueprint", "Space Grotesk", "Space Grotesk", "500;700", "400", "architectural, modular, modern",
     "architecture practices, engineering, construction tech",
     "One family with technical character; use Space Mono for drawings, specs and plot numbers."),
    # --- community, public and education -------------------------------------------------------------
    ("Civic", "Public Sans", "Public Sans", "700", "400;600", "neutral, accessible, official",
     "councils, public services, government portals",
     "Built for US government sites from Libre Franklin; neutral enough for any public service."),
    ("Good Cause", "Merriweather", "Merriweather Sans", "700", "400;600", "warm, earnest, readable",
     "charity, foundation, campaign, fundraising",
     "Merriweather's large x-height reads well on screens; the matching sans handles donate forms."),
    ("Classroom", "Andika", "Andika", "700", "400", "plain, learner-friendly",
     "early-years and literacy apps, schools",
     "SIL designed Andika for beginning readers: single-storey a and g, and clear distinctions between letters."),
    ("Campus", "Crimson Pro", "Work Sans", "600", "400;500", "academic, welcoming",
     "university, college, courses, research groups",
     "A Garamond-like serif for headings and pull quotes; Work Sans for timetables and forms."),
    ("Journal", "EB Garamond", "EB Garamond", "600", "400;500", "scholarly, historic",
     "academic journals, archives, essays",
     "A classic old-style face for long reading; set body at 19-20 px since its x-height is small."),
    ("Clubhouse", "Anton", "Barlow", "400", "400;600", "loud, sporty, team spirit",
     "sports clubs, leagues, fan sites",
     "Anton is a single heavy weight: short headings only, never paragraphs."),
    ("Gathering", "Epilogue", "Epilogue", "700;800", "400;500", "open, social, inclusive",
     "events, conferences, meetups, coworking",
     "Wide weight range in one family; heavy for dates and names, regular for agendas."),
    ("Forum", "IBM Plex Sans", "IBM Plex Sans", "600", "400;500", "neutral, conversational, robust",
     "forums, Q&A sites, communities",
     "Holds up in threaded, dense text; Plex Mono for code answers."),
    # --- play, creative and expressive --------------------------------------------------------------
    ("Arcade", "Press Start 2P", "Rubik", "400", "400;500", "8-bit, nostalgic",
     "retro games, game jams, pixel art",
     "Press Start 2P is bitmap-style: titles and score labels only; Rubik carries rules, menus and settings."),
    ("Puzzle Box", "Fredoka", "Fredoka", "600;700", "400;500", "playful, rounded, bouncy",
     "casual games, kids' apps, quizzes",
     "One rounded family across title, buttons and scores."),
    ("Neon Grid", "Orbitron", "Exo 2", "700", "400;500", "futuristic, sci-fi",
     "esports, sci-fi games, gaming hardware",
     "Orbitron is very wide and geometric: logos and short titles only."),
    ("Doodle", "Shantell Sans", "Shantell Sans", "600", "400", "hand-drawn, informal, friendly",
     "sketching apps, stickers, kids' creative tools",
     "A marker-style face with an informal axis; far more readable than most handwriting fonts."),
    ("Mixtape", "Righteous", "Karla", "400", "400;500", "retro, groovy, fun",
     "music creation apps, record shops, retro brands",
     "Righteous has one weight with a 70s feel; keep it to the logo and big headings."),
    ("Poster", "Bebas Neue", "Work Sans", "400", "400;500", "bold, compact, cinematic",
     "trailers, events, promotions",
     "Bebas Neue is capitals only: keep lines short and give it generous letter-spacing at small sizes."),
    ("Studio Desk", "Sometype Mono", "Instrument Sans", "500", "400;500", "maker-ish, crafted, technical",
     "creative tools, generative art, design utilities",
     "A characterful mono for titles and labels only; prose stays in the sans."),
    # --- multilingual -------------------------------------------------------------------------------
    ("Arabic Pair", "Noto Kufi Arabic", "Noto Sans Arabic", "600;700", "400;500", "clear, modern, right-to-left",
     "Arabic and bilingual Arabic-English sites",
     "Set dir=\"rtl\" and lang=\"ar\"; the Noto families share metrics with Noto Sans for the Latin parts."),
    ("Hebrew Pair", "Frank Ruhl Libre", "Noto Sans Hebrew", "700", "400;500", "literary, right-to-left",
     "Hebrew and bilingual Hebrew-English sites",
     "Frank Ruhl Libre is a classic Hebrew text face; use the Noto sans for interface text."),
    ("Japanese Pair", "Noto Serif JP", "Noto Sans JP", "600;700", "400;500", "balanced, readable",
     "Japanese and bilingual sites",
     "CJK fonts are large: let Google Fonts serve them in slices, and never load all weights."),
    ("Korean Pair", "Nanum Myeongjo", "Noto Sans KR", "700", "400;500", "elegant, clear",
     "Korean and bilingual sites",
     "A serif heading over a sans body is a common Korean editorial pairing; check line-height at 1.7 or more."),
    ("Chinese Pair", "Noto Serif SC", "Noto Sans SC", "600;700", "400;500", "formal, readable",
     "Simplified Chinese sites",
     "Use the TC variants for Traditional Chinese; subset or slice to keep downloads small."),
    ("Devanagari Pair", "Tiro Devanagari Hindi", "Mukta", "400", "400;500", "warm, traditional with modern body",
     "Hindi and bilingual Hindi-English sites",
     "Mukta covers Devanagari and Latin in one family; Tiro gives headings a book-like feel."),
    ("Thai Pair", "Noto Serif Thai", "Noto Sans Thai", "600", "400;500", "clear, balanced",
     "Thai and bilingual sites",
     "Thai needs taller line-height for its vowel marks; start at 1.7."),
    ("Global Sans", "Noto Sans", "Noto Sans", "600;700", "400;500", "neutral, universal",
     "sites in many languages, multi-country businesses",
     "Noto covers most scripts with matching design, so switching language does not change the look."),
    # --- reading-first and accessible defaults -----------------------------------------------------------
    ("Plain Text", "Source Sans 3", "Source Sans 3", "700", "400;600", "plain, efficient, neutral",
     "any site where content matters more than voice",
     "A good fallback when nothing in the brief points elsewhere; still choose sizes and spacing on purpose."),
    ("Long Read", "Lora", "Lora", "600", "400;500", "warm, bookish, calm",
     "essays, guides, recipes, long blog posts",
     "Lora is a calligraphic serif for body text on screen; keep the measure to 60-75 characters."),
    ("Recipe Card", "Roboto Slab", "Roboto", "600", "400;500", "sturdy, practical, homely",
     "recipe sites, cooking classes, meal kits",
     "Slab headings stay readable from across a kitchen; Roboto handles ingredient lists."),
    ("Field Guide", "Zilla Slab", "Open Sans", "600;700", "400;600", "outdoorsy, practical, sturdy",
     "farms, outdoor centres, guides, agriculture",
     "Zilla Slab was made for Mozilla; use the bold weight for headings and Open Sans for detail."),
    ("Low Vision", "Atkinson Hyperlegible", "Lexend", "700", "400;500", "maximum legibility",
     "accessibility-first services, public health, senior services",
     "Two faces built around legibility research; set body at 18 px or more with 1.6 line-height."),
]

STACKS = {
    "SANS_SERIF": 'system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif',
    "SERIF": 'Georgia, "Times New Roman", serif',
    "MONOSPACE": 'ui-monospace, "SF Mono", Menlo, Consolas, monospace',
    "DISPLAY": 'system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif',
    "HANDWRITING": 'system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif',
}

# ---- metadata ------------------------------------------------------------------------------------


def families() -> list[str]:
    return sorted({f for p in PAIRS for f in (p[1], p[2])})


def slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())


def parse(text: str) -> dict:
    """The parts of a METADATA.pb we use."""
    get = lambda key: re.findall(rf'^{key}: "([^"]*)"', text, re.M)  # noqa: E731
    weights = {int(w) for w in re.findall(r'style: "normal"\s+weight: (\d+)', text)}
    axis = re.search(r'tag: "wght"\s+min_value: ([\d.]+)\s+max_value: ([\d.]+)', text)
    return {
        "name": get("name")[0], "designer": get("designer")[0], "license": get("license")[0],
        "category": get("category"), "subsets": [s for s in get("subsets") if s != "menu"],
        "weights": sorted(weights), "wght": [int(float(axis[1])), int(float(axis[2]))] if axis else None,
    }


def fetch() -> dict:
    meta = {}
    for fam in families():
        for d in ("ofl", "apache", "ufl"):
            try:
                with urllib.request.urlopen(RAW.format(dir=d, slug=slug(fam)), timeout=20) as r:
                    meta[fam] = parse(r.read().decode("utf-8")) | {"dir": d}
                break
            except urllib.error.HTTPError as e:
                if e.code != 404:
                    raise
        else:
            raise SystemExit(f"not on Google Fonts: {fam}")
        if meta[fam]["name"] != fam:
            raise SystemExit(f"name mismatch: {fam} vs {meta[fam]['name']}")
    return meta


def has_weight(m: dict, w: int) -> bool:
    return m["wght"][0] <= w <= m["wght"][1] if m["wght"] else w in m["weights"]


# ---- build ---------------------------------------------------------------------------------------

LICENCES = {"OFL": "SIL Open Font License 1.1", "APACHE2": "Apache 2.0", "UFL": "Ubuntu Font Licence 1.0"}


def css_url(pairs: list[tuple[str, str]]) -> str:
    parts = []
    for fam, ws in pairs:
        parts.append("family=" + urllib.parse.quote_plus(fam) + ":wght@" + ws)
    return "https://fonts.googleapis.com/css2?" + "&".join(parts) + "&display=swap"


def row(p, meta) -> dict:
    name, head, body, hw, bw, mood, best, notes = p
    mh, mb = meta[head], meta[body]
    for fam, ws, m in ((head, hw, mh), (body, bw, mb)):
        for w in ws.split(";"):
            if not has_weight(m, int(w)):
                raise SystemExit(f"{name}: {fam} has no weight {w}")
    if head == body:
        load = [(head, ";".join(sorted(set(hw.split(";")) | set(bw.split(";")), key=int)))]
    else:
        load = [(head, hw), (body, bw)]
    kind = f"{mh['category'][0].replace('_', '-').lower()} + {mb['category'][0].replace('_', '-').lower()}"
    lic = sorted({LICENCES.get(m["license"], m["license"]) for m in (mh, mb)})
    shared = set(mh["subsets"]) & set(mb["subsets"]) or set(mb["subsets"])
    scripts = sorted({s.removesuffix("-ext").title() for s in shared} - {"Latin"}) or ["-"]
    return {
        "Pairing": name, "Mood": mood, "Best For": best, "Heading Font": head, "Body Font": body,
        "Heading Weights": hw.replace(";", ", "), "Body Weights": bw.replace(";", ", "), "Kind": kind,
        "Licence": "; ".join(lic), "Extra Scripts": ", ".join(scripts),
        "Heading Stack": f'"{head}", {STACKS.get(mh["category"][0], STACKS["SANS_SERIF"])}',
        "Body Stack": f'"{body}", {STACKS.get(mb["category"][0], STACKS["SANS_SERIF"])}',
        "Google Fonts URL": css_url(load), "Notes": notes,
    }


def build() -> str:
    meta = json.loads(META.read_text(encoding="utf-8"))
    names = [p[0] for p in PAIRS]
    dupes = {n for n in names if names.count(n) > 1}
    if dupes:
        raise SystemExit(f"duplicate pairing names: {sorted(dupes)}")
    buf = io.StringIO()
    w = csv.DictWriter(buf, COLS, lineterminator="\n")
    w.writeheader()
    for p in PAIRS:
        w.writerow(row(p, meta))
    return buf.getvalue()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--fetch", action="store_true", help="refresh fonts-meta.json from github.com/google/fonts")
    ap.add_argument("--check", action="store_true", help="exit 1 if the CSV differs from a fresh build")
    a = ap.parse_args()
    if a.fetch:
        META.write_text(json.dumps(fetch(), indent=1, sort_keys=True) + "\n", encoding="utf-8")
        print(f"wrote {META.relative_to(ROOT)}")
    text = build()
    if a.check:
        same = OUT.is_file() and OUT.read_text(encoding="utf-8") == text
        print("typography.csv is up to date" if same else "typography.csv is out of date: run tools/build_typography.py")
        return 0 if same else 1
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(PAIRS)} pairings)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
