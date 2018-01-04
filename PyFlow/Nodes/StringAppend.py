from Node import Node
from AbstractGraph import *


class StringAppend(Node, NodeBase):
    def __init__(self, name, graph):
        super(StringAppend, self).__init__(name, graph)
        self.first = self.addInputPin('first', DataTypes.String)
        self.second = self.addInputPin('second', DataTypes.String)
        self.output = self.addOutputPin('output', DataTypes.String)
        pinAffects(self.first, self.output)
        pinAffects(self.second, self.output)

    @staticmethod
    def pinTypeHints():
        return {'inputs': [DataTypes.String], 'outputs': [DataTypes.String]}

    @staticmethod
    def category():
        return 'String'

    def compute(self):

        first_str = self.first.getData()
        second_str = self.second.getData()
        try:
            result = first_str + second_str
            self.output.setData(result)
        except Exception, e:
            print e
