from ..Core.AbstractGraph import *
from ..Core.Settings import *
from ..Core import Node


class doN(NodeBase):
    def __init__(self, name):
        super(doN, self).__init__(name)
        self.enter = self.addInputPin('Enter', DataTypes.Exec, self.compute)
        self._N = self.addInputPin('N', DataTypes.Int)
        self._N.setData(10)
        self.reset = self.addInputPin('Reset', DataTypes.Exec, self.OnReset)

        self.completed = self.addOutputPin('Exit', DataTypes.Exec)
        self.counter = self.addOutputPin('Counter', DataTypes.Int)
        self.bClosed = False
        self._numCalls = 0

    def OnReset(self):
        self.bClosed = False
        self._numCalls = 0

    @staticmethod
    def pinTypeHints():
        return {'inputs': [DataTypes.Exec, DataTypes.Int], 'outputs': [DataTypes.Exec, DataTypes.Int]}

    @staticmethod
    def category():
        return 'FlowControl'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return 'The DoN node will fire off an execution pin N times. After the limit has been reached,\
        it will cease all outgoing execution until a pulse is sent into its Reset input.'

    def compute(self):
        maxCalls = self._N.getData()
        if not self.bClosed and self._numCalls <= maxCalls:
            self._numCalls += 1
            self.counter.setData(self._numCalls)
            self.completed.call()

            # if next time we will reach the limit - close
            if (self._numCalls + 1) > maxCalls:
                self.bClosed = True
