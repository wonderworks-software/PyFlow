"""@package FunctionLibraries

Set of decorated functioins which will be turned into nodes. See examples under **PyFlow/FunctionLibraries**.
"""
import os
from inspect import getmembers
from inspect import isfunction

_libs = {}
_foos = {}


def _getFunctions():
    # append from FunctionLibraries
    for lib in os.listdir(os.path.dirname(__file__)):
        if lib.endswith(".py") and "__init__" not in lib:
            libName = lib.split(".")[0]
            try:
                exec('from {0} import {0}'.format(libName))
                exec('lib_class = {0}'.format(libName))
                # Call lib constructor here!!!!
                # create method in base lib class for automatic creation of nodes
                # arrays for example or enums
                foos = [f for f in getmembers(lib_class, isfunction) if "__" not in f[0]]

                _libs[libName] = foos

                for f in _libs[libName]:
                    _foos[f[0]] = f[1]
            except Exception as e:
                # not load lib if any errors or unknown modules etc.
                print e, libName
                pass


## Get registered function library by name
# @param[in] libName library name (string)
# @returns [FunctionLibraryBase](@ref PyFlow.Core.FunctionLibrary.FunctionLibraryBase) dereived class or None
def getLib(libName):
    if libName in _libs:
        return _libs[libName]
    return None


## Get registered library names
# @returns array of names (string)
def libs():
    return _libs.keys()


## Finds function by name
# @details Searches from all refistered libraries.
def findFunctionByName(name):
    if name in _foos:
        return _foos[name]
    return None


_getFunctions()
