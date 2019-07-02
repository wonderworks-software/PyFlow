from nine import str
from multipledispatch import dispatch
from blinker import Signal

from PyFlow.Core.GraphBase import GraphBase
from PyFlow.Core.Common import *
from PyFlow.Core import version

ROOT_GRAPH_NAME = str('root')


class GraphManager(object):
    """docstring for GraphManager."""
    def __init__(self):
        super(GraphManager, self).__init__()
        self.graphChanged = Signal(object)
        self._graphs = {}
        self._activeGraph = None
        self._activeGraph = GraphBase(ROOT_GRAPH_NAME, self)
        self._activeGraph.setIsRoot(True)

    def findRootGraph(self):
        roots = []
        for graph in self.getAllGraphs():
            if graph.isRoot():
                roots.append(graph)
        assert(len(roots) == 1), "Fatal! Multiple roots!"
        return roots[0]

    def selectRootGraph(self):
        self.selectGraph(self.findRootGraph())

    def serialize(self):
        rootGraph = self.findRootGraph()
        saved = rootGraph.serialize()
        saved["fileVersion"] = str(version.currentVersion())
        saved["activeGraph"] = self.activeGraph().name
        return saved

    @dispatch(str)
    def removeGraph(self, name):
        graph = self.findGraph(name)
        if graph is not None:
            graph.clear()
            self._graphs.pop(graph.uid)
            if graph.parentGraph is not None:
                if graph in graph.parentGraph.childGraphs:
                    graph.parentGraph.childGraphs.remove(graph)
            del graph

    @dispatch(object)
    def removeGraph(self, graph):
        if graph.uid in self._graphs:
            graph.clear()
            self._graphs.pop(graph.uid)
            if graph.parentGraph is not None:
                if graph in graph.parentGraph.childGraphs:
                    graph.parentGraph.childGraphs.remove(graph)
            del graph

    def deserialize(self, data):
        if "fileVersion" in data:
            fileVersion = version.Version.fromString(data["fileVersion"])
        else:
            # handle older version
            pass
        self.clear(keepRoot=False)
        self._activeGraph = GraphBase(str('root'), self)
        self._activeGraph.populateFromJson(data)
        self._activeGraph.setIsRoot(True)
        self.selectGraph(self._activeGraph)

    def clear(self, keepRoot=True, *args, **kwargs):
        self.selectGraph(ROOT_GRAPH_NAME)
        self.removeGraph(ROOT_GRAPH_NAME)
        self._graphs.clear()
        self._graphs = {}
        del self._activeGraph
        self._activeGraph = None
        if keepRoot:
            self._activeGraph = GraphBase(ROOT_GRAPH_NAME, self)
            self.selectGraph(self._activeGraph)
            self._activeGraph.setIsRoot(True)

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
    def findGraph(self, name):
        graphs = self.graphsDict
        if name in graphs:
            return graphs[name]
        return None

    def findPinByName(self, pinFullName):
        result = None
        for graph in self.getAllGraphs():
            result = graph.findPin(pinFullName)
            if result is not None:
                break
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
                allNodes.extend(list(graph.nodes.values()))
            else:
                allNodes.extend([node for node in graph.nodes.values() if node.__class__.__name__ in classNameFilters])
        return allNodes

    def getAllVariables(self):
        result = []
        for graph in self.getAllGraphs():
            result.extend(list(graph.vars.values()))
        return result

    def getUniqGraphPinName(self, graph, name):
        existingNames = []
        for node in graph.getNodes(classNameFilters=['graphInputs', 'graphOutputs']):
            existingNames.extend([pin.name for pin in node.pins])
        return getUniqNameFromList(existingNames, name)

    def getUniqPinName(self, name):
        existingNames = []
        for node in self.getAllNodes():
            existingNames.extend([pin.name for pin in node.pins])
        return getUniqNameFromList(existingNames, name)

    def getAllNames(self):
        existingNames = [g.name for g in self.getAllGraphs()]
        existingNames.extend([n.name for n in self.getAllNodes()])
        existingNames.extend([var.name for var in self.getAllVariables()])
        for node in self.getAllNodes():
            existingNames.extend([pin.name for pin in node.pins])
        return existingNames

    def getUniqName(self, name):
        existingNames = self.getAllNames()
        return getUniqNameFromList(existingNames, name)

    def getUniqGraphName(self, name):
        existingNames = [g.name for g in self.getAllGraphs()]
        return getUniqNameFromList(existingNames, name)

    def getUniqNodeName(self, name):
        existingNames = [n.name for n in self.getAllNodes()]
        if name in existingNames:
            existingNames.remove(name)
        return getUniqNameFromList(existingNames, name)

    def getUniqVariableName(self, name):
        existingNames = [var.name for var in self.getAllVariables()]
        return getUniqNameFromList(existingNames, name)

    def plot(self):
        root = self.findRootGraph()
        print("Active graph: {0}".format(str(self.activeGraph().name)), "All graphs:", [g.name for g in self._graphs.values()])
        root.plot()


@SingletonDecorator
class GraphManagerSingleton(object):
    def __init__(self):
        self.man = GraphManager()

    def get(self):
        return self.man
