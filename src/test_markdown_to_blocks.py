import unittest
from markdown_to_blocks import markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_markdown(self):
        md = """"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    # Test for markdown with only a single paragraph
    def test_single_paragraph(self):
        md = """This is a single paragraph."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single paragraph."])

    # Test for markdown with multiple paragraphs
    def test_multiple_paragraphs(self):
        md = """This is the first paragraph.

This is the second paragraph."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is the first paragraph.", "This is the second paragraph."])

    # Test for markdown with a list
    def test_list(self):
        md = """- Item 1
- Item 2
- Item 3"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["- Item 1\n- Item 2\n- Item 3"])

    # Test for markdown with mixed content
    def test_mixed_content(self):
        md = """This is a paragraph.

- List item 1
- List item 2

Another paragraph."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [
            "This is a paragraph.",
            "- List item 1\n- List item 2",
            "Another paragraph."
        ])

    # Test for markdown with only whitespace
    def test_whitespace_markdown(self):
        md = """   \n   \n   """
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    # Test for markdown with special characters
    def test_special_characters(self):
        md = """!@#$%^&*()_+{}|:"<>?~`"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["!@#$%^&*()_+{}|:\"<>?~`"])

    # Test for markdown with nested lists
    def test_nested_lists(self):
        md = """- Item 1
  - Subitem 1.1
  - Subitem 1.2
- Item 2"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["- Item 1\n  - Subitem 1.1\n  - Subitem 1.2\n- Item 2"])

    # Test for markdown with headings
    def test_headings(self):
        md = """# Heading 1
## Heading 2
### Heading 3"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["# Heading 1", "## Heading 2", "### Heading 3"])

    # Test for markdown with code blocks
    def test_code_blocks(self):
        md = """```
def example_function():
    pass
```"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["```\ndef example_function():\n    pass\n```"])

    # Test for markdown with inline HTML
    def test_inline_html(self):
        md = """<div>This is a div</div>"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["<div>This is a div</div>"])

if __name__ == '__main__':
    unittest.main()
