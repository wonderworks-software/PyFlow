from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *


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

    def compute(self):
        # This node is special. Output pins of this node are actually inputs pins in terms of execution and data gathering
        # We get data from input pin on subgraphNode and put it to corresponding output pin on graphInputs node
        for valuePin in [p for p in self.outputs.values() if p.IsValuePin()]:
            # this can be changed to support multiple connections later
            # affected_by is list of connected pins
            valuePin.setData(valuePin.affected_by[0].getData())


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
