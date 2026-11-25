import io
import unittest
from billing import cli


class CliTests(unittest.TestCase):
    def test_list(self):
        out = io.StringIO()
        self.assertEqual(cli.main(["list"], out=out), 0)
        self.assertIn("Acme Corp", out.getvalue())
