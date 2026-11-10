import io
import os
import tempfile
import unittest

from notes import cli
from notes.render import render_list, render_note
from notes.search import search
from notes.store import Store


class StoreTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.dir.name, "n.json")

    def tearDown(self):
        self.dir.cleanup()

    def test_add_persists(self):
        Store(self.path).add("A", "body", ["x"])
        self.assertEqual(Store(self.path).all()[0].title, "A")

    def test_ids_increment(self):
        s = Store(self.path)
        self.assertEqual([s.add("a").id, s.add("b").id], [1, 2])

    def test_search(self):
        s = Store(self.path)
        s.add("Milk"); s.add("Eggs", tags=["dairy"])
        self.assertEqual([n.title for n in search(s.all(), "MILK")], ["Milk"])
        self.assertEqual([n.title for n in search(s.all(), "dairy")], ["Eggs"])

    def test_render(self):
        s = Store(self.path)
        n = s.add("T", "B", ["t"])
        self.assertEqual(render_note(n), "#1 T [t]\nB")
        self.assertEqual(render_list([]), "(no notes)")

    def test_cli_add_list(self):
        out = io.StringIO()
        self.assertEqual(cli.main(["--db", self.path, "add", "Hello"], out=out), 0)
        self.assertEqual(cli.main(["--db", self.path, "list"], out=out), 0)
        self.assertIn("1\tHello", out.getvalue())
