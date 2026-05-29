from mdextract import extract_markdown_images, extract_markdown_links
from textnode import TextType, TextNode

def split_nodes_image(old_nodes):
    # old_node = [TextNode("This is text with an ![image](https://img.com/a.png) and another ![second](https://img.com/b.png)", TextType.TEXT)]
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            image_nodes = extract_markdown_images(node.text)
            # this is what image_nodes looks like:
            # [("image", "https://img.com/a.png"), ("second", "https://img.com/b.png")]
            remaining_text = node.text
            for image_alt, image_url in image_nodes:
                sections = remaining_text.split(f"![{image_alt}]({image_url})", 1)
                # this is what sections looks like: 
                # ["This is text with an ", " and another ![second](https://img.com/b.png)"]
                # The delimiter is not in it because it's being used as split delimiter)
                if len(sections[0]) != 0:
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
                remaining_text = sections[1]
            if len(remaining_text) != 0:
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes
                



def split_nodes_link(old_nodes):
    # old_node = [TextNode("This is text with an [go_to_google](www.google) link and another [go_to_bootdev](www.boot.dev) link", TextType.TEXT)]
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            link_nodes = extract_markdown_links(node.text)
            # this is what link_nodes looks like:
            # [("go_to_google", "www.google.com"), ("go_to_bootdev", "www.boot.dev")]
            remaining_text = node.text
            for link_text, link_url in link_nodes:
                sections = remaining_text.split(f"[{link_text}]({link_url})", 1)
                # this is what sections looks like: 
                # ["This is text with an ", " link and another [go_to_bootdev](www.boot.dev) link"]
                # The delimiter is not in it because it's being used as split delimiter)
                if len(sections[0]) != 0:
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
                remaining_text = sections[1]
            if len(remaining_text) != 0:
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes
