from AbstractGraph import *
from Settings import *
from Node import Node


class IsArray(Node, NodeBase):
    def __init__(self, name, graph):
        super(IsArray, self).__init__(name, graph, spacings=Spacings)
        self.inp = self.addInputPin('obj', DataTypes.Any)
        self.out = self.addOutputPin('out', DataTypes.Bool)
        pinAffects(self.inp, self.out)

    @staticmethod
    def pinTypeHints():
        return {'inputs': [DataTypes.Any], 'outputs': [DataTypes.Bool]}

    @staticmethod
    def category():
        return 'Conditions'

    def compute(self):

        data = self.inp.getData()
        result = False
        try:
            len(data)
            result = True
        except Exception, e:
            result = False
            self.graph.writeToConsole("[ERROR] {0}. {1}".format(self.__class__.__name__, e))
        self.out.setData(result)
