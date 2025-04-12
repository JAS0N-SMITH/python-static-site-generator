import unittest
import sys
import os
from textnode import TextNode, TextType
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

class TestTextNode(unittest.TestCase):
    def setUp(self):
        self.normal_text_node = TextNode("This is normal text", TextType.NORMAL)
        self.bold_text_node = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.italic_text_node = TextNode("This is italic text", TextType.ITALIC_TEXT)
        self.code_text_node = TextNode("This is code text", TextType.CODE_TEXT)
        self.link_node = TextNode("This is a link", TextType.LINKS, "http://example.com")
        self.image_node = TextNode("This is an image", TextType.IMAGES, "http://example.com/image.jpg")

    def test_eq(self):
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(self.bold_text_node, node2)

    def test_neq(self):
        node2 = TextNode("This is a different text node", TextType.BOLD_TEXT)
        self.assertNotEqual(self.bold_text_node, node2)

    def test_repr(self):
        self.assertEqual(repr(self.bold_text_node), "TextNode(This is a text node, TextType.BOLD_TEXT, None)")

    def test_str(self):
        self.assertEqual(str(self.bold_text_node), "This is a text node")
        self.assertEqual(str(self.link_node), "[This is a link](http://example.com)")
        self.assertEqual(str(self.image_node), "![This is an image](http://example.com/image.jpg)")

    def test_str_no_url(self):
        link_node_no_url = TextNode("This is a link", TextType.LINKS)
        image_node_no_url = TextNode("This is an image", TextType.IMAGES)
        self.assertEqual(str(link_node_no_url), "[This is a link](None)")
        self.assertEqual(str(image_node_no_url), "![This is an image](None)")

    def test_str_no_text(self):
        bold_text_no_text = TextNode("", TextType.BOLD_TEXT)
        link_no_text = TextNode("", TextType.LINKS, "http://example.com")
        image_no_text = TextNode("", TextType.IMAGES, "http://example.com/image.jpg")
        self.assertEqual(str(bold_text_no_text), "")
        self.assertEqual(str(link_no_text), "[]")
        self.assertEqual(str(image_no_text), "![]")

    def test_str_no_text_no_url(self):
        link_no_text_no_url = TextNode("", TextType.LINKS)
        image_no_text_no_url = TextNode("", TextType.IMAGES)
        self.assertEqual(str(link_no_text_no_url), "[]")
        self.assertEqual(str(image_no_text_no_url), "![]")

    def test_str_no_text_no_url_no_type(self):
        node_no_type = TextNode("", None)
        node_no_type_with_url = TextNode("", None, "http://example.com")
        self.assertEqual(str(node_no_type), "")
        self.assertEqual(str(node_no_type_with_url), "[]")

    def test_normal_text(self):
        normal_text_node = TextNode("This is normal text", TextType.NORMAL)
        self.assertEqual(str(normal_text_node), "This is normal text")

    def test_italic_text(self):
        italic_text_node = TextNode("This is italic text", TextType.ITALIC_TEXT)
        self.assertEqual(str(italic_text_node), "This is italic text")

    def test_code_text(self):
        code_text_node = TextNode("This is code text", TextType.CODE_TEXT)
        self.assertEqual(str(code_text_node), "This is code text")

    def test_empty_textnode(self):
        empty_node = TextNode("", None)
        self.assertEqual(str(empty_node), "")

    def test_textnode_with_only_url(self):
        url_only_node = TextNode("", None, "http://example.com")
        self.assertEqual(str(url_only_node), "[]")

    def test_invalid_texttype(self):
        with self.assertRaises(ValueError):
            TextNode("Invalid type", "INVALID_TYPE")

    def test_equality_with_different_type(self):
        self.assertNotEqual(self.bold_text_node, "Not a TextNode")

    def test_missing_url_in_links_and_images(self):
        link_node_no_url = TextNode("This is a link", TextType.LINKS)
        image_node_no_url = TextNode("This is an image", TextType.IMAGES)
        self.assertEqual(str(link_node_no_url), "[This is a link](None)")
        self.assertEqual(str(image_node_no_url), "![This is an image](None)")

    def test_edge_cases_in_string_representation(self):
        special_char_node = TextNode("Special chars: !@#$%^&*()", TextType.NORMAL)
        long_text_node = TextNode("A" * 1000, TextType.NORMAL)
        multiline_text_node = TextNode("Line1\nLine2\nLine3", TextType.NORMAL)
        self.assertEqual(str(special_char_node), "Special chars: !@#$%^&*()")
        self.assertEqual(str(long_text_node), "A" * 1000)
        self.assertEqual(str(multiline_text_node), "Line1\nLine2\nLine3")

if __name__ == "__main__":
    unittest.main()