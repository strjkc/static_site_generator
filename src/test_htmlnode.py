import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):

    def test_abstract(self):
        node = HTMLNode("a", "This is a link", None, {'href': "https://", "target": "_blank"})
        self.assertRaises(NotImplementedError, node.to_html)

    def test_props_conversion(self):
        node = HTMLNode("a", "This is a link", None, {'href': "https://", "target": "_blank"})
        valid = f' href="https://" target="_blank"'
        self.assertEqual(node.props_to_html(), valid)

