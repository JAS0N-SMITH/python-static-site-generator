"""
Unit tests for the splitnodes module, specifically testing the split_nodes_delimiter function.
"""

import unittest
from splitnodes import split_nodes_delimiter
from textnode import TextNode, TextType

class TestSplitNodes(unittest.TestCase):
    """
    Test cases for the split_nodes_delimiter function.
    """

    def test_split_nodes_with_code_delimiter(self):
        """
        Test splitting text with a `code block` delimiter.
        """
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_with_bold_delimiter(self):
        """
        Test splitting text with a **bold** delimiter.
        """
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_with_no_delimiter(self):
        """
        Test splitting text with no delimiter present.
        """
        node = TextNode("This is plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        expected_nodes = [
            TextNode("This is plain text", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_with_empty_text(self):
        """
        Test splitting an empty text node.
        """
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        expected_nodes = [
            TextNode("", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected_nodes)

if __name__ == "__main__":
    unittest.main()