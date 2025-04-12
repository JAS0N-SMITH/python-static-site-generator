import unittest
from parameterized import parameterized
from textnode import TextNode, TextType
from converter import text_node_to_html_node

class TestConverter(unittest.TestCase):

    @parameterized.expand([
        ("text", TextType.TEXT, "Sample text", None, "Sample text", None),
        ("bold", TextType.BOLD, "Bold text", "b", "Bold text", None),
        ("italic", TextType.ITALIC, "Italic text", "i", "Italic text", None),
        ("code", TextType.CODE, "Code snippet", "code", "Code snippet", None),
        ("link", TextType.LINK, "Click here", "a", "Click here", {"href": "http://example.com"}),
        ("image", TextType.IMAGE, "Alt text", "img", "", {"alt": "Alt text", "src": "http://example.com/image.png"}),
    ])
    def test_text_node_to_html_node(self, text_type, text, expected_tag, expected_value, expected_props):
        if text_type == TextType.LINK or text_type == TextType.IMAGE:
            text_node = TextNode(text_type=text_type, text=text, url="http://example.com" if text_type == TextType.LINK else "http://example.com/image.png")
        else:
            text_node = TextNode(text_type=text_type, text=text)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, expected_tag)
        self.assertEqual(html_node.value, expected_value)
        if expected_props:
            self.assertEqual(html_node.props, expected_props)

    def test_text_node_to_html_node_invalid_type(self):
        with self.assertRaises(ValueError) as context:
            text_node = TextNode(text_type="INVALID_TYPE", text="Invalid text")
            text_node_to_html_node(text_node)
        self.assertEqual(str(context.exception), "Invalid text_type: INVALID_TYPE. Must be an instance of TextType.")

    def test_text_node_to_html_node_empty_text(self):
        text_node = TextNode(text_type=TextType.TEXT, text="")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "")

if __name__ == "__main__":
    unittest.main()