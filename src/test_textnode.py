import unittest

from leafnode import LeafNode
from textnode import TextType, TextNode, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, split_nodes_image, split_nodes_link, text_to_textnodes, extract_markdown_links

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_text_to_ptag(self):
        text = "This is a text node"
        text_node = TextNode(text, TextType.PLAIN)
        leaf_node = LeafNode(None, text)
        converted = text_node_to_html_node(text_node)
        self.assertEqual(leaf_node.to_html(), converted.to_html())

    def test_text_to_btag(self):
        text = "This should be bold"
        text_node = TextNode(text, TextType.BOLD)
        leaf_node = LeafNode("b", text)
        converted = text_node_to_html_node(text_node)
        self.assertEqual(leaf_node.to_html(), converted.to_html())

    def test_text_to_itag(self):
        text = "This should be italic"
        text_node = TextNode(text, TextType.ITALIC)
        leaf_node = LeafNode("i", text)
        converted = text_node_to_html_node(text_node)
        self.assertEqual(leaf_node.to_html(), converted.to_html())

    def test_text_to_codetag(self):
        text = "This is should be code formated"
        text_node = TextNode(text, TextType.CODE)
        leaf_node = LeafNode("code", text)
        converted = text_node_to_html_node(text_node)
        self.assertEqual(leaf_node.to_html(), converted.to_html())

    def test_text_to_imagetag(self):
        text = "This is alt text for an image"
        url = "https://link-to-an-image.com"
        text_node = TextNode(text, TextType.IMAGE, url)
        leaf_node = LeafNode("img", "",  props={"src": url, "alt":f"{text}"})
        converted = text_node_to_html_node(text_node)
        self.assertEqual(leaf_node.to_html(), converted.to_html())

    def test_text_to_linktag(self):
        text = "This is an anchor link"
        url = "https://link-to-a-website.com"
        text_node = TextNode(text, TextType.LINK, url)
        leaf_node = LeafNode("a", text, props={"href": url})
        converted = text_node_to_html_node(text_node)
        self.assertEqual(leaf_node.to_html(), converted.to_html())


    def test_split_bold(self):
        node_to_split = TextNode("The first part of the text **bold spot** the second part", TextType.PLAIN)
        expected_1 = TextNode("The first part of the text ", TextType.PLAIN)
        expected_2 = TextNode("bold spot", TextType.BOLD)
        expected_3 = TextNode(" the second part", TextType.PLAIN)

        new_node1, new_node2, new_node3 = split_nodes_delimiter([node_to_split], "**", TextType.BOLD)

        self.assertEqual(new_node1.text, expected_1.text)
        self.assertEqual(new_node1.text_type, expected_1.text_type)

        self.assertEqual(new_node2.text, expected_2.text)
        self.assertEqual(new_node2.text_type, expected_2.text_type)

        self.assertEqual(new_node3.text, expected_3.text)
        self.assertEqual(new_node3.text_type, expected_3.text_type)

    def test_split_code(self):
        node_to_split = TextNode("The first part of the text `def fun(input:str):` the second part", TextType.PLAIN)
        expected_1 = TextNode("The first part of the text ", TextType.PLAIN)
        expected_2 = TextNode("def fun(input:str):", TextType.CODE)
        expected_3 = TextNode(" the second part", TextType.PLAIN)

        new_node1, new_node2, new_node3 = split_nodes_delimiter([node_to_split], "`", TextType.CODE)

        self.assertEqual(new_node1.text, expected_1.text)
        self.assertEqual(new_node1.text_type, expected_1.text_type)

        self.assertEqual(new_node2.text, expected_2.text)
        self.assertEqual(new_node2.text_type, expected_2.text_type)

        self.assertEqual(new_node3.text, expected_3.text)
        self.assertEqual(new_node3.text_type, expected_3.text_type)

    def test_split_italic(self):
        node_to_split = TextNode("The first part of the text _italic part_ the second part", TextType.PLAIN)
        expected_1 = TextNode("The first part of the text ", TextType.PLAIN)
        expected_2 = TextNode("italic part", TextType.ITALIC)
        expected_3 = TextNode(" the second part", TextType.PLAIN)

        new_node1, new_node2, new_node3 = split_nodes_delimiter([node_to_split], "_", TextType.ITALIC)

        self.assertEqual(new_node1.text, expected_1.text)
        self.assertEqual(new_node1.text_type, expected_1.text_type)

        self.assertEqual(new_node2.text, expected_2.text)
        self.assertEqual(new_node2.text_type, expected_2.text_type)

        self.assertEqual(new_node3.text, expected_3.text)
        self.assertEqual(new_node3.text_type, expected_3.text_type)

    def test_get_image_regex(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        res = extract_markdown_images(text)
        valid = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(valid, res)

    def test_get_link_regex(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        res = extract_markdown_links(text)
        valid = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(valid, res)

    def test_text_text_to_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        old_node = TextNode(text, TextType.PLAIN)
        valid_nodes = [
            TextNode("This is text with a ", TextType.PLAIN ),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.PLAIN),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        new_nodes = split_nodes_image([old_node])
        for i, valid_node in enumerate(valid_nodes):
            self.assertEqual(valid_node.text, new_nodes[i].text)
            self.assertEqual(valid_node.text_type, new_nodes[i].text_type)
            self.assertEqual(valid_node.url,  new_nodes[i].url)

    def test_text_text_to_image_trailing_text(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg), some trailing text"
        old_node = TextNode(text, TextType.PLAIN)
        valid_nodes = [
            TextNode("This is text with a ", TextType.PLAIN ),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.PLAIN),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(", some trailing text", TextType.PLAIN)
        ]
        new_nodes = split_nodes_image([old_node])
        for i, valid_node in enumerate(valid_nodes):
            self.assertEqual(valid_node.text, new_nodes[i].text)
            self.assertEqual(valid_node.text_type, new_nodes[i].text_type)
            self.assertEqual(valid_node.url,  new_nodes[i].url)

    def test_text_text_to_image_only_image(self):
        text = "![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        old_node = TextNode(text, TextType.PLAIN)
        valid_nodes = [
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
        ]
        new_nodes = split_nodes_image([old_node])
        for i, valid_node in enumerate(valid_nodes):
            self.assertEqual(valid_node.text, new_nodes[i].text)
            self.assertEqual(valid_node.text_type, new_nodes[i].text_type)
            self.assertEqual(valid_node.url,  new_nodes[i].url)

    def test_text_text_to_image_empty_string(self):
        text = ""
        old_node = TextNode(text, TextType.PLAIN)
        valid_nodes = [
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
        ]
        self.assertRaises(ValueError, split_nodes_image, [old_node])

    def test_text_text_to_image_empty_None_item(self):
        text = "![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        old_node = None
        valid_nodes = [
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
        ]
        self.assertRaises(ValueError, split_nodes_image, [old_node])

    #def test_text_text_to_image_invalid_item(self):
        #text = "![rick roll] and some text here"
        #old_node = TextNode(text, TextType.PLAIN)
        #self.assertRaises(ValueError, split_nodes_image, [old_node])

    def test_text_text_to_image_start(self):
        text2 = "![rick roll](https://i.imgur.com/aKaOqIh.gif) This is text with a and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg), some trailing text"
        old_nodes = [
            TextNode(text2, TextType.PLAIN)
        ]

        valid_nodes = [
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" This is text with a and ", TextType.PLAIN),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(", some trailing text", TextType.PLAIN),
        ]
        new_nodes = split_nodes_image(old_nodes)
        for i, valid_node in enumerate(valid_nodes):
            self.assertEqual(valid_node.text, new_nodes[i].text)
            self.assertEqual(valid_node.text_type, new_nodes[i].text_type)
            self.assertEqual(valid_node.url,  new_nodes[i].url)


    def test_text_text_to_image_trailing_text_multi(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg), some trailing text"
        text2 = "![rick roll](https://i.imgur.com/aKaOqIh.gif) This is text with a and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg), some trailing text"
        old_nodes = [
            TextNode(text, TextType.PLAIN),
            TextNode(text2, TextType.PLAIN)
        ]

        valid_nodes = [
            TextNode("This is text with a ", TextType.PLAIN ),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.PLAIN),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(", some trailing text", TextType.PLAIN),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" This is text with a and ", TextType.PLAIN),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(", some trailing text", TextType.PLAIN),
        ]
        new_nodes = split_nodes_image(old_nodes)
        for i, valid_node in enumerate(valid_nodes):
            self.assertEqual(valid_node.text, new_nodes[i].text)
            self.assertEqual(valid_node.text_type, new_nodes[i].text_type)
            self.assertEqual(valid_node.url,  new_nodes[i].url)

    def test_text_text_to_link(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        old_node = TextNode(text, TextType.PLAIN)
        valid_nodes = [
            TextNode("This is text with a ", TextType.PLAIN ),
            TextNode("rick roll", TextType.LINK, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.PLAIN),
            TextNode("obi wan", TextType.LINK, "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        new_nodes = split_nodes_link([old_node])
        for i, valid_node in enumerate(valid_nodes):
            self.assertEqual(valid_node.text, new_nodes[i].text)
            self.assertEqual(valid_node.text_type, new_nodes[i].text_type)
            self.assertEqual(valid_node.url,  new_nodes[i].url)

    def test_text_text_to_link_trailing_text(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg), some trailing text"
        old_node = TextNode(text, TextType.PLAIN)
        valid_nodes = [
            TextNode("This is text with a ", TextType.PLAIN ),
            TextNode("rick roll", TextType.LINK, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.PLAIN),
            TextNode("obi wan", TextType.LINK, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(", some trailing text", TextType.PLAIN)
        ]
        new_nodes = split_nodes_link([old_node])
        for i, valid_node in enumerate(valid_nodes):
            self.assertEqual(valid_node.text, new_nodes[i].text)
            self.assertEqual(valid_node.text_type, new_nodes[i].text_type)
            self.assertEqual(valid_node.url,  new_nodes[i].url)

    def test_text_text_to_link_only_image(self):
        text = "[rick roll](https://i.imgur.com/aKaOqIh.gif)"
        old_node = TextNode(text, TextType.PLAIN)
        valid_nodes = [
            TextNode("rick roll", TextType.LINK, "https://i.imgur.com/aKaOqIh.gif"),
        ]
        new_nodes = split_nodes_link([old_node])
        for i, valid_node in enumerate(valid_nodes):
            self.assertEqual(valid_node.text, new_nodes[i].text)
            self.assertEqual(valid_node.text_type, new_nodes[i].text_type)
            self.assertEqual(valid_node.url,  new_nodes[i].url)

    def test_text_text_to_link_empty_string(self):
        text = ""
        old_node = TextNode(text, TextType.PLAIN)
        valid_nodes = [
            TextNode("rick roll", TextType.LINK, "https://i.imgur.com/aKaOqIh.gif"),
        ]
        self.assertRaises(ValueError, split_nodes_link, [old_node])

    def test_text_text_to_link_empty_None_item(self):
        text = "[rick roll](https://i.imgur.com/aKaOqIh.gif)"
        old_node = None
        valid_nodes = [
            TextNode("rick roll", TextType.LINK, "https://i.imgur.com/aKaOqIh.gif"),
        ]
        self.assertRaises(ValueError, split_nodes_link, [old_node])

    #def test_text_text_to_link_invalid_item(self):
        #text = "[rick roll] and some text here"
        #old_node = TextNode(text, TextType.PLAIN)
        #self.assertRaises(ValueError, split_nodes_link, [old_node])

    def test_text_text_to_link_start(self):
        text2 = "[rick roll](https://i.imgur.com/aKaOqIh.gif) This is text with a and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg), some trailing text"
        old_nodes = [
            TextNode(text2, TextType.PLAIN)
        ]

        valid_nodes = [
            TextNode("rick roll", TextType.LINK, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" This is text with a and ", TextType.PLAIN),
            TextNode("obi wan", TextType.LINK, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(", some trailing text", TextType.PLAIN),
        ]
        new_nodes = split_nodes_link(old_nodes)
        for i, valid_node in enumerate(valid_nodes):
            self.assertEqual(valid_node.text, new_nodes[i].text)
            self.assertEqual(valid_node.text_type, new_nodes[i].text_type)
            self.assertEqual(valid_node.url,  new_nodes[i].url)


    def test_text_text_to_link_trailing_text_multi(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg), some trailing text"
        text2 = "[rick roll](https://i.imgur.com/aKaOqIh.gif) This is text with a and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg), some trailing text"
        old_nodes = [
            TextNode(text, TextType.PLAIN),
            TextNode(text2, TextType.PLAIN)
        ]

        valid_nodes = [
            TextNode("This is text with a ", TextType.PLAIN ),
            TextNode("rick roll", TextType.LINK, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.PLAIN),
            TextNode("obi wan", TextType.LINK, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(", some trailing text", TextType.PLAIN),
            TextNode("rick roll", TextType.LINK, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" This is text with a and ", TextType.PLAIN),
            TextNode("obi wan", TextType.LINK, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(", some trailing text", TextType.PLAIN),
        ]
        new_nodes = split_nodes_link(old_nodes)
        for i, valid_node in enumerate(valid_nodes):
            self.assertEqual(valid_node.text, new_nodes[i].text)
            self.assertEqual(valid_node.text_type, new_nodes[i].text_type)
            self.assertEqual(valid_node.url,  new_nodes[i].url)

    def test_text_to_node(self):
        text = ["This is ", "**text**", " with an ", "_italic_", " word and a ", "`code block`", " and an ", "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)", " and a ", "[link](https://boot.dev)"]
        text_string = ''.join(text)
        valid_nodes = [
            TextNode(text[0], TextType.PLAIN),
            TextNode(text[1].replace("**", ""), TextType.BOLD),
            TextNode(text[2], TextType.PLAIN),
            TextNode(text[3].replace("_", ""), TextType.ITALIC),
            TextNode(text[4], TextType.PLAIN),
            TextNode(text[5].replace("`", ""), TextType.CODE),
            TextNode(text[6], TextType.PLAIN),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(text[8], TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://boot.dev")
        ]
        new_nodes = text_to_textnodes(text_string)
        for i, valid_node in enumerate(valid_nodes):
            self.assertEqual(valid_node.text, new_nodes[i].text)
            self.assertEqual(valid_node.text_type, new_nodes[i].text_type)
            self.assertEqual(valid_node.url,  new_nodes[i].url)



if __name__ == "__main__":
    unittest.main()
