from multipledispatch import dispatch
from blinker import Signal

from PyFlow.Core.GraphBase import GraphBase
from PyFlow.Core.Common import *


class GraphManager(object):
    """docstring for GraphManager."""
    def __init__(self):
        super(GraphManager, self).__init__()
        self.graphChanged = Signal(object)
        self._graphs = {}
        self._activeGraph = None
        self._activeGraph = GraphBase('root', self)

    def Tick(self, deltaTime):
        for graph in self._graphs.values():
            graph.Tick(deltaTime)

    def location(self):
        location = [self.activeGraph().name]
        parent = self.activeGraph().parentGraph
        while parent is not None:
            location.insert(0, parent.name)
            parent = parent.parentGraph
        return location

    def add(self, graph):
        self._graphs[graph.name] = graph

    def activeGraph(self):
        return self._activeGraph

    @dispatch(str)
    def selectGraph(self, name):
        if name in self._graphs:
            if name != self.activeGraph().name:
                oldGraph = self.activeGraph()
                newGraph = self._graphs[name]
                self._activeGraph = newGraph
                self.graphChanged.send(self.activeGraph())

    @dispatch(object)
    def selectGraph(self, graph):
        for newGraph in self._graphs.values():
            if newGraph.name == graph.name:
                if newGraph.name != self.activeGraph().name:
                    oldGraph = self.activeGraph()
                    self._activeGraph = newGraph
                    self.graphChanged.send(self.activeGraph())

    def getAllNodes(self):
        allNodes = []
        for graph in self._graphs.values():
            allNodes += graph.nodes.values()
        return allNodes

    def getUniqGraphName(self, name):
        existingNames = [g.name for g in self._graphs.values()]
        return getUniqNameFromList(existingNames, name)

    def getUniqNodeName(self, name):
        existingNames = [n.name for n in self.getAllNodes()]
        return getUniqNameFromList(existingNames, name)

    def plot(self):
        self.activeGraph().plot()
