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
    "findPinClassByType"
]


__PACKAGES = {}


def INITIALIZE():
    # TODO: Check for duplicated package names
    for importer, modname, ispkg in pkgutil.iter_modules(Packages.__path__):
        if ispkg:
            mod = importer.find_module(modname).load_module(modname)
            __PACKAGES[modname] = getattr(mod, modname)()


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
