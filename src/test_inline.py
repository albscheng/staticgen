import unittest

from inline import *
from textnode import TextNode, TextType

class TestInline(unittest.TestCase):
    def test_text_to_textnodes(self):
        str1 = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://www.github.com)"
        expected1 = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.github.com"),
        ]
        self.assertListEqual(expected1, text_to_textnodes(str1))

    
    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)

        node2 = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes2 = split_nodes_delimiter([node2], "**", TextType.BOLD)
        expected2 = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes2, expected2)
        
        node3 = TextNode("This is text with a _italic_ word", TextType.TEXT)
        new_nodes3 = split_nodes_delimiter([node3], "_", TextType.ITALIC)
        expected3 = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes3, expected3)

        plain = TextNode("Just plain text with no delimiters.", TextType.TEXT)
        plain_split = split_nodes_delimiter([plain], "**", TextType.BOLD)
        self.assertListEqual([plain], plain_split)

        node4 = TextNode("**This** is text with bold at start", TextType.TEXT)
        new_nodes4 = split_nodes_delimiter([node4], "**", TextType.BOLD)
        expected4 = [
            TextNode("This", TextType.BOLD),
            TextNode(" is text with bold at start", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes4, expected4)

        node5 = TextNode("This is text with code `at the end`", TextType.TEXT)
        new_nodes5 = split_nodes_delimiter([node5], "`", TextType.CODE)
        expected5 = [
            TextNode("This is text with code ", TextType.TEXT),
            TextNode("at the end", TextType.CODE),
        ]
        self.assertListEqual(new_nodes5, expected5)

        node6 = TextNode("This is ` code with weird whitespace  `", TextType.TEXT)
        new_nodes6 = split_nodes_delimiter([node6], "`", TextType.CODE)
        expected6 = [
            TextNode("This is ", TextType.TEXT),
            TextNode(" code with weird whitespace  ", TextType.CODE),
        ]
        self.assertListEqual(new_nodes6, expected6)
    
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

        no_opp = TextNode("This is just a text node", TextType.TEXT)
        self.assertListEqual([no_opp], split_nodes_image([no_opp]))

        node2 = TextNode(
            "This has ![image](https://i.imgur.com/abcde.png) and [link](https://www.github.com)!",
            TextType.TEXT,
        )
        new_nodes2 = split_nodes_image([node2])
        self.assertListEqual(
            [
                TextNode("This has ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/abcde.png"),
                TextNode(" and [link](https://www.github.com)!", TextType.TEXT),
            ],
            new_nodes2
        )

    
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

        no_opp = TextNode("This is just a text node", TextType.TEXT)
        self.assertListEqual([no_opp], split_nodes_link([no_opp]))

        node2 = TextNode(
            "This has ![image](https://i.imgur.com/abcde.png) and [link](https://www.github.com)!",
            TextType.TEXT,
        )
        new_nodes2 = split_nodes_link([node2])
        self.assertListEqual(
            [
                TextNode("This has ![image](https://i.imgur.com/abcde.png) and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.github.com"),
                TextNode("!", TextType.TEXT),
            ],
            new_nodes2
        )

    
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        extracted = extract_markdown_images(text)
        exp = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertListEqual(extracted, exp)

    
    def test_extract_markdown_links(self):
        text = "This is text with a link [to github](https://www.github.com) and [to youtube](https://www.youtube.com)"
        extracted = extract_markdown_links(text)
        exp = [("to github", "https://www.github.com"), ("to youtube", "https://www.youtube.com")]
        self.assertListEqual(extracted, exp)
