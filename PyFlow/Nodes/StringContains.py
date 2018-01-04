from Node import Node
from AbstractGraph import *


class StringContains(Node, NodeBase):
    def __init__(self, name, graph):
        super(StringContains, self).__init__(name, graph)
        self.first = self.addInputPin('source', DataTypes.String)
        self.second = self.addInputPin('pattern', DataTypes.String)
        self.output = self.addOutputPin('out', DataTypes.Bool)
        pinAffects(self.first, self.output)
        pinAffects(self.second, self.output)

    @staticmethod
    def pinTypeHints():
        return {'inputs': [DataTypes.String], 'outputs': [DataTypes.Bool]}

    @staticmethod
    def category():
        return 'String'

    def compute(self):

        first_str = self.first.getData()
        second_str = self.second.getData()
        try:
            result = second_str in first_str
            self.output.setData(result)
        except Exception, e:
            print e
