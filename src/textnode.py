from htmlnode import LeafNode

from enum import Enum

class TextType(Enum):
    TEXT   = "text"
    BOLD   = "bold"
    ITALIC = "italic"
    CODE   = "code"
    LINK   = "link"
    IMAGE  = "image"

"""
TextNode is a class that represents inline Markdown text
i.e.
    Normal text
    **Bold text**
    _Italic text_
    `Code text`
    Link: [anchor text](url)
    Image: ![alt text](url)
"""
class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        if self.text == other.text:
            if self.text_type == other.text_type:
                if self.url == other.url:
                    return True
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    

def text_node_to_html_node(text_node):
    # convert a TextNode to a LeafNode
    # return: LeafNode object

    props = None
    match text_node.text_type:
        case TextType.TEXT:
            tag = None
        case TextType.BOLD:
            tag = "b"
        case TextType.ITALIC:
            tag = "i"
        case TextType.CODE:
            tag = "code"
        case TextType.LINK:
            # <a href="..">text</a>
            tag = "a"
        case TextType.IMAGE:
            # <img src="url/of/image.jpg" alt="Description of image" />
            tag = "img"
        case _:
            raise Exception("Unexpected text node type encountered during conversion.")
    
    # link and image type have attributes
    if text_node.text_type == TextType.LINK:
        props = {"href": text_node.url}
    elif text_node.text_type == TextType.IMAGE:
        props = {
            "src": text_node.url,
            "alt": text_node.text,
        } 
        return LeafNode(tag, "", props)
    return LeafNode(tag, text_node.text, props)
