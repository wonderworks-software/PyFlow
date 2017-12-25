from Qt import QtCore
from AbstractGraph import *
from Settings import *
from Node import Node


class Print(Node, NodeBase):
    def __init__(self, name, graph):
        super(Print, self).__init__(name, graph)
        self.inExec = self.addInputPin("in", DataTypes.Exec, self.compute, True)
        self.outExec = self.addOutputPin("out", DataTypes.Exec, None, True)
        self.data = self.addInputPin("data", DataTypes.Any)

    @staticmethod
    def category():
        return 'String'

    def compute(self):
        if self.inExec.hasConnections():
            self.graph().writeToConsole(self.data.getData())
            print(self.data.getData())
        self.outExec.call()
