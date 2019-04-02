import os
import json
import weakref

from PyFlow.Core import NodeBase
from PyFlow.Core import GraphBase
from PyFlow.Core.GraphTree import GraphTree
from PyFlow.Core.Common import *


class subgraph(NodeBase):
    """this node encapsulates a graph, like compound in xsi

    pins can be edited only from inside the subgraph
    """
    def __init__(self, name):
        super(subgraph, self).__init__(name)
        self.rawGraph = None
        self.__inputsMap = {}  # { self.[inputPin]: innerOutPin }
        self.__outputsMap = {}  # { self.[outputPin]: innerInPin }

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

        wrapperRef = self.getWrapper()
        if wrapperRef is not None:
            # raw subgraph input pin created. Now call UI subgraph node to create UI companion
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

        wrapperRef = self.getWrapper()
        if wrapperRef is not None:
            # raw subgraph input pin created. Now call UI subgraph node to create UI companion
            wrapperRef().onGraphOutputPinExposed(subgraphOutputPin)

    def autoAffectPins(self):
        raise NotImplementedError("Error")

    def postCreate(self, jsonTemplate=None):
        self.rawGraph = GraphBase(self.name)
        GraphTree().addChildGraph(self.rawGraph)

        # connect with pin creation events and add dynamic pins
        # tell subgraph node pins been created
        self.rawGraph.inputPinCreated.connect(self.onGraphInputPinCreated)
        self.rawGraph.outputPinCreated.connect(self.onGraphOutputPinCreated)

    def compute(self, *args, **kwargs):
        # get data from subgraph node input pins and put it to inner companions
        # for inputPin, innerOutPin in self.__inputsMap.items():
        #     innerOutPin.setData(inputPin.getData())

        # put data from inner graph pins to outer subgraph node output companions
        for outputPin, innerPin in self.__outputsMap.items():
            outputPin.setData(innerPin.getData())
