import unittest
from extract_title import extract_title

class TestExtractTitle(unittest.TestCase):

    def test_valid_h1(self):
        markdown = "# Hello"
        self.assertEqual(extract_title(markdown), "Hello")

    def test_h1_with_whitespace(self):
        markdown = "#    Hello World   "
        self.assertEqual(extract_title(markdown), "Hello World")

    def test_no_h1(self):
        markdown = "## Subheader\nSome text"
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_empty_markdown(self):
        markdown = ""
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_multiple_h1(self):
        markdown = "# First Title\n# Second Title"
        self.assertEqual(extract_title(markdown), "First Title")

if __name__ == "__main__":
    unittest.main()