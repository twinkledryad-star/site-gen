import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import *

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "This is testing")
        node2 = HTMLNode("p", "This is testing")
        self.assertEqual(node, node2)

    def test_props_to_html(self):
        node = HTMLNode("div", "Hello", None, {"class": "greeting", "href": "https://boot.dev"})
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"'
        )
        
    def test_props_to_html1(self):
        node = HTMLNode("p", "Hello", None, {"class": "greeting", "href": "https://boot.dev"})
        to_html = f" class=\"greeting\" href=\"https://boot.dev\""
        self.assertEqual(node.props_to_html(), to_html)

    def test_props_to_html2(self):
        node = HTMLNode(props={"class": "sssup?", "href": "wassup.com"})
        to_html = f" class=\"sssup?\" href=\"wassup.com\""
        self.assertEqual(node.props_to_html(), to_html)
        

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_raw(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Hello, world!")
        self.assertEqual(node.to_html(), "<h1>Hello, world!</h1>")

    def test_leaf_to_html_value(self):
        node = LeafNode("h1", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')



class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>", )

    def test_to_html_with_children_error(self):
        child_node = LeafNode("b", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_children_error2(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_multiple_children(self):
        child_node = LeafNode("span", "child")
        child_node2 = LeafNode("b", "child2")
        child_node3 = LeafNode("i", "child3")
        parent_node = ParentNode("div", [child_node, child_node2, child_node3])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><b>child2</b><i>child3</i></div>")

    def test_to_html_with_children_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "greeting", "href": "https://boot.dev"})
        self.assertEqual(parent_node.to_html(), '<div class="greeting" href="https://boot.dev"><span>child</span></div>')

class TestTNodetoHNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("This is a text node", TextType.LINK, "www.google.com.tw")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {"href": "www.google.com.tw"})

    def test_image(self):
        node = TextNode("This is a anchor text", TextType.IMAGE, "www.google.com.tw")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "www.google.com.tw", "alt": "This is a anchor text"})

    def test_none_type(self):
        node = TextNode("This is a text node", None)
        
        with self.assertRaises(Exception):
            html_node = text_node_to_html_node(node)
        

if __name__ == "__main__":
    unittest.main()
