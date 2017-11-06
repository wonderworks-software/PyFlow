from AGraphPySide import BaseNode
from AbstractGraph import *


class MultNode(BaseNode.Node, AGNode):
    def __init__(self, name, graph):
        super(MultNode, self).__init__(name, graph, color=BaseNode.getPortColorByType(AGPortDataTypes.tInt))
        self.inputA = self.add_input_port('inputA', AGPortDataTypes.tFloat)
        self.inputB = self.add_input_port('inputB', AGPortDataTypes.tFloat)
        self.output = self.add_output_port('output', AGPortDataTypes.tFloat)
        portAffects(self.inputA, self.output)
        portAffects(self.inputB, self.output)

    @staticmethod
    def get_category():
        return 'Math'

    def compute(self):

        inp_a_data = self.inputA.get_data()
        inp_b_data = self.inputB.get_data()
        try:
            result = inp_a_data * inp_b_data
            self.output.set_data(result, False)
        except Exception, e:
            print e
