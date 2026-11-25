import unittest

from contacts.phone import normalize_phone
from contacts.store import ContactStore


class StoreTests(unittest.TestCase):
    def test_add_normalizes(self):
        s = ContactStore()
        self.assertEqual(s.add("Ann", "(415) 555-0100")["phone"], "+14155550100")

    def test_find_by_name(self):
        s = ContactStore()
        s.add("Ann Lee", "415-555-0100")
        s.add("Bob", "415-555-0101")
        self.assertEqual([c["name"] for c in s.find_by_name("ann")], ["Ann Lee"])

    def test_normalize_international(self):
        self.assertEqual(normalize_phone("+44 20 7946 0958"), "+442079460958")
        self.assertEqual(normalize_phone("0044 20 7946 0958"), "+442079460958")

    def test_normalize_rejects_short(self):
        with self.assertRaises(ValueError):
            normalize_phone("12")


if __name__ == "__main__":
    unittest.main()
