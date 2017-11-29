from AbstractGraph import *
from Settings import *
from Node import Node


class MakeInt(Node, NodeBase):
    def __init__(self, name, graph):
        super(MakeInt, self).__init__(name, graph, spacings=Spacings)
        self.output = self.add_output_port('out', DataTypes.Int)
        self.input = self.add_input_port('in', DataTypes.Int)

        portAffects(self.input, self.output)
        self.compute()

    @staticmethod
    def get_category():
        return 'GenericTypes'

    def compute(self):
        self.output.set_data(int(self.input.current_data()), False)
