from AbstractGraph import *
from Settings import *
from Node import Node


class FloatNode(Node, NodeBase):
    def __init__(self, name, graph):
        super(FloatNode, self).__init__(name, graph, spacings=Spacings)
        self.input = self.addInputPin('in', DataTypes.Float)
        self.output = self.addOutputPin('out', DataTypes.Float)

        pinAffects(self.input, self.output)
        self.compute()

    @staticmethod
    def pinTypeHints():
        return {'inputs': [DataTypes.Float], 'outputs': [DataTypes.Float]}

    @staticmethod
    def category():
        return 'GenericTypes'

    def compute(self):
        self.output.setData(float(self.input.currentData()))
