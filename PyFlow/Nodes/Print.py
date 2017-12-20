from Qt import QtCore
from AbstractGraph import *
from Settings import *
from Node import Node


class Print(Node, NodeBase):
    def __init__(self, name, graph):
        super(Print, self).__init__(name, graph)
        self.inExec = self.add_input_port("in", DataTypes.Exec, self.compute, True)
        self.outExec = self.add_output_port("out", DataTypes.Exec, None, True)
        self.data = self.add_input_port("data", DataTypes.Any)

    @staticmethod
    def category():
        return 'String'

    def compute(self):
        if self.inExec.hasConnections():
            self.graph().write_to_console(self.data.get_data())
            print(self.data.get_data())
        self.outExec.call()
