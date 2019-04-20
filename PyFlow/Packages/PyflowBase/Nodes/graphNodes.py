from blinker import Signal

from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *


class graphInputs(NodeBase):
    """Represents a group of input pins on compound node
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

    def addOutPin(self, name=None):
        if name is None:
            name = self.getUniqPinName('in')
        p = self.createOutputPin(name, 'AnyPin')
        p.setDynamic(True)
        p.setRenamingEnabled(True)
        p.singleInit = True
        # this will be passed to compound node for companion pin creation
        # and signals connection
        self.graph().inputPinCreated.send(p)
        return p

    def compute(self, *args, **kwargs):
        for i in self.outputs.values():
            for j in i.affected_by:
                i.setData(j.getData())

    def postCreate(self, jsonTemplate=None):
        super(graphInputs, self).postCreate(jsonTemplate=jsonTemplate)
        # recreate dynamically created pins
        if jsonTemplate is not None:
            for outPin in jsonTemplate["outputs"]:
                self.addOutPin(outPin['name'])


class graphOutputs(NodeBase):
    """Represents a group of output pins on compound node
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
        if jsonTemplate is not None:
            for outPin in jsonTemplate["inputs"]:
                self.addInPin(outPin['name'])

    def addInPin(self, name=None):
        if name is None:
            name = self.getUniqPinName('out')
        p = self.createInputPin(name, 'AnyPin')
        p.singleInit = True
        # p.setAlwaysPushDirty(True)
        self.graph().outputPinCreated.send(p)
        return p
