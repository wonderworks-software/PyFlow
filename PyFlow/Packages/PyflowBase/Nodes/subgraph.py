import os
import json

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
        self.__inputsMap = {}  # { self.[inputPin].uid: innerPinUid }
        self.__outputsMap = {}  # { self.[outputPin].uid: innerPinUid }

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
                                            outPin.constraint,
                                            outPin.supportedDataTypes())
        self.__inputsMap[subgraphInputPin.uid] = outPin.uid
        # connect
        outPin.nameChanged.connect(subgraphInputPin.setName)
        outPin.killed.connect(subgraphInputPin.kill)

    def onGraphInputPinDeleted(self, inPin):
        # remove companion pin for inner graphInputs node pin
        print("onGraphInputPinDeleted", inPin.getName())

    def onGraphOutputPinCreated(self, inPin):
        # add companion pin for graphOutputs node's input pin
        subgraphOutputPin = self.addOutputPin(inPin.name,
                                              inPin.dataType,
                                              inPin.defaultValue(),
                                              inPin.call,
                                              inPin.constraint,
                                              inPin.supportedDataTypes())
        self.__outputsMap[subgraphOutputPin.uid] = inPin.uid
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
