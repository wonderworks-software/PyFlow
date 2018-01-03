from AbstractGraph import *
from Settings import *
from Node import Node


class ForLoop(Node, NodeBase):
    def __init__(self, name, graph):
        super(ForLoop, self).__init__(name, graph, w=100, spacings=Spacings)
        self.inExec = self.addInputPin('inExec', DataTypes.Exec, self.compute, hideLabel=True)
        self.firstIndex = self.addInputPin('from', DataTypes.Int)
        self.lastIndex = self.addInputPin('to', DataTypes.Int)
        self.step = self.addInputPin('step', DataTypes.Int)
        self.step.setData(1)

        self.loopBody = self.addOutputPin('LoopBody', DataTypes.Exec)
        self.index = self.addOutputPin('Index', DataTypes.Int)
        self.completed = self.addOutputPin('Completed', DataTypes.Exec)

        portAffects(self.firstIndex, self.index)
        portAffects(self.lastIndex, self.index)
        portAffects(self.step, self.index)

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
        for i in range(indexFrom, indexTo, step):
            self.index.setData(i)
            self.loopBody.call()
            push(self.index)
        self.completed.call()
