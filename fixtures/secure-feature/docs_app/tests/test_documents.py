import json
import unittest

from docs_app import storage
from docs_app.tests.client import request


class DocumentTests(unittest.TestCase):
    def setUp(self):
        storage.reset()

    def test_list_requires_auth(self):
        self.assertEqual(request("GET", "/api/documents")[0], 401)

    def test_list_only_own_account(self):
        status, body = request("GET", "/api/documents", "tok-alice")
        self.assertEqual(status, 200)
        self.assertEqual([d["name"] for d in json.loads(body)], ["alice-notes.txt"])

    def test_create(self):
        status, body = request("POST", "/api/documents", "tok-bob", {"name": "x.txt", "content": "hi"})
        self.assertEqual(status, 201)
        names = [d["name"] for d in json.loads(request("GET", "/api/documents", "tok-bob")[1])]
        self.assertIn("x.txt", names)

    def test_create_bad_body(self):
        self.assertEqual(request("POST", "/api/documents", "tok-bob", {"nope": 1})[0], 400)

    def test_unknown_route(self):
        self.assertEqual(request("GET", "/api/nothing", "tok-bob")[0], 404)
