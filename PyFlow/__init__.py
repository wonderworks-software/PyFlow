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
    "getRawNodeInstance",
    "getAllPinClasses"
]


__PACKAGES = {}


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
            def packageName():
                return package_name  
            pins[dataType].packageName=staticmethod(packageName)             
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


def getRawNodeInstance(nodeClassName, packageName=None, libName=None):
    from PyFlow.Core.NodeBase import NodeBase
    package = GET_PACKAGE_CHECKED(packageName)
    # try find function first
    for key, lib in package.GetFunctionLibraries().items():
        foos = lib.getFunctions()
        if libName is not None:
            if libName == key and nodeClassName in foos:
                return NodeBase.initializeFromFunction(foos[nodeClassName])

    # try find node class
    nodes = package.GetNodeClasses()
    if nodeClassName in nodes:
        return nodes[nodeClassName](nodeClassName)

def INITIALIZE():
    # TODO: Check for duplicated package names
    for importer, modname, ispkg in pkgutil.iter_modules(Packages.__path__):
        if ispkg:
            mod = importer.find_module(modname).load_module(modname)
            package = getattr(mod, modname)()
            __PACKAGES[modname] = package

    for name,package in __PACKAGES.items():
        for node in package.GetNodeClasses().values():
            nodepackName = name
            def packageName():
                return nodepackName  
            node.packageName=staticmethod(packageName)
            print node.__name__,node.packageName()

    for name2,package2 in __PACKAGES.items():            
        for pin in package.GetPinClasses().values():
            pinpackName = name2
            def packageName():
                return pinpackName  
            pin.packageName=staticmethod(packageName) 
            print pin.__name__,pin.packageName()              