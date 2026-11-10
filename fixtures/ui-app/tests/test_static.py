import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read(name):
    with open(os.path.join(ROOT, name), encoding="utf-8") as fh:
        return fh.read()


class StaticSiteTests(unittest.TestCase):
    def test_index_references_existing_files(self):
        html = read("index.html")
        for ref in re.findall(r'(?:src|href)="([^"]+)"', html):
            self.assertTrue(os.path.exists(os.path.join(ROOT, ref)), ref)

    def test_components_present(self):
        for name in ("button", "dialog", "toast"):
            self.assertTrue(os.path.exists(os.path.join(ROOT, "components", name + ".js")))

    def test_dialog_is_accessible(self):
        js = read("components/dialog.js")
        self.assertIn('aria-modal', js)
        self.assertIn('Escape', js)

    def test_data_has_projects(self):
        self.assertGreaterEqual(len(re.findall(r"\bid:\s*\d+", read("data.js"))), 3)
