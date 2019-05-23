from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *


class consoleOutput(NodeBase):
    def __init__(self, name):
        super(consoleOutput, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.entity = self.createInputPin('entity', 'AnyPin', structure=PinStructure.Multi)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

    @staticmethod
    def pinTypeHints():
        return {'inputs': ['AnyPin'], 'outputs': ['AnyPin']}

    @staticmethod
    def category():
        return 'DefaultLib'

    @staticmethod
    def keywords():
        return ['print']

    @staticmethod
    def description():
        return "Python's 'print' function wrapper"

    def compute(self, *args, **kwargs):
        print(self.entity.getData())
        self.outExec.call()
