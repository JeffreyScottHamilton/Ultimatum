import json
import unittest

from invoicer.app import create_app
from tests.fixtures import DEMO_API_KEY, TOKEN_ADMIN, TOKEN_B, build_conn, call


class ReportTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(build_conn())

    def test_sort_by_amount_desc(self):
        status, body = call(self.app, "GET", "/api/reports/invoices", DEMO_API_KEY, query="sort=amount&dir=desc")
        self.assertEqual([r["customer"] for r in json.loads(body)], ["Acme", "Globex"])

    def test_unknown_sort_falls_back(self):
        status, body = call(self.app, "GET", "/api/reports/invoices", DEMO_API_KEY, query="sort=bogus&dir=sideways")
        self.assertEqual(status, 200)
        self.assertEqual([r["customer"] for r in json.loads(body)], ["Acme", "Globex"])

    def test_html_report(self):
        status, body = call(self.app, "GET", "/api/reports/invoices", TOKEN_B, query="format=html")
        self.assertIn(b"Initech", body)

    def test_admin_only(self):
        self.assertEqual(call(self.app, "GET", "/api/admin/tenants", TOKEN_B)[0], 403)
        self.assertEqual(call(self.app, "GET", "/api/admin/tenants", TOKEN_ADMIN)[0], 200)
