import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        # Test None case
        node1 = HTMLNode("h1", "Header", [], None)
        self.assertEqual(node1.props_to_html(), "")
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }

        # Test Successful case
        correct = " href=\"https://www.google.com\" target=\"_blank\""
        node2 = HTMLNode("p", "some text", [], props)
        self.assertIsNotNone(node2.props_to_html())
        self.assertEqual(node2.props_to_html(), correct)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html(self):
        node1 = LeafNode("p", "This is a paragraph of text.")
        str1 = "<p>This is a paragraph of text.</p>"
        self.assertEqual(node1.to_html(), str1)

        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        str2 = "<a href=\"https://www.google.com\">Click me!</a>"
        self.assertEqual(node2.to_html(), str2)

        node3 = LeafNode("h1", "Header", {"id": "main-header"})
        str3 = "<h1 id=\"main-header\">Header</h1>"
        self.assertEqual(node3.to_html(), str3)

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_greatgrandchildren(self):
        greatgrandchild_node = LeafNode("p", "foo")
        grandchild_node = ParentNode("span", [greatgrandchild_node])
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><span><p>foo</p></span></span></div>",
        )

if __name__ == "__main__":
    unittest.main()
