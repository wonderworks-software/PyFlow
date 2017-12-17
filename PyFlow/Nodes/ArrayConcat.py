from AbstractGraph import *
from Settings import *
from Node import Node


class ArrayConcat(Node, NodeBase):
    def __init__(self, name, graph):
        super(ArrayConcat, self).__init__(name, graph, spacings=Spacings)
        self.arrayA = self.add_input_port('first', DataTypes.Array)
        self.arrayB = self.add_input_port('second', DataTypes.Array)
        self.result = self.add_output_port('out', DataTypes.Array)
        portAffects(self.arrayA, self.result)
        portAffects(self.arrayB, self.result)

    @staticmethod
    def category():
        return 'Array'

    def compute(self):

        first = self.arrayA.get_data()
        secont = self.arrayB.get_data()
        try:
            res_arr = first + secont
            self.result.set_data(res_arr)
        except Exception, e:
            print e
