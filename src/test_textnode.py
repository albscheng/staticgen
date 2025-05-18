import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_constr(self):
        text = "This is a text node"
        node = TextNode(text, TextType.BOLD)
        self.assertEqual(node.text, text)
        self.assertEqual(node.text_type.value, "bold")
        self.assertIsNone(node.url)

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("something else", TextType.BOLD)
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)

    def test_repr(self):
        node = TextNode("foo", TextType.BOLD)
        self.assertEqual(str(node), "TextNode(foo, bold, None)")

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

        node2 = TextNode("This is a bold node", TextType.BOLD)
        html_node2 = text_node_to_html_node(node2)
        self.assertEqual(html_node2.tag, "b")
        self.assertEqual(html_node2.value, "This is a bold node")

        node3 = TextNode("This is an italic node", TextType.ITALIC)
        html_node3 = text_node_to_html_node(node3)
        self.assertEqual(html_node3.tag, "i")
        self.assertEqual(html_node3.value, "This is an italic node")
        
        node4 = TextNode("print(foo)", TextType.CODE)
        html_node4 = text_node_to_html_node(node4)
        self.assertEqual(html_node4.tag, "code")
        self.assertEqual(html_node4.value, "print(foo)")

        with self.assertRaises(Exception):
            bad_type_node = TextNode("illegal type", "foo")
            text_node_to_html_node(bad_type_node)

if __name__ == "__main__":
    unittest.main()
