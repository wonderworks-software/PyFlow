from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *
from copy import copy


class rerouteExecs(NodeBase):
    def __init__(self, name):
        super(rerouteExecs, self).__init__(name)
        self.input = self.createInputPin("in", 'ExecPin')
        self.output = self.createOutputPin("out", 'ExecPin')
        pinAffects(self.input, self.output)
        self.input.call = self.output.call

    def postCreate(self, jsonTemplate=None):
        super(rerouteExecs, self).postCreate(jsonTemplate=jsonTemplate)
        self.setName("reroute")

    @staticmethod
    def pinTypeHints():
        return {'inputs': [], 'outputs': []}

    @staticmethod
    def category():
        return 'Common'

    def compute(self, *args, **kwargs):
        pass
