from PyFlow.Core.AbstractGraph import *

# class TestGraph(Core.AbstractGraph.Graph):
#     def __init__(self, name):
#         super(TestGraph, self).__init__(name)

G = Graph("TestGraph")


class AddNode(NodeBase):
    def __init__(self, name, graph):
        super(AddNode, self).__init__(name, graph)
        self.a = self.addInputPin("A", DataTypes.Float, 2.0)
        self.b = self.addInputPin("B", DataTypes.Float, 2.0)
        self.out = self.addOutputPin("Out", DataTypes.Float)
        pinAffects(self.a, self.out)
        pinAffects(self.b, self.out)

    @staticmethod
    def pinTypeHints():
        return {'inputs': [DataTypes.Float], 'outputs': [DataTypes.Float]}

    @staticmethod
    def category():
        return 'Utils'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return 'None'

    def compute(self):
        a = self.a.getData()
        b = self.b.getData()
        self.out.setData(a + b)

addition = AddNode("add", G)

print(addition.out.getData())
