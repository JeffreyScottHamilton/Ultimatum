"""Approval gates, including the app gates: data-model and live-payments."""
from __future__ import annotations

import json

from _harness import UltCase

BRIEF = """# Brief

## Build brief
- Audience: gym members in Leeds
- Offer: monthly membership, 30 GBP
- Main visitor action: start a membership
"""


class Gates(UltCase):
    def setUp(self):
        super().setUp()
        self.write(".ultimatum/brief.md", BRIEF)

    def gate(self, *args):
        return self.ult("gate", *args, "--root", str(self.root))

    def test_status_lists_the_app_gates(self):
        r = self.gate("status", "--json")
        self.assertEqual(r.code, 0, r.all)
        data = json.loads(r.out)
        for item in ("brief", "mockup", "data-model", "publish", "deploy", "live-payments"):
            self.assertEqual(data[item]["state"], "waiting")

    def test_data_model_needs_the_schema_file(self):
        r = self.gate("approve", "data-model", "Looks right")
        self.assertEqual(r.code, 2)
        self.assertIn("--file", r.err)
        self.assertEqual(self.gate("check", "data-model").code, 1)

    def test_data_model_reopens_when_the_schema_changes(self):
        schema = self.write("supabase/migrations/0001_init.sql", "create table members (id uuid primary key);\n")
        r = self.gate("approve", "data-model", "Members table is fine", "--file", str(schema))
        self.assertEqual(r.code, 0, r.all)
        self.assertEqual(self.gate("check", "data-model").code, 0)
        schema.write_text("create table members (id uuid primary key, email text);\n")
        r = self.gate("check", "data-model")
        self.assertEqual(r.code, 1)
        self.assertIn("changed", r.out)

    def test_live_payments_is_used_once(self):
        r = self.gate("approve", "live-payments", "Yes, switch Stripe to live")
        self.assertEqual(r.code, 0, r.all)
        self.assertEqual(self.gate("check", "live-payments").code, 0)
        self.assertEqual(self.gate("done", "live-payments").code, 0)
        r = self.gate("check", "live-payments")
        self.assertEqual(r.code, 1)
        self.assertIn("used once", r.out)

    def test_unknown_item_is_refused(self):
        r = self.gate("approve", "payments", "yes")
        self.assertEqual(r.code, 2)
        self.assertIn("live-payments", r.err)
