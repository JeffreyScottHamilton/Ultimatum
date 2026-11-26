#!/usr/bin/env python3
"""Build Ultimatum's own colour palettes: plugins/ultimatum/data/design-own/colors.csv.

Each business type gets a family (our own hue, chroma and mood choices, below) and a
small per-name hue shift so neighbours in a family still differ. Colours are made in
OKLCH and every text pair is pushed in lightness until it meets WCAG 2.2 contrast:
4.5:1 for text (SC 1.4.3) and 3:1 for the focus ring against the page (SC 1.4.11).
The tests re-check every pair, so a hand edit that breaks contrast fails CI.

    python3 tools/build_palettes.py            # write the CSV
    python3 tools/build_palettes.py --check    # exit 1 if the CSV is out of date

Standard library only; no network.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "plugins" / "ultimatum" / "data" / "design-own" / "colors.csv"
NAMES = ROOT / "plugins" / "ultimatum" / "data" / "design-own" / "product-types.txt"

COLS = ("Product Type", "Family", "Mode", "Background", "Foreground", "Card", "Card Foreground",
        "Border", "Ring", "Muted", "Muted Foreground", "Primary", "On Primary", "Accent", "On Accent",
        "Secondary", "On Secondary", "Destructive", "On Destructive", "Notes", "Avoid")

# ---- colour maths (OKLab: https://bottosson.github.io/posts/oklab/) -------------------------


def _lin_to_srgb(c: float) -> float:
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def _srgb_to_lin(c: float) -> float:
    # sRGB transfer curve, as WCAG 2.2 defines relative luminance
    if c <= 0.04045:
        return c / 12.92
    return ((c + 0.055) / 1.055) ** 2.4


def oklch_to_rgb(L: float, C: float, h: float) -> tuple[float, float, float] | None:
    a, b = C * math.cos(math.radians(h)), C * math.sin(math.radians(h))
    l_ = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m_ = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s_ = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    r = 4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_
    g = -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_
    bl = -0.0041960863 * l_ - 0.7034186147 * m_ + 1.7076147010 * s_
    rgb = tuple(_lin_to_srgb(x) for x in (r, g, bl))
    return rgb if all(-1e-4 <= x <= 1 + 1e-4 for x in rgb) else None


def to_hex(L: float, C: float, h: float) -> str:
    """OKLCH to hex, lowering chroma until the colour fits in sRGB."""
    while True:
        rgb = oklch_to_rgb(L, C, h)
        if rgb is not None:
            return "#" + "".join(f"{round(min(1, max(0, x)) * 255):02X}" for x in rgb)
        C -= 0.005


def luminance(hex_: str) -> float:
    r, g, b = (_srgb_to_lin(byte / 255) for byte in bytes.fromhex(hex_.lstrip("#")))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: str, b: str) -> float:
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def fit(L: float, C: float, h: float, against: str, need: float) -> str:
    """Move lightness away from `against` until the colour reaches `need` contrast."""
    step = -0.01 if luminance(against) > 0.18 else 0.01
    while 0 <= L <= 1:
        c = to_hex(L, C, h)
        if contrast(c, against) >= need:
            return c
        L += step
    raise ValueError(f"no colour at hue {h} reaches {need}:1 on {against}")


def on(color: str, dark: str, light: str = "#FFFFFF") -> str:
    """The text colour for a fill: white or the family's dark ink, whichever is clearer."""
    return light if contrast(color, light) >= contrast(color, dark) else dark


# ---- families: our own choices ---------------------------------------------------------------
# name: (keywords, primary hue, primary chroma, accent hue, neutral hue, mode, notes, avoid)
FAMILIES: list[tuple[str, tuple[str, ...], float, float, float, float, str, str, str]] = [
    ("local trades", ("plumb", "electric", "home services", "construction", "parking", "automotive",
                      "car dealership", "mechanic", "auto repair", "roof", "hvac", "locksmith", "moving", "pest",
                      "painter", "clean", "landscap", "garden", "handyman", "logistics", "delivery", "ride", "transit", "road trip"),
     250, 0.14, 65, 250, "light",
     "A dependable blue or navy for the brand, with one warm signal colour kept for the phone number "
     "and the quote button so the next step is easy to spot on a phone in daylight.",
     "Low-contrast grey text on photos of vans or sites; more than one bright colour competing with the call button."),
    ("health", ("health", "clinic", "medical", "dental", "pharmacy", "patient", "telemedicine",
                "senior", "medication", "physio", "chiropract", "optician", "pill", "biotech", "life sciences", "veterinary"),
     195, 0.10, 150, 200, "light",
     "Calm teal or blue-green reads as clean without the cold hospital white; keep the accent for booking. "
     "Large body text and strong contrast help older visitors and people reading on the move.",
     "Red for anything but errors or warnings; tiny pale text; stock-photo blue gradients."),
    ("wellbeing", ("mental health", "therapist", "meditation", "mindfulness", "yoga", "sleep", "mood", "beauty",
                   "spa", "wellness", "salon", "barber", "nail", "massage", "tattoo", "diary", "journal", "white noise", "period", "cycle", "habit"),
     160, 0.07, 30, 120, "light",
     "Soft sage or eucalyptus with a muted warm accent: quiet enough to rest the eye, with enough "
     "contrast that labels and buttons are never faint.",
     "Pastel text on pastel fills; pulsing or glowing calls to action; a cream page used only because it feels soft."),
    ("food", ("restaurant", "caterer", "farm", "agriculture", "market stall", "food", "bakery", "cafe", "brewery", "winery", "recipe", "cooking",
              "grocery", "calorie", "nutrition", "fasting", "water", "hydration"),
     50, 0.13, 140, 60, "light",
     "Warm tomato, paprika or roast-coffee tones that sit well next to food photos, with a fresh green "
     "accent for menus, opening hours and the order or book button.",
     "Terracotta on cream as an automatic pick; text laid over busy food photos without a solid backing."),
    ("money", ("bank", "finance", "fintech", "insurance", "invoice", "billing", "expense", "bill split",
               "auction", "crowdfunding", "grant", "funding", "personal finance", "e-signature"),
     255, 0.11, 160, 250, "light",
     "Deep, steady blue for trust, a green kept strictly for positive amounts and confirmations, and red "
     "only for losses and errors, so colour never contradicts the numbers.",
     "Green or red as decoration; gold or crypto neon on a regulated product; colour as the only signal for gain or loss."),
    ("dark tools", ("developer", "ide", "api", "cybersecurity", "vpn", "password", "status page",
                    "incident", "feature flag", "config", "rpa", "automation", "quantum", "coding",
                    "open source", "changelog", "drone"),
     265, 0.15, 150, 260, "dark",
     "A dark neutral workspace with one clear signal colour for the main action and a second for "
     "success states; tuned for long sessions and code blocks.",
     "Neon on black for body text; several glowing accents; purple-to-blue gradients as the brand."),
    ("data", ("dashboard", "analytics", "crm", "inventory", "stock", "gis", "map", "earth observation",
              "satellite", "iot", "smart home", "energy", "climate", "ev", "charging", "space", "aerospace",
              "survey", "form builder", "productivity", "calendar", "scheduling", "saas", "b2b"),
     240, 0.13, 175, 245, "light",
     "A neutral canvas with one brand blue, so chart colours and status colours keep their meaning; "
     "keep greys for chrome and save saturation for data.",
     "Brand colours reused as chart series; many tints of one hue standing in for real hierarchy."),
    ("learning", ("educational", "course", "e-learning", "lms", "bootcamp", "flashcard", "study",
                  "language", "kids", "abc", "math", "micro-credentials", "badges", "trivia", "quiz",
                  "instrument", "academic", "tutor", "driving school", "research", "university", "citizen science", "wiki",
                  "knowledge base", "documentation"),
     230, 0.13, 85, 230, "light",
     "A clear, friendly blue with a sunny accent for progress and rewards; strong contrast for long "
     "reading and for students on cheap screens.",
     "Rainbow palettes on every element; yellow text on white; colour-only progress cues."),
    ("care and family", ("childcare", "daycare", "parenting", "baby", "family", "chores", "pet",
                         "couple", "relationship", "gift", "wishlist", "dating", "wedding"),
     15, 0.11, 200, 40, "light",
     "Warm rose or coral with a cool accent: friendly and human without becoming sugary; check the "
     "coral against white, where it often fails.",
     "Baby pastels for text; heart shapes and soft glows as the main decoration."),
    ("active", ("fitness", "gym", "running", "cycling", "sports", "personal trainer"),
     140, 0.17, 55, 150, "light",
     "An energetic green or lime-leaning primary with a hot accent for class times and sign-up; keep "
     "contrast high, since people check these pages mid-workout or outdoors.",
     "Neon on black as the only idea; red-orange gradients; tiny timetable text."),
    ("professional", ("legal", "law", "patent", "ip database", "consultant", "coach", "accountant",
                      "bookkeep", "tax", "counsel"),
     245, 0.08, 70, 240, "light",
     "A sober ink blue or deep green with a single warm accent for the consultation button; let type "
     "and spacing do the work so the firm reads as careful.",
     "Gavel-and-gold clichés; stock-photo handshakes tinted blue; grey body text that is too light."),
    ("utility", ("notes", "writing", "weather", "timer", "pomodoro", "scanner", "document manager",
                 "voice recorder", "memo", "translator", "calculator", "converter", "alarm", "clock",
                 "file manager", "transfer", "email", "collaboration", "remote work", "no-code",
                 "low-code", "design system", "component library", "signage", "kiosk", "emergency",
                 "sos", "safety"),
     220, 0.12, 30, 230, "light",
     "Mostly neutral, so the tool disappears behind the content, with one action colour; emergency and "
     "warning colours are reserved for real alerts.",
     "Decorative colour on every panel; alert red or orange used for branding."),
    ("luxury", ("luxury", "premium", "hotel", "hospitality", "jewel", "e-commerce luxury"),
     60, 0.06, 75, 70, "light",
     "Restraint: deep ink, a single warm metal or stone accent used sparingly, and plenty of space. "
     "The photos carry the colour.",
     "Gold gradients, glitter or shine effects; near-black with one acid accent as a default."),
    ("culture", ("museum", "gallery", "theater", "cinema", "music", "podcast", "video", "streaming",
                 "ott", "photography", "generative art", "art", "magazine", "blog", "news", "media",
                 "newsletter", "book", "reading", "creative agency", "portfolio", "architecture",
                 "interior", "home decoration"),
     20, 0.15, 260, 30, "light",
     "One confident editorial colour against a mostly neutral page, so artwork and photos stay the "
     "focus; use the accent for links and the ticket or subscribe button.",
     "Colour washes over artwork; several loud colours fighting the images."),
    ("community", ("non-profit", "charity", "church", "religious", "government", "public service",
                   "civic", "club", "forum", "discussion", "q&a", "community", "membership",
                   "social", "chat", "messaging", "anonymous", "confession", "local events", "events",
                   "coworking", "conference", "symposium", "ticketing", "box office", "event"),
     145, 0.12, 40, 140, "light",
     "An open, grounded green or a clear civic blue-green, with a warm accent for donate, join or "
     "register; plain enough for public trust.",
     "Emergency red for ordinary buttons; low-contrast palettes on public-service pages that must meet WCAG."),
    ("commerce", ("e-commerce", "marketplace", "classifieds", "buy-sell", "subscription box",
                  "florist", "plant", "wardrobe", "outfit", "digital products", "downloads", "review",
                  "testimonial", "directory", "listing", "real estate", "property", "travel", "tourism",
                  "airline", "hyperlocal", "booking", "appointment", "job", "recruitment", "freelancer",
                  "resume", "cv", "marketing agency", "link-in-bio"),
     280, 0.12, 50, 270, "light",
     "A distinct brand colour for identity and one high-visibility action colour for add to cart, book "
     "or apply; prices and stock notes in plain dark text.",
     "The brand hue on every button so the buy action no longer stands out; red sale badges on every item."),
    ("play", ("game", "gaming", "puzzle", "arcade", "retro", "idle", "clicker", "card", "board",
              "word", "crossword", "meme", "sticker", "wallpaper", "theme", "avatar", "photo editor",
              "filters", "short video", "drawing", "sketching", "beat maker", "music creation",
              "nft", "web3", "crypto", "spatial", "creator economy"),
     300, 0.18, 85, 290, "dark",
     "Saturated colour is welcome here, but give each colour one job (action, reward, danger) and keep "
     "text plain so menus stay readable.",
     "Every element glowing; text on animated backgrounds; colour as the only cue for game states."),
]
DEFAULT = ("general", (), 250, 0.12, 40, 250, "light",
           "A clear brand colour with one accent for the main action, on a neutral page.",
           "Gradients as the brand; many tints of one colour instead of a few chosen ones.")

DANGER_HUE = 27  # a red that stays red at any lightness used below


def family(name: str):
    low = name.lower()
    best, score = DEFAULT, 0
    for fam in FAMILIES:
        s = max((len(k) for k in fam[1] if k in low), default=0)
        if s > score:
            best, score = fam, s
    return best


def jitter(name: str, span: float) -> float:
    """A stable shift in [-span, span] from the name, so family members differ."""
    n = int(hashlib.sha256(name.encode()).hexdigest()[:8], 16) / 0xFFFFFFFF
    return (n * 2 - 1) * span


def palette(name: str) -> dict[str, str]:
    fam, _, h, c, ah, nh, mode, notes, avoid = family(name)
    h, ah = (h + jitter(name, 14)) % 360, (ah + jitter(name[::-1], 12)) % 360
    gap = (h - DANGER_HUE + 180) % 360 - 180
    if abs(gap) < 22:  # keep the brand clear of the error red
        h = (DANGER_HUE + (44 - abs(gap)) * (1 if gap >= 0 else -1)) % 360  # mirror out of the band
    if mode == "dark":
        bg, fg = to_hex(0.18, 0.015, nh), to_hex(0.95, 0.008, nh)
        card, muted, border = to_hex(0.22, 0.018, nh), to_hex(0.26, 0.018, nh), to_hex(0.34, 0.02, nh)
        primary = fit(0.72, c, h, bg, 4.5)
        accent = fit(0.80, c * 0.9, ah, bg, 4.5)
        mfg = fit(0.70, 0.015, nh, muted, 4.5)
        dest = fit(0.66, 0.19, DANGER_HUE, bg, 4.5)
    else:
        bg, fg = to_hex(0.99, 0.004, nh), to_hex(0.22, 0.02, nh)
        card, muted, border = "#FFFFFF", to_hex(0.955, 0.008, nh), to_hex(0.88, 0.012, nh)
        primary = fit(0.52, c, h, "#FFFFFF", 4.5)
        accent = to_hex(0.78, c * 0.9, ah)
        mfg = fit(0.50, 0.015, nh, muted, 4.5)
        dest = fit(0.55, 0.19, DANGER_HUE, "#FFFFFF", 4.5)
    secondary = to_hex(0.30 if mode == "dark" else 0.94, 0.03, h)
    ring = primary if contrast(primary, bg) >= 3 else fit(0.5, c, h, bg, 3)
    return {
        "Product Type": name, "Family": fam, "Mode": mode,
        "Primary": primary, "On Primary": on(primary, fg if mode == "light" else bg),
        "Secondary": secondary, "On Secondary": fg,
        "Accent": accent, "On Accent": on(accent, fg if mode == "light" else bg),
        "Background": bg, "Foreground": fg, "Card": card, "Card Foreground": fg,
        "Muted": muted, "Muted Foreground": mfg, "Border": border,
        "Destructive": dest, "On Destructive": on(dest, fg if mode == "light" else bg),
        "Ring": ring, "Notes": notes, "Avoid": avoid,
    }


def build() -> str:
    names = [n.strip() for n in NAMES.read_text(encoding="utf-8").splitlines() if n.strip()]
    buf = io.StringIO()
    w = csv.DictWriter(buf, COLS, lineterminator="\n")
    w.writeheader()
    for n in names:
        w.writerow(palette(n))
    return buf.getvalue()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="exit 1 if the CSV differs from a fresh build")
    text = build()
    if ap.parse_args().check:
        same = OUT.is_file() and OUT.read_text(encoding="utf-8") == text
        print("colors.csv is up to date" if same else "colors.csv is out of date: run tools/build_palettes.py")
        return 0 if same else 1
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({text.count(chr(10)) - 1} palettes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
