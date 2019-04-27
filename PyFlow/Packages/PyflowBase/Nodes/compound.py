import os
import json
import weakref
from copy import deepcopy

from blinker import Signal

from PyFlow.Core import NodeBase
from PyFlow.Core import GraphBase
from PyFlow.Core.Common import *


class compound(NodeBase):
    """this node encapsulates a graph, like compound in xsi

    pins can be edited only from inside the compound
    """
    def __init__(self, name):
        super(compound, self).__init__(name)
        self.pinExposed = Signal(object)
        self._rawGraph = None
        self.__inputsMap = {}
        self.__outputsMap = {}

    @property
    def rawGraph(self):
        return self._rawGraph

    @rawGraph.setter
    def rawGraph(self, newGraph):
        assert(newGraph is not None)
        self._rawGraph = newGraph

    def syncPins(self):
        # look for graph nodes pins was added
        nodeInputPins = self.namePinInputsMap
        nodeOutputPins = self.namePinOutputsMap

        graphInputsNodes = self.rawGraph.getNodes(classNameFilters=['graphInputs'])
        graphInputPins = {}
        for graphInputNode in graphInputsNodes:
            for outPin in graphInputNode.outputs.values():
                graphInputPins[outPin.name] = outPin
                # create companion pin if needed
                if outPin.name not in nodeInputPins:
                    self.onGraphInputPinCreated(outPin)

        graphOutputNodes = self.rawGraph.getNodes(classNameFilters=['graphOutputs'])
        graphOutputPins = {}
        for graphOutputNode in graphOutputNodes:
            for inPin in graphOutputNode.inputs.values():
                graphOutputPins[inPin.name] = inPin
                # create companion pin if needed
                if inPin.name not in nodeOutputPins:
                    self.onGraphOutputPinCreated(inPin)

        for nodeInputPinName, nodeInputPin in nodeInputPins.items():
            if nodeInputPinName not in graphInputPins:
                if nodeInputPin in self.__inputsMap:
                    nodeInputPin.kill()
                    clearSignal(nodeInputPin.killed)
                    self.__inputsMap.pop(nodeInputPin)

        for nodeOutputPinName, nodeOutputPin in nodeOutputPins.items():
            if nodeOutputPinName not in graphOutputPins:
                if nodeOutputPin in self.__outputsMap:
                    nodeOutputPin.kill()
                    clearSignal(nodeOutputPin.killed)
                    self.__outputsMap.pop(nodeOutputPin)

    def Tick(self, delta):
        self.syncPins()
        self.rawGraph.Tick(delta)
        super(compound, self).Tick(delta)

    def setName(self, name):
        super(compound, self).setName(name)
        if self.rawGraph is not None:
            self.rawGraph.name = self.getName()

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

    def serialize(self, copying=False):
        default = NodeBase.serialize(self, copying=copying)
        default['graphData'] = self.rawGraph.serialize(copying=copying)
        return default

    def onGraphInputPinCreated(self, outPin):
        """Reaction when pin added to graphInputs node

        Arguments:
            outPin {PinBase} -- output pin on graphInputs node
        """

        # add companion pin for graphInputs node's output pin
        subgraphInputPin = self.createInputPin(outPin.name,
                                               outPin.dataType,
                                               outPin.defaultValue(),
                                               outPin.call,
                                               outPin.constraint)
        subgraphInputPin.supportedDataTypes = outPin.supportedDataTypes
        subgraphInputPin.singleInit = outPin.singleInit
        subgraphInputPin.setRenamingEnabled(False)
        subgraphInputPin.setDynamic(False)
        subgraphInputPin.setType(outPin)
        self.__inputsMap[subgraphInputPin] = outPin
        pinAffects(subgraphInputPin, outPin)
        # connect

        def forceRename(name):
            subgraphInputPin.setName(name, force=True)
        outPin.nameChanged.connect(forceRename, weak=False)

        # handle inner connect/disconnect
        def onInnerConnected(other):
            if subgraphInputPin.hasConnections() and subgraphInputPin.dataType != other.dataType:
                subgraphInputPin.disconnectAll()
            subgraphInputPin._data = other.currentData()
            subgraphInputPin.setType(other)
        outPin.onPinConnected.connect(onInnerConnected, weak=False)

        # handle outer connect/disconnect
        def onSubgraphInputConnected(other):
            outPin.setType(other)
        subgraphInputPin.onPinConnected.connect(onSubgraphInputConnected, weak=False)

        # broadcast for UI wrapper class
        self.pinExposed.send(subgraphInputPin)

    def onGraphOutputPinCreated(self, inPin):
        """Reaction when pin added to graphOutputs node

        Arguments:
            inPin {PinBase} -- input pin on graphOutputs node
        """

        # add companion pin for graphOutputs node's input pin
        subgraphOutputPin = self.createOutputPin(inPin.name,
                                                 inPin.dataType,
                                                 inPin.defaultValue(),
                                                 inPin.call,
                                                 inPin.constraint)
        subgraphOutputPin.supportedDataTypes = inPin.supportedDataTypes
        subgraphOutputPin.singleInit = inPin.singleInit
        subgraphOutputPin.setRenamingEnabled(False)
        subgraphOutputPin.setDynamic(False)
        subgraphOutputPin.setType(inPin)
        self.__outputsMap[subgraphOutputPin] = inPin
        pinAffects(inPin, subgraphOutputPin)

        # connect
        def forceRename(name):
            subgraphOutputPin.setName(name, force=True)
        inPin.nameChanged.connect(forceRename, weak=False)

        # watch if something is connected to inner companion
        # and change default value
        def onInnerInpPinConnected(other):
            subgraphOutputPin._data = other.currentData()
            subgraphOutputPin.setType(other)
        inPin.onPinConnected.connect(onInnerInpPinConnected, weak=False)

        # handle outer connect/disconnect
        def onSubgraphOutputConnected(other):
            inPin.setType(other)
        subgraphOutputPin.onPinConnected.connect(onSubgraphOutputConnected, weak=False)

        # broadcast for UI wrapper class
        self.pinExposed.send(subgraphOutputPin)

    def kill(self, *args, **kwargs):
        self.rawGraph.remove()
        super(compound, self).kill(*args, **kwargs)

    def postCreate(self, jsonTemplate=None):
        super(compound, self).postCreate(jsonTemplate=jsonTemplate)

        if jsonTemplate is not None and 'graphData' in jsonTemplate:
            parentGraph = self.graph().graphManager.findGraph(jsonTemplate['owningGraphName'])
            self.rawGraph = GraphBase(self.name, self.graph().graphManager, parentGraph)
            # recreate graph contents
            jsonTemplate['graphData']['name'] = self.getName()
            self.rawGraph.populateFromJson(jsonTemplate['graphData'])

            self.syncPins()

            inputsMap = self.namePinInputsMap
            for inpJson in jsonTemplate['inputs']:
                inputsMap[inpJson['name']].uid = uuid.UUID(inpJson['uuid'])

            outputsMap = self.namePinOutputsMap
            for outJson in jsonTemplate['outputs']:
                outputsMap[outJson['name']].uid = uuid.UUID(outJson['uuid'])
        else:
            self.rawGraph = GraphBase(self.name, self.graph().graphManager, self.graph().graphManager.activeGraph())

    def addNode(self, node):
        self.rawGraph.addNode(node)

    def autoAffectPins(self):
        raise NotImplementedError("Error")

    def compute(self, *args, **kwargs):
        # put data from inner graph pins to outer compound node output companions
        for outputPin, innerPin in self.__outputsMap.items():
            outputPin.setData(innerPin.getData())
