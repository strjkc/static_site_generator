import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_not_tag(self):
        valid = "Testing Value"
        node = LeafNode(None, valid)
        self.assertEqual(node.to_html(), valid)

    def test_with_tag(self):
        value = "Testing Value"
        valid = f"<p>{value}</p>"
        node = LeafNode("p", value)
        self.assertEqual(valid, node.to_html())

    def test_with_props(self):
        value = "Click Here!"
        test_link = "https://testing.com"
        valid = f"<a href=\"{test_link}\">{value}</a>"
        node = LeafNode("a", value, {"href": test_link})
        self.assertEqual(node.to_html(), valid)

