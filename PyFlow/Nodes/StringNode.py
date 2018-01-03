from AbstractGraph import *
from Settings import *
from Node import Node


class StringNode(Node, NodeBase):
    def __init__(self, name, graph):
        super(StringNode, self).__init__(name, graph, spacings=Spacings)
        self.input = self.addInputPin('in', DataTypes.String)
        self.output = self.addOutputPin('out', DataTypes.String)

        portAffects(self.input, self.output)
        self.compute()

    @staticmethod
    def inputPinsTypes():
        return [DataTypes.String]

    @staticmethod
    def category():
        return 'GenericTypes'

    def compute(self):
        self.output.setData(self.input.getData())
