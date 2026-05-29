import unittest

from mark_to_html_node import *

class TestMk2HtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        self.assertEqual(html, expected)

   
    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>")


    def test_quoteblock(self):
        md = """
> This is a quote.
> It can span multiple lines.
> It can also have **bold texts**
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><blockquote>This is a quote. It can span multiple lines. It can also have <b>bold texts</b></blockquote></div>"
        self.assertEqual(html, expected)
    
    def test_ulistblock(self):
        md = """
- First item
- Second item with **bold**
- Third item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><ul><li>First item</li><li>Second item with <b>bold</b></li><li>Third item</li></ul></div>"
        self.assertEqual(html, expected)

    def test_olistblock(self):
        md = """
1. First item
2. Second item with _italic_
3. Third item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><ol><li>First item</li><li>Second item with <i>italic</i></li><li>Third item</li></ol></div>"
        self.assertEqual(html, expected)

    def test_headingblocks(self):
        
        def imlazy(md):
            return markdown_to_html_node(md).to_html()

        md1 = imlazy("# Heading 1")
        md2 = imlazy("### Heading 3")
        md3 = imlazy("###### Heading 6")

        expected1 = "<div><h1>Heading 1</h1></div>"
        expected2 = "<div><h3>Heading 3</h3></div>"
        expected3 = "<div><h6>Heading 6</h6></div>"

        self.assertEqual(md1, expected1)
        self.assertEqual(md2, expected2)
        self.assertEqual(md3, expected3)
        
    def test_combined(self):
        md ="""
# My Page

This is a paragraph with **bold** text.

> This is a quote.

- Apples
- Bananas

1. Wake up
2. Write code

```
This **should not** become bold.
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = """<div><h1>My Page</h1><p>This is a paragraph with <b>bold</b> text.</p><blockquote>This is a quote.</blockquote><ul><li>Apples</li><li>Bananas</li></ul><ol><li>Wake up</li><li>Write code</li></ol><pre><code>This **should not** become bold.
</code></pre></div>"""
        self.assertEqual(html, expected)