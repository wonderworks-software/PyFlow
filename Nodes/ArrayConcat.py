from AbstractGraph import *
from AGraphPySide.Settings import *
from AGraphPySide import BaseNode


class ArrayConcat(BaseNode.Node, AGNode):
    def __init__(self, name, graph):
        super(ArrayConcat, self).__init__(name, graph, spacings=Spacings)
        self.arrayA = self.add_input_port('first', AGPortDataTypes.tArray)
        self.arrayB = self.add_input_port('second', AGPortDataTypes.tArray)
        self.result = self.add_output_port('out', AGPortDataTypes.tArray)
        portAffects(self.arrayA, self.result)
        portAffects(self.arrayB, self.result)


    @staticmethod
    def get_category():
        return 'Array'

    def compute(self):

        first = self.arrayA.get_data()
        secont = self.arrayB.get_data()
        try:
            res_arr = first + secont
            self.result.set_data(res_arr, False)
        except Exception, e:
            print e
