"""Common utils working with packags.
"""


import importlib
import pkgutil
import collections
from copy import copy
import os

from PyFlow.Packages import *


__all__ = [
    "INITIALIZE",
    "GET_PACKAGES",
    "GET_PACKAGE_CHECKED",
    "CreateRawPin",
    "getPinDefaultValueByType",
    "findPinClassByType",
    "getRawNodeInstance",
    "getAllPinClasses",
    "getHashableDataTypes",
]


__PACKAGES = {}
__HASHABLE_TYPES = []


def GET_PACKAGES():
    return __PACKAGES


def GET_PACKAGE_CHECKED(package_name):
    assert package_name in __PACKAGES
    return __PACKAGES[package_name]


def getAllPinClasses():
    result = []
    for package in list(__PACKAGES.values()):
        result += list(package.GetPinClasses().values())
    return result


def findPinClassByType(dataType):
    for package_name, package in GET_PACKAGES().items():
        pins = package.GetPinClasses()
        if dataType in pins:
            return pins[dataType]
    return None


def getPinDefaultValueByType(dataType):
    pin = findPinClassByType(dataType)
    if pin:
        return pin.pinDataTypeHint()[1]
    return None


def getHashableDataTypes():
    if len(__HASHABLE_TYPES) == 0:
        for pin in getAllPinClasses():
            t = pin.internalDataStructure()
            if t is not type(None) and t is not None:
                if isinstance(pin.internalDataStructure()(), collections.Hashable):
                    __HASHABLE_TYPES.append(pin.__name__)
    return copy(__HASHABLE_TYPES)


def getPinFromData(data):
    for pin in [pin for pin in getAllPinClasses() if pin.IsValuePin()]:
        pType = pin.internalDataStructure()
        if data == pType:
            return pin


def CreateRawPin(name, owningNode, dataType, direction, **kwds):
    pinClass = findPinClassByType(dataType)
    if pinClass is None:
        return None
    inst = pinClass(name, owningNode, direction, **kwds)
    return inst


def getRawNodeInstance(nodeClassName, packageName=None, libName=None, **kwargs):
    from PyFlow.Core.NodeBase import NodeBase
    package = GET_PACKAGE_CHECKED(packageName)
    # try find function first
    if libName is not None:
        for key, lib in package.GetFunctionLibraries().items():
            foos = lib.getFunctions()
            if libName == key and nodeClassName in foos:
                return NodeBase.initializeFromFunction(foos[nodeClassName])

    # try find node class
    nodes = package.GetNodeClasses()
    if nodeClassName in nodes:
        return nodes[nodeClassName](nodeClassName, **kwargs)


def INITIALIZE(additionalPackageLocations=[]):
    from PyFlow.UI.Tool import REGISTER_TOOL
    from PyFlow.UI.Widgets.InputWidgets import REGISTER_UI_INPUT_WIDGET_PIN_FACTORY
    from PyFlow.UI.Canvas.UINodeBase import REGISTER_UI_NODE_FACTORY
    from PyFlow.UI.Canvas.UIPinBase import REGISTER_UI_PIN_FACTORY
    from PyFlow import ConfigManager

    packagePaths = Packages.__path__

    # check for additional package locations
    if "PYFLOW_PACKAGES_PATHS" in os.environ:
        delim = ';'
        pathsString = os.environ["PYFLOW_PACKAGES_PATHS"]
        # remove delimeters from right
        pathsString = pathsString.rstrip(delim)
        for packagesRoot in pathsString.split(delim):
            if os.path.exists(packagesRoot):
                packagePaths.append(packagesRoot)
    packagePaths.extend(additionalPackageLocations)

    for importer, modname, ispkg in pkgutil.iter_modules(packagePaths):
        if ispkg:
            mod = importer.find_module(modname).load_module(modname)
            package = getattr(mod, modname)()
            __PACKAGES[modname] = package

    registeredInternalPinDataTypes = set()

    for name, package in __PACKAGES.items():
        packageName = package.__class__.__name__
        for node in package.GetNodeClasses().values():
            node._packageName = packageName

        for pin in package.GetPinClasses().values():
            pin._packageName = packageName
            if pin.IsValuePin():
                internalType = pin.internalDataStructure()
                if internalType in registeredInternalPinDataTypes:
                    raise Exception("Pin with {0} internal data type alredy been registered".format(internalType))
                registeredInternalPinDataTypes.add(internalType)

        uiPinsFactory = package.UIPinsFactory()
        if uiPinsFactory is not None:
            REGISTER_UI_PIN_FACTORY(packageName, uiPinsFactory)

        uiPinInputWidgetsFactory = package.PinsInputWidgetFactory()
        if uiPinInputWidgetsFactory is not None:
            REGISTER_UI_INPUT_WIDGET_PIN_FACTORY(packageName, uiPinInputWidgetsFactory)

        uiNodesFactory = package.UINodesFactory()
        if uiNodesFactory is not None:
            REGISTER_UI_NODE_FACTORY(packageName, uiNodesFactory)

        for toolClass in package.GetToolClasses().values():
            REGISTER_TOOL(packageName, toolClass)
    getHashableDataTypes()
