import unittest

# Ensure LeafNode is defined in htmlnode module
from htmlnode import HTMLNode, HTMLLeafNode

class TestHtmlNode(unittest.TestCase):
    def test_htmlnode_creation(self):
        node = HTMLNode(tag='div', value='Hello, World!', children=[], props={'class': 'greeting'})
        self.assertEqual(node.tag, 'div')
        self.assertEqual(node.value, 'Hello, World!')
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {'class': 'greeting'})

        child_node = HTMLNode(tag='span', value='Child Node')
        node_with_children = HTMLNode(tag='div', value='Parent Node', children=[child_node])
        self.assertEqual(len(node_with_children.children), 1)
        self.assertEqual(node_with_children.children[0].tag, 'span')
        self.assertEqual(node_with_children.children[0].value, 'Child Node')

    def test_htmlnode_empty_content(self):
        node = HTMLNode(tag='br', value='')
        self.assertEqual(node.tag, 'br')
        self.assertEqual(node.value, '')
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {})

    def test_htmlnode_with_multiple_children(self):
        child1 = HTMLNode(tag='p', value='Paragraph 1')
        child2 = HTMLNode(tag='p', value='Paragraph 2')
        parent_node = HTMLNode(tag='div', value='Parent', children=[child1, child2])
        self.assertEqual(len(parent_node.children), 2)
        self.assertEqual(parent_node.children[0].tag, 'p')
        self.assertEqual(parent_node.children[0].value, 'Paragraph 1')
        self.assertEqual(parent_node.children[1].tag, 'p')
        self.assertEqual(parent_node.children[1].value, 'Paragraph 2')

    def test_htmlnode_with_props(self):
        node = HTMLNode(tag='img', value='', props={'src': 'image.png', 'alt': 'An image'})
        self.assertEqual(node.tag, 'img')
        self.assertEqual(node.value, '')
        self.assertEqual(node.props, {'src': 'image.png', 'alt': 'An image'})

    def test_htmlnode_defaults(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {})

    def test_htmlnode_without_tag(self):
        node = HTMLNode(value='Raw Text')
        self.assertIsNone(node.tag)
        self.assertEqual(node.value, 'Raw Text')
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {})

    def test_htmlnode_without_value(self):
        child = HTMLNode(tag='span', value='Child')
        node = HTMLNode(tag='div', children=[child])
        self.assertEqual(node.tag, 'div')
        self.assertIsNone(node.value)
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].tag, 'span')
        self.assertEqual(node.children[0].value, 'Child')

    def test_htmlnode_without_children(self):
        node = HTMLNode(tag='p', value='Paragraph')
        self.assertEqual(node.tag, 'p')
        self.assertEqual(node.value, 'Paragraph')
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {})

    def test_htmlnode_without_props(self):
        node = HTMLNode(tag='a', value='Link')
        self.assertEqual(node.tag, 'a')
        self.assertEqual(node.value, 'Link')
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {})

    def test_htmlnode_to_hml_not_implemented(self):
        node = HTMLNode(tag='div')
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_htmlnode_props_to_html(self):
        node = HTMLNode(tag='input', props={'type': 'text', 'value': 'Hello'})
        #  must have space before each prop but not after
        #  e.g. -> ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), ' type="text" value="Hello"')

    def test_leaf_to_html_p(self):
        node = HTMLLeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

if __name__ == '__main__':
    unittest.main()