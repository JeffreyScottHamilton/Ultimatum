import unittest

from inventory.labels import shelf_label


class LabelTests(unittest.TestCase):
    def test_labels(self):
        for i in range(500):
            with self.subTest(i=i):
                self.assertEqual(len(shelf_label(f"sku{i}", i)), 15)


if __name__ == "__main__":
    unittest.main()
