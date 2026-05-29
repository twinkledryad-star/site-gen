from htmlnode import HTMLNode, ParentNode, LeafNode
from mark_to_block import BlockType, markdown_to_blocks, block_to_block_type
from textnode import text_node_to_html_node, TextNode, TextType
from texttotextnode import text_to_textnodes

def text_to_children(text):
        # what a text looks like:
        # text = "This is **bolded** text with _italic_ and `code` here"
        text_nodes = text_to_textnodes(text)
        # what text_nodes looks like:
        # [
        # TextNode("This is ", TextType.TEXT),
        # TextNode("bolded", TextType.BOLD),
        # TextNode(" text with ", TextType.TEXT),
        # TextNode("italic", TextType.ITALIC),
        # TextNode(" and ", TextType.TEXT),
        # TextNode("code", TextType.CODE),
        # TextNode(" here", TextType.TEXT),
        # ]
        return [text_node_to_html_node(node) for node in text_nodes]
        # new_list = []
        # for node in text_nodes:
        #     new_list.append(text_node_to_html_node(node))
        # return new_list

        # what new_list look like
        # [
        # LeafNode(None, "This is "),
        # LeafNode("b", "bolded"),
        # LeafNode(None, " text with "),
        # LeafNode("i", "italic"),
        # LeafNode(None, " and "),
        # LeafNode("code", "code"),
        # LeafNode(None, " here"),
        # ]
        


def paragraph_to_html_node(block):
    split_block = block.split("\n")
    join_block = " ".join(split_block)
    children = text_to_children(join_block)
    return ParentNode(tag="p", children=children)

def heading_to_html_node(block):
    stripped = block.lstrip("#")
    header_length = len(block) - len(stripped)
    cleaned = stripped[1:]
    children = text_to_children(cleaned)
    return ParentNode(tag=f"h{header_length}", children=children)

def code_to_html_node(block):
    if not block.startswith("```\n") or not block.endswith("```"):
        raise ValueError("Invalid format for code block")
    stripped = block[4:-3]
    text_node = TextNode(text=stripped, text_type=TextType.CODE)
    code_node = [text_node_to_html_node(text_node)]
    return ParentNode(tag="pre", children=code_node )

def quote_to_html_node(block):
    split_block = block.split("\n")
    new_list = []
    for line in split_block:
        if not line.startswith(">"):
            raise ValueError("Wrong format for quote block")
        stripped = line.lstrip(">").lstrip(" ")
        new_list.append(stripped)


    children = text_to_children(" ".join(new_list))
    return ParentNode(tag="blockquote", children=children)

def ulist_to_html_node(block):
    new_list = []
    split_block = block.split("\n")
    for line in split_block:
        sub_parent = ParentNode(tag="li", children=text_to_children(line[2:]))
        new_list.append(sub_parent)
    return ParentNode(tag="ul", children=new_list)

def olist_to_html_node(block):
    new_list = []
    split_block = block.split("\n")
    for line in split_block:
        sub_parent = ParentNode(tag="li", children=text_to_children(line[3:]))
        new_list.append(sub_parent)
    return ParentNode(tag="ol", children=new_list)
    




def block_to_html_node(block, block_type):
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    elif block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    elif block_type == BlockType.CODE:
        return code_to_html_node(block)
    elif block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    elif block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    elif block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    else:
        raise ValueError("Invalid block type")

def markdown_to_html_node(markdown):

    # this is what a markdown looks like:
    # md = """
# This is **bolded** paragraph
# text in a p
# tag here

# This is another paragraph with _italic_ text and `code` here

# """ 

    blocks = markdown_to_blocks(markdown)
    new_list = []
    for block in blocks:
        block_type = block_to_block_type(block)
        new_list.append(block_to_html_node(block=block, block_type=block_type))
    return ParentNode("div", new_list)
        