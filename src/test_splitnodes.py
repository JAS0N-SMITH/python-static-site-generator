"""
Unit tests for the splitnodes module, specifically testing the split_nodes_delimiter function.
"""

import unittest
from splitnodes import split_nodes_delimiter, split_nodes_image, split_nodes_link
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

    def test_split_nodes_image(self):
        """
        Test splitting text with markdown image syntax.
        """
        node = TextNode(
            "This is an image ![alt text](https://example.com/image.png) in text", TextType.TEXT)
        new_nodes = split_nodes_image([node])

        expected_nodes = [
            TextNode("This is an image ", TextType.TEXT),
            TextNode("alt text", TextType.IMAGE),
            TextNode("https://example.com/image.png", TextType.TEXT),
            TextNode(" in text", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_image_multiple(self):
        """
        Test splitting text with multiple markdown image syntaxes.
        """
        node = TextNode(
            "Image1 ![alt1](url1) and Image2 ![alt2](url2)", TextType.TEXT)
        new_nodes = split_nodes_image([node])

        expected_nodes = [
            TextNode("Image1 ", TextType.TEXT),
            TextNode("alt1", TextType.IMAGE),
            TextNode("url1", TextType.TEXT),
            TextNode(" and Image2 ", TextType.TEXT),
            TextNode("alt2", TextType.IMAGE),
            TextNode("url2", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_image_malformed(self):
        """
        Test splitting text with malformed markdown image syntax.
        """
        node = TextNode(
            "This is a malformed image ![alt text](url", TextType.TEXT)
        new_nodes = split_nodes_image([node])

        expected_nodes = [
            TextNode(
                "This is a malformed image ![alt text](url", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_link(self):
        """
        Test splitting text with markdown link syntax.
        """
        node = TextNode(
            "This is a link [example](https://example.com) in text", TextType.TEXT)
        new_nodes = split_nodes_link([node])

        expected_nodes = [
            TextNode("This is a link ", TextType.TEXT),
            TextNode("example", TextType.LINK),
            TextNode("https://example.com", TextType.TEXT),
            TextNode(" in text", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_link_multiple(self):
        """
        Test splitting text with multiple markdown link syntaxes.
        """
        node = TextNode(
            "Link1 [text1](url1) and Link2 [text2](url2)", TextType.TEXT)
        new_nodes = split_nodes_link([node])

        expected_nodes = [
            TextNode("Link1 ", TextType.TEXT),
            TextNode("text1", TextType.LINK),
            TextNode("url1", TextType.TEXT),
            TextNode(" and Link2 ", TextType.TEXT),
            TextNode("text2", TextType.LINK),
            TextNode("url2", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_link_malformed(self):
        """
        Test splitting text with malformed markdown link syntax.
        """
        node = TextNode("This is a malformed link [text](url", TextType.TEXT)
        new_nodes = split_nodes_link([node])

        expected_nodes = [
            TextNode("This is a malformed link [text](url", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected_nodes)

if __name__ == "__main__":
    unittest.main()