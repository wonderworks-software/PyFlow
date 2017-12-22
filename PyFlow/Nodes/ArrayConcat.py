from AbstractGraph import *
from Settings import *
from Node import Node


class ArrayConcat(Node, NodeBase):
    def __init__(self, name, graph):
        super(ArrayConcat, self).__init__(name, graph, spacings=Spacings)
        self.arrayA = self.addInputPin('first', DataTypes.Array)
        self.arrayB = self.addInputPin('second', DataTypes.Array)
        self.result = self.addOutputPin('out', DataTypes.Array)
        portAffects(self.arrayA, self.result)
        portAffects(self.arrayB, self.result)

    @staticmethod
    def category():
        return 'Array'

    def compute(self):

        first = self.arrayA.getData()
        secont = self.arrayB.getData()
        try:
            res_arr = first + secont
            self.result.setData(res_arr)
        except Exception, e:
            print e
