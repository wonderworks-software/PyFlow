from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *
from copy import copy


class reroute(NodeBase):
    def __init__(self, name):
        super(reroute, self).__init__(name)
        self.input = self.createInputPin("in", 'AnyPin', constraint="1")
        self.input.enableOptions(PinOptions.ListSupported | PinOptions.ExecSupported)
        self.output = self.createOutputPin("out", 'AnyPin', constraint="1")
        self.output.enableOptions(PinOptions.ListSupported | PinOptions.ExecSupported)
        pinAffects(self.input, self.output)
        self.input.call = self.output.call

    @staticmethod
    def pinTypeHints():
        return {'inputs': [], 'outputs': []}

    @staticmethod
    def category():
        return 'Common'

    def compute(self, *args, **kwargs):
        self.output.setData(self.input.getData())
