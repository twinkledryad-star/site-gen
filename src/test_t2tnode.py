import unittest
from textnode import TextNode, TextType
from texttotextnode import text_to_textnodes

class Test_T2TNode(unittest.TestCase):
    def test_t2tnodes(self):
        old_node = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_node = text_to_textnodes(old_node)
        expected = [
        TextNode("This is ", TextType.TEXT),
        TextNode("text", TextType.BOLD),
        TextNode(" with an ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word and a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" and an ", TextType.TEXT),
        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", TextType.TEXT),
        TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(new_node, expected)
    
    def test_plain_test(self):
        old_node = "This is just plain text"
        new_node = text_to_textnodes(old_node)
        expected = [TextNode("This is just plain text", TextType.TEXT)]
        self.assertEqual(new_node, expected)

    def test_single_bold(self):
        old_node = "This is a single bold **text** only"
        new_node = text_to_textnodes(old_node)
        expected = [TextNode("This is a single bold ", TextType.TEXT), TextNode("text", TextType.BOLD), TextNode(" only", TextType.TEXT)]
        self.assertEqual(new_node, expected)

    def test_single_italic(self):
        old_node = "This is a single italic _text_ only"
        new_node = text_to_textnodes(old_node)
        expected = [TextNode("This is a single italic ", TextType.TEXT), TextNode("text", TextType.ITALIC), TextNode(" only", TextType.TEXT)]
        self.assertEqual(new_node, expected)

    def test_single_link(self):
        old_node = "This is a single [link](https://boot.dev) only"
        new_node = text_to_textnodes(old_node)
        expected = [TextNode("This is a single ", TextType.TEXT), TextNode("link", TextType.LINK, "https://boot.dev"), TextNode(" only", TextType.TEXT)]
        self.assertEqual(new_node, expected)

    def test_single_picture(self):
        old_node = "This is a single image ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) only"
        new_node = text_to_textnodes(old_node)
        expected = [TextNode("This is a single image ", TextType.TEXT), TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"), TextNode(" only", TextType.TEXT)]
        self.assertEqual(new_node, expected)

    def test_empty_string(self):
        old_node = ""
        new_node = text_to_textnodes(old_node)
        expected = []
        self.assertEqual(new_node, expected)

    def test_multi_bold(self):
        old_node = "This is a text with multiple **bold** **text** here"
        new_node = text_to_textnodes(old_node)
        expected = [TextNode("This is a text with multiple ", TextType.TEXT), TextNode("bold", TextType.BOLD), TextNode(" ", TextType.TEXT), TextNode("text", TextType.BOLD), TextNode(" here", TextType.TEXT)]
        self.assertEqual(new_node, expected)

    def test_bold_italic_together(self):
        old_node = "This is a text with **bold**_italic_ text put together"
        new_node = text_to_textnodes(old_node)
        expected = [TextNode("This is a text with ", TextType.TEXT), TextNode("bold", TextType.BOLD), TextNode("italic", TextType.ITALIC), TextNode(" text put together", TextType.TEXT)]
        self.assertEqual(new_node, expected)

    def test_just_image(self):
        old_node = "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)"
        new_node = text_to_textnodes(old_node)
        expected = [TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(new_node, expected)

    def test_unclosed_delimiter(self):
        old_node = "This is a text with unclosed **delimiter"
        with self.assertRaises(Exception):
            new_node = text_to_textnodes(old_node)

if __name__ == "__main__":
    unittest.main()
