from htmlnode import HTMLParentNode, HTMLLeafNode
from markdown_to_blocks import markdown_to_blocks
from block_type import block_to_block_type, BlockType
from converter import text_node_to_html_node
from textnode import TextNode, TextType
import re
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def markdown_to_html_node(markdown):
    """
    Converts a full markdown document into a single parent HTMLNode.

    Args:
        markdown (str): The markdown document to convert.

    Returns:
        HTMLParentNode: A single parent HTMLNode containing child nodes.
    """
    # Define inline patterns for formatting globally
    inline_patterns = [
        (r'\*\*(.*?)\*\*', "b"),  # Bold
        (r'_(.*?)_', "i"),           # Italic
        (r'\[(.*?)\]\((.*?)\)', "a"),  # Links
        (r'!\[(.*?)\]\((.*?)\)', "img"),  # Images
        (r'`(.*?)`', "code"),  # Inline code
    ]

    # Split the markdown into blocks
    blocks = markdown_to_blocks(markdown)

    # Create a parent HTML node (div)
    parent_node = HTMLParentNode(tag="div", children=[])

    for block in blocks:
        # Determine the type of block
        block_type = block_to_block_type(block)
        logging.debug(
            "Processing block: %s... identified as %s", block[:30], block_type)

        # Add detailed debug logging for block type detection
        logging.debug("Block content: %s", block)
        logging.debug("Detected block type: %s", block_type)

        # Map BlockType to correct HTML tags
        tag_mapping = {
            BlockType.PARAGRAPH: "p",
            # Default to h1 for simplicity; can be extended for other levels
            BlockType.HEADING: "h1",
            BlockType.CODE: "pre",
            BlockType.QUOTE: "blockquote",
            BlockType.UNORDERED_LIST: "ul",
            BlockType.ORDERED_LIST: "ol",
        }

        tag = tag_mapping.get(block_type, "div")

        if block_type == BlockType.CODE:
            # Special case for code blocks
            text_node = TextNode(block.strip("`\n"), text_type=TextType.CODE)
            html_node = HTMLParentNode(
                tag=tag, children=[text_node_to_html_node(text_node)])
        elif block_type == BlockType.HEADING:
            # Remove leading '#' characters and strip whitespace
            heading_content = block.lstrip('#').strip()
            text_node = TextNode(heading_content, text_type=TextType.TEXT)
            html_node = HTMLParentNode(
                tag=tag, children=[text_node_to_html_node(text_node)])
        # Ensure blockquote processing is logged in detail
        elif block_type == BlockType.QUOTE:
            logging.debug("Processing blockquote block: %s", block)
            quote_lines = block.splitlines()
            logging.debug("Split blockquote lines: %s", quote_lines)
            quote_content = '\n'.join(line.lstrip('> ').strip()
                                      for line in quote_lines if line.startswith('>'))
            logging.debug("Processed blockquote content: %s", quote_content)
            text_node = TextNode(quote_content, text_type=TextType.TEXT)
            html_node = HTMLParentNode(tag="blockquote", children=[
                text_node_to_html_node(text_node)])
            logging.debug("Final blockquote HTML node: %s",
                          html_node.to_html())
        elif block_type == BlockType.PARAGRAPH:
            # Ensure the parent tag is 'p' and handle inline formatting and links
            children = []
            last_index = 0
            # Update inline code processing to ensure all inline tags are preserved
            for pattern, tag in inline_patterns:
                matches = list(re.finditer(pattern, block))
                for match in matches:
                    start, end = match.span()
                    # Add text before the match
                    if start > last_index:
                        children.append(text_node_to_html_node(
                            TextNode(block[last_index:start], TextType.TEXT)))
                    # Add the formatted text or link
                    if tag == "a":
                        link_text, link_url = match.groups()
                        link_node = HTMLParentNode(tag="a", props={"href": link_url}, children=[
                            text_node_to_html_node(TextNode(link_text, TextType.TEXT))])
                        children.append(link_node)
                    elif tag == "i":
                        formatted_text = match.group(1)
                        italic_node = TextNode(formatted_text, TextType.ITALIC)
                        children.append(text_node_to_html_node(italic_node))
                    elif tag == "b":
                        formatted_text = match.group(1)
                        bold_node = TextNode(formatted_text, TextType.BOLD)
                        children.append(text_node_to_html_node(bold_node))
                    elif tag == "code":
                        formatted_text = match.group(1)
                        code_node = TextNode(formatted_text, TextType.CODE)
                        children.append(text_node_to_html_node(code_node))
                    last_index = end
            # Add remaining text after the last match
            if last_index < len(block):
                children.append(text_node_to_html_node(
                    TextNode(block[last_index:], TextType.TEXT)))
            html_node = HTMLParentNode(tag="p", children=children)
        elif block_type in [BlockType.UNORDERED_LIST, BlockType.ORDERED_LIST]:
            # Handle list items
            logging.debug("List block detected with tag: %s", tag)
            list_items = block.splitlines()
            list_children = []
            for item in list_items:
                if not item.strip():
                    continue  # Skip empty lines
                item_children = []
                # Strip list markers (e.g., '-' or '1.') from the beginning of the item
                if block_type == BlockType.UNORDERED_LIST:
                    item = item.lstrip('-').strip()
                elif block_type == BlockType.ORDERED_LIST:
                    item = re.sub(r'^\d+\.\s*', '', item).strip()

                # Process inline patterns within the list item
                last_index = 0
                for pattern, inline_tag in inline_patterns:
                    match = re.search(pattern, item)
                    if match:
                        start, end = match.span()
                        # Add text before the match
                        if start > last_index:
                            item_children.append(text_node_to_html_node(
                                TextNode(item[last_index:start], TextType.TEXT)))
                        # Add the formatted text or link
                        if inline_tag == "a":
                            link_text, link_url = match.groups()
                            link_node = HTMLParentNode(tag="a", props={"href": link_url}, children=[
                                text_node_to_html_node(TextNode(link_text, TextType.TEXT))])
                            logging.debug(
                                "Adding link node with attributes: %s", link_node)
                            item_children.append(link_node)
                        elif inline_tag == "i":
                            formatted_text = match.group(1)
                            italic_node = TextNode(
                                formatted_text, TextType.ITALIC)
                            logging.debug(
                                "Adding italic node: %s", italic_node)
                            item_children.append(
                                text_node_to_html_node(italic_node))
                        elif inline_tag == "b":
                            formatted_text = match.group(1)
                            bold_node = TextNode(formatted_text, TextType.BOLD)
                            logging.debug("Adding bold node: %s", bold_node)
                            item_children.append(
                                text_node_to_html_node(bold_node))
                        elif inline_tag == "code":
                            formatted_text = match.group(1)
                            code_node = TextNode(
                                formatted_text, TextType.CODE)
                            # Ensure inline <code> tags are processed correctly
                            # Add debug logging for inline code processing
                            logging.debug(
                                "Processing inline code: %s", formatted_text)
                            logging.debug("Adding code node: %s", code_node)
                            item_children.append(
                                text_node_to_html_node(code_node))
                        last_index = end
                # Add remaining text after the last match
                if last_index < len(item):
                    item_children.append(text_node_to_html_node(
                        TextNode(item[last_index:], TextType.TEXT)))
                list_children.append(HTMLParentNode(
                    tag="li", children=item_children))

            # Ensure the parent tag is correctly set as 'ul' or 'ol'
            html_node = HTMLParentNode(tag=tag, children=list_children)
            logging.debug("Finalized list node: %s", html_node.to_html())
        elif block_type == BlockType.CODE:
            # Wrap code blocks in <pre><code>
            code_content = block.strip('`\n')
            code_node = TextNode(code_content, text_type=TextType.CODE)
            html_node = HTMLParentNode(tag="pre", children=[
                HTMLParentNode(tag="code", children=[text_node_to_html_node(code_node)])])
            logging.debug("Processing code block: %s", block)
            logging.debug("Code content: %s", code_content)
            logging.debug("Generated code node: %s", code_node)
            logging.debug("Final code block HTML node: %s",
                          html_node.to_html())
        elif block_type == BlockType.IMAGE:
            # Handle image blocks
            match = re.match(r'!\[(.*?)\]\((.*?)\)', block)
            if match:
                alt_text, img_url = match.groups()
                html_node = HTMLLeafNode(
                    tag="img", props={"src": img_url, "alt": alt_text}
                )
            else:
                html_node = HTMLParentNode(tag="p", children=[
                    text_node_to_html_node(TextNode(block, TextType.TEXT))
                ])
        else:
            # Ensure a valid tag is provided for unrecognized block types
            html_node = HTMLParentNode(tag="div", children=[
                text_node_to_html_node(TextNode(block, TextType.TEXT))
            ])

        # Add the block node as a child of the parent node
        if not html_node.children and html_node.tag != "img":
            # Ensure parent nodes have at least one child
            placeholder_node = text_node_to_html_node(
                TextNode("", TextType.TEXT))
            html_node.children.append(placeholder_node)

        parent_node.children.append(html_node)

    return parent_node