from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *
from copy import copy


class reroute(NodeBase):
    def __init__(self, name):
        super(reroute, self).__init__(name)
        self.input = self.addInputPin("in", 'AnyPin', constraint="1")
        self.output = self.addOutputPin("out", 'AnyPin', constraint="1")
        pinAffects(self.input, self.output)
        self.input.call = self.output.call

    @staticmethod
    def pinTypeHints():
        return {'inputs': [], 'outputs': []}

    @staticmethod
    def category():
        return 'Common'

    def compute(self):
        self.output.setData(copy(self.input.getData()))
