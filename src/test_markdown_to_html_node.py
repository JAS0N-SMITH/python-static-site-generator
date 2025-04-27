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
        self.assertEqual(result.children[0].tag, "p")
        self.assertEqual(result.children[0].children[0].value, "This is a single paragraph.")

    def test_code_block(self):
        """Test a code block."""
        markdown = "```\ndef example_function():\n    pass\n```"
        result = markdown_to_html_node(markdown)
        self.assertEqual(len(result.children), 1)
        self.assertEqual(result.children[0].tag, "pre")
        self.assertEqual(result.children[0].children[0].value, "def example_function():\n    pass")

    def test_mixed_blocks(self):
        """Test mixed block types including paragraph and code."""
        markdown = "This is a paragraph.\n\n```\ndef example_function():\n    pass\n```"
        result = markdown_to_html_node(markdown)
        self.assertEqual(len(result.children), 2)
        self.assertEqual(result.children[0].tag, "p")
        self.assertEqual(result.children[0].children[0].value, "This is a paragraph.")
        self.assertEqual(result.children[1].tag, "pre")
        self.assertEqual(result.children[1].children[0].value, "def example_function():\n    pass")

    def test_inline_formatting(self):
        """Test inline formatting within a paragraph."""
        markdown = "This is **bold** and _italic_ text."
        result = markdown_to_html_node(markdown)
        self.assertEqual(len(result.children), 1)
        self.assertEqual(result.children[0].tag, "p")
        self.assertEqual(len(result.children[0].children), 5)
        self.assertEqual(result.children[0].children[1].tag, "b")
        self.assertEqual(result.children[0].children[1].value, "bold")
        self.assertEqual(result.children[0].children[3].tag, "i")
        self.assertEqual(result.children[0].children[3].value, "italic")

    def test_heading_conversion(self):
        """Test that markdown headings properly strip '#' characters."""
        markdown = "# Heading 1"
        result = markdown_to_html_node(markdown)
        self.assertEqual(len(result.children), 1)
        self.assertEqual(result.children[0].tag, "h1")
        self.assertEqual(result.children[0].children[0].value, "Heading 1")

    def test_inline_formatting_in_list(self):
        """Test inline formatting within list items."""
        markdown = """\
- _italic_ text
- **bold** text
- [link](https://example.com)
"""
        result = markdown_to_html_node(markdown)
        self.assertEqual(len(result.children), 1)  # One unordered list
        self.assertEqual(result.children[0].tag, "ul")
        # Three list items
        self.assertEqual(len(result.children[0].children), 3)

        # Check first list item (italic text)
        self.assertEqual(result.children[0].children[0].tag, "li")
        self.assertEqual(len(result.children[0].children[0].children), 1)
        self.assertEqual(result.children[0].children[0].children[0].tag, "i")
        self.assertEqual(
            result.children[0].children[0].children[0].value, "italic")

        # Check second list item (bold text)
        self.assertEqual(result.children[0].children[1].tag, "li")
        self.assertEqual(len(result.children[0].children[1].children), 1)
        self.assertEqual(result.children[0].children[1].children[0].tag, "b")
        self.assertEqual(
            result.children[0].children[1].children[0].value, "bold")

        # Check third list item (link)
        self.assertEqual(result.children[0].children[2].tag, "li")
        self.assertEqual(len(result.children[0].children[2].children), 1)
        self.assertEqual(result.children[0].children[2].children[0].tag, "a")
        self.assertEqual(
            result.children[0].children[2].children[0].props["href"], "https://example.com")
        self.assertEqual(
            result.children[0].children[2].children[0].children[0].value, "link")

    def test_expected_tags(self):
        """Test that all expected tags are correctly generated."""
        markdown = """# Tolkien Fan Club

- _italic_ text
- **bold** text
- [link](https://example.com)

> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien

```
def main():
    print("Hello, world!")
```
"""
        result = markdown_to_html_node(markdown)

        # Check heading
        self.assertEqual(result.children[0].tag, "h1")
        self.assertEqual(
            result.children[0].children[0].value, "Tolkien Fan Club")

        # Check list
        self.assertEqual(result.children[1].tag, "ul")
        self.assertEqual(len(result.children[1].children), 3)
        self.assertEqual(result.children[1].children[0].children[0].tag, "i")
        self.assertEqual(result.children[1].children[1].children[0].tag, "b")
        self.assertEqual(result.children[1].children[2].children[0].tag, "a")

        # Check blockquote
        self.assertEqual(result.children[2].tag, "blockquote")
        self.assertIn("I am in fact a Hobbit in all but size.",
                      result.children[2].children[0].value)

        # Check code block
        self.assertEqual(result.children[3].tag, "pre")
        self.assertEqual(result.children[3].children[0].tag, "code")
        self.assertIn(
            "def main():", result.children[3].children[0].value)

    def test_image_conversion(self):
        """Test that markdown image syntax is converted to an <img> tag."""
        markdown = "![JRR Tolkien sitting](/images/tolkien.png)"
        result = markdown_to_html_node(markdown)
        self.assertEqual(len(result.children), 1)
        self.assertEqual(result.children[0].tag, "img")
        self.assertEqual(
            result.children[0].props["src"], "/images/tolkien.png")
        self.assertEqual(
            result.children[0].props["alt"], "JRR Tolkien sitting")

if __name__ == "__main__":
    unittest.main()