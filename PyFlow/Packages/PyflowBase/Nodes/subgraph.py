import os
import json

from PyFlow.Core import NodeBase
from PyFlow.Core import GraphBase
from PyFlow.Core.Common import *


class subgraph(NodeBase):
    def __init__(self, name):
        super(subgraph, self).__init__(name)
        self.rawGraph = GraphBase(name)
        self.dinOutputs = {}
        self.dinInputs = {}

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
        return 'Encapsulate a graph inside a node'

    def addInPin(self, pin):
        p = self.addInputPin(pin.name, 'AnyPin', constraint="%s%s" % (pin.owningNode().name, pin.name))
        p.setAlwaysPushDirty(True)
        pin.constraint = "%s%s" % (pin.owningNode().name, pin.name)
        self._Constraints["%s%s" % (pin.owningNode().name, pin.name)].append(pin)
        pin.owningNode()._Constraints["%s%s" % (pin.owningNode().name, pin.name)] = [pin, p]
        self.dinInputs[pin] = p
        return p

    def addOutPin(self, pin):
        p = self.addOutputPin(pin.name, 'AnyPin', constraint="%s%s" % (pin.owningNode().name, pin.name))
        p.setAlwaysPushDirty(True)
        pin.constraint = "%s%s" % (pin.owningNode().name, pin.name)
        self._Constraints["%s%s" % (pin.owningNode().name, pin.name)].append(pin)
        pin.owningNode()._Constraints["%s%s" % (pin.owningNode().name, pin.name)] = [pin, p]
        self.dinOutputs[pin] = p
        return p

    def compute(self):
        for key, value in self.dinInputs.items():
            key.setData(value.getData())
        for key, value in self.dinOutputs.items():
            value.setData(key.getData())
