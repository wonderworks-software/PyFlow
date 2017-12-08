from Node import Node
from AbstractGraph import *


class AddFloat(Node, NodeBase):
    def __init__(self, name, graph):
        super(AddFloat, self).__init__(name, graph)
        self.inputB = self.add_input_port('inputB', DataTypes.Float)
        self.inputA = self.add_input_port('inputA', DataTypes.Float)
        self.output = self.add_output_port('output', DataTypes.Float)
        portAffects(self.inputA, self.output)
        portAffects(self.inputB, self.output)

    @staticmethod
    def get_category():
        return 'Math'

    def compute(self):

        inp_a_data = self.inputA.get_data()
        inp_b_data = self.inputB.get_data()
        try:
            result = inp_a_data + inp_b_data
            self.output.set_data(result)
        except Exception, e:
            print e
