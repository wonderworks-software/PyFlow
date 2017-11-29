from AbstractGraph import *
from Settings import *
from Node import Node


class StringNode(Node, NodeBase):
    def __init__(self, name, graph):
        super(StringNode, self).__init__(name, graph, spacings=Spacings)
        self.input = self.add_input_port('in', DataTypes.String)
        self.output = self.add_output_port('out', DataTypes.String)

        portAffects(self.input, self.output)
        self.compute()

    @staticmethod
    def get_category():
        return 'GenericTypes'

    def compute(self):
        self.output.set_data(self.input.get_data(), False)
