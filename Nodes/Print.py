from PySide import QtCore
from AbstractGraph import *
from AGraphPySide.Settings import *
from AGraphPySide import BaseNode


class Print(BaseNode.Node, AGNode):
    def __init__(self, name, graph):
        super(Print, self).__init__(name, graph)
        self.inExec = self.add_input_port("IN", AGPortDataTypes.tExec, self.compute)
        self.data = self.add_input_port("data", AGPortDataTypes.tAny)

    @staticmethod
    def get_category():
        return 'Util'

    def compute(self):
        self.graph().write_to_console(self.data.get_data(), True)
