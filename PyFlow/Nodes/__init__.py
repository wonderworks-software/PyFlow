"""@package Nodes

Class based nodes.
"""
import os
from .. import FunctionLibraries
from inspect import getmembers
from inspect import isfunction


_instances = {}


# append from Nodes
for n in os.listdir(os.path.dirname(__file__)):
    if n.endswith(".py") and "__init__" not in n:
        nodeName = n.split(".")[0]
        try:
            exec("from {0} import *".format(nodeName))
            exec("node_class = {0}".format(nodeName))
            _instances[nodeName] = node_class
        except Exception as e:
            # do not load node if errors or unknown modules
            print(e, nodeName)
            pass


def getNode(name):
    if name in _instances:
        return _instances[name]
    return None


def getNodeNames():
    return _instances.keys()
