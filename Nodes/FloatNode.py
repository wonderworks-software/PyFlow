from AbstractGraph import *
from AGraphPySide.Settings import *
from AGraphPySide import BaseNode


class FloatNode(BaseNode.Node, AGNode):
    def __init__(self, name, graph):
        super(FloatNode, self).__init__(name, graph, spacings=Spacings)
        self.input = self.add_input_port('in', AGPortDataTypes.tFloat)
        self.output = self.add_output_port('out', AGPortDataTypes.tFloat)

        portAffects(self.input, self.output)
        self.compute()

    @staticmethod
    def get_category():
        return 'GenericTypes'

    def compute(self):
        self.output.set_data(float(self.input.current_data()), False)
