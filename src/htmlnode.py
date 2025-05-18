
class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        # tag: string representing tag name "a", "h1" etc
        # value: string representing the value of html tag
        # children: list of HTMLNode objects representing the node's children
        # props: dict of attributes
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        # convert the props dictionary to string
        if self.props is None:
            return ""
        s = ""
        for k,v in self.props.items():
            s += " " + k + "=\"" + v + "\""
        return s
    
class LeafNode(HTMLNode):
    """
        Leaf Node is any value that is wrapping with open/close tags
        node = LeafNode("p", "Hello, world!")
    """
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        # returns HTML string rendered from leaf node
        if self.value is None:
            raise ValueError("Leaf node must have a value")
        if self.tag is None:
            return self.value
        
        props_str = self.props_to_html()
        return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"
            
class ParentNode(HTMLNode):
    """
        Parent Node is simply wrapping a list of LeafNodes with a tag
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
            ],
        )
    """
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        # return: string of HTML tag of the node AND its children

        # if object has no tag, ValueError
        if self.tag is None:
            raise ValueError("Parent node must have a tag")
        # if children is missing, ValueError
        if self.children is None or len(self.children) == 0:
            raise ValueError("Parent node cannot have missing children")

        # iterate over all children, call to_html on each
        results = ""
        for leaf in self.children:
            results += leaf.to_html()

        # add open/close tags of parent
        props_str = self.props_to_html()
        return f"<{self.tag}{props_str}>{results.strip()}</{self.tag}>"
