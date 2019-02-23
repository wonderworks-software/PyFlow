from PyFlow.UI.Node import Node

class UISwitchOnString(Node):
    def __init__(self, raw_node, w=80, color=Colors.NodeBackgrounds, headColor=Colors.NodeNameRect, bUseTextureBg=True):
        super(Node, self).__init__(raw_node, w=w, color=color, headColor=headColor, bUseTextureBg=bUseTextureBg)
