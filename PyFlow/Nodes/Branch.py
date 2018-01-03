from Qt import QtCore
from AbstractGraph import *
from Settings import *
from Node import Node


class Branch(Node, NodeBase):
    def __init__(self, name, graph):
        super(Branch, self).__init__(name, graph)
        self.trueExec = self.addOutputPin("True", DataTypes.Exec)
        self.falseExec = self.addOutputPin("False", DataTypes.Exec)
        self.inExec = self.addInputPin("In", DataTypes.Exec, self.compute)
        self.condition = self.addInputPin("condition", DataTypes.Bool)

    @staticmethod
    def inputPinsTypes():
        return [DataTypes.Exec, DataTypes.Bool]

    @staticmethod
    def category():
        return 'FlowControl'

    def compute(self):
        data = self.condition.getData()
        if data:
            self.trueExec.call()
        else:
            self.falseExec.call()
