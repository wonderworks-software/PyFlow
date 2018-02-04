from Core.AbstractGraph import *
from Core.Settings import *
from Core import Node


class deltaTime(Node):
    def __init__(self, name, graph):
        super(deltaTime, self).__init__(name, graph)
        self._deltaTime = 0.0
        self.out0 = self.addOutputPin('out0', DataTypes.Float)

    @staticmethod
    def pinTypeHints():
        return {'inputs': [], 'outputs': [DataTypes.Float]}

    @staticmethod
    def category():
        return 'Utils'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return 'Editor delta time.'

    def Tick(self, deltaTime):
        self._deltaTime = deltaTime

    def compute(self):
        self.out0.setData(self._deltaTime)
