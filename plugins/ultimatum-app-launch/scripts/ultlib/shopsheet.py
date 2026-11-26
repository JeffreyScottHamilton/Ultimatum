"""Read a product sheet: the user's own columns or an Etsy listings export, one internal name per field.

Used by `ult shop catalog` and `ult shop scaffold`. Standard library only.
"""
from __future__ import annotations

import csv
import io
import re

# Column names people use in their own sheets, mapped to one internal name.
ALIASES = {
    "handle": ("handle", "url handle", "slug"),
    "title": ("title", "name", "product", "product name"),
    "description": ("description", "body", "body (html)", "details"),
    "option_name": ("option name", "option1 name", "variation 1 name", "variant name"),
    "option_value": ("option value", "option1 value", "variation 1 values", "variant", "option"),
    "sku": ("sku", "variant sku"),
    "price": ("price", "variant price", "regular price"),
    "compare_at": ("compare at", "compare-at price", "compare at price", "variant compare at price", "was price"),
    "cost": ("cost", "cost per item", "unit cost"),
    "weight_g": ("weight (g)", "weight g", "weight", "grams", "variant grams"),
    "inventory": ("inventory", "quantity", "stock", "variant inventory qty"),
    "image": ("image", "image src", "image url", "image1", "photo"),
    "alt": ("alt", "alt text", "image alt text"),
    "tags": ("tags",),
    "type": ("type", "product type", "category"),
    "vendor": ("vendor", "brand"),
    "barcode": ("barcode", "gtin", "upc", "ean"),
    "payment_link": ("payment link", "payment_link", "checkout link"),
}
def _key(name: str) -> str | None:
    n = re.sub(r"\s+", " ", name.strip().lower())
    for k, names in ALIASES.items():
        if n in names:
            return k
    return None


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:80] or "product"


def _money(v: str) -> float | None:
    v = re.sub(r"[^\d.,-]", "", v or "").replace(",", ".") if v else ""
    if v.count(".") > 1:
        head, _, tail = v.rpartition(".")
        v = head.replace(".", "") + "." + tail
    try:
        return round(float(v), 2)
    except ValueError:
        return None


def read_sheet(text: str) -> list[dict]:
    """Rows with internal keys. Etsy exports put several images and variants in one row."""
    rows = []
    for raw in csv.DictReader(io.StringIO(text.lstrip("﻿"))):
        row = {}
        for col, val in raw.items():
            k = _key(col or "")
            if k and val not in (None, "") and k not in row:
                row[k] = val.strip()
        if not row.get("title") and not row.get("handle"):
            if not rows or not (row.get("sku") or row.get("option_value")):
                continue
            row["handle"] = rows[-1]["handle"]  # a variant row under the product above it
        row.setdefault("handle", slug(row.get("title", "")))
        rows.append(row)
    # A variant row may leave the title blank: carry it down from its handle.
    titles = {r["handle"]: r["title"] for r in rows if r.get("title")}
    for r in rows:
        r.setdefault("title", titles.get(r["handle"], ""))
    return rows


