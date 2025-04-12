"""
This module provides functionality to split text nodes into smaller nodes based on delimiters, enabling the conversion of raw markdown strings into structured text nodes. For example, the string:

    This is text with a **bolded phrase** in the middle

Can be split into:

    [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("bolded phrase", TextType.BOLD),
        TextNode(" in the middle", TextType.TEXT),
    ]

Nested inline elements are not supported for simplicity. For instance, we do not handle cases like:

    This is an _italic and **bold** word_.

Functions:
    split_nodes_delimiter(old_nodes, delimiter, text_type):
        Splits text nodes based on a given delimiter and assigns the specified text type to the delimited segments.
"""

from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Splits a list of text nodes into smaller nodes based on a delimiter.

    Args:
        old_nodes (list): A list of TextNode objects to process.
        delimiter (str): The delimiter to split the text on (e.g., `**`, `_`, or `` ` ``).
        text_type (TextType): The type to assign to the delimited segments.

    Returns:
        list: A new list of TextNode objects with the text split and types assigned.
    """
    new_nodes = []

    for node in old_nodes:
        if isinstance(node, TextNode):
            if not node.text:  # Preserve empty TextNode
                new_nodes.append(node)
                continue

            parts = node.text.split(delimiter)
            for i, part in enumerate(parts):
                if part.strip():  # Ignore empty segments
                    new_nodes.append(
                        TextNode(part, text_type if i % 2 == 1 else TextType.TEXT)
                    )
        else:
            new_nodes.append(node)  # Append non-TextNode objects as-is

    return new_nodes