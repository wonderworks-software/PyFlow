from PyFlow.Core.Common import *
from PyFlow.Core.GraphManager import GraphManagerSingleton


@SingletonDecorator
class PathsRegistry(object):
    """Holds paths to nodes and pins. Can rebuild paths and return entities by paths."""
    def __init__(self):
        self._data = {}

    def rebuild(self):
        man = GraphManagerSingleton().get()
        allNodes = man.getAllNodes()
        self._data.clear()
        for node in allNodes:
            self._data[node.path()] = node
            for pin in node.pins:
                self._data[pin.path()] = pin

    def getAllPaths(self):
        return list(self._data)

    def contains(self, path):
        return path in self._data

    # def resolvePath(self, base, path):
    #     temp = os.path.normpath(os.path.join(base, path))
    #     res = "/".join(temp.split(os.sep))

    def getEntity(self, path):
        if self.contains(path):
            return self._data[path]
        return None
