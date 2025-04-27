from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block: str) -> BlockType:
    if not block.strip():
        return BlockType.PARAGRAPH

    lines = block.splitlines()

    # Check for heading
    if lines[0].startswith(tuple(f"{'#' * i} " for i in range(1, 7))):
        return BlockType.HEADING

    # Check for code block
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    # Check for quote block
    if all(line.startswith("> ") for line in lines):
        return BlockType.QUOTE

    # Check for unordered list block
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # Check for ordered list block
    try:
        if all(line.startswith(f"{i}. ") for i, line in enumerate(lines, start=1)):
            return BlockType.ORDERED_LIST
    except ValueError:
        pass

    # Default to paragraph
    return BlockType.PARAGRAPH