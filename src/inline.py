from textnode import TextNode, TextType

import re

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

# text_to_textnodes converts a raw string of markdown text to TextNode objects
def text_to_textnodes(text):
    # text: string containing markdown-flavoured text
    # returns list of TextNode
    nodes = [TextNode(text, TextType.TEXT)]
    print("Nodes init")
    print(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    print("Nodes after BOLD")
    print(nodes)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    print("Nodes after ITALIC")
    print(nodes)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    print("Nodes after CODE")
    print(nodes)
    nodes = split_nodes_image(nodes)
    print("Nodes after IMG")
    print(nodes)
    nodes = split_nodes_link(nodes)
    print("Nodes after LINK")
    print(nodes)

    print("")
    print(nodes)
    return nodes

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
            # delimiter was NOT found (no-op)
            split_nodes.append(node)
        else:
            raise Exception("Unhandled case in split_nodes_delimiter")

    return split_nodes

# split_nodes_image splits one "text" TextNode into a list of TextNode
# if the inline text contains images
def split_nodes_image(old_nodes):
    # For each image extracted from the text, split the text before and after the image markdown
    split_nodes = []
    for node in old_nodes:
        original_text = node.text
        extracted_imgs = extract_markdown_images(original_text)
        # if no images, nothing to do
        if len(extracted_imgs) == 0:
            split_nodes.append(node)
        for i in range(0, len(extracted_imgs)):
            image_alt, image_link = extracted_imgs[i]
            # split text into before and after image
            sections = original_text.split(f"![{image_alt}]({image_link})", 1)
            # before the image
            if len(sections[0]) > 0:
                split_nodes.append(TextNode(sections[0], TextType.TEXT))
            # image itself
            split_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            # after the image
            if len(sections[1]) > 0:
                original_text = sections[1]
                if i == len(extracted_imgs) - 1:
                    # this is the last image in the string
                    # append the trailing bits of the string
                    split_nodes.append(TextNode(original_text, TextType.TEXT))

    return split_nodes

# split_nodes_image splits one "text" TextNode into a list of TextNode
# if the inline text contains links
def split_nodes_link(old_nodes):
    split_nodes = []
    for node in old_nodes:
        original_text = node.text
        extracted_links = extract_markdown_links(original_text)
        # if no links, nothing to do
        if len(extracted_links) == 0:
            split_nodes.append(node)
        for i in range(0, len(extracted_links)):
            link_text, link_url = extracted_links[i]
            # split text into before and after link
            sections = original_text.split(f"[{link_text}]({link_url})", 1)
            # before the link
            if len(sections[0]) > 0:
                split_nodes.append(TextNode(sections[0], TextType.TEXT))
            # link itself
            split_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            # after the image
            if len(sections[1]) > 0:
                original_text = sections[1]
                if i == len(extracted_links) - 1:
                    # this is the last link in the string
                    # append the trailing bits of the string
                    split_nodes.append(TextNode(original_text, TextType.TEXT))
    return split_nodes

# extract_markdown_images extracts images from any string of markdown text
def extract_markdown_images(text):
    # text: raw markdown text
    # returns list of tuples (alt text, url)
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

# extract_markdown_links extracts links from any string of markdown text
def extract_markdown_links(text):
    # text: raw markdown text
    # returns list of tuples (anchor text, url)
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)
