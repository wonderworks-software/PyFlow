import os
import FunctionLibraries
from inspect import getmembers
from inspect import isfunction


_instances = {}


# append from Nodes
for n in os.listdir(os.path.dirname(__file__)):
    if n.endswith(".py") and "__init__" not in n:
        nodeName = n.split(".")[0]
        exec("from {0} import *".format(nodeName))
        exec("node_class = {0}".format(nodeName))
        _instances[nodeName] = node_class
from Reroute import RerouteMover
_instances[RerouteMover.__name__] = RerouteMover


def getNode(name):
    if name in _instances:
        return _instances[name]
    return None
