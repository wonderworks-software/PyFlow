from AbstractGraph import *
from Settings import *
from Node import Node


class MakeInt(Node, NodeBase):
    def __init__(self, name, graph):
        super(MakeInt, self).__init__(name, graph, spacings=Spacings)
        self.output = self.addOutputPin('out', DataTypes.Int)
        self.input = self.addInputPin('in', DataTypes.Int)

        pinAffects(self.input, self.output)
        self.compute()

    @staticmethod
    def pinTypeHints():
        return {'inputs': [DataTypes.Int], 'outputs': [DataTypes.Int]}

    @staticmethod
    def category():
        return 'GenericTypes'

    def compute(self):
        self.output.setData(int(self.input.currentData()))
