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
        self.__inputsMap[subgraphInputPin] = outPin
        pinAffects(subgraphInputPin, outPin)
        # connect
        outPin.nameChanged.connect(subgraphInputPin.setName)
        outPin.killed.connect(subgraphInputPin.kill)

    def onGraphInputPinDeleted(self, inPin):
        # remove companion pin for inner graphInputs node pin
        print("onGraphInputPinDeleted", inPin.getName())

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
        self.__outputsMap[subgraphOutputPin] = inPin
        pinAffects(inPin, subgraphOutputPin)
        # connect
        inPin.nameChanged.connect(subgraphOutputPin.setName)
        inPin.killed.connect(subgraphOutputPin.kill)

    def onGraphOutputPinDeleted(self, outPin):
        # remove companion pin for inner graphOutputs node pin
        print("onGraphOutputPinDeleted", outPin.getName())

    def postCreate(self, jsonTemplate=None):
        self.rawGraph = GraphBase(self.name)
        GraphTree().addChildGraph(self.rawGraph)

        # connect with pin creation events and add dynamic pins
        self.rawGraph.onInputPinCreated.connect(self.onGraphInputPinCreated)
        self.rawGraph.onInputPinDeleted.connect(self.onGraphInputPinDeleted)
        self.rawGraph.onOutputPinCreated.connect(self.onGraphOutputPinCreated)
        self.rawGraph.onOutputPinDeleted.connect(self.onGraphOutputPinDeleted)

    def compute(self):
        # get data from subgraph node input pins and put it to inner companions
        # for inputPin, innerOutPin in self.__inputsMap.items():
        #     innerOutPin.setData(inputPin.getData())

        # put data from inner graph pins to outer subgraph node output companions
        for outputPin, innerPin in self.__outputsMap.items():
            outputPin.setData(innerPin.getData())
