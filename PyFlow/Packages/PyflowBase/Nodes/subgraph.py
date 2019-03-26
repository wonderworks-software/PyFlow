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

    def onGraphInputPinCreated(self, inPin):
        # add companion pin for inner graphInputs node pin
        pass

    def onGraphInputPinDeleted(self, inPin):
        # remove companion pin for inner graphInputs node pin
        pass

    def onGraphOutputPinCreated(self, outPin):
        # add companion pin for inner graphOutputs node pin
        pass

    def onGraphOutputPinDeleted(self, outPin):
        # remove companion pin for inner graphOutputs node pin
        pass

    def postCreate(self, jsonTemplate=None):
        self.rawGraph = GraphBase(self.name)
        GraphTree().addChildGraph(self.rawGraph)

        # connect with pin creation events and add dynamic pins
        self.rawGraph.onInputPinCreated.connect(self.onGraphInputPinCreated)
        self.rawGraph.onInputPinDeleted.connect(self.onGraphInputPinDeleted)
        self.rawGraph.onOutputPinCreated.connect(self.onGraphOutputPinCreated)
        self.rawGraph.onOutputPinDeleted.connect(self.onGraphOutputPinDeleted)
