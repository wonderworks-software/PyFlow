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

    def serialize(self):
        return self.graphsDict['root'].serialize()

    def deserialize(self, data):
        self.clear(keepRoot=False)
        # rootGraphJson = data[list(data.keys())[0]]
        self._activeGraph = GraphBase.deserialize(data, self)

    def clear(self, *args, keepRoot=True, **kwargs):
        for graph in self._graphs.values():
            graph.clear()
        self._graphs.clear()
        if keepRoot:
            newGraph = GraphBase('root', self)
            self.selectGraph(newGraph)
        else:
            del self._activeGraph
            self._activeGraph = None

    def Tick(self, deltaTime):
        for graph in self._graphs.values():
            graph.Tick(deltaTime)

    def findVariableRefs(self, variable):
        result = []
        for node in self.getAllNodes(classNameFilters=['getVar', 'setVar']):
            if node.variableUid() == variable.uid:
                result.append(node)
        return result

    @dispatch(str)
    def findNode(self, name):
        """Finds a node across all graphs
        """
        result = None
        for graph in self.getAllGraphs():
            result = graph.findNode(name)
            if result is not None:
                break
        return result

    @dispatch(uuid.UUID)
    def findNode(self, uid):
        """Finds a node across all graphs
        """
        for graph in self.getAllGraphs():
            if uid in graph.nodes:
                return graph.nodes[uid]
        return None

    @dispatch(uuid.UUID)
    def findVariable(self, uuid):
        """Finds a variable across all graphs
        """
        result = None
        for graph in self._graphs.values():
            if uuid in graph.vars:
                result = graph.vars[uuid]
                break
        return result

    @dispatch(str)
    def findVariable(self, name):
        """Finds a variable across all graphs
        """
        for graph in self._graphs.values():
            for var in graph.vars.values():
                if var.name == name:
                    return var
        return None

    def location(self):
        location = [self.activeGraph().name]
        parent = self.activeGraph().parentGraph
        while parent is not None:
            location.insert(0, parent.name)
            parent = parent.parentGraph
        return location

    @property
    def graphsDict(self):
        result = {}
        for graph in self.getAllGraphs():
            result[graph.name] = graph
        return result

    def add(self, graph):
        if graph.name in self._graphs:
            graph.name = self.getUniqGraphName(graph.name)
        self._graphs[graph.uid] = graph

    def activeGraph(self):
        return self._activeGraph

    @dispatch(str)
    def selectGraph(self, name):
        graphs = self.graphsDict
        if name in graphs:
            if name != self.activeGraph().name:
                oldGraph = self.activeGraph()
                newGraph = graphs[name]
                self._activeGraph = newGraph
                self.graphChanged.send(self.activeGraph())

    @dispatch(object)
    def selectGraph(self, graph):
        for newGraph in self.getAllGraphs():
            if newGraph.name == graph.name:
                if newGraph.name != self.activeGraph().name:
                    oldGraph = self.activeGraph()
                    self._activeGraph = newGraph
                    self.graphChanged.send(self.activeGraph())
                    break

    def getAllGraphs(self):
        return [g for g in self._graphs.values()]

    def getAllNodes(self, classNameFilters=[]):
        allNodes = []
        for graph in self.getAllGraphs():
            if len(classNameFilters) == 0:
                allNodes += graph.nodes.values()
            else:
                allNodes += [node for node in graph.nodes.values() if node.__class__.__name__ in classNameFilters]
        return allNodes

    def getAllVariables(self):
        result = []
        for graph in self.getAllGraphs():
            result += list(graph.vars.values())
        return result

    def getUniqName(self, name):
        existingNames = [g.name for g in self.getAllGraphs()]
        existingNames.extend([n.name for n in self.getAllNodes()])
        existingNames.extend([var.name for var in self.getAllVariables()])
        return getUniqNameFromList(existingNames, name)

    def getUniqGraphName(self, name):
        existingNames = [g.name for g in self.getAllGraphs()]
        return getUniqNameFromList(existingNames, name)

    def getUniqNodeName(self, name):
        existingNames = [n.name for n in self.getAllNodes()]
        return getUniqNameFromList(existingNames, name)

    def getUniqVariableName(self, name):
        existingNames = [var.name for var in self.getAllVariables()]
        return getUniqNameFromList(existingNames, name)

    def plot(self):
        self.activeGraph().plot()
