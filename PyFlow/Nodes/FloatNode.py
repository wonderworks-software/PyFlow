from AbstractGraph import *
from Settings import *
from Node import Node


class FloatNode(Node, NodeBase):
    def __init__(self, name, graph):
        super(FloatNode, self).__init__(name, graph, spacings=Spacings)
        self.input = self.add_input_port('in', DataTypes.Float)
        self.output = self.add_output_port('out', DataTypes.Float)

        portAffects(self.input, self.output)
        self.compute()

    @staticmethod
    def get_category():
        return 'GenericTypes'

    def compute(self):
        self.output.set_data(float(self.input.current_data()))
