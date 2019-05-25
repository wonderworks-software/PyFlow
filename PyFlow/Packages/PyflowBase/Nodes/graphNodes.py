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

    def getUniqPinName(self, name):
        result = name
        if self.graph is not None:
            owningCompoundNode = self.graph().graphManager.findNode(self.graph().name)
            if owningCompoundNode is not None:
                result = owningCompoundNode.getUniqPinName(name)
            else:
                result = self.graph().graphManager.getUniqName(name)
        return result

    @staticmethod
    def category():
        return 'Common'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return ''

    def addOutPin(self, name=None, dataType="AnyPin"):
        if name is None:
            name = self.getUniqPinName('in')
        p = self.createOutputPin(name, dataType, constraint=name, structConstraint=name, structure=PinStructure.Multi)
        p.enableOptions(PinOptions.RenamingEnabled | PinOptions.Dynamic)
        return p

    def compute(self, *args, **kwargs):
        for i in self.outputs.values():
            for j in i.affected_by:
                i.setData(j.getData())

    def postCreate(self, jsonTemplate=None):
        super(graphInputs, self).postCreate(jsonTemplate=jsonTemplate)
        # recreate dynamically created pins
        existingPins = self.namePinOutputsMap
        if jsonTemplate is not None:
            for outPinJson in jsonTemplate["outputs"]:
                if outPinJson['name'] not in existingPins:
                    dynOut = self.addOutPin(outPinJson['name'], outPinJson["dataType"])
                    dynOut.uid = uuid.UUID(outPinJson['uuid'])


class graphOutputs(NodeBase):
    """Represents a group of output pins on compound node
    """
    def __init__(self, name):
        super(graphOutputs, self).__init__(name)

    def getUniqPinName(self, name):
        result = name
        if self.graph is not None:
            owningCompoundNode = self.graph().graphManager.findNode(self.graph().name)
            if owningCompoundNode is not None:
                result = owningCompoundNode.getUniqPinName(name)
            else:
                result = self.graph().graphManager.getUniqName(name)
        return result

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
        existingPins = self.namePinInputsMap
        if jsonTemplate is not None:
            for inPinJson in jsonTemplate["inputs"]:
                if inPinJson['name'] not in existingPins:
                    inDyn = self.addInPin(inPinJson['name'], inPinJson["dataType"])
                    inDyn.uid = uuid.UUID(inPinJson['uuid'])

    def addInPin(self, name=None, dataType="AnyPin"):
        if name is None:
            name = self.getUniqPinName('out')
        p = self.createInputPin(name, dataType,constraint=name,structConstraint=name,structure=PinStructure.Multi)
        p.enableOptions(PinOptions.RenamingEnabled | PinOptions.Dynamic)
        return p
