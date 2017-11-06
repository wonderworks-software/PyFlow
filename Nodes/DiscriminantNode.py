from AGraphPySide import BaseNode
from AbstractGraph import *


class DiscriminantNode(BaseNode.Node, AGNode):
    def __init__(self, name, graph):
        super(DiscriminantNode, self).__init__(name, graph)
        self.inputA = self.add_input_port('A', AGPortDataTypes.tFloat)
        self.inputB = self.add_input_port('B', AGPortDataTypes.tFloat)
        self.inputC = self.add_input_port('C', AGPortDataTypes.tFloat)
        self.output = self.add_output_port('out', AGPortDataTypes.tFloat)
        portAffects(self.inputA, self.output)
        portAffects(self.inputB, self.output)
        portAffects(self.inputC, self.output)

    @staticmethod
    def get_category():
        return 'Math'

    def compute(self):

        inpA_data = self.inputA.get_data()
        inpB_data = self.inputB.get_data()
        inpC_data = self.inputC.get_data()
        try:
            result = pow(inpB_data, 2) - 4 * inpA_data * inpC_data
        except Exception, e:
            print self.name, e
            return
        self.output.set_data(result, False)
