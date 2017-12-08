import os
from inspect import getmembers
from inspect import isfunction

_libs = {}
_foos = {}

# append from FunctionLibraries
for lib in os.listdir(os.path.dirname(__file__)):
    if lib.endswith(".py") and "__init__" not in lib:
        libName = lib.split(".")[0]
        exec('from {0} import {0}'.format(libName))
        exec('lib_class = {0}'.format(libName))
        foos = getmembers(lib_class, isfunction)
        _libs[libName] = foos
        for f in _libs[libName]:
            _foos[f[0]] = f[1]


def getLib(libName):
    if libName in _libs:
        return _libs[libName]
    return None


def libs():
    return _libs.keys()


def findFunctionByName(name):
    if name in _foos:
        return _foos[name]
    return None


def shoutDown():
    _foos.clear()
    _libs.clear()
