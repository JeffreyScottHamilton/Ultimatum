import os
import tempfile
import unittest

from billing.report import read_rows, render


class ReportTests(unittest.TestCase):
    def test_render(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "x.csv")
            with open(p, "w") as fh:
                fh.write("sku,unit_price,qty,tax_pct\nA,10.00,2,0\nB,5.00,1,10\n")
            out = render(read_rows(p))
        self.assertEqual(out.splitlines(), ["A,20.00", "B,5.50", "TOTAL,25.50"])


if __name__ == "__main__":
    unittest.main()
