import os
import json

from PyFlow.Core import NodeBase
from PyFlow.Core import GraphBase
from PyFlow.Core.GraphTree import GraphTree
from PyFlow.Core.Common import *


class subgraph(NodeBase):
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

    def postCreate(self, jsonTemplate=None):
        self.rawGraph = GraphBase(self.name)
        GraphTree().addChildGraph(self.rawGraph)
