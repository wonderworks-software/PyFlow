from __future__ import absolute_import
import importlib
from .Packages import *
import pkgutil

__all__ = [
    "INITIALIZE",
    "GET_PACKAGES",
    "GET_PINS"
]

__PACKAGES = {}
_PINS = {}


def GET_PINS(PackageName=None):
    if PackageName is None:
        return _PINS

    try:
        return _PINS[PackageName]
    except Exception("Package not found") as e:
        raise e


def REGISTER_PIN_TYPE(PackageName, pinSubclass):
    '''
    pin registration
    '''
    # Create subdict for package if not exists
    if PackageName not in _PINS:
        _PINS[PackageName] = {}

    dType = pinSubclass.pinDataTypeHint()[0]
    if dType not in _PINS[PackageName]:
        _PINS[PackageName][pinSubclass.pinDataTypeHint()[0]] = pinSubclass
    else:
        raise Exception("Error registering pin type {0}\n pin with ID [{1}] already registered".format(pinSubclass.__name__))


def INITIALIZE():
    # Check for duplicated package names
    # ...

    # import packages
    for importer, modname, ispkg in pkgutil.iter_modules(Packages.__path__):
        if ispkg:
            mod = importer.find_module(modname).load_module(modname)
            __PACKAGES[modname] = mod


def GET_PACKAGES():
    return __PACKAGES
