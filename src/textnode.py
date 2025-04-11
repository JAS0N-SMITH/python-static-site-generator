from enum import Enum

class TextType(Enum):
	NORMAL = "Normal text"
	BOLD_TEXT = "**Bold text**"
	ITALIC_TEXT = "_Italic text_"
	CODE_TEXT = "`Code text`"
	LINKS = "[anchor text](url)"
	IMAGES = "![alt text](url)"

class TextNode:
	def __init__(self, text: str, text_type: TextType, url: str = None):
		self.text = text
		self.text_type = text_type
		self.url = url

	def __eq__(self, other):
		if not isinstance(other, TextNode):
			return False
		return self.text == other.text and self.text_type == other.text_type and self.url == other.url

	def __repr__(self):
		return f"TextNode({self.text}, {self.text_type}, {self.url})"

	def __str__(self):
		if self.text_type == TextType.LINKS:
			return f"[{self.text}]({self.url})"
		elif self.text_type == TextType.IMAGES:
			return f"![{self.text}]({self.url})"
		else:
			return self.text