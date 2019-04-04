import json

from multipledispatch import dispatch
from blinker import Signal
from treelib import Tree
try:
    from collections.abc import Hashable
except:
    from collections import Hashable

from PyFlow.Core.Common import SingletonDecorator
from PyFlow.Core.Common import getUniqNameFromList


@SingletonDecorator
class GraphTree:
    """Graph tree. Here is all the data
    """
    def __init__(self, rootGraph=None):
        assert(rootGraph is not None)
        # signals
        self.onGraphSwitched = Signal()

        self.__tree = Tree()
        self.__activeGraph = None
        if self.setRootGraph(rootGraph):
            self.switchGraph(rootGraph.name)
        else:
            assert(False), "Failed to set root graph!"

    def serialize(self):
        # save hierarchy
        result = {
            'tree': self.getTree().to_json(),
            'graphs': {}
        }

        tree = self.getTree()
        for nodeId in tree.nodes:
            node = tree.nodes[nodeId]
            result['graphs'][node.identifier] = node.data.serialize()

        return result

    def deserialize(self, jsonData):
        from PyFlow.Core.GraphBase import GraphBase

        # restore hierarchy
        tree = deserializeTree(jsonData['tree'])
        # recreate graphs and apply them as data to nodes
        # TODO: check graphs created from root, to children
        for graphIdentifier in jsonData['graphs']:
            graphJson = jsonData['graphs'][graphIdentifier]
            restoredGraph = GraphBase.deserialize(graphJson)
            tree[graphIdentifier].data = restoredGraph

        # apply root graph to tree
        self.setRootGraph(tree[tree.root].data)

    def clear(self):
        t = self.getTree()
        t._nodes.clear()
        t.root = None
        self.__activeGraph.clear()
        self.__activeGraph = None

    def getUniqGraphName(self, name):
        existingGraphNames = [g.name for g in self.getAllGraphs()]
        return getUniqNameFromList(existingGraphNames, name)

    def addChildGraph(self, rawGraph=None):
        uniqName = self.getUniqGraphName(rawGraph.name)
        rawGraph.name = uniqName
        self.getTree().create_node(rawGraph.name, rawGraph.name, self.activeGraph().name, rawGraph)

    def getUniqNodeName(self, name):
        existingNodeNames = []
        for treeNode in self.getTree().all_nodes():
            for rawNode in treeNode.data.getNodes():
                existingNodeNames.append(rawNode.getName())
        return getUniqNameFromList(existingNodeNames, name)

    def plot(self):
        self.activeGraph().plot()

    def getVarsList(self, graph=None):
        """Returns this graph variables as well as all parent graph's ones

        returns:
            [varinstance1, varinstance2, ...]
        """
        if graph is None:
            graph = self.activeGraph()
        result = []
        result += list(graph.vars.values())
        parent = self.getParentGraph(graph)
        while parent is not None:
            result += list(parent.vars.values())
            parent = self.getParentGraph(parent)
        return result

    def getVarsDict(self, graph=None):
        """Returns this graph variables as well as all parent graph's ones

        returns:
            {'graphName': { varUid: varInstance1 }, ...}
        """
        if graph is None:
            graph = self.activeGraph()
        result = {}
        result[graph.name] = graph.vars
        parent = self.getParentGraph(graph)
        while parent is not None:
            result[parent.name] = parent.vars
            parent = self.getParentGraph(parent)
        return result

    def Tick(self, deltaTime):
        for node in self.getTree().all_nodes():
            node.data.Tick(deltaTime)

    def switchGraph(self, newGraphName):
        if newGraphName not in self.getTree():
            return False

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

    def setRootGraph(self, graph):
        t = self.getTree()
        if t.size() == 0:
            t.create_node(graph.name, graph.name, data=graph)
            self.__activeGraph = graph
            return True
        return False

    def getRootGraph(self):
        return self.__tree[self.__tree.root].data

    def getTree(self):
        return self.__tree


def deserializeTree(jsonTree):
    def giveKey(d):
        return list(d.keys())[0]

    def helper(node, subtree):
        for childStruct in subtree[node]['children']:
            if type(childStruct) == list:
                childStruct = tuple(childStruct)
            if isinstance(childStruct, Hashable):
                newTree.create_node(childStruct, childStruct, parent=node)
            else:
                childNode = giveKey(childStruct)
                newTree.create_node(childNode, childNode, parent=node)
                helper(childNode, childStruct)
    newTree = Tree()
    jsonTree = json.loads(jsonTree)

    # handle if root only
    if isinstance(jsonTree, str):
        root = jsonTree
        newTree.create_node(root, root)
        return newTree

    if isinstance(jsonTree, dict):
        root = giveKey(jsonTree)
        newTree.create_node(root, root)
        helper(root, jsonTree)
    return newTree
