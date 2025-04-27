def extract_title(markdown):
    """
    Extract the H1 header from a markdown string.

    Args:
        markdown (str): The markdown content as a string.

    Returns:
        str: The content of the H1 header without the leading '#' and stripped of whitespace.

    Raises:
        ValueError: If no H1 header is found in the markdown.
    """
    for line in markdown.splitlines():
        line = line.strip()
        if line.startswith('# ') and len(line) > 2:
            return line[2:].strip()
    raise ValueError("No H1 header found in the markdown.")