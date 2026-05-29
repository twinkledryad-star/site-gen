import unittest
from mark_to_block import markdown_to_blocks, block_to_block_type, BlockType

class Test_MK2Block(unittest.TestCase):
    
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_mk2blocks_extraline(self):
        md = """
This is **bolded** paragraph


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_mk2blocks_trailingspaces(self):
        md = """
   This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items   
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


    def test_md2block_whitespaces(self):
        md = """

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_md2block_emptystring(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])


    def test_mk2blocks_singleline(self):
        md = """
   This is **bolded** paragraph
This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
- This is a list
- with items   
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph\nThis is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line\n- This is a list\n- with items",
            ],
        )

    def test_mk2blocks_trailinglines(self):
        md = """


   This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items   


"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class Test_BK2Block(unittest.TestCase):
    def test_block_type_code(self):
        block = "```\ndef hello():\n    print('hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_type_not_code(self):
        block = "```no newline after backticks```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_with_no_space(self):
        block = "#not my heading here"
        expected = block_to_block_type(block)
        self.assertEqual(expected, BlockType.PARAGRAPH)

    def test_single_heading1(self):
        block = "# my heading here"
        expected = block_to_block_type(block)
        self.assertEqual(expected, BlockType.HEADING)

    def test_single_heading6(self):
        block = "###### my heading here"
        expected = block_to_block_type(block)
        self.assertEqual(expected, BlockType.HEADING)
    
    def test_quote(self):
        block ="> This is a quote\n> that spans two lines\n> and three lines"
        expected = block_to_block_type(block)
        self.assertEqual(expected, BlockType.QUOTE)

    def test_quote2(self):
        block ="""> This is a quote
> that spans two lines
> and three lines"""
        expected = block_to_block_type(block)
        self.assertEqual(expected, BlockType.QUOTE)

    def test_fake_quote(self):
        block ="> This is a quote\n> that spans two lines\nbut not third line" 
        expected = block_to_block_type(block)
        self.assertEqual(expected, BlockType.PARAGRAPH)

    def test_paragraph(self):
        block = "This is just a regular pargraph"
        expected = block_to_block_type(block)
        self.assertEqual(expected, BlockType.PARAGRAPH)

    def test_unorder_list(self):
        block = "- This is a list\n- with items\n- in it"
        expected = block_to_block_type(block)
        self.assertEqual(expected, BlockType.UNORDERED_LIST)

    def test_unorder_list2(self):
        block = """- This is a list
- with items
- in it"""
        expected = block_to_block_type(block)
        self.assertEqual(expected, BlockType.UNORDERED_LIST)

    def test_fake_unorder_list(self):
        block = "- This is a not a list\n- with items\n in it"
        expected = block_to_block_type(block)
        self.assertEqual(expected, BlockType.PARAGRAPH)
    
    def test_order_list(self):
        block = "1. This is a list with \n2. two lines in it"
        expected = block_to_block_type(block)
        self.assertEqual(expected, BlockType.ORDERED_LIST)
    
    def test_fake_order_list(self):
        block = "2. This is a list with \n3. wrong starting number"
        expected = block_to_block_type(block)
        self.assertEqual(expected, BlockType.PARAGRAPH)

    def test_wrong_order_list(self):
        block = """1. This is a list with
3. two lines in it
4. but in wrong order"""
        expected = block_to_block_type(block)
        self.assertEqual(expected, BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
