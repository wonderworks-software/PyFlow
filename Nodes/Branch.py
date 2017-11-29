from PySide import QtCore
from AbstractGraph import *
from AGraphPySide.Settings import *
from AGraphPySide.Node import Node


class Branch(Node, NodeBase):
    def __init__(self, name, graph):
        super(Branch, self).__init__(name, graph)
        self.trueExec = self.add_output_port("True", DataTypes.Exec)
        self.falseExec = self.add_output_port("False", DataTypes.Exec)
        self.inExec = self.add_input_port("In", DataTypes.Exec, self.compute)
        self.condition = self.add_input_port("condition", DataTypes.Bool)

    @staticmethod
    def get_category():
        return 'FlowControl'

    def compute(self):
        data = self.condition.get_data()
        if data:
            self.trueExec.call()
        else:
            self.falseExec.call()
