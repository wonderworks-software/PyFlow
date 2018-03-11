from ..Core.AbstractGraph import *
from ..Core.Settings import *
from ..Core import Node


class flipFlop(Node, NodeBase):
    def __init__(self, name, graph):
        super(flipFlop, self).__init__(name, graph)
        self.bState = True
        self.inp0 = self.addInputPin('in0', DataTypes.Exec, self.compute, hideLabel=True)
        self.outA = self.addOutputPin('A', DataTypes.Exec)
        self.outB = self.addOutputPin('B', DataTypes.Exec)
        self.bIsA = self.addOutputPin('IsA', DataTypes.Bool)

    @staticmethod
    def pinTypeHints():
        return {'inputs': [DataTypes.Exec], 'outputs': [DataTypes.Exec, DataTypes.Bool]}

    @staticmethod
    def category():
        return 'FlowControl'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return 'Changes flow each time called'

    def compute(self):
        if self.bState:
            self.bIsA.setData(self.bState)
            self.outA.call()
        else:
            self.bIsA.setData(self.bState)
            self.outB.call()
        self.bState = not self.bState
