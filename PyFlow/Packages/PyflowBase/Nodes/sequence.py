from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *


class sequence(NodeBase):
    def __init__(self, name):
        super(sequence, self).__init__(name)
        self.inExecPin = self.addInputPin('inExec', 'ExecPin', None, self.compute)

    def addOutPin(self):
        p = self.addOutputPin(str(len(self.outputs)), 'ExecPin')

    @staticmethod
    def pinTypeHints():
        return {'inputs': ['ExecPin'], 'outputs': ['ExecPin']}

    @staticmethod
    def category():
        return 'FlowControl'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return 'The Sequence node allows for a single execution pulse to trigger a series of events in order. The node may have any number of outputs, all of which get called as soon as the Sequence node receives an input. They will always get called in order, but without any delay. To a typical user, the outputs will likely appear to have been triggered simultaneously.'

    def addOutPin(self):
        name = str(len(self.outputs))
        p = self.addOutputPin(name, 'ExecPin')
        pinAffects(self.inExecPin, p)
        return p

    def compute(self):
        for out in self.outputs.values():
            out.call()
