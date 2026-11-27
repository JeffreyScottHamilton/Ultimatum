"""`ult market` — marketing checks you can run: page and search basics, A/B test maths, tracking plans.

    ult market page PATH... [--kind home|landing|pricing|service|signup|article] [--json]
    ult market abtest plan --base 0.04 --lift 0.10 [--alpha 0.05] [--power 0.8] [--variants 2] [--daily N]
    ult market abtest read --a 120/3000 --b 151/3010 [--planned N] [--alpha 0.05] [--json]
    ult market events PLAN.json|PLAN.csv [--json]

`page` reads built HTML (a file or a folder) and checks what search, sharing and forms need:
title and description, one h1, canonical, language, viewport, social preview tags, image
alt text, JSON-LD that parses and carries the properties its type needs, form labels and
field counts, and link or button text that says where it goes. Across several pages it
also flags repeated titles and descriptions. Word choice is `ult copylint`'s job.

`abtest plan` gives the visitors each version needs before the result can be read;
`abtest read` gives the lift, a p-value, a 95% interval and a plain verdict, and checks
that traffic split the way it was meant to (sample ratio).

`events` checks a tracking plan: object_action names in snake_case, past-tense actions,
no duplicates, no personal data in properties, and a trigger for every event.

Rules and reasons: skills/website/references/craft/marketing/. Exit 0 when nothing fails
(warnings are listed), 1 on any failure, 2 on bad arguments. Standard library only, no network.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from statistics import NormalDist

KINDS = ("home", "landing", "pricing", "service", "signup", "article")
VAGUE_LINKS = {"click here", "here", "read more", "learn more", "more", "link", "this", "go", "details"}
VAGUE_SUBMIT = {"submit", "send", "go", "ok", "click here", "continue"}
FIELD_TYPES_SKIPPED = {"hidden", "submit", "button", "reset", "image"}
SIGNUP_FIELD_LIMIT = 4
LEAD_FIELD_LIMIT = 5
AUTOCOMPLETE_FOR = {"email": "email", "tel": "tel"}

# Properties a JSON-LD type needs before search engines can use it. Kept small on purpose:
# the ones whose absence makes the markup useless, not every recommended field.
SCHEMA_NEEDS = {
    "Organization": ["name", "url"],
    "LocalBusiness": ["name", "address"],
    "Product": ["name"],
    "Offer": ["price", "priceCurrency"],
    "Article": ["headline"],
    "BlogPosting": ["headline"],
    "NewsArticle": ["headline"],
    "BreadcrumbList": ["itemListElement"],
    "FAQPage": ["mainEntity"],
    "Event": ["name", "startDate", "location"],
    "Service": ["name"],
    "WebSite": ["name", "url"],
    "SoftwareApplication": ["name"],
    "Recipe": ["name", "image"],
    "Person": ["name"],
}
# Subtypes of LocalBusiness that small-business sites use; they need what LocalBusiness needs.
LOCAL_SUBTYPES = {"Restaurant", "Dentist", "Plumber", "Electrician", "HairSalon", "BeautySalon",
                  "AutoRepair", "Bakery", "CafeOrCoffeeShop", "LegalService", "Attorney",
                  "MedicalBusiness", "Physician", "RealEstateAgent", "Store", "HomeAndConstructionBusiness",
                  "ProfessionalService", "HealthAndBeautySupplies", "DaySpa", "ExerciseGym", "Florist",
                  "Locksmith", "MovingCompany", "RoofingContractor", "GeneralContractor", "HousePainter",
                  "AccountingService", "FinancialService", "ChildCare", "Hotel", "VeterinaryCare"}
PRODUCT_NEEDS_ONE_OF = ("offers", "review", "aggregateRating")
CURRENCY = re.compile(r"(?:[$€£¥₹]\s?\d|\d[\d.,]*\s?(?:USD|EUR|GBP|CAD|AUD)\b)")


def finding(level, rule, message, file="", line=0):
    return {"level": level, "rule": rule, "message": message, "file": file, "line": line}


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = None
        self.title = None
        self._in_title = False
        self.meta = {}
        self.links = []
        self.h1 = []
        self._h1_buf = None
        self.images = []
        self.jsonld = []
        self._jsonld_buf = None
        self.forms = []
        self._form = None
        self.labels_for = set()
        self._label_depth = 0
        self.actions = []
        self._action = None
        self.text = []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v if v is not None else "") for k, v in attrs}
        line = self.getpos()[0]
        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "title":
            self._in_title = True
            self.title = ""
        elif tag == "meta":
            key = (a.get("name") or a.get("property") or "").lower()
            if key:
                self.meta[key] = a.get("content", "")
        elif tag == "link":
            self.links.append(a)
        elif tag == "h1":
            self._h1_buf = ""
        elif tag == "img":
            self.images.append((line, a))
        elif tag == "script":
            if a.get("type", "").lower() == "application/ld+json":
                self._jsonld_buf = ["", line]
            else:
                self._skip += 1
        elif tag == "style":
            self._skip += 1
        elif tag == "form":
            self._form = {"line": line, "fields": [], "submit": None, "attrs": a}
            self.forms.append(self._form)
        elif tag == "label":
            if a.get("for"):
                self.labels_for.add(a["for"])
            self._label_depth += 1
        elif tag in ("input", "select", "textarea"):
            kind = a.get("type", "text").lower() if tag == "input" else tag
            if self._form is not None:
                if kind in ("submit", "image") or (tag == "input" and kind == "button"):
                    if self._form["submit"] is None:
                        self._form["submit"] = (a.get("value") or "").strip()
                elif kind not in FIELD_TYPES_SKIPPED:
                    self._form["fields"].append({"line": line, "type": kind, "attrs": a,
                                                 "wrapped": self._label_depth > 0})
        elif tag in ("a", "button"):
            self._action = {"tag": tag, "line": line, "attrs": a, "text": ""}

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "h1" and self._h1_buf is not None:
            self.h1.append(" ".join(self._h1_buf.split()))
            self._h1_buf = None
        elif tag == "script":
            if self._jsonld_buf is not None:
                self.jsonld.append(tuple(self._jsonld_buf))
                self._jsonld_buf = None
            elif self._skip:
                self._skip -= 1
        elif tag == "style" and self._skip:
            self._skip -= 1
        elif tag == "form":
            self._form = None
        elif tag == "label" and self._label_depth:
            self._label_depth -= 1
        elif tag in ("a", "button") and self._action is not None:
            act = self._action
            act["text"] = " ".join(act["text"].split())
            self.actions.append(act)
            if (act["tag"] == "button" and self._form is not None and self._form["submit"] is None
                    and act["attrs"].get("type", "submit").lower() == "submit"):
                self._form["submit"] = act["text"]
            self._action = None

    def handle_data(self, data):
        if self._jsonld_buf is not None:
            self._jsonld_buf[0] += data
            return
        if self._skip:
            return
        if self._in_title:
            self.title += data
        if self._h1_buf is not None:
            self._h1_buf += data
        if self._action is not None:
            self._action["text"] += data
        self.text.append(data)


def _types(node):
    t = node.get("@type", [])
    return t if isinstance(t, list) else [t]


def _walk(node):
    if isinstance(node, dict):
        if "@graph" in node and isinstance(node["@graph"], list):
            for g in node["@graph"]:
                yield from _walk(g)
        if "@type" in node:
            yield node
        for k, v in node.items():
            if k != "@graph" and isinstance(v, (dict, list)):
                yield from _walk(v)
    elif isinstance(node, list):
        for item in node:
            yield from _walk(item)


def check_jsonld(blocks, file):
    out = []
    types_seen = []
    for raw, line in blocks:
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            out.append(finding("fail", "jsonld-parse", f"JSON-LD does not parse: {e.msg} (char {e.pos})", file, line))
            continue
        tops = data if isinstance(data, list) else [data]
        for top in tops:
            if isinstance(top, dict) and "@context" not in top:
                out.append(finding("fail", "jsonld-context", "JSON-LD block has no @context (use https://schema.org)", file, line))
        for node in _walk(data):
            for t in _types(node):
                types_seen.append(t)
                need = SCHEMA_NEEDS.get("LocalBusiness" if t in LOCAL_SUBTYPES else t, [])
                missing = [p for p in need if p not in node]
                if missing:
                    out.append(finding("fail", "jsonld-props", f"{t} is missing {', '.join(missing)}", file, line))
                if t == "Product" and not any(p in node for p in PRODUCT_NEEDS_ONE_OF):
                    out.append(finding("warn", "jsonld-props", "Product needs offers, review or aggregateRating to show anything in results", file, line))
                if t == "FAQPage":
                    out.append(finding("warn", "jsonld-faq", "FAQ rich results are shown only for well-known government and health sites; keep the FAQ for readers, expect no rich result", file, line))
                if t == "HowTo":
                    out.append(finding("warn", "jsonld-howto", "HowTo rich results were retired; the markup does no harm but earns nothing", file, line))
                if (t in LOCAL_SUBTYPES or t in ("LocalBusiness", "Organization")) and ("aggregateRating" in node or "review" in node):
                    out.append(finding("warn", "jsonld-self-review", f"Review stars on your own {t} are not shown (self-serving reviews); put real reviews on the page instead", file, line))
    return out, types_seen


def _has_label(field, labels_for):
    a = field["attrs"]
    return bool(field["wrapped"] or (a.get("id") and a["id"] in labels_for)
                or a.get("aria-label") or a.get("aria-labelledby") or a.get("title"))


def check_forms(p, file, kind):
    out = []
    for form in p.forms:
        fields = form["fields"]
        if not fields:
            continue
        has_email = any(f["type"] == "email" or "email" in (f["attrs"].get("name", "") + f["attrs"].get("id", "")).lower() for f in fields)
        limit = SIGNUP_FIELD_LIMIT if kind == "signup" else LEAD_FIELD_LIMIT
        if has_email and len(fields) > limit:
            out.append(finding("warn", "form-fields", f"{len(fields)} fields on a sign-up or lead form; aim for {limit} or fewer and ask the rest later", file, form["line"]))
        passwords = [f for f in fields if f["type"] == "password"]
        if len(passwords) > 1:
            out.append(finding("warn", "form-confirm", "A second password box adds work; offer show-password instead", file, passwords[1]["line"]))
        for f in fields:
            a = f["attrs"]
            if not _has_label(f, p.labels_for):
                out.append(finding("fail", "form-label", f"{f['type']} field '{a.get('name', '?')}' has no label (placeholder text is not a label)", file, f["line"]))
            ident = (a.get("name", "") + " " + a.get("id", "")).lower()
            if f["type"] == "text" and "email" in ident:
                out.append(finding("warn", "form-type", "Email field should be type=email (right keyboard on phones, built-in check)", file, f["line"]))
            if f["type"] == "text" and re.search(r"\b(phone|tel|mobile)\b", ident.replace("_", " ")):
                out.append(finding("warn", "form-type", "Phone field should be type=tel", file, f["line"]))
            want = AUTOCOMPLETE_FOR.get(f["type"])
            if want and not a.get("autocomplete"):
                out.append(finding("warn", "form-autocomplete", f"Add autocomplete=\"{want}\" so browsers can fill it", file, f["line"]))
        submit = (form["submit"] or "").strip().lower()
        if form["submit"] is not None and (not submit or submit in VAGUE_SUBMIT):
            out.append(finding("warn", "form-submit", f"Submit button says '{form['submit'] or '(empty)'}'; say what happens (\"Get my quote\", \"Book a call\")", file, form["line"]))
    return out


def check_page(text, file="", kind=None):
    p = PageParser()
    p.feed(text)
    p.close()
    out = []
    title = " ".join((p.title or "").split())
    if not title:
        out.append(finding("fail", "title", "No <title>", file))
    elif not 15 <= len(title) <= 60:
        out.append(finding("warn", "title", f"Title is {len(title)} characters; 15 to 60 shows in full in results", file))
    desc = " ".join(p.meta.get("description", "").split())
    if not desc:
        out.append(finding("warn", "description", "No meta description; results will show a snippet chosen for you", file))
    elif not 70 <= len(desc) <= 160:
        out.append(finding("warn", "description", f"Description is {len(desc)} characters; 70 to 160 reads in full", file))
    if not p.lang:
        out.append(finding("warn", "lang", "<html> has no lang attribute", file))
    if "viewport" not in p.meta:
        out.append(finding("fail", "viewport", "No viewport meta; phones will show the desktop layout zoomed out", file))
    if "noindex" in p.meta.get("robots", "").lower():
        out.append(finding("warn", "noindex", "Page asks not to be indexed; remove before launch unless that is intended", file))
    if not p.h1:
        out.append(finding("fail", "h1", "No h1; say what the page is about in one heading", file))
    elif len(p.h1) > 1:
        out.append(finding("warn", "h1", f"{len(p.h1)} h1 headings; keep one and make the rest h2", file))
    canon = [l for l in p.links if "canonical" in l.get("rel", "").lower().split()]
    if not canon:
        out.append(finding("warn", "canonical", "No canonical link; add one with the full https URL", file))
    elif not canon[0].get("href", "").startswith("https://"):
        out.append(finding("warn", "canonical", "Canonical should be a full https:// URL", file))
    for key in ("og:title", "og:description", "og:image"):
        if key not in p.meta:
            out.append(finding("warn", "social", f"No {key}; shared links will look bare", file))
    img = p.meta.get("og:image", "")
    if img and not img.startswith(("https://", "http://")):
        out.append(finding("warn", "social", "og:image must be a full URL or most apps will not load it", file))
    for line, a in p.images:
        if "alt" not in a:
            out.append(finding("fail", "img-alt", f"Image {a.get('src', '?')} has no alt (use alt=\"\" for decoration)", file, line))
    for act in p.actions:
        label = (act["text"] or act["attrs"].get("aria-label", "")).strip().lower().rstrip(".!→ ")
        if label in VAGUE_LINKS:
            out.append(finding("warn", "vague-action", f"{act['tag']} text '{act['text']}' does not say where it goes", file, act["line"]))
    jl, types = check_jsonld(p.jsonld, file)
    out += jl
    out += check_forms(p, file, kind)
    body = " ".join(" ".join(p.text).split())
    if kind == "pricing" and not CURRENCY.search(body):
        out.append(finding("warn", "pricing", "Pricing page shows no price; say a number or a 'from' price", file))
    if kind == "service" and not any(t in LOCAL_SUBTYPES or t in ("LocalBusiness", "Service", "Organization") for t in types):
        out.append(finding("warn", "schema-missing", "Service page has no LocalBusiness, Service or Organization markup", file))
    if kind == "article" and not any(t in ("Article", "BlogPosting", "NewsArticle") for t in types):
        out.append(finding("warn", "schema-missing", "Article page has no Article or BlogPosting markup", file))
    if kind in ("home", "landing", "service", "pricing") and not any(a["tag"] == "button" or a["attrs"].get("href") for a in p.actions):
        out.append(finding("fail", "no-action", "No link or button to act on", file))
    return out, {"title": title, "description": desc}


def collect(paths):
    files = []
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            files += sorted(f for f in path.rglob("*") if f.suffix.lower() in (".html", ".htm") and "node_modules" not in f.parts)
        elif path.is_file():
            files.append(path)
        else:
            raise FileNotFoundError(raw)
    return files


def check_site(paths, kind=None):
    files = collect(paths)
    report, seen_t, seen_d = [], {}, {}
    for f in files:
        items, head = check_page(f.read_text(encoding="utf-8", errors="replace"), str(f), kind)
        report += items
        if head["title"]:
            seen_t.setdefault(head["title"].lower(), []).append(str(f))
        if head["description"]:
            seen_d.setdefault(head["description"].lower(), []).append(str(f))
    for label, seen in (("title", seen_t), ("description", seen_d)):
        for value, where in seen.items():
            if len(where) > 1:
                report.append(finding("warn", f"duplicate-{label}", f"Same {label} on {len(where)} pages: {', '.join(where)}", where[0]))
    return files, report


# ---------------------------------------------------------------- A/B tests

def sample_size(base, lift, alpha=0.05, power=0.8, variants=2):
    """Visitors per version for a two-sided test of two proportions.

    `lift` is relative (0.10 = a 10% better rate). With more than two versions each is compared
    with the control, so alpha is split across the comparisons (Bonferroni)."""
    if not 0 < base < 1 or lift <= 0 or not 0 < base * (1 + lift) < 1:
        raise ValueError("base must be between 0 and 1 and base*(1+lift) below 1")
    if variants < 2:
        raise ValueError("variants must be 2 or more")
    a = alpha / (variants - 1)
    p1, p2 = base, base * (1 + lift)
    pbar = (p1 + p2) / 2
    z_a = NormalDist().inv_cdf(1 - a / 2)
    z_b = NormalDist().inv_cdf(power)
    n = (z_a * math.sqrt(2 * pbar * (1 - pbar)) + z_b * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2 / (p2 - p1) ** 2
    return math.ceil(n)


def plan(base, lift, alpha=0.05, power=0.8, variants=2, daily=None):
    n = sample_size(base, lift, alpha, power, variants)
    out = {"per_version": n, "total": n * variants, "base": base, "target": round(base * (1 + lift), 6),
           "alpha": alpha, "power": power, "variants": variants}
    if daily:
        days = math.ceil(n * variants / daily)
        out["days"] = days
        out["run_days"] = max(14, 7 * math.ceil(days / 7))
        if days > 56:
            out["advice"] = "Over 8 weeks: test a bigger change, a busier page, or an earlier step with more visitors"
    return out


def _parse_pair(s):
    m = re.fullmatch(r"\s*(\d+)\s*/\s*(\d+)\s*", s or "")
    if not m or int(m.group(2)) == 0 or int(m.group(1)) > int(m.group(2)):
        raise ValueError(f"expected CONVERSIONS/VISITORS, got {s!r}")
    return int(m.group(1)), int(m.group(2))


def read(a, b, planned=None, alpha=0.05, split=0.5):
    (ca, na), (cb, nb) = a, b
    ra, rb = ca / na, cb / nb
    pooled = (ca + cb) / (na + nb)
    se0 = math.sqrt(pooled * (1 - pooled) * (1 / na + 1 / nb))
    z = (rb - ra) / se0 if se0 else 0.0
    pval = 2 * (1 - NormalDist().cdf(abs(z)))
    se = math.sqrt(ra * (1 - ra) / na + rb * (1 - rb) / nb)
    half = NormalDist().inv_cdf(0.975) * se
    total = na + nb
    exp_a = total * split
    chi = (na - exp_a) ** 2 / exp_a + (nb - (total - exp_a)) ** 2 / (total - exp_a)
    srm_p = math.erfc(math.sqrt(chi / 2))  # chi-square with one degree of freedom
    out = {"a": {"conversions": ca, "visitors": na, "rate": round(ra, 6)},
           "b": {"conversions": cb, "visitors": nb, "rate": round(rb, 6)},
           "lift_abs": round(rb - ra, 6), "lift_rel": round((rb - ra) / ra, 4) if ra else None,
           "p_value": round(pval, 6), "ci95_abs": [round(rb - ra - half, 6), round(rb - ra + half, 6)],
           "srm_p": round(srm_p, 6)}
    if srm_p < 0.001:
        out["verdict"] = "broken split"
        out["why"] = "Traffic did not split as planned (sample ratio mismatch); find the cause before reading the result"
    elif planned and min(na, nb) < planned:
        out["verdict"] = "not finished"
        out["why"] = f"Each version needs {planned} visitors; the smaller has {min(na, nb)}. Stopping early inflates false wins"
    elif pval < alpha:
        out["verdict"] = "B wins" if rb > ra else "A wins"
        out["why"] = f"p = {pval:.4f} below {alpha}; the true difference is likely between {out['ci95_abs'][0]:+.4f} and {out['ci95_abs'][1]:+.4f}"
    else:
        out["verdict"] = "no clear difference"
        out["why"] = f"p = {pval:.4f}; keep the simpler version or test a bigger change"
    return out


# ---------------------------------------------------------------- tracking plans

EVENT_NAME = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)+$")
PAST_IRREGULAR = {"sent", "shown", "paid", "won", "lost", "made", "bought", "read", "seen", "begun", "chosen", "given", "taken", "left", "set", "built"}
PII = re.compile(r"^(e_?mail|email_address|phone(_number)?|mobile|first_name|last_name|full_name|name|address|street|street_address|postcode|zip(_code)?|ip(_address)?|ssn|dob|date_of_birth|birthday|password|card_number|iban)$")


def load_plan(path):
    p = Path(path)
    if p.suffix.lower() == ".csv":
        with p.open(newline="", encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        return [{"event": r.get("event", "").strip(),
                 "properties": [x.strip() for x in re.split(r"[;,|]", r.get("properties", "") or "") if x.strip()],
                 "trigger": (r.get("trigger") or "").strip()} for r in rows]
    data = json.loads(p.read_text(encoding="utf-8"))
    events = data.get("events", data) if isinstance(data, dict) else data
    if not isinstance(events, list):
        raise ValueError("plan must be a list of events or {\"events\": [...]}")
    return [{"event": str(e.get("event", "")).strip(), "properties": list(e.get("properties", []) or []),
             "trigger": str(e.get("trigger", "") or "").strip()} for e in events]


def check_events(events, file=""):
    out, seen = [], {}
    for i, e in enumerate(events, 1):
        name = e["event"]
        if not name:
            out.append(finding("fail", "event-name", f"row {i}: event has no name", file, i))
            continue
        key = name.lower()
        if key in seen:
            out.append(finding("fail", "event-duplicate", f"{name} is listed twice (rows {seen[key]} and {i})", file, i))
        seen.setdefault(key, i)
        if not EVENT_NAME.match(name):
            out.append(finding("fail", "event-name", f"{name}: use snake_case object_action, e.g. quote_form_submitted", file, i))
        else:
            verb = name.rsplit("_", 1)[1]
            if not (verb.endswith("ed") or verb in PAST_IRREGULAR):
                out.append(finding("warn", "event-tense", f"{name}: end with what happened, in the past tense (…_clicked, …_submitted)", file, i))
        if not e["trigger"]:
            out.append(finding("warn", "event-trigger", f"{name}: say exactly when it fires", file, i))
        for prop in e["properties"]:
            prop = str(prop).strip()
            if PII.match(prop.lower()):
                out.append(finding("fail", "event-pii", f"{name}: property '{prop}' is personal data; keep it out of analytics", file, i))
            elif not re.fullmatch(r"[a-z][a-z0-9_]*", prop):
                out.append(finding("warn", "event-prop", f"{name}: property '{prop}' should be snake_case", file, i))
    if len(events) > 30:
        out.append(finding("warn", "event-count", f"{len(events)} events; start with the 5 to 15 that answer a decision", file))
    return out


# ---------------------------------------------------------------- CLI

def _print(report, label, n, out, as_json, extra=None):
    fails = sum(1 for r in report if r["level"] == "fail")
    warns = len(report) - fails
    if as_json:
        json.dump({**(extra or {}), "checked": n, "fail": fails, "warn": warns, "findings": report}, out, indent=1)
        out.write("\n")
    else:
        for r in report:
            loc = f"{r['file']}:{r['line']}" if r["line"] else r["file"]
            print(f"{loc}: {r['level']} {r['rule']}: {r['message']}", file=out)
        print(f"market {label}: {n} checked, {fails} fail, {warns} warn", file=out)
    return 1 if fails else 0


def cmd_market(args, out=sys.stdout) -> int:
    try:
        if args.what == "page":
            files, report = check_site(args.paths, args.kind)
            if not files:
                print("market page: no HTML files found", file=sys.stderr)
                return 2
            return _print(report, "page", len(files), out, args.json)
        if args.what == "events":
            events = load_plan(args.plan)
            return _print(check_events(events, args.plan), "events", len(events), out, args.json)
        if args.what == "abtest":
            if args.step == "plan":
                r = plan(args.base, args.lift, args.alpha, args.power, args.variants, args.daily)
            else:
                r = read(_parse_pair(args.a), _parse_pair(args.b), args.planned, args.alpha, args.split)
            if args.json:
                json.dump(r, out, indent=1)
                out.write("\n")
            elif args.step == "plan":
                print(f"{r['per_version']} visitors per version ({r['total']} total) to detect {r['base']:.2%} -> {r['target']:.2%}"
                      f" at alpha {r['alpha']}, power {r['power']}", file=out)
                if "days" in r:
                    print(f"about {r['days']} days of traffic; run {r['run_days']} days (whole weeks, at least two)", file=out)
                if "advice" in r:
                    print(r["advice"], file=out)
            else:
                print(f"A {r['a']['rate']:.2%} ({r['a']['conversions']}/{r['a']['visitors']})  B {r['b']['rate']:.2%} ({r['b']['conversions']}/{r['b']['visitors']})", file=out)
                rel = f"{r['lift_rel']:+.1%}" if r["lift_rel"] is not None else "n/a"
                print(f"lift {r['lift_abs']:+.4f} ({rel}), p {r['p_value']:.4f}, 95% interval {r['ci95_abs'][0]:+.4f} to {r['ci95_abs'][1]:+.4f}, split check p {r['srm_p']:.4f}", file=out)
                print(f"verdict: {r['verdict']}. {r['why']}", file=out)
            return 1 if r.get("verdict") == "broken split" else 0
    except FileNotFoundError as e:
        print(f"market: no such path: {e}", file=sys.stderr)
        return 2
    except (ValueError, json.JSONDecodeError) as e:
        print(f"market: {e}", file=sys.stderr)
        return 2
    return 2


def register(sub):
    p = sub.add_parser("market", help="Marketing checks: page and search basics, A/B test maths, tracking plans")
    s = p.add_subparsers(dest="what", required=True)
    pg = s.add_parser("page", help="check built HTML for search, sharing, schema and form basics")
    pg.add_argument("paths", nargs="+")
    pg.add_argument("--kind", choices=KINDS)
    pg.add_argument("--json", action="store_true")
    ab = s.add_parser("abtest", help="plan or read an A/B test")
    st = ab.add_subparsers(dest="step", required=True)
    pl = st.add_parser("plan")
    pl.add_argument("--base", type=float, required=True, help="current conversion rate, e.g. 0.04")
    pl.add_argument("--lift", type=float, required=True, help="smallest relative change worth finding, e.g. 0.10")
    pl.add_argument("--alpha", type=float, default=0.05)
    pl.add_argument("--power", type=float, default=0.8)
    pl.add_argument("--variants", type=int, default=2)
    pl.add_argument("--daily", type=int, help="visitors per day reaching the test")
    pl.add_argument("--json", action="store_true")
    rd = st.add_parser("read")
    rd.add_argument("--a", required=True, help="control CONVERSIONS/VISITORS")
    rd.add_argument("--b", required=True, help="variant CONVERSIONS/VISITORS")
    rd.add_argument("--planned", type=int, help="planned visitors per version")
    rd.add_argument("--alpha", type=float, default=0.05)
    rd.add_argument("--split", type=float, default=0.5, help="share of traffic meant for A")
    rd.add_argument("--json", action="store_true")
    ev = s.add_parser("events", help="check a tracking plan (JSON or CSV)")
    ev.add_argument("plan")
    ev.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_market)


if __name__ == "__main__":
    root = argparse.ArgumentParser(prog="market")
    register(root.add_subparsers(dest="cmd", required=True))
    a = root.parse_args(["market", *sys.argv[1:]])
    sys.exit(a.func(a))
