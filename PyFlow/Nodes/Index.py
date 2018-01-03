from AbstractGraph import *
from Settings import *
from Node import Node


class Index(Node, NodeBase):
    def __init__(self, name, graph):
        super(Index, self).__init__(name, graph, spacings=Spacings)
        self.inArray = self.addInputPin('iterable', DataTypes.Any)
        self.value = self.addInputPin('value', DataTypes.Any)
        self.index = self.addOutputPin('idx', DataTypes.Float)
        self.success = self.addOutputPin('success', DataTypes.Bool)
        portAffects(self.inArray, self.index)
        portAffects(self.value, self.index)

    @staticmethod
    def inputPinsTypes():
        return [DataTypes.Any]

    @staticmethod
    def category():
        return 'Array'

    def compute(self):

        ls = self.inArray.getData()
        value = self.value.getData()
        try:
            idx = ls.index(value)
            self.index.setData(int(idx))
            self.success.setData(True)
        except Exception, e:
            self.success.setData(False)
            self.graph.writeToConsole("[ERROR] {0}. {1}".format(self.__class__.__name__, e))
