from ..Core.AbstractGraph import *
from ..Core.Settings import *
from ..Core import Node


class forLoop(Node, NodeBase):
    def __init__(self, name, graph):
        super(forLoop, self).__init__(name, graph)
        self.inExec = self.addInputPin('inExec', DataTypes.Exec, self.compute, hideLabel=True)
        self.firstIndex = self.addInputPin('Start', DataTypes.Int)
        self.lastIndex = self.addInputPin('Stop', DataTypes.Int)
        self.step = self.addInputPin('Step', DataTypes.Int)
        self.step.setData(1)

        self.loopBody = self.addOutputPin('LoopBody', DataTypes.Exec)
        self.index = self.addOutputPin('Index', DataTypes.Int)
        self.completed = self.addOutputPin('Completed', DataTypes.Exec)

        pinAffects(self.firstIndex, self.index)
        pinAffects(self.lastIndex, self.index)
        pinAffects(self.step, self.index)

    @staticmethod
    def pinTypeHints():
        return {'inputs': [DataTypes.Exec, DataTypes.Int], 'outputs': [DataTypes.Exec, DataTypes.Int]}

    @staticmethod
    def category():
        return 'FlowControl'

    @staticmethod
    def keywords():
        return ['iter']

    @staticmethod
    def description():
        return 'For loop'

    def compute(self):
        indexFrom = self.firstIndex.getData()
        indexTo = self.lastIndex.getData()
        step = self.step.getData()
        if step == 0:
            self.completed.call()
        else:
            for i in range(indexFrom, indexTo, step):
                self.index.setData(i)
                self.loopBody.call()
            self.completed.call()
