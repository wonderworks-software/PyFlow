from __future__ import absolute_import
import importlib
from .Packages import *
import pkgutil

__all__ = [
    "INITIALIZE",
    "GET_PACKAGES"
]

_PACKAGES = {}

def INITIALIZE():
    # Check for duplicated package names
    # ...

    # import packages
    for importer, modname, ispkg in pkgutil.iter_modules(Packages.__path__):
        if ispkg:
            # package_mod = importlib.import_module(modname)
            mod = importer.find_module(modname).load_module(modname)
            _PACKAGES[modname] = mod


def GET_PACKAGES():
    return _PACKAGES
