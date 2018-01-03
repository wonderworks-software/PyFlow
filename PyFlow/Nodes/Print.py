from Qt import QtCore
from AbstractGraph import *
from Settings import *
from Node import Node


class Print(Node, NodeBase):
    def __init__(self, name, graph):
        super(Print, self).__init__(name, graph)
        self.inExec = self.addInputPin("in", DataTypes.Exec, self.compute, True)
        self.outExec = self.addOutputPin("out", DataTypes.Exec, None, True)
        self.obj = self.addInputPin("string", DataTypes.String)

    @staticmethod
    def inputPinsTypes():
        return [DataTypes.String]

    @staticmethod
    def category():
        return 'String'

    def compute(self):
        if self.inExec.hasConnections():
            data = self.obj.getData()
            self.graph().writeToConsole(data)
        self.outExec.call()
