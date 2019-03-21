from blinker import Signal
from treelib import Tree

from PyFlow.Core.Common import SingletonDecorator


@SingletonDecorator
class GraphTree:

    onGraphSwitched = Signal()

    def __init__(self, rootGraph=None):
        self.__tree = Tree()
        self.__tree.create_node(rootGraph.name, rootGraph.name, data=rootGraph)
        self.__activeGraph = rootGraph

    def addChildGraph(self, rawGraph=None):
        self.getTree().create_node(rawGraph.name, rawGraph.name, self.activeGraph().name, rawGraph)

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

    def getParentGraph(self):
        parentNodeName = self.getTree()[self.activeGraph().name].bpointer
        if parentNodeName is not None:
            return self.getTree()[parentNodeName].data
        return None

    def getRootGraph(self):
        return self.__tree[self.__tree.root].data

    def getTree(self):
        return self.__tree
