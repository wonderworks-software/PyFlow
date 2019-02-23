from __future__ import absolute_import
import importlib
from PyFlow.Packages import *
import pkgutil


__all__ = [
    "INITIALIZE",
    "GET_PACKAGES",
    "GET_PACKAGE_CHECKED",
    "CreateRawPin",
    "getPinDefaultValueByType",
    "findPinClassByType",
    "getRawNodeInstance"
]


__PACKAGES = {}


def GET_PACKAGES():
    return __PACKAGES


def GET_PACKAGE_CHECKED(package_name):
    assert package_name in __PACKAGES
    return __PACKAGES[package_name]


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


def CreateRawPin(name, owningNode, dataType, direction, **kwds):
    pinClass = findPinClassByType(dataType)
    if pinClass is None:
        return None
    inst = pinClass(name, owningNode, dataType, direction, **kwds)
    return inst


def getRawNodeInstance(nodeClassName, packageName=None):
    from PyFlow.Core.NodeBase import NodeBase
    package = GET_PACKAGE_CHECKED(packageName)
    # try find function first
    # TODO: convert functions to nodes on initialization
    for lib in package.GetFunctionLibraries().values():
        foos = lib.getFunctions()
        if nodeClassName in foos:
            return NodeBase.initializeFromFunction(foos[nodeClassName])

    # try find node class
    nodes = package.GetNodeClasses()
    if nodeClassName in nodes:
        return nodes[nodeClassName](nodeClassName)


def getUINodeInstance(raw_instance):
    packageName = raw_instance.packageName()
    print(packageName)
    # TODO: create UI node here and return
    assert(False)
    return None


def INITIALIZE():
    # TODO: Check for duplicated package names
    for importer, modname, ispkg in pkgutil.iter_modules(Packages.__path__):
        if ispkg:
            mod = importer.find_module(modname).load_module(modname)
            package = getattr(mod, modname)()
            __PACKAGES[modname] = package
