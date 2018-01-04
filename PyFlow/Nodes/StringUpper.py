from AbstractGraph import *
from Settings import *
from Node import Node


class StringUpper(Node, NodeBase):
    def __init__(self, name, graph):
        super(StringUpper, self).__init__(name, graph, spacings=Spacings)
        self.in_str = self.addInputPin('str', DataTypes.String)
        self.out_str = self.addOutputPin('upper str', DataTypes.String)
        pinAffects(self.in_str, self.out_str)

    @staticmethod
    def pinTypeHints():
        return {'inputs': [DataTypes.String], 'outputs': [DataTypes.String]}

    @staticmethod
    def category():
        return 'String'

    def compute(self):

        str_data = self.in_str.getData()
        try:
            self.out_str.setData(str_data.upper())
        except Exception, e:
            print e
