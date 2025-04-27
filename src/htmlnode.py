import logging


"""
This module defines the HTMLNode class.

The HTMLNode class has 4 data members set in the constructor:

    tag - A string representing the HTML tag name (e.g., "p", "a", "h1", etc.)
    value - A string representing the value of the HTML tag (e.g., the text inside a paragraph)
    children - A list of HTMLNode objects representing the children of this node
    props - A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}
"""


class HTMLNode:
    """
    Initialize an HTMLNode instance.

    :param tag: The HTML tag name (e.g., "p", "a", "h1", etc.)
    :param value: The value of the HTML tag (e.g., the text inside a paragraph)
    :param children: A list of HTMLNode objects representing the children of this node
    :param props: A dictionary of key-value pairs representing the attributes of the HTML tag
    """

    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None):
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
    """
    Initialize an HTMLLeafNode instance.
    :param tag: The HTML tag name (e.g., "p", "a", "h1", etc.)
    :param value: The value of the HTML tag (e.g., the text inside a paragraph)
    :param props: A dictionary of key-value pairs representing the attributes of the HTML tag
    """

    def __init__(self, tag: str | None, value: str = None, props: dict = None):
        logging.debug(
            "Creating HTMLLeafNode with tag: %s, value: %s, props: %s", tag, value, props)
        if tag is None and value is None:
            logging.error(
                "HTMLLeafNode is being created without a tag and without a value. Props: %s", props)
            raise ValueError("HTMLLeafNode must have a tag or a value.")
        super().__init__(tag=tag, value=value, props=props)
        self.children = []

    def to_html(self):
        if self.tag is None:
            # Return plain text if no tag is provided
            if self.value is None:
                raise ValueError("Leaf nodes with no tag must have a value.")
            return self.value
        if self.tag == "img":
            # Handle self-closing tags like <img>
            return f"<{self.tag}{self.props_to_html()} />"
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class HTMLParentNode(HTMLNode):
    """ 
    The tag and children arguments are not optional
    It doesn't take a value argument
    props is optional
    (It's the exact opposite of the LeafNode class)
    :param tag: The HTML tag name (e.g., "p", "a", "h1", etc.)
    :param children: A list of HTMLNode objects representing the children of this node
    :param props: A dictionary of key-value pairs representing the attributes of the HTML tag
    """

    def __init__(self, tag: str, children: list = None, props: dict = None):
        if children is None:
            children = []
        super().__init__(tag=tag, value=None, children=children, props=props)
        self.value = None
        # Ensure children is always a list
        if not isinstance(self.children, list):
            raise TypeError("children must be a list")
        # Ensure props is always a dictionary
        if not isinstance(self.props, dict):
            raise TypeError("props must be a dictionary")
        # Ensure tag is provided
        if self.tag is None:
            raise ValueError("tag must be provided")
        # Ensure all children are HTMLNode instances
        for child in self.children:
            if not isinstance(child, HTMLNode):
                raise TypeError("children must be HTMLNode instances")

    def to_html(self):
        """
        Generate an HTML string representation of the node and its children.

        This method recursively calls `to_html` on each child node, concatenating their
        HTML representations. The resulting HTML is wrapped between the opening and 
        closing tags of the parent node.

        :raises ValueError: If the node does not have a tag or if it has no children.
        :return: A string representing the HTML structure of the node and its children.
        """
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag.")
        if not self.children:
            logging.error(
                "Parent node with tag '%s' has no children. Node details: %s", self.tag, self)
            raise ValueError("All parent nodes must have children.")
        children_html = ''.join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
