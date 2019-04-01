from blinker import Signal

from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *


class graphInputs(NodeBase):
    """Represents a group of input pins on subgraph node
    """
    def __init__(self, name):
        super(graphInputs, self).__init__(name)

    @staticmethod
    def pinTypeHints():
        return {'inputs': [], 'outputs': []}

    @staticmethod
    def category():
        return 'Common'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return ''

    def addOutPin(self):
        name = str(len(self.outputs))
        p = self.addOutputPin(name, 'AnyPin')
        p.actLikeDirection = PinDirection.Input
        # this will be passed to subgraph node for companion pin creation
        # and signals connection
        self.graph().inputPinCreated.send(p)
        # self.onPinCreated.send(p)
        return p

    def compute(self, *args, **kwargs):
        for i in self.outputs.values():
            for j in i.affected_by:
                i.setData(j.getData())

    def postCreate(self, jsonTemplate=None):
        super(graphInputs, self).postCreate(jsonTemplate=jsonTemplate)
        # recreate dynamically created pins
        pass


class graphOutputs(NodeBase):
    """Represents a group of output pins on subgraph node
    """
    def __init__(self, name):
        super(graphOutputs, self).__init__(name)

    @staticmethod
    def pinTypeHints():
        return {'inputs': [], 'outputs': []}

    @staticmethod
    def category():
        return 'Common'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return ''

    def postCreate(self, jsonTemplate=None):
        super(graphOutputs, self).postCreate(jsonTemplate=jsonTemplate)
        # recreate dynamically created pins
        pass

    def addInPin(self):
        name = str(len(self.outputs))
        p = self.addInputPin(name, 'AnyPin')
        p.actLikeDirection = PinDirection.Output
        p.setAlwaysPushDirty(True)
        self.graph().outputPinCreated.send(p)
        return p
