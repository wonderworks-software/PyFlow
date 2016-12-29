from AGraphPySide import BaseNode
from AbstractGraph import *


class DiscriminantNode(BaseNode.Node, AGNode):
    def __init__(self, name, graph):
        super(DiscriminantNode, self).__init__(name, graph)
        AGNode.__init__(self, name, graph)
        self.inputA = self.add_input_port('A', AGPortDataTypes.tNumeric)
        self.inputB = self.add_input_port('B', AGPortDataTypes.tNumeric)
        self.inputC = self.add_input_port('C', AGPortDataTypes.tNumeric)
        self.output = self.add_output_port('out', AGPortDataTypes.tNumeric)
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
            result = pow(inpB_data, 2) - 4*inpA_data*inpC_data
        except Exception, e:
            print self.name, e
            return
        self.output.set_data(result, False)
