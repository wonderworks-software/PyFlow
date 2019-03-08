from PyFlow.Core import NodeBase
from PyFlow.Core.AGraphCommon import *
from copy import copy

class rerute(NodeBase):
    def __init__(self, name):
        super(rerute, self).__init__(name)
        self.input = self.addInputPin("in", 'AnyPin',constraint="1")
        self.output = self.addOutputPin("out", 'AnyPin',constraint="1")
        pinAffects(self.input, self.output)

    @staticmethod
    def pinTypeHints():
        return {'inputs': ['ExecPin', 'BoolPin'], 'outputs': ['BoolPin']}

    @staticmethod
    def category():
        return 'FlowControl'

    def compute(self):
        self.output.setData(copy(self.input.getData()))
