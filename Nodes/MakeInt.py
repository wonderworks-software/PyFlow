from AbstractGraph import *
from AGraphPySide.Settings import *
from AGraphPySide import BaseNode


class MakeInt(BaseNode.Node, AGNode):
    def __init__(self, name, graph):
        super(MakeInt, self).__init__(name, graph, spacings=Spacings)
        self.output = self.add_output_port('out', AGPortDataTypes.tInt)
        self.input = self.add_input_port('in', AGPortDataTypes.tInt)

        portAffects(self.input, self.output)
        self.compute()

    @staticmethod
    def get_category():
        return 'GenericTypes'

    def compute(self):
        self.output.set_data(int(self.input.current_data()), False)
