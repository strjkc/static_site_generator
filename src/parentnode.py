from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props= None):
        super().__init__(tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Tag missing")
        if not self.children:
            raise ValueError("Children missing")
        prop_string = ""
        if self.props:
            prop_string = self.props_to_html()
        open_tag= f"<{self.tag}{prop_string}>"
        for child in self.children:
            child_html = child.to_html()
            open_tag += child_html
        return f"{open_tag}</{self.tag}>"


