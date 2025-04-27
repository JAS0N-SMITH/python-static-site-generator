import unittest
from markdown_to_html_node import markdown_to_html_node
from htmlnode import HTMLParentNode

class TestMarkdownToHtmlNode(unittest.TestCase):

    def test_empty_markdown(self):
        """Test that an empty markdown string returns an empty div node."""
        result = markdown_to_html_node("")
        self.assertIsInstance(result, HTMLParentNode)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 0)

    def test_single_paragraph(self):
        """Test a single paragraph block."""
        markdown = "This is a single paragraph."
        result = markdown_to_html_node(markdown)
        self.assertEqual(len(result.children), 1)
        self.assertEqual(result.children[0].tag, "paragraph")
        self.assertEqual(result.children[0].children[0].value, "This is a single paragraph.")

    def test_code_block(self):
        """Test a code block."""
        markdown = "```\ndef example_function():\n    pass\n```"
        result = markdown_to_html_node(markdown)
        self.assertEqual(len(result.children), 1)
        self.assertEqual(result.children[0].tag, "code")
        self.assertEqual(result.children[0].children[0].value, "def example_function():\n    pass")

    def test_mixed_blocks(self):
        """Test mixed block types including paragraph and code."""
        markdown = "This is a paragraph.\n\n```\ndef example_function():\n    pass\n```"
        result = markdown_to_html_node(markdown)
        self.assertEqual(len(result.children), 2)
        self.assertEqual(result.children[0].tag, "paragraph")
        self.assertEqual(result.children[0].children[0].value, "This is a paragraph.")
        self.assertEqual(result.children[1].tag, "code")
        self.assertEqual(result.children[1].children[0].value, "def example_function():\n    pass")

    def test_inline_formatting(self):
        """Test inline formatting within a paragraph."""
        markdown = "This is **bold** and _italic_ text."
        result = markdown_to_html_node(markdown)
        self.assertEqual(len(result.children), 1)
        self.assertEqual(result.children[0].tag, "paragraph")
        self.assertEqual(len(result.children[0].children), 5)
        self.assertEqual(result.children[0].children[1].tag, "b")
        self.assertEqual(result.children[0].children[1].value, "bold")
        self.assertEqual(result.children[0].children[3].tag, "i")
        self.assertEqual(result.children[0].children[3].value, "italic")

if __name__ == "__main__":
    unittest.main()