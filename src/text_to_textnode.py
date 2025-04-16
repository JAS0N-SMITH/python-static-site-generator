from splitnodes import split_nodes_delimiter, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType

def text_to_textnode(text):
    """
    Converts a string of text into a list of TextNode objects based on various formatting rules.

    Args:
        text (str): The input text to be converted.

    Returns:
        list: A list of TextNode objects representing the formatted text.
    """
    # Split the text into nodes based on delimiters
    nodes = split_nodes_delimiter([TextNode(text, TextType.TEXT)], '**', TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, '_', TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
    
    # Further split the nodes based on images
    nodes = split_nodes_image(nodes)
    
    # Further split the nodes based on links
    nodes = split_nodes_link(nodes)

    return nodes

