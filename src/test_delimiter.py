import unittest
from nodedelimiter import split_nodes_delimiter
from textnode import *

class TestDelimiter(unittest.TestCase):
    def test_code(self):
        old_node = split_nodes_delimiter(([TextNode("This is text with a `code block` in the middle", TextType.TEXT)]), "`", TextType.CODE)
        new_node = [
                    TextNode("This is text with a ", TextType.TEXT), 
                    TextNode("code block", TextType.CODE), 
                    TextNode(" in the middle", TextType.TEXT)
                    ]
        self.assertEqual(old_node, new_node)

    def test_bold(self):
        old_node = [TextNode("There is a **bold text** here", TextType.TEXT)]
        result = split_nodes_delimiter(old_node, "**", TextType.BOLD)
        expected = [
                    TextNode("There is a ", TextType.TEXT),
                    TextNode("bold text", TextType.BOLD),
                    TextNode(" here", TextType.TEXT)
                    ]
        self.assertEqual(result, expected)

    def test_invalid(self):
        old_node = [TextNode("There is a **bold text here", TextType.TEXT)]
        with self.assertRaises(Exception):
            result = split_nodes_delimiter(old_node, "**", TextType.BOLD)

    def test_multiple_delimiters(self):
        node = TextNode("`one` and `two`", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("", TextType.TEXT),
            TextNode("one", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("two", TextType.CODE),
            TextNode("", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_non_text_passthrough(self):
        node = TextNode("already bold", TextType.BOLD)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [TextNode("already bold", TextType.BOLD)])

    if __name__ == "__main__":
        unittest.main()
