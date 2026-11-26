"""Covers ultlib.shop, ultlib.shopsheet, ultlib.shopcheck and ultlib.shopfiles through the CLI."""
import csv
import json
import shutil
import subprocess
import unittest

from _harness import UltCase

SHEET = """Title,Description,Option Name,Option Value,SKU,Price,Compare at,Cost,Weight (g),Inventory,Image,Alt,Payment link
Cedar Candle,"Hand-poured soy candle with cedar and smoke notes, forty hour burn, reusable glass jar.",Size,Small,CC-S,24,30,6,300,20,https://example.com/c.jpg,Cedar candle,https://buy.stripe.com/test_abc
,,Size,Large,CC-L,36,,9,600,10,,,
"""
BAD_ROW = "Linen Spray,Short,,,CC-S,12,10,13,,5,,,\n"


class TestShopCatalog(UltCase):
    def test_clean_sheet_converts_to_shopify_with_variants_as_drafts(self):
        self.write("sheet.csv", SHEET)
        r = self.ult("shop", "catalog", "sheet.csv", "--to", "shopify", "--out", "out.csv")
        self.assertEqual(r.code, 0, r.all)
        self.assertIn("1 products, 2 rows, 0 blockers", r.out)
        self.assertIn("check before relying", r.out)
        rows = list(csv.DictReader((self.root / "out.csv").read_text().splitlines()))
        self.assertEqual([x["Variant SKU"] for x in rows], ["CC-S", "CC-L"])
        self.assertEqual({x["Handle"] for x in rows}, {"cedar-candle"})
        self.assertEqual(rows[0]["Status"], "draft")
        self.assertEqual(rows[1]["Title"], "")  # variant rows leave product fields blank

    def test_problems_block_bad_sheets(self):
        self.write("sheet.csv", SHEET + BAD_ROW)
        r = self.ult("shop", "catalog", "sheet.csv", "--json")
        self.assertEqual(r.code, 1, r.all)
        texts = [p["text"] for p in json.loads(r.out)["problems"]]
        self.assertTrue(any("SKU CC-S repeats" in t for t in texts), texts)
        self.assertTrue(any("cost 13.0 is at or above" in t for t in texts), texts)
        self.assertTrue(any("compare-at price" in t for t in texts), texts)

    def test_woocommerce_groups_variations_under_a_parent(self):
        self.write("sheet.csv", SHEET)
        self.assertEqual(self.ult("shop", "catalog", "sheet.csv", "--to", "woocommerce", "--out", "w.csv").code, 0)
        rows = list(csv.DictReader((self.root / "w.csv").read_text().splitlines()))
        self.assertEqual([x["Type"] for x in rows], ["variable", "variation", "variation"])
        self.assertEqual(rows[1]["Parent"], "cedar-candle")
        self.assertEqual(rows[2]["Weight (kg)"], "0.6")

    def test_missing_sheet(self):
        self.assertEqual(self.ult("shop", "catalog", "nope.csv").code, 2)


class TestShopNumbers(UltCase):
    def test_margin_and_break_even(self):
        r = self.ult("shop", "numbers", "--price", "24", "--cost", "6", "--shipping", "5",
                     "--fee-pct", "3", "--fee-fixed", "0", "--fixed-monthly", "40", "--json")
        self.assertEqual(r.code, 0, r.all)
        n = json.loads(r.out)
        self.assertEqual(n["fees"], 0.72)
        self.assertEqual(n["contribution"], 12.28)
        self.assertEqual(n["break_even_roas"], 1.95)
        self.assertEqual(n["sales_to_cover_fixed"], 4)

    def test_losing_price_fails(self):
        r = self.ult("shop", "numbers", "--price", "10", "--cost", "8", "--shipping", "4")
        self.assertEqual(r.code, 1)
        self.assertIn("loses money", r.out)


class TestShopFiles(UltCase):
    def test_scaffolded_store_passes_its_own_check(self):
        self.write("sheet.csv", SHEET)
        r = self.ult("shop", "scaffold", "--catalog", "sheet.csv", "--brand", "Ember & Oak", "--out", "site")
        self.assertEqual(r.code, 0, r.all)
        page = (self.root / "site" / "products" / "cedar-candle.html").read_text()
        self.assertIn('"@type": "Product"', page)
        self.assertIn("https://buy.stripe.com/test_abc", page)
        self.assertIn("Ember &amp; Oak", page)
        r = self.ult("shop", "check", "site")
        self.assertEqual(r.code, 0, r.all)
        self.assertIn("0 blockers", r.out)

    def test_check_finds_broken_store(self):
        self.write("site/index.html", '<html><head><title>x</title></head><body>'
                   '<img src="missing.png"><a href="gone.html">x</a></body></html>')
        self.write("site/products/mug.html", "<html><head><title>Mug</title>"
                   '<meta name="viewport" content="width=device-width"></head><body><h1>Mug</h1></body></html>')
        r = self.ult("shop", "check", "site", "--json")
        self.assertEqual(r.code, 1, r.all)
        texts = [p["text"] for p in json.loads(r.out)["problems"]]
        for want in ("no viewport", "image missing.png is missing", "link gone.html", "no alt attribute",
                     "without Product structured data", "no 404 page"):
            self.assertTrue(any(want in t for t in texts), (want, texts))

    def test_check_empty_folder(self):
        (self.root / "empty").mkdir()
        self.assertEqual(self.ult("shop", "check", "empty").code, 2)

    def test_emails_have_placeholders_and_unsubscribe_on_marketing(self):
        r = self.ult("shop", "emails", "--brand", "Ember", "--color", "#aa3300", "--out", "mail")
        self.assertEqual(r.code, 0, r.all)
        welcome = (self.root / "mail" / "welcome.html").read_text()
        order = (self.root / "mail" / "order-confirmation.html").read_text()
        self.assertIn("{{unsubscribe_url}}", welcome)
        self.assertNotIn("{{unsubscribe_url}}", order)
        self.assertIn("{{order_number}}", order)
        self.assertIn("#aa3300", order)
        self.assertIn("{{store_address}}", order)

    def test_test_order_script_guards_payment(self):
        self.assertEqual(self.ult("shop", "test-order", "--url", "file:///etc").code, 2)
        r = self.ult("shop", "test-order", "--url", "http://localhost:8000/", "--out", "t.cjs")
        self.assertEqual(r.code, 0, r.all)
        js = (self.root / "t.cjs").read_text()
        self.assertIn('if (page.url().includes("cs_test_"))', js)
        self.assertIn('"http://localhost:8000/"', js)
        if shutil.which("node"):
            self.assertEqual(subprocess.run(["node", "--check", str(self.root / "t.cjs")]).returncode, 0)


if __name__ == "__main__":
    unittest.main()
