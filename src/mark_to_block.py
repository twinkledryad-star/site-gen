from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    
    # example of markdown:
    # "This is a heading

        # This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

        # - This is the first list item in a list block
        # - This is a list item
        # - This is another list item"

    new_list = []
    split_md = markdown.split("\n\n")
    for md in split_md:
        if md.strip() != "":
            new_list.append(md.strip())

    return new_list

def block_to_block_type(markdown_block):
    if markdown_block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    
    if markdown_block.startswith("```\n") and markdown_block.endswith("```"):
        return BlockType.CODE
        
    
    split_block = markdown_block.split("\n")
    if all(line.startswith(">") for line in split_block):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in split_block):
        return BlockType.UNORDERED_LIST


    i = 1
    for line in split_block:
        if not line.startswith(f"{i}. "):
                break
        i += 1
    else:
        return BlockType.ORDERED_LIST
                
    
    
    return BlockType.PARAGRAPH