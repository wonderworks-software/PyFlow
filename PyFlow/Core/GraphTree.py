from multipledispatch import dispatch
from blinker import Signal
from treelib import Tree

from PyFlow.Core.Common import SingletonDecorator
from PyFlow.Core.Common import getUniqNameFromList


@SingletonDecorator
class GraphTree:
    """Graph tree. Here is all the data
    """

    onGraphSwitched = Signal()

    def __init__(self, rootGraph=None):
        self.__tree = Tree()
        self.__tree.create_node(rootGraph.name, rootGraph.name, data=rootGraph)
        self.__activeGraph = rootGraph

    def addChildGraph(self, rawGraph=None):
        self.getTree().create_node(rawGraph.name, rawGraph.name, self.activeGraph().name, rawGraph)

    def getUniqNodeName(self, name):
        existingNodeNames = []
        for treeNode in self.getTree().all_nodes():
            for rawNode in treeNode.data.getNodes():
                existingNodeNames.append(rawNode.getName())
        return getUniqNameFromList(existingNodeNames, name)

    def getVars(self, graph=None):
        """Returns this graph variables as well as all parent graph's ones

        returns:
            {'graphName': varsDict, ...}
        """
        if graph is None:
            graph = self.activeGraph()
        result = dict()
        result[graph.name] = graph.vars
        parent = self.getParentGraph(graph)
        while parent is not None:
            # TODO: check for unique graph names
            result[parent.name] = parent.vars
            parent = self.getParentGraph(parent)
        return result

    def Tick(self, deltaTime):
        for node in self.getTree().all_nodes():
            node.data.Tick(deltaTime)

    def switchGraph(self, newGraphName):
        old = self.activeGraph()
        new = self.getTree()[newGraphName].data
        if old == new:
            return False
        self.__activeGraph = new
        self.onGraphSwitched.send(old=old, new=new)
        return True

    def goUp(self):
        parentGraph = self.getParentGraph()
        if parentGraph is not None:
            self.switchGraph(parentGraph)

    def location(self, sep='|'):
        activeGraphName = self.activeGraph().name
        if activeGraphName in self.__tree:
            result = sep.join(reversed([i for i in self.__tree.rsearch(activeGraphName)]))
            return result
        return "Unknown"

    def show(self):
        self.__tree.show()

    def activeGraph(self):
        return self.__activeGraph

    def getAllNodes(self):
        nodes = []
        for treeNode in self.getTree().all_nodes():
            nodes += list(treeNode.data.nodes.values())
        return nodes

    def getAllGraphs(self):
        graphs = []
        for treeNode in self.getTree().all_nodes():
            graphs.append(treeNode.data)
        return graphs

    @dispatch(object)
    def getParentGraph(self, graph):
        parentNodeName = self.getTree()[graph.name].bpointer
        if parentNodeName is not None:
            return self.getTree()[parentNodeName].data
        return None

    @dispatch()
    def getParentGraph(self):
        parentNodeName = self.getTree()[self.activeGraph().name].bpointer
        if parentNodeName is not None:
            return self.getTree()[parentNodeName].data
        return None

    def getRootGraph(self):
        return self.__tree[self.__tree.root].data

    def getTree(self):
        return self.__tree
