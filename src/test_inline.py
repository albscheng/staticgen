import unittest

from inline import split_nodes_delimiter
from textnode import TextNode, TextType

class TestInline(unittest.TestCase):
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
