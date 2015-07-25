from AbstractGraph import *


class AGIntNode(AGNode):
    def __init__(self, name, graph):
        super(AGIntNode, self).__init__(name, graph)
        self.graph = graph
        self.name = name
        self.output = self.add_output_port('out', AGPortDataTypes.tNumeric)
        self.set_data(0)
        self.val = 0

    def set_data(self, data, dirty_propagate=True):
        self.output.set_data(data, dirty_propagate)
        self.val = data

    def compute(self):

        self.output.set_data(self.val, False)
