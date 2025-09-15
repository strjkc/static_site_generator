import os.path
from enum import Enum
import re

from leafnode import LeafNode
from parentnode import ParentNode
from textnode import text_to_textnodes, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    U_LIST = "unordered_list"
    O_LIST = "ordered_list"

def block_to_block_type(block:str) -> BlockType:
    if  re.fullmatch(r"^```.*```$", block, re.DOTALL):
        return BlockType.CODE
    elif re.fullmatch(r"^>.*", block, re.DOTALL):
        return BlockType.QUOTE
    else:
        try:
            first_space = block.index(" ")
        except:
            return BlockType.PARAGRAPH
        chars = block[:first_space + 1]
        if len(chars) < 8:
            if re.fullmatch(r"#+ ", chars):
                return BlockType.HEADING
            elif re.match(r"^- ", chars):
                return BlockType.U_LIST
            elif re.match(r"^\d+\. ", chars):
                return BlockType.O_LIST
    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown: str) -> list[str]:
    lines = markdown.split("\n\n")
    lines_normalized = [line.strip() for line in lines if line.strip()]
    return lines_normalized

def get_heading_tag(text:str):
    space = text.index(" ")
    heading = text[:space]
    return f"h{len(heading)}"

def strip_block_markdown(text:str):
    space = text.index(" ")
    return text[space+1:]

def block_to_single_line(text:str):
    block_lines = text.split("\n")
    block_new = [line.strip() for line in block_lines if line.strip()]
    return ' '.join(block_new)

def markdown_to_html_node(markdown:str):
    nodes_from_markdown = []
    markdown_blocks = markdown_to_blocks(markdown)
    for block in markdown_blocks:
        print(block)
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            h_tag = get_heading_tag(block)
            text_nodes = text_to_textnodes(strip_block_markdown(block_to_single_line(block)))
            leaf_nodes = [text_node_to_html_node(node) for node in text_nodes]
            parent_node = ParentNode(h_tag, leaf_nodes)
            nodes_from_markdown.append(parent_node)
        elif block_type == BlockType.CODE:
            text = block.replace("```", "").split("\n")
            t = [line for line in text if line.strip()]
            code_text = '\n'.join(t)
            code_node = LeafNode("code", f"{code_text}\n")
            parent_node = ParentNode("pre", [code_node])
            nodes_from_markdown.append(parent_node)
        elif block_type == BlockType.QUOTE:
            text_nodes = text_to_textnodes(block_to_single_line(block[1:]))
            leafs = [text_node_to_html_node(node) for node in text_nodes]
            parent_node = ParentNode("blockquote", leafs)
            nodes_from_markdown.append(parent_node)
        elif block_type == BlockType.PARAGRAPH:
            text_nodes = text_to_textnodes(block_to_single_line(block))
            leafs = [text_node_to_html_node(node) for node in text_nodes]
            parent_node = ParentNode("p", leafs)
            nodes_from_markdown.append(parent_node)
        elif block_type == BlockType.U_LIST:
            lines = block.split("\n")
            striped_lines = [strip_block_markdown(line) for line in lines]
            text_nodes = [text_to_textnodes(line) for line in striped_lines]
            leafs = []
            for nodes in text_nodes:
                html_nodes= []
                for node in nodes:
                    html_node = text_node_to_html_node(node)
                    html_nodes.append(html_node)
                leafs.append(ParentNode("li",html_nodes))
            parent_node = ParentNode("ul", leafs)
            nodes_from_markdown.append(parent_node)
        elif block_type == BlockType.O_LIST:
            lines = block.split("\n")
            text_nodes = [text_to_textnodes(strip_block_markdown(line)) for line in lines]
            leafs = []
            for nodes in text_nodes:
                html_nodes = []
                for node in nodes:
                    html_node =  text_node_to_html_node(node)
                    html_nodes.append(html_node)
                leafs.append(ParentNode("li",html_nodes))
            parent_node = ParentNode("ol", leafs)
            nodes_from_markdown.append(parent_node)
    return ParentNode("div", nodes_from_markdown)

def extract_title(markdown:str):
    header = re.findall("^# .*", markdown)[0]
    return header[2:]

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as md_file:
        md = md_file.read()
        with open(template_path, "r") as tp_file:
            tp = tp_file.read()
            html_node = markdown_to_html_node(md)
            html = html_node.to_html()
            title = extract_title(md)
            tp = tp.replace("{{ Title }}", title)
            tp = tp.replace("{{ Content }}", html)
            tp = tp.replace("href=\"/", f"href=\"{basepath}")
            tp = tp.replace("src=\"/", f"src=\"{basepath}")
            if not os.path.exists(dest_path):
                os.mkdir(dest_path)
            with open(f"{dest_path}/index.html", "w") as out:
                out.write(tp)