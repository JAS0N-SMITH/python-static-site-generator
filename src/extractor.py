# extractor.py
import re

def extract_markdown_images(text):
    """
    Extracts markdown images from the given text.

    Args:
        text (str): The raw markdown text.

    Returns:
        list: A list of tuples, each containing the alt text and URL of an image.
    """
    # Updated regular expression to handle nested brackets
    pattern = r'!\[([^\]]*(?:\[[^\]]*\][^\]]*)*)\]\(([^)]+)\)'
    
    # Find all matches in the text
    matches = re.findall(pattern, text)
    
    # Return a list of tuples (alt_text, url)
    return [(alt_text.strip(), url.strip()) for alt_text, url in matches]


def extract_markdown_links(text):
    """
    Extracts markdown links from the given text.

    Args:
        text (str): The raw markdown text.

    Returns:
        list: A list of tuples, each containing the anchor text and URL of a link.
    """
    # Updated regular expression to handle nested brackets
    pattern = r'\[([^\]]*(?:\[[^\]]*\][^\]]*)*)\]\(([^)]+)\)'
    
    # Find all matches in the text
    matches = re.findall(pattern, text)
    
    # Return a list of tuples (anchor_text, url)
    return [(anchor_text.strip(), url.strip()) for anchor_text, url in matches]
