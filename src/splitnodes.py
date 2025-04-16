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
from extractor import extract_markdown_images, extract_markdown_links

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
                        TextNode(
                            part,
                            text_type if i % 2 == 1 else node.text_type or TextType.TEXT
                        )
                    )
        else:
            new_nodes.append(node)  # Append non-TextNode objects as-is

    return new_nodes

# Now that we have the extraction functions, we will need to be able to split raw markdown text into TextNodes based on images and links.
# '''


def split_nodes_image(old_nodes):
    """
    Splits a list of text nodes into smaller nodes based on markdown images.

    Args:
        old_nodes (list): A list of TextNode objects to process.

    Returns:
        list: A new list of TextNode objects with the images extracted and types assigned.
    """
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode):
            if not node.text:  # Preserve empty TextNode
                new_nodes.append(node)
                continue

            matches = extract_markdown_images(node.text)
            if matches:
                remaining_text = node.text
                for alt_text, url in matches:
                    pre_text, remaining_text = remaining_text.split(
                        f"![{alt_text}]({url})", 1)
                    if pre_text:
                        new_nodes.append(TextNode(pre_text, TextType.TEXT))
                    new_nodes.append(TextNode(alt_text, TextType.IMAGE))
                    new_nodes.append(TextNode(url, TextType.TEXT))
                if remaining_text:
                    new_nodes.append(TextNode(remaining_text, TextType.TEXT))
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)  # Append non-TextNode objects as-is

    return new_nodes


def split_nodes_link(old_nodes):
    """
    Splits a list of text nodes into smaller nodes based on markdown links.

    Args:
        old_nodes (list): A list of TextNode objects to process.

    Returns:
        list: A new list of TextNode objects with the links extracted and types assigned.
    """
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode):
            if not node.text:  # Preserve empty TextNode
                new_nodes.append(node)
                continue

            matches = extract_markdown_links(node.text)
            if matches:
                remaining_text = node.text
                for anchor_text, url in matches:
                    pre_text, remaining_text = remaining_text.split(
                        f"[{anchor_text}]({url})", 1)
                    if pre_text:
                        new_nodes.append(TextNode(pre_text, TextType.TEXT))
                    new_nodes.append(TextNode(anchor_text, TextType.LINK))
                    new_nodes.append(TextNode(url, TextType.TEXT))
                if remaining_text:
                    new_nodes.append(TextNode(remaining_text, TextType.TEXT))
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)  # Append non-TextNode objects as-is

    return new_nodes


# Example usage:
# node = TextNode(
#     "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
#     TextType.TEXT,
# )
# new_nodes = split_nodes_link([node])
# [
#     TextNode("This is text with a link ", TextType.TEXT),
#     TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
#     TextNode(" and ", TextType.TEXT),
#     TextNode(
#         "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
#     ),
# ]
