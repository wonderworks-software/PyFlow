from AbstractGraph import *
from Settings import *
from Node import Node


DESC = '''node desc
'''


class RetriggerableDelay(Node, NodeBase):
    def __init__(self, name, graph):
        super(RetriggerableDelay, self).__init__(name, graph, w=80, spacings=Spacings)
        self.inp0 = self.addInputPin('in0', DataTypes.Exec, self.compute)
        self.delay = self.addInputPin('delay(s)', DataTypes.Float)
        self.out0 = self.addOutputPin('out0', DataTypes.Exec)
        self.count = 0.0
        self.process = False

    @staticmethod
    def pinTypeHints():
        return {'inputs': [DataTypes.Exec, DataTypes.Float], 'outputs': [DataTypes.Exec]}

    @staticmethod
    def category():
        return 'FlowControl'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return DESC

    def Tick(self, delta):
        if self.process:
            self.count += delta
            if self.count > self.delay.getData():
                self.out0.call()
                self.reset()

    def reset(self):
        self.process = False
        self.count = 0.0

    def compute(self):
        if self.process:
            self.reset()
        self.process = True
