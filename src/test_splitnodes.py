import unittest
from splitnodes import split_nodes_image, split_nodes_link
from textnode import TextNode, TextType

class TestSplitNode(unittest.TestCase):

    def test_split_image_mixed(self):
        old_nodes = [TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT), TextNode(
        "This is image node", TextType.IMAGE)]
        new_nodes = split_nodes_image(old_nodes)
    
        expected_result = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode("This is image node", TextType.IMAGE)]
        self.assertEqual(new_nodes, expected_result)
    
    def test_split_image_single(self):
        old_nodes = [TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)

        expected_result = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")]
        self.assertEqual(new_nodes, expected_result)
    
    def test_split_image_multiple(self):
        old_nodes = [TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)

        expected_result = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")]
        self.assertEqual(new_nodes, expected_result)

    def test_split_image_backtoback(self):
        old_nodes = [TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)

        expected_result = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")]
        self.assertEqual(new_nodes, expected_result)

    def test_split_image_at_start(self):
        old_nodes = [TextNode(
        "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)

        expected_result = [
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")]
        self.assertEqual(new_nodes, expected_result)

    def test_split_link_single(self):
        old_nodes = [TextNode(
        "This is text with an [link1](www.google.com)", TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)

        expected_result = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "www.google.com")]
        self.assertEqual(new_nodes, expected_result)

    def test_split_link_multiple(self):
        old_nodes = [TextNode(
        "This is text with an [link1](www.google.com) and another [link2](www.boot.dev)", TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)

        expected_result = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "www.google.com"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "www.boot.dev")]
        self.assertEqual(new_nodes, expected_result)

    def test_split_link_backtoback(self):
        old_nodes = [TextNode(
        "This is text with an [link1](www.google.com)[link2](www.boot.dev)", TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)

        expected_result = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "www.google.com"),
            TextNode("link2", TextType.LINK, "www.boot.dev")]
        self.assertEqual(new_nodes, expected_result)
    
    
    def test_split_link_at_start(self):
        old_nodes = [TextNode(
        "[link1](www.google.com) and another [link2](www.boot.dev)", TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)

        expected_result = [
            TextNode("link1", TextType.LINK, "www.google.com"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "www.boot.dev")]
        self.assertEqual(new_nodes, expected_result)

    def test_no_image(self):
        old_nodes = [TextNode("This is just a plain text", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)

        expected_result = [TextNode("This is just a plain text", TextType.TEXT)]

        self.assertEqual(new_nodes, expected_result)

    def test_no_link(self):
        old_nodes = [TextNode("This is just a plain text", TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)

        expected_result = [TextNode("This is just a plain text", TextType.TEXT)]

        self.assertEqual(new_nodes, expected_result)

    def test_image_splitter_ignores_links(self):
        old_nodes = [TextNode(
        "This is text with a [link](www.google.com) and an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)

        expected_result = [
            TextNode("This is text with a [link](www.google.com) and an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")]
        self.assertEqual(new_nodes, expected_result)

    def test_link_splitter_ignores_images(self):
        old_nodes = [TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](www.google.com)", TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)

        expected_result = [
            TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "www.google.com")]
        self.assertEqual(new_nodes, expected_result)

    def test_split_link_mixed(self):
        old_nodes = [TextNode(
        "This is text with a [link](www.google.com)", TextType.TEXT), TextNode(
        "This is link node", TextType.LINK, "www.boot.dev")]
        new_nodes = split_nodes_link(old_nodes)

        expected_result = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "www.google.com"),
            TextNode("This is link node", TextType.LINK, "www.boot.dev")]
        self.assertEqual(new_nodes, expected_result)

    def test_split_image_multiple_input_nodes(self):
        old_nodes = [
            TextNode("Check this ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT),
            TextNode("This is plain text", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)

        expected_result = [
            TextNode("Check this ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode("This is plain text", TextType.TEXT)]
        self.assertEqual(new_nodes, expected_result)

if __name__ == "__main__":
    unittest.main()