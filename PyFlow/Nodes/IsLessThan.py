from Node import Node
from AbstractGraph import *


class IsLessThan(Node, NodeBase):
    def __init__(self, name, graph):
        super(IsLessThan, self).__init__(name, graph)
        self.inputA = self.add_input_port('inputA', DataTypes.Float)
        self.inputB = self.add_input_port('inputB', DataTypes.Float)
        self.output = self.add_output_port('output', DataTypes.Bool)
        portAffects(self.inputA, self.output)
        portAffects(self.inputB, self.output)

    @staticmethod
    def category():
        return 'Conditions'

    def compute(self):

        inp_a_data = self.inputA.get_data()
        inp_b_data = self.inputB.get_data()
        try:
            if inp_a_data < inp_b_data:
                self.output.set_data(True)
            else:
                self.output.set_data(False)
        except Exception, e:
            print e
            self.output.set_data(False)
