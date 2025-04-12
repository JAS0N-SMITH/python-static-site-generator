import unittest
from htmlnode import HTMLNode, HTMLLeafNode, HTMLParentNode


class TestHTMLNode(unittest.TestCase):
    """Tests for the HTMLNode class."""

    def setUp(self):
        self.default_props = {'class': 'greeting'}
        self.child_node = HTMLNode(tag='span', value='Child Node')

    def test_creation_with_all_attributes(self):
        """Test creating an HTMLNode with all attributes."""
        node = HTMLNode(tag='div', value='Hello, World!',
                        children=[], props=self.default_props)
        self.assertEqual(node.tag, 'div')
        self.assertEqual(node.value, 'Hello, World!')
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, self.default_props)

    def test_creation_with_children(self):
        """Test creating an HTMLNode with children."""
        node = HTMLNode(tag='div', value='Parent Node',
                        children=[self.child_node])
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].tag, 'span')
        self.assertEqual(node.children[0].value, 'Child Node')

    def test_creation_with_empty_content(self):
        """Test creating an HTMLNode with empty content."""
        node = HTMLNode(tag='br', value='')
        self.assertEqual(node.tag, 'br')
        self.assertEqual(node.value, '')
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {})

    def test_props_to_html(self):
        """Test converting props to HTML string."""
        node = HTMLNode(tag='input', props={'type': 'text', 'value': 'Hello'})
        self.assertEqual(node.props_to_html(), ' type="text" value="Hello"')

    def test_to_html_not_implemented(self):
        """Test that to_html raises NotImplementedError."""
        node = HTMLNode(tag='div')
        with self.assertRaises(NotImplementedError):
            node.to_html()


class TestHTMLLeafNode(unittest.TestCase):
    """Tests for the HTMLLeafNode class."""

    def test_to_html(self):
        """Test converting a leaf node to HTML."""
        node = HTMLLeafNode(tag='p', value='Hello, world!')
        self.assertEqual(node.to_html(), '<p>Hello, world!</p>')


class TestHTMLParentNode(unittest.TestCase):
    """Tests for the HTMLParentNode class."""

    def setUp(self):
        self.child1 = HTMLLeafNode(tag='p', value='Paragraph 1')
        self.child2 = HTMLLeafNode(tag='p', value='Paragraph 2')
        self.props = {'class': 'container'}
        self.parent_node = HTMLParentNode(
            tag='div', children=[self.child1, self.child2], props=self.props)

    def test_creation(self):
        """Test creating an HTMLParentNode."""
        self.assertEqual(self.parent_node.tag, 'div')
        self.assertEqual(self.parent_node.props, self.props)
        self.assertEqual(len(self.parent_node.children), 2)
        self.assertEqual(self.parent_node.children[0].tag, 'p')
        self.assertEqual(
            self.parent_node.children[0].value, 'Paragraph 1')

    def test_to_html(self):
        """Test converting a parent node to HTML."""
        expected_html = '<div class="container"><p>Paragraph 1</p><p>Paragraph 2</p></div>'
        self.assertEqual(self.parent_node.to_html(), expected_html)

    def test_creation_without_children_raises_error(self):
        """Test that creating a parent node without children raises ValueError."""
        with self.assertRaises(ValueError):
            HTMLParentNode(tag='div', children=[])

    def test_creation_without_tag_raises_error(self):
        """Test that creating a parent node without a tag raises ValueError."""
        with self.assertRaises(ValueError):
            HTMLParentNode(tag=None, children=[self.child1])

    def test_invalid_children_type_raises_error(self):
        """Test that invalid children type raises TypeError."""
        with self.assertRaises(TypeError):
            HTMLParentNode(tag='div', children=['not_a_node'])

    def test_props_to_html(self):
        """Test converting props to HTML string."""
        self.assertEqual(self.parent_node.props_to_html(),
                         ' class="container"')

    def test_to_html_with_children(self):
        """Test converting a parent node with children to HTML."""
        child_node = HTMLLeafNode("span", "child")
        parent_node = HTMLParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),
                         "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        """Test converting a parent node with grandchildren to HTML."""
        grandchild_node = HTMLLeafNode("b", "grandchild")
        child_node = HTMLParentNode("span", [grandchild_node])
        parent_node = HTMLParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_nested_levels(self):
        """Test converting a deeply nested parent node to HTML."""
        level3 = HTMLLeafNode("i", "level3")
        level2 = HTMLParentNode("span", [level3])
        level1 = HTMLParentNode("div", [level2])
        self.assertEqual(
            level1.to_html(),
            "<div><span><i>level3</i></span></div>",
        )

    def test_to_html_with_mixed_children(self):
        """Test converting a parent node with mixed children to HTML."""
        child1 = HTMLLeafNode("p", "child1")
        child2 = HTMLParentNode("span", [HTMLLeafNode("b", "child2")])
        parent_node = HTMLParentNode("div", [child1, child2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><p>child1</p><span><b>child2</b></span></div>",
        )

    def test_to_html_with_no_children(self):
        """Test converting a parent node with no children to HTML."""
        with self.assertRaises(ValueError):
            HTMLParentNode(tag='div', children=[]).to_html()


if __name__ == '__main__':
    unittest.main()
