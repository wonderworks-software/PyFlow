## Copyright 2015-2019 Ilgar Lunin, Pedro Cabrera

## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at

##     http://www.apache.org/licenses/LICENSE-2.0

## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.


from blinker import Signal

from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *


class graphInputs(NodeBase):
    """Represents a group of input pins on compound node
    """

    def __init__(self, name):
        super(graphInputs, self).__init__(name)
        self.bCacheEnabled = True

    def getUniqPinName(self, name):
        graphNodes = self.graph().getNodesList(
            classNameFilters=["graphInputs", "graphOutputs"]
        )
        conflictingPinNames = set()
        for node in graphNodes:
            for pin in node.pins:
                conflictingPinNames.add(pin.name)
        result = getUniqNameFromList(conflictingPinNames, name)
        return result

    @staticmethod
    def category():
        return "SubGraphs"

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return ""

    def addOutPin(self, name=None, dataType="AnyPin"):
        if name is None:
            name = self.getUniqPinName("in")
        p = self.createOutputPin(
            name,
            dataType,
            constraint=name,
            structConstraint=name,
            structure=StructureType.Multi,
        )
        p.enableOptions(PinOptions.RenamingEnabled | PinOptions.Dynamic)
        if dataType == "AnyPin":
            p.enableOptions(PinOptions.AllowAny | PinOptions.DictElementSupported)
        return p

    def compute(self, *args, **kwargs):
        for o in self.outputs.values():
            for i in o.affected_by:
                if len(i.affected_by) > 0:
                    for e in i.affected_by:
                        o.setData(e.getData())
                else:
                    o.setData(i.getData())

    def postCreate(self, jsonTemplate=None):
        super(graphInputs, self).postCreate(jsonTemplate=jsonTemplate)
        # recreate dynamically created pins
        existingPins = self.namePinOutputsMap
        if jsonTemplate is not None:
            sortedOutputs = sorted(jsonTemplate["outputs"], key=lambda x: x["pinIndex"])
            for outPinJson in sortedOutputs:
                if outPinJson["name"] not in existingPins:
                    dynOut = self.addOutPin(outPinJson["name"], outPinJson["dataType"])
                    dynOut.uid = uuid.UUID(outPinJson["uuid"])


class graphOutputs(NodeBase):
    """Represents a group of output pins on compound node
    """

    def __init__(self, name):
        super(graphOutputs, self).__init__(name)
        self.bCacheEnabled = False

    def getUniqPinName(self, name):
        graphNodes = self.graph().getNodesList(
            classNameFilters=["graphInputs", "graphOutputs"]
        )
        conflictingPinNames = set()
        for node in graphNodes:
            for pin in node.pins:
                conflictingPinNames.add(pin.name)
        result = getUniqNameFromList(conflictingPinNames, name)
        return result

    @staticmethod
    def category():
        return "SubGraphs"

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return ""

    def postCreate(self, jsonTemplate=None):
        super(graphOutputs, self).postCreate(jsonTemplate=jsonTemplate)
        # recreate dynamically created pins
        existingPins = self.namePinInputsMap
        if jsonTemplate is not None:
            sortedInputs = sorted(jsonTemplate["inputs"], key=lambda x: x["pinIndex"])
            for inPinJson in sortedInputs:
                if inPinJson["name"] not in existingPins:
                    inDyn = self.addInPin(inPinJson["name"], inPinJson["dataType"])
                    inDyn.uid = uuid.UUID(inPinJson["uuid"])

    def addInPin(self, name=None, dataType="AnyPin"):
        if name is None:
            name = self.getUniqPinName("out")
        p = self.createInputPin(
            name,
            dataType,
            constraint=name,
            structConstraint=name,
            structure=StructureType.Multi,
        )
        p.enableOptions(PinOptions.RenamingEnabled | PinOptions.Dynamic)
        if dataType == "AnyPin":
            p.enableOptions(PinOptions.AllowAny | PinOptions.DictElementSupported)
        return p

    def compute(self, *args, **kwargs):
        compoundNode = None
        for i in self.inputs.values():
            for o in i.affects:
                compoundNode = o.owningNode()
                o.setDirty()
        if compoundNode:
            compoundNode.processNode()
