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

    def findVariableRefs(self, variable):
        result = []
        for node in self.getAllNodes(classNameFilters=['getVar', 'setVar']):
            if node.variableUid() == variable.uid:
                result.append(node)
        return result

    def location(self):
        location = [self.activeGraph().name]
        parent = self.activeGraph().parentGraph
        while parent is not None:
            location.insert(0, parent.name)
            parent = parent.parentGraph
        return location

    def add(self, graph):
        if graph.name in self._graphs:
            graph.name = self.getUniqGraphName(graph.name)
        # TODO: Use uuid as key. In this case no need to bother actualizing self.__graphs keys when graph renamed
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

    def getAllNodes(self, classNameFilters=[]):
        allNodes = []
        for graph in self._graphs.values():
            if len(classNameFilters) == 0:
                allNodes += graph.nodes.values()
            else:
                allNodes += [node for node in graph.nodes.values() if node.__class__.__name__ in classNameFilters]
        return allNodes

    def getAllVariables(self):
        result = []
        for graph in self._graphs.values():
            result += list(graph.vars.values())
        return result

    def getUniqName(self, name):
        existingNames = [g.name for g in self._graphs.values()]
        existingNames.extend([n.name for n in self.getAllNodes()])
        existingNames.extend([var.name for var in self.getAllVariables()])
        return getUniqNameFromList(existingNames, name)

    def getUniqGraphName(self, name):
        existingNames = [g.name for g in self._graphs.values()]
        return getUniqNameFromList(existingNames, name)

    def getUniqNodeName(self, name):
        existingNames = [n.name for n in self.getAllNodes()]
        return getUniqNameFromList(existingNames, name)

    def getUniqVariableName(self, name):
        existingNames = [var.name for var in self.getAllVariables()]
        return getUniqNameFromList(existingNames, name)

    def plot(self):
        self.activeGraph().plot()
