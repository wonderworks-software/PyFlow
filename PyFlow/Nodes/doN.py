from Core.AbstractGraph import *
from Core.Settings import *
from Core import Node


class doN(Node):
    def __init__(self, name, graph):
        super(doN, self).__init__(name, graph)
        self.enter = self.addInputPin('enter', DataTypes.Exec, self.compute, hideLabel=True)
        self.N = self.addInputPin('n', DataTypes.Int)
        self.N.setData(10)
        self.reset = self.addInputPin('reset', DataTypes.Exec, self.OnReset)

        self.completed = self.addOutputPin('exit', DataTypes.Exec)
        self.counter = self.addOutputPin('counter', DataTypes.Int)
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
        return 'The DoN node will fire off an execution pin N times. After the limit has been reached, it will cease all outgoing execution until a pulse is sent into its Reset input.'

    def compute(self):
        maxCalls = self.N.getData()
        if not self.bClosed and self._numCalls <= maxCalls:
            self._numCalls += 1
            self.counter.setData(self._numCalls)
            self.completed.call()

            # if next time we will reach the limit - close
            if (self._numCalls + 1) > maxCalls:
                self.bClosed = True
