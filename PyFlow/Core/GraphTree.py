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
class GraphTree(Tree):
    """Graph tree. Here is all the data
    """
    def __init__(self, rootGraph=None):
        Tree.__init__(self, tree=None, deep=False, node_class=None)
        assert(rootGraph is not None)
        # signals
        self.onGraphSwitched = Signal()

        self.__activeGraph = None
        self.createRoot(rootGraph)

    def to_dict(self, nid=None, key=None, sort=True, reverse=False, with_data=False):
        """Transform the whole tree into a dict."""

        nid = self.root if (nid is None) else nid
        ntag = self[nid].tag
        tree_dict = {ntag: {"children": []}}
        if with_data:
            tree_dict[ntag]["data"] = self[nid].data.serialize()

        if self[nid].expanded:
            queue = [self[i] for i in self[nid].fpointer]
            key = (lambda x: x) if (key is None) else key
            if sort:
                queue.sort(key=key, reverse=reverse)

            for elem in queue:
                tree_dict[ntag]["children"].append(
                    self.to_dict(elem.identifier, with_data=with_data, sort=sort, reverse=reverse))
            if len(tree_dict[ntag]["children"]) == 0:
                tree_dict = self[nid].tag if not with_data else \
                    {ntag: {"data": self[nid].data.serialize()}}
            return tree_dict

    def createRoot(self, graph):
        if self.__activeGraph is None:
            self.create_node(graph.name, graph.name, data=graph)
            self.__activeGraph = graph

    def serialize(self):
        return self.to_dict(with_data=True)

    def deserialize(self, jsonData):
        self.reset()
        from PyFlow.Core.GraphBase import GraphBase

        def giveKey(d):
            return list(d.keys())[0]

        def getGraphsDict(treeNode, out):
            for name, graph in treeNode.items():
                out[name] = graph['data']
                if 'children' in graph:
                    for child in graph['children']:
                        getGraphsDict(child, out)

        def helper(node, subtree, graphsDict):
            if 'children' in subtree[node]:
                for childStruct in subtree[node]['children']:
                    if type(childStruct) == list:
                        childStruct = tuple(childStruct)
                    if isinstance(childStruct, Hashable):
                        graph = GraphBase.deserialize(graphsDict[childStruct])
                        if childStruct in self:
                            self[childStruct].data = graph
                        else:
                            self.create_node(childStruct, childStruct, parent=node, data=graph)
                    else:
                        childNode = giveKey(childStruct)
                        graph = GraphBase.deserialize(graphsDict[childNode])
                        if childNode in self:
                            self[childNode].data = graph
                        else:
                            self.create_node(childNode, childNode, parent=node, data=graph)
                        helper(childNode, childStruct, graphsDict)

        root = giveKey(jsonData)
        graphJson = jsonData['root']['data']
        restoredRootGraph = GraphBase.deserialize(graphJson)
        self.createRoot(restoredRootGraph)
        # recursively create graphs
        # create graphs dict
        graphsDict = {}
        getGraphsDict(jsonData, graphsDict)
        helper(root, jsonData, graphsDict)
        self.switchGraph(self[self.root].data.name)

    def reset(self):
        """Like clear, but leaves root graph
        """
        rootNode = self[self.root]

        # remove all graphs contents
        for graph in self.getAllGraphs():
            graph.clear()

        for childGraphId in rootNode.fpointer:
            self.remove_node(childGraphId)

        self._activeGraph = rootNode.data

    def clear(self):
        # remove all graphs contents
        for graph in self.getAllGraphs():
            graph.clear()

        # clear internal tree dict
        self._nodes.clear()

        # clear root identifier
        self.root = None

        # clear active graph pointer
        self.__activeGraph = None

    def getUniqGraphName(self, name):
        existingGraphNames = [g.name for g in self.getAllGraphs()]
        return getUniqNameFromList(existingGraphNames, name)

    def addChildGraph(self, rawGraph=None):
        uniqName = self.getUniqGraphName(rawGraph.name)
        rawGraph.name = uniqName
        self.create_node(rawGraph.name, rawGraph.name, self.activeGraph().name, rawGraph)

    def getUniqNodeName(self, name):
        existingNodeNames = []
        for treeNode in self.all_nodes():
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
        for node in self.all_nodes():
            node.data.Tick(deltaTime)

    def switchGraph(self, newGraphName):
        if newGraphName not in self:
            return False

        old = self.activeGraph()
        new = self[newGraphName].data
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
        if activeGraphName in self:
            result = sep.join(reversed([i for i in self.rsearch(activeGraphName)]))
            return result
        return "Unknown"

    def activeGraph(self):
        return self.__activeGraph

    def getAllNodes(self):
        nodes = []
        for treeNode in self.all_nodes():
            nodes += list(treeNode.data.nodes.values())
        return nodes

    def getAllGraphs(self):
        graphs = []
        for treeNode in self.all_nodes():
            graphs.append(treeNode.data)
        return graphs

    @dispatch(object)
    def getParentGraph(self, graph):
        parentNodeName = self[graph.name].bpointer
        if parentNodeName is not None:
            return self[parentNodeName].data
        return None

    @dispatch()
    def getParentGraph(self):
        parentNodeName = self[self.activeGraph().name].bpointer
        if parentNodeName is not None:
            return self[parentNodeName].data
        return None

    def getRootGraph(self):
        return self[self.root].data
