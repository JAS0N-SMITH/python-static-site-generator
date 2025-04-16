import re

def markdown_to_blocks(markdown):
    """
    Converts a raw Markdown string into a list of "block" strings, where each block represents a distinct section of the document.

    Args:
        markdown (str): The input Markdown string to be converted.

    Returns:
        list: A list of strings representing the blocks of the Markdown document.
    """
    # Split the markdown text into blocks based on new lines and headings
    blocks = []
    for block in re.split(r'(\n\n|(?=^#))', markdown, flags=re.MULTILINE):
        block = block.strip()
        if block:
            blocks.append(block)

    return blocks

