from enum import Enum
import re

from htmlnode import HTMLNode
from leafnode import LeafNode

class TextType(Enum):
    PLAIN= "plain text"
    BOLD= "bold text"
    ITALIC= "italic text"
    CODE= "code text"
    LINK= "link"
    IMAGE= "image"


class TextNode():
    def __init__(self,text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text is other.text and self.text_type is other.text_type and self.url is other.url:
            return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(node:TextNode)->LeafNode:
    if node.text_type == TextType.BOLD:
        return LeafNode("b", node.text)
    elif node.text_type == TextType.PLAIN:
        return LeafNode(None, node.text)
    elif node.text_type == TextType.ITALIC:
        return LeafNode("i", node.text)
    elif node.text_type == TextType.CODE:
        return LeafNode("code", node.text)
    elif node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": node.url, "alt": node.text})
    elif node.text_type == TextType.LINK:
        return LeafNode("a", node.text, {"href":node.url})
    raise ValueError("Invalid type of text string")

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter:str, text_type:TextType):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        sections = node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, delimiters not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            elif i % 2 == 0:
                new_nodes.append(TextNode(sections[i], TextType.PLAIN))
            else:
                new_nodes.append(TextNode(sections[i], text_type))
    return new_nodes

def extract_markdown_images(text):
    get_images=r"!\[(.*?)\]\((.*?)\)"
    return re.findall(get_images, text)

def extract_markdown_links(text):
    get_images=r"\[(.*?)\]\((.*?)\)"
    return re.findall(get_images, text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    if not old_nodes:
        raise ValueError("old nodes are empty or None")
    for node in old_nodes:
        if not node:
            raise ValueError("Node is None")
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        if not node.text:
            raise ValueError("note text empty")
        text = node.text
        pairs = extract_markdown_images(text)
        if not pairs:
            new_nodes.append(node)
            continue
        for pair in pairs:
            if len(pair) != 2:
                raise ValueError("Markdown not properly formated")
            alt, url = pair
            delimiter = f"![{alt}]({url})"
            first_part, second_part = text.split(delimiter, 1)
            text = second_part
            if first_part:
                text_node = TextNode(first_part, TextType.PLAIN)
                new_nodes.append(text_node)
            img_node = TextNode(alt, TextType.IMAGE, url)
            new_nodes.append(img_node)
        if text:
            new_node = TextNode(text, TextType.PLAIN)
            new_nodes.append(new_node)
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    if not old_nodes:
        raise ValueError("old nodes are empty or None")
    for node in old_nodes:
        if not node:
            raise ValueError("Node is None")
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        if not node.text:
            raise ValueError("node text empty")
        text = node.text
        pairs = extract_markdown_links(text)
        if not pairs:
            new_nodes.append(node)
            continue
        for pair in pairs:
            if len(pair) != 2:
                raise ValueError("Markdown not properly formated")
            alt, url = pair
            delimiter = f"[{alt}]({url})"
            first_part, second_part = text.split(delimiter, 1)
            text = second_part
            if first_part:
                text_node = TextNode(first_part, TextType.PLAIN)
                new_nodes.append(text_node)
            img_node = TextNode(alt, TextType.LINK, url)
            new_nodes.append(img_node)
        if text:
            new_node = TextNode(text, TextType.PLAIN)
            new_nodes.append(new_node)
    return new_nodes


def text_to_textnodes(text):
    initial_node = TextNode(text, TextType.PLAIN)
    nodes = split_nodes_delimiter([initial_node], '`', TextType.CODE)
    nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, '_', TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes



