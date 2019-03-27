from blinker import Signal

from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *


class graphInputs(NodeBase):
    """Represents a group of input pins on subgraph node
    """
    def __init__(self, name):
        super(graphInputs, self).__init__(name)
        self.onPinCreated = Signal(object)

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
        p.setAlwaysPushDirty(True)
        p.actLikeDirection = PinDirection.Input
        self.onPinCreated.send(p)
        return p

    def postCreate(self, jsonTemplate=None):
        super(graphInputs, self).postCreate(jsonTemplate=jsonTemplate)
        # recreate dynamically created pins
        # connect with owning graph before
        self.onPinCreated.connect(self.graph().onInputPinCreated.send)
        # add outputs
        pass

    def compute(self):
        # This node is special. Output pins of this node are actually inputs pins in terms of execution and data gathering
        # We get data from input pin on subgraphNode and put it to corresponding output pin on graphInputs node
        for valuePin in [p for p in self.outputs.values() if p.IsValuePin()]:
            # this can be changed to support multiple connections later
            # affected_by is list of connected pins
            valuePin.setData(list(valuePin.affected_by)[0].getData())


class graphOutputs(NodeBase):
    """Represents a group of output pins on subgraph node
    """
    def __init__(self, name):
        super(graphOutputs, self).__init__(name)
        self.onPinCreated = Signal(object)

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
        # connect with owning graph before
        self.onPinCreated.connect(self.graph().onOutputPinCreated.send)
        # add outputs
        pass

    def addInPin(self):
        name = str(len(self.outputs))
        p = self.addInputPin(name, 'AnyPin')
        p.actLikeDirection = PinDirection.Output
        p.setAlwaysPushDirty(True)
        self.onPinCreated.send(p)
        return p
