from typing import Optional

"""define a class called HTMLNode in it.

The HTMLNode class should have 4 data members set in the constructor:

    tag - A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
    value - A string representing the value of the HTML tag (e.g. the text inside a paragraph)
    children - A list of HTMLNode objects representing the children of this node
    props - A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}

"""

class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None):
        """
        Initialize an HTMLNode instance.

        :param tag: The HTML tag name (e.g., "p", "a", "h1", etc.)
        :param value: The value of the HTML tag (e.g., the text inside a paragraph)
        :param children: A list of HTMLNode objects representing the children of this node
        :param props: A dictionary of key-value pairs representing the attributes of the HTML tag
        """
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

        # Ensure children is always a list
        if not isinstance(self.children, list):
            raise TypeError("children must be a list")
        # Ensure props is always a dictionary
        if not isinstance(self.props, dict):
            raise TypeError("props must be a dictionary")
        # Ensure tag is either None or a string
        if self.tag is not None and not isinstance(self.tag, str):
            raise TypeError("tag must be a string or None")
        # Ensure value is either None or a string
        if self.value is not None and not isinstance(self.value, str):
            raise TypeError("value must be a string or None")
        # Ensure all children are HTMLNode instances
        for child in self.children:
            if not isinstance(child, HTMLNode):
                raise TypeError("children must be HTMLNode instances")
        # Ensure all props keys and values are strings
        for key, value in self.props.items():
            if not isinstance(key, str) or not isinstance(value, str):
                raise TypeError("props keys and values must be strings")
        
    def to_html(self):
        raise NotImplementedError("to_hml method is not implemented yet")
    
    def props_to_html(self):
        return "".join([f' {key}="{value}"' for key, value in self.props.items()])
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    
# create child class for leaf nodes
class HTMLLeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: dict = None):
        super().__init__(tag=tag, value=value, props=props)
        self.children = []
    
    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"