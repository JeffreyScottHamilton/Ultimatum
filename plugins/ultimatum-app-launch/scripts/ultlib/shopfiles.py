"""Store files `ult shop` writes: order emails, a starter static store, and a test-order browser script.

  ult shop emails [--brand NAME] [--color HEX] [--out DIR]
  ult shop scaffold --catalog SHEET.csv [--brand NAME] [--currency USD] [--out DIR]
  ult shop test-order --url URL [--out FILE]

Everything here only writes local files. The test-order script is run by the agent with `node`,
against a store the user named, and fills a card only on a Stripe test-mode checkout.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

from ultlib.shopsheet import _money, read_sheet

EMAILS = {
    "welcome": ("Welcome to {brand}", "Thanks for joining, {{first_name}}.",
                "You will hear from us when something new is ready. Nothing else, no daily mail.",
                "Visit the shop", "{{shop_url}}"),
    "abandoned-cart": ("You left something in your cart", "Still thinking it over?",
                       "Your cart is saved: {{cart_items}}. Questions about size, shipping or returns? Reply to this email.",
                       "Return to cart", "{{cart_url}}"),
    "order-confirmation": ("Order {{order_number}} confirmed", "Thank you, {{first_name}}.",
                           "We have your order {{order_number}}: {{order_items}}. Total {{order_total}}. "
                           "We will email again when it ships.", "View your order", "{{order_url}}"),
    "shipping": ("Order {{order_number}} is on its way", "It shipped.",
                 "Your order is with {{carrier}}. Tracking number {{tracking_number}}.",
                 "Track the parcel", "{{tracking_url}}"),
}
PLACEHOLDERS = {
    "{{first_name}}": "customer first name", "{{shop_url}}": "store home page", "{{cart_items}}": "cart line items",
    "{{cart_url}}": "link back to the saved cart", "{{order_number}}": "order number",
    "{{order_items}}": "ordered items", "{{order_total}}": "order total with currency", "{{order_url}}": "order status page",
    "{{carrier}}": "shipping carrier", "{{tracking_number}}": "tracking number", "{{tracking_url}}": "carrier tracking link",
    "{{unsubscribe_url}}": "unsubscribe link (required on marketing mail)", "{{store_address}}": "postal address of the business",
}


def _hex(color: str) -> str:
    return color if re.fullmatch(r"#[0-9a-fA-F]{6}", color or "") else "#1f2937"


def email_html(kind: str, brand: str, color: str) -> str:
    subject, head, body, button, link = EMAILS[kind]
    b, c = html.escape(brand), _hex(color)
    marketing = kind in ("welcome", "abandoned-cart")
    foot = ('<a href="{{unsubscribe_url}}" style="color:#6b7280">Unsubscribe</a><br>' if marketing else "")
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(subject.format(brand=brand))}</title></head>
<body style="margin:0;background:#f3f4f6;font-family:Arial,Helvetica,sans-serif;color:#111827">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td align="center" style="padding:24px 12px">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:560px;background:#ffffff;border-radius:8px">
<tr><td style="padding:24px 28px;font-size:20px;font-weight:bold;color:{c}">{b}</td></tr>
<tr><td style="padding:0 28px"><h1 style="font-size:22px;margin:0 0 12px">{html.escape(head)}</h1>
<p style="font-size:16px;line-height:1.5;margin:0 0 20px">{html.escape(body)}</p>
<a href="{link}" style="display:inline-block;background:{c};color:#ffffff;text-decoration:none;padding:12px 20px;border-radius:6px;font-size:16px">{html.escape(button)}</a>
</td></tr>
<tr><td style="padding:28px;font-size:12px;color:#6b7280;line-height:1.5">{foot}{b} · {{{{store_address}}}}</td></tr>
</table></td></tr></table></body></html>
"""


def cmd_emails(args) -> int:
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for kind in EMAILS:
        (out / f"{kind}.html").write_text(email_html(kind, args.brand, args.color), encoding="utf-8")
    lines = ["# Email placeholders", "", "Replace each with your email tool's own variable before sending.", ""]
    lines += [f"- `{k}`: {v}" for k, v in PLACEHOLDERS.items()]
    lines += ["", "Subjects:"] + [f"- {k}: {v[0].format(brand=args.brand)}" for k, v in EMAILS.items()]
    (out / "PLACEHOLDERS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {len(EMAILS)} emails and PLACEHOLDERS.md to {out}; send a test of each to a real inbox before launch")
    return 0


CSS = """*{box-sizing:border-box}body{margin:0;font-family:system-ui,sans-serif;color:#111;line-height:1.5}
header,main,footer{max-width:1040px;margin:0 auto;padding:16px}header{display:flex;justify-content:space-between}
a{color:inherit}.grid{display:grid;gap:20px;grid-template-columns:repeat(auto-fill,minmax(220px,1fr))}
.card img,.product img{width:100%;height:auto;border-radius:8px;background:#eee}
.buy{display:inline-block;padding:12px 20px;background:#111;color:#fff;border:0;border-radius:6px;font-size:16px;cursor:pointer;text-decoration:none}
footer{font-size:14px;color:#555}
"""
CART_JS = """// Tiny cart kept in this browser only. Checkout goes to each product's Stripe Payment Link.
const KEY = "cart";
function read() { try { return JSON.parse(localStorage.getItem(KEY) || "[]"); } catch (e) { return []; } }
function save(items) { try { localStorage.setItem(KEY, JSON.stringify(items)); } catch (e) {} show(); }
function show() { const n = document.getElementById("cart-count"); if (n) n.textContent = read().length; }
document.addEventListener("click", (e) => {
  const b = e.target.closest("[data-add]"); if (!b) return;
  save(read().concat([b.dataset.add]));
});
show();
"""


def _page(title: str, desc: str, body: str, brand: str, depth: int, og: str = "", extra: str = "") -> str:
    up = "../" * depth
    og_tag = f'<meta property="og:image" content="{html.escape(og)}">' if og else ""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc[:155])}">
<meta property="og:title" content="{html.escape(title)}">{og_tag}
<link rel="stylesheet" href="{up}style.css">{extra}</head>
<body><header><a href="{up}index.html">{html.escape(brand)}</a><span>Cart: <span id="cart-count">0</span></span></header>
<main>{body}</main>
<footer><a href="{up}shipping-returns.html">Shipping and returns</a> · <a href="{up}privacy.html">Privacy</a></footer>
<script src="{up}cart.js"></script></body></html>
"""


def _product(group: list[dict], brand: str, currency: str) -> tuple[str, str]:
    head = group[0]
    title, desc = head.get("title", ""), head.get("description", "") or head.get("title", "")
    price = _money(head.get("price", "")) or 0
    img = head.get("image", "")
    link = head.get("payment_link", "")
    ld = {"@context": "https://schema.org", "@type": "Product", "name": title, "description": desc,
          "sku": head.get("sku", ""), "brand": {"@type": "Brand", "name": brand},
          "offers": {"@type": "Offer", "price": f"{price:.2f}", "priceCurrency": currency,
                     "availability": "https://schema.org/InStock"}}
    if img:
        ld["image"] = img
    pic = f'<img src="{html.escape(img)}" alt="{html.escape(head.get("alt") or title)}" width="800" height="800">' if img else ""
    buy = (f'<a class="buy" href="{html.escape(link)}" data-add="{html.escape(head["handle"])}">Buy now</a>' if link
           else '<p><strong>Add this product\'s Stripe Payment Link in the sheet (column "payment link") before launch.</strong></p>')
    options = "".join(f"<li>{html.escape(r.get('option_value', ''))}</li>" for r in group if r.get("option_value"))
    body = (f'<article class="product">{pic}<h1>{html.escape(title)}</h1><p>{currency} {price:.2f}</p>'
            f'<p>{html.escape(desc)}</p>{"<ul>" + options + "</ul>" if options else ""}{buy}</article>')
    extra = f'<script type="application/ld+json">{json.dumps(ld)}</script><meta property="og:type" content="product">'
    return _page(f"{title} | {brand}", desc, body, brand, 1, img, extra), \
        f'<a class="card" href="products/{head["handle"]}.html">{pic}<h2>{html.escape(title)}</h2><p>{currency} {price:.2f}</p></a>'


def cmd_scaffold(args) -> int:
    src, out = Path(args.catalog), Path(args.out)
    if not src.is_file():
        print(f"no such sheet: {src}")
        return 2
    groups: dict[str, list[dict]] = {}
    for r in read_sheet(src.read_text(encoding="utf-8", errors="replace")):
        groups.setdefault(r["handle"], []).append(r)
    (out / "products").mkdir(parents=True, exist_ok=True)
    cards = []
    for handle, group in groups.items():
        page, card = _product(group, args.brand, args.currency)
        (out / "products" / f"{handle}.html").write_text(page, encoding="utf-8")
        cards.append(card)
    first_img = next((g[0]["image"] for g in groups.values() if g[0].get("image")), "")
    home = f'<h1>{html.escape(args.brand)}</h1><div class="grid">{"".join(cards)}</div>'
    (out / "index.html").write_text(_page(args.brand, f"Shop {args.brand}.", home, args.brand, 0, first_img), encoding="utf-8")
    for name, head, text in (("shipping-returns", "Shipping and returns", "Write your real shipping times, costs and return window here."),
                             ("privacy", "Privacy", "Write what you collect, why, and who processes payments (Stripe)."),
                             ("404", "Page not found", "That page is not here.")):
        body = f'<h1>{head}</h1><p>{text}</p><p><a href="index.html">Back to the shop</a></p>'
        (out / f"{name}.html").write_text(_page(f"{head} | {args.brand}", text, body, args.brand, 0), encoding="utf-8")
    (out / "style.css").write_text(CSS, encoding="utf-8")
    (out / "cart.js").write_text(CART_JS, encoding="utf-8")
    missing = sum(1 for g in groups.values() if not g[0].get("payment_link"))
    print(f"wrote a starter store with {len(groups)} products to {out}; next: `ult shop check {out}`")
    if missing:
        print(f"{missing} products have no Stripe Payment Link yet (make them in Stripe test mode first)")
    return 0


TEST_ORDER = """// Test order: home -> product -> add to cart -> checkout, with a screenshot of each step.
// Run: node {name}   (needs Playwright; screenshots go to {shots})
// A card is typed only on a Stripe test-mode checkout (URL contains cs_test_). Nothing is paid.
const {{ chromium }} = require("playwright");
const fs = require("fs");
const START = {url};
const SHOTS = {shots};
(async () => {{
  fs.mkdirSync(SHOTS, {{ recursive: true }});
  const browser = await chromium.launch();
  const page = await browser.newPage({{ viewport: {{ width: 390, height: 844 }} }});
  const log = [];
  const shot = async (n, label) => {{ await page.screenshot({{ path: `${{SHOTS}}/${{n}}-${{label}}.png`, fullPage: true }}); log.push(`${{n}} ${{label}}: ${{page.url()}}`); }};
  const click = async (re) => {{ const el = page.getByRole("link", {{ name: re }}).or(page.getByRole("button", {{ name: re }})).first();
    if (await el.count()) {{ await el.click(); await page.waitForLoadState("load"); return true; }} return false; }};
  try {{
    await page.goto(START, {{ waitUntil: "load" }}); await shot(1, "home");
    const product = page.locator("a[href*='product']").first();
    if (await product.count()) {{ await product.click(); await page.waitForLoadState("load"); }}
    await shot(2, "product");
    if (!(await click(/add to (cart|bag)|buy now|buy/i))) log.push("no add-to-cart or buy button found");
    await shot(3, "added");
    await click(/checkout|check out|view cart|cart/i); await shot(4, "checkout");
    if (page.url().includes("cs_test_")) {{
      await page.fill("input[name=email]", "test@example.com").catch(() => {{}});
      await page.fill("input[name=cardNumber]", "4242 4242 4242 4242").catch(() => {{}});
      await page.fill("input[name=cardExpiry]", "12 / 34").catch(() => {{}});
      await page.fill("input[name=cardCvc]", "123").catch(() => {{}});
      await page.fill("input[name=billingName]", "Test Buyer").catch(() => {{}});
      await shot(5, "test-card-filled");
      log.push("Stripe test checkout filled; press Pay by hand or extend this script");
    }} else if (/checkout|stripe|shopify/.test(page.url())) {{
      log.push("live checkout reached: stopped before any payment field");
    }}
  }} catch (e) {{ log.push("stopped: " + e.message); await shot(9, "error").catch(() => {{}}); }}
  fs.writeFileSync(`${{SHOTS}}/steps.txt`, log.join("\\n") + "\\n");
  console.log(log.join("\\n"));
  await browser.close();
}})();
"""


def cmd_test_order(args) -> int:
    if not re.match(r"https?://", args.url or ""):
        print("--url must start with http:// or https:// (a local preview like http://localhost:9292 works)")
        return 2
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    shots = ".ultimatum/test-order"
    out.write_text(TEST_ORDER.format(name=out.name, url=json.dumps(args.url), shots=json.dumps(shots)), encoding="utf-8")
    print(f"wrote {out}; run it with `node {out}` and look at every screenshot in {shots}/ before saying checkout works")
    return 0


def register(sub):
    c = sub.add_parser("emails", help="welcome, abandoned cart, order and shipping email templates")
    c.add_argument("--brand", default="Your Shop")
    c.add_argument("--color", default="#1f2937")
    c.add_argument("--out", default="store/emails")
    c.set_defaults(func=cmd_emails)
    c = sub.add_parser("scaffold", help="starter static store from a product sheet (Stripe Payment Links)")
    c.add_argument("--catalog", required=True)
    c.add_argument("--brand", default="Your Shop")
    c.add_argument("--currency", default="USD")
    c.add_argument("--out", default="store/site")
    c.set_defaults(func=cmd_scaffold)
    c = sub.add_parser("test-order", help="write a Playwright script that walks a test order with screenshots")
    c.add_argument("--url", required=True)
    c.add_argument("--out", default="store/test-order.cjs")
    c.set_defaults(func=cmd_test_order)
