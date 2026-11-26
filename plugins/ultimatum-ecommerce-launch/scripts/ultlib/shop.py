"""`ult shop` — store tools for E-commerce Launch that produce real files.

  ult shop catalog SHEET.csv [--to shopify|woocommerce] [--out FILE]
      read a product sheet (own columns or an Etsy listings export), list the problems,
      and write the file the platform's CSV import takes
  ult shop numbers --price P --cost C [...]
      margin after fees and shipping, the most a sale can cost in ads, break-even ROAS
  ult shop check DIR        pre-launch check of a built store folder (see shopcheck.py)
  ult shop emails | scaffold | test-order   files from shopfiles.py

Standard library only; reads and writes local files, never the network.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

from ultlib.shopsheet import _money, read_sheet, slug  # noqa: F401 - slug re-exported

SHOPIFY_COLUMNS = ["Handle", "Title", "Body (HTML)", "Vendor", "Type", "Tags", "Published", "Option1 Name",
                   "Option1 Value", "Variant SKU", "Variant Grams", "Variant Inventory Qty", "Variant Price",
                   "Variant Compare At Price", "Variant Requires Shipping", "Variant Taxable", "Variant Barcode",
                   "Image Src", "Image Alt Text", "Cost per item", "Status"]
WOO_COLUMNS = ["Type", "SKU", "Name", "Parent", "Published", "Description", "Regular price", "Sale price",
               "Stock", "Weight (kg)", "Images", "Tags", "Attribute 1 name", "Attribute 1 value(s)",
               "Attribute 1 visible", "Attribute 1 global"]
COLUMN_NOTE = ("column names follow the platform's import template as of November 2026; "
               "download its sample CSV and compare before importing (check before relying)")


def problems(rows: list[dict]) -> list[tuple[str, str]]:
    """(blocker|fix, message) for each problem a buyer or the import would hit."""
    out, seen = [], {}
    for n, r in enumerate(rows, 2):
        where = f"row {n} ({r.get('title') or r['handle']})"
        price, cost = _money(r.get("price", "")), _money(r.get("cost", ""))
        if not r.get("title"):
            out.append(("blocker", f"{where}: no title"))
        if price is None or price <= 0:
            out.append(("blocker", f"{where}: price missing or not a number"))
        sku = r.get("sku", "")
        if not sku:
            out.append(("fix", f"{where}: no SKU (one per variant keeps stock and orders straight)"))
        elif sku in seen:
            out.append(("blocker", f"{where}: SKU {sku} repeats row {seen[sku]}"))
        else:
            seen[sku] = n
        cmp_at = _money(r.get("compare_at", ""))
        if cmp_at is not None and price is not None and cmp_at <= price:
            out.append(("fix", f"{where}: compare-at price {cmp_at} is not above the price {price}"))
        if cost is not None and price is not None and cost >= price:
            out.append(("blocker", f"{where}: cost {cost} is at or above the price {price}"))
        if not r.get("weight_g"):
            out.append(("fix", f"{where}: no packed weight (shipping rates need it)"))
        if not r.get("image"):
            out.append(("fix", f"{where}: no image"))
        elif not r.get("alt"):
            out.append(("fix", f"{where}: image has no alt text"))
        if r.get("title") and len(r.get("description", "")) < 80 and _first_of_handle(rows, r):
            out.append(("fix", f"{where}: description under 80 characters"))
    return out


def _first_of_handle(rows, row) -> bool:
    return next(r for r in rows if r["handle"] == row["handle"]) is row


def _grams(v: str) -> str:
    m = _money(v or "")
    return str(int(round(m))) if m is not None else ""


def to_shopify(rows: list[dict]) -> list[dict]:
    out = []
    for r in rows:
        first = _first_of_handle(rows, r)
        out.append({
            "Handle": r["handle"], "Title": r.get("title", "") if first else "",
            "Body (HTML)": r.get("description", "") if first else "", "Vendor": r.get("vendor", "") if first else "",
            "Type": r.get("type", "") if first else "", "Tags": r.get("tags", "") if first else "",
            "Published": "FALSE" if first else "", "Option1 Name": (r.get("option_name") or "Title") if first else "",
            "Option1 Value": r.get("option_value") or "Default Title", "Variant SKU": r.get("sku", ""),
            "Variant Grams": _grams(r.get("weight_g", "")), "Variant Inventory Qty": r.get("inventory", ""),
            "Variant Price": r.get("price", ""), "Variant Compare At Price": r.get("compare_at", ""),
            "Variant Requires Shipping": "TRUE", "Variant Taxable": "TRUE", "Variant Barcode": r.get("barcode", ""),
            "Image Src": r.get("image", ""), "Image Alt Text": r.get("alt", ""), "Cost per item": r.get("cost", ""),
            "Status": "draft" if first else "",
        })
    return out


def to_woocommerce(rows: list[dict]) -> list[dict]:
    out, groups = [], {}
    for r in rows:
        groups.setdefault(r["handle"], []).append(r)
    for handle, group in groups.items():
        head = group[0]
        weight = _money(head.get("weight_g", ""))
        base = {"Name": head.get("title", ""), "Published": "0", "Description": head.get("description", ""),
                "Images": head.get("image", ""), "Tags": head.get("tags", ""),
                "Weight (kg)": f"{weight / 1000:g}" if weight else ""}
        if len(group) == 1:
            out.append({**base, "Type": "simple", "SKU": head.get("sku", handle), "Regular price": head.get("price", ""),
                        "Stock": head.get("inventory", "")})
            continue
        values = ", ".join(r.get("option_value", "") for r in group)
        name = head.get("option_name") or "Option"
        out.append({**base, "Type": "variable", "SKU": handle, "Attribute 1 name": name,
                    "Attribute 1 value(s)": values, "Attribute 1 visible": "1", "Attribute 1 global": "0"})
        for r in group:
            w = _money(r.get("weight_g", ""))
            out.append({"Type": "variation", "SKU": r.get("sku", ""), "Name": f"{head.get('title', '')} - {r.get('option_value', '')}",
                        "Parent": handle, "Published": "1", "Regular price": r.get("price", ""), "Stock": r.get("inventory", ""),
                        "Weight (kg)": f"{w / 1000:g}" if w else "", "Attribute 1 name": name,
                        "Attribute 1 value(s)": r.get("option_value", "")})
    return out


def write_csv(path: Path, columns: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def cmd_catalog(args) -> int:
    src = Path(args.sheet)
    if not src.is_file():
        print(f"no such sheet: {src}")
        return 2
    rows = read_sheet(src.read_text(encoding="utf-8", errors="replace"))
    found = problems(rows)
    blockers = [m for k, m in found if k == "blocker"]
    if args.json:
        print(json.dumps({"rows": len(rows), "products": len({r['handle'] for r in rows}),
                          "problems": [{"kind": k, "text": m} for k, m in found]}, indent=2))
    else:
        print(f"catalog: {len({r['handle'] for r in rows})} products, {len(rows)} rows, "
              f"{len(blockers)} blockers, {len(found) - len(blockers)} fixes")
        for k, m in found[:60]:
            print(f"  {k}: {m}")
    if args.to:
        out = Path(args.out or f"store/import-{args.to}.csv")
        cols, conv = (SHOPIFY_COLUMNS, to_shopify) if args.to == "shopify" else (WOO_COLUMNS, to_woocommerce)
        write_csv(out, cols, conv(rows))
        print(f"wrote {out}: products import as drafts or unpublished; {COLUMN_NOTE}")
    return 1 if blockers else 0


def unit_numbers(price, cost, shipping=0.0, fee_pct=0.0, fee_fixed=0.0, returns_pct=0.0, discount_pct=0.0) -> dict:
    """Per-sale contribution before ads, and the ad numbers that follow from it."""
    sold = price * (1 - discount_pct / 100)
    fees = sold * fee_pct / 100 + fee_fixed
    returns = sold * returns_pct / 100
    contribution = sold - cost - shipping - fees - returns
    return {"sale_price": round(sold, 2), "fees": round(fees, 2), "returns_allowance": round(returns, 2),
            "contribution": round(contribution, 2),
            "margin_pct": round(100 * contribution / sold, 1) if sold else 0.0,
            "max_ad_cost_per_sale": round(max(contribution, 0), 2),
            "break_even_roas": round(sold / contribution, 2) if contribution > 0 else None}


def cmd_numbers(args) -> int:
    n = unit_numbers(args.price, args.cost, args.shipping, args.fee_pct, args.fee_fixed, args.returns_pct, args.discount_pct)
    if args.fixed_monthly and n["contribution"] > 0:
        n["sales_to_cover_fixed"] = -(-args.fixed_monthly // n["contribution"])
    if args.json:
        print(json.dumps(n, indent=2))
        return 0
    print(f"per sale: price {n['sale_price']}, fees {n['fees']}, returns {n['returns_allowance']}, "
          f"left after costs {n['contribution']} ({n['margin_pct']}%)")
    if n["contribution"] <= 0:
        print("loses money on every sale before any ads: raise the price or cut cost or shipping")
        return 1
    print(f"ads: at most {n['max_ad_cost_per_sale']} per sale; break-even ROAS {n['break_even_roas']}")
    if "sales_to_cover_fixed" in n:
        print(f"monthly fixed costs need {int(n['sales_to_cover_fixed'])} sales")
    if args.fee_pct == 2.9 and args.fee_fixed == 0.30:
        print("fees used are example card rates; put in the provider's own rates (check before relying)")
    return 0


def register(sub):
    from ultlib import shopcheck, shopfiles  # noqa: PLC0415 - sibling modules
    p = sub.add_parser("shop", help="store files: catalog import, numbers, pre-launch check, emails, starter store")
    s = p.add_subparsers(dest="shop_cmd", required=True)
    c = s.add_parser("catalog", help="check a product sheet and write the platform import CSV")
    c.add_argument("sheet")
    c.add_argument("--to", choices=("shopify", "woocommerce"))
    c.add_argument("--out")
    c.add_argument("--json", action="store_true")
    c.set_defaults(func=cmd_catalog)
    c = s.add_parser("numbers", help="margin per sale and what ads can cost")
    c.add_argument("--price", type=float, required=True)
    c.add_argument("--cost", type=float, required=True, help="product cost including packaging")
    c.add_argument("--shipping", type=float, default=0.0, help="what the store pays to ship one order")
    c.add_argument("--fee-pct", type=float, default=2.9)
    c.add_argument("--fee-fixed", type=float, default=0.30)
    c.add_argument("--returns-pct", type=float, default=0.0)
    c.add_argument("--discount-pct", type=float, default=0.0)
    c.add_argument("--fixed-monthly", type=float, default=0.0, help="platform plan, apps, tools per month")
    c.add_argument("--json", action="store_true")
    c.set_defaults(func=cmd_numbers)
    shopcheck.register(s)
    shopfiles.register(s)
