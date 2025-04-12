"""
This module contains a function that converts a TextNode to an HTMLLeafNode.
It handles different types of text nodes and raises exceptions for invalid types.
It imports the HTMLLeafNode class from the htmlnode module and the TextNode class and TextType enum from the textnode module.
It is designed to be used in a larger application that deals with HTML generation and text formatting.
"""
from htmlnode import HTMLLeafNode
from textnode import TextNode, TextType

def text_node_to_html_node(text_node: TextNode) -> HTMLLeafNode:
    """
    Converts a TextNode to an HTMLLeafNode based on its TextType.

    Args:
        text_node (TextNode): The TextNode to convert.

    Returns:
        HTMLLeafNode: The corresponding HTMLLeafNode representation.

    Raises:
        ValueError: If the TextNode has an invalid TextType.
    """
    tag_mapping = {
        TextType.TEXT: (None, text_node.text, None),
        TextType.BOLD: ("b", text_node.text, None),
        TextType.ITALIC: ("i", text_node.text, None),
        TextType.CODE: ("code", text_node.text, None),
        TextType.LINK: ("a", text_node.text, {"href": text_node.url}),
        TextType.IMAGE: ("img", "", {"alt": text_node.text, "src": text_node.url}),
    }

    if text_node.text_type in tag_mapping:
        tag, value, props = tag_mapping[text_node.text_type]
        return HTMLLeafNode(tag, value, props)
    else:
        valid_types = ", ".join([t.name for t in TextType])
        raise ValueError(f"Invalid TextType: {text_node.text_type}. Valid types are: {valid_types}")
