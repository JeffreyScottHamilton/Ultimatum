import unittest
from textkit import slugify


class SlugifyTests(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(slugify("Hello World"), "hello-world")

    def test_punctuation(self):
        self.assertEqual(slugify("Hello, World!"), "hello-world")

    def test_accents(self):
        self.assertEqual(slugify("Café Déjà Vu"), "cafe-deja-vu")

    def test_collapses_separators(self):
        self.assertEqual(slugify("a  _ b -- c"), "a-b-c")

    def test_max_length(self):
        self.assertEqual(slugify("one two three", max_length=7), "one-two")

    def test_digits_preserved(self):
        self.assertEqual(slugify("Release 2.0 Notes"), "release-20-notes")


if __name__ == "__main__":
    unittest.main()
