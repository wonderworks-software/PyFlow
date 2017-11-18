from PySide import QtCore
from AbstractGraph import *
from AGraphPySide.Settings import *
from AGraphPySide import BaseNode


class Branch(BaseNode.Node, AGNode):
    def __init__(self, name, graph):
        super(Branch, self).__init__(name, graph)
        self.trueExec = self.add_output_port("True", AGPortDataTypes.tExec)
        self.falseExec = self.add_output_port("False", AGPortDataTypes.tExec)
        self.inExec = self.add_input_port("In", AGPortDataTypes.tExec, self.compute)
        self.condition = self.add_input_port("condition", AGPortDataTypes.tBool)

    @staticmethod
    def get_category():
        return 'FlowControl'

    def compute(self):
        data = self.condition.get_data()
        if data:
            self.trueExec.call()
        else:
            self.falseExec.call()
