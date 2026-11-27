#!/usr/bin/env python3
"""Lint pages, stylesheets and component files for the checkable design tells.

Standard library only, no network. Reads .html/.htm pages with the local .css
they link, standalone .css, and component files (.jsx/.tsx/.vue/.svelte/
.astro), whose class strings (including cn()/clsx() arguments and Tailwind
utilities) and <style> blocks are read the same way. Each rule names the row it
checks in slop-tells.csv (this folder) or ../hallmark/gates.csv. A hit is
evidence to look at, not a verdict; the judged rows still need a reviewer.

A comment containing "page-lint: allow RULE[,RULE]: reason" waives those rules
for that page and the stylesheets it links. A waiver without a reason is itself
a finding and waives nothing.

Usage:
    page_lint.py PATH [PATH ...] [--only RULE,RULE] [--genre G]
                 [--format text|json|github] [--json] [--rules]
Exit 1 when anything is found, 0 when clean, 2 on bad arguments.
"""
import argparse
import colorsys
import json
import math
import os
import re
import sys
from html.parser import HTMLParser

RULES = {
    # rule: (severity, tell id, note)
    # colour
    "purple-gradient": ("medium", "classic-purple-gradient / gate 2a",
                        "gradient through purple, violet or indigo; pick one anchor hue and use solid colour"),
    "gradient-text": ("medium", "gradient-text / gate 2b",
                      "gradient-filled text; use one solid colour and weight for emphasis"),
    "pure-black-white": ("low", "gate 7a",
                         "pure #000 or #fff set directly on an element rather than in :root tokens; shift it slightly toward the brand hue"),
    "pure-black-surface": ("low", "gate 7b",
                           "a surface token is pure black or white; tint the paper toward the anchor hue"),
    "framework-swatch": ("medium", "gate 74",
                         "a framework default swatch such as indigo-500 or slate-900 picked straight from the box; derive the palette from the brand"),
    "grey-neutral": ("low", "gate 22",
                     "zero-chroma grey on a page that has an anchor hue; give every neutral a trace of that hue"),
    "colour-literal": ("low", "gate 48",
                       "colour or font-family literals outside the token block; move them into tokens and refer to those"),
    "low-contrast": ("high", "gate 40",
                     "text colour against its background is under 4.5:1 (3:1 for large text)"),
    "gray-on-colour": ("medium", "gate 41",
                       "grey text on a saturated fill reads as dirty; use a tint or shade of the fill"),
    "cream-look": ("medium", "cream-palette / gate 65",
                   "cream paper, serif display and a clay accent together: the stock look; move one axis"),
    # type
    "system-font-main": ("medium", "classic-system-font",
                         "system font stack is the main face; choose and name a pairing"),
    "default-font": ("low", "overused-font / gate 1",
                     "a very common default face is the display or body font; check it was chosen on purpose"),
    "too-many-fonts": ("medium", "gate 37",
                       "more than three font families on one page"),
    "flat-type-scale": ("medium", "flat-type-hierarchy",
                        "h1 and h2 sizes too close to read as two levels (ratio under 1.2)"),
    "oversized-h1": ("medium", "oversized-h1",
                     "display size so large the headline becomes texture (120px, 10vw or a clamp past 128px)"),
    "italic-word": ("low", "gate 38i",
                    "one italic word inside an upright heading"),
    "italic-display": ("medium", "italic-serif-display / gate 38ii",
                       "headings set in italic as the house style"),
    "caps-tight-leading": ("medium", "gate 55a",
                           "uppercase heading with line-height under 1.0 collides when it wraps"),
    "mono-costume": ("low", "gate 64",
                     "monospace on labels or meta that are not code, figures or measurements"),
    "tracked-caps": ("low", "gate 67",
                     "small uppercase label with wide letter-spacing; sentence case one step down reads better"),
    "extreme-tracking": ("medium", "gate 75",
                         "letter-spacing of -0.05em or tighter; glyphs start to touch"),
    "tiny-text": ("medium", "gate 75",
                  "text under 12px"),
    "tight-leading": ("medium", "gate 75",
                      "body text with line-height under 1.3"),
    "prose-width": ("medium", "gate 25",
                    "running text measure outside 45 to 75 characters"),
    "justified-text": ("low", "gate 75",
                       "justified text on the web leaves rivers; align left"),
    "all-caps-body": ("medium", "gate 75",
                      "uppercase applied to running text"),
    "heading-order": ("medium", "accessibility",
                      "heading levels skip (h2 to h4) or more than one h1"),
    "display-no-wrap": ("low", "gate 50",
                        "large display heading with no overflow-wrap; a long word overflows at 320px"),
    # layout
    "uniform-radius": ("medium", "classic-uniform-radius",
                       "one border-radius on almost everything; set radii by element role"),
    "left-border-card": ("medium", "classic-left-border-card / border-accent-on-rounded",
                         "thick coloured left border on a rounded box"),
    "nested-cards": ("medium", "nested-cards / gate 4",
                     "a card inside a card; flatten with spacing or a rule"),
    "hero-vh": ("medium", "gate 6a",
                "hero sized with vh; size it by its content and let the next section show"),
    "raw-spacing": ("low", "gate 24a",
                    "raw padding, margin or gap values although spacing tokens exist"),
    "off-scale-spacing": ("low", "gate 24b",
                          "spacing values off the 4px scale (three nudges are tolerated)"),
    "horizontal-scroll": ("high", "gate 34",
                          "100vw widths or overflow-x on html/body: the page scrolls sideways or hides that it would"),
    "bare-fr-images": ("low", "gate 50",
                       "image grid tracks set to bare 1fr; use minmax(0, 1fr) so wide media cannot stretch them"),
    "double-sticky": ("medium", "gate 56",
                      "two elements sticky at top 0; one slides under the other"),
    "wordy-hero": ("medium", "gate 58",
                   "hero carries too much text (about 80 words, or three or more paragraphs)"),
    "cramped-padding": ("low", "gate 59",
                        "buttons or cards with under 8px padding"),
    "icon-card-trio": ("medium", "classic-three-column-grid / icon-tile-stack / gate 3",
                       "a row of equal cards, each an icon above a heading"),
    "empty-slots": ("medium", "gate 68",
                    "more than five empty image or content slots: a wireframe shipped as a page"),
    "fake-chrome": ("medium", "gate 47a",
                    "hand-drawn browser bar or window dots"),
    "device-frame": ("low", "gate 47b",
                     "a phone, laptop, terminal or editor frame; one frame with real content inside is fine"),
    # effects
    "glow": ("medium", "dark-glow / radial-halo / radial-spotlight-glow / gate 29",
             "large coloured glow, blurred orb or radial halo; use plain contrast"),
    "frosted-glass": ("medium", "judge-frosted-glass",
                      "backdrop blur used on several surfaces; keep it to one layer whose depth is explained"),
    "hard-offset-shadow": ("low", "gate 29",
                           "hard offset shadow with no blur (the sticker look)"),
    "thin-border-wide-shadow": ("low", "gate 29",
                                "hairline border plus a wide soft shadow on the same box; pick one edge"),
    "pattern-background": ("low", "classic-blobs-waves",
                           "repeating stripes or a drawn grid as background texture"),
    "organic-shape": ("low", "classic-blobs-waves / shape-assembled-illustration",
                      "blob radius or many-point clip-path used as decoration"),
    "marquee": ("medium", "marquee",
                "scrolling strip (marquee element or endless horizontal animation)"),
    # copy
    "generic-copy": ("high", "classic-generic-hero-copy / marketing-buzzword / gate 19",
                     "stock marketing phrase; say what it is and who it is for"),
    "theater-phrase": ("medium", "theater-slop-phrase",
                       "stagey filler phrase; cut it and state the point"),
    "rebuttal-cadence": ("medium", "aphoristic-cadence / gate 19",
                         "the 'not X, it's Y' or 'No X. No Y.' cadence"),
    "em-dash": ("low", "gate 19",
                "two or more em or en dashes in the copy; use commas, colons or full stops"),
    "template-punctuation": ("low", "gate 63",
                             "dot-separated meta lines, an arrow stuck on the end of a link, or CAPS - dash labels"),
    "needs-source": ("high", "judge-fake-stats / judge-fake-testimonials / gate 46a",
                     "a metric, rating, customer count or logo wall with no source; use the owner's real number or cut it"),
    "numbered-labels": ("low", "gate 54",
                        "01 / 02 / 03 section numbers as decoration"),
    "stock-newsletter": ("low", "gate 85",
                         "page ends on an email sign-up; check that subscribing is the page's job"),
    "vague-cta": ("medium", "judge-vague-cta",
                  "every call to action is generic (Get started, Learn more); name what the click gets"),
    "eyebrow-chip": ("low", "hero-eyebrow-chip / kicker-above-heading / gate 54",
                     "short pill or label right above the h1"),
    "emoji-heading": ("medium", "classic-emoji-design",
                      "emoji in a heading"),
    "emoji-icon": ("medium", "classic-emoji-design / gate 30a",
                   "emoji standing in for an icon"),
    "placeholder": ("high", "judge-stock-hero / gate 19",
                    "placeholder text, name or image left in the page"),
    # motion
    "transition-all": ("medium", "gate 10a",
                       "transition: all, or animating top/left/width/height; animate transform and opacity"),
    "layout-transition": ("low", "gate 10b",
                          "transition on margin or padding moves the layout every frame"),
    "bounce-easing": ("medium", "gate 12",
                      "bounce or overshoot easing on interface state"),
    "focus-fade": ("medium", "gate 15",
                   "focus ring that fades in; show focus instantly"),
    "autoplay-carousel": ("medium", "gate 18",
                          "auto-rotating content with no pause control"),
    "no-reduced-motion": ("high", "gate 27",
                          "animation or transform transition with no prefers-reduced-motion fallback"),
    "hidden-at-rest": ("high", "gate 62",
                       "content hidden until a script reveals it; the page ships blank when the script fails"),
    "pulsing-dot": ("low", "gate 63",
                    "decorative pulsing status dot"),
    "blinking-cursor": ("low", "gate 63",
                        "fake blinking caret or typing animation"),
    # access and states
    "img-no-alt": ("medium", "accessibility",
                   "img without an alt attribute (use alt=\"\" for decoration)"),
    "focus-removed": ("high", "gate 26a",
                      "outline removed with no focus-visible replacement"),
    "no-focus-style": ("medium", "gate 26a",
                       "the page has links or controls but no focus or focus-visible style at all"),
    "missing-states": ("low", "gate 26b",
                       "buttons are styled but have no :active (or no :disabled where real controls exist)"),
    "input-focus-border": ("low", "gate 39a",
                           "field focus shown only by changing the border; add a ring that does not shift layout"),
    "control-height": ("low", "gate 39b",
                       "button or field height outside 32 to 56px"),
    "unlabelled-svg": ("low", "gate 33",
                       "inline svg or canvas with no label and no aria-hidden"),
    "autoplay-sound": ("high", "gate 28a",
                       "video autoplays without muted"),
    "lazy-hero-image": ("medium", "gate 28a",
                        "loading=lazy on the first or hero image delays the largest paint"),
    "video-poster": ("low", "gate 28b",
                     "video with no poster frame"),
    "form-no-action": ("medium", "gate 70",
                       "form with no action; make sure submitting sends something before showing success"),
    # images and icons
    "broken-image": ("high", "gate 76",
                     "image with an empty or # source, or a local file that does not exist"),
    "stock-photo": ("low", "gate 76",
                    "stock-site image and nobody credited; confirm the licence"),
    "two-icon-libraries": ("low", "gate 30b",
                           "two or more icon libraries on one page"),
    # waivers
    "waiver-no-reason": ("low", "linter",
                         "page-lint waiver with no reason or an unknown rule; it waives nothing"),
}

GENRE_EXEMPT = {
    "atmospheric": {"glow", "frosted-glass", "pattern-background"},
    "playful": {"bounce-easing", "organic-shape", "hard-offset-shadow"},
    "modern-minimal": {"grey-neutral", "pure-black-surface", "pure-black-white"},
    "editorial": {"italic-display", "italic-word"},
}

GENERIC_PHRASES = (
    "welcome to", "unlock the power", "all-in-one", "all in one solution", "seamless",
    "revolutioni", "supercharge", "next-generation", "next generation", "game-changer",
    "game changer", "elevate your", "cutting-edge", "cutting edge", "empower your",
    "take your business to the next level", "world-class", "best-in-class", "leverage the power",
    "harness the power", "transform the way", "in today's fast-paced", "in today’s fast-paced",
    "reimagine", "the future of", "say goodbye to", "look no further", "effortless",
    "streamline your", "boost your", "skyrocket", "unleash", "in a world where",
    "whether you're a", "whether you’re a", "we've got you covered", "at the intersection of",
    "redefine", "built for the modern", "made simple", "powerful yet simple",
    "designed to help you", "one platform", "your one-stop", "state-of-the-art",
)
THEATER_PHRASES = (
    "let's dive in", "let’s dive in", "here's the thing", "here’s the thing", "buckle up",
    "the best part?", "spoiler:", "plot twist", "but wait", "here's the kicker",
    "here’s the kicker", "secret sauce", "let that sink in", "where the magic happens",
    "say hello to", "ready to level up", "ready to take", "imagine a world",
)
REBUTTAL = (
    re.compile(r"\bnot (?:just |only |merely |simply )?(?:a |an |the |about )?[\w'’-]+(?: [\w'’-]+){0,2}\s*[,;:.—–-]+\s*(?:it'?s|it’s|it is|this is|we'?re|we’re|but)\b"),
    re.compile(r"\bno [\w'’-]+\.\s+no [\w'’-]+\."),
    re.compile(r"\bless [\w'’-]+[.,]?\s+more [\w'’-]+"),
    re.compile(r"\b[\w'’-]+ isn'?t [\w'’ -]+\. it'?s\b"),
)
VAGUE_CTA = {"get started", "learn more", "start now", "sign up", "try it", "try now",
             "click here", "discover more", "explore", "read more", "start free"}
DEFAULT_FONTS = ("inter", "poppins", "montserrat", "roboto", "open sans", "lato", "arial", "helvetica")
SYSTEM_FIRST = ("system-ui", "-apple-system", "blinkmacsystemfont", "ui-sans-serif", "segoe ui")
GENERIC_FAMILIES = {"serif", "sans-serif", "monospace", "cursive", "fantasy", "system-ui", "inherit",
                    "initial", "unset", "ui-serif", "ui-sans-serif", "ui-monospace", "ui-rounded",
                    "-apple-system", "blinkmacsystemfont", "emoji", "math", "fangsong"}
MONO_FONTS = ("monospace", "ui-monospace", "jetbrains mono", "ibm plex mono", "fira code", "fira mono",
              "space mono", "sf mono", "menlo", "monaco", "consolas", "courier", "geist mono",
              "dm mono", "roboto mono", "source code pro", "ubuntu mono", "berkeley mono")
SERIF_FONTS = ("fraunces", "playfair", "instrument serif", "dm serif", "cormorant", "libre baskerville",
               "eb garamond", "garamond", "newsreader", "lora", "georgia", "times", "merriweather",
               "source serif", "pt serif", "crimson", "spectral", "literata", "baskerville", "caslon")
PLACEHOLDER = re.compile(
    r"lorem ipsum|placehold\.co|placeholder\.com|via\.placeholder|dummyimage\.com|picsum\.photos"
    r"|\[your (?:company|name|product)\]|\bacme\b|\bjohn doe\b|\bjane doe\b|your company name|company name here",
    re.I)
EMOJI = re.compile("[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F000-\U0001F2FF]")
NAMED_PURPLE = re.compile(r"\b(purple|violet|indigo|blueviolet|darkviolet|mediumpurple|rebeccapurple|fuchsia|magenta|orchid)\b", re.I)
HEX = re.compile(r"#([0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})\b")
COLOUR_FN = re.compile(r"\b(?:rgba?|hsla?|oklch|oklab|lab|lch|hwb|color)\([^()]*\)", re.I)
NAMED_COLOURS = {
    "black": (0, 0, 0), "white": (255, 255, 255), "red": (255, 0, 0), "green": (0, 128, 0),
    "blue": (0, 0, 255), "gray": (128, 128, 128), "grey": (128, 128, 128), "silver": (192, 192, 192),
    "purple": (128, 0, 128), "violet": (238, 130, 238), "indigo": (75, 0, 130), "orange": (255, 165, 0),
    "yellow": (255, 255, 0), "pink": (255, 192, 203), "navy": (0, 0, 128), "teal": (0, 128, 128),
    "magenta": (255, 0, 255), "fuchsia": (255, 0, 255), "cyan": (0, 255, 255), "aqua": (0, 255, 255),
    "lightgray": (211, 211, 211), "lightgrey": (211, 211, 211), "darkgray": (169, 169, 169),
    "darkgrey": (169, 169, 169), "gainsboro": (220, 220, 220), "whitesmoke": (245, 245, 245),
}
NAMED_RE = re.compile(r"(?<![\w-])(" + "|".join(NAMED_COLOURS) + r")(?![\w-])", re.I)
FRAMEWORK_HEX = {"#6366f1", "#4f46e5", "#4338ca", "#8b5cf6", "#7c3aed", "#6d28d9", "#a855f7",
                 "#9333ea", "#0f172a", "#1e293b", "#020617", "#3b82f6", "#2563eb", "#111827", "#18181b",
                 "#09090b", "#ec4899", "#06b6d4"}
CHROME_HEX = {"#ff5f56", "#ff5f57", "#ffbd2e", "#febc2e", "#27c93f", "#28c840", "#28ca42"}
COLOUR_PROPS = ("color", "background", "background-color", "border-color", "fill", "stroke",
                "outline-color", "border", "border-top", "border-bottom", "border-left", "border-right",
                "box-shadow", "text-shadow", "background-image", "caret-color", "accent-color",
                "text-decoration-color", "column-rule-color")
CARD_CLASS = re.compile(r"(^|[\s_-])card(s)?($|[\s_-])", re.I)
CHIP_CLASS = re.compile(r"eyebrow|kicker|badge|pill|chip|tag|overline|label", re.I)
HERO_CLASS = re.compile(r"(^|[\s_-])(hero|banner|masthead|splash|jumbotron)($|[\s_-])", re.I)
HERO_SEL = re.compile(r"hero|banner|masthead|splash|jumbotron|landing|\.cover\b", re.I)
LABEL_SEL = re.compile(r"label|caption|meta|eyebrow|kicker|tag|badge|chip|overline|\bth\b|nav|\bsmall\b|date|byline|category", re.I)
CODEISH_SEL = re.compile(r"\bcode\b|\bpre\b|\bkbd\b|\bsamp\b|price|stat|figure|metric|number|\btime\b|data|num", re.I)
HEADING_SEL = re.compile(r"(^|[\s>+~,(])h[1-3]\b|display|headline|title|hero", re.I)
PROSE_SEL = re.compile(r"(^|[\s>+~,])(p|article|blockquote|li|dd)\b|prose|lead|\.content|\.text|\.body|\bmain\b", re.I)
BODY_SEL = re.compile(r"^(body|html|:root)$|(^|[\s>+~,])(p|li|article|blockquote|dd)\b|prose|lead\b", re.I)
REVEAL_SEL = re.compile(r"reveal|fade-?(in|up)|animate-on-scroll|\baos|scroll-anim|appear|in-?view|wow\b|slide-?in|\bsr-", re.I)
BUTTON_SEL = re.compile(r"(^|[\s>+~,.])(button|btn|cta)\b", re.I)
FIELD_SEL = re.compile(r"(^|[\s>+~,.])(input|textarea|select|field)\b", re.I)
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
SKIP_TAGS = ("script", "noscript", "template")
PAGE_EXT = (".html", ".htm")
COMPONENT_EXT = (".jsx", ".tsx", ".vue", ".svelte", ".astro")
WAIVER = re.compile(r"page-lint:\s*allow\s+([a-z][a-z0-9-]*(?:\s*,\s*[a-z][a-z0-9-]*)*)\s*(?::([^\n]*))?")
ICON_IMPORTS = (("lucide-react", "lucide"), ("lucide-vue", "lucide"), ("lucide-svelte", "lucide"),
                ("react-icons", "react-icons"), ("@heroicons/", "heroicons"), ("@phosphor-icons/", "phosphor"),
                ("@tabler/icons", "tabler"), ("@radix-ui/react-icons", "radix"), ("react-feather", "feather"),
                ("@fortawesome/", "fontawesome"), ("@mui/icons-material", "material"),
                ("iconoir-react", "iconoir"), ("@iconify/", "iconify"))
ICON_LINKS = (("font-awesome", "fontawesome"), ("fontawesome", "fontawesome"), ("material+icons", "material"),
              ("material+symbols", "material"), ("bootstrap-icons", "bootstrap"), ("remixicon", "remix"),
              ("phosphor", "phosphor"), ("tabler-icons", "tabler"), ("boxicons", "boxicons"),
              ("ionicons", "ionicons"), ("lucide", "lucide"), ("feather", "feather"))
PAID_STOCK = ("shutterstock.com", "istockphoto.com", "gettyimages.", "stock.adobe.com", "depositphotos.com",
              "dreamstime.com", "123rf.com", "alamy.com")
FREE_STOCK = ("images.unsplash.com", "unsplash.com/photos", "plus.unsplash.com", "images.pexels.com",
              "cdn.pixabay.com", "pixabay.com/get")
TW_SIZE = {"xs": 12, "sm": 14, "base": 16, "lg": 18, "xl": 20, "2xl": 24, "3xl": 30, "4xl": 36,
           "5xl": 48, "6xl": 60, "7xl": 72, "8xl": 96, "9xl": 128}


# ---------------------------------------------------------------- colour

def to_rgb(c):
    """Return (r, g, b, alpha) with channels 0-255 for a colour literal, or None."""
    c = c.strip().lower()
    m = HEX.fullmatch(c)
    if m:
        h = m.group(1)
        if len(h) in (3, 4):
            h = "".join(ch * 2 for ch in h)
        a = int(h[6:8], 16) / 255 if len(h) == 8 else 1.0
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (a,)
    if c in NAMED_COLOURS:
        return NAMED_COLOURS[c] + (1.0,)
    m = re.fullmatch(r"(rgba?|hsla?|oklch)\((.*)\)", c)
    if not m:
        return None
    fn, args = m.group(1), m.group(2)
    parts = [p for p in re.split(r"[\s,/]+", args.strip()) if p]
    if len(parts) < 3:
        return None
    alpha = 1.0
    if len(parts) >= 4:
        alpha = _num(parts[3], 1.0)
    try:
        if fn.startswith("rgb"):
            ch = [(_num(p, 255.0) if p.endswith("%") else float(p)) for p in parts[:3]]
            return tuple(max(0, min(255, round(x))) for x in ch) + (alpha,)
        if fn.startswith("hsl"):
            h = float(parts[0].replace("deg", "")) % 360
            s = float(parts[1].rstrip("%")) / 100
            l = float(parts[2].rstrip("%")) / 100
            r, g, b = colorsys.hls_to_rgb(h / 360, l, s)
            return (round(r * 255), round(g * 255), round(b * 255), alpha)
        L = _num(parts[0], 1.0) if parts[0].endswith("%") else float(parts[0])
        C = float(parts[1].rstrip("%")) * (0.004 if parts[1].endswith("%") else 1)
        H = math.radians(float(parts[2].replace("deg", "")))
        a_, b_ = C * math.cos(H), C * math.sin(H)
        l_ = (L + 0.3963377774 * a_ + 0.2158037573 * b_) ** 3
        m_ = (L - 0.1055613458 * a_ - 0.0638541728 * b_) ** 3
        s_ = (L - 0.0894841775 * a_ - 1.2914855480 * b_) ** 3
        lin = (4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_,
               -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_,
               -0.0041960863 * l_ - 0.7034186147 * m_ + 1.7076147010 * s_)
        out = []
        for x in lin:
            x = max(0.0, min(1.0, x))
            x = 12.92 * x if x <= 0.0031308 else 1.055 * x ** (1 / 2.4) - 0.055
            out.append(round(x * 255))
        return tuple(out) + (alpha,)
    except ValueError:
        return None


def _num(p, scale):
    p = p.strip()
    try:
        if p.endswith("%"):
            return float(p[:-1]) / 100 * scale
        return float(p)
    except ValueError:
        return scale


def hls(rgb):
    h, l, s = colorsys.rgb_to_hls(*(x / 255 for x in rgb[:3]))
    return h * 360, l, s


def hue_sat(colour):
    """(hue degrees, saturation 0-1) for a colour literal, or None; near-white/black count as unsaturated."""
    rgb = to_rgb(colour)
    if not rgb:
        return None
    h, l, s = hls(rgb)
    return h, s if 0.05 < l < 0.95 else 0.0


def chroma(rgb):
    return max(rgb[:3]) - min(rgb[:3])


def luminance(rgb):
    def ch(x):
        x /= 255
        return x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(x) for x in rgb[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def colours_in(value, named=False):
    out = [m.group(0) for m in HEX.finditer(value)]
    out += [m.group(0) for m in COLOUR_FN.finditer(value)]
    if named:
        out += [m.group(0) for m in NAMED_RE.finditer(value)]
    return out


def is_purple(value):
    if NAMED_PURPLE.search(value):
        return True
    for c in colours_in(value):
        hs = hue_sat(c)
        if hs and 250 <= hs[0] <= 320 and hs[1] >= 0.25:
            return True
    return False


def is_pure_bw(value):
    rgb = to_rgb(value)
    return bool(rgb) and rgb[3] >= 0.99 and (rgb[:3] == (0, 0, 0) or rgb[:3] == (255, 255, 255))


def solid(value):
    """The single opaque colour a background or color value sets, or None."""
    v = value.strip().lower()
    if "gradient(" in v or "url(" in v:
        return None
    cs = colours_in(v, named=True)
    if len(cs) != 1:
        return None
    rgb = to_rgb(cs[0])
    return rgb if rgb and rgb[3] >= 0.99 else None


# ---------------------------------------------------------------- lengths

def px(value, fs=16.0):
    m = re.match(r"\s*(-?[\d.]+)(px|rem|em|pt)?\b", value)
    if not m:
        return None
    try:
        n = float(m.group(1))
    except ValueError:
        return None
    unit = m.group(2)
    if unit == "rem":
        return n * 16
    if unit == "em":
        return n * fs
    if unit == "pt":
        return n * 4 / 3
    if unit is None and n != 0:
        return None
    return n


def em_value(value, fs=16.0):
    """letter-spacing in em."""
    m = re.match(r"\s*(-?[\d.]+)(px|rem|em)?", value)
    if not m:
        return None
    n = float(m.group(1))
    if m.group(2) == "em":
        return n
    if m.group(2) == "rem":
        return n * 16 / fs
    if m.group(2) == "px":
        return n / fs
    return None if n else 0.0


def leading(value, fs=None):
    v = value.strip()
    m = re.fullmatch(r"(-?[\d.]+)(%|px|rem|em)?", v)
    if not m:
        return None
    n = float(m.group(1))
    unit = m.group(2)
    if unit is None or unit == "em":
        return n
    if unit == "%":
        return n / 100
    if fs:
        return (n * 16 if unit == "rem" else n) / fs
    return None


def split_top(value, sep=","):
    out, depth, cur = [], 0, []
    for ch in value:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == sep and depth == 0:
            out.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    out.append("".join(cur))
    return [x.strip() for x in out if x.strip()]


def shadows(value):
    """[(x, y, blur, spread, colour or None)] for a box-shadow/text-shadow value."""
    out = []
    for part in split_top(value):
        cs = colours_in(part, named=True)
        rest = part
        for c in cs:
            rest = rest.replace(c, " ")
        nums = [px(n) for n in re.findall(r"-?[\d.]+(?:px|rem|em)?", rest)]
        nums = [n for n in nums if n is not None]
        if len(nums) >= 2:
            nums += [0.0] * (4 - len(nums))
            out.append((nums[0], nums[1], nums[2], nums[3], cs[0] if cs else None))
    return out


# ---------------------------------------------------------------- css model

class Rule:
    __slots__ = ("file", "line", "sel", "decls", "media", "tokens", "inline")

    def __init__(self, file, line, sel, decls, media, inline=False):
        self.file, self.line, self.sel, self.decls, self.media, self.inline = file, line, sel, decls, media, inline
        low = sel.lower()
        self.tokens = (not inline) and (
            low in (":root", "html", ":host", "*", ".dark", ".light", "html.dark")
            or low.startswith(":root") or "[data-theme" in low or low.startswith("@")
            or (bool(decls) and all(k.startswith("--") for k in decls)))


KEYFRAMES = ("@keyframes", "@-webkit-keyframes", "@-moz-keyframes")


def parse_css(text, file, base_line=1, inline=False):
    text = re.sub(r"/\*.*?\*/", lambda m: re.sub(r"[^\n]", " ", m.group(0)), text, flags=re.S)
    rules, kfs = [], {}
    frames, cur, line = [], [], base_line

    def emit(prelude, parts, ln):
        anc = [fr[0] for fr in frames[:-1]]
        kf = [a for a in anc if a.lower().startswith(KEYFRAMES)]
        decls = {}
        for part in parts:
            if ":" in part:
                k, v = part.split(":", 1)
                k = k.strip().lower()
                if re.fullmatch(r"-{0,2}[\w-]+", k):
                    decls[k] = re.sub(r"\s*!important\s*$", "", v.strip())
        if kf:
            name = kf[-1].split()[1] if len(kf[-1].split()) > 1 else ""
            kfs.setdefault(name, {"file": file, "line": ln, "steps": []})["steps"].append(decls)
            return
        low = prelude.lower()
        if low.startswith(KEYFRAMES):
            name = prelude.split()[1] if len(prelude.split()) > 1 else ""
            kfs.setdefault(name, {"file": file, "line": ln, "steps": []})
            return
        if low.startswith("@") and not low.startswith(("@font-face", "@property", "@page", "@counter-style")):
            return
        sel = prelude
        parents = [a for a in anc if not a.startswith("@")]
        if parents:
            p = parents[-1]
            sel = sel.replace("&", p) if "&" in sel else p + " " + sel
        media = " ".join(a for a in anc if a.startswith("@")).lower()
        rules.append(Rule(file, ln, sel, decls, media, inline))

    for ch in text:
        if ch == "\n":
            line += 1
        if ch == "{":
            frames.append(["".join(cur).strip(), [], line])
            cur = []
        elif ch == ";":
            if frames:
                frames[-1][1].append("".join(cur))
            cur = []
        elif ch == "}":
            if frames:
                frames[-1][1].append("".join(cur))
                prelude, parts, ln = frames[-1]
                emit(prelude, parts, ln)
                frames.pop()
            cur = []
        else:
            cur.append(ch)
    return rules, kfs


# ---------------------------------------------------------------- findings

class Finder:
    def __init__(self):
        self.found = []
        self.waived = {}
        self.keys = set()

    def add(self, path, line, rule, extra=""):
        if rule in self.waived:
            return
        sev, tell, note = RULES[rule]
        note = note + (f" ({extra})" if extra else "")
        key = (path, line, rule, note)
        if key in self.keys:
            return
        self.keys.add(key)
        self.found.append({"file": path, "line": line, "rule": rule, "severity": sev,
                           "tell": tell, "note": note})


def read_waivers(text, path, issues):
    out = {}
    for m in WAIVER.finditer(text):
        line = text.count("\n", 0, m.start()) + 1
        reason = (m.group(2) or "").strip()
        reason = re.sub(r"\s*(-->|\*/\}?|\}|\*/)\s*$", "", reason).strip()
        names = [n.strip() for n in m.group(1).split(",")]
        unknown = [n for n in names if n not in RULES]
        if not reason or unknown:
            issues.append((path, line, ", ".join(unknown) if unknown else "no reason"))
            continue
        for n in names:
            out[n] = reason
    return out


# ---------------------------------------------------------------- markup

class Node:
    __slots__ = ("tag", "a", "line", "kids", "parent", "cls")

    def __init__(self, tag, a, line, parent):
        self.tag, self.a, self.line, self.parent, self.kids = tag, a, line, parent, []
        self.cls = ""

    def elements(self):
        return [k for k in self.kids if isinstance(k, Node)]

    def walk(self):
        for k in self.kids:
            if isinstance(k, Node):
                yield k
                yield from k.walk()

    def text(self):
        out = []
        for k in self.kids:
            out.append(k.text() if isinstance(k, Node) else k[0])
        return " ".join(" ".join(out).split())

    def ancestors(self):
        n = self.parent
        while n is not None:
            yield n
            n = n.parent


def string_literals(expr):
    out = []
    for m in re.finditer(r"([\"'`])((?:\\.|(?!\1).)*)\1", expr, re.S):
        out.append(re.sub(r"\$\{[^}]*\}", " ", m.group(2)))
    return " ".join(out)


def component_to_markup(src):
    """Turn JSX/Vue/Svelte/Astro source into markup the HTML parser can read."""
    src = re.sub(r"^---\n.*?\n---\n", lambda m: "\n" * m.group(0).count("\n"), src, count=1, flags=re.S)
    out, i = [], 0
    attr = re.compile(r"([\w:.@-]+)\s*=\s*\{")
    while True:
        m = attr.search(src, i)
        if not m:
            out.append(src[i:])
            break
        out.append(src[i:m.start()])
        j, depth, quote = m.end(), 1, None
        while j < len(src) and depth:
            ch = src[j]
            if quote:
                if ch == "\\":
                    j += 1
                elif ch == quote:
                    quote = None
            elif ch in "\"'`":
                quote = ch
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
            j += 1
        expr = src[m.end():j - 1]
        name = m.group(1)
        newlines = "\n" * expr.count("\n")
        if name in ("className", "class", "class:list"):
            out.append('class="%s"%s' % (string_literals(expr).replace('"', " "), newlines))
        else:
            out.append('%s="_"%s' % (re.sub(r"[^\w:.@-]", "", name) or "x", newlines))
        i = j
    text = "".join(out)
    text = re.sub(r"\bclassName=", "class=", text)
    return text


class Tree(HTMLParser):
    def __init__(self, component):
        super().__init__(convert_charrefs=True)
        self.component = component
        self.root = Node("#root", {}, 1, None)
        self.cur = self.root
        self.styles, self.links = [], []
        self.in_style, self.style_buf, self.style_line = False, [], 1
        self.skip = 0
        self.skip_tags = ("script", "noscript") if component else SKIP_TAGS

    def handle_starttag(self, tag, attrs, pushing=True):
        line = self.getpos()[0]
        if self.in_style:
            return
        if tag == "style":
            self.in_style, self.style_buf, self.style_line = True, [], line
            return
        if self.skip:
            if tag in self.skip_tags:
                self.skip += 1
            return
        if tag in self.skip_tags:
            self.skip += 1
            return
        a = {k.lower(): ("" if v is None else v) for k, v in attrs}
        n = Node(tag, a, line, self.cur)
        cls = [a.get("class", "")]
        for k in (":class", "v-bind:class", "classname"):
            if k in a:
                cls.append(string_literals(a[k]) if k != "classname" else a[k])
        for k in a:
            if k.startswith("class:") and k != "class:list":
                cls.append(k[6:])
        n.cls = " ".join(" ".join(cls).split())
        self.cur.kids.append(n)
        if tag == "link" and "stylesheet" in (a.get("rel") or "").lower() and a.get("href"):
            self.links.append((a["href"], line))
        if pushing and tag not in VOID:
            self.cur = n

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs, pushing=False)

    def handle_endtag(self, tag):
        if tag == "style" and self.in_style:
            self.in_style = False
            css = "".join(self.style_buf)
            css = re.sub(r"^\s*\{?`|`\}?\s*$", "", css)
            self.styles.append((css, self.style_line))
            return
        if self.in_style:
            return
        if self.skip:
            if tag in self.skip_tags:
                self.skip -= 1
            return
        n = self.cur
        while n is not self.root and n.tag != tag:
            n = n.parent
        if n is not self.root:
            self.cur = n.parent

    def handle_data(self, data):
        if self.in_style:
            self.style_buf.append(data)
            return
        if self.skip or not data.strip():
            return
        line = self.getpos()[0] + data[:len(data) - len(data.lstrip())].count("\n")
        self.cur.kids.append((data, line))


def tw_split(cls):
    """[(variants, base)] for each class token, splitting variants outside brackets."""
    out = []
    for tok in cls.split():
        parts, depth, cur = [], 0, []
        for ch in tok:
            if ch == "[":
                depth += 1
            elif ch == "]":
                depth -= 1
            if ch == ":" and depth == 0:
                parts.append("".join(cur))
                cur = []
            else:
                cur.append(ch)
        parts.append("".join(cur))
        base = parts[-1].lstrip("!")
        out.append((tuple(parts[:-1]), base))
    return out


def tw_px(base, prefix):
    """Arbitrary-value or scale size in px for text-[..]/text-xl style classes."""
    m = re.fullmatch(re.escape(prefix) + r"\[(-?[\d.]+)(px|rem|vw)\]", base)
    if m:
        n = float(m.group(1))
        return ("vw", n) if m.group(2) == "vw" else ("px", n * (16 if m.group(2) == "rem" else 1))
    m = re.fullmatch(re.escape(prefix) + r"(xs|sm|base|lg|[2-9]?xl)", base)
    if m:
        return ("px", TW_SIZE[m.group(1)])
    return None


# ---------------------------------------------------------------- one page

class Unit:
    def __init__(self, path, f, mode):
        self.path, self.f, self.mode = path, f, mode
        self.rules, self.kfs = [], {}
        self.facts = {"radius_tw": [], "blur_tw": 0, "sticky": [], "focus": False, "active": False,
                      "disabled": False, "motion": None, "reduced": False, "buttons": False,
                      "real_controls": False, "interactive": False, "styled_buttons": False}
        self.tokens = {}
        self.source = ""

    def add_css(self, text, file, line=1, inline=False):
        rules, kfs = parse_css(text, file, line, inline)
        self.rules += rules
        for k, v in kfs.items():
            self.kfs.setdefault(k, v)["steps"] += v["steps"] if k in self.kfs and self.kfs[k] is not v else []

    def resolve(self, value, depth=0):
        if "var(" not in value or depth > 6:
            return value

        def sub(m):
            name, fb = m.group(1), m.group(2)
            if name in self.tokens:
                return self.tokens[name]
            return fb.strip() if fb else ""
        return self.resolve(re.sub(r"var\(\s*(--[\w-]+)\s*(?:,\s*([^()]*(?:\([^()]*\))?[^()]*))?\)", sub, value), depth + 1)

    # ------------------------------------------------------------ css checks
    def check_css(self):
        f = self.f
        for r in self.rules:
            for k, v in r.decls.items():
                if k.startswith("--") and (r.tokens or r.sel.lower() in ("body",)):
                    self.tokens[k] = v
        radii, blurs, sizes, literals, greys, anchors = [], [], {}, [], [], []
        families, spacing_raw, offscale, motion = {}, [], [], []
        spacing_tokens = any(re.match(r"--(space|spacing|gap|gutter|s|step|pad|size)[-\d]", k) for k in self.tokens)
        body_fg = None
        page_bg = None
        for r in self.rules:
            if re.search(r"(^|,)\s*(body|html)\s*(,|$)", r.sel.lower()):
                c = r.decls.get("color")
                if c and solid(self.resolve(c)):
                    body_fg = solid(self.resolve(c))
                b = r.decls.get("background-color") or r.decls.get("background")
                if b and solid(self.resolve(b)):
                    page_bg = solid(self.resolve(b))
        for k, v in self.tokens.items():
            if page_bg is None and re.fullmatch(r"--(bg|background|surface|paper|page|canvas|base)(-\w+)?", k):
                page_bg = solid(self.resolve(v))
        has_focus_visible = any(":focus-visible" in r.sel or ":focus-within" in r.sel for r in self.rules)
        for r in self.rules:
            d, sel, low_sel, line, path = r.decls, r.sel, r.sel.lower(), r.line, r.file
            fs = px(d["font-size"]) if "font-size" in d and px(d["font-size"]) else 16.0
            if "prefers-reduced-motion" in r.media:
                self.facts["reduced"] = True
            if ":focus" in low_sel:
                self.facts["focus"] = True
            if ":active" in low_sel:
                self.facts["active"] = True
            if ":disabled" in low_sel or "[disabled" in low_sel or "aria-disabled" in low_sel:
                self.facts["disabled"] = True
            if BUTTON_SEL.search(low_sel) and ":" not in low_sel:
                self.facts["styled_buttons"] = True
            for prop, raw in d.items():
                val = self.resolve(raw)
                low = val.lower()
                custom = prop.startswith("--")
                if "gradient(" in low and is_purple(low):
                    f.add(path, line, "purple-gradient", sel)
                if prop in ("background-clip", "-webkit-background-clip") and "text" in low:
                    bgv = self.resolve(d.get("background", "") + " " + d.get("background-image", "")).lower()
                    if "gradient(" in bgv:
                        f.add(path, line, "gradient-text", sel)
                for c in colours_in(raw.lower()):
                    if c.lower() in FRAMEWORK_HEX:
                        f.add(path, line, "framework-swatch", f"{sel} {prop}: {c}")
                    if c.lower() in CHROME_HEX:
                        f.add(path, line, "fake-chrome", f"{sel} uses window-button colour {c}")
                for c in colours_in(raw, named=prop in COLOUR_PROPS or custom):
                    rgb = to_rgb(c)
                    if not rgb:
                        continue
                    h, l, s = hls(rgb)
                    if s >= 0.35 and 0.15 < l < 0.85 and rgb[3] > 0.5:
                        anchors.append((h, s, l, path, line))
                    if chroma(rgb) <= 2 and 8 < rgb[0] < 247:
                        greys.append((c, path, line))
                    if not r.tokens and not custom:
                        literals.append((path, line))
                if not r.tokens and not custom and prop in (
                        "color", "background", "background-color", "border-color", "fill", "stroke"):
                    if re.search(r"(^|\s)(#000(000)?|#fff(fff)?|black|white)\b", raw.lower()):
                        f.add(path, line, "pure-black-white", f"{sel} {{ {prop}: {raw} }}")
                if custom and r.tokens and re.fullmatch(r"--(bg|background|surface|paper|page|canvas|base|color-bg|color-background|color-surface)(-\w+)?", prop):
                    if is_pure_bw(low):
                        f.add(path, line, "pure-black-surface", f"{prop}: {raw}")
                if prop == "font-family" or (custom and re.match(r"--(font|family|ff)", prop)):
                    first = low.split(",")[0].strip().strip("'\"")
                    if first and first not in GENERIC_FAMILIES and "var(" not in first:
                        families.setdefault(first, (path, line))
                    if prop == "font-family" and not r.tokens and "var(" not in raw:
                        literals.append((path, line))
                if prop == "font-family":
                    first = low.split(",")[0].strip().strip("'\"")
                    if sel in ("body", "html", ":root") or re.search(r"\bh1\b", sel):
                        if first in SYSTEM_FIRST:
                            f.add(path, line, "system-font-main", sel)
                        elif first in DEFAULT_FONTS:
                            f.add(path, line, "default-font", f"{sel}: {first}")
                    if any(first.startswith(m) for m in MONO_FONTS) and LABEL_SEL.search(low_sel) and not CODEISH_SEL.search(low_sel):
                        f.add(path, line, "mono-costume", sel)
                if prop == "border-radius" and not r.tokens:
                    radii.append((low, path, line))
                    if "/" in low and len(set(re.findall(r"\d+%", low))) >= 3:
                        f.add(path, line, "organic-shape", f"{sel} border-radius: {raw}")
                if prop in ("clip-path", "-webkit-clip-path"):
                    if "path(" in low or ("polygon(" in low and low.count(",") >= 7):
                        f.add(path, line, "organic-shape", f"{sel} {prop}")
                if prop in ("box-shadow", "text-shadow"):
                    for x, y, blur, spread, col in shadows(low):
                        hs = hue_sat(col) if col else None
                        if blur >= 40 and hs and hs[1] >= 0.3:
                            f.add(path, line, "glow", sel)
                        if blur == 0 and (abs(x) >= 3 or abs(y) >= 3) and prop == "box-shadow":
                            f.add(path, line, "hard-offset-shadow", sel)
                        if blur >= 24 and prop == "box-shadow":
                            bd = (d.get("border", "") + " " + d.get("border-width", "")).lower()
                            if re.search(r"(^|\s)(1px|0\.5px|thin)\b", bd):
                                f.add(path, line, "thin-border-wide-shadow", sel)
                if prop == "filter" or prop == "text-shadow":
                    if re.search(r"drop-shadow\([^)]*\b([4-9]\d|\d{3,})px", low):
                        f.add(path, line, "glow", sel)
                    m = re.search(r"blur\(\s*([\d.]+)(px|rem)", low)
                    if prop == "filter" and m and float(m.group(1)) * (16 if m.group(2) == "rem" else 1) >= 40:
                        f.add(path, line, "glow", f"{sel} blurred orb")
                if prop in ("background", "background-image") and "radial-gradient(" in low:
                    for c in colours_in(low, named=True):
                        hs = hue_sat(c)
                        rgb = to_rgb(c)
                        if hs and hs[1] >= 0.4 and rgb and rgb[3] > 0.05 and re.search(r"hero|glow|spot|halo|aurora|orb|blob|bg|backdrop|body", low_sel):
                            f.add(path, line, "glow", f"{sel} radial halo")
                            break
                if prop in ("background", "background-image"):
                    if "repeating-" in low and "gradient(" in low:
                        f.add(path, line, "pattern-background", sel)
                    elif low.count("linear-gradient(") >= 1 and re.search(r"\b1px\b", low) and "transparent" in low \
                            and "background-size" in d:
                        f.add(path, line, "pattern-background", f"{sel} drawn grid")
                if prop in ("backdrop-filter", "-webkit-backdrop-filter") and "blur" in low:
                    blurs.append((path, line))
                if prop.startswith("border-left") and prop != "border-left-color":
                    w = px(low)
                    if w and w >= 3 and "border-radius" in d and px(d["border-radius"]) not in (None, 0.0):
                        f.add(path, line, "left-border-card", sel)
                if prop == "font-size":
                    for tag in ("h1", "h2"):
                        if re.fullmatch(rf"{tag}|.*\b{tag}\b(?![-\w])", sel.split(",")[0].strip()):
                            v = px(low) if not low.startswith(("clamp", "calc", "var")) else None
                            if v:
                                sizes[tag] = (v, path, line)
                    if re.search(r"(^|[\s,>])h1\b|hero-title|display", low_sel):
                        v = px(low) if not low.startswith(("clamp", "calc", "min", "max")) else None
                        vw = re.fullmatch(r"([\d.]+)vw", low.strip())
                        cl = re.match(r"clamp\(.*,\s*([\d.]+)(px|rem)\s*\)$", low.strip())
                        big = (v and v >= 120) or (vw and float(vw.group(1)) >= 10) or \
                            (cl and float(cl.group(1)) * (16 if cl.group(2) == "rem" else 1) >= 128)
                        if big:
                            f.add(path, line, "oversized-h1", f"{sel}: {raw}")
                    v = px(low) if not low.startswith(("clamp", "calc", "var", "min", "max")) else None
                    if v is not None and 0 < v < 12 and not r.tokens and not re.search(r"\bsup\b|\bsub\b", low_sel):
                        f.add(path, line, "tiny-text", f"{sel}: {raw}")
                if prop == "font-style" and "italic" in low and HEADING_SEL.search(low_sel) and not re.search(r"\bem\b|\bi\b", low_sel):
                    f.add(path, line, "italic-display", sel)
                if prop == "letter-spacing":
                    ls = em_value(low, fs)
                    caps = "uppercase" in d.get("text-transform", "").lower() or "small-caps" in d.get("font-variant", "").lower() \
                        or "small-caps" in d.get("font-variant-caps", "").lower()
                    if ls is not None and ls <= -0.05:
                        f.add(path, line, "extreme-tracking", f"{sel}: {raw}")
                    if ls is not None and ((caps and ls > 0.04 and fs < 24) or ls >= 0.12):
                        f.add(path, line, "tracked-caps", f"{sel}: {raw}")
                if prop == "line-height":
                    lh = leading(low, fs)
                    caps = "uppercase" in d.get("text-transform", "").lower()
                    if lh is not None and lh < 1.0 and caps and HEADING_SEL.search(low_sel):
                        f.add(path, line, "caps-tight-leading", f"{sel}: {raw}")
                    if lh is not None and 0 < lh < 1.3 and BODY_SEL.search(low_sel) and not HEADING_SEL.search(low_sel):
                        f.add(path, line, "tight-leading", f"{sel}: {raw}")
                if prop == "max-width" and PROSE_SEL.search(low_sel):
                    m = re.fullmatch(r"([\d.]+)ch", low.strip())
                    if m and not 45 <= float(m.group(1)) <= 75:
                        f.add(path, line, "prose-width", f"{sel}: {raw}")
                    elif px(low) and px(low) > 760 and re.search(r"(^|[\s>+~,])p\b|prose|lead|article", low_sel):
                        f.add(path, line, "prose-width", f"{sel}: {raw}")
                if prop == "text-align" and "justify" in low and not r.tokens:
                    f.add(path, line, "justified-text", sel)
                if prop == "text-transform" and "uppercase" in low and re.search(r"^(body|html|main|article)$|(^|[\s>+~,])(p|li|blockquote)\b|prose|lead\b", low_sel):
                    f.add(path, line, "all-caps-body", sel)
                if prop in ("height", "min-height") and re.search(r"\b\d+(\.\d+)?(s|d|l)?vh\b", low) and HERO_SEL.search(low_sel):
                    n = float(re.search(r"([\d.]+)(s|d|l)?vh", low).group(1))
                    if n >= 50:
                        f.add(path, line, "hero-vh", f"{sel} {prop}: {raw}")
                if prop in ("width", "min-width") and re.fullmatch(r"100(s|d|l)?vw", low.strip()):
                    f.add(path, line, "horizontal-scroll", f"{sel} {prop}: {raw}")
                if prop in ("overflow-x", "overflow") and re.search(r"\b(hidden|clip)\b", low) and \
                        re.search(r"^(html|body)(\s*,\s*(html|body))?$", low_sel) and (prop == "overflow-x" or "hidden" in low.split()[:1] and len(low.split()) == 2):
                    f.add(path, line, "horizontal-scroll", f"{sel} {prop}: {raw}")
                if prop == "grid-template-columns" and re.search(r"\b1fr\b", re.sub(r"minmax\([^)]*\)", "", low)) \
                        and re.search(r"galler|photo|image|media|thumb|portfolio|logos|shots", low_sel):
                    f.add(path, line, "bare-fr-images", f"{sel}: {raw}")
                if prop in ("padding", "padding-top", "padding-bottom", "padding-left", "padding-right",
                            "padding-inline", "padding-block", "margin", "margin-top", "margin-bottom",
                            "margin-left", "margin-right", "margin-inline", "margin-block", "gap", "row-gap",
                            "column-gap") and not r.tokens:
                    for tok in low.split():
                        v = px(tok)
                        if v is None or v == 0 or "var(" in tok or "calc" in tok:
                            continue
                        if "var(" not in raw:
                            spacing_raw.append((path, line))
                        if abs(v) > 2 and round(abs(v), 2) % 4:
                            offscale.append((path, line, tok))
                if prop == "padding" and re.search(r"(^|[\s.])(btn|button|card|panel|tile)\b", low_sel) and ":" not in low_sel:
                    vals = [px(t) for t in low.split()]
                    if vals and all(v is not None for v in vals) and 0 < max(vals) < 8:
                        f.add(path, line, "cramped-padding", f"{sel} padding: {raw}")
                if prop in ("transition", "transition-property"):
                    parts = [p.split()[0] for p in split_top(low) if p.split()]
                    if "all" in parts or re.search(r"(^|,)\s*all\b", low) and prop == "transition-property":
                        f.add(path, line, "transition-all", f"{sel}: {raw}")
                    elif set(parts) & {"top", "left", "right", "bottom", "width", "height"}:
                        f.add(path, line, "transition-all", f"{sel} animates {', '.join(sorted(set(parts) & {'top', 'left', 'right', 'bottom', 'width', 'height'}))}")
                    if any(p.startswith(("margin", "padding")) for p in parts):
                        f.add(path, line, "layout-transition", f"{sel}: {raw}")
                    if ":focus" in low_sel and low.strip() != "none":
                        f.add(path, line, "focus-fade", sel)
                    elif "outline" in parts:
                        f.add(path, line, "focus-fade", f"{sel} transitions outline")
                    if low.strip() != "none" and ("transform" in parts or "all" in parts or "translate" in parts or "scale" in parts):
                        motion.append((path, line))
                if prop in ("transition", "transition-timing-function", "animation", "animation-timing-function"):
                    for m in re.finditer(r"cubic-bezier\(([^)]*)\)", low):
                        try:
                            nums = [float(x) for x in m.group(1).split(",")]
                        except ValueError:
                            continue
                        if len(nums) == 4 and (nums[1] < 0 or nums[1] > 1 or nums[3] < 0 or nums[3] > 1):
                            f.add(path, line, "bounce-easing", f"{sel}: {m.group(0)}")
                if prop in ("animation", "animation-name") and low.strip() not in ("none", ""):
                    names = re.findall(r"[a-z_][\w-]*", low)
                    if any(n in self.kfs for n in names) or prop == "animation-name":
                        motion.append((path, line))
                    if any(re.search(r"bounce|elastic|wobble|jelly|rubber|boing", n) for n in names):
                        f.add(path, line, "bounce-easing", f"{sel}: {raw}")
                    for n in names:
                        for step in self.kfs.get(n, {}).get("steps", []):
                            moved = set(step) & {"top", "left", "right", "bottom", "width", "height"}
                            if moved:
                                f.add(path, line, "transition-all", f"{sel} keyframes {n} animate {', '.join(sorted(moved))}")
                                break
                if prop == "outline" or prop == "outline-style":
                    if re.fullmatch(r"\s*(none|0(px)?)\s*", low) and not ("box-shadow" in d or "border" in d):
                        if (":focus" in low_sel and ":not(:focus-visible)" not in low_sel) or \
                                re.search(r"^(\*|a|button|input|textarea|select)$|(^|[\s,])(a|button|input|\*)(\s*,|$)", low_sel):
                            if not has_focus_visible:
                                f.add(path, line, "focus-removed", sel)
                if (":focus" in low_sel) and FIELD_SEL.search(low_sel):
                    if any(k.startswith("border") for k in d) and not any(
                            k in d and d[k].strip().lower() not in ("none", "0") for k in ("outline", "box-shadow")):
                        f.add(path, line, "input-focus-border", sel)
                if prop in ("height", "min-height") and (BUTTON_SEL.search(low_sel) or FIELD_SEL.search(low_sel)) and ":" not in low_sel:
                    v = px(low)
                    if v and (v > 56 or v < 32):
                        f.add(path, line, "control-height", f"{sel} {prop}: {raw}")
                if prop in ("opacity", "visibility") and REVEAL_SEL.search(low_sel) and not r.tokens and "@starting-style" not in r.media:
                    if (prop == "opacity" and re.fullmatch(r"\s*0(\.0+)?\s*", low)) or (prop == "visibility" and "hidden" in low):
                        if not re.search(r"(^|\s)(\.js|html\.js|\[data-js\]|\.has-js)\b", low_sel) and not re.search(
                                r"\.(is-)?(visible|shown|in|active|revealed)\b|\.aos-animate", low_sel):
                            f.add(path, line, "hidden-at-rest", sel)
            anim = d.get("animation", "") + " " + d.get("animation-iteration-count", "") + " " + d.get("animation-name", "")
            alow = anim.lower()
            if "infinite" in alow and re.search(r"marquee|ticker|scroll|logos?", anim + sel, re.I):
                f.add(path, line, "marquee", sel)
            if "infinite" in alow and (re.search(r"\bdot\b|status|live|indicator|beacon|ping", low_sel) or re.search(r"\b(ping|pulse)\b", alow)):
                if re.search(r"dot|status|live|indicator|beacon|ping|badge", low_sel) or re.search(r"\bping\b", alow):
                    f.add(path, line, "pulsing-dot", sel)
            if "infinite" in alow and (re.search(r"blink|caret|cursor|typing", alow) or re.search(r"cursor|caret", low_sel)):
                f.add(path, line, "blinking-cursor", sel)
            if "position" in d and d["position"].strip().lower() == "sticky" and re.fullmatch(r"\s*0(px)?\s*", d.get("top", "x")):
                self.facts["sticky"].append((path, line, sel))
            fv = d.get("color")
            bv = d.get("background-color") or d.get("background")
            if bv and not r.tokens:
                bg = solid(self.resolve(bv))
                fg = solid(self.resolve(fv)) if fv else (body_fg if ":" not in low_sel and BUTTON_SEL.search(low_sel) or re.search(r"badge|chip|tag|pill|nav", low_sel) else None)
                if fg and bg:
                    size = px(d.get("font-size", "16px")) or 16
                    bold = d.get("font-weight", "400").strip() in ("bold", "700", "800", "900")
                    need = 3.0 if size >= 24 or (size >= 18.66 and bold) else 4.5
                    ratio = contrast(fg, bg)
                    if ratio < need:
                        f.add(path, line, "low-contrast", f"{sel} {ratio:.2f}:1")
                    fh, fl, fsat = hls(fg)
                    bh, bl, bsat = hls(bg)
                    if chroma(fg) <= 12 and 0.25 < fl < 0.8 and bsat >= 0.35 and 0.2 < bl < 0.85:
                        f.add(path, line, "gray-on-colour", sel)
            elif fv and re.fullmatch(r"(body|html)", low_sel) and page_bg:
                fg = solid(self.resolve(fv))
                if fg and contrast(fg, page_bg) < 4.5:
                    f.add(path, line, "low-contrast", f"{sel} {contrast(fg, page_bg):.2f}:1")
        # aggregates
        if len(radii) >= 6:
            counts = {}
            for v, _, _ in radii:
                counts[v] = counts.get(v, 0) + 1
            top, n = max(counts.items(), key=lambda x: x[1])
            if n / len(radii) >= 0.8:
                f.add(radii[0][1], radii[0][2], "uniform-radius", f"{n} of {len(radii)} rules use {top}")
        if len(blurs) + self.facts["blur_tw"] >= 3:
            where = blurs[0] if blurs else (self.path, 1)
            f.add(where[0], where[1], "frosted-glass", f"{len(blurs) + self.facts['blur_tw']} surfaces")
        if "h1" in sizes and "h2" in sizes and sizes["h2"][0] > 0 and sizes["h1"][0] / sizes["h2"][0] < 1.2:
            f.add(sizes["h1"][1], sizes["h1"][2], "flat-type-scale",
                  f"h1 {sizes['h1'][0]:g}px, h2 {sizes['h2'][0]:g}px")
        if "h1" in sizes and sizes["h1"][0] >= 64 and not any(
                re.search(r"\bh1\b|display|headline", r.sel.lower()) and
                any(k in r.decls for k in ("overflow-wrap", "word-wrap", "word-break", "hyphens"))
                for r in self.rules) and not any(
                k in ("overflow-wrap", "word-wrap", "hyphens") for r in self.rules
                if r.sel.lower() in ("*", "body", "html", ":root", "h1, h2, h3", "h1,h2,h3") for k in r.decls):
            f.add(sizes["h1"][1], sizes["h1"][2], "display-no-wrap", f"h1 {sizes['h1'][0]:g}px")
        if len(families) > 3:
            p, ln = list(families.values())[3]
            f.add(p, ln, "too-many-fonts", ", ".join(families))
        if literals:
            f.add(literals[0][0], literals[0][1], "colour-literal", f"{len(literals)} outside tokens")
        if greys and anchors:
            f.add(greys[0][1], greys[0][2], "grey-neutral", ", ".join(sorted({g[0] for g in greys})[:4]))
        if spacing_tokens and spacing_raw:
            f.add(spacing_raw[0][0], spacing_raw[0][1], "raw-spacing", f"{len(spacing_raw)} values")
        if len(offscale) > 3:
            f.add(offscale[0][0], offscale[0][1], "off-scale-spacing",
                  f"{len(offscale)} values, e.g. {', '.join(sorted({o[2] for o in offscale})[:4])}")
        if len(self.facts["sticky"]) >= 2:
            p, ln, s = self.facts["sticky"][1]
            f.add(p, ln, "double-sticky", ", ".join(x[2] for x in self.facts["sticky"][:3]))
        if motion and not self.facts["motion"]:
            self.facts["motion"] = motion[0]
        # cream look: warm pale paper + serif display + clay accent
        if page_bg:
            h, l, s = hls(page_bg)
            warm_paper = 25 <= h <= 65 and s >= 0.15 and l >= 0.88
            serif = any(any(fn.startswith(sf) for sf in SERIF_FONTS) for fn in families)
            clay = any(5 <= a[0] <= 35 and a[1] >= 0.4 and 0.3 < a[2] < 0.65 for a in anchors)
            if warm_paper and serif and clay:
                where = next(((a[3], a[4]) for a in anchors if 5 <= a[0] <= 35), (self.path, 1))
                f.add(where[0], where[1], "cream-look")
        return families

    # ------------------------------------------------------------ markup checks
    def check_tree(self, tree):
        f, path, comp = self.f, self.path, self.mode == "component"
        root = tree.root
        nodes = list(root.walk())
        libs = set()
        src_low = self.source.lower()
        for needle, lib in ICON_IMPORTS:
            if re.search(r"from\s+['\"]" + re.escape(needle), src_low) or re.search(r"require\(['\"]" + re.escape(needle), src_low):
                libs.add(lib)
        for href, _ in tree.links:
            for needle, lib in ICON_LINKS:
                if needle in href.lower():
                    libs.add(lib)
        headings, imgs, ctas, h1 = [], [], [], None
        hero = next((n for n in nodes if HERO_CLASS.search(n.cls) or n.a.get("id") == "hero"), None)
        tw_radii, empties = [], []
        page_words = root.text().lower()
        has_pause = bool(re.search(r"\bpause\b", page_words)) or any(
            "pause" in (n.a.get("aria-label", "") + n.cls).lower() for n in nodes)
        numbered = []
        for n in nodes:
            tag, a, line, cls = n.tag, n.a, n.line, n.cls
            low_cls = cls.lower()
            tw = tw_split(cls)
            bases = {b for _, b in tw}
            if tag in ("a", "button", "input", "select", "textarea", "summary") or "tabindex" in a:
                if tag != "a" or "href" in a:
                    self.facts["interactive"] = True
            if tag in ("button", "input", "select", "textarea"):
                self.facts["real_controls"] = True
            if tag == "marquee":
                f.add(path, line, "marquee", "<marquee>")
            if tag in ("img",) or (comp and tag == "image"):
                imgs.append(n)
                src = a.get("src", "")
                if "alt" not in a:
                    f.add(path, line, "img-no-alt", src)
                if PLACEHOLDER.search(src):
                    f.add(path, line, "placeholder", src)
                if src.strip() in ("", "#") and "srcset" not in a:
                    f.add(path, line, "broken-image", f"src=\"{src}\"")
                elif not comp and src and src != "_" and not re.match(r"^[a-z]+:|^//|^/|^#|^\{", src, re.I):
                    local = os.path.join(os.path.dirname(path), src.split("?")[0].split("#")[0])
                    if not os.path.exists(local):
                        f.add(path, line, "broken-image", f"{src} not found")
                if any(h in src.lower() for h in PAID_STOCK):
                    f.add(path, line, "stock-photo", f"paid stock host: {src[:60]}")
                elif any(h in src.lower() for h in FREE_STOCK) and not re.search(r"unsplash|pexels|pixabay|photo by|photograph by|credit", page_words):
                    f.add(path, line, "stock-photo", f"no credit on the page: {src[:60]}")
            if tag == "video":
                if "autoplay" in a and "muted" not in a:
                    f.add(path, line, "autoplay-sound")
                if "poster" not in a:
                    f.add(path, line, "video-poster")
            if tag == "form" and not comp:
                act = a.get("action")
                if (act is None or act.strip() in ("", "#") or act.lower().startswith("javascript:")) and not any(
                        k in a for k in ("hx-post", "hx-get", "data-netlify", "netlify", "data-action")) and a.get("method", "").lower() != "dialog":
                    f.add(path, line, "form-no-action", f"action={act!r}" if act is not None else "no action")
            if tag == "form" and comp and a.get("action", None) in ("#",):
                f.add(path, line, "form-no-action", "action=\"#\"")
            if any(k in a for k in ("data-autoplay", "data-swiper-autoplay")) or a.get("data-ride") == "carousel" or \
                    a.get("data-bs-ride") == "carousel" or ("autoplay" in a and tag not in ("video", "audio")) or \
                    re.search(r"(^|\s)autoplay(\s|$)", low_cls):
                if not has_pause:
                    f.add(path, line, "autoplay-carousel", tag)
            if tag == "svg":
                labelled = any(k in a for k in ("aria-label", "aria-labelledby")) or a.get("aria-hidden") == "true" or \
                    a.get("role") in ("presentation", "none") or any(isinstance(k, Node) and k.tag == "title" for k in n.kids)
                hidden_up = any(p.a.get("aria-hidden") == "true" for p in n.ancestors())
                if not labelled and not hidden_up:
                    f.add(path, line, "unlabelled-svg", "svg")
            if tag == "canvas" and not any(k in a for k in ("aria-label", "aria-labelledby", "aria-hidden", "role")) and not n.text():
                f.add(path, line, "unlabelled-svg", "canvas")
            # icon libraries by class
            toks = set(low_cls.split())
            if toks & {"fa", "fas", "far", "fal", "fab", "fa-solid", "fa-regular", "fa-brands"}:
                libs.add("fontawesome")
            if any(t.startswith(("material-icons", "material-symbols")) for t in toks):
                libs.add("material")
            if "bi" in toks and any(t.startswith("bi-") for t in toks):
                libs.add("bootstrap")
            if any(re.fullmatch(r"ri-[\w-]+-(line|fill)", t) for t in toks):
                libs.add("remix")
            if "ph" in toks or any(t.startswith("ph-") for t in toks):
                libs.add("phosphor")
            if "ti" in toks and any(t.startswith("ti-") for t in toks):
                libs.add("tabler")
            if "bx" in toks or any(t.startswith(("bx-", "bxs-")) for t in toks):
                libs.add("boxicons")
            if tag == "ion-icon":
                libs.add("ionicons")
            if tag == "iconify-icon" or "iconify" in toks:
                libs.add("iconify")
            if "data-lucide" in a or "lucide" in toks:
                libs.add("lucide")
            if "data-feather" in a:
                libs.add("feather")
            # reveal on scroll
            if any(k in a for k in ("data-aos", "data-sal", "data-scroll-reveal", "data-sr")) or \
                    re.search(r"(^|\s)(wow|reveal|aos-init)(\s|$)", low_cls):
                f.add(path, line, "hidden-at-rest", "reveal attribute" if any(k.startswith("data-") for k in a) else cls)
            elif ("opacity-0" in bases or "invisible" in bases) and re.search(r"reveal|fade|animate|appear|scroll", low_cls + " ".join(a)):
                f.add(path, line, "hidden-at-rest", cls[:60])
            # cards
            is_card = bool(CARD_CLASS.search(cls)) or (comp and tag == "card")
            if is_card and any(CARD_CLASS.search(p.cls) or (comp and p.tag == "card") for p in n.ancestors()):
                f.add(path, line, "nested-cards", cls or tag)
            if CARD_CLASS.search(cls) is None and {"border", "rounded-xl", "rounded-2xl", "rounded-lg", "shadow", "shadow-md", "shadow-lg"} & bases:
                boxy = lambda node: bool({"rounded-xl", "rounded-2xl", "rounded-lg", "rounded-3xl"} & {b for _, b in tw_split(node.cls)}) and \
                    bool({"border", "shadow", "shadow-sm", "shadow-md", "shadow-lg", "shadow-xl"} & {b for _, b in tw_split(node.cls)}) and \
                    any(re.fullmatch(r"p-\d+", b) for _, b in tw_split(node.cls))
                if boxy(n) and any(boxy(p) for p in n.ancestors()):
                    f.add(path, line, "nested-cards", "rounded bordered box inside another")
            if re.search(r"(device|phone|iphone|macbook|laptop|ipad|tablet|terminal|editor|code|browser)[-_]?(frame|mockup|window|shell|bezel|chrome)|(^|[\s_-])mockup($|[\s_-])", low_cls):
                f.add(path, line, "device-frame", cls)
            if re.search(r"traffic|window-?dots|browser-?(bar|top|header|dots)|title-?bar|mac-?(dots|buttons)|window-?(controls|buttons|bar)", low_cls):
                f.add(path, line, "fake-chrome", cls)
            # empty slots
            if tag in ("div", "span", "figure", "li", "section", "a") and not n.elements() and not n.text() and \
                    re.search(r"img|image|photo|thumb|avatar|media|logo|placeholder|slot|screenshot|preview|picture|cover|figure|chart|video|map|skeleton|box|block|tile|card", low_cls) and \
                    "background" not in a.get("style", "") and not re.search(r"icon|dot|spacer|divider|line|sr-only|overlay|orb|blob|glow|bg-", low_cls):
                empties.append(n)
            # headings
            if re.fullmatch(r"h[1-6]", tag):
                headings.append(n)
                t = n.text()
                if EMOJI.search(t):
                    f.add(path, line, "emoji-heading", t[:60])
                if tag == "h1" and h1 is None:
                    h1 = n
                for k in n.walk():
                    if (k.tag in ("em", "i") or "italic" in k.cls.split()) and not re.search(r"\b(fa|bi|ri|ti|ph|icon)\b|fa-|icon", k.cls):
                        w = len(k.text().split())
                        if 0 < w <= 2 and len(t.split()) > w + 1:
                            f.add(path, k.line, "italic-word", k.text())
                            break
                prev = None
                if n.parent:
                    sibs = n.parent.elements()
                    i = sibs.index(n)
                    prev = sibs[i - 1] if i else None
                if tag == "h1" and prev is not None and 0 < len(prev.text().split()) <= 5:
                    pb = {b for _, b in tw_split(prev.cls)}
                    if CHIP_CLASS.search(prev.cls) or ("uppercase" in pb and any(b.startswith("tracking-") for b in pb)) or \
                            ("rounded-full" in pb and any(b.startswith(("px-", "py-")) for b in pb)):
                        f.add(path, prev.line, "eyebrow-chip", prev.text())
            # calls to action
            buttonish = tag == "button" or (tag == "a" and (re.search(r"btn|button|cta", cls, re.I) or (
                any(b.startswith("bg-") for b in bases) and any(b.startswith("px-") for b in bases))))
            if buttonish:
                t = n.text()
                ctas.append((t.lower().rstrip("!. →>↗»›"), line))
                if re.search(r"(→|↗|›|»|➜|⟶|->)\s*$|^\s*(→|↗|›|»|➜|⟶)", t):
                    f.add(path, line, "template-punctuation", f"arrow in \"{t[:40]}\"")
                self.facts["buttons"] = True
                for v, b in tw:
                    m = re.fullmatch(r"(?:min-)?h-(\d+)", b)
                    if m and not v:
                        h = int(m.group(1)) * 4
                        if h > 56 or h < 32:
                            f.add(path, line, "control-height", f"{b} = {h}px")
            elif tag == "a" and re.search(r"(→|↗|➜|⟶|->)\s*$", n.text()):
                f.add(path, line, "template-punctuation", f"arrow in \"{n.text()[:40]}\"")
            # emoji as icon
            if not re.fullmatch(r"h[1-6]", tag):
                first = next((k for k in n.kids if not isinstance(k, Node) or k.tag), None)
                if first is not None and not isinstance(first, Node):
                    s = first[0].strip()
                    if s and EMOJI.match(s) and (re.search(r"icon", low_cls) or tag in ("li", "span", "a", "button", "div", "p", "dt")):
                        if len(n.text().split()) <= 12 or re.search(r"icon", low_cls):
                            f.add(path, line, "emoji-icon", s[:2])
            # numbered labels
            t = n.text()
            if not n.elements() and re.fullmatch(r"\(?[/#]?0\d[.)/:]?\)?(\s*[—–/·-]\s*\w+(\s\w+){0,3})?", t.strip()):
                numbered.append(n)
            # tailwind utilities
            self.check_tw(n, tw, bases, hero)
        # page level from markup
        if len(empties) > 5:
            f.add(path, empties[0].line, "empty-slots", f"{len(empties)} empty slots")
        rows = {}
        for e in empties:
            rows.setdefault(id(e.parent), []).append(e)
        if len(empties) <= 5:
            for row in rows.values():
                if len(row) >= 4:
                    f.add(path, row[0].line, "empty-slots", f"{len(row)} empty slots in one row")
                    break
        if len(numbered) >= 2:
            f.add(path, numbered[0].line, "numbered-labels", ", ".join(x.text() for x in numbered[:3]))
        if len(libs) >= 2:
            f.add(path, 1, "two-icon-libraries", ", ".join(sorted(libs)))
        levels = [int(h.tag[1]) for h in headings]
        for prev, cur, h in zip(levels, levels[1:], headings[1:]):
            if cur > prev + 1:
                f.add(path, h.line, "heading-order", f"h{prev} then h{cur}")
                break
        if levels.count(1) > 1:
            f.add(path, [h for h in headings if h.tag == "h1"][1].line, "heading-order", f"{levels.count(1)} h1 elements")
        if ctas and all(t in VAGUE_CTA for t, _ in ctas):
            f.add(path, ctas[0][1], "vague-cta", ", ".join(sorted({t for t, _ in ctas})))
        if hero is None and h1 is not None and h1.parent is not None and h1.parent.tag in ("section", "header"):
            hero = h1.parent
        if hero is not None:
            words = len(hero.text().split())
            paras = sum(1 for k in hero.walk() if k.tag == "p")
            if words >= 80 or paras >= 3:
                f.add(path, hero.line, "wordy-hero", f"{words} words, {paras} paragraphs")
            first_imgs = [k for k in hero.walk() if k.tag in ("img", "image")]
            for k in first_imgs[:1]:
                if k.a.get("loading") == "lazy":
                    f.add(path, k.line, "lazy-hero-image", k.a.get("src", ""))
        if imgs and imgs[0].a.get("loading") == "lazy" and (hero is None or imgs[0] not in list(hero.walk())):
            pos = nodes.index(imgs[0])
            if pos < 40:
                f.add(path, imgs[0].line, "lazy-hero-image", imgs[0].a.get("src", ""))
        # icon trio
        for n in nodes:
            kids = n.elements()
            if len(kids) < 3:
                continue
            iconic = 0
            for k in kids:
                desc = list(k.walk())
                first_el = next((d for d in desc if d.tag not in ("div", "span")), None)
                icon_first = first_el is not None and (
                    first_el.tag in ("svg", "i") or (first_el.tag == "img" and re.search(r"icon|\.svg", first_el.cls + first_el.a.get("src", ""), re.I))
                    or re.search(r"icon", first_el.cls, re.I)) or any(re.search(r"icon", d.cls, re.I) for d in desc[:2]) \
                    or bool(desc) and False
                emoji_first = bool(EMOJI.match(k.text()[:2]))
                has_head = any(re.fullmatch(r"h[2-6]", d.tag) or re.search(r"title", d.cls) for d in desc)
                if (icon_first or emoji_first) and has_head:
                    iconic += 1
            if iconic >= 3 and iconic >= len(kids) * 0.75 and len(kids) <= 4:
                f.add(path, n.line, "icon-card-trio", f"{iconic} icon-over-heading tiles")
        # last section is a newsletter sign-up
        body_blocks = [n for n in nodes if n.tag in ("section", "footer", "aside", "div") and n.parent is not None
                       and n.parent.tag in ("body", "main", "#root", "footer")]
        if body_blocks:
            last = [b for b in body_blocks if b.tag in ("section", "footer")]
            for b in last[-2:]:
                emails = any(k.tag == "input" and k.a.get("type") == "email" for k in b.walk())
                if emails and re.search(r"newsletter|subscribe|stay in the loop|stay updated|in your inbox|mailing list", b.text().lower()):
                    f.add(path, b.line, "stock-newsletter", b.tag)
                    break
        # logo wall without source
        for n in nodes:
            if re.search(r"logos|clients|brands|trusted|customers|partners|logo-wall|logo-cloud", n.cls, re.I):
                marks = sum(1 for k in n.walk() if k.tag in ("img", "svg", "image"))
                if marks >= 4:
                    f.add(path, n.line, "needs-source", f"logo wall of {marks}")
                    break
        # copy
        self.check_copy(root, comp)
        return nodes

    def check_tw(self, n, tw, bases, hero):
        f, path, line = self.f, self.path, n.line
        if not tw:
            return
        variants = {v for vs, _ in tw for v in vs}
        if variants & {"focus", "focus-visible", "focus-within"}:
            self.facts["focus"] = True
        if "active" in variants:
            self.facts["active"] = True
        if "disabled" in variants or "aria-disabled" in variants:
            self.facts["disabled"] = True
        if variants & {"motion-safe", "motion-reduce"}:
            self.facts["reduced"] = True
        grad = any(re.match(r"bg-(gradient-to|linear|radial|conic)", b) for b in bases)
        stops = [b for b in bases if re.match(r"(from|via|to)-", b)]
        if (grad or stops) and any(re.match(r"(from|via|to)-(purple|violet|indigo|fuchsia)-", b) or is_purple(b.replace("_", " ")) for b in stops):
            f.add(path, line, "purple-gradient", " ".join(stops))
        if "bg-clip-text" in bases and (grad or stops):
            f.add(path, line, "gradient-text", "bg-clip-text")
        sw = [b for b in bases if re.fullmatch(r"(bg|text|border|from|via|to|ring|fill|stroke|outline|shadow|decoration|divide|accent|caret)-(indigo|violet|purple)-\d{2,3}(/\d+)?", b)
              or re.fullmatch(r"(bg|text|border|from|via|to)-slate-(900|950)", b)]
        if sw:
            f.add(path, line, "framework-swatch", ", ".join(sw[:3]))
        bw = [b for b in bases if b in ("bg-black", "bg-white", "text-black", "text-white")]
        if bw:
            f.add(path, line, "pure-black-white", ", ".join(bw))
        if any(re.fullmatch(r"(bg|text|border)-neutral-\d+", b) for b in bases):
            self.facts.setdefault("tw_neutral", line)
        for b in bases:
            m = re.fullmatch(r"rounded(-[\w\[\].]+)?", b)
            if m and b != "rounded-full" and b != "rounded-none":
                self.facts["radius_tw"].append((b, line))
                break
        if any(re.fullmatch(r"border-l-(\d+|\[\d+px\])", b) and int(re.sub(r"\D", "", b) or 0) >= 3 for b in bases) and \
                any(b.startswith("rounded") and b != "rounded-none" for b in bases):
            f.add(path, line, "left-border-card", "border-l with rounded")
        if any(re.fullmatch(r"blur-(2xl|3xl)|blur-\[(\d+)px\]", b) and (not b.startswith("blur-[") or int(re.sub(r"\D", "", b)) >= 40) for b in bases):
            f.add(path, line, "glow", "blurred orb")
        if any(re.fullmatch(r"shadow-(purple|violet|indigo|fuchsia|blue|cyan|pink|emerald)-\d+(/\d+)?", b) for b in bases) or \
                any(re.match(r"shadow-\[0_0_(\d+)px", b) and int(re.match(r"shadow-\[0_0_(\d+)px", b).group(1)) >= 40 for b in bases):
            f.add(path, line, "glow", "coloured shadow")
        if any(b.startswith("backdrop-blur") for b in bases):
            self.facts["blur_tw"] += 1
        if any(re.fullmatch(r"animate-(marquee|scroll|ticker|infinite-scroll|loop|slide)[\w-]*", b) for b in bases):
            f.add(path, line, "marquee", "animate class")
        heading = re.fullmatch(r"h[1-3]", n.tag)
        if n.tag == "h1":
            for b in bases:
                s = tw_px(b, "text-")
                if s and ((s[0] == "px" and s[1] >= 120) or (s[0] == "vw" and s[1] >= 10)):
                    f.add(path, line, "oversized-h1", b)
        if heading and "italic" in bases:
            f.add(path, line, "italic-display", n.tag)
        if heading and "uppercase" in bases and any(b in ("leading-none",) or re.fullmatch(r"leading-\[0?\.\d+\]", b) for b in bases):
            f.add(path, line, "caps-tight-leading", n.tag)
        if "font-mono" in bases and ("uppercase" in bases or "text-xs" in bases) and n.tag not in ("code", "pre", "kbd", "samp"):
            f.add(path, line, "mono-costume", n.tag)
        if "uppercase" in bases and any(b in ("tracking-wide", "tracking-wider", "tracking-widest") or re.fullmatch(r"tracking-\[0?\.\d+em\]", b) for b in bases):
            f.add(path, line, "tracked-caps", n.tag)
        if any(b == "tracking-tighter" or (re.fullmatch(r"-?tracking-\[-?0?\.\d+em\]", b) and "-" in b.split("[")[1] and float(re.search(r"-?0?\.\d+", b.split("[")[1]).group(0)) <= -0.05) for b in bases):
            f.add(path, line, "extreme-tracking", n.tag)
        for b in bases:
            s = tw_px(b, "text-")
            if s and s[0] == "px" and s[1] < 12:
                f.add(path, line, "tiny-text", b)
        if n.tag in ("p", "li", "blockquote") and any(b in ("leading-none", "leading-tight") or re.fullmatch(r"leading-\[(0?\.\d+|1(\.[0-2]\d*)?)\]", b) for b in bases):
            f.add(path, line, "tight-leading", n.tag)
        if "text-justify" in bases:
            f.add(path, line, "justified-text", n.tag)
        if n.tag in ("p", "li") and "uppercase" in bases and len(n.text().split()) > 12:
            f.add(path, line, "all-caps-body", n.tag)
        if bases & {"h-screen", "min-h-screen", "h-dvh", "min-h-dvh", "h-svh", "min-h-svh", "h-[100vh]", "min-h-[100vh]"}:
            if n is hero or HERO_CLASS.search(n.cls) or (n.tag in ("section", "header") and any(k.tag == "h1" for k in n.walk())):
                f.add(path, line, "hero-vh", " ".join(sorted(bases & {"h-screen", "min-h-screen", "h-dvh", "min-h-dvh", "h-svh", "min-h-svh", "h-[100vh]", "min-h-[100vh]"})))
        if "w-screen" in bases and not bases & {"fixed", "absolute"}:
            f.add(path, line, "horizontal-scroll", "w-screen")
        if "sticky" in bases and "top-0" in bases:
            self.facts["sticky"].append((path, line, n.tag + ".sticky"))
        if "transition-all" in bases:
            f.add(path, line, "transition-all", "transition-all")
        if "animate-bounce" in bases or any(re.search(r"cubic-bezier\([^)]*(-\d|[,_]1\.\d)", b) for b in bases):
            f.add(path, line, "bounce-easing", "animate-bounce" if "animate-bounce" in bases else "overshoot curve")
        plain_anim = [b for vs, b in tw if b.startswith("animate-") and b != "animate-none" and not set(vs) & {"motion-safe", "motion-reduce"}]
        if plain_anim and not self.facts["motion"]:
            self.facts["motion"] = (path, line)
        if bases & {"animate-ping", "animate-pulse"} and not n.text() and (
                any(re.fullmatch(r"(w|h|size)-[1-4](\.5)?", b) for b in bases) or "rounded-full" in bases):
            f.add(path, line, "pulsing-dot", "animate-ping" if "animate-ping" in bases else "animate-pulse")
        removed = [(vs, b) for vs, b in tw if b in ("outline-none", "outline-0") and (not vs or set(vs) & {"focus", "focus-visible"})]
        if removed and not any(b.startswith(("ring", "outline-")) and b not in ("outline-none", "outline-0") and set(vs) & {"focus", "focus-visible"}
                               for vs, b in tw):
            f.add(path, line, "focus-removed", "outline-none with no focus ring")

    def check_copy(self, root, comp):
        f, path = self.f, self.path
        dashes, dash_line = 0, None
        stack = [(root, False)]
        texts = []

        def collect(node, inside):
            for k in node.kids:
                if isinstance(k, Node):
                    collect(k, True)
                else:
                    if comp and (not inside or re.search(r"[{}();=]|=>", k[0])):
                        continue
                    texts.append((k[0], k[1]))
        collect(root, False)
        for data, line in texts:
            low = " ".join(data.lower().split())
            for p in GENERIC_PHRASES:
                if p in low:
                    f.add(path, line, "generic-copy", f"\"{p}\"")
                    break
            for p in THEATER_PHRASES:
                if p in low:
                    f.add(path, line, "theater-phrase", f"\"{p}\"")
                    break
            for rx in REBUTTAL:
                m = rx.search(low)
                if m:
                    f.add(path, line, "rebuttal-cadence", f"\"{m.group(0)[:50]}\"")
                    break
            m = PLACEHOLDER.search(data)
            if m:
                f.add(path, line, "placeholder", m.group(0))
            n = data.count("—") + data.count("–") + len(re.findall(r"\s--\s", data))
            if n:
                dashes += n
                dash_line = dash_line or line
            if re.search(r"\w\s+·\s+\w", data) or re.search(r"\b[A-Z]{3,}\s+[-–—]\s+\w", data):
                f.add(path, line, "template-punctuation", data.strip()[:50])
            if re.search(r"\b\d[\d,.]*\s*(?:k|m|million|thousand)?\+?\s+(?:happy |satisfied |active )?(?:customers|users|teams|companies|developers|businesses|clients|creators|downloads|brands|members)\b", low) \
                    or "★★★★★" in data or "⭐⭐⭐⭐⭐" in data or re.search(r"\b(?:4\.\d|5\.0)\s*(?:/\s*5|stars?\b|rating)", low) \
                    or re.search(r"\b(?:trusted|loved|used) by\b", low) or re.search(r"\b\d+(?:\.\d+)?x (?:faster|more|better|cheaper)\b", low) \
                    or re.search(r"\b\d{2,3}% (?:faster|more|less|increase|reduction|fewer|cheaper)\b", low):
                f.add(path, line, "needs-source", data.strip()[:50])
        if dashes >= 2:
            f.add(path, dash_line, "em-dash", f"{dashes} dashes")

    def check_page_level(self, has_markup):
        f, path = self.f, self.path
        fx = self.facts
        if fx["motion"] and not fx["reduced"]:
            f.add(fx["motion"][0], fx["motion"][1], "no-reduced-motion")
        if has_markup and fx["interactive"] and (self.rules or fx["radius_tw"]) and not fx["focus"]:
            f.add(path, 1, "no-focus-style")
        if (fx["styled_buttons"] or fx["buttons"]) and (self.rules or fx["radius_tw"]):
            missing = []
            if not fx["active"]:
                missing.append(":active")
            if fx["real_controls"] and not fx["disabled"]:
                missing.append(":disabled")
            if missing and has_markup:
                f.add(path, 1, "missing-states", "no " + " or ".join(missing))
        tr = fx["radius_tw"]
        if len(tr) >= 6:
            counts = {}
            for b, _ in tr:
                counts[b] = counts.get(b, 0) + 1
            top, n = max(counts.items(), key=lambda x: x[1])
            if n / len(tr) >= 0.8:
                f.add(path, tr[0][1], "uniform-radius", f"{n} of {len(tr)} elements use {top}")
        if "tw_neutral" in fx and any(re.search(r"(bg|text)-(red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose)-\d", self.source)
                                      for _ in [0]):
            f.add(path, fx["tw_neutral"], "grey-neutral", "neutral-* utilities")


# ---------------------------------------------------------------- driver

def read(path):
    try:
        return open(path, encoding="utf-8", errors="replace").read()
    except OSError as e:
        print(f"skip {path}: {e}", file=sys.stderr)
        return None


def lint_page(path, f, linked, issues):
    text = read(path)
    if text is None:
        return
    comp = path.lower().endswith(COMPONENT_EXT)
    unit = Unit(path, f, "component" if comp else "html")
    unit.source = text
    waivers = read_waivers(text, path, issues)
    markup = component_to_markup(text) if comp else text
    tree = Tree(comp)
    tree.feed(markup)
    tree.close()
    for css, line in tree.styles:
        unit.add_css(css, path, line)
    for n in tree.root.walk():
        st = n.a.get("style")
        if st and st != "_":
            unit.add_css("x{" + st + "}", path, n.line, inline=True)
            unit.rules[-1].sel = f"<{n.tag} style>" if unit.rules and unit.rules[-1].sel == "x" else unit.rules[-1].sel
    for href, _ in tree.links:
        if re.match(r"^[a-z]+:|^//", href):
            continue  # remote: never fetched
        css_path = os.path.normpath(os.path.join(os.path.dirname(path), href.split("?")[0].lstrip("/")))
        if os.path.isfile(css_path):
            css = read(css_path)
            if css is None:
                continue
            linked.add(os.path.realpath(css_path))
            waivers.update(read_waivers(css, css_path, issues))
            unit.add_css(css, css_path)
    f.waived = waivers
    unit.check_tree(tree)
    unit.check_css()
    unit.check_page_level(True)
    f.waived = {}


def lint_sheet(path, f, issues):
    text = read(path)
    if text is None:
        return
    unit = Unit(path, f, "css")
    unit.add_css(text, path)
    f.waived = read_waivers(text, path, issues)
    unit.check_css()
    unit.check_page_level(False)
    f.waived = {}


def walk(paths):
    exts = PAGE_EXT + COMPONENT_EXT + (".css",)
    for p in paths:
        if os.path.isfile(p):
            yield p
            continue
        for root, dirs, files in os.walk(p):
            dirs[:] = sorted(d for d in dirs if d not in {"node_modules", ".git", ".next", "dist-ssr", ".svelte-kit"})
            for name in sorted(files):
                if name.lower().endswith(exts):
                    yield os.path.join(root, name)


def lint(paths):
    f, linked, issues = Finder(), set(), []
    files = list(dict.fromkeys(walk(paths)))
    for p in files:
        if not p.lower().endswith(".css"):
            lint_page(p, f, linked, issues)
    for p in files:
        if p.lower().endswith(".css") and os.path.realpath(p) not in linked:
            lint_sheet(p, f, issues)
    for path, line, why in issues:
        f.add(path, line, "waiver-no-reason", why)
    return f.found


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if "--rules" in argv:
        for k, (sev, tell, note) in RULES.items():
            print(f"{k}: [{sev}] {note} -- {tell}")
        return 0
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--only", default="")
    ap.add_argument("--genre", choices=sorted(GENRE_EXEMPT), default=None)
    ap.add_argument("--format", choices=("text", "json", "github"), default="text")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    only = {r for r in a.only.split(",") if r}
    if only - set(RULES):
        print("unknown rule(s): " + ", ".join(sorted(only - set(RULES))), file=sys.stderr)
        return 2
    exempt = GENRE_EXEMPT.get(a.genre, set())
    found = [x for x in lint(a.paths) if (not only or x["rule"] in only) and x["rule"] not in exempt]
    found.sort(key=lambda x: (x["file"], x["line"], x["rule"]))
    fmt = "json" if a.json else a.format
    if fmt == "json":
        print(json.dumps(found, indent=2))
    elif fmt == "github":
        for x in found:
            level = "error" if x["severity"] == "high" else "warning"
            note = x["note"].replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
            print(f"::{level} file={x['file']},line={x['line']},title=page-lint {x['rule']}::{note}")
    else:
        for x in found:
            print(f"{x['file']}:{x['line']} {x['rule']} [{x['severity']}]: {x['note']}")
        print(f"{len(found)} finding(s)" if found else "no findings")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
