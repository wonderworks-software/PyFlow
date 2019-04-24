import os
import json
import weakref

from PyFlow.Core import NodeBase
from PyFlow.Core import GraphBase
from PyFlow.Core.Common import *


class compound(NodeBase):
    """this node encapsulates a graph, like compound in xsi

    pins can be edited only from inside the compound
    """
    def __init__(self, name):
        super(compound, self).__init__(name)
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

    def Tick(self, delta):
        self.rawGraph.Tick(delta)
        super(compound, self).Tick(delta)

        # look for graph nodes pins was added
        # We need only create companions, deletion will be performed by signals automatically
        graphInputs = self.rawGraph.getNodes(classNameFilters=['graphInputs'])
        for graphInputNode in graphInputs:
            for outPin in graphInputNode.outputs.values():
                # create companion pin if needed
                if outPin.name not in self.namePinInputsMap:
                    self.onGraphInputPinCreated(outPin)

        graphOutputs = self.rawGraph.getNodes(classNameFilters=['graphOutputs'])
        for graphOutputNode in graphOutputs:
            for inPin in graphOutputNode.inputs.values():
                # create companion pin if needed
                if inPin.name not in self.namePinOutputsMap:
                    self.onGraphOutputPinCreated(inPin)

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
        # remove dynamically created ins outs. They will be recreated automatically when graph data populated
        default['inputs'] = []
        default['outputs'] = []

        default['graphData'] = self.rawGraph.serialize()
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
        self.__inputsMap[subgraphInputPin] = outPin
        pinAffects(subgraphInputPin, outPin)
        # connect

        def forceRename(name):
            subgraphInputPin.setName(name, force=True)
        outPin.nameChanged.connect(forceRename, weak=False)

        def onInnerKilled(*args, **kwargs):
            if subgraphInputPin in self.__inputsMap:
                self.__inputsMap.pop(subgraphInputPin)
            subgraphInputPin.kill()
        outPin.killed.connect(onInnerKilled, weak=False)

        # handle inner connect/disconnect
        def onInnerConnected(other):
            if subgraphInputPin.hasConnections() and subgraphInputPin.dataType != other.dataType:
                subgraphInputPin.disconnectAll()
            subgraphInputPin._data = other.currentData()
            subgraphInputPin.setType(other)
            if other.dataType == "ExecPin":
                subgraphInputPin.call = other.call
        outPin.onPinConnected.connect(onInnerConnected, weak=False)

        # handle outer connect/disconnect
        def onSubgraphInputConnected(other):
            outPin.setType(other)
        subgraphInputPin.onPinConnected.connect(onSubgraphInputConnected, weak=False)

        # TODO: rewrite with signal
        wrapper = self.getWrapper()
        if wrapper is not None:
            # raw compound input pin created. Now call UI compound node to create UI companion
            wrapper.onGraphInputPinExposed(subgraphInputPin)

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
        self.__outputsMap[subgraphOutputPin] = inPin
        pinAffects(inPin, subgraphOutputPin)

        # connect
        def forceRename(name):
            subgraphOutputPin.setName(name, force=True)
        inPin.nameChanged.connect(forceRename, weak=False)

        def onInnerInpPinKilled(*args, **kwargs):
            self.__outputsMap.pop(subgraphOutputPin)
            subgraphOutputPin.kill()
        inPin.killed.connect(onInnerInpPinKilled, weak=False)

        # watch if something is connected to inner companion
        # and change default value
        def onInnerInpPinConnected(other):
            subgraphOutputPin._data = other.currentData()
            subgraphOutputPin.setType(other)
            if other.dataType == "ExecPin":
                other.call = subgraphOutputPin.call
        inPin.onPinConnected.connect(onInnerInpPinConnected, weak=False)

        # handle outer connect/disconnect
        def onSubgraphOutputConnected(other):
            inPin.setType(other)
        subgraphOutputPin.onPinConnected.connect(onSubgraphOutputConnected, weak=False)

        # TODO: rewrite with signal
        wrapper = self.getWrapper()
        if wrapper is not None:
            # raw compound input pin created. Now call UI compound node to create UI companion
            wrapper.onGraphOutputPinExposed(subgraphOutputPin)

    def kill(self, *args, **kwargs):
        self.rawGraph.remove()
        super(compound, self).kill(*args, **kwargs)

    def postCreate(self, jsonTemplate=None):
        super(compound, self).postCreate(jsonTemplate=jsonTemplate)
        self.rawGraph = GraphBase(self.name, self.graph().graphManager)

        if jsonTemplate is not None and 'graphData' in jsonTemplate:
            # recreate graph contents
            jsonTemplate['graphData']['name'] = self.getName()
            self.rawGraph.populateFromJson(jsonTemplate['graphData'])

    def addNode(self, node):
        self.rawGraph.addNode(node)

    def autoAffectPins(self):
        raise NotImplementedError("Error")

    def compute(self, *args, **kwargs):
        # put data from inner graph pins to outer compound node output companions
        for outputPin, innerPin in self.__outputsMap.items():
            outputPin.setData(innerPin.getData())
