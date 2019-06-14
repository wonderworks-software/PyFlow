"""Common utils working with packags.
"""


import importlib
import pkgutil
import collections
from PyFlow.Packages import *


__all__ = [
    "INITIALIZE",
    "GET_PACKAGES",
    "GET_PACKAGE_CHECKED",
    "CreateRawPin",
    "getPinDefaultValueByType",
    "findPinClassByType",
    "getRawNodeInstance",
    "getAllPinClasses"
]


__PACKAGES = {}

_HASHABLES = []

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
    validKeyTypes = []
    for pin in getAllPinClasses():
        t = pin.internalDataStructure()
        if t != type(None) and t != None:
            if isinstance(pin.internalDataStructure()(),collections.Hashable):
                validKeyTypes.append(pin.__name__)
    return validKeyTypes

def CreateRawPin(name, owningNode, dataType, direction, **kwds):
    pinClass = findPinClassByType(dataType)
    if pinClass is None:
        return None
    inst = pinClass(name, owningNode, direction, **kwds)
    owningNode.pins.add(inst)
    owningNode.pinsCreationOrder[inst.uid] = inst
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


def INITIALIZE():
    from PyFlow.UI.Tool import REGISTER_TOOL
    from PyFlow.UI.Widgets.InputWidgets import REGISTER_UI_INPUT_WIDGET_PIN_FACTORY
    from PyFlow.UI.Canvas.UINodeBase import REGISTER_UI_NODE_FACTORY
    from PyFlow.UI.Canvas.UIPinBase import REGISTER_UI_PIN_FACTORY

    for importer, modname, ispkg in pkgutil.iter_modules(Packages.__path__):
        if ispkg:
            mod = importer.find_module(modname).load_module(modname)
            package = getattr(mod, modname)()
            __PACKAGES[modname] = package

    for name, package in __PACKAGES.items():
        packageName = package.__class__.__name__
        for node in package.GetNodeClasses().values():
            node._packageName = packageName

        for pin in package.GetPinClasses().values():
            pin._packageName = packageName

        uiPinsFactory = package.UIPinsFactory()
        REGISTER_UI_PIN_FACTORY(packageName, uiPinsFactory)

        uiPinInputWidgetsFactory = package.PinsInputWidgetFactory()
        REGISTER_UI_INPUT_WIDGET_PIN_FACTORY(packageName, uiPinInputWidgetsFactory)

        uiNodesFactory = package.UINodesFactory()
        REGISTER_UI_NODE_FACTORY(packageName, uiNodesFactory)

        for toolClass in package.GetToolClasses().values():
            REGISTER_TOOL(packageName, toolClass)
    _HASHABLES.extend(getHashableDataTypes())
