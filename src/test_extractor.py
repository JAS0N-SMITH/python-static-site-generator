import unittest
from extractor import extract_markdown_images, extract_markdown_links

class TestExtractor(unittest.TestCase):

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images2(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertEqual(extract_markdown_images(text), expected)

        text = "No images here!"
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_edge_cases(self):
        # Test with empty string
        text = ""
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

        # Test with malformed markdown image syntax
        text = "![alt text](missing-closing-parenthesis"
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

        text = "![alt text]missing-opening-parenthesis)"
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

        # Test with nested brackets
        text = "![alt [nested]](https://example.com/image.png)"
        expected = [("alt [nested]", "https://example.com/image.png")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]
        self.assertEqual(extract_markdown_links(text), expected)

        text = "No links here!"
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links_edge_cases(self):
        # Test with empty string
        text = ""
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

        # Test with malformed markdown link syntax
        text = "[anchor text](missing-closing-parenthesis"
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

        text = "[anchor text]missing-opening-parenthesis)"
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

        # Test with nested brackets
        text = "[anchor [nested]](https://example.com)"
        expected = [("anchor [nested]", "https://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)

if __name__ == "__main__":
    unittest.main()