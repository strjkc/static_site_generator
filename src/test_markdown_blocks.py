import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node


class TestMarkdownBlock(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_is_heading(self):
        text1 = "###### this is a heading"
        text2 = "##### this is a heading"
        text3 = "#### this is a heading"
        text4 = "### this is a heading"
        text5 = "## this is a heading"
        text6 = "# this is a heading"
        text7 = "####### this is NOT a heading"
        text8 = "##<#### this is NOT a heading"
        text9 = "<###### this is NOT a heading"
        text10 = " this is NOT a heading"
        text11 = "######this is NOT a heading"
        result1 = block_to_block_type(text1)
        self.assertEqual(result1, BlockType.HEADING)
        result2 = block_to_block_type(text2)
        self.assertEqual(result2, BlockType.HEADING)
        result3 = block_to_block_type(text3)
        self.assertEqual(result3, BlockType.HEADING)
        result4 = block_to_block_type(text4)
        self.assertEqual(result4, BlockType.HEADING)
        result5 = block_to_block_type(text5)
        self.assertEqual(result5, BlockType.HEADING)
        result6 = block_to_block_type(text6)
        self.assertEqual(result6, BlockType.HEADING)
        result7 = block_to_block_type(text7)
        self.assertEqual(result7, BlockType.PARAGRAPH)
        result8 = block_to_block_type(text8)
        self.assertEqual(result8, BlockType.PARAGRAPH)
        result9 = block_to_block_type(text9)
        self.assertEqual(result9, BlockType.PARAGRAPH)
        result10 = block_to_block_type(text10)
        self.assertEqual(result10, BlockType.PARAGRAPH)
        result11 = block_to_block_type(text11)
        self.assertEqual(result11, BlockType.PARAGRAPH)

    def test_is_code(self):
       text1 = "```This is a code block```"
       text2 = "```This is NOT a code block"
       text3 = "This is NOT a code block```"
       text4 = "This is``` NOT``` a code block"
       text5 = "``This is NOT a code block```"
       text6 = "`This is NOT a code block```"
       text7 = "```This is NOT a code block``"
       text8 = "```This is NOT a code block`"
       res1 = block_to_block_type(text1)
       self.assertEqual(res1, BlockType.CODE)
       res2 = block_to_block_type(text2)
       self.assertEqual(res2, BlockType.PARAGRAPH)
       res3 = block_to_block_type(text3)
       self.assertEqual(res3, BlockType.PARAGRAPH)
       res4 = block_to_block_type(text4)
       self.assertEqual(res4, BlockType.PARAGRAPH)
       res5 = block_to_block_type(text5)
       self.assertEqual(res5, BlockType.PARAGRAPH)
       res6 = block_to_block_type(text6)
       self.assertEqual(res6, BlockType.PARAGRAPH)
       res7 = block_to_block_type(text7)
       self.assertEqual(res7, BlockType.PARAGRAPH)
       res8 = block_to_block_type(text8)
       self.assertEqual(res8, BlockType.PARAGRAPH)

    def test_is_quote(self):
        text1 = ">This is a quote>"
        text2 = ">>This is a quote>>"
        text3 = "This is NOT a quote>"
        text4 = ">This is NOT a quote"
        text5 = "This is NOT a quote"
        text6 = ">>This is NOT a quote"
        text7 = ">>This is a quote>"
        text8 = "This is> NOT a> quote>"
        res1 = block_to_block_type(text1)
        self.assertEqual(BlockType.QUOTE, res1)
        res2 = block_to_block_type(text2)
        self.assertEqual(BlockType.QUOTE, res2)
        res3 = block_to_block_type(text3)
        self.assertEqual(BlockType.PARAGRAPH, res3)
        res4 = block_to_block_type(text4)
        self.assertEqual(BlockType.QUOTE, res4)
        res5 = block_to_block_type(text5)
        self.assertEqual(BlockType.PARAGRAPH, res5)
        res6 = block_to_block_type(text6)
        self.assertEqual(BlockType.QUOTE, res6)
        res7 = block_to_block_type(text7)
        self.assertEqual(BlockType.QUOTE, res7)
        res8 = block_to_block_type(text8)
        self.assertEqual(BlockType.PARAGRAPH, res8)

    def test_is_u_list(self):
        text1 = ["- item", "- item-", "- -item-", "- -item-"]
        text10 = ["-item", "-item-", "iteam-", "item", "-- item"]
        for item in text1:
            res = block_to_block_type(item)
            self.assertEqual(BlockType.U_LIST, res)
        for item in text10:
            res = block_to_block_type(item)
            self.assertEqual(BlockType.PARAGRAPH, res)

    def test_is_o_list(self):
        text1 = ["1. Item", "11. Item", "0.  Item", "01. Item"]
        text10 = ["1 Item", "1.Item", "It1. em"]
        for item in text1:
            res = block_to_block_type(item)
            self.assertEqual(BlockType.O_LIST, res)
        for item in text10:
            res = block_to_block_type(item)
            self.assertEqual(BlockType.PARAGRAPH, res)

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )