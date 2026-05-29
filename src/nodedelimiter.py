from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_strings = node.text.split(delimiter)
        if len(split_strings) % 2 == 0:
            raise Exception("Invalid markdown syntax")
        # for i in range(len(split_strings)):
        #     if i % 2 == 0:
        #         new_nodes.append(TextNode(split_strings[i], TextType.TEXT))
        #     else:
        #         new_nodes.append(TextNode(split_strings[i], text_type))
        
        for i, sentences in enumerate(split_strings):
                if i % 2== 0:
                     new_nodes.append(TextNode(sentences, TextType.TEXT))
                else:
                     new_nodes.append(TextNode(sentences, text_type))

    return new_nodes
