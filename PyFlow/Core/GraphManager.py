from nine import str
from multipledispatch import dispatch
from blinker import Signal

from PyFlow.Core.GraphBase import GraphBase
from PyFlow.Core.Common import *
from PyFlow.Core import version

ROOT_GRAPH_NAME = str('root')


class GraphManager(object):
    """Data structure that holds graph tree

    This class switches active graph. Can insert or remove graphs to tree,
    can search nodes and variables across all graphs. Also this class responsible
    for giving unique names.
    """
    def __init__(self):
        super(GraphManager, self).__init__()
        self.graphChanged = Signal(object)
        self._graphs = {}
        self._activeGraph = None
        self._activeGraph = GraphBase(ROOT_GRAPH_NAME, self)
        self._activeGraph.setIsRoot(True)

    def findRootGraph(self):
        """Returns top level root graph

        :rtype: :class:`~PyFlow.Core.GraphBase.GraphBase`
        """
        roots = []
        for graph in self.getAllGraphs():
            if graph.isRoot():
                roots.append(graph)
        assert(len(roots) == 1), "Fatal! Multiple roots!"
        return roots[0]

    def selectRootGraph(self):
        """Selects root graph
        """
        self.selectGraph(self.findRootGraph())

    def serialize(self):
        """Serializes itself to json.

        All child graphs will be serialized.

        :rtype: dict
        """
        rootGraph = self.findRootGraph()
        saved = rootGraph.serialize()
        saved["fileVersion"] = str(version.currentVersion())
        saved["activeGraph"] = self.activeGraph().name
        return saved

    def removeGraphByName(self, name):
        """Removes graph by :attr:`~PyFlow.Core.GraphBase.GraphBase.name`

        :param name: name of graph to be removed
        :type name: str
        """
        graph = self.findGraph(name)
        if graph is not None:
            graph.clear()
            self._graphs.pop(graph.uid)
            if graph.parentGraph is not None:
                if graph in graph.parentGraph.childGraphs:
                    graph.parentGraph.childGraphs.remove(graph)
            del graph

    def removeGraph(self, graph):
        """Removes supplied graph

        :param graph: Graph to be removed
        :type graph: :class:`~PyFlow.Core.GraphBase.GraphBase`
        """
        if graph.uid in self._graphs:
            graph.clear()
            self._graphs.pop(graph.uid)
            if graph.parentGraph is not None:
                if graph in graph.parentGraph.childGraphs:
                    graph.parentGraph.childGraphs.remove(graph)
            del graph

    def deserialize(self, data):
        """Populates itself from serialized data

        :param data: Serialized data
        :type data: dict
        """
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
        """Wipes everything.

        :param keepRoot: Whether to remove root graph or not
        :type keepRoot: bool
        """
        self.selectGraphByName(ROOT_GRAPH_NAME)
        self.removeGraphByName(ROOT_GRAPH_NAME)
        self._graphs.clear()
        self._graphs = {}
        del self._activeGraph
        self._activeGraph = None
        if keepRoot:
            self._activeGraph = GraphBase(ROOT_GRAPH_NAME, self)
            self.selectGraph(self._activeGraph)
            self._activeGraph.setIsRoot(True)

    def Tick(self, deltaTime):
        """Periodically calls :meth:`~PyFlow.Core.GraphBase.GraphBase.Tick` on all graphs

        :param deltaTime: Elapsed time from last call
        :type deltaTime: float
        """
        for graph in self._graphs.values():
            graph.Tick(deltaTime)

    def findVariableRefs(self, variable):
        """Returns a list of variable accessors spawned across all graphs

        :param variable: Variable to search accessors for
        :type variable: :class:`~PyFlow.Core.Variable.Variable`
        :rtype: list(:class:`~PyFlow.Core.NodeBase.NodeBase`)
        """
        result = []
        for node in self.getAllNodes(classNameFilters=['getVar', 'setVar']):
            if node.variableUid() == variable.uid:
                result.append(node)
        return result

    def findGraph(self, name):
        """Tries to find graph by :attr:`~PyFlow.Core.GraphBase.GraphBase.name`

        :param name: Name of target graph
        :type name: str
        :rtype: :class:`~PyFlow.Core.GraphBase.GraphBase` or None
        """
        graphs = self.getGraphsDict()
        if name in graphs:
            return graphs[name]
        return None

    def findPinByName(self, pinFullName):
        """Tries to find pin by name across all graphs

        :param pinFullName: Full name of pin including node namespace
        :type pinFullName: str
        :rtype: :class:`~PyFlow.Core.PinBase.PinBase` or None
        """
        result = None
        for graph in self.getAllGraphs():
            result = graph.findPin(pinFullName)
            if result is not None:
                break
        return result

    def findNode(self, name):
        """Finds a node across all graphs

        :param name: Node name to search by
        :type name: str
        :rtype: :class:`~PyFlow.Core.NodeBase.NodeBase`
        """
        result = None
        for graph in self.getAllGraphs():
            result = graph.findNode(name)
            if result is not None:
                break
        return result

    def findVariableByUid(self, uuid):
        """Finds a variable across all graphs

        :param uuid: Variable unique identifier
        :type uuid: :class:`~uuid.UUID`
        :rtype: :class:`~PyFlow.Core.Variable.Variable` or None
        """
        result = None
        for graph in self._graphs.values():
            if uuid in graph.getVars():
                result = graph.getVars()[uuid]
                break
        return result

    def findVariableByName(self, name):
        """Finds a variable across all graphs

        :param name: Variable name
        :type name: str
        :rtype: :class:`~PyFlow.Core.Variable.Variable` or None
        """
        for graph in self._graphs.values():
            for var in graph.getVars().values():
                if var.name == name:
                    return var
        return None

    def location(self):
        """Returns location of active graph

        .. seealso ::

            :meth:`PyFlow.Core.GraphBase.GraphBase.location`
        """
        return self.activeGraph().location()

    def getGraphsDict(self):
        """Creates and returns dictionary where graph name associated with graph

        :rtype: dict(str, :class:`~PyFlow.Core.GraphBase.GraphBase`)
        """
        result = {}
        for graph in self.getAllGraphs():
            result[graph.name] = graph
        return result

    def add(self, graph):
        """Adds graph to storage and ensures that graph name is unique

        :param graph: Graph to add
        :type graph: :class:`~PyFlow.Core.GraphBase.GraphBase`
        """
        graph.name = self.getUniqGraphName(graph.name)
        self._graphs[graph.uid] = graph

    def activeGraph(self):
        """Returns active graph

        :rtype: :class:`~PyFlow.Core.GraphBase.GraphBase`
        """
        return self._activeGraph

    def selectGraphByName(self, name):
        """Sets active graph by graph name and fires event

        :param name: Name of target graph
        :type name: str
        """
        graphs = self.getGraphsDict()
        if name in graphs:
            if name != self.activeGraph().name:
                oldGraph = self.activeGraph()
                newGraph = graphs[name]
                self._activeGraph = newGraph
                self.graphChanged.send(self.activeGraph())

    def selectGraph(self, graph):
        """Sets supplied graph as active and fires event

        :param graph: Target graph
        :type graph: :class:`~PyFlow.Core.GraphBase.GraphBase`
        """
        for newGraph in self.getAllGraphs():
            if newGraph.name == graph.name:
                if newGraph.name != self.activeGraph().name:
                    oldGraph = self.activeGraph()
                    self._activeGraph = newGraph
                    self.graphChanged.send(self.activeGraph())
                    break

    def getAllGraphs(self):
        """Returns all graphs

        :rtype: list(:class:`~PyFlow.Core.GraphBase.GraphBase`)
        """
        return [g for g in self._graphs.values()]

    def getAllNodes(self, classNameFilters=[]):
        """Returns all nodes across all graphs

        :param classNameFilters: If class name filters specified, only those node classes will be considered
        :type classNameFilters: list(str)
        :rtype: list(:class:`~PyFlow.Core.NodeBase.NodeBase`)
        """
        allNodes = []
        for graph in self.getAllGraphs():
            if len(classNameFilters) == 0:
                allNodes.extend(list(graph.getNodes().values()))
            else:
                allNodes.extend([node for node in graph.getNodes().values() if node.__class__.__name__ in classNameFilters])
        return allNodes

    def getAllVariables(self):
        """Returns a list of all variables

        :rtype: list(:class:`~PyFlow.Core.Variable.Variable`)
        """
        result = []
        for graph in self.getAllGraphs():
            result.extend(list(graph.getVars().values()))
        return result

    def getUniqGraphPinName(self, graph, name):
        """Returns unique pin name for graph

        Used by compound node and graphInputs graphOutputs nodes.
        To make all exposed to compound pins names unique.

        :param graph: Target graph
        :type graph: :class:`~PyFlow.Core.GraphBase.GraphBase`
        :param name: Target pin name
        :type name: str

        :rtype: str
        """
        existingNames = []
        for node in graph.getNodesList(classNameFilters=['graphInputs', 'graphOutputs']):
            existingNames.extend([pin.name for pin in node.pins])
        return getUniqNameFromList(existingNames, name)

    def getAllNames(self):
        """Returns list of all registered names

        Includes graphs, nodes, pins, variables names

        :rtype: list(str)
        """
        existingNames = [g.name for g in self.getAllGraphs()]
        existingNames.extend([n.name for n in self.getAllNodes()])
        existingNames.extend([var.name for var in self.getAllVariables()])
        for node in self.getAllNodes():
            existingNames.extend([pin.name for pin in node.pins])
        return existingNames

    def getUniqName(self, name):
        """Returns unique name

        :param name: Source name
        :type name: str
        :rtype: str
        """
        existingNames = self.getAllNames()
        return getUniqNameFromList(existingNames, name)

    def getUniqGraphName(self, name):
        """Returns unique graph name

        :param name: Source name
        :type name: str
        :rtype: str
        """
        existingNames = [g.name for g in self.getAllGraphs()]
        return getUniqNameFromList(existingNames, name)

    def getUniqNodeName(self, name):
        """Returns unique node name

        :param name: Source name
        :type name: str
        :rtype: str
        """
        existingNames = [n.name for n in self.getAllNodes()]
        if name in existingNames:
            existingNames.remove(name)
        return getUniqNameFromList(existingNames, name)

    def getUniqVariableName(self, name):
        """Returns unique variable name

        :param name: Source name
        :type name: str
        :rtype: str
        """
        existingNames = [var.name for var in self.getAllVariables()]
        return getUniqNameFromList(existingNames, name)

    def plot(self):
        """Prints all data to console. May be useful for debugging
        """
        root = self.findRootGraph()
        print("Active graph: {0}".format(str(self.activeGraph().name)), "All graphs:", [g.name for g in self._graphs.values()])
        root.plot()


@SingletonDecorator
class GraphManagerSingleton(object):
    """Singleton class that holds graph manager instance inside. Used by app as main graph manager
    """
    def __init__(self):
        self.man = GraphManager()

    def get(self):
        """Returns graph manager instance

        :rtype: :class:`~PyFlow.Core.GraphManager.GraphManager`
        """
        return self.man
