from textnode import TextNode, TextType

"""
Convert raw markdown strings to TextNodes

    This is text with a **bolded phrase** in the middle

                        to
    [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("bolded phrase", TextType.BOLD),
        TextNode(" in the middle", TextType.TEXT),
    ]
"""

# split_nodes_delimiter splits one "text" TextNode into a list of TextNode
# if the inline text contains bold, italics, or code
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # old_nodes: list 
    # delimiter: string, like "`"
    # text_type: TextType
    # returns list of TextNode
    split_nodes = []

    for node in old_nodes:
        sp = node.text.split(delimiter)
        if len(sp) == 3:
            # this means delimiter was found
            # index=1 is the target string
            if len(sp[0]) > 0:
                split_nodes.append(TextNode(sp[0], TextType.TEXT))
            split_nodes.append(TextNode(sp[1], text_type))
            if len(sp[2]) > 0:
                split_nodes.append(TextNode(sp[2], TextType.TEXT))
        elif len(sp) == 1:
            # delimiter was NOT found (plain text)
            split_nodes.append(TextNode(sp[0], TextType.TEXT))
        else:
            raise Exception("Unhandled case in split_nodes_delimiter")

    return split_nodes
