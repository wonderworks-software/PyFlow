from PyFlow.Core import NodeBase
from PyFlow.Core.AGraphCommon import *


class graphInputs(NodeBase):
    def __init__(self, name):
        super(graphInputs, self).__init__(name)

    @staticmethod
    def pinTypeHints():
        return {'inputs': [], 'outputs': []}

    @staticmethod
    def category():
        return '__hiden__'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return ''

    def addOutPin(self):
        name = str(len(self.outputs))
        p = self.addOutputPin(name, 'AnyPin')
        p.setAlwaysPushDirty(True)
        if p.uid not in self.graph().pins:
            self.graph().pins[p.uid] = p
        return p

class graphOutputs(NodeBase):
    def __init__(self, name):
        super(graphOutputs, self).__init__(name)

    @staticmethod
    def pinTypeHints():
        return {'inputs': [], 'outputs': []}

    @staticmethod
    def category():
        return '__hiden__'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return ''

    def addInPin(self):
        name = str(len(self.outputs))
        p = self.addInputPin(name, 'AnyPin')
        p.setAlwaysPushDirty(True)
        if p.uid not in self.graph().pins:
            self.graph().pins[p.uid] = p
        return p
