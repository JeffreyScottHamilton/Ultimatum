"""`ult shop check DIR` — pre-launch check of a built store folder (static HTML export or theme preview save).

Reads every .html file under DIR and reports what a buyer, a search engine or a link preview would hit:
missing title or meta description, no viewport tag, no single h1, images without alt text or too heavy,
relative links that point nowhere, product pages without Product structured data, no og:image.
Standard library only; never fetches a URL.
"""
from __future__ import annotations

import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

HEAVY_IMAGE_BYTES = 500_000


class _Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title, self.meta, self.h1, self.imgs, self.links = "", {}, 0, [], []
        self.ld, self._in, self._buf = [], None, []

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        if tag == "title":
            self._in, self._buf = "title", []
        elif tag == "meta":
            name = (a.get("name") or a.get("property") or "").lower()
            if name:
                self.meta[name] = a.get("content", "")
        elif tag == "h1":
            self.h1 += 1
        elif tag == "img":
            self.imgs.append(a)
        elif tag in ("a", "link") and a.get("href"):
            if tag == "a" or a.get("rel", "") in ("stylesheet", "icon"):
                self.links.append(a["href"])
        elif tag == "script" and a.get("src"):
            self.links.append(a["src"])
        elif tag == "script" and a.get("type", "").lower() == "application/ld+json":
            self._in, self._buf = "ld", []

    def handle_data(self, data):
        if self._in:
            self._buf.append(data)

    def handle_endtag(self, tag):
        if self._in == "title" and tag == "title":
            self.title = "".join(self._buf).strip()
        elif self._in == "ld" and tag == "script":
            self.ld.append("".join(self._buf))
        else:
            return
        self._in = None


def _ld_types(blobs: list[str]) -> tuple[set[str], list[str]]:
    types, bad = set(), []
    for blob in blobs:
        try:
            data = json.loads(blob)
        except ValueError as e:
            bad.append(f"structured data is not valid JSON ({e.msg})")
            continue
        items = data if isinstance(data, list) else data.get("@graph", [data]) if isinstance(data, dict) else []
        for it in items:
            if isinstance(it, dict):
                t = it.get("@type")
                types.update(t if isinstance(t, list) else [t] if t else [])
                if it.get("@type") == "Product" and not (it.get("offers") or {}):
                    bad.append("Product structured data has no offers (price and currency)")
    return types, bad


def _local_target(page: Path, root: Path, href: str) -> Path | None:
    u = urlparse(href)
    if u.scheme or u.netloc or href.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
        return None
    path = unquote(u.path)
    if not path:
        return None
    target = (root / path.lstrip("/")) if path.startswith("/") else (page.parent / path)
    if target.is_dir() or path.endswith("/"):
        target = target / "index.html"
    return target


def check_page(page: Path, root: Path) -> list[tuple[str, str]]:
    p = _Page()
    p.feed(page.read_text(encoding="utf-8", errors="replace"))
    rel, out = page.relative_to(root).as_posix(), []

    def add(kind, msg):
        out.append((kind, f"{rel}: {msg}"))

    if not p.title:
        add("blocker", "no <title>")
    elif len(p.title) > 65:
        add("fix", f"title is {len(p.title)} characters (search results cut near 60)")
    desc = p.meta.get("description", "")
    if not desc:
        add("fix", "no meta description")
    elif len(desc) > 160:
        add("fix", f"meta description is {len(desc)} characters (keep under about 155)")
    if "viewport" not in p.meta:
        add("blocker", "no viewport meta tag (the page will render zoomed out on phones)")
    if p.h1 != 1:
        add("fix", f"{p.h1} h1 headings (use exactly one)")
    if "og:image" not in p.meta:
        add("fix", "no og:image (link previews will be blank)")
    for img in p.imgs:
        src = img.get("src", "")
        if "alt" not in img:
            add("fix", f"image {src or '(no src)'} has no alt attribute")
        target = _local_target(page, root, src) if src else None
        if target is not None:
            if not target.is_file():
                add("blocker", f"image {src} is missing")
            elif target.stat().st_size > HEAVY_IMAGE_BYTES:
                add("fix", f"image {src} is {target.stat().st_size // 1000} KB (compress or resize)")
            if not (img.get("width") and img.get("height")):
                add("fix", f"image {src} has no width and height (the page jumps as it loads)")
    for href in p.links:
        target = _local_target(page, root, href)
        if target is not None and not target.is_file():
            add("blocker", f"link {href} points to a file that does not exist")
    types, bad = _ld_types(p.ld)
    for b in bad:
        add("fix", b)
    looks_like_product = "product" in rel.lower() or "og:type" in p.meta and p.meta["og:type"] == "product"
    if looks_like_product and "Product" not in types:
        add("fix", "product page without Product structured data (price, availability, image)")
    return out


def check_dir(root: Path) -> tuple[int, list[tuple[str, str]]]:
    pages = sorted(x for x in root.rglob("*.html") if ".ultimatum" not in x.parts and "node_modules" not in x.parts)
    found = []
    for page in pages:
        found += check_page(page, root)
    if pages and not any(x.name in ("404.html", "not-found.html") for x in pages):
        found.append(("fix", "no 404 page"))
    return len(pages), found


def cmd_check(args) -> int:
    root = Path(args.dir)
    if not root.is_dir():
        print(f"no such folder: {root}")
        return 2
    n, found = check_dir(root)
    if not n:
        print(f"no .html files under {root}; for a hosted theme, save the preview pages (or run the store locally) first")
        return 2
    blockers = sum(1 for k, _ in found if k == "blocker")
    if args.json:
        print(json.dumps({"pages": n, "problems": [{"kind": k, "text": m} for k, m in found]}, indent=2))
    else:
        print(f"shop check: {n} pages, {blockers} blockers, {len(found) - blockers} fixes")
        for k, m in found[:80]:
            print(f"  {k}: {m}")
        if len(found) > 80:
            print(f"  ... {len(found) - 80} more (use --json)")
        print("not checked here: checkout, taxes, shipping rates, real-phone layout; run the test order for those")
    return 1 if blockers else 0


def register(sub):
    c = sub.add_parser("check", help="pre-launch check of a built store folder")
    c.add_argument("dir")
    c.add_argument("--json", action="store_true")
    c.set_defaults(func=cmd_check)
