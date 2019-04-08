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
        self.rawGraph = None
        self.__inputsMap = {}  # { self.[inputPin]: innerOutPin }
        self.__outputsMap = {}  # { self.[outputPin]: innerInPin }

    def Tick(self, delta):
        self.rawGraph.Tick(delta)
        super(compound, self).Tick(delta)

    def setName(self, name):
        super(compound, self).setName(name)
        if self.rawGraph is not None:
            self.rawGraph.name = name

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

    def serialize(self):
        default = NodeBase.serialize(self)
        # default['graphData'] = self.rawGraph.serialize()
        # default['graphName'] = self.rawGraph.name
        return default

    def onGraphInputPinCreated(self, outPin):
        """Reaction when pin added to graphInputs node

        Arguments:
            outPin {PinBase} -- output pin on graphInputs node
        """

        # add companion pin for graphInputs node's output pin
        subgraphInputPin = self.addInputPin(outPin.name,
                                            outPin.dataType,
                                            outPin.defaultValue(),
                                            outPin.call,
                                            outPin.constraint)
        subgraphInputPin.supportedDataTypes = outPin.supportedDataTypes
        subgraphInputPin.singleInit = outPin.singleInit
        self.__inputsMap[subgraphInputPin] = outPin
        pinAffects(subgraphInputPin, outPin)
        # connect
        outPin.nameChanged.connect(subgraphInputPin.setName)

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
        wrapperRef = self.getWrapper()
        if wrapperRef is not None:
            # raw compound input pin created. Now call UI compound node to create UI companion
            wrapperRef().onGraphInputPinExposed(subgraphInputPin)

    def onGraphOutputPinCreated(self, inPin):
        """Reaction when pin added to graphOutputs node

        Arguments:
            inPin {PinBase} -- input pin on graphOutputs node
        """

        # add companion pin for graphOutputs node's input pin
        subgraphOutputPin = self.addOutputPin(inPin.name,
                                              inPin.dataType,
                                              inPin.defaultValue(),
                                              inPin.call,
                                              inPin.constraint)
        subgraphOutputPin.supportedDataTypes = inPin.supportedDataTypes
        subgraphOutputPin.singleInit = inPin.singleInit
        self.__outputsMap[subgraphOutputPin] = inPin
        pinAffects(inPin, subgraphOutputPin)
        # connect
        inPin.nameChanged.connect(subgraphOutputPin.setName)

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
        wrapperRef = self.getWrapper()
        if wrapperRef is not None:
            # raw compound input pin created. Now call UI compound node to create UI companion
            wrapperRef().onGraphOutputPinExposed(subgraphOutputPin)

    def addNode(self, node):
        self.rawGraph.addNode(node)

    def autoAffectPins(self):
        raise NotImplementedError("Error")

    def postCreate(self, jsonTemplate=None):
        self.rawGraph = GraphBase(self.name)
        self.graph().addCompoundToTree(self)

        # connect with pin creation events and add dynamic pins
        # tell compound node pins been created
        self.rawGraph.inputPinCreated.connect(self.onGraphInputPinCreated)
        self.rawGraph.outputPinCreated.connect(self.onGraphOutputPinCreated)

    def compute(self, *args, **kwargs):
        # put data from inner graph pins to outer compound node output companions
        for outputPin, innerPin in self.__outputsMap.items():
            outputPin.setData(innerPin.getData())
