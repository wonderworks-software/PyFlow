from AbstractGraph import *
from Settings import *
from Node import Node
from Qt.QtWidgets import QCheckBox
from Qt.QtWidgets import QSizePolicy
from Qt.QtWidgets import QGraphicsProxyWidget

DESC = """Generic type node.
Boolean type."""


class BoolNode(Node, NodeBase):
    def __init__(self, name, graph):
        super(BoolNode, self).__init__(name, graph, spacings=Spacings)
        self.input = self.addInputPin('in', DataTypes.Bool, hideLabel=True)
        self.output = self.addOutputPin('out', DataTypes.Bool, hideLabel=True)
        pinAffects(self.input, self.output)

    @staticmethod
    def pinTypeHints():
        return {'inputs': [DataTypes.Bool], 'outputs': [DataTypes.Bool]}

    @staticmethod
    def description():
        return DESC

    @staticmethod
    def category():
        return 'GenericTypes'

    def compute(self):
        self.output.setData(self.input.getData())
