import json
import unittest

from invoicer.app import create_app
from tests.fixtures import DEMO_API_KEY, TOKEN_B, build_conn, call


class InvoiceTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(build_conn())

    def test_requires_auth(self):
        self.assertEqual(call(self.app, "GET", "/api/invoices")[0], 401)

    def test_list_scoped_to_tenant(self):
        status, body = call(self.app, "GET", "/api/invoices", TOKEN_B)
        self.assertEqual(status, 200)
        self.assertEqual([i["id"] for i in json.loads(body)], [3])

    def test_get_own_invoice(self):
        status, body = call(self.app, "GET", "/api/invoices/1", DEMO_API_KEY)
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)["customer"], "Acme")

    def test_get_missing(self):
        self.assertEqual(call(self.app, "GET", "/api/invoices/99", DEMO_API_KEY)[0], 404)

    def test_create(self):
        status, body = call(self.app, "POST", "/api/invoices", TOKEN_B, {"customer": "Z", "amount_cents": 5})
        self.assertEqual(status, 201)
        new_id = json.loads(body)["id"]
        self.assertEqual(call(self.app, "GET", "/api/invoices/%d" % new_id, TOKEN_B)[0], 200)

    def test_create_invalid(self):
        self.assertEqual(call(self.app, "POST", "/api/invoices", TOKEN_B, {"x": 1})[0], 400)

    def test_update_own_invoice(self):
        status, _ = call(self.app, "PUT", "/api/invoices/3", TOKEN_B, {"customer": "Initech", "amount_cents": 10000})
        self.assertEqual(status, 200)
        body = call(self.app, "GET", "/api/invoices/3", TOKEN_B)[1]
        self.assertEqual(json.loads(body)["amount_cents"], 10000)
