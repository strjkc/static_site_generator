from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if self.value is None:
            raise Exception(ValueError, "All leaf nodes must have a value")
        if self.props:
            props_string = super().props_to_html()
            return f'<{self.tag}{props_string}>{self.value}</{self.tag}>'
        elif self.tag:
            return f'<{self.tag}>{self.value}</{self.tag}>'
        return f'{self.value}'


