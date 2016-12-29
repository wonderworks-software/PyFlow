from AGraphPySide import BaseNode
from AbstractGraph import *


class IsGreaterThan(BaseNode.Node, AGNode):
    def __init__(self, name, graph):
        super(IsGreaterThan, self).__init__(name, graph)
        AGNode.__init__(self, name, graph)
        self.inputA = self.add_input_port('inputA', AGPortDataTypes.tNumeric)
        self.inputB = self.add_input_port('inputB', AGPortDataTypes.tNumeric)
        self.output = self.add_output_port('output', AGPortDataTypes.tBool)
        portAffects(self.inputA, self.output)
        portAffects(self.inputB, self.output)

    @staticmethod
    def get_category():
        return 'Conditions'

    def compute(self):

        inp_a_data = self.inputA.get_data()
        inp_b_data = self.inputB.get_data()
        try:
            if inp_a_data > inp_b_data:
                self.output.set_data(True, False)
            else:
                self.output.set_data(False, False)
        except Exception, e:
            print e
            self.output.set_data(False, False)
