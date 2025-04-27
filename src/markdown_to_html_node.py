from htmlnode import HTMLParentNode
from markdown_to_blocks import markdown_to_blocks
from block_type import block_to_block_type, BlockType
from converter import text_node_to_html_node
from text_to_textnode import text_to_textnode
from textnode import TextNode, TextType

def markdown_to_html_node(markdown):
    """
    Converts a full markdown document into a single parent HTMLNode.

    Args:
        markdown (str): The markdown document to convert.

    Returns:
        HTMLParentNode: A single parent HTMLNode containing child nodes.
    """
    # Split the markdown into blocks
    blocks = markdown_to_blocks(markdown)

    # Create a parent HTML node (div)
    parent_node = HTMLParentNode(tag="div", children=[])

    for block in blocks:
        # Determine the type of block
        block_type = block_to_block_type(block)

        if block_type == BlockType.CODE:
            # Special case for code blocks
            text_node = TextNode(block.strip("`\n"), text_type=TextType.CODE)
            html_node = HTMLParentNode(tag="code", children=[text_node_to_html_node(text_node)])
        else:
            # For other block types, use text_to_children
            child_nodes = text_to_textnode(block)
            html_node = HTMLParentNode(tag=block_type.value, children=[text_node_to_html_node(node) for node in child_nodes])

        # Add the block node as a child of the parent node
        parent_node.children.append(html_node)

    return parent_node