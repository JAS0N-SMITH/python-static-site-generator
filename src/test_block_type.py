import unittest
from block_type import BlockType, block_to_block_type

class TestBlockType(unittest.TestCase):

    def test_paragraph(self):
        block = "This is a simple paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading(self):
        block = "# Heading 1"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code_block(self):
        block = """```
        def hello():
            return 'world'
        ```"""
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_block(self):
        block = "> This is a quote.\n> Another line of the quote."
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_empty_block(self):
        block = ""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_mixed_content(self):
        block = "# Heading\nThis is a paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_incorrect_heading_format(self):
        block = "####Heading without space"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_incorrect_ordered_list(self):
        block = "1. First item\n3. Skipped number"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_incorrect_unordered_list(self):
        block = "-Item without space"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()