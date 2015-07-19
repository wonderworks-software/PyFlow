import BaseNode
from Settings import *
from Port import *
from PySide import QtCore
from AbstractGraph import *


class SumNode(BaseNode.Node, AGNode):
    def __init__(self, name, graph):
        super(SumNode, self).__init__(name, graph)
        AGNode.__init__(self, name)
        self.graph = graph
        self.inputA = self.add_input_port('inputA')
        self.inputB = self.add_input_port('inputB')
        self.output = self.add_output_port('output')
        portAffects(self.inputA, self.output)
        portAffects(self.inputB, self.output)

    def compute(self):

        inpA_data = self.inputA.get_data()
        inpB_data = self.inputB.get_data()

        result = inpA_data + inpB_data

        self.output.set_data(result)
