import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_add_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ]
        )
        valid = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(valid, node.to_html())


    def test_no_children(self):
        node = ParentNode(
            "p",
            [
            ]
        )
        self.assertRaises(ValueError, node.to_html)

    def test_no_tag(self):
        node = ParentNode(
            None,
            [
                LeafNode("b", "Bold text"),
            ]
        )
        self.assertRaises(ValueError, node.to_html)


    def test_one_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
            ]
        )
        valid = "<p><b>Bold text</b></p>"
        self.assertRaises(ValueError)
        self.assertEqual(valid, node.to_html())

    def test_nested_parents(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "span",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode("p", "Paragraph text"),
                        LeafNode("i", "Italic text"),
                    ]
                ),
                LeafNode(None, "Normal text"),
            ]
        )
        valid = "<div><span><b>Bold text</b><p>Paragraph text</p><i>Italic text</i></span>Normal text</div>"
        self.assertEqual(valid, node.to_html())

