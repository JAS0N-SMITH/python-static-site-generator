"""This module defines a TextNode class that represents a text element 
with various types (normal text, bold, italic, etc.)
"""

from enum import Enum


class TextType(Enum):
    TEXT = "Normal text"
    BOLD = "**Bold text**"
    ITALIC = "_Italic text_"
    CODE = "`Code text`"
    LINK = "[anchor text](url)"
    IMAGE = "![alt text](url)"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = None):
        if text_type is not None and not isinstance(text_type, TextType):
            raise ValueError(
                f"Invalid text_type: {text_type}. Must be an instance of TextType.")
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.name if self.text_type else None}, {self.url})"

    def __str__(self):
        if self.text_type == TextType.LINK:
            if not self.text:
                return "[]"
            return f"[{self.text}]({self.url or 'None'})"
        elif self.text_type == TextType.IMAGE:
            if not self.text:
                return "![]"
            return f"![{self.text}]({self.url or 'None'})"
        elif self.text_type is None:
            return "[]" if self.url else ""
        else:
            return self.text or ""
