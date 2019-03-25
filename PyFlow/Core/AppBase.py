from PyFlow.Core.GraphTree import GraphTree
from PyFlow.Core.GraphBase import GraphBase


class AppBase(object):
    """docstring for AppBase."""
    def __init__(self, *args, **kwds):
        super(AppBase, self).__init__()
        # initialize GraphTree singleton
        GraphTree(GraphBase('root'))

    def Tick(self, deltaTime):
        GraphTree().Tick(deltaTime)
