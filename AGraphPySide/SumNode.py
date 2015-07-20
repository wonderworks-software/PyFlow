import BaseNode
from AbstractGraph import *


class SumNode(BaseNode.Node, AGNode):
    def __init__(self, name, graph):
        super(SumNode, self).__init__(name, graph)
        AGNode.__init__(self, name, graph)
        self.inputA = self.add_input_port('inputA')
        self.inputB = self.add_input_port('inputB')
        self.output = self.add_output_port('output')
        portAffects(self.inputA, self.output)
        portAffects(self.inputB, self.output)

    def compute(self):

        inp_a_data = self.inputA.get_data()
        inp_b_data = self.inputB.get_data()

        result = inp_a_data + inp_b_data

        self.output.set_data(result)
